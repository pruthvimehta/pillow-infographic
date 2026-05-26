# Pillow Infographic — Claude Skill

A custom Claude Code skill by **Pruthvi Mehta** that generates beautiful, downloadable **infographic PNG images** using Python Pillow — works entirely **offline**, no API key needed, no internet required.

---

## What This Skill Does

You give Claude a topic or paste any text — it turns it into a clean, branded infographic PNG at **1080px wide**. Everything runs locally on your machine.

No Gemini. No API key. No internet connection needed.

---

## How to Trigger It

Just talk to Claude naturally:

- `/pillow-infographic 5 money habits`
- "Generate an infographic about financial planning"
- "Make an infographic as a PNG"
- "Create a downloadable infographic"
- "I want a shareable image for LinkedIn"
- "Turn this into an infographic"

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

- **Python 3** — must be installed on your machine
- **Pillow library** — install it by running:
  ```bash
  pip3 install pillow
  ```
- No API key needed
- No internet connection needed

---

## Repository Structure

```
pillow-infographic/
├── SKILL.md          # Skill instructions for Claude
├── scripts/
│   └── generate.py   # Python script that generates the infographic
└── README.md
```

---

## How It Works

1. Claude reads your topic or text input
2. Generates or structures the content points
3. Runs `generate.py` using Python Pillow to create the PNG
4. Saves and displays the infographic directly in the chat

---

Built by [Pruthvi Mehta](https://github.com/pruthvimehta)
