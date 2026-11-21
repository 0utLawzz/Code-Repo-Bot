# Typography Poster Automation Blueprint

Status: transition / build phase
Owner: ChatGPT (creative direction, brief writing, queue supervision) + Make.com (recurring execution)
Primary repository: https://github.com/0utLawzz/Code-Repo-Bot
Branch: main

## Operating model

- ChatGPT reads `skill/SKILL.md`, the reference design, quote bank, history, current queue, and latest generated images before preparing the next brief.
- ChatGPT writes one new job brief and commits it to `data/jobs.json` plus `jobs/pending/`.
- Make is intended to poll the repository on a recurring schedule (target: hourly), claim pending jobs, call the selected image-generation provider, upload the resulting image into `outputs/images/`, then update the same job to `completed`.
- ChatGPT periodically checks the queue and generated image folder, picks completed images, and prepares a publishing payload.
- Publishing is a separate stage. Do not publish until a social channel is connected and explicitly selected.
- The existing GitHub Actions workflow is temporarily paused; retain it for later reuse.

## Job lifecycle

`brief_ready -> claimed -> generating -> image_uploaded -> completed -> publishing_queue -> published`

Failure states: `retry_wait`, `failed`. A failed or delayed job must remain visible and retryable; never silently discard it.

## Queue contract

Each job must contain:
- `job_id`: unique stable ID
- `created_at`: ISO-8601 UTC timestamp
- `quote_id`: quote bank ID
- `quote`: exact approved quote
- `theme`: design theme name
- `prompt`: complete image prompt
- `output_path`: exact target path under `outputs/images/`
- `status`: lifecycle state
- `attempts`: integer
- `image_url`: public raw GitHub URL after upload, if available
- `last_error`: empty unless a failure occurred

## Storage layout

- `data/jobs.json`: queue and job status ledger
- `jobs/pending/`: ready-to-generate prompt briefs
- `outputs/images/`: final generated posters (PNG/JPG)
- `outputs/published/`: publication receipts and post references
- `docs/AUTOMATION_BLUEPRINT.md`: this operating specification

## Buffer target

Maintain a reserve target of 6 completed, unpublished images for a planned 3-post/day publishing pace. This is a target, not a reason to generate duplicates. Top up only with unused quotes and themes.

## Hourly watchdog

The intended watchdog checks:
1. Pending jobs older than one hour.
2. Jobs stuck in claimed/generating state.
3. Completed image count against the reserve target.
4. Image file presence and non-zero size.
5. Whether a publishing slot is missing its assigned image.

When a job is overdue, retry it within a bounded attempt count, then mark it failed and send an alert. Do not create a second job for the same quote while the first is recoverable.

## Current integration notes (2026-11-22)

- GitHub OAuth connection is available in the connected Make team.
- No DeepAI image-generation connection is currently available; it requires authorization before Make can call it.
- Buffer account connection exists, but the connected organization currently returns no social channels. No publishing channel is ready.
- Metricool is not currently available as a connected action tool in this ChatGPT workspace. Buffer is the practical first publishing integration once a channel is connected.
- Make's GitHub `newCommit` module is a pull-request commit watcher, not a general repository-file watcher. Do not use it as the hourly file-queue trigger. A proper repository polling method must be selected before activating generation.
- No webhook trigger is part of this design.

## Safety and idempotency

- Use stable `job_id` as the idempotency key.
- A completed job must not generate again.
- An uploaded image must not be overwritten by a retry; use a unique output filename per job.
- Publishing must use a separate status transition and save the social post ID / URL.
- Keep the GitHub Actions workflow file; only its scheduled cron trigger is paused.
