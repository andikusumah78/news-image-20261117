#!/usr/bin/env python3
"""Draw the news-image-20261117 entry: a newspaper front page summing up
Tuesday 17 November 2026's world news, drawn programmatically with Pillow.

Stories (all reported on 17 Nov 2026, cross-checked across several news
briefs citing BBC / AP / Al Jazeera / Reuters):
  1. Ukraine strikes the Kerch Bridge to Crimea; a road span collapses.
     Russia hits Kyiv's bridges with ballistic missiles.
  2. Trump arrives in Manila for the ASEAN summit; a three-way meeting
     with Xi Jinping and Vladimir Putin is set for Thursday in Shenzhen.
  3. Two tankers hit mines and catch fire near the Strait of Hormuz;
     a third US aircraft carrier arrives in the region.
  4. A ULA Vulcan rocket fails in flight, destroying 40 Amazon satellites.

Layout (1024 x 1024): masthead with the date, one big main panel for the
Kerch Bridge, and three smaller panels for the other stories, each with a
short headline and subline so the image reads on its own.

Deterministic: no randomness, no network, no clock. Running this script
twice produces byte-identical output (PNG metadata carries no timestamps
when saved with Pillow's default settings here).
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
F_REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")
F_SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")

NAVY = (13, 27, 46)
NAVY2 = (16, 34, 58)
GOLD = (214, 164, 65)
WHITE = (255, 255, 255)
LIGHT = (210, 220, 230)
DARK = (20, 24, 31)


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, max_size, max_w, min_size=14):
    """Largest bold font (<= max_size) that fits max_w, never below min_size."""
    size = max_size
    while size > min_size:
        f = ImageFont.truetype(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return ImageFont.truetype(path, min_size)


def vgrad(draw, box, top, bottom):
    """Vertical gradient inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    steps = max(1, y1 - y0)
    for i in range(steps):
        t = i / steps
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_smoke(base, cx, cy, scale=1.0, color=(60, 60, 66, 150)):
    """Soft smoke plume: blurred ellipses on an RGBA overlay."""
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    puffs = [
        (0, 0, 44, 38), (-22, -18, 36, 30), (20, -20, 38, 32),
        (-8, -40, 42, 34), (14, -44, 32, 28), (-2, -62, 36, 30),
        (10, -80, 28, 24), (-10, -82, 26, 22),
    ]
    for dx, dy, w, h in puffs:
        x0 = cx + int(dx * scale) - w // 2
        y0 = cy + int(dy * scale) - h // 2
        d.ellipse([x0, y0, x0 + w, y0 + h], fill=color)
    layer = layer.filter(ImageFilter.GaussianBlur(10))
    base.alpha_composite(layer)


def draw_fire(base, cx, cy, scale=1.0):
    """Orange fire glow: blurred layered ellipses on an RGBA overlay."""
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([cx - 46 * scale, cy - 26 * scale, cx + 46 * scale, cy + 26 * scale],
              fill=(255, 110, 20, 220))
    d.ellipse([cx - 30 * scale, cy - 18 * scale, cx + 30 * scale, cy + 18 * scale],
              fill=(255, 180, 40, 230))
    d.ellipse([cx - 16 * scale, cy - 10 * scale, cx + 16 * scale, cy + 10 * scale],
              fill=(255, 230, 120, 240))
    layer = layer.filter(ImageFilter.GaussianBlur(8))
    base.alpha_composite(layer)


def main_panel(img, draw):
    """Kerch Bridge at dusk: deck with a collapsed middle span."""
    x0, y0, x1, y1 = 0, 104, 1024, 560
    # dusk sky
    vgrad(draw, (x0, y0, x1, 470), (38, 52, 82), (176, 84, 46))
    vgrad(draw, (x0, 470, x1, y1), (240, 163, 94), (120, 62, 40))
    # low sun, half hidden behind smoke
    draw.ellipse([700, 392, 790, 482], fill=(255, 214, 140))
    draw.ellipse([712, 404, 778, 470], fill=(255, 232, 180))
    # sea
    vgrad(draw, (x0, 470, x1, y1), (24, 62, 78), (10, 30, 42))
    for sx, sw in [(60, 180), (300, 120), (620, 200), (860, 140)]:
        draw.line([(sx, 500), (sx + sw, 500)], fill=(150, 120, 70), width=3)
        draw.line([(sx + 40, 528), (sx + sw - 20, 528)], fill=(120, 95, 55), width=2)
    # bridge towers (left and right, standing)
    for tx in (150, 830):
        draw.polygon([(tx - 16, 470), (tx - 8, 330), (tx + 8, 330), (tx + 16, 470)],
                     fill=DARK)
        draw.rectangle([tx - 26, 322, tx + 26, 336], fill=DARK)
    # deck: left span, right span, middle GONE (collapsed)
    draw.rectangle([0, 448, 400, 470], fill=DARK)
    draw.rectangle([640, 448, 1024, 470], fill=DARK)
    # deck railing ticks
    for bx in range(0, 400, 28):
        draw.line([(bx, 448), (bx, 436)], fill=DARK, width=4)
    for bx in range(648, 1024, 28):
        draw.line([(bx, 448), (bx, 436)], fill=DARK, width=4)
    # fallen span slanting down into the sea, broken (lighter edge so it reads)
    draw.polygon([(400, 448), (470, 448), (560, 540), (520, 552)], fill=(44, 50, 62))
    draw.polygon([(560, 540), (600, 548), (590, 566), (552, 558)], fill=(44, 50, 62))
    draw.line([(400, 448), (470, 448), (560, 540)], fill=(150, 150, 160), width=3)
    draw.line([(400, 448), (520, 552)], fill=(120, 120, 130), width=2)
    # cables from towers to deck (standing parts only)
    for cx0, cx1 in [(150, 380), (830, 660)]:
        draw.line([(cx0, 336), (cx1, 448)], fill=(30, 34, 42), width=3)
    # fire + smoke at the break (smoke first, fire in front)
    draw_smoke(img, 520, 448, scale=0.9)
    draw_smoke(img, 420, 456, scale=0.55, color=(70, 60, 55, 130))
    draw_fire(img, 520, 472, scale=1.0)
    # caption strip (taller, so headline + subline both fit)
    draw.rectangle([0, 560, 1024, 640], fill=NAVY)
    draw.rectangle([0, 560, 1024, 566], fill=GOLD)
    f_h = fit_font(draw, "KERCH BRIDGE HIT — ROAD SPAN COLLAPSES", F_BOLD, 42, 1024 - 56)
    f_s = font(F_REG, 23)
    draw.text((28, 570), "KERCH BRIDGE HIT — ROAD SPAN COLLAPSES",
              font=f_h, fill=WHITE)
    draw.text((28, 612), "Ukraine strikes the Crimea link again as Russia hits Kyiv bridges",
              font=f_s, fill=LIGHT)


def panel_manila(img, draw, x0, y0, x1, y1):
    """Trump arrives in Manila for the ASEAN summit."""
    vgrad(draw, (x0, y0, x1, y1 - 130), (250, 196, 110), (140, 180, 210))
    draw.ellipse([x0 + 30, y0 + 26, x0 + 96, y0 + 92], fill=(255, 240, 190))
    # skyline silhouette
    base = y1 - 130
    skyline = [(0, 90), (34, 130), (70, 70), (108, 120), (146, 60),
               (186, 110), (224, 80), (262, 125), (298, 95)]
    for i, (dx, hgt) in enumerate(skyline):
        draw.rectangle([x0 + dx, base - hgt, x0 + dx + 34, base], fill=(52, 58, 72))
    # jet plane flying in above the skyline (Trump arriving)
    px, py = x0 + 190, y0 + 42
    draw.polygon([(px - 52, py), (px + 52, py - 6), (px + 66, py + 2),
                  (px + 52, py + 8), (px - 52, py + 10)], fill=(40, 44, 56))
    draw.polygon([(px + 8, py - 2), (px + 34, py - 26), (px + 40, py - 2)],
                 fill=(40, 44, 56))
    draw.polygon([(px - 30, py + 8), (px - 8, py + 30), (px - 2, py + 8)],
                 fill=(40, 44, 56))
    draw.line([(px - 52, py + 5), (px - 84, py + 8)], fill=(200, 200, 210), width=2)
    caption(draw, x0, y1 - 130, x1, y1,
            "TRUMP IN MANILA",
            "ASEAN summit opens; Xi–Putin talks set for Thursday")


def panel_hormuz(img, draw, x0, y0, x1, y1):
    """Tankers hit by mines near the Strait of Hormuz."""
    vgrad(draw, (x0, y0, x1, y1 - 130), (200, 120, 60), (90, 50, 30))
    vgrad(draw, (x0, y1 - 210, x1, y1 - 130), (30, 70, 88), (14, 40, 56))
    # tanker silhouette
    base = y1 - 130
    draw.polygon([(x0 + 30, base - 52), (x0 + 300, base - 52), (x0 + 282, base - 8),
                  (x0 + 48, base - 8)], fill=(18, 22, 30))
    draw.rectangle([x0 + 210, base - 92, x0 + 268, base - 52], fill=(18, 22, 30))
    draw.rectangle([x0 + 84, base - 76, x0 + 104, base - 52], fill=(18, 22, 30))
    draw.line([(x0 + 30, base - 8), (x0 + 300, base - 8)], fill=(120, 90, 50), width=2)
    draw_smoke(img, x0 + 150, base - 60, scale=0.6)
    draw_fire(img, x0 + 150, base - 54, scale=0.7)
    # distant carrier silhouette
    draw.rectangle([x0 + 262, base - 118, x0 + 320, base - 96], fill=(40, 44, 54))
    caption(draw, x0, y1 - 130, x1, y1,
            "TANKERS HIT BY MINES",
            "Strait of Hormuz; third US carrier arrives")


def panel_rocket(img, draw, x0, y0, x1, y1):
    """ULA Vulcan rocket fails; 40 Amazon satellites lost."""
    vgrad(draw, (x0, y0, x1, y1 - 130), (8, 12, 30), (24, 32, 66))
    stars = [(18, 30), (60, 70), (110, 22), (160, 58), (210, 28), (260, 66),
             (300, 34), (40, 120), (90, 150), (200, 130), (250, 110), (320, 130),
             (130, 96), (280, 170), (30, 180), (180, 180)]
    for sx, sy in stars:
        draw.ellipse([x0 + sx - 2, y0 + sy - 2, x0 + sx + 2, y0 + sy + 2],
                     fill=(220, 225, 240))
    # rocket body ascending, tilted slightly
    cx = x0 + 170
    draw.polygon([(cx - 16, y0 + 150), (cx, y0 + 78), (cx + 16, y0 + 150)], fill=(225, 228, 235))
    draw.polygon([(cx - 16, y0 + 150), (cx - 30, y0 + 178), (cx - 16, y0 + 168)], fill=(200, 60, 40))
    draw.polygon([(cx + 16, y0 + 150), (cx + 30, y0 + 178), (cx + 16, y0 + 168)], fill=(200, 60, 40))
    draw.rectangle([cx - 16, y0 + 150, cx + 16, y0 + 196], fill=(200, 205, 215))
    # flame
    draw.polygon([(cx - 10, y0 + 196), (cx, y0 + 246), (cx + 10, y0 + 196)],
                 fill=(255, 170, 40))
    # debris burst higher up
    for dx, dy, r in [(-52, -8, 4), (44, -18, 3), (-20, -30, 3), (26, 6, 4),
                      (0, -38, 3), (-38, 22, 3), (52, 18, 3)]:
        draw.ellipse([cx + dx - r, y0 + 60 + dy - r, cx + dx + r, y0 + 60 + dy + r],
                     fill=(255, 150, 60))
    caption(draw, x0, y1 - 130, x1, y1,
            "VULCAN ROCKET FAILS",
            "40 Amazon satellites lost")


def caption(draw, x0, y0, x1, y1, headline, sub):
    draw.rectangle([x0, y0, x1, y1], fill=NAVY)
    draw.rectangle([x0, y0, x1, y0 + 5], fill=GOLD)
    f_h = fit_font(draw, headline, F_BOLD, 28, (x1 - x0) - 32)
    f_s = font(F_REG, 20)
    draw.text((x0 + 16, y0 + 14), headline, font=f_h, fill=WHITE)
    lines = wrap(draw, sub, f_s, (x1 - x0) - 32)
    y = y0 + 56
    for line in lines[:2]:
        draw.text((x0 + 16, y), line, font=f_s, fill=LIGHT)
        y += 26


def build():
    img = Image.new("RGB", (W, H), NAVY)
    overlay = img.convert("RGBA")
    draw = ImageDraw.Draw(overlay)
    # masthead
    draw.rectangle([0, 0, W, 104], fill=NAVY)
    draw.rectangle([0, 100, W, 104], fill=GOLD)
    draw.text((28, 22), "THE WORLD", font=font(F_SERIF_BOLD, 58), fill=WHITE)
    draw.text((W - 28 - draw.textlength("TUESDAY", font=font(F_BOLD, 30)),
               26), "TUESDAY", font=font(F_BOLD, 30), fill=GOLD)
    draw.text((W - 28 - draw.textlength("17 NOVEMBER 2026", font=font(F_BOLD, 30)),
               62), "17 NOVEMBER 2026", font=font(F_BOLD, 30), fill=WHITE)
    main_panel(overlay, draw)
    # bottom row: three panels
    panel_manila(overlay, draw, 0, 640, 341, 1024)
    panel_hormuz(overlay, draw, 342, 640, 682, 1024)
    panel_rocket(overlay, draw, 683, 640, 1024, 1024)
    # dividers
    draw.line([(341, 640), (341, 1024)], fill=GOLD, width=2)
    draw.line([(682, 640), (682, 1024)], fill=GOLD, width=2)
    out = overlay.convert("RGB")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    out.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    build()
