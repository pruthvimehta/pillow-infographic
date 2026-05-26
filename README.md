# Pillow Infographic — Claude Skill

A custom Claude Code skill by **Pruthvi Mehta** that generates visually rich **1080x1350px infographic images** from any topic or block of text using Google's Gemini Imagen API.

---

## What This Skill Does

You give Claude a topic or paste any text — it turns it into a beautiful, shareable infographic image. No design tool needed.

It supports 3 visual styles:
- 🟡 **Professional** — Clean white background with coral accents. LinkedIn-ready.
- 🌑 **Bold & Dark** — Deep navy with gold accents. Premium, high-contrast look.
- ✏️ **Sketch / Cartoon** — Hand-drawn doodle style. Great for Instagram.

---

## How to Trigger It

Just talk to Claude naturally:

- `/generate-infographic 5 money habits`
- "Generate an infographic about financial planning"
- "Make this visual" *(paste any text)*
- "Turn this into an infographic"
- "Create a visual summary of this"

---

## How to Install

### Step 1 — Download

1. Go to [github.com/pruthvimehta/pillow-infographic](https://github.com/pruthvimehta/pillow-infographic)
2. Click the green **`< > Code`** button
3. Click **`Download ZIP`**
4. Unzip the downloaded file — you'll get a folder called `pillow-infographic-main`

### Step 2 — Copy to Claude

Open your **Terminal** and run:

```bash
cp -r ~/Downloads/pillow-infographic-main ~/.claude/skills/pillow-infographic
```

### Step 3 — Restart Claude Code

Close and reopen Claude Code — the skill will be automatically detected and ready to use.

---

## Requirements

- **Google Gemini API key** — stored inside `scripts/generate_image.py`
- **Python 3** — must be installed on your machine

---

## Repository Structure

```
pillow-infographic/
├── pillow-infographic/
│   ├── SKILL.md               # Skill instructions for Claude
│   └── scripts/
│       └── generate_image.py  # Python script that calls Gemini API
└── README.md
```

---

## How It Works

1. Claude reads your topic or text input
2. Asks you to pick a visual style
3. Builds a detailed image prompt
4. Runs `generate_image.py` to call the Gemini API
5. Displays the generated infographic directly in the chat

---

Built by [Pruthvi Mehta](https://github.com/pruthvimehta)
