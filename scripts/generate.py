#!/usr/bin/env python3
"""Read the design skill, choose a non-duplicate quote, and write a prompt brief."""
from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = ROOT / "skill" / "SKILL.md"
QUOTES_PATH = ROOT / "data" / "quotes.json"
HISTORY_PATH = ROOT / "data" / "history.json"
OUTPUT_DIR = ROOT / "outputs"

STYLES = [
    {
        "name": "Retro Earth Tone",
        "palette": "charcoal #202B2B, terracotta #A96F43, sage #A9B9AC, warm cream #E8DDB7, mustard #D9A441",
        "layout": "Tightly stacked, heavy geometric lettering with compact spacing and a strong vertical rhythm."
    },
    {
        "name": "Kinetic Editorial",
        "palette": "deep navy #172B45, pale blue #D0D9E8, off-white #F4F3EE, accent red #D71935",
        "layout": "Asymmetrical editorial composition mixing oversized words, small supporting type and one restrained circular accent."
    },
    {
        "name": "Swiss Grid",
        "palette": "ink #171717, paper #F1EFE8, signal red #D62828",
        "layout": "Precise grid alignment, deliberate margins, strong typographic scale contrast and disciplined negative space."
    },
    {
        "name": "Minimal Bold",
        "palette": "near-black #111111 and warm white #F5F1E8",
        "layout": "Few dominant words, generous negative space, crisp alignment and exceptionally clear hierarchy."
    },
    {
        "name": "Neo-Brutalist",
        "palette": "black #101010, bone #F2E8D5, electric orange #F05A28",
        "layout": "Oversized block typography, assertive geometric divisions and high-contrast editorial balance."
    },
    {
        "name": "Experimental Type",
        "palette": "midnight #17212B, muted lavender #C7C9E2, acid yellow #E7D96B",
        "layout": "Creative interlocking and selective rotated words, varied scale and controlled asymmetry while keeping every word readable."
    }
]

def normalized(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().casefold()

def slug(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return value[:48] or "quote"

def main() -> None:
    # Mandatory skill-first behavior: load and validate the full skill before any quote selection.
    if not SKILL_PATH.is_file():
        raise SystemExit("Required skill file is missing; refusing to generate.")
    skill = SKILL_PATH.read_text(encoding="utf-8")
    required = ["Mandatory first step", "Core design rules", "Output required for each quote", "Duplicate avoidance"]
    missing = [section for section in required if section not in skill]
    if missing:
        raise SystemExit("Skill validation failed: " + ", ".join(missing))

    quotes = json.loads(QUOTES_PATH.read_text(encoding="utf-8"))
    history = json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
    generated = history.setdefault("generated", [])
    used_ids = {item.get("quote_id") for item in generated}
    used_texts = {normalized(item.get("quote_text", "")) for item in generated}

    available = [
        q for q in quotes
        if q.get("id") and q.get("text")
        and q["id"] not in used_ids
        and normalized(q["text"]) not in used_texts
    ]
    if not available:
        print("No unused quotes remain. No output created.")
        return

    run_time = datetime.now(timezone.utc)
    slot = os.environ.get("RUN_SLOT", "manual")
    # Rotate style by generation count so consecutive runs do not repeat the same style.
    style = STYLES[len(generated) % len(STYLES)]
    quote = available[0]
    quote_text = quote["text"]
    digest = hashlib.sha256(normalized(quote_text).encode("utf-8")).hexdigest()
    stamp = run_time.strftime("%Y%m%d-%H%M%S")
    output_name = f"{stamp}-{slot}-{slug(quote_text)}.md"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    prompt = f"""# Typography Poster Design Brief

- **Generated (UTC):** {run_time.isoformat()}
- **Run slot:** {slot}
- **Quote ID:** {quote['id']}
- **Style:** {style['name']}
- **Aspect ratio:** 4:5 portrait
- **Quote fingerprint:** `{digest}`

## Exact quotation

> {quote_text}

## Art direction

**Palette:** {style['palette']}

**Composition:** {style['layout']}

**Typography:** Use bold geometric sans-serif display lettering as the primary artwork. Establish a clear hierarchy by making the most meaningful word or phrase dominant. Combine scale and weight intentionally; use tight kerning only where it improves the composition. Keep supporting text secondary.

**Background:** Use a clean, solid background with subtle print-like texture only if it supports the palette. Preserve generous safe margins.

## Ready-to-use image-generation prompt

Create a premium, print-ready 4:5 portrait motivational typography poster. The exact text must read: "{quote_text}". Treat typography as the artwork, not as a text overlay. Art direction: {style['name']}. Use this palette: {style['palette']}. Composition: {style['layout']} Use bold, highly legible geometric sans-serif letterforms, precise spacing, strong visual hierarchy and intentional negative space. Keep the quotation complete, correctly spelled and in the exact supplied order. No extra words, no logos, no watermark, no mockup, no unrelated illustration and no decorative clutter. Professional editorial graphic design, crisp edges, balanced margins, high-resolution output.

## Negative prompt

Misspelled text, extra letters, missing words, duplicated words, illegible typography, random symbols, clutter, stock photography, 3D mockup, watermark, logo, ornate script fonts, weak contrast, cropped lettering.

## Quality-control checklist

- [ ] Exact quotation and word order verified.
- [ ] Every word readable and inside safe margins.
- [ ] Main phrase has clear visual dominance.
- [ ] Palette is limited and harmonious.
- [ ] Composition is distinct from previous outputs.
- [ ] Final rendered lettering proofread.
"""
    (OUTPUT_DIR / output_name).write_text(prompt, encoding="utf-8")

    generated.append({
        "quote_id": quote["id"],
        "quote_text": quote_text,
        "quote_hash": digest,
        "style": style["name"],
        "generated_at_utc": run_time.isoformat(),
        "run_slot": slot,
        "output": f"outputs/{output_name}"
    })
    history["generated"] = generated
    HISTORY_PATH.write_text(json.dumps(history, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Created {output_name} using skill/SKILL.md; duplicate check passed.")

if __name__ == "__main__":
    main()
