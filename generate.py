#!/usr/bin/env python3
"""Generate entry.png for news-image-20261118 — THE WORLD IN ONE DAY.

Draws the 1024x1024 infographic programmatically with Pillow.
All facts are from research-notes.md (verified across AP/Reuters/AFP/NYT/BBC
via JustSecurity, OpenChronicle, Horizon, OneTurn, 18 Nov 2026).
No photos, no logos, no AI-generated text. Deterministic output:
same code + same fonts -> same PNG bytes (Pillow writes no timestamps).
Run: python3 generate.py  (writes entry.png next to this file)
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (15, 42, 68)
NAVY_DARK = (10, 30, 50)
GOLD = (242, 193, 78)
RED = (192, 57, 43)
TEAL = (14, 122, 110)
AMBER = (176, 124, 0)
BLUE = (31, 76, 140)
GREY = (60, 68, 78)
PAPER = (252, 250, 245)
WHITE = (255, 255, 255)
INK = (24, 28, 34)
MUTED = (82, 90, 100)
LINE = (214, 210, 200)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
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


def draw_wrapped(draw, x, y, text, fnt, color, max_w, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.28)
    lines = wrap(draw, text, fnt, max_w)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def panel(draw, box, fill, border=None):
    draw.rounded_rectangle(box, radius=10, fill=fill,
                           outline=border, width=2 if border else 1)


def kicker_headline(draw, x, y, max_w, kicker, kcolor, headline, hsize=28):
    draw.text((x, y), kicker, font=font(BOLD, 15), fill=kcolor)
    y += 24
    y = draw_wrapped(draw, x, y, headline, font(BOLD, hsize), INK,
                     max_w, leading=hsize + 6)
    return y + 6


def stat_box(draw, x, y, w, big, label, accent):
    draw.rounded_rectangle([x, y, x + w, y + 52], radius=8, fill=accent)
    draw.text((x + 14, y + 6), big, font=font(BOLD, 22), fill=WHITE)
    draw.text((x + 14, y + 30), label, font=font(BOLD, 14), fill=WHITE)
    return y + 52


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Header (0..168) ----
    d.rectangle([0, 0, W, 168], fill=NAVY)
    d.rectangle([0, 168, W, 172], fill=GOLD)
    d.text((24, 16), "THE WORLD IN ONE DAY",
           font=font(BOLD, 44), fill=WHITE)
    d.text((24, 70), "WEDNESDAY  18 NOVEMBER 2026",
           font=font(BOLD, 36), fill=GOLD)
    d.text((24, 122),
           "Six stories that defined the day \u2014 from Shenzhen to the Gulf, "
           "Crimea to Alaska.",
           font=font(REG, 17), fill=(214, 226, 236))

    # ---- Hero: Shenzhen (24,188)-(560,520) ----
    # One combined body paragraph (16pt) so it cannot run past the stat box.
    panel(d, [24, 188, 560, 520], WHITE, LINE)
    y = kicker_headline(d, 44, 206, 496, "DIPLOMACY  \u2022  ASIA", GOLD, "XI MEETS PUTIN IN SHENZHEN", 30)
    y = draw_wrapped(d, 44, y, "Xi Jinping met Vladimir Putin in Shenzhen on 18 November, a day "
                     "before a planned trilateral summit with Donald Trump on 19 November. "
                     "Xi spoke against trade protectionism; Putin criticised Western sanctions.",
                     font(REG, 16), INK, 496, leading=20)
    stat_box(d, 44, 412, 496, "19 NOV", "TRILATERAL SUMMIT WITH TRUMP", NAVY)
    # flag bars: CN red, RU white/blue/red, US red/white/blue (drawn shapes)
    fx = 44
    for cols in [[(192, 57, 43)], [(255, 255, 255), (31, 76, 140), (192, 57, 43)],
                 [(192, 57, 43), (255, 255, 255), (31, 76, 140)]]:
        bx = fx
        for c in cols:
            d.rectangle([bx, 478, bx + 22, 492], fill=c, outline=GREY)
            bx += 22
        fx += 86
    d.text((330, 476), "CN  \u2022  RU  \u2022  US", font=font(BOLD, 14), fill=MUTED)

    # ---- Right column: Gulf (576,188)-(1000,348) ----
    panel(d, [576, 188, 1000, 348], (255, 244, 242), LINE)
    y = kicker_headline(d, 594, 200, 388, "CONFLICT  \u2022  MIDDLE EAST", RED, "GULF ON EDGE", 24)
    y = draw_wrapped(d, 594, y, "The US struck a Revolutionary Guard missile site on Iran\u2019s "
                     "Qeshm Island, in the Strait of Hormuz. Early on 18 Nov, Iran struck "
                     "Kuwait\u2019s Ali Al Salem Air Base and Bahrain.",
                     font(REG, 15), INK, 388, leading=19)

    # ---- Right column: Crimea (576,364)-(1000,520) ----
    panel(d, [576, 364, 1000, 520], (238, 242, 248), LINE)
    y = kicker_headline(d, 594, 376, 388, "WAR IN EUROPE", BLUE, "CRIMEA BRIDGE HIT AGAIN", 24)
    y = draw_wrapped(d, 594, y, "Ukraine attacked the Kerch / Crimea Bridge for a second day; "
                     "one arch and part of the road span collapsed. Zelensky called it "
                     "\u201cunprecedented\u201d \u2014 prepared for weeks, in seven stages.",
                     font(REG, 15), INK, 388, leading=19)

    # ---- Middle row (y 536..800), three panels ----
    panels = [
        (24,  "US POLITICS", BLUE, "ALASKA FLIPS THE SENATE",
         "Democrat Mary Peltola beat Republican Dan Sullivan in Alaska. "
         "Democrats take a projected majority in the incoming Senate. "
         "Last race called; biggest flip since 1958.",
         "56\u201344", "PROJECTED SENATE MAJORITY", BLUE),
        (356, "HEALTH  \u2022  AFRICA", TEAL, "EBOLA IN CONGO",
         "Nearly three-quarters of children under 5 infected with Ebola "
         "do not survive. Bunia and Beni are the epicentres.",
         "NEARLY 3 IN 4", "UNDER-5S DO NOT SURVIVE", TEAL),
        (688, "HEALTH  \u2022  USA", AMBER, "MEASLES IN THE US",
         "The US loses its measles elimination status, held for 26 years. "
         "States reported more than 5,400 cases and 10 deaths \u2014 a first "
         "since the early 1990s.",
         "5,400+ CASES", "REPORTED  \u2022  10 DEATHS", AMBER),
    ]
    for x, kick, kc, head, body, big, label, accent in panels:
        panel(d, [x, 536, x + 312, 800], WHITE, LINE)
        y = kicker_headline(d, x + 18, 552, 276, kick, kc, head, 24)
        y = draw_wrapped(d, x + 18, y, body, font(REG, 15), INK, 276, leading=19)
        stat_box(d, x + 18, 736, 276, big, label, accent)

    # ---- Footer ALSO TODAY (24,816)-(1000,1000) ----
    panel(d, [24, 816, 1000, 1000], NAVY, None)
    d.text((44, 830), "ALSO TODAY", font=font(BOLD, 18), fill=GOLD)
    briefs = [
        (44,  "ISRAEL", "Matan Kahana elected Knesset speaker, 66 of 120 votes."),
        (356, "SIBERIA", "Russian An-12 crashed near Kemerovo; all 19 on board dead."),
        (688, "NVIDIA", "Record quarterly sales; Q4 forecast $130bn. Board rules out "
         "Jensen Huang\u2019s return as CEO."),
    ]
    for x, kick, text in briefs:
        d.text((x, 862), kick, font=font(BOLD, 15), fill=GOLD)
        draw_wrapped(d, x, 886, text, font(REG, 15), WHITE, 292, leading=20)
    d.line([44, 972, 980, 972], fill=(90, 110, 130), width=1)
    d.text((44, 980), "Sources: AP, Reuters, AFP, NYT, BBC \u2014 18 Nov 2026",
           font=font(REG, 14), fill=(190, 204, 216))

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
