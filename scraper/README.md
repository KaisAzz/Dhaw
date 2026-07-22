# Dhaw — Scraper des coupures STEG

Pipeline d'acquisition de données réelles pour l'app Dhaw (carte des coupures
d'électricité en Tunisie).

## Pourquoi la presse et pas la STEG directement ?

La STEG **ne publie pas** ses avis de délestage/coupures sur une page
structurée de steg.com.tn : ils sortent d'abord sur sa **page Facebook
officielle** (souvent en images), puis sont retranscrits en texte par la
presse (Webdo, La Presse, Tunisie Numérique…) qui expose des **flux RSS
ouverts**. Scraper Facebook viole ses CGU et est fragile ; scraper la presse
via RSS est légal, stable et suffisant.

## Architecture

```
RSS (Webdo, La Presse, TN, DirectInfo)          toutes les 15 min (cron)
        │  filtre mots-clés : steg | délestage | coupure électricité/courant
        ▼
Téléchargement article ──► nettoyage HTML
        ▼
Extraction :
  • zones        → matching gazetteer (zones_tn.py, ~250 entrées, extensible)
  • gouvernorat  → via gazetteer + motif « gouvernorat de X »
  • fenêtre      → regex « entre 10h00 et 17h00 » / « de 8h à 12h »
  • date         → « lundi 20 juillet 2026 », « demain » + date de publication
  • type         → delestage | planifiee | annonce
        ▼
outages.json  (dédupliqué, 14 jours glissants)
        ▼
App Dhaw : fetch('outages.json') → marqueurs + choropleth
```

## Fichiers

- `steg_scraper.py` — pipeline complet (réseau) + mode `--test` hors-ligne
- `zones_tn.py` — gazetteer zone→gouvernorat (LA pièce à enrichir en continu)
- `ocr_fb.py` — fallback OCR (fra+ara) des captures Facebook STEG quand
  l'article ne contient pas la liste en texte
- `geocode.py` — géocodage fin zone→lat/lng via Nominatim/OSM (cache local,
  rate-limit 1 req/s, validation par distance au gouvernorat, fallback
  centroïde) + mode `--test`
- `fixtures/webdo_20260720.txt` — article réel de test (délestage du 20/07/2026)
- `outages.sample.json` — sortie générée par le test (143 zones extraites)

## Usage

```bash
pip install requests pillow pytesseract
sudo apt install tesseract-ocr tesseract-ocr-fra tesseract-ocr-ara  # pour l'OCR

python3 steg_scraper.py --test    # test hors-ligne sur la fixture
python3 geocode.py --test         # test hors-ligne du géocodeur

python3 steg_scraper.py           # run réel (produit outages.json)
python3 geocode.py                # enrichit outages.json avec lat/lng
```

Cron (VPS) :
```
*/15 * * * * cd /opt/dhaw/scraper && python3 steg_scraper.py && python3 geocode.py >> scraper.log 2>&1
```

## Intégration app

L'app Dhaw (`dhaw.html`) tente `fetch('outages.json')` au chargement puis
toutes les 5 min : si le fichier existe (servi par le même serveur web), elle
bascule en **mode données réelles** (badge vert « 📡 DONNÉES STEG/PRESSE »,
simulation désactivée, lien source presse dans les popups). Sinon elle reste
en mode démo. Les événements géocodés `precision: "zone"` sont placés au
point exact ; les autres au centroïde du gouvernorat (mention « position
approximative »).

## Schéma de sortie

```json
{
 "generated_at": "2026-07-22T14:30:00+01:00",
 "events": [
  {
   "id": "a3f9c1e2b4d5f6a7-0",
   "type": "delestage",            // delestage | planifiee | annonce
   "date": "2026-07-20",
   "window": "10:00 – 17:00",
   "gov": "Ben Arous",
   "zone": "Fouchana",
   "source": "https://www.webdo.tn/...",
   "title": "Coupures d'électricité : Les régions concernées...",
   "scraped_at": "2026-07-22T14:30:00+01:00"
  }
 ]
}
```

## Limites connues & évolutions

1. **Doublons de matching** (« Ariana » + « L Ariana ») : filtrage simple à
   ajouter côté app ou en post-traitement.
2. ~~Articles en images~~ → fait : `ocr_fb.py` (nécessite tesseract installé).
3. ~~Géocodage fin~~ → fait : `geocode.py`.
4. **Temps réel citoyen** : le scraping couvre l'officiel ; le vrai « temps
   réel » viendra des signalements citoyens de l'app (déjà maquettés) — il
   faudra un petit backend (API + base) pour les stocker.
5. **Sources additionnelles** : Mosaïque FM, Shems FM, TAP ; page FB STEG via
   accord officiel (open data / API partenaire — la STEG a une Cellule
   d'accès à l'information, base légale : loi 22-2016 sur l'accès à l'info).

## Éthique / légal

- User-Agent identifié (`DhawBot`) + contact, cadence raisonnable (15 min),
  respect des robots.txt.
- On ne republie que des **faits** (zones/horaires annoncés par la STEG),
  avec **lien source** vers l'article — pas de copie du contenu éditorial.
