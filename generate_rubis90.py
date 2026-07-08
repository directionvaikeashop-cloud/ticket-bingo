# -*- coding: utf-8 -*-
"""generate_rubis90.py — Tickets RUBIS 90 — Ticket Bingo (TUKEA)
Grille 5 colonnes R-U-B-I-S x 3 rangées. Centre libre. 14 numéros.
Colonnes : R=1-18, U=19-36, B=37-54, I=55-72, S=73-90.
1 page = 1 ticket. Chiffres NOIRS, cadre COULEUR arc-en-ciel."""
import random
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
try:
    pdfmetrics.registerFont(TTFont('DJL','/usr/share/fonts/truetype/dejavu/DejaVuSans-ExtraLight.ttf')); POLICE='DJL'
except Exception:
    POLICE='Helvetica'
GRIS_CLAIR=colors.Color(0.80,0.80,0.80)
RAINBOW=[colors.HexColor(h) for h in ('#E53935','#FB8C00','#F9A825','#43A047','#00ACC1','#1E88E5','#3949AB','#8E24AA','#D81B60','#6D4C41')]
CELL=26*mm; HEAD_H=12*mm; SUBHEAD_H=7*mm; FOOT_H=9*mm; MARGIN=6*mm
LETTERS=["R","U","B","I","S"]; RANGES=[(1,18),(19,36),(37,54),(55,72),(73,90)]
CARD_W=5*CELL; CARD_H=HEAD_H+SUBHEAD_H+3*CELL+FOOT_H; PAGE_W=CARD_W+2*MARGIN; PAGE_H=CARD_H+2*MARGIN
SEED_BASE=90000

def _gen_nums(rng):
    cols=[]
    for ci,(lo,hi) in enumerate(RANGES):
        if ci==2:
            n=sorted(rng.sample(range(lo,hi+1),2)); cols.append([n[0],None,n[1]])
        else:
            n=sorted(rng.sample(range(lo,hi+1),3)); cols.append([n[0],n[1],n[2]])
    return [[cols[c][r] for c in range(5)] for r in range(3)]

def _signature(g): return tuple(tuple(('X' if v is None else v) for v in row) for row in g)

def _draw_ticket(cv, serial, grille, accent, couleur=True):
    bord=accent if couleur else GRIS_CLAIR
    x0=MARGIN; y0=MARGIN+FOOT_H; grid_top=y0+3*CELL
    def cx(c): return x0+(c+0.5)*CELL
    def cy(r): return grid_top-(r+0.5)*CELL
    cv.setStrokeColor(bord); cv.setLineWidth(2.2)
    cv.roundRect(MARGIN,MARGIN,CARD_W,HEAD_H+SUBHEAD_H+3*CELL+FOOT_H,4*mm,stroke=1,fill=0)
    cv.setFillColor(bord); cv.setFont(POLICE,9)
    cv.drawCentredString(MARGIN+CARD_W/2,grid_top+SUBHEAD_H+(HEAD_H-8)/2,"Le jeux RUBIS 90 by TUKEA 89 22 23 05")
    for i,lettre in enumerate(LETTERS):
        cv.setFillColor(bord); cv.setFont(POLICE,11)
        cv.drawCentredString(cx(i),grid_top+2*mm,lettre)
    cv.setStrokeColor(GRIS_CLAIR); cv.setLineWidth(0.5)
    for i in range(1,5): cv.line(x0+i*CELL,y0+2*mm,x0+i*CELL,grid_top-2*mm)
    for j in range(1,3):
        yy=grid_top-j*CELL; cv.line(x0+2*mm,yy,x0+CARD_W-2*mm,yy)
    cv.line(MARGIN+3*mm,grid_top,MARGIN+CARD_W-3*mm,grid_top)
    cv.line(MARGIN+3*mm,y0,MARGIN+CARD_W-3*mm,y0)
    for r in range(3):
        for c in range(5):
            v=grille[r][c]
            if v is None: continue
            cv.setFillColor(colors.black); cv.setFont(POLICE,30)
            cv.drawCentredString(cx(c),cy(r)-10,str(v))
    cv.setFillColor(GRIS_CLAIR); cv.setFont(POLICE,7.5)
    cv.drawString(MARGIN+4*mm,MARGIN+FOOT_H/2-3,"N° SERIE")
    cv.setFillColor(bord); cv.setFont(POLICE,11)
    cv.drawRightString(MARGIN+CARD_W-4*mm,MARGIN+FOOT_H/2-4,"%06d"%serial)

def generate_pdf(nb_tickets=500, serie_start=1, output_path="/data/RUBIS90.pdf", couleur=True):
    nb_tickets=max(1,min(int(nb_tickets),1000)); serie_start=max(1,int(serie_start))
    rng=random.Random(SEED_BASE+serie_start); vus=set()
    cv=canvas.Canvas(output_path,pagesize=(PAGE_W,PAGE_H)); produits=0
    while produits<nb_tickets:
        g=_gen_nums(rng); sig=_signature(g)
        if sig in vus: continue
        vus.add(sig); serial=serie_start+produits
        _draw_ticket(cv,serial,g,RAINBOW[(serial-1)%len(RAINBOW)],couleur)
        cv.showPage(); produits+=1
    cv.save(); return output_path

def generate_pdf_nb(nb_tickets=500, serie_start=1, output_path="/data/RUBIS90_NB.pdf"):
    return generate_pdf(nb_tickets,serie_start,output_path,couleur=False)

if __name__=="__main__":
    generate_pdf(nb_tickets=4,serie_start=1,output_path="rubis90_test.pdf"); print("RUBIS90 genere")
