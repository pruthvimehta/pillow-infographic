# Claude Skills Repository

A personal collection of custom Claude Code skills built by **Pruthvi Mehta**.

---

## What is a Skill?

A **skill** is a set of instructions that teaches Claude how to perform a specific task — like generating an infographic or optimizing content for search engines. Once installed, you can trigger a skill by typing a command or describing what you want.

---

## Skills in this Repository

### 1. `pillow-infographic`
Generates a visually rich **1080x1350px infographic image** from any topic or block of text using Google's Gemini Imagen API.

**How to trigger:**
- Type `/generate-infographic <your topic>`
- Say "generate an infographic about X"
- Say "make this visual" or "turn this into an infographic"
- Paste a block of text and ask for a visual summary

**What it does:**
1. Extracts key points from your input
2. Asks you to pick a visual style (Professional, Bold & Dark, or Sketch/Cartoon)
3. Generates a high-quality infographic image
4. Displays it inline in the chat

**Requires:** Google Gemini API key (set inside the script)

---

### 2. `seo-aeo-geo`
Optimizes any content for **SEO** (Search Engine Optimization), **AEO** (Answer Engine Optimization), and **GEO** (Generative Engine Optimization) — making your writing more discoverable, answerable, and AI-citable.

**How to trigger:**
- Say "optimize this for SEO"
- Say "make this AEO-friendly" or "GEO optimize this"
- Say "help this rank" or "make this AI-friendly"
- Paste any draft and say "improve discoverability"
- Ask "will this rank?" or "can AI find this?"

**Works with:** LinkedIn posts, Instagram captions, articles, newsletters, reels, carousels, and more.

**Output includes:**
- Optimized version of your content
- SEO / AEO / GEO breakdown
- Content scorecard (scored out of 10)
- Keywords and entities
- Bonus upgrade suggestions

---

## How to Install a Skill

1. **Download** the skill folder from this repository
2. **Place it** inside your Claude skills directory:
   ```
   ~/.claude/skills/<skill-name>/
   ```
3. **Restart Claude Code** — the skill will be automatically detected and available

### Example

```bash
# Clone this repository
git clone git@github.com:pruthvimehta/Claude-skills-.git

# Copy a skill to your Claude skills directory
cp -r Claude-skills-/seo-aeo-geo ~/.claude/skills/seo-aeo-geo
cp -r Claude-skills-/pillow-infographic ~/.claude/skills/pillow-infographic
```

---

## How to Use a Skill

Once installed, just talk to Claude naturally — skills are triggered automatically based on what you say.

You can also use the explicit slash command format:
```
/seo-aeo-geo
/generate-infographic
```

---

## Repository Structure

```
Claude-skills-/
├── pillow-infographic/
│   ├── SKILL.md               # Skill instructions for Claude
│   └── scripts/
│       └── generate_image.py  # Python script for image generation
├── seo-aeo-geo/
│   └── SKILL.md               # Skill instructions for Claude
└── README.md
```

---

## Adding More Skills

To contribute or add your own skill:

1. Create a folder with your skill name inside this repo
2. Add a `SKILL.md` file with the skill instructions
3. Add any supporting scripts in a `scripts/` subfolder
4. Push to GitHub

```bash
git add .
git commit -m "Add <skill-name> skill"
git push origin main
```
