#!/usr/bin/env python3
"""
generate_image.py — Gemini Image Generation Script for generate-infographic skill
Calls Google's Gemini API to generate infographic images and saves them to /tmp/
Usage: python3 generate_image.py "<prompt>"
"""

import sys
import os
import json
import base64
import time
import urllib.request
import urllib.error

# ─────────────────────────────────────────────
# PASTE YOUR GEMINI API KEY HERE
API_KEY = "AIzaSyDzkiELzx_F2T7T3SEaDA3Ky7X2z-DeOG0"
# ─────────────────────────────────────────────

MODEL = "gemini-3.1-flash-image-preview"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
OUTPUT_DIR = "/tmp"


def generate(prompt: str) -> str:
    """Generate an infographic image from a prompt. Returns the saved file path."""

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["IMAGE", "TEXT"],
            "temperature": 0.9
        }
    }

    body = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            raw = response.read()
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        print(f"ERROR: HTTP {e.code} — {e.reason}", file=sys.stderr)
        print(f"Details: {error_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"ERROR: Could not reach Gemini API — {e.reason}", file=sys.stderr)
        sys.exit(1)

    try:
        body_resp = json.loads(raw)
    except json.JSONDecodeError:
        print("ERROR: Invalid JSON response from API", file=sys.stderr)
        print(raw.decode("utf-8", errors="replace"), file=sys.stderr)
        sys.exit(1)

    # Check for API-level errors
    if "error" in body_resp:
        err = body_resp["error"]
        print(f"ERROR: {err.get('code')} — {err.get('message')}", file=sys.stderr)
        sys.exit(1)

    candidates = body_resp.get("candidates", [])
    if not candidates:
        print("ERROR: No candidates returned from API. Full response:", file=sys.stderr)
        print(json.dumps(body_resp, indent=2), file=sys.stderr)
        sys.exit(1)

    parts = candidates[0].get("content", {}).get("parts", [])
    image_part = next((p for p in parts if "inlineData" in p), None)

    if not image_part:
        print("ERROR: No image data found in response parts. Full response:", file=sys.stderr)
        print(json.dumps(body_resp, indent=2), file=sys.stderr)
        sys.exit(1)

    inline = image_part["inlineData"]
    b64_data = inline.get("data")
    mime_type = inline.get("mimeType", "image/png")
    ext = "jpg" if "jpeg" in mime_type else "png"

    image_bytes = base64.b64decode(b64_data)

    timestamp = int(time.time())
    output_path = os.path.join(OUTPUT_DIR, f"infographic_{timestamp}.{ext}")

    with open(output_path, "wb") as f:
        f.write(image_bytes)

    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python3 generate_image.py "<prompt>"', file=sys.stderr)
        sys.exit(1)

    prompt_text = sys.argv[1]
    path = generate(prompt_text)
    print(path)  # stdout — Claude reads this as the file path
