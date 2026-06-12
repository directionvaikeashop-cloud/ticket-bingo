# -*- coding: utf-8 -*-
"""
GENERATEUR P6 (format carte application)
TUKEA — Ticket Bingo
1 page = 1 carte BINGO 5x5 carree (105 x 105 mm), couleurs arc-en-ciel par carte.
Regle MARATHON : 1 numero par case, colonnes B/I/N/G/O (plages 1-15/16-30/31-45/46-60/61-75),
case centrale MARATHON, cartouche serie S000001 sous le N. Chiffres maximises (36 pts).
Valide par Maeva le 12/06/2026.
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

PW, PH = 105 * mm, 105 * mm
NOIR = colors.black
GRIS = colors.Color(0.42, 0.42, 0.42)
GRISCLAIR = colors.Color(0.80, 0.80, 0.80)
ARCENCIEL = [
    colors.Color(0.85, 0.20, 0.25), colors.Color(0.90, 0.55, 0.10), colors.Color(0.72, 0.60, 0.05),
    colors.Color(0.15, 0.60, 0.35), colors.Color(0.20, 0.45, 0.85), colors.Color(0.45, 0.30, 0.75),
    colors.Color(0.80, 0.25, 0.65),
]
COLS = [("B", 1, 15), ("I", 16, 30), ("N", 31, 45), ("G", 46, 60), ("O", 61, 75)]


def _gen_carte(rng):
    carte = {}
    for lettre, a, b in COLS:
        nb = 4 if lettre == "N" else 5
        carte[lettre] = tuple(rng.sample(range(a, b + 1), nb))
    return carte


def _signature(carte):
    return tuple(carte[l] for l, _, _ in COLS)


def _draw_carte(cv, serial, carte, coul):
    M = 5 * mm
    top = PH - M
    bot = M + 4 * mm
    gw = (PW - 2 * M) / 5
    header_h = 8.5 * mm
    grid_top = top - header_h
    rh = (grid_top - bot) / 5
    cv.setStrokeColor(coul)
    cv.setLineWidth(1.6)
    cv.roundRect(M, bot, PW - 2 * M, top - bot, 3.5 * mm, fill=0, stroke=1)
    cv.setStrokeColor(GRISCLAIR)
    cv.setLineWidth(0.7)
    cv.line(M, grid_top, PW - M, grid_top)
    for ci in range(1, 5):
        x = M + ci * gw
        cv.line(x, bot, x, top)
    for ri in range(1, 5):
        y = bot + ri * rh
        cv.line(M, y, PW - M, y)
    for ci, (lettre, a, b) in enumerate(COLS):
        cx = M + ci * gw + gw / 2
        cv.setFillColor(coul)
        if lettre == "N":
            cv.setFont(POLICE, 10.5)
            cv.drawCentredString(cx, top - 3.9 * mm, lettre)
            bw, bh = gw * 0.86, 3.6 * mm
            bx, by = cx - bw / 2, top - 8.2 * mm
            cv.setStrokeColor(GRIS)
            cv.setLineWidth(0.7)
            cv.rect(bx, by, bw, bh, fill=0, stroke=1)
            cv.setFillColor(GRIS)
            cv.setFont(POLICE, 7.5)
            cv.drawCentredString(cx, by + 1 * mm, "S%06d" % serial)
        else:
            cv.setFont(POLICE, 14)
            cv.drawCentredString(cx, top - 6 * mm, lettre)
    for ci, (lettre, a, b) in enumerate(COLS):
        nums = carte[lettre]
        ni = 0
        for ri in range(5):
            cx = M + ci * gw + gw / 2
            cy = bot + (4 - ri) * rh + rh / 2
            if lettre == "N" and ri == 2:
                cv.setFillColor(GRIS)
                cv.setFont(POLICE, 8.5)
                cv.drawCentredString(cx, cy + 1.6 * mm, "MARA")
                cv.drawCentredString(cx, cy - 2.6 * mm, "THON")
                continue
            n = nums[ni]
            ni += 1
            cv.setFillColor(NOIR)
            cv.setFont(POLICE, 36)
            t = str(n)
            tw = cv.stringWidth(t, POLICE, 36)
            cv.drawString(cx - tw / 2, cy - 12.5, t)
    cv.setFont(POLICE, 7)
    cv.setFillColor(GRIS)
    cv.drawCentredString(PW / 2, M + 0.5 * mm, "P6  —  TUKEA 89 22 23 05")


def generate_pdf(nb_tickets=500, serie_start=1, output_path="/data/P6.pdf"):
    """Genere nb_tickets cartes uniques (1 par page), serials a partir de serie_start."""
    nb_tickets = max(1, min(int(nb_tickets), 1000))
    serie_start = max(1, int(serie_start))
    rng = random.Random(600000 + serie_start)
    vus = set()
    cv = canvas.Canvas(output_path, pagesize=(PW, PH))
    produits = 0
    while produits < nb_tickets:
        carte = _gen_carte(rng)
        sig = _signature(carte)
        if sig in vus:
            continue
        vus.add(sig)
        serial = serie_start + produits
        _draw_carte(cv, serial, carte, ARCENCIEL[(serial - 1) % len(ARCENCIEL)])
        cv.showPage()
        produits += 1
    cv.save()
    return output_path
