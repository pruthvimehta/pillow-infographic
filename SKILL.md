---
name: pillow-infographic
description: Generate a professional downloadable infographic PNG entirely locally using Python Pillow — no external API needed, no Gemini, no internet. Use this skill when the user asks to "generate an infographic", "make an infographic", "create an infographic as a PNG", "download an infographic", or wants a shareable image file for LinkedIn or Instagram. This skill works offline and produces a clean, branded PNG at 1080px wide. ALWAYS trigger this skill when the user wants a downloadable infographic file.
---

> **Skill by [Pruthvi Mehta](https://www.linkedin.com/in/pruthvimehta/)** — CA & Content Creator
> Instagram: [@ca.pruthvimehta](https://www.instagram.com/ca.pruthvimehta/) | LinkedIn: [pruthvimehta](https://www.linkedin.com/in/pruthvimehta/)

---
# Pillow Infographic Generator

Generate beautiful, downloadable infographic PNGs using Python Pillow — works entirely offline, no API key needed, no internet required.

---

## Step 1 — Gather Content

**If the user provides a topic only** (no points), ask first:
> "Should I generate the content points for you, or will you provide them?"

- If generating: produce 3–5 punchy, insight-driven sections with 2–3 bullets each. Match the user's niche, tone, and audience.
- If user provides content: use it as-is without changing wording.

Confirm the following before proceeding:
- Title of the infographic
- Number of sections (2–5 recommended)
- Section headings + 2–3 bullet points each
- A closing quote or insight (optional but recommended)
- Byline — always ask: "What should the byline say? For example: By [Your Name] | [Your Role]"
- Tag label at the top (optional) — e.g. "MARKETING TIPS" or "PRODUCTIVITY INSIGHTS"
- Subtitle under the title (optional) — one short line

---

## Step 2 — Ask for Style & Colours

Ask the user which style they want:

> Which style do you prefer?
> 1. 🟡 **Professional** — White background, coral (#FF6B6B) accents, clean LinkedIn-ready layout
> 2. 🎨 **Bold & Dark** — Deep navy background, gold accents, premium high-contrast look
> 3. 🌿 **Soft & Warm** — Cream background, teal + orange palette, friendly and approachable
> 4. 🎨 **Custom** — Pick your own background and accent colour

**If user picks Custom**, ask:
> "What background colour would you like? (e.g. #1A1A2E or 'dark purple')"
> "What accent colour? (e.g. #E94560 or 'bright red') — this will be used for headings, badges, and highlights"

You only need these 2 colours. Everything else (card backgrounds, text colours, borders, quote box) is automatically derived. But if the user wants to override anything else, they can also provide:
- `title` — heading text colour
- `body` — body/bullet text colour
- `card_bg` — card background colour
- `card_border` — card border colour
- `quote_bg` — quote box background
- `accent_dark` — darker version of accent for quote text
- `footer` — footer text colour
- `tag_fg` — text colour on the tag pill
- `num_fg` — text colour on the number badges

If the user gives a colour name (e.g. "dark navy", "mint green"), convert it to the closest hex value yourself before writing the JSON.

Wait for the user's response before generating.

---


## Step 2b — Ask for Font (Optional)

Ask the user if they want a custom font:
> "Would you like a specific font? You can choose any Google Font — for example: Poppins, Montserrat, Playfair Display, Raleway, Nunito, Oswald, Space Grotesk, Outfit, Plus Jakarta Sans. Leave blank to use the default clean system font."

If the user picks a font, add `"font": "Font Name"` to the JSON. The font downloads automatically — no installation needed.

**Popular Google Fonts that work well:**

| Font | Best For |
|------|----------|
| Poppins | Modern, clean, versatile — great all-rounder |
| Montserrat | Bold headers, startup / brand feel |
| Playfair Display | Elegant, editorial, luxury |
| Raleway | Minimal, geometric, sophisticated |
| Nunito | Friendly, rounded, approachable |
| Oswald | Strong, condensed, impactful headers |
| Space Grotesk | Tech, developer, modern brand |
| Outfit | Clean, contemporary, neutral |
| Plus Jakarta Sans | Professional, Indonesian design community favourite |

If the requested font isn't found, the script automatically falls back to the system font — so it never crashes.

---
## Step 3 — Install Pillow (if needed)

Before running the script, ensure Pillow is installed:

```bash
pip install pillow --break-system-packages -q
```

---

## Step 4 — Generate the PNG

### Input JSON format

**Preset style:**
```json
{
  "title": "Your Infographic Title",
  "subtitle": "Optional one-line subtitle",
  "tag": "OPTIONAL TAG LABEL",
  "style": "professional",
  "font": "Poppins",
  "sections": [
    {
      "heading": "Section One Heading",
      "bullets": [
        "First bullet point here",
        "Second bullet point here",
        "Third bullet point here"
      ]
    }
  ],
  "quote": "Optional closing quote or insight text",
  "byline": "By Your Name | Your Role"
}
```

**Custom colours:**
```json
{
  "title": "Your Infographic Title",
  "subtitle": "Optional one-line subtitle",
  "tag": "OPTIONAL TAG LABEL",
  "style": "custom",
  "colors": {
    "bg": "#1A1A2E",
    "accent": "#E94560"
  },
  "sections": [
    {
      "heading": "Section One Heading",
      "bullets": [
        "First bullet point here",
        "Second bullet point here",
        "Third bullet point here"
      ]
    }
  ],
  "quote": "Optional closing quote or insight text",
  "byline": "By Your Name | Your Role"
}
```

**Full custom override (optional — only if user wants full control):**
```json
"colors": {
  "bg": "#1A1A2E",
  "accent": "#E94560",
  "accent_dark": "#A01030",
  "title": "#FFFFFF",
  "body": "#AAAACC",
  "card_bg": "#2A2A4E",
  "card_border": "#3A3A5E",
  "quote_bg": "#2A2A4E",
  "tag_fg": "#FFFFFF",
  "num_fg": "#FFFFFF",
  "footer": "#7777AA"
}
```

**Style values:** `"professional"` | `"bold_dark"` | `"soft_warm"` | `"custom"`

**Optional fields:** `tag`, `subtitle`, `quote` — omit if not needed

### Run the script

Write content to `/tmp/infographic_input.json`, then:

```bash
python3 PATH_TO_SKILL/scripts/generate.py
```

Replace `PATH_TO_SKILL` with the actual path where the skill is installed.

**Output location:** Script tries these in order, saves to first writable one:
1. `/mnt/user-data/outputs/` (Claude Desktop / claude.ai)
2. `~/Downloads/`
3. `/tmp/`

---

## Step 5 — Present the File

Use `present_files` to share the PNG. Then ask:
> "Want any tweaks — wording, colours, layout, font size, or byline?"

Iterate as needed by updating the JSON and rerunning the script.

---

## Style Reference

| Style | Background | Accent | Best For |
|-------|-----------|--------|----------|
| `professional` | White #FFFFFF | Coral #FF6B6B | LinkedIn, business content |
| `bold_dark` | Navy #0D1B2A | Gold #FFD700 | Premium, finance, tech |
| `soft_warm` | Cream #FAFAF5 | Teal #2BB5A0 | Instagram, lifestyle, wellness |
| `custom` | Your choice | Your choice | Brand colours, personal style |

---

## Notes

- Canvas width is fixed at 1080px; height auto-computes based on content — nothing gets cut off
- For custom colours, only `bg` and `accent` are required — everything else is auto-derived smartly
- The script detects if your background is dark or light and adjusts text colours accordingly
- Fonts used: DejaVu Sans (pre-installed on Ubuntu/Linux) — no download needed
- On Mac/Windows, the script falls back to the system default font if DejaVu isn't found
- Output is always a PNG, ready for LinkedIn, Instagram, or WhatsApp
- The script handles text wrapping automatically — no manual line breaks needed
- Works entirely offline — no API key, no subscription, no usage limits

---

## Credits

**Skill built by Pruthvi Mehta**
Chartered Accountant | Content Creator | Personal Finance & AI

- Instagram: [@ca.pruthvimehta](https://www.instagram.com/ca.pruthvimehta/)
- LinkedIn: [linkedin.com/in/pruthvimehta](https://www.linkedin.com/in/pruthvimehta/)

This skill is free to use and share. If you find it useful, a credit to Pruthvi Mehta would be appreciated.
