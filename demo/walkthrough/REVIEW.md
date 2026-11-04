# Walkthrough review

The film follows a guided repository workflow: discover tools, validate a specification, inspect task context, approve checks, and read the execution evidence. It lasts 85 seconds, including paired Kujo and Hermes logo bumpers. A receipt-first story and a catalog-only tour were considered but not built; the workflow gives developers a concrete use case.

The official Kujo mark and Hermes website logo remain unmodified. The black body, white bumpers, Departure Mono lettering, and short logo offsets follow the existing Kujo integration-video style. This is a new composition, not a claim that the old CMD bumper was recovered.

## Evidence and checks

- Real Hermes v0.22.7 CLI, local Qwen3.5 4B through Ollama, canonical Kujo 1.8.0 runtime.
- Native discovery returned 51 bindings. Spec returned `valid: true` with no errors or warnings. PackWrite reported seven phases and no missing files.
- Eval ran after the actual interactive “Allow once” choice. Both checks passed. A follow-up Hermes tool call retrieved the same receipt with `verified: true`.
- `scripts/verify_evidence.py` checks recorded tool responses, capture hashes, canonical command identity, approval evidence, result counts, and all copied receipt hashes.
- HyperFrames check passed with zero lint, runtime, layout, contrast, or audio errors. All 22 sampled contrast checks passed. Its 599 craft samples produced ten stillness warnings, retained deliberately so viewers can read the catalog, results, and tool lists during narration.
- Beat, transition, and phone sheets were inspected. A fresh reviewer found no actionable P0/P1 visual or story issues. Extra samples cover the bumper offsets, short terminal cuts, later tool families, and final benefits.
- The local preview returned HTTP 200. Delivery metadata, full decode, and audio measurements are recorded in `evidence/delivery-verification.json` and `evidence/delivery-audio.json`.

The source soundtrack measured −17.22 LUFS integrated and −1.41 dBTP. The final MP4 measured −14.24 LUFS and −1.24 dBTP after renderer audio processing. Its 2,550 frames decoded without errors at 1920 × 1080, 30 fps; duration is exactly 85.0 seconds. Audio was measured, not auditioned by a listener. No claim of a listening review is made.

## Editorial limits

The terminal clips replay actual captured bytes. Waiting time is shortened. Catalog, Spec, PackWrite, and receipt excerpts are labeled as recorded tool results, not presented as a recreated Hermes interface. The demo is guided: the small model required explicit tool names and a separate receipt follow-up. Earlier attempts and the model's contradictory discovery paraphrase remain in the evidence. The film uses verified tool data for its claims.

The approval dialog is the strongest native-interface shot. The setup shot is the weakest: its doctor output contains long local paths and is useful mainly when paused at 1080p. A future vertical cut should crop that evidence and enlarge each result separately. The current film is intended for landscape viewing; headers and outcome text remain readable on the phone sheets, while hashes and terminal details are pause-to-inspect evidence.

The broader tool list describes included bindings. Workcell, Lens, and other tools retain their documented prerequisites. No claim is made that every binding ran here or that successful execution establishes release readiness. Nothing was posted or submitted externally.

The scoped Loop gates passed for recorded execution evidence, full delivery decode and audio, PackWrite context validation, and whitespace checks. The first delivery gate exposed FFmpeg reading the harness input stream; adding `-nostdin` fixed the verifier, and the full gate set then passed. The earlier low-disk render attempt was resolved by removing the task-specific model downloads.

Original vendor bytes and recorded evidence are exempt from whitespace normalization through the local `.gitattributes`; authored scripts and documentation remain checked. This preserves terminal recordings, FFmpeg logs, and patch context lines.
