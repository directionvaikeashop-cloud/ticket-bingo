# -*- coding: utf-8 -*-
"""
generate_flash_quines.py
Module de génération de tickets FLASH QUINES ALLONGER — Ticket Bingo (TUKEA)

Ticket horizontal allongé (bandeau) :
  - en-tête : "PAPEETE" + "FLASH QUINES ALLONGER by TUKEA 89 22 23 05"
  - 9 numéros, un par dizaine (1-9, 10-19, ... 80-90), dans des bulles arrondies
    en ZIGZAG (haut / bas), avec des croix X décoratives entre les bulles.
  - n° de série en bas à droite.
9 numéros au total. 1 page = 1 ticket. Tickets uniques.
Chiffres NOIRS, encadrement COULEUR (arc-en-ciel par ticket), coins arrondis.

Usage:
    from generate_flash_quines import generate_pdf
    path = generate_pdf(nb_tickets=500, serie_start=1, output_path="/data/FLASH_QUINES.pdf")
"""
import random
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

try:
    pdfmetrics.registerFont(TTFont('DJL', '/usr/share/fonts/truetype/dejavu/DejaVuSans-ExtraLight.ttf'))
    POLICE = 'DJL'
except Exception:
    POLICE = 'Helvetica'

GRIS = colors.Color(0.42, 0.42, 0.42)
GRIS_CLAIR = colors.Color(0.80, 0.80, 0.80)

RAINBOW = [
    colors.HexColor('#E53935'), colors.HexColor('#FB8C00'), colors.HexColor('#F9A825'),
    colors.HexColor('#43A047'), colors.HexColor('#00ACC1'), colors.HexColor('#1E88E5'),
    colors.HexColor('#3949AB'), colors.HexColor('#8E24AA'), colors.HexColor('#D81B60'),
    colors.HexColor('#6D4C41'),
]

# 9 dizaines (loto 90)
DECADES = [(1, 9)] + [(d, d + 9) for d in range(10, 80, 10)] + [(80, 90)]

CARD_W = 252 * mm
CARD_H = 44 * mm
MARGIN = 5 * mm
HEAD_H = 9 * mm
PAGE_W = CARD_W + 2 * MARGIN
PAGE_H = CARD_H + 2 * MARGIN


def _gen_nums(rng):
    """1 numéro par dizaine (9 au total)."""
    return [rng.randint(a, b) for (a, b) in DECADES]


def _signature(nums):
    return tuple(nums)


def _draw_ticket(cv, serial, nums, accent, couleur=True):
    bord = accent if couleur else GRIS_CLAIR
    x0, y0 = MARGIN, MARGIN

    # cadre extérieur arrondi (couleur)
    cv.setStrokeColor(bord)
    cv.setLineWidth(2.0)
    cv.roundRect(x0, y0, CARD_W, CARD_H, 5 * mm, stroke=1, fill=0)

    grid_top = y0 + CARD_H - HEAD_H

    # en-tête : PAPEETE (boîte gauche) + titre
    cv.setStrokeColor(GRIS_CLAIR)
    cv.setLineWidth(0.6)
    cv.line(x0 + 3 * mm, grid_top, x0 + CARD_W - 3 * mm, grid_top)
    cv.line(x0 + 33 * mm, grid_top, x0 + 33 * mm, y0 + CARD_H - 2 * mm)
    cv.setFillColor(bord)
    cv.setFont(POLICE, 11)
    cv.drawCentredString(x0 + 18 * mm, grid_top + (HEAD_H - 11) / 2, "PAPEETE")
    cv.setFont(POLICE, 11)
    cv.drawCentredString(x0 + 33 * mm + (CARD_W - 36 * mm) / 2, grid_top + (HEAD_H - 11) / 2,
                         "FLASH QUINES ALLONGER by TUKEA 89 22 23 05")

    # zone des bulles (sous l'en-tête)
    zone_top = grid_top - 1 * mm
    zone_bot = y0 + 2 * mm
    slot_w = (CARD_W - 6 * mm) / 9
    bx0 = x0 + 3 * mm
    y_haut = zone_top - (zone_top - zone_bot) * 0.30
    y_bas = zone_bot + (zone_top - zone_bot) * 0.30

    # bulles + numéros (zigzag : pair = haut, impair = bas), GROS chiffres NOIRS
    bw, bh = slot_w * 0.84, 16 * mm
    for k, val in enumerate(nums):
        cxb = bx0 + (k + 0.5) * slot_w
        cyb = y_haut if k % 2 == 0 else y_bas
        cv.setStrokeColor(bord)
        cv.setLineWidth(1.4)
        cv.setFillColor(colors.white)
        cv.roundRect(cxb - bw / 2, cyb - bh / 2, bw, bh, 3 * mm, stroke=1, fill=1)
        cv.setFillColor(colors.black)
        cv.setFont(POLICE, 38)
        cv.drawCentredString(cxb, cyb - 13, str(val))

    # n° de série en bas à droite
    cv.setFillColor(bord)
    cv.setFont(POLICE, 9)
    cv.drawRightString(x0 + CARD_W - 5 * mm, y0 + 2.5 * mm, "%06d" % serial)


def generate_pdf(nb_tickets=500, serie_start=1, output_path="/data/FLASH_QUINES.pdf", couleur=True):
    """Génère nb_tickets tickets FLASH QUINES ALLONGER uniques. couleur=False => Noir & Blanc."""
    nb_tickets = max(1, min(int(nb_tickets), 1000))
    serie_start = max(1, int(serie_start))
    rng = random.Random(755000 + serie_start)
    vus = set()
    cv = canvas.Canvas(output_path, pagesize=(PAGE_W, PAGE_H))
    produits = 0
    while produits < nb_tickets:
        nums = _gen_nums(rng)
        sig = _signature(nums)
        if sig in vus:
            continue
        vus.add(sig)
        serial = serie_start + produits
        _draw_ticket(cv, serial, nums, RAINBOW[(serial - 1) % len(RAINBOW)], couleur)
        cv.showPage()
        produits += 1
    cv.save()
    return output_path


def generate_pdf_nb(nb_tickets=500, serie_start=1, output_path="/data/FLASH_QUINES_NB.pdf"):
    """Version Noir & Blanc (économe en encre)."""
    return generate_pdf(nb_tickets, serie_start, output_path, couleur=False)


if __name__ == "__main__":
    generate_pdf(nb_tickets=4, serie_start=1, output_path="flash_quines_test.pdf")
    print("FLASH QUINES ALLONGER généré")
