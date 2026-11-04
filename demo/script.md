# Reproducible demo: target 85 seconds

Prepare a fresh sample repository:

```sh
python3 demo/prepare.py /tmp/kujo-hermes-demo
```

Install the plugin and canonical sources as documented in README. Set `profile: full` and add `/tmp/kujo-hermes-demo` (its resolved real path on macOS may be `/private/tmp/kujo-hermes-demo`) to `trusted_workspaces`. Use a real interactive Hermes conversation, manual approvals and a working model. Do not use the automated test decision callback in the recording.

| Time | Screen / action | Voiceover |
|---|---|---|
| 0–12s | Show `hermes plugins doctor` and `/kujo doctor` with configured runtime | “Kujo Hermes brings Kujo's developer tools directly into Hermes. No other agent plugin is required.” |
| 12–25s | Prompt: “Discover the Kujo tools available for repository inspection, PackWrite context, Spec validation and Eval verification.” | “A compact native interface discovers engineering, context, verification and orchestration tools.” |
| 25–55s | Prompt: “In /private/tmp/kujo-hermes-demo, inspect with Scout, summarize the existing PackWrite pack, validate task.spec.json, and run eval.json. Ask for required approvals.” Approve Scout and Eval in the real host panel. | “Each step invokes the actual canonical tool. Repository mutations need a human approval.” |
| 55–75s | Prompt: “Show Eval's passed and failed counts. Retrieve its execution receipt and identify the canonical Ability, command and evidence hashes.” | “Results stay structured. Receipts link the exact operation to its evidence.” |
| 75–85s | Prompt: “Run ShipCheck and summarize remaining release blockers, citing its receipt. Do not call this release-ready unless its checks pass.” | “Kujo's wider tooling ecosystem, inside Hermes, with verifiable execution and clear boundaries.” |

Exact native calls if explaining the tool trace:

```json
{"ability":"kujo.scout.repository.inspect","input":{},"workspace":"/private/tmp/kujo-hermes-demo"}
{"ability":"kujo.packwrite.pack.summary","input":{},"workspace":"/private/tmp/kujo-hermes-demo"}
{"ability":"kujo.spec.contract.validate","input":{"file":"task.spec.json"},"workspace":"/private/tmp/kujo-hermes-demo"}
{"ability":"kujo.eval.suite.run","input":{"config":"eval.json"},"workspace":"/private/tmp/kujo-hermes-demo"}
{"ability":"kujo.shipcheck.repository.scan","input":{},"workspace":"/private/tmp/kujo-hermes-demo"}
```

Use the returned actual `receipt_id` with `kujo_receipts`. Never paste a fabricated ID, show a prewritten success as execution, or hide failed checks. The sample is intentionally small; ShipCheck can report remaining release concerns. If waiting is edited out, label the cuts. Rehearse against the installed model before recording; the 85-second schedule is a script, not a measured recording duration.

The repeatable host E2E test runs the same native workflow with deterministic human decisions and creates real receipts. That test is verification evidence, not substitute footage of an autonomous conversation. No video has been recorded or posted by this project.
