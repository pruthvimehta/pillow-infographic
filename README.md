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

1. Click **`<> Code`** → **`Download ZIP`**
2. Go to **[claude.ai](https://claude.ai)** → **Skills** → **Create Skill**
3. Upload the **ZIP file** directly → **Save**

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

---

## Connect with Pruthvi

- Instagram: [instagram.com/ca.pruthvimehta](https://instagram.com/ca.pruthvimehta)
- LinkedIn: [linkedin.com/in/pruthvimehta](https://linkedin.com/in/pruthvimehta)
- YouTube: [youtube.com/@ca.pruthvimehta](https://youtube.com/@ca.pruthvimehta)
