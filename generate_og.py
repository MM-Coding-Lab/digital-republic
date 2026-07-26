#!/usr/bin/env python3
"""Generate OG hero images for The Digital Republic manifesto.

Uses Google Gemini 3.1 Flash Image Preview with typography baked directly
into the composition (no post-overlay). Reads GOOGLE_AI_API_KEY from
wordpress-blog-agent/.env.blog-agent.

Usage:
    python3 generate_og.py              # generates both PL and EN
    python3 generate_og.py --lang pl
    python3 generate_og.py --lang en
"""

from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

from dotenv import load_dotenv
from PIL import Image

ENV_PATH = Path(__file__).parent.parent / "wordpress-blog-agent" / ".env.blog-agent"
OUTPUT_DIR = Path(__file__).parent
IMAGE_WIDTH = 1200
IMAGE_HEIGHT = 630

PROMPTS = {
    "pl": (
        "Editorial-quality wide-format illustration, 16:9 cinematic composition. "
        "Render the title text 'MANIFEST CYFROWEJ REPUBLIKI' (in Polish, must be spelled exactly) "
        "in large bold modern sans-serif typography, stacked on three lines, left-aligned, "
        "positioned in the upper-left third of the image, occupying significant visual weight, "
        "color: deep navy blue or off-white depending on background contrast. "
        "Below the title, a thin horizontal accent line and a small subtitle 'technologia · transparentność · odpowiedzialność' in elegant smaller type. "
        "Right side of the composition: rich minimalist illustration of translucent classical greek columns "
        "merging seamlessly with a geometric digital network of glowing connection nodes and thin circuit lines, "
        "subtle warm gold and bright cyan glowing accents on the network. "
        "Background: deep saturated gradient from dark navy blue at edges to slightly lighter blue-teal in the center, "
        "giving depth and atmosphere — NOT plain white, NOT empty. "
        "Refined editorial / manifesto aesthetic, sense of civic dignity and technological optimism, "
        "high contrast between text and background for readability, modern and sophisticated. "
        "The text must be clearly legible. Aspect ratio strictly 16:9, no white margins, image fills full frame."
    ),
    "en": (
        "Editorial-quality wide-format illustration, 16:9 cinematic composition. "
        "Render the title text 'THE DIGITAL REPUBLIC MANIFESTO' (in English, must be spelled exactly) "
        "in large bold modern sans-serif typography, stacked on three lines, left-aligned, "
        "positioned in the upper-left third of the image, occupying significant visual weight, "
        "color: deep navy blue or off-white depending on background contrast. "
        "Below the title, a thin horizontal accent line and a small subtitle 'technology · transparency · accountability' in elegant smaller type. "
        "Right side of the composition: rich minimalist illustration of translucent classical greek columns "
        "merging seamlessly with a geometric digital network of glowing connection nodes and thin circuit lines, "
        "subtle warm gold and bright cyan glowing accents on the network. "
        "Background: deep saturated gradient from dark navy blue at edges to slightly lighter blue-teal in the center, "
        "giving depth and atmosphere — NOT plain white, NOT empty. "
        "Refined editorial / manifesto aesthetic, sense of civic dignity and technological optimism, "
        "high contrast between text and background for readability, modern and sophisticated. "
        "The text must be clearly legible. Aspect ratio strictly 16:9, no white margins, image fills full frame."
    ),
}

OUTPUT_NAMES = {
    "pl": "og-image-pl-v2.png",
    "en": "og-image-en-v2.png",
}


def generate(lang: str, api_key: str) -> Path:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    prompt = PROMPTS[lang]

    print(f"[{lang}] Calling Gemini 3.1 Flash Image Preview...")
    response = client.models.generate_content(
        model="gemini-3.1-flash-image-preview",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio="16:9",
                image_size="2K",
            ),
        ),
    )

    for part in response.parts:
        if part.inline_data is not None:
            img = Image.open(io.BytesIO(part.as_image().image_bytes))
            img = img.convert("RGB").resize(
                (IMAGE_WIDTH, IMAGE_HEIGHT), Image.LANCZOS
            )
            out_path = OUTPUT_DIR / OUTPUT_NAMES[lang]
            img.save(out_path, quality=95)
            print(f"[{lang}] Saved: {out_path} ({IMAGE_WIDTH}x{IMAGE_HEIGHT})")
            return out_path

    raise RuntimeError(f"[{lang}] Gemini returned no image data")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate OG hero images for Digital Republic")
    parser.add_argument("--lang", choices=["pl", "en", "both"], default="both")
    args = parser.parse_args()

    load_dotenv(ENV_PATH)
    import os

    api_key = os.getenv("GOOGLE_AI_API_KEY")
    if not api_key:
        print("Error: GOOGLE_AI_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    langs = ["pl", "en"] if args.lang == "both" else [args.lang]
    for lang in langs:
        generate(lang, api_key)


if __name__ == "__main__":
    main()
