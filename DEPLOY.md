# Déployer Dhaw gratuitement (GitHub Pages + Actions)

Coût : **0 DT**. Pas de serveur. Le site est hébergé par GitHub Pages et le
scraper tourne automatiquement toutes les 30 minutes via GitHub Actions.

## Étape 1 — Créer le dépôt

1. Crée un compte sur [github.com](https://github.com) si tu n'en as pas.
2. Nouveau dépôt : **github.com/new** → nom `dhaw` → **Public** → Create.

## Étape 2 — Pousser les fichiers

Option A (ligne de commande, recommandé) :
```bash
cd dossier-dhaw          # le contenu de ce zip
git init
git add .
git commit -m "Dhaw v1"
git branch -M main
git remote add origin https://github.com/TON_PSEUDO/dhaw.git
git push -u origin main
```

Option B (sans installer git) : sur la page du dépôt → « uploading an
existing file » → glisser-déposer tout le contenu du zip (y compris le
dossier `.github` — sur Windows, active l'affichage des fichiers cachés).

## Étape 3 — Activer GitHub Pages

Dépôt → **Settings** → **Pages** → Source : `Deploy from a branch` →
Branch : `main` / `(root)` → **Save**.

Après ~1 min, le site est en ligne :
`https://TON_PSEUDO.github.io/dhaw/`

## Étape 4 — Activer le scraper automatique

1. Dépôt → onglet **Actions** → si demandé, clique « I understand… enable ».
2. Workflow « Scraper STEG → outages.json » → **Run workflow** (premier run
   manuel pour tester).
3. Ensuite il tourne seul toutes les 30 min : il scrape la presse, géocode
   les zones, et commit `outages.json` → le site bascule automatiquement en
   mode « 📡 DONNÉES STEG/PRESSE ».

## Vérifications

- `https://TON_PSEUDO.github.io/dhaw/outages.json` doit répondre.
- Sur le site, le badge en haut doit passer de « 🧪 MODE DÉMO » à
  « 📡 DONNÉES STEG/PRESSE · MAJ hh:mm » (si des événements de moins de
  14 jours existent).
- La géolocalisation utilisateur fonctionne car GitHub Pages est en HTTPS. ✔

## Limites du gratuit (et quand migrer)

| Besoin | GitHub Pages | Quand ça coince |
|---|---|---|
| Site statique + carte | ✔ illimité (100 Go/mois) | jamais pour un début |
| Scraper cron | ✔ Actions (2000 min/mois, ce workflow ≈ 300 min/mois) | OK |
| Signalements citoyens | ✘ pas de backend | dès qu'on veut les stocker |

Pour les signalements citoyens (étape suivante), il faudra un petit backend
gratuit : **Supabase** (Postgres + API REST gratuite) ou **Cloudflare
Workers + D1** — l'app enverra un POST au lieu de garder le signalement en
mémoire. On peut le brancher sans toucher à l'hébergement Pages.

## Nom de domaine (optionnel)

`dhaw.tn` s'achète chez un registrar .tn (ATI ou revendeurs). Dans
Settings → Pages → Custom domain, pointer un CNAME vers
`TON_PSEUDO.github.io`.
