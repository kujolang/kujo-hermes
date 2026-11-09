# A coupon must not add shipping

A $50 cart qualifies for free shipping. Applying a 10% coupon should make it $45. The fixture instead charges $50.99 because it checks eligibility after the discount.

The native workflow validates a Spec contract, runs three real Python tests through Kujo Eval, preserves the failure receipt, changes one line, reruns the unchanged tests and preserves the passing receipt. A separate verifier checks receipt digests and artifact snapshots. The correction is applied by the fixture driver; this is a reproducible integration demonstration, **not a claim of an autonomous model repair**.

## Run from a clean state

Use the Python environment from a supported Hermes installation. For a source checkout, include the Hermes source directory on `PYTHONPATH`. Set paths to your installed canonical sources and official runtime:

```sh
python demo/checkout/run.py \
  --sources /absolute/path/to/hermes-sources \
  --kujo /absolute/path/to/kujo \
  --output /tmp/kujo-checkout-take-1
python demo/checkout/verify.py /tmp/kujo-checkout-take-1
```

The output directory must not exist. Repeat with `take-2` to reset without deleting evidence. The script asks for native execution approval and pauses before applying the disclosed correction. `--test-decisions` replaces only the human transport with deterministic denial/approval answers; real Hermes hooks, registry, canonical tools and receipt storage still execute. Do not use that flag to film a supposed human approval.

Expected measured results: before, **2 passed / 1 failed**, with `AssertionError: 5099 != 4500`; after, **3 passed / 0 failed**. Both receipts and snapshots remain under the output directory. No network/model service is required for this deterministic proof. Existing installed source dependencies are required.

## Record a real Hermes conversation

Copy `fixture/` into a new Git repository, trust that exact root with `hermes kujo setup --trust-workspace /absolute/path`, and start a fresh conversation. Use the prompts and framing in [the storyboard](../../docs/hackathon/DEMO-STORYBOARD.md). Let Hermes edit `checkout.py`; do not run the driver and imply Hermes made its deterministic correction. Capture the actual model, result and approvals. Local/free model behavior is nondeterministic; rehearse without claiming guaranteed autonomous completion.

The committed [November 9 evidence](../../docs/hackathon/evidence/) includes actual native receipts and before/after artifacts. Verify it without importing Hermes or the plugin:

```sh
python3 demo/checkout/verify.py docs/hackathon/evidence
```

This proves the saved JSON and artifact snapshots match their hashes. It does not prove authorship, protect against an attacker replacing both files and checksums, or establish correctness outside these three tests. Kujo does not intercept arbitrary commits or releases.
