# Kujo Hermes walkthrough

An 85-second walkthrough with official Kujo and Hermes logo bumpers, real Hermes CLI recordings, and ElevenLabs Siren narration. The local Qwen3.5 4B model runs through Ollama without an inference API fee. Narration uses an existing paid ElevenLabs account.

The video shows discovery, schema inspection, Spec validation, PackWrite context, approval for Eval, and receipt retrieval. The tool overview describes the bundled catalog; it does not claim every binding ran in this recording. See the main repository's compatibility and readiness documents for prerequisites and coverage.

## Edit and render

```sh
cd demo/walkthrough
npm run dev
npm run check -- --json
npm run render -- --quality delivery --fps 30 --workers 2 --output delivery/kujo-hermes-walkthrough.mp4
```

`python3 scripts/build_recordings.py` rebuilds the three terminal clips from the committed recordings (macOS Menlo font). `python3 scripts/build_composition.py` rebuilds the scenes from the captured evidence. `python3 scripts/verify_evidence.py` verifies that evidence without rerunning tools.

The root composition lasts 85 seconds at 1920 × 1080. `timeline.json` stores the narration cues. Scenes live in `compositions/`; `assets/master.m4a` is the mixed soundtrack. The committed terminal clips are edited from real asciinema recordings. Their `.edits.json` files identify the source windows. Waiting time is shortened and disclosed on screen.

`NARRATION.md`, `SPEC.md`, `STORYLINES.md`, and `REVIEW.md` describe the copy, design, alternatives, and verification. `evidence/asset-sources.json` records logo, font, and music provenance. The paired monochrome bumper follows the existing Kujo integration-video style.

## Reproduce the live run

Follow `../script.md` and the repository installation guide to prepare the sample project, canonical Kujo sources, runtime, and trusted workspace. Install the plugin in Hermes v0.22.7. Use a separate Hermes home so the recording does not change your daily settings.

Install Ollama and pull `qwen3.5:4b`. Create a local alias using this Modelfile:

```text
FROM qwen3.5:4b
PARAMETER num_ctx 65536
PARAMETER num_predict 1024
PARAMETER temperature 0.1
PARAMETER presence_penalty 0
```

```sh
ollama create qwen3.5:hermes-demo -f Modelfile
```

Use `config.example.yaml` to configure Hermes' custom provider at `http://127.0.0.1:11434/v1`, with that model. Set `tools.tool_search.enabled: off` to expose the six native plugin tools directly. Ability schemas remain available on demand through `kujo_inspect`. Keep manual approvals enabled. Restart the isolated Hermes gateway after changing plugin trust settings; a new conversation can reuse an already loaded plugin host. The small model required explicit tool and Ability names; the recorded prompts preserve that guidance. This recording used the actual Hermes v0.22.7 source with the existing local Python 3.11.16 dependency environment on an Intel Mac; inference waits were substantially longer than the edited video.

The opening prompts are in `scripts/record_hermes.py`. Eval ran as a background invocation. After approval, the recorded follow-up was: “Retrieve the actual finished receipt with kujo_receipts, receipt_id=RETURNED_ID. Report passed and failed counts from its result, plus verified. Do not run Eval again.” Adapt its host, interpreter, workspace, and Hermes-home paths to your machine. Record each shot with asciinema. The Eval shot opens the interactive CLI: one-shot mode correctly blocks operations that need an approval prompt. Exit the interactive session after its final answer. Approve the displayed Eval command only after reviewing it. The recorder runs the actual Hermes CLI; it does not replace tool execution or approval handlers.

The simple terminal converters require Pillow and pyte. The interactive approval clip uses `cut_cast.py`, asciinema `agg`, and FFmpeg so its Unicode dialog renders correctly. They replay recorded ANSI terminal output into images and H.264 clips. The soundtrack builder requires FFmpeg. `generate_voice.py` makes billable ElevenLabs requests and is not needed to edit or render the committed soundtrack. It uses cached takes and refuses to repeat an uncertain request automatically.

No release, social post, catalog submission, or external pull request is part of this deliverable.

Ollama’s [OpenAI compatibility documentation](https://github.com/ollama/ollama/blob/main/docs/api/openai-compatibility.mdx) describes the `reasoning_effort` field. The demo named custom provider sets it to `none`; Hermes forwards this through the provider’s `extra_body` configuration.

The edit uses the actual catalog response rather than the model’s contradictory discovery paraphrase. Earlier attempts also exposed a misspelled Ability ID and stale gateway settings; these did not bypass validation or trust checks. The source recordings preserve those attempts. This is a guided demonstration, not a model reliability benchmark.

The temporary Qwen3.5 models were removed after recording to free render space. The Modelfile and pull command reproduce them; the video and execution evidence do not depend on keeping the model installed.

The final Loop evaluation is scoped to this video in `evidence/loop/`; the repository’s broader integration checklist retains its separate, partially certified state. PackWrite’s existing project handoff is updated without regenerating the pack.

Use Hermes’ supported Python runtime for installation (3.14 for this release). The separate Linux 3.14 clean-install and end-to-end evidence is linked from the main README; this macOS recording does not replace that certification.
