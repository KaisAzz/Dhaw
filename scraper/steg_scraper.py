# -*- coding: utf-8 -*-
"""
Dhaw — Scraper des annonces de coupures STEG via la presse tunisienne.

Pipeline :
  1. Poll des flux RSS (Webdo, La Presse, Tunisie Numérique, Direct Info)
  2. Filtre par mots-clés (STEG / délestage / coupure électricité)
  3. Téléchargement + nettoyage de l'article
  4. Extraction : date, fenêtre horaire, zones (matching gazetteer)
  5. Sortie : outages.json (schéma compatible avec l'app Dhaw)

Usage :
  pip install requests
  python steg_scraper.py            # run complet (réseau)
  python steg_scraper.py --test     # test hors-ligne sur les fixtures

À planifier en cron toutes les 15 min :
  */15 * * * * cd /opt/dhaw/scraper && python3 steg_scraper.py >> scraper.log 2>&1
"""

import json, re, sys, hashlib, unicodedata, html
from datetime import datetime, timedelta, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

from zones_tn import GAZETTEER, GOVERNORATS

BASE = Path(__file__).parent
OUT_FILE = BASE / "outages.json"
SEEN_FILE = BASE / "seen.json"

FEEDS = [
    "https://www.webdo.tn/fr/rss",
    "https://www.lapresse.tn/feed/",
    "https://www.tunisienumerique.com/feed/",
    "https://directinfo.webmanagercenter.com/feed/",
]

KEYWORDS = re.compile(
    r"(steg|d[ée]lestage|coupure[sz]?\s+(?:de\s+)?(?:d.)?[ée]lectricit|"
    r"coupure[sz]?\s+(?:de\s+)?courant|قطع.{0,12}كهرباء)", re.I)

UA = {"User-Agent": "DhawBot/0.1 (+https://dhaw.tn ; contact@dhaw.tn) veille coupures"}
TUNIS_TZ = timezone(timedelta(hours=1))

# ---------------------------------------------------------------- utils ----
def normalize(s: str) -> str:
    """minuscules, sans accents, séparateurs unifiés."""
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[’'`\-_/.,;:!?()«»\"…–—]", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()

def strip_html(raw: str) -> str:
    raw = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
    raw = re.sub(r"<[^>]+>", " ", raw)
    return re.sub(r"\s+", " ", html.unescape(raw))

def article_id(url: str) -> str:
    return hashlib.sha1(url.encode()).hexdigest()[:16]

# ------------------------------------------------------------ extraction ----
GOV_NORM = {normalize(g): g for g in GOVERNORATS}

RE_WINDOW = re.compile(
    r"entre\s+(\d{1,2})\s*h\s*(\d{2})?\s+et\s+(\d{1,2})\s*h\s*(\d{2})?"
    r"|de\s+(\d{1,2})\s*h\s*(\d{2})?\s+[àa]\s+(\d{1,2})\s*h\s*(\d{2})?", re.I)

MOIS = {m: i + 1 for i, m in enumerate(
    ["janvier","fevrier","mars","avril","mai","juin","juillet",
     "aout","septembre","octobre","novembre","decembre"])}
RE_DATE = re.compile(
    r"(lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche)?\s*"
    r"(\d{1,2})(?:er)?\s+(janvier|f[ée]vrier|mars|avril|mai|juin|juillet|"
    r"ao[ûu]t|septembre|octobre|novembre|d[ée]cembre)\s*(\d{4})?", re.I)

def extract_window(text: str):
    m = RE_WINDOW.search(text)
    if not m:
        return None
    g = m.groups()
    if g[0] is not None:
        h1, m1, h2, m2 = g[0], g[1] or "00", g[2], g[3] or "00"
    else:
        h1, m1, h2, m2 = g[4], g[5] or "00", g[6], g[7] or "00"
    return f"{int(h1):02d}:{m1} – {int(h2):02d}:{m2}"

def extract_date(text: str, pub_date: datetime):
    norm = normalize(text)
    if "demain" in norm:
        return (pub_date + timedelta(days=1)).strftime("%Y-%m-%d")
    m = RE_DATE.search(text)
    if m:
        day = int(m.group(2))
        month = MOIS.get(normalize(m.group(3)), pub_date.month)
        year = int(m.group(4)) if m.group(4) else pub_date.year
        try:
            return datetime(year, month, day).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return pub_date.strftime("%Y-%m-%d")

def extract_zones(text: str):
    """Retourne [(zone_affichable, gouvernorat), ...] via le gazetteer.
    Matching par fenêtre glissante de 1 à 4 mots normalisés."""
    norm_text = normalize(text)
    words = norm_text.split()
    found, seen = [], set()
    for i in range(len(words)):
        for size in (4, 3, 2, 1):
            cand = " ".join(words[i:i + size])
            if cand in GAZETTEER and cand not in seen:
                seen.add(cand)
                found.append((cand.title(), GAZETTEER[cand]))
                break
    # gouvernorats cités directement ("gouvernorat de X")
    for m in re.finditer(r"gouvernorats?\s+d[eu]\s*(?:l[a']?\s*)?(\w[\w\s']{2,20}?)[,.;]",
                         norm_text):
        g = GOV_NORM.get(m.group(1).strip())
        if g and g not in {gv for _, gv in found}:
            found.append((g, g))
    return found

def classify(title: str, text: str) -> str:
    n = normalize(title + " " + text[:400])
    if "delestage" in n or "tournante" in n or "canicule" in n:
        return "delestage"        # coupures tournantes non planifiées précisément
    if "programmee" in n or "maintenance" in n or "entretien" in n or "travaux" in n:
        return "planifiee"
    return "annonce"

def parse_article(title: str, text: str, url: str, pub_date: datetime):
    zones = extract_zones(text)
    if not zones:
        return []
    window = extract_window(text) or "horaire non précisé"
    date = extract_date(text, pub_date)
    kind = classify(title, text)
    return [{
        "id": article_id(url) + f"-{i}",
        "type": kind,
        "date": date,
        "window": window,
        "gov": gov,
        "zone": zone,
        "source": url,
        "title": title.strip(),
        "scraped_at": datetime.now(TUNIS_TZ).isoformat(timespec="seconds"),
    } for i, (zone, gov) in enumerate(zones)]

# ------------------------------------------------------------- réseau ------
def fetch(url: str) -> str:
    import requests
    r = requests.get(url, headers=UA, timeout=20)
    r.raise_for_status()
    return r.text

def parse_rss(xml_text: str):
    """-> [(title, link, pub_date), ...]"""
    items = []
    root = ET.fromstring(xml_text)
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub = item.findtext("pubDate") or ""
        try:
            dt = datetime.strptime(pub[:25].strip(), "%a, %d %b %Y %H:%M:%S")
        except ValueError:
            dt = datetime.now()
        items.append((title, link, dt))
    return items

def run():
    seen = json.loads(SEEN_FILE.read_text()) if SEEN_FILE.exists() else {}
    existing = (json.loads(OUT_FILE.read_text())["events"]
                if OUT_FILE.exists() else [])
    events = {e["id"]: e for e in existing}
    new_count = 0

    for feed in FEEDS:
        try:
            rss = fetch(feed)
        except Exception as exc:
            print(f"[warn] flux inaccessible {feed}: {exc}")
            continue
        for title, link, pub in parse_rss(rss):
            if not KEYWORDS.search(title):
                continue
            aid = article_id(link)
            if aid in seen:
                continue
            try:
                raw = fetch(link)
                text = strip_html(raw)
            except Exception as exc:
                print(f"[warn] article inaccessible {link}: {exc}")
                continue
            evs = parse_article(title, text, link, pub)
            # Fallback OCR : article quasi vide mais captures FB présentes
            try:
                from ocr_fb import ocr_fallback
                extra = ocr_fallback(raw, min_zones_found=5,
                                     zones_found=len(evs))
                if extra:
                    evs = parse_article(title, text + "\n" + extra, link, pub)
            except ImportError:
                pass  # pytesseract non installé : on continue sans OCR
            for ev in evs:
                if ev["id"] not in events:
                    events[ev["id"]] = ev
                    new_count += 1
            seen[aid] = datetime.now().isoformat()
            print(f"[ok] {title}")

    # purge : garder 14 jours glissants
    cutoff = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")
    events = {k: v for k, v in events.items() if v["date"] >= cutoff}

    OUT_FILE.write_text(json.dumps(
        {"generated_at": datetime.now(TUNIS_TZ).isoformat(timespec="seconds"),
         "events": sorted(events.values(), key=lambda e: e["date"], reverse=True)},
        ensure_ascii=False, indent=1))
    SEEN_FILE.write_text(json.dumps(seen))
    print(f"\n{new_count} nouveaux événements — total {len(events)} -> {OUT_FILE.name}")

# ---------------------------------------------------------------- test -----
def run_test():
    fixture = (BASE / "fixtures" / "webdo_20260720.txt").read_text(encoding="utf-8")
    events = parse_article(
        "Coupures d’électricité : Les régions concernées ce lundi par le plan "
        "de délestage de la STEG",
        fixture,
        "https://www.webdo.tn/fr/actualite/national/exemple/401328/",
        datetime(2026, 7, 20, 11, 15),
    )
    print(f"{len(events)} zones extraites\n")
    by_gov = {}
    for e in events:
        by_gov.setdefault(e["gov"], []).append(e["zone"])
    for gov, zones in sorted(by_gov.items()):
        print(f"  {gov:<12} : {', '.join(zones)}")
    print(f"\nFenêtre : {events[0]['window']} | Date : {events[0]['date']} | "
          f"Type : {events[0]['type']}")
    (BASE / "outages.sample.json").write_text(json.dumps(
        {"generated_at": datetime.now(TUNIS_TZ).isoformat(timespec="seconds"),
         "events": events}, ensure_ascii=False, indent=1))
    print("-> outages.sample.json écrit")

if __name__ == "__main__":
    run_test() if "--test" in sys.argv else run()
