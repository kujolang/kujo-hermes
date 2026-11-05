# Kujo Hermes — square walkthrough

An 88-second square film for developers who work in Hermes. It shows the native installation path, then explains what context packs, contracts, checks and receipts let them do. The Kujo/Hermes bumpers and CMD-style glitches carry over from the landscape film. The ending asks viewers to install today.

## Install

With Hermes 0.22.7+, its supported Python runtime, Git and an official Kujo runtime >=1.6,<2 installed, run this from a Git repository root:

```sh
hermes plugins install kujolang/kujo-hermes
hermes kujo setup --trust-workspace .
```

Accept the native installation prompts. Setup fetches pinned source repositories and configures the active profile. Start a new conversation; restart a running gateway. Use `hermes kujo doctor` for missing optional dependencies. No npm package or other agent plugin is required. Some tools need external services, credentials or containers. Isolated-host profiles use the manual configuration in the main README because Hermes does not expose plugin CLI commands in that mode.

## What the pictures prove

The tool views reuse distinct, unchanged recordings from [the verified landscape edit](../walkthrough/README.md). These are the official Hermes desktop workspace's native Markdown viewer, showing files derived from actual native tool results. They are not model-written chat. The approval excerpt is the original real local Qwen3.5 4B conversation. The other views do not claim a fresh autonomous model run.

PackWrite shows a seeded pack summary with seven phases, not new pack generation. Spec validates a task contract. Eval reports two actual passing checks. ShipCheck still reports warnings. Scout records a repository scan. The receipt verifies stored hashes; it does not prove the code is correct. The source results, inputs, approvals and receipts remain in `../walkthrough/evidence/v5-workflows/`.

The installation scene replays the new actual public GitHub install and setup captures in `evidence/install.cast` and `evidence/setup.cast`, with network waiting condensed. Screen commands are literal, runnable instructions. The installer uses official Hermes v0.22.7. It prepares a supported Python 3.14.9 environment. The first recorder kept its older Python 3.11 entry point after that preparation and could not load the new binary dependency; setup was recaptured using Hermes's selected 3.14 interpreter and an official Kujo 1.8 runtime on PATH. Both raw captures preserve the chronology. This is a corrected recording launcher, not a plugin permission bypass. The earlier native-tool desktop recordings use the documented Python 3.11 compatibility environment; the project's separate Linux certification remains distinct.

`story.json` owns the benefit-led narration. `timeline.json` and `evidence/shot-map.json` bind every spoken subject to its own screen. All source widths remain visible, with no zoom or side crop. Detailed interface text is smaller in the square/mobile export; the large headline carries each benefit.

## Reproduce and edit

The committed `assets/master.m4a` is the finished soundtrack. Rendering does not require a voice-provider account. To change the voice script, `scripts/generate_voice.py` generates only missing Siren V4 takes on the authorized ElevenLabs account. It checks generation-time commercial eligibility, saves timestamps and request provenance, and refuses to retry an uncertain paid request automatically. Individual MP3 stems and the original music WAV are local cache files. Music and transition provenance are inherited from the landscape project's evidence.

```sh
python3 scripts/build_composition.py
npx --yes hyperframes@0.9.13 check --json
npx --yes hyperframes@0.9.13 snapshot --review
npx --yes hyperframes@0.9.13 preview
npx --yes hyperframes@0.9.13 render --fps 30 --quality delivery \
  --output delivery/kujo-hermes-square.mp4
python3 scripts/master_delivery.py
ffmpeg -i delivery/kujo-hermes-square.mp4 -vf scale=480:480 \
  -c:v libx264 -crf 21 -pix_fmt yuv420p -c:a aac -b:a 128k \
  -movflags +faststart delivery/kujo-hermes-square-480p.mp4
python3 scripts/verify_sources.py
python3 scripts/verify_delivery.py
python3 scripts/verify_video_subjects.py
```

The editable preview is available at `http://localhost:3052/#project/square` while the local server runs. Its **Edit with Framey** button opens the [HyperFrames desktop app](https://hyperframes.studio/studio/download?src=cli). Review and delivery measurements are recorded in `REVIEW.md` and `evidence/`. Audio is measured, not auditioned by the automated reviewer. No release, catalog pull request, social post or contest submission is published by this work.
