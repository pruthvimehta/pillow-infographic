#!/usr/bin/env python3
"""
Pillow Infographic Generator
Reads /tmp/infographic_input.json and writes a PNG to /mnt/user-data/outputs/

Supports:
- 3 preset styles: professional, bold_dark, soft_warm
- Custom colours: just provide bg + accent hex
- Google Fonts: any font name downloaded automatically from GitHub
- Falls back to DejaVu Sans if font unavailable
"""

import json, os, re, time, urllib.request
from PIL import Image, ImageDraw, ImageFont

INPUT_FILE  = "/tmp/infographic_input.json"
FONT_CACHE  = "/tmp/gfonts_cache"
os.makedirs(FONT_CACHE, exist_ok=True)

# ── Preset styles ─────────────────────────────────────────────────────────────

STYLES = {
    "professional": {
        "bg": "#FFFFFF", "card_bg": "#F7F7F7", "card_border": "#EEEEEE",
        "accent": "#FF6B6B", "accent_dark": "#993333", "title": "#1a1a1a",
        "body": "#555555", "quote_bg": "#FFF0F0", "tag_fg": "#FFFFFF",
        "num_fg": "#FFFFFF", "footer": "#888888",
    },
    "bold_dark": {
        "bg": "#0D1B2A", "card_bg": "#142233", "card_border": "#1E3348",
        "accent": "#FFD700", "accent_dark": "#B8960C", "title": "#FFFFFF",
        "body": "#C8D8E8", "quote_bg": "#142233", "tag_fg": "#0D1B2A",
        "num_fg": "#0D1B2A", "footer": "#7A9BB5",
    },
    "soft_warm": {
        "bg": "#FAFAF5", "card_bg": "#F0F7F4", "card_border": "#D4EDE5",
        "accent": "#2BB5A0", "accent_dark": "#1A7A6E", "title": "#1a1a1a",
        "body": "#4A5568", "quote_bg": "#E8F7F4", "tag_fg": "#FFFFFF",
        "num_fg": "#FFFFFF", "footer": "#888888",
    },
}

# ── Colour utilities ──────────────────────────────────────────────────────────

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b):
    return f"#{int(r):02X}{int(g):02X}{int(b):02X}"

def is_dark(h):
    r, g, b = hex_to_rgb(h)
    return (0.299*r + 0.587*g + 0.114*b) < 128

def darken(h, f=0.6):
    r, g, b = hex_to_rgb(h)
    return rgb_to_hex(r*f, g*f, b*f)

def lighten(h, mix=0.88):
    r, g, b = hex_to_rgb(h)
    return rgb_to_hex(r+(255-r)*mix, g+(255-g)*mix, b+(255-b)*mix)

def nudge(h, amt=20):
    r, g, b = hex_to_rgb(h)
    return rgb_to_hex(min(r+amt,255), min(g+amt,255), min(b+amt,255))

def resolve_style(data):
    key = data.get("style", "professional")
    if key in STYLES:
        return STYLES[key]
    c  = data.get("colors", {})
    bg = c.get("bg", "#FFFFFF")
    ac = c.get("accent", "#4A90D9")
    dark_bg = is_dark(bg)
    dark_ac = is_dark(ac)
    if dark_bg:
        card_bg = nudge(bg, 20); card_border = nudge(bg, 38); quote_bg = card_bg
    else:
        card_bg = c.get("card_bg", lighten(ac, 0.92))
        card_border = c.get("card_border", lighten(ac, 0.80))
        quote_bg = c.get("quote_bg", lighten(ac, 0.88))
    return {
        "bg": bg, "card_bg": c.get("card_bg", card_bg),
        "card_border": c.get("card_border", card_border),
        "accent": ac, "accent_dark": c.get("accent_dark", darken(ac, 0.65)),
        "title":  c.get("title",  "#FFFFFF" if dark_bg else "#1a1a1a"),
        "body":   c.get("body",   "#C0D0E0" if dark_bg else "#555555"),
        "quote_bg": c.get("quote_bg", quote_bg),
        "tag_fg": c.get("tag_fg", "#FFFFFF" if dark_ac else "#1a1a1a"),
        "num_fg": c.get("num_fg", "#FFFFFF" if dark_ac else "#1a1a1a"),
        "footer": c.get("footer", "#7A9BB5" if dark_bg else "#888888"),
    }

# ── Google Fonts downloader ───────────────────────────────────────────────────

def _try_url(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = r.read()
        return data if len(data) > 10_000 else None
    except Exception:
        return None

def download_google_font(family, bold=False):
    """
    Download a Google Font TTF from the GitHub mirror.
    Returns local path or None on failure.
    """
    style = "Bold" if bold else "Regular"
    fl = family.lower().replace(" ", "")   # folder name
    fc = family.replace(" ", "")           # file prefix (no spaces)
    cache_path = os.path.join(FONT_CACHE, f"{fl}-{style}.ttf")

    if os.path.exists(cache_path):
        return cache_path

    base = "https://raw.githubusercontent.com/google/fonts/main"
    attempts = [
        f"{base}/ofl/{fl}/{fc}-{style}.ttf",
        f"{base}/ofl/{fl}/static/{fc}-{style}.ttf",
        f"{base}/apache/{fl}/{fc}-{style}.ttf",
        f"{base}/apache/{fl}/static/{fc}-{style}.ttf",
        f"{base}/ofl/{fl}/{fc}[wght].ttf",
        f"{base}/ofl/{fl}/{fc}[wdth,wght].ttf",
        f"{base}/ofl/{fl}/static/{fc}_18pt-{style}.ttf",
    ]

    for url in attempts:
        data = _try_url(url)
        if data:
            with open(cache_path, "wb") as f:
                f.write(data)
            print(f"Font downloaded: {family} {style}")
            return cache_path

    print(f"Font not found: {family} {style} — falling back to system font")
    return None

# ── Font loader ───────────────────────────────────────────────────────────────

SYSTEM_FONTS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans{bold}.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans{bold}.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]

def load_font(size, bold=False, family=None):
    """Load a font by family name (Google Font) or fall back to system font."""
    bold_suffix = "-Bold" if bold else ""

    # Try Google Font first if family specified
    if family:
        path = download_google_font(family, bold=bold)
        if path:
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass

    # System font fallback
    for pattern in SYSTEM_FONTS:
        path = pattern.format(bold="-Bold" if bold else "")
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue

    return ImageFont.load_default()

# ── Text wrapping ─────────────────────────────────────────────────────────────

def wrap(draw, text, font, max_w):
    words, lines, current = text.split(), [], ""
    for word in words:
        test = (current + " " + word).strip()
        if draw.textbbox((0, 0), test, font=font)[2] <= max_w:
            current = test
        else:
            if current: lines.append(current)
            current = word
    if current: lines.append(current)
    return lines

# ── Constants ─────────────────────────────────────────────────────────────────

W = 1080
PAD = 72

# ── Height estimation ─────────────────────────────────────────────────────────

def estimate_height(data, fonts):
    d = ImageDraw.Draw(Image.new("RGB", (W, 100)))
    y = 60
    if data.get("tag"): y += 72
    y += len(wrap(d, data["title"], fonts["title"], W-2*PAD)) * 62 + 12
    if data.get("subtitle"): y += 40
    y += 48
    for sec in data["sections"]:
        h = wrap(d, sec["heading"], fonts["section"], W-2*PAD-90)
        b = [wrap(d, b, fonts["bullet"], W-2*PAD-100) for b in sec["bullets"]]
        y += 30 + len(h)*38 + 18 + sum(len(bl)*34+10 for bl in b) + 30 + 28
    if data.get("quote"):
        q = wrap(d, f'"{data["quote"]}"', fonts["quote"], W-2*PAD-30)
        y += max(130, len(q)*34+50) + 28
    return y + 80 + 40

# ── Output path ───────────────────────────────────────────────────────────────

def get_output_dir():
    for p in ["/mnt/user-data/outputs", os.path.expanduser("~/Downloads"), "/tmp"]:
        if os.path.exists(p) and os.access(p, os.W_OK):
            return p
    return "/tmp"

# ── Helpers ───────────────────────────────────────────────────────────────────

def draw_circle(draw, cx, cy, r, fill):
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=fill)

def centered(draw, text, font, y, color):
    bb = draw.textbbox((0, 0), text, font=font)
    draw.text(((W-(bb[2]-bb[0]))//2, y), text, font=font, fill=color)
    return bb[3]-bb[1]

# ── Main render ───────────────────────────────────────────────────────────────

def render(data):
    c      = resolve_style(data)
    family = data.get("font")  # optional Google Font name

    fonts = {
        "tag":     load_font(24, bold=True,  family=family),
        "title":   load_font(52, bold=True,  family=family),
        "sub":     load_font(26, bold=False, family=family),
        "section": load_font(30, bold=True,  family=family),
        "bullet":  load_font(25, bold=False, family=family),
        "quote":   load_font(25, bold=False, family=family),
        "footer":  load_font(24, bold=False, family=family),
        "num":     load_font(32, bold=True,  family=family),
    }

    H   = estimate_height(data, fonts)
    img = Image.new("RGB", (W, H), c["bg"])
    draw = ImageDraw.Draw(img)
    y   = 60

    # Tag pill
    if data.get("tag"):
        t = data["tag"].upper()
        bb = draw.textbbox((0,0), t, font=fonts["tag"])
        tw = bb[2]-bb[0]
        tx = (W-tw-40)//2
        draw.rounded_rectangle([tx, y, tx+tw+40, y+44], radius=22, fill=c["accent"])
        draw.text((tx+20, y+8), t, font=fonts["tag"], fill=c["tag_fg"])
        y += 72

    # Title
    for line in wrap(draw, data["title"], fonts["title"], W-2*PAD):
        h = centered(draw, line, fonts["title"], y, c["title"])
        y += h+8
    y += 4

    # Subtitle
    if data.get("subtitle"):
        centered(draw, data["subtitle"], fonts["sub"], y, c["body"])
        y += 40

    # Divider
    draw.rectangle([W//2-40, y, W//2+40, y+5], fill=c["accent"])
    y += 42

    # Sections
    for i, sec in enumerate(data["sections"]):
        hlines = wrap(draw, sec["heading"], fonts["section"], W-2*PAD-90)
        bsets  = [wrap(draw, b, fonts["bullet"], W-2*PAD-100) for b in sec["bullets"]]
        card_h = 30 + len(hlines)*38 + 18 + sum(len(bl)*34+10 for bl in bsets) + 30
        y1, y2 = y, y+card_h
        draw.rounded_rectangle([PAD-10, y1, W-PAD+10, y2], radius=18,
                                fill=c["card_bg"], outline=c["card_border"], width=2)
        draw.rounded_rectangle([PAD-10, y1+20, PAD-2, y2-20], radius=4, fill=c["accent"])
        cx, cy = PAD+30, y1+36
        draw_circle(draw, cx, cy, 26, c["accent"])
        nb = draw.textbbox((0,0), str(i+1), font=fonts["num"])
        draw.text((cx-(nb[2]-nb[0])//2, cy-(nb[3]-nb[1])//2-2),
                  str(i+1), font=fonts["num"], fill=c["num_fg"])
        tx2, ty = PAD+68, y1+18
        for line in hlines:
            draw.text((tx2, ty), line, font=fonts["section"], fill=c["title"]); ty += 38
        ty += 10
        for bl in bsets:
            draw.ellipse([tx2, ty+11, tx2+8, ty+19], fill=c["accent"])
            for line in bl:
                draw.text((tx2+18, ty), line, font=fonts["bullet"], fill=c["body"]); ty += 34
            ty += 6
        y = y2+28

    # Quote
    if data.get("quote"):
        qlines = wrap(draw, f'"{data["quote"]}"', fonts["quote"], W-2*PAD-30)
        qh = max(130, len(qlines)*34+50)
        draw.rounded_rectangle([PAD-10, y, W-PAD+10, y+qh], radius=14,
                                fill=c["quote_bg"], outline=c["accent"], width=3)
        draw.rectangle([PAD-10, y+20, PAD-2, y+qh-20], fill=c["accent"])
        qy = y+18
        for ql in qlines:
            draw.text((PAD+14, qy), ql, font=fonts["quote"], fill=c["accent_dark"]); qy += 34
        y += qh+28

    # Footer
    if data.get("byline"):
        fb = draw.textbbox((0,0), data["byline"], font=fonts["footer"])
        draw.text(((W-(fb[2]-fb[0]))//2, y+10), data["byline"],
                  font=fonts["footer"], fill=c["footer"])
        draw.ellipse([W//2-4, y+52, W//2+4, y+60], fill=c["accent"])

    out = os.path.join(get_output_dir(), f"infographic_{int(time.time())}.png")
    img.save(out, "PNG")
    print(out)
    return out

if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        data = json.load(f)
    render(data)
