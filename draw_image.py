#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news front page.

Everything is drawn from shapes and text with Pillow: no photos, no
network, no outside files except the system fonts. Running this script
rewrites entry.png deterministically (same bytes every run).
"""

import math
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (18, 18, 18)
FAINT = (90, 84, 74)
RED = (178, 32, 44)
BLUE = (24, 68, 128)
SEA = (196, 216, 228)
LAND = (232, 222, 196)
GOLD = (212, 160, 32)
GREEN = (46, 110, 62)
ORANGE = (224, 110, 20)

FONT_DIR = "/usr/share/fonts/truetype"
SERIF_B = os.path.join(FONT_DIR, "dejavu/DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "dejavu/DejaVuSerif.ttf")
SANS_B = os.path.join(FONT_DIR, "dejavu/DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "dejavu/DejaVuSans.ttf")
SANS_I = os.path.join(FONT_DIR, "liberation/LiberationSans-Italic.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    lines = []
    for chunk in text.split("\n"):
        line = ""
        for word in chunk.split():
            trial = f"{line} {word}".strip()
            if draw.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def block(draw, x, y, width, text, fnt, fill=INK, leading=None, align="left"):
    """Draw a wrapped paragraph; returns the y just below it."""
    leading = leading or int(fnt.size * 1.22)
    for line in wrap(draw, text, fnt, width):
        if align == "center":
            lx = x + (width - draw.textlength(line, font=fnt)) / 2
        else:
            lx = x
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def burst(draw, cx, cy, r_outer, r_inner, points=10, fill=RED):
    """A jagged starburst (explosion / impact marker)."""
    pts = []
    for i in range(points * 2):
        ang = math.pi * i / points - math.pi / 2
        r = r_outer if i % 2 == 0 else r_inner
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def dashed(draw, points, fill, width=3, dash=9, gap=7):
    """A dashed polyline through the given points."""
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        total = math.hypot(x1 - x0, y1 - y0)
        if total == 0:
            continue
        ux, uy = (x1 - x0) / total, (y1 - y0) / total
        d = 0.0
        while d < total:
            seg = min(dash, total - d)
            draw.line(
                [(x0 + ux * d, y0 + uy * d), (x0 + ux * (d + seg), y0 + uy * (d + seg))],
                fill=fill,
                width=width,
            )
            d += dash + gap


def panel(draw, x, y, w, h, fill=(255, 255, 255)):
    draw.rectangle([x, y, x + w, y + h], fill=fill, outline=INK, width=2)
    return x, y, w, h


def kicker(draw, x, y, text, color=RED):
    f = font(SANS_B, 20)
    draw.text((x, y), text.upper(), font=f, fill=color)
    return y + 28


def headline(draw, x, y, w, text, size, fnt_path=SERIF_B, fill=INK):
    f = font(fnt_path, size)
    return block(draw, x, y, w, text, f, fill=fill, leading=int(size * 1.06))


def draw_map(draw, x, y, w, h):
    """Schematic map: eastern Europe, Poland marked, missile arcs in."""
    draw.rectangle([x, y, x + w, y + h], fill=SEA)
    # Landmass: one big tan polygon standing in for the continent.
    draw.polygon(
        [
            (x + 6, y + h - 6),
            (x + 6, y + 52),
            (x + 70, y + 30),
            (x + 200, y + 16),
            (x + w - 8, y + 34),
            (x + w - 8, y + h - 6),
        ],
        fill=LAND,
    )
    # Poland: a compact red-tinted shape, left of centre.
    poland = [
        (x + 128, y + 128),
        (x + 132, y + 86),
        (x + 176, y + 74),
        (x + 222, y + 84),
        (x + 232, y + 112),
        (x + 204, y + 140),
        (x + 152, y + 144),
    ]
    draw.polygon(poland, fill=(226, 148, 138), outline=RED, width=3)
    # Ukraine, south-east of Poland.
    draw.polygon(
        [
            (x + 236, y + 104),
            (x + 300, y + 96),
            (x + 336, y + 118),
            (x + 316, y + 152),
            (x + 252, y + 148),
            (x + 230, y + 128),
        ],
        fill=(233, 226, 205),
        outline=(150, 140, 120),
        width=2,
    )
    # Missile arcs from the east, ending in impact bursts over Poland.
    dashed(draw, [(x + w - 8, y + 40), (x + 300, y + 80), (x + 208, y + 124)],
           fill=RED, width=3)
    dashed(draw, [(x + w - 8, y + 70), (x + 300, y + 110), (x + 168, y + 132)],
           fill=RED, width=3)
    burst(draw, x + 208, y + 124, 12, 6, fill=RED)
    burst(draw, x + 168, y + 132, 10, 5, fill=ORANGE)
    # NATO jets: small triangles flying in from the west.
    for jx, jy in [(x + 40, y + 34), (x + 72, y + 52)]:
        draw.polygon(
            [(jx, jy - 8), (jx + 20, jy), (jx, jy + 8), (jx + 5, jy)],
            fill=BLUE,
        )
    draw.text((x + 148, y + 100), "POLAND", font=font(SANS_B, 17), fill=INK)
    draw.text((x + 244, y + 122), "UKRAINE", font=font(SANS, 13), fill=FAINT)
    draw.text((x + w - 62, y + 8), "RUSSIA", font=font(SANS, 13), fill=FAINT)
    draw.text((x + 10, y + 8), "BALTIC SEA", font=font(SANS_I, 13), fill=(70, 100, 130))
    draw.text((x + 10, y + h - 22), "GERMANY", font=font(SANS, 13), fill=FAINT)
    tag = "NATO JETS SCRAMBLED"
    tf = font(SANS_B, 13)
    draw.text((x + w - 10 - draw.textlength(tag, font=tf), y + h - 22),
              tag, font=tf, fill=BLUE)


def draw_bridge(draw, x, y, w, h):
    """A river bridge with its middle span broken and smoking."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 228, 238))
    draw.rectangle([x, y + h - 18, x + w, y + h], fill=(120, 160, 195))
    # Deck: left half level, right half dropped and tilted, gap in between.
    draw.line([(x + 10, y + 40), (x + w // 2 - 14, y + 40)], fill=INK, width=6)
    draw.line([(x + w // 2 + 34, y + 52), (x + w - 10, y + 58)],
              fill=INK, width=6)
    for tx in (x + 44, x + w - 56):
        draw.rectangle([tx, y + 10, tx + 10, y + 42], fill=INK)
    # Broken span hanging between the two deck ends.
    draw.line([(x + w // 2 - 14, y + 40), (x + w // 2 + 34, y + 52)],
              fill=RED, width=4)
    # Smoke rising over the break.
    for cx, cy, r in [(x + w // 2 + 6, y + 22, 9), (x + w // 2 + 18, y + 12, 11),
                      (x + w // 2 + 30, y + 20, 8)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 118, 112))
    burst(draw, x + w // 2 + 10, y + 42, 11, 5, fill=ORANGE)


def draw_chart(draw, x, y, w, h):
    """A falling market line, with the day's two big drops labelled."""
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    f = font(SANS_B, 20)
    draw.text((x + 10, y + 4), "S&P 500  −3.7%", font=f, fill=RED)
    nik = "NIKKEI  −5.1%"
    draw.text((x + w - 10 - draw.textlength(nik, font=f), y + 4),
              nik, font=f, fill=RED)
    top, bottom = y + 32, y + h - 8
    left, right = x + 10, x + w - 10
    for gy in range(3):
        gyv = top + gy * (bottom - top) / 2
        draw.line([(left, gyv), (right, gyv)], fill=(225, 222, 214), width=1)
    pts = [(left + i * (right - left) / 9,
            top + (bottom - top) * v)
           for i, v in enumerate([0.06, 0.10, 0.08, 0.22, 0.30,
                                  0.28, 0.48, 0.58, 0.74, 0.92])]
    draw.line(pts, fill=RED, width=5, joint="curve")
    draw.polygon([(pts[-1][0], pts[-1][1]), (pts[-1][0] - 18, pts[-1][1] - 2),
                  (pts[-1][0] - 4, pts[-1][1] + 14)], fill=RED)


def draw_flags(draw, x, y, w, h):
    """Union Jack beside the EU circle of stars."""
    fw, fh = 104, 44
    ux, uy = x + (w - (2 * fw + 18)) // 2, y + 1
    # Union Jack, simplified: blue field, white saltire and cross, red cross.
    draw.rectangle([ux, uy, ux + fw, uy + fh], fill=(0, 36, 125))
    draw.line([(ux, uy), (ux + fw, uy + fh)], fill=(255, 255, 255), width=11)
    draw.line([(ux + fw, uy), (ux, uy + fh)], fill=(255, 255, 255), width=11)
    draw.line([(ux + fw // 2, uy), (ux + fw // 2, uy + fh)],
              fill=(255, 255, 255), width=17)
    draw.line([(ux, uy + fh // 2), (ux + fw, uy + fh // 2)],
              fill=(255, 255, 255), width=17)
    draw.line([(ux + fw // 2, uy), (ux + fw // 2, uy + fh)],
              fill=(200, 16, 46), width=9)
    draw.line([(ux, uy + fh // 2), (ux + fw, uy + fh // 2)],
              fill=(200, 16, 46), width=9)
    # EU flag: blue field, ring of twelve gold stars.
    ex = ux + fw + 18
    draw.rectangle([ex, uy, ex + fw, uy + fh], fill=(0, 51, 153))
    cx, cy = ex + fw // 2, uy + fh // 2
    for k in range(12):
        ang = -math.pi / 2 + k * math.pi / 6
        sx, sy = cx + 17 * math.cos(ang), cy + 15 * math.sin(ang)
        burst(draw, sx, sy, 4.5, 2, points=5, fill=GOLD)


def draw_tower(draw, x, y, w, h):
    """A tall Riyadh tower with a blast at its crown."""
    draw.rectangle([x, y, x + w, y + h], fill=(226, 214, 190))
    tx = x + w // 2 - 18
    draw.polygon([(tx, y + h - 2), (tx, y + 22), (tx + 12, y + 12),
                  (tx + 24, y + 12), (tx + 36, y + 22), (tx + 36, y + h - 2)],
                 fill=(52, 58, 72))
    for wy in range(y + 26, y + h - 6, 9):
        draw.line([(tx + 4, wy), (tx + 32, wy)], fill=(240, 200, 90), width=2)
    burst(draw, tx + 18, y + 12, 12, 6, fill=ORANGE)
    burst(draw, tx + 18, y + 12, 7, 3, fill=RED)
    draw.text((x + 6, y + h - 16), "RIYADH", font=font(SANS_B, 13), fill=FAINT)


def draw_cyclone(draw, x, y, w, h):
    """A spiral storm curling over a coastline."""
    draw.rectangle([x, y, x + w, y + h], fill=(196, 220, 235))
    # Coast: green land on the left, sea on the right.
    draw.polygon([(x, y), (x + 56, y), (x + 44, y + h), (x, y + h)],
                 fill=(140, 190, 130))
    draw.text((x + 6, y + h - 16), "ODISHA", font=font(SANS_B, 13), fill=GREEN)
    draw.text((x + 72, y + 2), "AKVAN", font=font(SANS_B, 15), fill=BLUE)
    cx, cy = x + w - 62, y + h // 2 + 4
    for k in range(4):
        r = 7 + k * 5
        draw.arc([cx - r, cy - r, cx + r, cy + r],
                 200 + k * 28, 200 + k * 28 + 250, fill=(255, 255, 255), width=5)
    burst(draw, cx, cy, 8, 4, fill=BLUE)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36                      # outer margin
    CW = W - 2 * M              # content width

    # ---- Masthead ----
    d.text((M, 26), "THE WORLD IN ONE DAY", font=font(SERIF_B, 56), fill=INK)
    rule(d, M, 96, W - M, width=3)
    date_f = font(SANS_B, 30)
    date = "FRIDAY  ·  20 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=date_f)) / 2, 106), date,
           font=date_f, fill=RED)
    rule(d, M, 148, W - M, width=2)

    # ---- Lead story: Poland ----
    ly = 162
    panel(d, M, ly, CW, 268, fill=(255, 255, 255))
    kicker(d, M + 18, ly + 12, "Lead — Europe on edge")
    headline(d, M + 18, ly + 42, 520, "RUSSIAN MISSILES\nSTRIKE POLAND", 46)
    block(d, M + 18, ly + 152, 520,
          "Two missiles and a suspected drone come down on Polish soil. "
          "Warsaw calls it a deliberate provocation; NATO calls it a grave "
          "violation of allied airspace.",
          font(SANS, 22), leading=28)
    draw_map(d, M + 566, ly + 42, CW - 584, 206)

    # ---- Second row: Kyiv + markets ----
    ry = 448
    rh = 232
    half = (CW - 18) // 2
    panel(d, M, ry, half, rh)
    kicker(d, M + 16, ry + 12, "War — Ukraine")
    headline(d, M + 16, ry + 40, half - 32, "KYIV BRIDGES HIT", 34)
    draw_bridge(d, M + 16, ry + 92, half - 32, 84)
    block(d, M + 16, ry + 184, half - 32,
          "Overnight strikes kill 3, damage two bridges and cut power.",
          font(SANS, 18), leading=22)
    panel(d, M + half + 18, ry, half, rh)
    kicker(d, M + half + 34, ry + 12, "Markets — Correction")
    headline(d, M + half + 34, ry + 40, half - 32, "SHARES TUMBLE", 34)
    draw_chart(d, M + half + 34, ry + 92, half - 32, 84)
    block(d, M + half + 34, ry + 184, half - 32,
          "AI worries sink Wall Street and Tokyo for a sixth straight day; "
          "Anthropic slides on day two.",
          font(SANS, 18), leading=22)

    # ---- Third row: three stories ----
    ty = 698
    th = 196
    third = (CW - 36) // 3
    xs = [M, M + third + 18, M + 2 * (third + 18)]

    panel(d, xs[0], ty, third, th)
    kicker(d, xs[0] + 14, ty + 10, "Politics — UK · EU", color=BLUE)
    headline(d, xs[0] + 14, ty + 36, third - 28, "BREXIT RESET DEAL", 24)
    draw_flags(d, xs[0] + 14, ty + 98, third - 28, 46)
    block(d, xs[0] + 14, ty + 148, third - 28,
          "Food trade, carbon and youth mobility agreed.",
          font(SANS, 17), leading=21)

    panel(d, xs[1], ty, third, th)
    kicker(d, xs[1] + 14, ty + 10, "Middle East — Riyadh")
    headline(d, xs[1] + 14, ty + 36, third - 28, "TOWER HIT IN RIYADH", 24)
    draw_tower(d, xs[1] + 14, ty + 98, third - 28, 46)
    block(d, xs[1] + 14, ty + 150, third - 28,
          "Houthi strike hits the PIF Tower in the Saudi capital.",
          font(SANS, 17), leading=21)

    panel(d, xs[2], ty, third, th)
    kicker(d, xs[2] + 14, ty + 10, "Disaster — Asia")
    headline(d, xs[2] + 14, ty + 36, third - 28, "CYCLONE AKVAN", 24)
    draw_cyclone(d, xs[2] + 14, ty + 98, third - 28, 46)
    block(d, xs[2] + 14, ty + 148, third - 28,
          "Landfall in Odisha; a 6.7 quake shakes Peru.",
          font(SANS, 17), leading=21)

    # ---- Footer ticker ----
    rule(d, M, 912, W - M, width=2)
    d.text((M, 926), "ALSO TODAY", font=font(SANS_B, 20), fill=RED)
    block(d, M, 952, CW,
          "Rights groups urge sanctions after the world court's genocide ruling  ·  "
          "COP31 final text drops “fossil fuels”  ·  Palisades arson verdict  ·  "
          "Bayer to pay $7.25bn over Roundup  ·  GTA VI sets a $3.79bn first-day record  ·  "
          "BepiColombo reaches Mercury",
          font(SANS, 18), leading=23, fill=FAINT)

    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
