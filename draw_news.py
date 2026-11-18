#!/usr/bin/env python3
"""Draw the news-image entry for 17 November 2026.

A one-page newspaper front page, 1024x1024, built only from the stories
verified from live reporting on the day itself (Reuters, Al Jazeera, NPR,
BBC, Just Security's Early Edition). Run: python3 draw_news.py
Writes entry.png next to this file.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
RED = (179, 38, 30)
NAVY = (31, 56, 100)
TEAL = (14, 94, 94)
GOLD = (176, 132, 30)
GREY = (90, 88, 80)
PANEL = (255, 255, 255)
LINE = (200, 194, 178)

F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
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


def text_block(draw, x, y, text, fnt, max_w, fill=INK, leading=1.28):
    lines = wrap(draw, text, fnt, max_w)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def headline(draw, x, y, text, fnt, max_w, fill=INK, leading=1.08):
    return text_block(draw, x, y, text, fnt, max_w, fill=fill, leading=leading)


def kicker(draw, x, y, text, color=RED):
    fnt = font(F_SANS_B, 21)
    draw.text((x, y), text.upper(), font=fnt, fill=color)
    return y + 30


def panel(draw, x, y, w, h, fill=PANEL):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=fill,
                           outline=LINE, width=2)


def draw_bridge(draw, x, y, w, h):
    """Stylised Kerch Bridge over water with a blast."""
    sky = (214, 228, 240)
    draw.rectangle([x, y, x + w, y + h], fill=sky)
    # water
    draw.rectangle([x, y + h - 46, x + w, y + h], fill=(58, 110, 158))
    for i in range(5):
        wx = x + 14 + i * 62
        draw.arc([wx, y + h - 38, wx + 44, y + h - 18], 0, 180, fill=(255, 255, 255), width=3)
    # deck + pylons + cables
    deck_y = y + h - 96
    draw.rectangle([x + 8, deck_y, x + w - 8, deck_y + 10], fill=(70, 70, 74))
    for px in (x + 66, x + w - 86):
        draw.rectangle([px, y + 26, px + 12, deck_y], fill=(90, 90, 96))
    for tx in (x + 72, x + w - 80):
        draw.line([tx + 6, y + 26, x + 8, deck_y], fill=(120, 120, 126), width=2)
        draw.line([tx + 6, y + 26, x + w - 8, deck_y], fill=(120, 120, 126), width=2)
    # blast starburst over the middle of the deck
    cx, cy = x + w // 2, deck_y - 26
    for ang in range(0, 360, 30):
        import math
        r1, r2 = 12, 44
        a = math.radians(ang)
        x1, y1 = cx + r1 * math.cos(a), cy + r1 * math.sin(a)
        x2, y2 = cx + r2 * math.cos(a), cy + r2 * math.sin(a)
        draw.line([x1, y1, x2, y2], fill=(230, 120, 20), width=6)
    draw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(245, 180, 40),
                 outline=(200, 80, 10), width=3)
    draw.text((cx - 7, cy - 13), "!", font=font(F_SANS_B, 26), fill=(140, 20, 10))


def draw_tanker(draw, x, y, w, h):
    sky = (222, 234, 240)
    draw.rectangle([x, y, x + w, y + h], fill=sky)
    draw.rectangle([x, y + h - 34, x + w, y + h], fill=(46, 98, 140))
    # hull
    draw.polygon([(x + 12, y + h - 66), (x + w - 12, y + h - 66),
                  (x + w - 36, y + h - 34), (x + 36, y + h - 34)], fill=(150, 40, 30))
    # containers
    for i, col in enumerate([(210, 170, 60), (60, 120, 90)]):
        cx0 = x + 30 + i * 52
        draw.rectangle([cx0, y + h - 96, cx0 + 46, y + h - 68], fill=col,
                       outline=(60, 60, 60), width=2)
    # bridge tower
    draw.rectangle([x + w - 44, y + h - 108, x + w - 20, y + h - 66],
                   fill=(240, 240, 240), outline=(90, 90, 90), width=2)
    # small flame above the first container
    draw.polygon([(x + 44, y + h - 96), (x + 56, y + h - 122), (x + 68, y + h - 96)],
                 fill=(240, 140, 30))


def draw_flags(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 236, 244))
    fw, fh = 44, 30
    gap = (w - 3 * fw) // 4
    fy = y + 22
    for i, label in enumerate(("CN", "US", "RU")):
        fx = x + gap + i * (fw + gap)
        if label == "CN":
            draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 41, 16),
                           outline=(60, 60, 60), width=2)
            draw.text((fx + 6, fy + 4), "*", font=font(F_SANS_B, 16), fill=(255, 220, 60))
        elif label == "US":
            draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(40, 60, 140),
                           outline=(60, 60, 60), width=2)
            for r in range(3):
                yy = fy + 5 + r * 10
                draw.line([fx, yy, fx + fw, yy], fill=(255, 255, 255), width=3)
            draw.rectangle([fx, fy, fx + 18, fy + 14], fill=(40, 60, 140))
        else:
            draw.rectangle([fx, fy, fx + fw, fy + 10], fill=(255, 255, 255),
                           outline=(60, 60, 60), width=1)
            draw.rectangle([fx, fy + 10, fx + fw, fy + 20], fill=(30, 60, 160))
            draw.rectangle([fx, fy + 20, fx + fw, fy + 30], fill=(210, 30, 30),
                           outline=(60, 60, 60), width=1)
        draw.line([fx + fw // 2, fy + fh, fx + fw // 2, y + h - 24],
                  fill=(80, 80, 80), width=3)
        lw = draw.textlength(label, font=font(F_SANS_B, 14))
        draw.text((fx + fw // 2 - lw / 2, y + h - 20), label,
                  font=font(F_SANS_B, 14), fill=INK)


def draw_globe(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 236, 244))
    cx, cy, r = x + w // 2, y + h // 2 + 6, 58
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 130, 190),
                 outline=NAVY, width=3)
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(255, 255, 255), width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=2)
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 180, fill=(255, 255, 255), width=2)
    # plane
    px, py = cx + 44, cy - 52
    draw.polygon([(px, py), (px + 26, py + 8), (px, py + 12), (px - 6, py + 4)],
                 fill=RED)


def draw_barrier(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
    # road
    draw.rectangle([x, y + h - 34, x + w, y + h], fill=(90, 90, 90))
    for i in range(6):
        wx = x + 10 + i * 34
        draw.rectangle([wx, y + h - 18, wx + 18, y + h - 14], fill=(255, 255, 255))
    # barrier stripes
    bx, by = x + 18, y + 26
    for i in range(5):
        col = (200, 30, 30) if i % 2 == 0 else (255, 255, 255)
        draw.rectangle([bx + i * 34, by, bx + (i + 1) * 34, by + 22], fill=col,
                       outline=(60, 60, 60), width=1)
    draw.rectangle([bx, by + 22, bx + 8, y + h - 34], fill=(60, 60, 60))
    draw.rectangle([bx + 162, by + 22, bx + 170, y + h - 34], fill=(60, 60, 60))
    # sign
    draw.rounded_rectangle([x + w - 78, y + 30, x + w - 14, y + 74], radius=6,
                           fill=(255, 255, 255), outline=RED, width=3)
    draw.text((x + w - 66, y + 38), "STOP", font=font(F_SANS_B, 20), fill=RED)


def draw_virus(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(244, 228, 228))
    cx, cy = x + w // 2, y + h // 2
    for ang in range(0, 360, 45):
        import math
        a = math.radians(ang)
        x1, y1 = cx + 34 * math.cos(a), cy + 34 * math.sin(a)
        x2, y2 = cx + 52 * math.cos(a), cy + 52 * math.sin(a)
        draw.line([x1, y1, x2, y2], fill=(179, 38, 30), width=5)
        draw.ellipse([x2 - 6, y2 - 6, x2 + 6, y2 + 6], fill=(179, 38, 30))
    draw.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=(210, 70, 60),
                 outline=(140, 20, 15), width=3)
    for dx, dy in ((-14, -8), (10, -14), (-4, 12), (16, 10)):
        draw.ellipse([cx + dx - 6, cy + dy - 6, cx + dx + 6, cy + dy + 6],
                     fill=(140, 20, 15))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin

    # ---- Masthead ----
    d.text((M, 22), "THE WORLD IN ONE DAY", font=font(F_SERIF, 58), fill=INK)
    d.line([M, 96, W - M, 96], fill=INK, width=4)
    d.line([M, 102, W - M, 102], fill=INK, width=2)
    d.text((M, 112), "TUESDAY, 17 NOVEMBER 2026",
           font=font(F_SANS_B, 26), fill=RED)
    right_label = "SIX STORIES  •  EVERY REGION"
    rl_font = font(F_SANS_B, 20)
    d.text((W - M - d.textlength(right_label, font=rl_font), 114),
           right_label, font=rl_font, fill=GREY)

    # ---- Lead story: Kerch Bridge ----
    x, y, w, h = M, 158, W - 2 * M, 296
    panel(d, x, y, w, h)
    tx = x + 24
    ty = y + 16
    ty = kicker(d, tx, ty, "Europe — Russia-Ukraine war")
    ty = headline(d, tx, ty, "BRIDGES UNDER FIRE",
                  font(F_SERIF, 46), 540, leading=1.05)
    ty += 6
    ty = text_block(d, tx, ty,
                    "Ukraine struck the Kerch Bridge linking Russia to "
                    "Crimea for a second straight day — President Zelenskyy "
                    "hailed an \u201cunprecedented operation\u201d. Russia hit "
                    "river crossings in Kyiv in reply.",
                    font(F_SANS, 22), 540)
    draw_bridge(d, x + w - 392, y + 16, 368, h - 32)

    # ---- Row 2: two stories ----
    y2, h2 = 470, 232
    w2 = (W - 2 * M - 16) // 2
    # Hormuz
    panel(d, M, y2, w2, h2)
    tx = M + 18
    ty = kicker(d, tx, y2 + 12, "Middle East — Shipping")
    ty = headline(d, tx, ty, "TANKERS HIT NEAR HORMUZ",
                  font(F_SERIF, 25), w2 - 206, leading=1.05)
    ty += 4
    text_block(d, tx, ty,
               "Two tankers struck mines and caught fire near the Strait "
               "of Hormuz, Iran said. Drones fired at a US radar base in "
               "Bahrain were intercepted.",
               font(F_SANS, 17), w2 - 206)
    draw_tanker(d, M + w2 - 180, y2 + 52, 168, h2 - 68)
    # Summit
    x3 = M + w2 + 16
    panel(d, x3, y2, w2, h2)
    tx = x3 + 18
    ty = kicker(d, tx, y2 + 12, "Asia-Pacific — Diplomacy", color=NAVY)
    ty = headline(d, tx, ty, "XI, TRUMP & PUTIN TO MEET",
                  font(F_SERIF, 25), w2 - 206, leading=1.05)
    ty += 4
    text_block(d, tx, ty,
               "Beijing confirms the three leaders will meet in Shenzhen "
               "on Thursday, on the sidelines of the APEC summit China "
               "is hosting.",
               font(F_SANS, 17), w2 - 206)
    draw_flags(d, x3 + w2 - 180, y2 + 52, 168, h2 - 68)

    # ---- Row 3: three stories ----
    y3, h3 = 718, 196
    w3 = (W - 2 * M - 32) // 3
    stories = [
        ("Asia — Summit", "TRUMP LANDS IN MANILA",
         "The US president arrives for the ASEAN summit, then flies "
         "to China for talks on denuclearisation, Iran, Ukraine "
         "and trade.", NAVY, draw_globe),
        ("Europe — Security", "ESTONIA SHUTS RUSSIA BORDER",
         "Estonia will close its border crossings with Russia from "
         "1 December, citing a foiled Russian plot to bomb a "
         "drone plant.", RED, draw_barrier),
        ("Americas — Health", "US LOSES MEASLES-FREE STATUS",
         "The United States loses its measles-elimination status "
         "after nearly 30 years, amid its worst outbreak in "
         "over three decades.", TEAL, draw_virus),
    ]
    for i, (kick, head, body, col, icon) in enumerate(stories):
        px = M + i * (w3 + 16)
        panel(d, px, y3, w3, h3)
        tx = px + 16
        ty = kicker(d, tx, y3 + 12, kick, color=col)
        ty = headline(d, tx, ty, head, font(F_SERIF, 23), w3 - 32, leading=1.05)
        ty += 4
        text_block(d, tx, ty, body, font(F_SANS, 16), w3 - 32)
    # Row 3 stays text-led; the lead and row-2 illustrations carry the art.

    # ---- Bottom strip ----
    y4 = 930
    d.rectangle([M, y4, W - M, y4 + 56], fill=NAVY)
    d.text((M + 16, y4 + 6), "ALSO TODAY:",
           font=font(F_SANS_B, 20), fill=(255, 210, 90))
    text_block(d, M + 170, y4 + 8,
               "Depardieu admits a sexual-assault charge in a Paris court  •  "
               "Japan scrambles jets as Russian planes enter its airspace  •  "
               "Britain sanctions eight Israeli settlement builders",
               font(F_SANS, 18), W - 2 * M - 186, fill=(255, 255, 255))

    # ---- Footer ----
    foot = "Drawn from live reporting: Reuters  •  Al Jazeera  •  NPR  •  BBC  •  Just Security"
    d.text((M, 996), foot, font=font(F_SANS, 15), fill=GREY)
    right = "make.fun  •  @raju-pramana"
    rf = font(F_SANS, 15)
    d.text((W - M - d.textlength(right, font=rf), 996), right, font=rf, fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
