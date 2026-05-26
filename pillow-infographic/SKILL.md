---
name: generate-infographic
description: Generates a visually rich 1080x1350px infographic image from any topic or block of text using Google's Gemini Imagen API. ALWAYS trigger this skill when the user: - Asks to "generate an infographic", "make an infographic", "create an infographic", or "visualize this as an infographic" - Uses the `/generate-infographic` command followed by any text or topic - Says things like "turn this into an infographic", "make this visual", "infographic about X", "design an infographic for Y" - Pastes a block of text and asks for a visual summary or visual explainer. Even if the user doesn't say "infographic" but clearly wants a visually designed, shareable image that communicates information — trigger this skill.
---

# Generate Infographic

You have access to Google's Gemini Imagen API to generate high-quality infographic images at 1080x1350px (portrait, ~4:5 ratio).

## Step 1 — Extract the Topic

Parse the user's input to understand the core topic or content to be visualized. The input may come:

- After a `/generate-infographic` command (e.g. `/generate-infographic 5 money habits`)
- As a full block of text to be summarized visually
- As a short topic phrase

If the input is a long block of text, distill it into 6-8 key points that will make the infographic clear and educational.

If the input is very short (2-3 words only), ask for a bit more detail before generating.

## Step 2 — Ask for Style Preference

Before generating, ask the user which visual style they want:

> Which style do you prefer for this infographic?
> 1. 🟡 **Professional** — Clean, minimal layout. White background with coral/pink accents. Bold typography, numbered sections, connector lines. LinkedIn-ready.
> 2. 🎨 **Bold & Dark** — Deep navy background with gold accents. Premium, high-contrast look. Great for AI, finance, and career topics.
> 3. ✏️ **Sketch / Cartoon** — Hand-drawn doodle aesthetic. Teal & orange palette. Playful icons, sketch-style arrows. Great for Instagram and younger audiences.

Wait for the user's response (they can say "1", "2", "3", "professional", "navy", "sketch", etc.) before proceeding.

## Step 3 — Build the Image Prompt

Based on the chosen style, craft a **detailed, specific image generation prompt** using the templates below. Fill in `[TOPIC]`, `[KEY_POINTS]`, and `[TITLE]` from the user's content.

---

### Style 1: Professional (White & Coral)

```
A professional, clean infographic poster titled "[TITLE]" about [TOPIC].

Visual style:
- Pure white (#FFFFFF) background filling the entire canvas
- Coral pink (#FF6B6B) as the primary accent color for headers and badges
- Dark charcoal (#1a1a1a) for body text
- Numbered circular badges in coral with white numbers for each section
- Thin coral connector lines linking sections in a vertical flow layout
- Clean geometric shapes — rounded rectangles — as section containers
- Consistent spacing and visual hierarchy throughout
- Professional LinkedIn-style infographic, minimal icons, clean typography

Content to include (as sections with bullets):
[KEY_POINTS]

Dimensions: tall portrait format (4:5 ratio). No watermarks, no extra borders. Infographic only.
```

---

### Style 2: Bold & Dark (Navy & Gold)

```
A premium, bold infographic poster titled "[TITLE]" about [TOPIC].

Visual style:
- Deep navy (#0D1B2A) background filling the entire canvas
- Gold (#FFD700) as the primary accent for headers, numbers, and dividers
- White (#FFFFFF) for body text
- Numbered gold badges for each section
- Gold horizontal divider lines between sections
- Dark card containers with slight navy variation for section boxes
- Bold sans-serif typography, high contrast, premium feel
- Suitable for AI, finance, and career content

Content to include (as sections with bullets):
[KEY_POINTS]

Dimensions: tall portrait format (4:5 ratio). No watermarks, no extra borders. Infographic only.
```

---

### Style 3: Sketch / Cartoon

```
A hand-drawn sketch-style infographic poster titled "[TITLE]" about [TOPIC].

Visual style:
- Off-white or light cream (#FAFAF5) background
- Dark teal (#2BB5A0) as the primary accent color for section headers and highlight boxes
- Warm orange (#FF6B35) for numbered labels, arrows, and call-outs
- Hand-drawn, doodle-style icons and small illustrations for each section (e.g. checklist, lightbulb, gear, arrow)
- Slightly irregular, sketch-like borders on section boxes — not perfectly straight
- Chunky, bold hand-lettering style fonts for headings; clean handwriting style for body
- Curved arrows and connectors that look drawn by hand
- Energetic, dynamic layout — slightly imperfect but charming
- Social media-ready infographic — vibrant and shareable

Content to include (as sections with bullets):
[KEY_POINTS]

Dimensions: tall portrait format (4:5 ratio). No watermarks, no extra borders. Infographic only.
```

---

## Step 4 — Generate the Image

Run the image generation script with the constructed prompt:

```bash
python3 "$HOME/.claude/skills/generate-infographic/scripts/generate_image.py" "<escaped_prompt>"
```

The script will:
- Call the Gemini API (`gemini-2.0-flash-preview-image-generation`) via `generateContent`
- Save the image to `/tmp/infographic_<timestamp>.png`
- Print the file path on success, or an error message on failure

## Step 5 — Display the Image Inline

Once the script outputs the file path, **read the image file and display it inline** to the user using the `Read` tool on the returned path. Show the image directly in the conversation.

Then say something like:
> "Here's your [Professional/Bold/Sketch] infographic on [TOPIC]! Let me know if you'd like to tweak the content, style, layout, or colors."

## Error Handling

- If the API returns an error, show the error message and suggest the user check their API key in the script
- If the image path is not returned, mention that generation may have failed and offer to retry
- If the user's input is very short (e.g. just 2-3 words), ask for more detail before generating so the infographic has enough content to be useful

## Notes

- The Imagen API generates at 3:4 aspect ratio (closest to 1080x1350). Output will naturally be portrait-oriented.
- Keep the image prompt focused and specific — Gemini performs best with clear layout instructions
- For text-heavy inputs, summarize into 6-8 concise key points to avoid cluttering the infographic
- Always include the title prominently at the top of the infographic in the prompt
- The API key is stored directly in the script — remind the user to keep it private
