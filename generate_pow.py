# -*- coding: utf-8 -*-
"""
generate_pow.py
Module de génération de tickets POW 9 BOULES — Ticket Bingo (TUKEA)
Grille 3×3 PLEINE (9 numéros), colonnes 1-9 / 10-18 / 19-27.
1 page = 1 ticket. Tickets uniques. Chiffres NOIRS, cadre COULEUR arc-en-ciel.
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

GRIS_CLAIR = colors.Color(0.80, 0.80, 0.80)
RAINBOW = [colors.HexColor('#E53935'), colors.HexColor('#FB8C00'), colors.HexColor('#F9A825'),
    colors.HexColor('#43A047'), colors.HexColor('#00ACC1'), colors.HexColor('#1E88E5'),
    colors.HexColor('#3949AB'), colors.HexColor('#8E24AA'), colors.HexColor('#D81B60'),
    colors.HexColor('#6D4C41')]

CELL = 36 * mm
HEAD_H = 13 * mm
FOOT_H = 10 * mm
MARGIN = 6 * mm
CARD_W = 3 * CELL
CARD_H = HEAD_H + 3 * CELL + FOOT_H
PAGE_W = CARD_W + 2 * MARGIN
PAGE_H = CARD_H + 2 * MARGIN
SEED_BASE = 901000


def _gen_nums(rng):
    c0 = sorted(rng.sample(range(1, 9+1), 3))
    c1 = sorted(rng.sample(range(10, 18+1), 3))
    c2 = sorted(rng.sample(range(19, 27+1), 3))
    return [[c0[0], c1[0], c2[0]], [c0[1], c1[1], c2[1]], [c0[2], c1[2], c2[2]]]


def _signature(grille):
    return tuple(tuple(row) for row in grille)


def _draw_ticket(cv, serial, grille, accent, couleur=True):
    bord = accent if couleur else GRIS_CLAIR
    x0, y0 = MARGIN, MARGIN + FOOT_H
    grid_top = y0 + 3 * CELL
    def cx(col): return x0 + (col + 0.5) * CELL
    def cy(row): return grid_top - (row + 0.5) * CELL
    cv.setStrokeColor(bord); cv.setLineWidth(2.2)
    cv.roundRect(MARGIN, MARGIN, CARD_W, HEAD_H + 3 * CELL + FOOT_H, 5 * mm, stroke=1, fill=0)
    cv.setStrokeColor(GRIS_CLAIR); cv.setLineWidth(0.5)
    for i in range(1, 3):
        cv.line(x0 + i * CELL, y0 + 2 * mm, x0 + i * CELL, grid_top - 2 * mm)
    for j in range(1, 3):
        yy = grid_top - j * CELL
        cv.line(x0 + 2 * mm, yy, x0 + CARD_W - 2 * mm, yy)
    cv.line(MARGIN + 3 * mm, grid_top, MARGIN + CARD_W - 3 * mm, grid_top)
    cv.line(MARGIN + 3 * mm, y0, MARGIN + CARD_W - 3 * mm, y0)
    cv.setFillColor(bord); cv.setFont(POLICE, 9.5)
    cv.drawCentredString(MARGIN + CARD_W / 2, grid_top + (HEAD_H - 9) / 2,
                         "Le jeux POW pour 9 boules by TUKEA 89 22 23 05")
    for r in range(3):
        for c in range(3):
            cv.setFillColor(colors.black); cv.setFont(POLICE, 46)
            cv.drawCentredString(cx(c), cy(r) - 16, str(grille[r][c]))
    cv.setFillColor(GRIS_CLAIR); cv.setFont(POLICE, 8)
    cv.drawString(MARGIN + 5 * mm, MARGIN + FOOT_H / 2 - 3, "N° SERIE")
    cv.setFillColor(bord); cv.setFont(POLICE, 12)
    cv.drawRightString(MARGIN + CARD_W - 5 * mm, MARGIN + FOOT_H / 2 - 4, "%06d" % serial)


def generate_pdf(nb_tickets=500, serie_start=1, output_path="/data/POW.pdf", couleur=True):
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


def generate_pdf_nb(nb_tickets=500, serie_start=1, output_path="/data/POW_NB.pdf"):
    return generate_pdf(nb_tickets, serie_start, output_path, couleur=False)


if __name__ == "__main__":
    generate_pdf(nb_tickets=4, serie_start=1, output_path="pow_test.pdf")
    print("POW 9 BOULES genere")
