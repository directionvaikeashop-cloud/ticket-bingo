# -*- coding: utf-8 -*-
"""generate_bno.py — Tickets BNO 8 BOULES — Ticket Bingo (TUKEA)
Grille 3×3, colonnes 1-15 / 31-45 / 61-75. CENTRE vide. 8 numéros.
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
CELL=36*mm; HEAD_H=13*mm; FOOT_H=10*mm; MARGIN=6*mm
CARD_W=3*CELL; CARD_H=HEAD_H+3*CELL+FOOT_H; PAGE_W=CARD_W+2*MARGIN; PAGE_H=CARD_H+2*MARGIN
SEED_BASE=801000

def _gen_nums(rng):
    c0=sorted(rng.sample(range(1,15+1),3))
    c2=sorted(rng.sample(range(61,75+1),3))
    c1n=sorted(rng.sample(range(31,45+1),2))
    c1=[c1n[0],None,c1n[1]]
    return [[c0[0],c1[0],c2[0]],[c0[1],None,c2[1]],[c0[2],c1[2],c2[2]]]

def _signature(g): return tuple(tuple(('X' if v is None else v) for v in row) for row in g)

def _draw_ticket(cv, serial, grille, accent, couleur=True):
    bord=accent if couleur else GRIS_CLAIR
    x0,y0=MARGIN,MARGIN+FOOT_H; grid_top=y0+3*CELL
    def cx(c): return x0+(c+0.5)*CELL
    def cy(r): return grid_top-(r+0.5)*CELL
    cv.setStrokeColor(bord); cv.setLineWidth(2.2)
    cv.roundRect(MARGIN,MARGIN,CARD_W,HEAD_H+3*CELL+FOOT_H,5*mm,stroke=1,fill=0)
    cv.setStrokeColor(GRIS_CLAIR); cv.setLineWidth(0.5)
    for i in range(1,3): cv.line(x0+i*CELL,y0+2*mm,x0+i*CELL,grid_top-2*mm)
    for j in range(1,3):
        yy=grid_top-j*CELL; cv.line(x0+2*mm,yy,x0+CARD_W-2*mm,yy)
    cv.line(MARGIN+3*mm,grid_top,MARGIN+CARD_W-3*mm,grid_top)
    cv.line(MARGIN+3*mm,y0,MARGIN+CARD_W-3*mm,y0)
    cv.setFillColor(bord); cv.setFont(POLICE,9.5)
    cv.drawCentredString(MARGIN+CARD_W/2,grid_top+(HEAD_H-9)/2,"Le jeux BNO pour 8 boules by TUKEA 89 22 23 05")
    for r in range(3):
        for c in range(3):
            v=grille[r][c]
            if v is None: continue
            cv.setFillColor(colors.black); cv.setFont(POLICE,46)
            cv.drawCentredString(cx(c),cy(r)-16,str(v))
    cv.setFillColor(GRIS_CLAIR); cv.setFont(POLICE,8)
    cv.drawString(MARGIN+5*mm,MARGIN+FOOT_H/2-3,"N° SERIE")
    cv.setFillColor(bord); cv.setFont(POLICE,12)
    cv.drawRightString(MARGIN+CARD_W-5*mm,MARGIN+FOOT_H/2-4,"%06d"%serial)

def generate_pdf(nb_tickets=500, serie_start=1, output_path="/data/BNO 8 BOULES.pdf", couleur=True):
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

def generate_pdf_nb(nb_tickets=500, serie_start=1, output_path="/data/BNO 8 BOULES_NB.pdf"):
    return generate_pdf(nb_tickets,serie_start,output_path,couleur=False)

if __name__=="__main__":
    generate_pdf(nb_tickets=4,serie_start=1,output_path="bno_test.pdf"); print("BNO 8 BOULES genere")
