# Kujo Hermes — checkout workflow

A 73.2-second square showcase of Hermes investigating a checkout overcharge with
Kujo Spec, Eval and execution receipts. Qwen3.5 4B runs locally through Ollama;
there is no model API fee. Roger V4 provides the shorter narration. The upbeat instrumental comes from the user-owned Website Cloner film, with a music-led hold on the passing checks.

The original model recording uses Hermes 0.23.0 and the real native plugin. The script in
`scripts/record.py` launches Hermes and supplies the first task. It does not modify
the implementation. The recording operator approves the repository checks once and asks the model
to make the correction. The deterministic driver in `../checkout/run.py` is not
used to perform that correction.

[Watch 1080 square](delivery/kujo-hermes-checkout.mp4) · [Download 480 square](delivery/kujo-hermes-checkout-480p.mp4) · [Optional captions](delivery/kujo-hermes-checkout.vtt)

## Install the plugin

With Hermes, an official Kujo runtime and Git installed, run:

```sh
hermes plugins install kujolang/kujo-hermes
hermes kujo setup --trust-workspace .
```

Accept the prompts. Start a new conversation, or restart a running gateway.
Some Abilities need additional tools or service credentials. See the project README.

## Recording and evidence

Installation footage reuses the successful native command recordings from
`../square`, made with Hermes 0.22.7 before the official release. Its original
provenance remains there. The install commands and setup behavior are unchanged.
The official release and documentation-corrected catalog candidate are separately
verified by clean-install CI on Hermes 0.22.7 and 0.23.0. The new release bumper and
narration do not turn this footage into a fresh installation recording.

New local takes are retained as failures: a rejected tag ref, two disk-full
source-environment preparations, and a managed-environment source-reference
failure. A restored-source retry also exhausted local disk. No failed output is
used as successful installation footage. Prerequisites are Hermes, Kujo and Git;
waits are condensed. The source screen is held for the longer spoken cue.

The model workflow remains the original verified recording. It was not rerun or
relabeled as a new release-day model session. The narrow terminal keeps the full
source screen visible in the square frame. This is Hermes CLI footage, not a
Desktop-app recording.

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

For another installation capture, use an installed supported Hermes CLI and
`record_release_install.py --home /absolute/test-home --workspace /absolute/demo-repo`.
It pins the tested catalog SHA, accepts native prompts through the terminal, and
requires enough disk for Hermes dependency preparation. The failed takes retain
the exact earlier invocation, before the recorder gained explicit path options.

The release revision re-renders 0–3.2 and 54–73.2 seconds and preserves the
verified workflow picture between them. `scripts/assemble_release.py` joins
those renders to the previous master (recorded SHA in `release-delivery-plan.json`)
and creates both exports. A complete HyperFrames render of `index.html` is also
supported; the final AAC master is remuxed without changing its audio.
