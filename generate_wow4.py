# -*- coding: utf-8 -*-
"""generate_wow4.py — Tickets WOW 4 — Ticket Bingo (TUKEA)
Grille 2×2, colonnes W (30-44) et O (45-60). 4 numéros.
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
GRIS_CLAIR=colors.Color(0.80,0.80,0.80); GRIS=colors.Color(0.42,0.42,0.42)
RAINBOW=[colors.HexColor(h) for h in ('#E53935','#FB8C00','#F9A825','#43A047','#00ACC1','#1E88E5','#3949AB','#8E24AA','#D81B60','#6D4C41')]
CELL=42*mm; HEAD_H=13*mm; SUBHEAD_H=8*mm; FOOT_H=10*mm; MARGIN=6*mm
CARD_W=2*CELL; CARD_H=HEAD_H+SUBHEAD_H+2*CELL+FOOT_H; PAGE_W=CARD_W+2*MARGIN; PAGE_H=CARD_H+2*MARGIN
SEED_BASE=401000
RANGES=[(30,44),(45,60)]

def _gen_nums(rng):
    w=sorted(rng.sample(range(30,45),2))
    o=sorted(rng.sample(range(45,61),2))
    return [[w[0],o[0]],[w[1],o[1]]]

def _signature(g): return tuple(tuple(row) for row in g)

def _draw_ticket(cv, serial, grille, accent, couleur=True):
    bord=accent if couleur else GRIS_CLAIR
    x0=MARGIN; y0=MARGIN+FOOT_H; grid_top=y0+2*CELL
    def cx(c): return x0+(c+0.5)*CELL
    def cy(r): return grid_top-(r+0.5)*CELL
    cv.setStrokeColor(bord); cv.setLineWidth(2.2)
    cv.roundRect(MARGIN,MARGIN,CARD_W,HEAD_H+SUBHEAD_H+2*CELL+FOOT_H,5*mm,stroke=1,fill=0)
    # en-tête
    cv.setFillColor(bord); cv.setFont(POLICE,9.5)
    cv.drawCentredString(MARGIN+CARD_W/2,grid_top+SUBHEAD_H+(HEAD_H-9)/2,"Le jeux WOW pour 4 boules by TUKEA 89 22 23 05")
    # sous-en-tête colonnes W / O avec plages
    for i,(lettre,(lo,hi)) in enumerate(zip(["W","O"],RANGES)):
        cv.setFillColor(bord); cv.setFont(POLICE,11)
        cv.drawCentredString(cx(i),grid_top+2.5*mm,lettre)
        cv.setFillColor(GRIS); cv.setFont(POLICE,6)
        cv.drawCentredString(cx(i),grid_top-1*mm+SUBHEAD_H-6*mm,"%d - %d"%(lo,hi))
    cv.setStrokeColor(GRIS_CLAIR); cv.setLineWidth(0.5)
    cv.line(x0+CELL,y0+2*mm,x0+CELL,grid_top-2*mm)
    cv.line(x0+2*mm,grid_top-CELL,x0+CARD_W-2*mm,grid_top-CELL)
    cv.line(MARGIN+3*mm,grid_top,MARGIN+CARD_W-3*mm,grid_top)
    cv.line(MARGIN+3*mm,y0,MARGIN+CARD_W-3*mm,y0)
    for r in range(2):
        for c in range(2):
            cv.setFillColor(colors.black); cv.setFont(POLICE,52)
            cv.drawCentredString(cx(c),cy(r)-18,str(grille[r][c]))
    cv.setFillColor(GRIS_CLAIR); cv.setFont(POLICE,8)
    cv.drawString(MARGIN+5*mm,MARGIN+FOOT_H/2-3,"N° SERIE")
    cv.setFillColor(bord); cv.setFont(POLICE,12)
    cv.drawRightString(MARGIN+CARD_W-5*mm,MARGIN+FOOT_H/2-4,"%06d"%serial)

def generate_pdf(nb_tickets=500, serie_start=1, output_path="/data/WOW4.pdf", couleur=True):
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

def generate_pdf_nb(nb_tickets=500, serie_start=1, output_path="/data/WOW4_NB.pdf"):
    return generate_pdf(nb_tickets,serie_start,output_path,couleur=False)

if __name__=="__main__":
    generate_pdf(nb_tickets=4,serie_start=1,output_path="wow4_test.pdf"); print("WOW4 genere")
