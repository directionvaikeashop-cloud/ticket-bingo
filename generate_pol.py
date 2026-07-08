# -*- coding: utf-8 -*-
"""
generate_pol.py
Module de génération de tickets POL (6 boules) — Ticket Bingo (TUKEA)

Grille 3×3, colonnes 30-40 / 41-50 / 51-60.
2 cases barrées (X) : haut-gauche et bas-droite. Case centrale = numéro de série.
  - col0 (30-40) : 2 numéros (rangées milieu & bas)   ; X en haut
  - col1 (41-50) : 2 numéros (rangées haut & bas)     ; SÉRIE au milieu
  - col2 (51-60) : 2 numéros (rangées haut & milieu)  ; X en bas
6 numéros au total. 1 page = 1 ticket. Tickets uniques.
Chiffres NOIRS, encadrement COULEUR (arc-en-ciel par ticket), coins arrondis.

Usage:
    from generate_pol import generate_pdf
    path = generate_pdf(nb_tickets=500, serie_start=1, output_path="/data/POL.pdf")
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

CELL = 36 * mm
HEAD_H = 13 * mm
FOOT_H = 10 * mm
MARGIN = 6 * mm
CARD_W = 3 * CELL
CARD_H = HEAD_H + 3 * CELL + FOOT_H
PAGE_W = CARD_W + 2 * MARGIN
PAGE_H = CARD_H + 2 * MARGIN

# Graine dédiée POL (doit être IDENTIQUE dans _regen_pol côté app.py)
SEED_BASE = 601000


def _gen_nums(rng):
    """Retourne la grille 3×3 (None = case barrée X, 'SER' = numéro de série au centre)."""
    c0 = sorted(rng.sample(range(30, 41), 2))   # rangées milieu, bas
    c1 = sorted(rng.sample(range(41, 51), 2))   # rangées haut, bas
    c2 = sorted(rng.sample(range(51, 61), 2))   # rangées haut, milieu
    grille = [
        [None,  c1[0], c2[0]],   # haut : X en col0
        [c0[0], "SER", c2[1]],   # milieu : SÉRIE au centre
        [c0[1], c1[1], None],    # bas : X en col2
    ]
    return grille


def _signature(grille):
    return tuple(tuple(("X" if v is None else v) for v in row) for row in grille)


def _draw_ticket(cv, serial, grille, accent, couleur=True):
    bord = accent if couleur else GRIS_CLAIR
    x0, y0 = MARGIN, MARGIN + FOOT_H
    grid_top = y0 + 3 * CELL

    def cx(col):
        return x0 + (col + 0.5) * CELL

    def cy(row):
        return grid_top - (row + 0.5) * CELL

    # cadre extérieur arrondi (couleur)
    cv.setStrokeColor(bord)
    cv.setLineWidth(2.2)
    cv.roundRect(MARGIN, MARGIN, CARD_W, HEAD_H + 3 * CELL + FOOT_H, 5 * mm, stroke=1, fill=0)

    # grille interne (3×3, lignes claires)
    cv.setStrokeColor(GRIS_CLAIR)
    cv.setLineWidth(0.5)
    for i in range(1, 3):
        cv.line(x0 + i * CELL, y0 + 2 * mm, x0 + i * CELL, grid_top - 2 * mm)
    for j in range(1, 3):
        yy = grid_top - j * CELL
        cv.line(x0 + 2 * mm, yy, x0 + CARD_W - 2 * mm, yy)
    cv.line(MARGIN + 3 * mm, grid_top, MARGIN + CARD_W - 3 * mm, grid_top)
    cv.line(MARGIN + 3 * mm, y0, MARGIN + CARD_W - 3 * mm, y0)

    # en-tête
    cv.setFillColor(bord)
    cv.setFont(POLICE, 9.5)
    cv.drawCentredString(MARGIN + CARD_W / 2, grid_top + (HEAD_H - 9) / 2,
                         "Le jeux POL pour 6 boules by TUKEA 89 22 23 05")

    # numéros (noir), X (gris clair), série (couleur au centre)
    for r in range(3):
        for c in range(3):
            v = grille[r][c]
            if v is None:
                cv.setStrokeColor(GRIS_CLAIR)
                cv.setLineWidth(1.0)
                m = 9 * mm
                xa, ya = x0 + c * CELL + m, grid_top - r * CELL - m
                xb, yb = x0 + (c + 1) * CELL - m, grid_top - (r + 1) * CELL + m
                cv.line(xa, ya, xb, yb)
                cv.line(xa, yb, xb, ya)
            elif v == "SER":
                cv.setFillColor(bord)
                cv.setFont(POLICE, 20)
                cv.drawCentredString(cx(c), cy(r) - 7, "%06d" % serial)
            else:
                cv.setFillColor(colors.black)
                cv.setFont(POLICE, 46)
                cv.drawCentredString(cx(c), cy(r) - 16, str(v))

    # pied : N° SERIE + numéro
    cv.setFillColor(GRIS_CLAIR)
    cv.setFont(POLICE, 8)
    cv.drawString(MARGIN + 5 * mm, MARGIN + FOOT_H / 2 - 3, "N° SERIE")
    cv.setFillColor(bord)
    cv.setFont(POLICE, 12)
    cv.drawRightString(MARGIN + CARD_W - 5 * mm, MARGIN + FOOT_H / 2 - 4, "%06d" % serial)


def generate_pdf(nb_tickets=500, serie_start=1, output_path="/data/POL.pdf", couleur=True):
    """Génère nb_tickets tickets POL uniques. couleur=False => Noir & Blanc."""
    nb_tickets = max(1, min(int(nb_tickets), 1000))
    serie_start = max(1, int(serie_start))
    rng = random.Random(SEED_BASE + serie_start)
    vus = set()
    cv = canvas.Canvas(output_path, pagesize=(PAGE_W, PAGE_H))
    produits = 0
    while produits < nb_tickets:
        grille = _gen_nums(rng)
        sig = _signature(grille)
        if sig in vus:
            continue
        vus.add(sig)
        serial = serie_start + produits
        _draw_ticket(cv, serial, grille, RAINBOW[(serial - 1) % len(RAINBOW)], couleur)
        cv.showPage()
        produits += 1
    cv.save()
    return output_path


def generate_pdf_nb(nb_tickets=500, serie_start=1, output_path="/data/POL_NB.pdf"):
    """Version Noir & Blanc (économe en encre)."""
    return generate_pdf(nb_tickets, serie_start, output_path, couleur=False)


if __name__ == "__main__":
    generate_pdf(nb_tickets=4, serie_start=1, output_path="pol_test.pdf")
    print("POL généré")
