# Demo storyboard — 86 seconds

Recorded replacement: [70-second checkout showcase](../../demo/checkout-video/README.md), with its [actual timeline](../../demo/checkout-video/STORYBOARD.md). The real local-model run, operator approvals, missed approval timeout/retry and verification evidence are preserved there. The original proposal below remains historical.
## The memorable moment

A 10% coupon makes a $50 cart cost **$50.99**. Hermes's initial code looks plausible. Kujo Eval exposes the exact assertion, `5099 != 4500`. The correction changes one expression; the same three tests pass. Both receipts survive. The benefit is concrete: catch an agent's regression and hand another developer the evidence.

This is a recording plan backed by two deterministic native runs, not a claim that the revised autonomous video has been recorded. The existing 88-second square film remains a separate artifact. Do not reuse its passing Eval screen under narration about a failure.

## Prepare the take

Prerequisites: installed Hermes with a supported Python environment, official Kujo >=1.6,<2, Git and the pinned sources. Use an existing free/local tool-capable model only after a real rehearsal. Record its exact name/version; do not imply free hosted availability without checking. No model response is predetermined. Keep the deterministic reproduction for debugging, not as a disguised model conversation.

```sh
cp -R demo/checkout/fixture /tmp/kujo-checkout-film-1
cd /tmp/kujo-checkout-film-1
git init
hermes plugins install kujolang/kujo-hermes
hermes kujo setup --trust-workspace /tmp/kujo-checkout-film-1
hermes
```

The destination must be new. Repeat with `film-2` for a reset. Record a new conversation; do not overwrite the failed evidence. Installation includes dependency/enable prompts and setup source downloads. If waits are shortened, label the cut “installation wait shortened.” Never imply the separate Kujo runtime was installed by these two commands.

First prompt:

> This checkout charges $50.99 for a $50 cart with a ten percent coupon. Free-shipping eligibility must use the original subtotal. Use Kujo Spec to validate task.spec.yml, then Kujo Eval to run eval.json before changing anything. Show the failing check and receipt. Do not change the tests.

Approve only the displayed expected execution. Follow-up:

> Correct checkout.py, keeping the tests unchanged. Rerun the same Kujo Eval suite. Retrieve the failing and passing receipts, explain what changed, and state what these checks do not cover. Do not commit or release anything.

The expected tool inputs are real, tested interfaces:

```json
{"ability":"kujo.spec.contract.validate","input":{"file":"task.spec.yml"},"workspace":"/tmp/kujo-checkout-film-1"}
{"ability":"kujo.eval.suite.run","input":{"config":"eval.json"},"workspace":"/tmp/kujo-checkout-film-1"}
```

Use `kujo_receipts` with the actual returned `receipt_id`; paginate if required. Do not insert a known old ID as though it came from this take. Tool search/inspection may occur before execution and can be condensed transparently. Spec validates the contract format; it does not prove implementation compliance.

## Shot list

| Time | Actual screen/action | Narration or caption | Framing and transition |
|---|---|---|---|
| 0–3 | Existing Kujo × Hermes bumper, shortened | “A coupon should save your customer money.” | Square 1080 master; same monochrome logos. Brief original glitch into the actual view. |
| 3–10 | Real fixture result or Hermes's inspected checkout: `total(5000, 10)` gives `5099`; show requirement `4500` | “This one adds shipping. A fifty-dollar order becomes fifty dollars and ninety-nine cents.” | Full application width; one large caption: “Coupon adds $5.99 shipping.” No row of feature names. |
| 10–17 | Real install/setup capture, then Hermes plugin available | “Install the plugin, set up Kujo for this repository, then ask Hermes to check its work.” | Two native commands; small but readable prerequisites “Hermes + Kujo + Git.” Condense only waiting. |
| 17–24 | Actual first prompt; Spec returns `valid: true`; Eval approval appears | “Spec keeps the task's requirements explicit. Before repository code runs, you review the execution.” | Show the prompt and genuine human approval. No deterministic callback presented as a click. |
| 24–34 | Real Eval result, 2 passed / 1 failed; open failed test detail | “Eval runs the checks. The coupon test fails: fifty ninety-nine instead of forty-five. We have the exact failing command and assertion.” | Hold `5099 != 4500` for at least 4 seconds. This is the defining moment. Show only the relevant result pane at a readable size, without clipping text. |
| 34–44 | Follow-up prompt; Hermes edits `discounted >= 5000` to `subtotal_cents >= 5000` | “Hermes corrects the shipping rule. Eligibility uses the original subtotal. The tests stay unchanged.” | Real diff, one line. If model takes longer, cut waiting and disclose time compression. Do not animate fake typing. |
| 44–55 | Approve rerun; actual same Eval suite, 3 passed / 0 failed | “Run the same checks again. All three now pass, including the case that failed.” | Full result visible; one headline “Same tests. 3 passed.” Brief restrained glitch between completed scenes. |
| 55–67 | Retrieve both native receipts; show real IDs, command and artifact references | “Both runs remain available. Another developer can inspect what ran, the failure and the corrected result.” | A clean evidence view derived from this take is acceptable only labeled “Recorded execution evidence”; do not disguise it as chat. |
| 67–75 | Run `python3 demo/checkout/verify.py <take-evidence-directory>` against exported snapshots, or show its verified original output | “The saved files can be checked independently. These are records of the checks—not a claim that every possible bug is gone.” | Use actual export from this take. The committed deterministic proof may be shown only with its distinct provenance label. |
| 75–81 | Hermes compact discovery showing ShipCheck, PackWrite and Scout | “The same native tools also give you release checks, execution packs and repository inspection.” | Names secondary to benefits; avoid opening five tiny windows. No claim of PackWrite generation in this shot. |
| 81–86 | Same Kujo/Hermes outro with repo and install CTA | “Install Kujo Hermes. Keep the evidence with the work.” | Brief original glitch into bumper. “Install today · github.com/kujolang/kujo-hermes”. No contest mention. |

If the independent export adds complexity, remove the 67–75 shot and extend the actual receipt view. The stronger film is the one that remains authentic and readable. Do not introduce an unimplemented export command. The supplied reproduction script already produces export files; a new autonomous take must copy its actual receipts/artifacts or omit the export claim.

## Production and acceptance

- Master 1080×1080, 30 fps; downloadable 480×480 H.264/AAC, fast-start MP4. Keep duration at 86 seconds; verify container duration under 90.
- Full application width remains visible. Arrange the actual window before recording so important content fits; do not shrink a wide desktop into illegible text. Main result text should be roughly 24 pixels or larger in the 480 export. Preview on a phone.
- One caption per shot. Remove persistent header/footer stacks. Keep the pointer still except when it explains an action.
- Keep the familiar intro/outro and short glitch joins, including bumper boundaries; no glitch over the failed assertion or receipt details. Technology supplies the drama.
- Match each sentence to its own actual result. Hold failure and success long enough to read. Use silence or room tone under approval rather than racing through it.
- Record narration after the take is verified. Audition it; loudness measurements alone are not listening. Captions should not cover the evidence.
- Save raw capture, full model conversation, approvals, source diff, unchanged test hash, receipts and timeline. Note model, host/source versions, any condensed waits and each derived view.
- Before delivery: inspect beginning/middle/end frames, all transitions, text bounds, audio sync, 480p readability and both receipt IDs. Have a person unfamiliar with Kujo explain the benefit after watching.

## Rehearsal fallback

The deterministic native workflow is reproducible with `demo/checkout/run.py`; it has already produced real red/green evidence. If the free model fails the repair, report that result and retry from a new fixture without weakening tests. A film can honestly show a developer applying the correction while Hermes runs verification, but its narration must say so. Do not manufacture an autonomous success to meet the storyboard.
