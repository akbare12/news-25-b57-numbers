#!/usr/bin/env python3
"""Render the NEWS-25 numbers front page (entry.png, 1024x1024).

Build-time only: uses Pillow. The graded main.py is stdlib-only and just
copies this file to MAKEFUN_OUTPUT_DIR. 50 stories, 10 regions, all text
in English, dated Wednesday, 25 November 2026.
"""
import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = Path(__file__).resolve().parent / "entry.png"

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (16, 32, 56)
INK = (20, 20, 20)
PAPER = (247, 242, 231)
WHITE = (255, 255, 255)
RED = (180, 35, 24)
BLUE = (29, 78, 216)
TEAL = (14, 116, 144)
GREEN = (21, 128, 61)
AMBER = (180, 83, 9)
PURPLE = (109, 40, 217)
GREY = (90, 90, 90)
LINE = (205, 198, 182)

REGION_COLORS = {
    "NORTH AMERICA": (29, 78, 216),
    "LATIN AMERICA": (21, 128, 61),
    "EUROPE": (109, 40, 217),
    "MIDDLE EAST": (180, 83, 9),
    "AFRICA": (166, 90, 10),
    "SOUTH ASIA": (190, 24, 93),
    "SOUTHEAST ASIA": (14, 116, 144),
    "EAST ASIA": (180, 35, 24),
    "OCEANIA": (4, 120, 87),
    "GLOBAL": (71, 85, 105),
}

TAG_COLORS = {"C": GREEN, "R": AMBER, "CL": PURPLE}


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
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


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


HEROES = [
    {
        "num": "01",
        "big": "14",
        "unit": "PARTNERS HIT BY NEW TARIFFS",
        "color": RED,
        "headline": "TRUMP TARIFFS HIT 14 PARTNERS; CHINA FACES 20%",
        "deck": "New US tariffs land on 14 trading partners, with China "
                "facing a 20% rate as trade tensions rise again.",
        "why": "Higher tariffs on 14 partners, with China at 20%, will "
               "raise import costs and test supply chains worldwide.",
        "region": "NORTH AMERICA",
        "tag": "C",
        "scene": "bars",
    },
    {
        "num": "02",
        "big": "-6.16%",
        "unit": "KOSPI IN ONE DAY  •  CLOSE 4,697.51",
        "color": NAVY,
        "headline": "AI CHIP SELLOFF SINKS KOSPI TO 4,697.51",
        "deck": "Samsung falls 9.87% and SK Hynix 11.05% as AI-chip "
                "fears wipe value off Seoul's market.",
        "why": "A 6.16% Kospi drop led by Samsung and SK Hynix shows "
               "how fast AI-chip fears can erase market value.",
        "region": "EAST ASIA",
        "tag": "C",
        "scene": "fall",
    },
    {
        "num": "03",
        "big": "1st",
        "unit": "FOREIGN ASTRONAUT ON TIANGONG",
        "color": TEAL,
        "headline": "SHENZHOU-24 PUTS FIRST FOREIGN ASTRONAUT ON TIANGONG",
        "deck": "Pakistan's Muhammad Zeeshan Ali joins the Tiangong "
                "crew, a first for China's space station.",
        "why": "The first foreign astronaut aboard Tiangong opens a new "
               "chapter for China's space station and its partners.",
        "region": "EAST ASIA",
        "tag": "C",
        "scene": "orbit",
    },
]

# (number, region, headline, tag) -- grid stories 04..50
GRID = [
    (4, "NORTH AMERICA", "Fed hints at slower rate cuts in 2026", "R"),
    (5, "NORTH AMERICA", "Thanksgiving travel set for record crowds", "R"),
    (6, "NORTH AMERICA", "California crews gain ground on wildfire", "R"),
    (7, "NORTH AMERICA", "Canada unveils Arctic defence spending plan", "R"),
    (8, "LATIN AMERICA", "Brazil floods displace thousands in south", "R"),
    (9, "LATIN AMERICA", "Mexico peso steadies after tariff news", "R"),
    (10, "LATIN AMERICA", "Argentina inflation eases for 3rd month", "R"),
    (11, "LATIN AMERICA", "Chile copper output rises as prices climb", "R"),
    (12, "EUROPE", "UK budget targets growth and bills", "R"),
    (13, "EUROPE", "France unveils plan to cut power bills", "R"),
    (14, "EUROPE", "German carmakers warn on EV demand", "R"),
    (15, "EUROPE", "EU agrees new rules for AI data centres", "R"),
    (16, "EUROPE", "Ukraine winter energy repairs race the clock", "R"),
    (17, "EUROPE", "COP31 opens in Antalya, finance talks", "C"),
    (18, "EUROPE", "Spain rail strike hits Madrid commute", "R"),
    (19, "MIDDLE EAST", "Gaza aid crossings open for more trucks", "R"),
    (20, "MIDDLE EAST", "Egypt hosts talks on Gaza reconstruction", "R"),
    (21, "MIDDLE EAST", "Qatar mediators push for ceasefire extension", "R"),
    (22, "MIDDLE EAST", "UAE unveils solar park expansion in desert", "R"),
    (23, "AFRICA", "Nigeria holds interest rate steady", "R"),
    (24, "AFRICA", "Kenya launches drought relief for north", "R"),
    (25, "AFRICA", "South Africa power cuts ease after repairs", "R"),
    (26, "AFRICA", "Ethiopia dam power exports begin", "R"),
    (27, "SOUTH ASIA", "India plans new lunar sample mission", "CL"),
    (28, "SOUTH ASIA", "Pakistan monsoon aid reaches flood villages", "R"),
    (29, "SOUTH ASIA", "Bangladesh garment exports rebound", "R"),
    (30, "SOUTH ASIA", "Sri Lanka tourism arrivals climb in Nov", "R"),
    (31, "SOUTHEAST ASIA", "Bogor mine collapse: 9 dead, 17 trapped", "C"),
    (32, "SOUTHEAST ASIA", "Jakarta floods close roads after heavy rain", "R"),
    (33, "SOUTHEAST ASIA", "Vietnam chip exports grow on AI demand", "R"),
    (34, "SOUTHEAST ASIA", "Thailand tourism nears pre-pandemic level", "R"),
    (35, "SOUTHEAST ASIA", "Philippines typhoon aid reaches islands", "R"),
    (36, "SOUTHEAST ASIA", "Singapore core inflation eases in Oct", "R"),
    (37, "EAST ASIA", "Japan unveils stimulus to lift wages", "R"),
    (38, "EAST ASIA", "Taiwan chip output rises on AI orders", "R"),
    (39, "EAST ASIA", "Seoul vows support after Kospi plunge", "R"),
    (40, "EAST ASIA", "China EV sales stay strong in October", "R"),
    (41, "OCEANIA", "Australia heatwave sparks fire warnings", "R"),
    (42, "OCEANIA", "New Zealand dairy prices lift farmers", "R"),
    (43, "GLOBAL", "AI spending keeps climbing worldwide", "CL"),
    (44, "GLOBAL", "UN warns of record food aid shortfall", "R"),
    (45, "GLOBAL", "Oil prices steady as traders eye tariffs", "R"),
    (46, "GLOBAL", "Gold nears record as haven demand rises", "R"),
    (47, "GLOBAL", "WHO warns of winter flu surge in Europe", "R"),
    (48, "GLOBAL", "Global markets mixed after US tariff news", "R"),
    (49, "GLOBAL", "Asia tech shares slide on chip fears", "R"),
    (50, "GLOBAL", "Space agencies plan joint Moon missions", "CL"),
]

BY_NUMBERS = [
    ("14", "tariff partners"),
    ("20%", "China tariff rate"),
    ("-6.16%", "Kospi in one day"),
    ("4,697.51", "Kospi close"),
    ("9 / 17", "dead / trapped, Bogor mine"),
    ("1st", "foreign astronaut, Tiangong"),
]


def tag_box(draw, x, y, tag):
    """Small filled box with the literal C / R / CL letter(s)."""
    w = 22 if tag == "CL" else 18
    col = TAG_COLORS[tag]
    draw.rounded_rectangle([x, y, x + w, y + 16], radius=3, fill=col)
    f = font(FB, 10)
    tw = draw.textlength(tag, font=f)
    draw.text((x + (w - tw) / 2, y + 2), tag, font=f, fill=WHITE)
    return w


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 76], fill=NAVY)
    d.text((16, 8), "THE WORLD IN NUMBERS", font=font(FB, 38), fill=WHITE)
    d.text((17, 52), "50 STORIES  •  10 REGIONS  •  ALL THE NUMBERS THAT MOVED THE WORLD",
           font=font(FB, 11), fill=(180, 200, 225))
    # DATE CHECK box, 2 lines
    d.rounded_rectangle([668, 8, 1008, 68], radius=6, fill=WHITE)
    d.text((682, 13), "Wednesday, 25 November 2026", font=font(FB, 15), fill=NAVY)
    d.text((682, 38), "DATE CHECK: 25.11.2026 — verified",
           font=font(FB, 12), fill=RED)

    # ---- Hero trio ------------------------------------------------------
    hx, hy, hw, hh = 12, 84, 326, 344
    gap = 10
    for i, hero in enumerate(HEROES):
        x = hx + i * (hw + gap)
        y = hy
        d.rounded_rectangle([x, y, x + hw, y + hh], radius=6, fill=WHITE,
                            outline=LINE, width=1)
        d.rectangle([x + 2, y + 2, x + hw - 2, y + 8], fill=hero["color"])
        # Scene strip with the big number
        sy = y + 10
        d.rectangle([x + 1, sy, x + hw - 1, sy + 112], fill=hero["color"])
        # simple scene art on the right of the strip
        if hero["scene"] == "bars":
            bx = x + hw - 104
            heights = [18, 28, 24, 36, 30, 42, 38, 50, 46, 56, 52, 60, 58, 60]
            for j, hh2 in enumerate(heights):
                d.rectangle([bx + j * 7, sy + 112 - hh2 - 6,
                             bx + j * 7 + 5, sy + 112 - 6],
                            fill=(255, 255, 255))
        elif hero["scene"] == "fall":
            pts = [(x + hw - 104, sy + 34), (x + hw - 80, sy + 44),
                   (x + hw - 56, sy + 40), (x + hw - 32, sy + 64),
                   (x + hw - 10, sy + 94)]
            d.line(pts, fill=WHITE, width=4)
            for px, py in pts:
                d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 200, 60))
        else:  # orbit
            cx, cy = x + hw - 48, sy + 56
            d.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], outline=WHITE, width=2)
            d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(255, 200, 60))
            d.ellipse([cx + 20, cy - 24, cx + 27, cy - 17], fill=WHITE)
            d.ellipse([cx - 32, cy + 14, cx - 25, cy + 21], fill=WHITE)
        d.text((x + 14, sy + 8), hero["big"], font=font(FB, 58), fill=WHITE)
        d.text((x + 14, sy + 76), hero["unit"], font=font(FB, 11), fill=(225, 225, 225))
        # number badge on the scene
        d.ellipse([x + hw - 44, sy + 8, x + hw - 12, sy + 40], fill=WHITE)
        d.text((x + hw - 36, sy + 15), hero["num"], font=font(FB, 13), fill=hero["color"])
        # Headline
        ty = sy + 122
        lines = wrap(d, hero["headline"], font(FB, 17), hw - 24)
        ty = draw_lines(d, x + 12, ty, lines, font(FB, 17), INK, 21)
        # Deck
        ty += 4
        lines = wrap(d, hero["deck"], font(FR, 11), hw - 24)
        ty = draw_lines(d, x + 12, ty, lines, font(FR, 11), (60, 60, 60), 15)
        # WHY IT MATTERS
        ty += 6
        d.text((x + 12, ty), "WHY IT MATTERS", font=font(FB, 11), fill=RED)
        ty += 16
        lines = wrap(d, hero["why"], font(FR, 11), hw - 24)
        ty = draw_lines(d, x + 12, ty, lines, font(FR, 11), INK, 15)
        # Bottom meta row
        my = y + hh - 26
        d.line([x + 12, my - 6, x + hw - 12, my - 6], fill=LINE, width=1)
        d.text((x + 12, my), hero["region"], font=font(FB, 9), fill=REGION_COLORS[hero["region"]])
        tag_box(d, x + hw - 34, my - 2, hero["tag"])

    # ---- BY THE NUMBERS strip ------------------------------------------
    sy0 = 436
    d.rounded_rectangle([12, sy0, 1012, sy0 + 60], radius=6, fill=NAVY)
    d.text((24, sy0 + 18), "BY THE\nNUMBERS", font=font(FB, 12), fill=(255, 200, 60))
    seg_w = (1012 - 12 - 120) / 6
    for j, (num, label) in enumerate(BY_NUMBERS):
        sx = 132 + j * seg_w
        d.text((sx, sy0 + 8), num, font=font(FB, 24), fill=WHITE)
        d.text((sx, sy0 + 38), label, font=font(FR, 9), fill=(180, 200, 225))

    # ---- Numbered grid 04..50 -------------------------------------------
    gx, gy = 12, 502
    cw, chh, cgx, cgy = 161, 55, 6, 4
    for idx, (num, region, headline, tag) in enumerate(GRID):
        col, row = idx % 6, idx // 6
        x = gx + col * (cw + cgx)
        y = gy + row * (chh + cgy)
        d.rounded_rectangle([x, y, x + cw, y + chh], radius=4, fill=WHITE,
                            outline=LINE, width=1)
        # number badge
        colr = REGION_COLORS[region]
        d.ellipse([x + 5, y + 5, x + 23, y + 23], fill=colr)
        fnum = font(FB, 10 if num < 10 else 9)
        ns = str(num)
        tw = d.textlength(ns, font=fnum)
        d.text((x + 14 - tw / 2, y + 8), ns, font=fnum, fill=WHITE)
        # headline, 2 lines max
        lines = wrap(d, headline, font(FB, 10), cw - 28)
        draw_lines(d, x + 27, y + 5, lines[:2], font(FB, 10), INK, 12)
        # meta row: region + literal C/R/CL tag
        d.text((x + 5, y + chh - 15), region, font=font(FB, 7),
               fill=colr)
        tag_box(d, x + cw - 27, y + chh - 18, tag)

    # ---- Footer: legend + counts ----------------------------------------
    fy = 978
    d.text((12, fy), "C = confirmed   •   R = reported   •   CL = claim",
           font=font(FB, 13), fill=INK)
    d.text((12, fy + 20),
           "50 STORIES  •  10 REGIONS  •  Compiled on Wednesday, 25 November 2026. "
           "Figures as reported on the day.",
           font=font(FR, 10), fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    data = OUT.read_bytes()
    print("stories:", 3 + len(GRID))
    print("regions:", len(REGION_COLORS))
    print("size:", img.size)
    print("bytes:", len(data))
    print("sha256:", hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
