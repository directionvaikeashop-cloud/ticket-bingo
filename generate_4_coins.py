import random, os
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSans-ExtraLight.ttf'
_font_registered = False
def _register_font():
    global _font_registered
    if not _font_registered:
        pdfmetrics.registerFont(TTFont('DJL', FONT_PATH))
        _font_registered = True

GREY = colors.Color(0.42, 0.42, 0.42)
RAINBOW = ['#E53935','#FF7043','#FB8C00','#F9A825','#43A047','#00ACC1','#1E88E5','#3949AB','#8E24AA','#D81B60','#6D4C41','#546E7A']

PAGE_W = 105 * mm
PAGE_H = 148 * mm
MARGIN = 4 * mm
CARD_W = PAGE_W - 2*MARGIN
CARD_H = PAGE_H - 2*MARGIN
CARD_X = MARGIN
CARD_Y = MARGIN

def _gen_grille():
    nums = sorted(random.sample(range(1, 76), 16))
    return nums[:8], nums[8:]

def _draw_grid(c, nums, start_y, height, light):
    col_w = CARD_W / 4
    row_h = height / 2
    for i, num in enumerate(nums):
        row = i // 4
        ci = i % 4
        cx = CARD_X + ci * col_w + col_w/2
        cy = start_y + height - (row + 0.5) * row_h
        c.setStrokeColor(light)
        c.setLineWidth(0.4)
        if ci > 0:
            c.line(CARD_X + ci*col_w, start_y, CARD_X + ci*col_w, start_y + height)
        if row > 0:
            c.line(CARD_X, start_y + height - row*row_h, CARD_X + CARD_W, start_y + height - row*row_h)
        fs = 42
        c.setFillColor(GREY)
        c.setFont('DJL', fs)
        c.drawCentredString(cx, cy - fs*0.37, str(num))

def _draw_ticket(c, serie, color_hex):
    col = colors.HexColor(color_hex)
    light = colors.Color(0.82, 0.82, 0.82)

    c.setFillColor(colors.white)
    c.setStrokeColor(col)
    c.setLineWidth(1.5)
    c.roundRect(CARD_X, CARD_Y, CARD_W, CARD_H, 2*mm, stroke=1, fill=1)

    g_haut, g_bas = _gen_grille()
    MID_H = 14*mm
    mid_y = CARD_Y + CARD_H/2 - MID_H/2

    # Bande centrale colorée
    c.setFillColor(col)
    c.rect(CARD_X, mid_y, CARD_W, MID_H, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont('DJL', 6.5)
    c.drawCentredString(CARD_X + CARD_W/2, mid_y + MID_H*0.65, "Le jeux 4 COINS by TUKEA 89 22 23 05")
    c.setFont('DJL', 7)
    c.drawCentredString(CARD_X + CARD_W/2, mid_y + MID_H*0.2, f"N° {serie:06d}")

    bloc_h = (CARD_H - MID_H) / 2
    _draw_grid(c, g_haut, mid_y + MID_H, bloc_h, light)
    _draw_grid(c, g_bas, CARD_Y, bloc_h, light)

def generate_pdf(nb_tickets=500, serie_start=1, output_path=None, game_name="4COINS"):
    _register_font()
    if output_path is None:
        os.makedirs('/data', exist_ok=True)
        output_path = f'/data/{game_name}_{serie_start:05d}.pdf'
    c = canvas.Canvas(output_path, pagesize=(PAGE_W, PAGE_H))
    for i in range(nb_tickets):
        _draw_ticket(c, serie_start + i, RAINBOW[i % len(RAINBOW)])
        c.showPage()
    c.save()
    return output_path

if __name__ == '__main__':
    path = generate_pdf(nb_tickets=12, serie_start=1, output_path='/mnt/user-data/outputs/4_COINS_TEST.pdf')
    print(f"PDF : {path}")
