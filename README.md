# Typography Poster Studio

A lightweight, GitHub-hosted typography-poster prompt system.

## What it does
- Keeps the reusable design skill in `skill/SKILL.md`.
- Runs twice daily using GitHub Actions (09:00 and 21:00 Asia/Karachi).
- Reads and validates the skill before preparing each design brief.
- Selects an unused quote and checks duplicates by stable ID, normalized text and SHA-256 fingerprint.
- Saves each generated prompt brief under `outputs/` and updates `data/history.json`.
- Requires every poster prompt to place the exact **OutLawZ** signature small and elegant at the very bottom, centered beneath the quote and safely inside the canvas.

## Duplicate protection
The persistent history is the source of truth. Legacy records without a fingerprint are fingerprinted from their stored quotation text during duplicate checks. If no unused quote remains, the generator creates no output and does not modify history.

## Storage
GitHub is the source of truth. No Google Sheet, external database, or API key is required for this initial version.

## Important limitation
The scheduled workflow creates a complete image-generation prompt/brief; it does not render an image or publish to social media. Actual image rendering and social-media auto-publishing require supported provider/platform connectors and their permissions. No API key is assumed or stored.

## Run manually
GitHub → Actions → **Typography Poster — Twice Daily** → Run workflow.

## Schedule
- 09:00 Pakistan Standard Time (04:00 UTC)
- 21:00 Pakistan Standard Time (16:00 UTC)

GitHub Actions schedules can start a little later than the exact minute during periods of high load.

## Add quotes
Edit `data/quotes.json`. Give every quote a stable unique `id` and exact `text`. Duplicate protection checks the ID, normalized text and SHA-256 fingerprint against generation history.

## Files
- `skill/SKILL.md`: design skill and mandatory signature rules.
- `scripts/generate.py`: scheduler-side generator and duplicate guard.
- `data/quotes.json`: local quote bank.
- `data/history.json`: persistent generation history.
- `outputs/`: generated prompt briefs.
