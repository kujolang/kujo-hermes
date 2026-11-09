# Kujo Hermes — checkout workflow

An 88-second square walkthrough of Hermes investigating a checkout overcharge with
Kujo Spec, Eval and execution receipts. Qwen3.5 4B runs locally through Ollama;
there is no model API fee. Siren V4 provides the narration.

The new recording uses Hermes 0.23.0 and the real native plugin. The script in
`scripts/record.py` launches Hermes and supplies the first task. It does not modify
the implementation. The recording operator approves the repository checks once and asks the model
to make the correction. The deterministic driver in `../checkout/run.py` is not
used to perform that correction.

[Watch 1080 square](delivery/kujo-hermes-checkout.mp4) · [Download 480 square](delivery/kujo-hermes-checkout-480p.mp4)

## Install the plugin

With Hermes, an official Kujo runtime and Git installed, run:

```sh
hermes plugins install kujolang/kujo-hermes
hermes kujo setup --trust-workspace .
```

Accept the prompts. Start a new conversation, or restart a running gateway.
Some Abilities need additional tools or service credentials. See the project README.

## Recording and evidence

The existing installation capture comes from `../square`; its provenance and
uncut terminal recordings remain there. The checkout session uses a narrow terminal
so the full screen fits the square frame. The Mac was locked during this session,
so this is a real Hermes CLI recording, not a desktop-app recording.

`evidence/checkout.cast` preserves the terminal output and source timing.
`scripts/cast_video.py` replays those terminal cells, condensing waits through
explicit edit windows; it does not synthesize tool results. Clip edit maps preserve
the source timestamps. Exported visible messages exclude private reasoning.

`Modelfile` sets the 64K context required by Hermes. An earlier attempt using 16K
was rejected before any tool call; `evidence/setup-context-error.cast` preserves
that failure. This is an environment correction, not a permission bypass.

Spec validates the contract format. Eval executes the fixture's real tests.
Passing three checks does not prove all checkout behavior. Receipts record local
execution evidence; they are not signed attestations or a global release gate.

## Reproduce

Use the existing fixture in `../checkout/fixture` in a fresh run directory. Install
Ollama, then run `ollama create qwen3.5:hermes-checkout64k -f Modelfile` after pulling
`qwen3.5:4b`. The recorder defaults to the repository's audited Hermes installation,
Python environment, Kujo runtime and pinned source cache under `.local/`.

From the repository root:

```sh
asciinema rec --output-format asciicast-v2 --window-size 60x24 \
  --command 'python3 demo/checkout-video/scripts/record.py' checkout-new.cast
```

After the first Eval result, preserve the receipt and workspace with
`scripts/snapshot_evidence.py before`. Ask Hermes to correct `checkout.py` without
changing the tests, rerun the same Eval suite, and retrieve both receipts. Preserve
that result with `scripts/snapshot_evidence.py after`. The snapshot commands refuse
to replace existing snapshot directories. Pass `--run-dir` with a new directory when repeating the workflow; adapt the
snapshot/export helper paths to that directory.

Check exported evidence independently:

```sh
python3 demo/checkout/verify.py demo/checkout-video/evidence/run
```

## Edit the film

`story.json` contains narration; `timeline.json` binds it to the scenes. The
established Kujo/Hermes bumpers and CMD glitches appear at every scene boundary.
`STORYBOARD.md`, `SPEC.md` and `REVIEW.md` record editorial choices and limitations.
Run `npx hyperframes@0.9.13 preview --background` from this folder for an editable
preview. HyperFrames Studio can open the same composition.

No public post, release or contest submission is performed by these scripts.

The raw model session lasts about an hour, including CPU inference, operator
pauses and a missed approval timeout. The edited film does not represent real-time
latency or an uninterrupted autonomous run. A recording controller drained the
terminal and approved the retry only after checking the exact Eval arguments and
workspace. No approval policy was bypassed.

Replay uses pyte 0.8.2, Pillow and the Mac system Menlo font. Emoji presentation
selectors are removed for pyte compatibility; no result words are substituted.
The original cast remains the source of truth.
