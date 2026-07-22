# -*- coding: utf-8 -*-
"""
Dhaw — Fallback OCR : quand un article ne contient que les captures d'écran
Facebook de la STEG (images scontent.*.fbcdn.net), on les télécharge et on
extrait le texte en français + arabe avec Tesseract.

Prérequis (serveur) :
  sudo apt install tesseract-ocr tesseract-ocr-fra tesseract-ocr-ara
  pip install pytesseract pillow requests
"""

import re
from io import BytesIO

UA = {"User-Agent": "DhawBot/0.1 (+https://dhaw.tn ; contact@dhaw.tn)"}

# URLs d'images du CDN Facebook présentes dans le HTML de l'article
RE_FB_IMG = re.compile(
    r"https://scontent[^\"'\s>\)]+?fbcdn\.net[^\"'\s>\)]+", re.I)

def extract_fb_image_urls(raw_html: str, max_n: int = 10):
    """Retourne les URLs d'images FB uniques trouvées dans l'article."""
    seen, urls = set(), []
    for m in RE_FB_IMG.finditer(raw_html):
        u = m.group(0).replace("&amp;", "&")
        # clé de dédup : le nom de fichier (les URLs varient par leurs tokens)
        key = u.split("?")[0].rsplit("/", 1)[-1]
        if key not in seen:
            seen.add(key)
            urls.append(u)
    return urls[:max_n]

def preprocess(img):
    """Améliore l'OCR : niveaux de gris + agrandissement + seuillage doux."""
    from PIL import Image, ImageOps
    img = ImageOps.grayscale(img)
    w, h = img.size
    if w < 1200:                       # les captures FB sont souvent petites
        img = img.resize((w * 2, h * 2), Image.LANCZOS)
    return ImageOps.autocontrast(img)

def ocr_images(urls, langs: str = "fra+ara"):
    """Télécharge et OCRise chaque image. -> texte concaténé."""
    import requests, pytesseract
    from PIL import Image
    chunks = []
    for u in urls:
        try:
            r = requests.get(u, headers=UA, timeout=30)
            r.raise_for_status()
            img = preprocess(Image.open(BytesIO(r.content)))
            txt = pytesseract.image_to_string(img, lang=langs)
            if txt.strip():
                chunks.append(txt)
        except Exception as exc:
            print(f"[warn] OCR impossible {u[:60]}…: {exc}")
    return "\n".join(chunks)

def ocr_fallback(raw_html: str, min_zones_found: int, zones_found: int):
    """Appelé par steg_scraper : OCR seulement si le texte de l'article n'a
    presque rien donné ET que des images FB sont présentes."""
    if zones_found >= min_zones_found:
        return ""
    urls = extract_fb_image_urls(raw_html)
    if not urls:
        return ""
    print(f"[ocr] {len(urls)} image(s) Facebook -> OCR fra+ara…")
    return ocr_images(urls)
