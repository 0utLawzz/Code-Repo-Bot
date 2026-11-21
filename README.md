# Typography Poster Studio

A lightweight, GitHub-hosted typography-poster prompt system.

## What it does
- Keeps the reusable design skill in `skill/SKILL.md`.
- Runs twice daily using GitHub Actions (09:00 and 21:00 Asia/Karachi).
- Reads and validates the skill before preparing each design brief.
- Selects a quote from the local quote bank and prevents reuse through a persistent history file.
- Saves each generated prompt brief under `outputs/` and updates `data/history.json`.

## Storage
GitHub is the source of truth. No Google Sheet, external database, or API key is required for this initial version.

## Important limitation
The scheduled workflow creates a complete image-generation prompt/brief; it does not render an image. Actual image rendering through ChatGPT ImageGen or another provider requires a supported integration and credentials. No API key is assumed or stored.

## Run manually
GitHub → Actions → **Typography Poster — Twice Daily** → Run workflow.

## Schedule
- 09:00 Pakistan Standard Time (04:00 UTC)
- 21:00 Pakistan Standard Time (16:00 UTC)

GitHub Actions schedules can start a little later than the exact minute during periods of high load.

## Add quotes
Edit `data/quotes.json`. Give every quote a stable unique `id` and exact `text`. The history check uses normalized quote text and IDs.

## Files
- `skill/SKILL.md`: design skill and rules.
- `scripts/generate.py`: scheduler-side generator and duplicate guard.
- `data/quotes.json`: local quote bank.
- `data/history.json`: persistent generation history.
- `outputs/`: generated prompt briefs.
