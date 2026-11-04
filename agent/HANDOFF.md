# Handoff

## Current Status
Working native integration; partial ecosystem certification. See docs/readiness.md for evidence and precise limitations.

## Completed Phases
Research, design, native implementation, unit/canonical/host/live-model validation, review corrections and packaging preparation. Source attribution is in catalog/sources.lock.json and docs/provenance.json.

## Known Issues
External browser/container prerequisites and unbound producer domains. Clean install, dependencies and real host E2E passed on Linux Python 3.14 (CI 41925825469); local download timeouts are environment-specific. No submission authorized.

## Next Agent Notes
Start with docs/readiness.md and submission/checklist.md. Preserve explicit human approvals, source pins and the distinct receipt contract. Do not mark blocked certification as passed. Use the exact reproducible scripts after resolving prerequisites.

## Walkthrough video milestone — 2026-11-04

The 85-second walkthrough is recorded and rendered at `demo/walkthrough/delivery/kujo-hermes-walkthrough.mp4`, with official Kujo/Hermes logo bumpers and Siren V4 narration. Real local Qwen3.5 4B drove Hermes discovery, Spec validation, PackWrite summary, approved Eval, and receipt retrieval. The small model needed guided prompts and a receipt follow-up. Source recordings, exact tool responses, copied receipts, editable scenes, and verification scripts are under `demo/walkthrough/`. See its README and REVIEW before revising or publishing. Broader ecosystem certification gaps above remain unchanged; no external submission is authorized.
