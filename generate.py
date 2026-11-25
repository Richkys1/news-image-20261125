#!/usr/bin/env python3
"""Render the front-page image for Wednesday, 25 November 2026.

Draws a newspaper front page with Pillow + DejaVu fonts: masthead, one lead
story with an illustration panel, a 2x3 grid of stories, and an ALSO TODAY
footer. Every story was verified against a live source on 25 November 2026
before it was written in. Deterministic: fixed fonts, fixed layout, no
randomness, no timestamps. Writes entry.png (1024x1024) next to this script.
"""
import hashlib
import math

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
PAPER = (253, 253, 248)
INK = (18, 18, 18)
RED = (168, 24, 24)
NAVY = (22, 38, 66)
GREY = (110, 110, 105)
FAINT = (238, 236, 228)
SMOKE = (120, 120, 118)
FLAME = (214, 96, 32)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    """Draw wrapped text; return the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in wrap_text(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def mine(draw, cx, cy, r, color):
    """A naval mine: a dark circle with spikes."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    for k in range(8):
        ang = k * math.pi / 4
        x0 = cx + int((r - 2) * math.cos(ang))
        y0 = cy + int((r - 2) * math.sin(ang))
        x1 = cx + int((r + 9) * math.cos(ang))
        y1 = cy + int((r + 9) * math.sin(ang))
        draw.line([x0, y0, x1, y1], fill=color, width=3)


def burning_tanker(draw, x, y, w, h):
    """A tanker on fire above two mines, drawn in paper white on navy."""
    white = (253, 253, 248)
    hull_y = y + int(h * 0.52)
    # hull with a raked bow
    draw.polygon([
        (x, hull_y),
        (x + int(w * 0.88), hull_y),
        (x + w, hull_y + int(h * 0.20)),
        (x + int(w * 0.10), hull_y + int(h * 0.20)),
    ], fill=white)
    # deckhouse and funnel
    bx = x + int(w * 0.60)
    draw.rectangle([bx, hull_y - int(h * 0.26), bx + int(w * 0.22), hull_y], fill=white)
    fx = x + int(w * 0.38)
    draw.rectangle([fx, hull_y - int(h * 0.20), fx + int(w * 0.09), hull_y], fill=white)
    # masts
    for mx in (int(w * 0.16), int(w * 0.30), int(w * 0.50)):
        draw.line([x + mx, hull_y, x + mx, hull_y - int(h * 0.14)], fill=white, width=4)
    # smoke rising from the funnel and the deckhouse
    for sx, sy, sr in ((fx + 8, hull_y - int(h * 0.30), 13),
                       (fx + 2, hull_y - int(h * 0.42), 10),
                       (bx + 14, hull_y - int(h * 0.36), 11)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=SMOKE)
    # flame licks at the funnel top
    draw.polygon([(fx - 2, hull_y - int(h * 0.20)), (fx + 6, hull_y - int(h * 0.34)),
                  (fx + 14, hull_y - int(h * 0.20))], fill=FLAME)
    # two mines in the water below the hull
    water_y = hull_y + int(h * 0.30)
    mine(draw, x + int(w * 0.22), water_y, 11, white)
    mine(draw, x + int(w * 0.72), water_y + 6, 11, white)
    # wave marks, kept clear of the caption below
    for wy in (water_y + 16, water_y + 26):
        for k in range(4):
            wx = x + k * int(w * 0.26) + (8 if k % 2 else 0)
            draw.arc([wx, wy, wx + int(w * 0.13), wy + 12], 0, 180, fill=white, width=3)


def main():
    img = Image.new("RGB", (PAGE, PAGE), PAPER)
    d = ImageDraw.Draw(img)
    m = 36                      # margin
    cw = PAGE - 2 * m           # content width

    # ---- masthead ----
    d.text((PAGE // 2, 26), "THE WORLD TODAY", font=load(SERIF_B, 62),
           fill=INK, anchor="ma")
    d.text((PAGE // 2, 100), "WEDNESDAY, 25 NOVEMBER 2026", font=load(SANS_B, 21),
           fill=RED, anchor="ma")
    d.line([(m, 132), (PAGE - m, 132)], fill=INK, width=3)
    d.line([(m, 138), (PAGE - m, 138)], fill=INK, width=1)

    # ---- lead story ----
    ly = 156
    d.text((m, ly), "STRAIT OF HORMUZ  •  THE LEAD", font=load(SANS_B, 19), fill=RED)
    y = para(d, m, ly + 30, "TWO TANKERS BURN IN THE STRAIT OF HORMUZ",
             load(SERIF_B, 40), 620, leading=48)
    y = para(d, m, y + 8,
             "Iran's Revolutionary Guards say two oil tankers hit naval mines and "
             "caught fire. Saudi-led jets struck Hodeidah; the Houthis threatened "
             "Jeddah.",
             load(SANS, 20), 620, leading=26)
    d.text((m, y + 8), "Shipping through the strait is down more than 40% this month.",
           font=load(SANS_B, 19), fill=NAVY)

    # lead art panel: burning tanker over mines
    px, py, pw, ph = 700, 156, 288, 236
    d.rectangle([px, py, px + pw, py + ph], fill=NAVY)
    burning_tanker(d, px + 24, py + 22, pw - 48, 120)
    d.text((px + pw // 2, py + 178), "MINES IN THE STRAIT", font=load(SANS_B, 19),
           fill=(253, 253, 248), anchor="ma")
    d.text((px + pw // 2, py + 206), "2 TANKERS ABLAZE", font=load(SANS, 17),
           fill=(200, 205, 220), anchor="ma")
    d.line([(m, 414), (PAGE - m, 414)], fill=INK, width=2)

    # ---- grid: 2 rows x 3 cols ----
    stories = [
        ("MOSCOW", "PUTIN: RETALIATION 'INEVITABLE'",
         "Ukraine keeps hitting Russian refineries despite Trump's plea, Putin "
         "says. Drone strikes have cut refinery output 45% since late October."),
        ("MARKETS", "AI RALLY FIZZLES — NVIDIA FALLS 5.9%",
         "A day after soaring 31.5% on Huang's return, Nvidia drops. The Nikkei "
         "falls 2.8%; SoftBank slumps 14.8%."),
        ("BROOKLYN", "HUAWEI GUILTY ON 10 OF 12 COUNTS",
         "A jury convicts Huawei of bank fraud, wire fraud and sanctions "
         "violations. Sentencing is set for September 2027."),
        ("CARTAGENA", "ALL HOSTAGES FREED AFTER 17-HOUR SIEGE",
         "Special forces storm an Éxito supermarket and free about 30 "
         "hostages. One captor is killed."),
        ("JIUQUAN", "PAKISTAN'S FIRST ASTRONAUT REACHES TIANGONG",
         "Shenzhou-24 docks 3½ hours after launch. Zeeshan Ali, 40, is the "
         "first foreigner on Tiangong."),
        ("DHAKA", "BANGLADESH RAISES GARMENT PAY 36%",
         "The minimum wage rises to 17,000 taka ($136) after weeks of protests — "
         "the smallest increase in more than a decade."),
    ]
    gy = 434
    cell_w = (cw - 2 * 24) // 3
    cell_h = 196
    for i, (kick, head, body) in enumerate(stories):
        col, row = i % 3, i // 3
        x = m + col * (cell_w + 24)
        yy = gy + row * cell_h
        d.text((x, yy), kick, font=load(SANS_B, 16), fill=RED)
        yy = para(d, x, yy + 24, head, load(SERIF_B, 23), cell_w, leading=28)
        para(d, x, yy + 4, body, load(SANS, 16), cell_w, leading=21)
        if col < 2:
            d.line([(x + cell_w + 12, gy + row * cell_h + 4),
                    (x + cell_w + 12, gy + row * cell_h + cell_h - 16)],
                   fill=GREY, width=1)
    d.line([(m, gy + 2 * cell_h - 8), (PAGE - m, gy + 2 * cell_h - 8)], fill=INK, width=2)

    # ---- ALSO TODAY footer ----
    fy = gy + 2 * cell_h + 8
    d.text((m, fy), "ALSO TODAY", font=load(SANS_B, 20), fill=RED)
    also = ("Pope Leo laments the COP31 collapse in Antalya — the first climate "
            "summit since 2009 to end with no deal  •  3 dead, 23 miners still "
            "trapped in a flooded gold mine in Bogor, West Java  •  Shanghai party "
            "chief Chen Jining probed — the fourth Politburo member to fall since "
            "2025  •  North Korea expels Switzerland's envoy and orders him out "
            "in 48 hours  •  Saudi-led jets hit Hodeidah; a Houthi strike injures "
            "11 in Riyadh")
    para(d, m, fy + 30, also, load(SANS, 17), cw, leading=23)
    d.line([(m, 992), (PAGE - m, 992)], fill=INK, width=1)
    d.text((PAGE // 2, 998), "THE WORLD TODAY  •  25 NOVEMBER 2026", font=load(SANS, 14),
           fill=GREY, anchor="ma")

    img.save("entry.png", format="PNG", optimize=True)
    data = open("entry.png", "rb").read()
    print("entry.png:", len(data), "bytes, sha256:", hashlib.sha256(data).hexdigest()[:16])


if __name__ == "__main__":
    main()
