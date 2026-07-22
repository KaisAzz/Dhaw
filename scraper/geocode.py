# -*- coding: utf-8 -*-
"""
Dhaw — Géocodage fin des zones : zone -> (lat, lng) via Nominatim/OSM.

- Cache local (geocache.json) : chaque zone n'est géocodée qu'une fois.
- Rate-limit 1.1 s/requête (politique d'usage Nominatim).
- Validation : le point doit rester à moins de MAX_KM du centroïde du
  gouvernorat annoncé, sinon on rejette (homonymes hors zone).
- Fallback : centroïde du gouvernorat (précision 'gouvernorat').

Usage :
  python3 geocode.py                 # enrichit outages.json en place
  python3 geocode.py --test          # test hors-ligne (mock)

À lancer après steg_scraper.py dans le cron :
  */15 * * * * cd /opt/dhaw/scraper && python3 steg_scraper.py && python3 geocode.py
"""

import json, sys, time, math, random
from pathlib import Path

BASE = Path(__file__).parent
OUT_FILE = BASE / "outages.json"
CACHE_FILE = BASE / "geocache.json"

UA = {"User-Agent": "DhawBot/0.1 (+https://dhaw.tn ; contact@dhaw.tn)"}
NOMINATIM = "https://nominatim.openstreetmap.org/search"
MAX_KM = 120  # tolérance zone <-> centroïde du gouvernorat annoncé

# Centroïdes des 24 gouvernorats (calculés depuis geoBoundaries ADM1)
GOV_CENTROIDS = {
    "Tunis": [36.8174, 10.2075], "Ben Arous": [36.6614, 10.2489],
    "El Kef": [36.0479, 8.7189], "Sousse": [35.8190, 10.4263],
    "Sfax": [34.6282, 10.3500], "Jendouba": [36.6470, 8.6767],
    "Kairouan": [35.6502, 9.8404], "Kasserine": [35.3339, 8.7700],
    "Mahdia": [35.3849, 10.6727], "Manouba": [36.7819, 9.8911],
    "Sidi Bouzid": [34.8683, 9.5238], "Kébili": [33.3383, 9.3750],
    "Béja": [36.7117, 9.2911], "Tataouine": [32.3468, 10.2866],
    "Gabès": [33.7937, 9.8806], "Bizerte": [37.1067, 9.7372],
    "Ariana": [36.9488, 10.1222], "Nabeul": [36.7428, 10.7104],
    "Monastir": [35.5836, 10.7700], "Siliana": [36.0329, 9.2949],
    "Zaghouan": [36.3051, 10.0189], "Gafsa": [34.4347, 8.8173],
    "Médenine": [33.2648, 10.7978], "Tozeur": [34.1413, 8.0240],
}

def haversine_km(a, b):
    lat1, lon1, lat2, lon2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = (math.sin((lat2 - lat1) / 2) ** 2 +
         math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2)
    return 6371 * 2 * math.asin(math.sqrt(h))

def nominatim_lookup(zone: str, gov: str):
    """-> [lat, lng] ou None. 1 requête, bornée à la Tunisie."""
    import requests
    params = {"q": f"{zone}, {gov}, Tunisia", "format": "json",
              "limit": 1, "countrycodes": "tn"}
    r = requests.get(NOMINATIM, params=params, headers=UA, timeout=20)
    r.raise_for_status()
    res = r.json()
    if not res:  # retry sans le gouvernorat (orthographes divergentes)
        time.sleep(1.1)
        params["q"] = f"{zone}, Tunisia"
        r = requests.get(NOMINATIM, params=params, headers=UA, timeout=20)
        res = r.json()
    if res:
        return [float(res[0]["lat"]), float(res[0]["lon"])]
    return None

def geocode_zone(zone: str, gov: str, cache: dict, lookup=nominatim_lookup):
    """-> (lat, lng, precision). precision: 'zone' | 'gouvernorat'."""
    key = f"{zone}|{gov}"
    if key in cache:
        c = cache[key]
        return c["lat"], c["lng"], c["precision"]

    center = GOV_CENTROIDS.get(gov)
    pt, precision = None, "gouvernorat"
    try:
        pt = lookup(zone, gov)
        time.sleep(1.1)  # politique Nominatim : max ~1 req/s
    except Exception as exc:
        print(f"[warn] geocode '{zone}': {exc}")

    if pt and center and haversine_km(pt, center) <= MAX_KM:
        precision = "zone"
    elif center:
        # fallback : centroïde du gouvernorat, léger jitter pour éviter
        # l'empilement des marqueurs
        pt = [center[0] + random.uniform(-.08, .08),
              center[1] + random.uniform(-.08, .08)]
    else:
        pt = [34.1, 9.4]  # centre Tunisie (ne devrait jamais arriver)

    cache[key] = {"lat": round(pt[0], 5), "lng": round(pt[1], 5),
                  "precision": precision}
    return cache[key]["lat"], cache[key]["lng"], precision

def enrich(lookup=nominatim_lookup):
    if not OUT_FILE.exists():
        print("outages.json introuvable — lancer d'abord steg_scraper.py")
        return
    data = json.loads(OUT_FILE.read_text(encoding="utf-8"))
    cache = (json.loads(CACHE_FILE.read_text(encoding="utf-8"))
             if CACHE_FILE.exists() else {})
    todo = [e for e in data["events"] if "lat" not in e]
    print(f"{len(todo)} événements à géocoder "
          f"({len(cache)} zones déjà en cache)")
    for i, ev in enumerate(todo):
        lat, lng, prec = geocode_zone(ev["zone"], ev["gov"], cache, lookup)
        ev["lat"], ev["lng"], ev["geo_precision"] = lat, lng, prec
        if (i + 1) % 20 == 0:  # sauvegarde incrémentale
            CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False))
    CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False, indent=1))
    OUT_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=1))
    done = sum(1 for e in data["events"] if e.get("geo_precision") == "zone")
    print(f"OK — {done}/{len(data['events'])} événements géocodés à la zone, "
          f"le reste au centroïde du gouvernorat")

# ---------------------------------------------------------------- test -----
def run_test():
    MOCK = {  # simule Nominatim pour test hors-ligne
        "Fouchana": [36.6994, 10.1665],       # bon (Ben Arous)
        "Kelibia": [36.8475, 11.0939],        # bon (Nabeul)
        "La Marsa": [36.8764, 10.3253],       # bon (Tunis)
        "Douz": [33.4664, 9.0203],            # bon (Kébili)
        "Medina": [36.7994, 10.1706],         # homonyme OK
        "Ghraba": [48.85, 2.35],              # aberrant -> doit être rejeté
    }
    def mock_lookup(zone, gov):
        return MOCK.get(zone)
    cache = {}
    tests = [("Fouchana", "Ben Arous"), ("Kelibia", "Nabeul"),
             ("La Marsa", "Tunis"), ("Douz", "Kébili"),
             ("Ghraba", "Sfax"), ("Zone Inconnue Xyz", "Gafsa")]
    for zone, gov in tests:
        lat, lng, prec = geocode_zone(zone, gov, cache, mock_lookup)
        print(f"  {zone:<18} ({gov:<10}) -> {lat:.4f},{lng:.4f}  [{prec}]")
    # vérifs
    assert cache["Fouchana|Ben Arous"]["precision"] == "zone"
    assert cache["Ghraba|Sfax"]["precision"] == "gouvernorat"      # rejeté
    assert cache["Zone Inconnue Xyz|Gafsa"]["precision"] == "gouvernorat"
    print("\nTous les tests passent ✔")

if __name__ == "__main__":
    run_test() if "--test" in sys.argv else enrich()
