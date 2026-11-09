# Verification ledger — November 9, 2026

This ledger separates runtime behavior, package validation and network-dependent installation. Read full logs: the Hermes validator can continue after dependency preparation fails.

| Check | Result / evidence |
|---|---|
| Baseline unit suite | 61 passed, `unit-baseline.log` |
| Updated unit suite | 61 passed, `unit-final.log` |
| Hermes source | Official v0.23.0, `2bd378ed1b8d6bf2192cb26e0a55ff3091e6bd19` |
| Native E2E | Passed, `hermes-023-e2e.json` and `.log`: six canonical operations, denial, approval, receipt retrieval, failed Spec, unload |
| Approval transport | Test-only deterministic human-decision callback through real Hermes hooks; not a live human or autonomous model claim |
| Checkout reproduction | Two fresh runs passed, `checkout-1.log` and `checkout-2.log`; final source rerun in `checkout-final.log` |
| Check outcomes | Before 2 passed / 1 failed, actual `5099 != 4500`; after 3 passed / 0 failed; same test file |
| Receipt export | `before-receipt.json`, `after-receipt.json`, `contract-receipt.json`, `checkout-native-run.json` |
| Artifact integrity | `independent-verification.log`: 10 before / 19 after artifacts and both receipt digests checked independently |
| Tamper rejection | `tamper-rejection.log`: altered snapshot artifact rejected; original evidence untouched |
| PackWrite | Existing execution pack validated, zero warnings, `packwrite-validate.log`; not a new generated pack |
| Loop | Actual canonical harness in `.loop-engineering/hackathon-audit/`; final verdict recorded there |
| Official Doctor | Passed on clean candidate tree, `doctor-023-clean-tree.log`, six tools / two hooks |
| Official validator | `validate-023-clean-tree.log` passes manifest/capabilities/security, but dependency setup failed on duplicate package names in an already-used profile; **not a full install-deps pass** |
| Fresh dependency attempt | `validate-023.log`: DNS/download failure; `validate-023-fresh-profile.log` is the separate fresh-profile retry, using the already-installed official runtime tool cache |
| Existing film audit | Actual decoded MP4 contact sheet `current-demo-frames.jpg`; no new film or audio audition claimed |

The native E2E used Hermes 0.23.0 source with an existing supported Python 3.14.9 environment. It does not alone certify a fresh 0.23.0 dependency resolution. The fresh-profile attempt and final public-pin installation are recorded separately below when finished.

Early doctor attempts targeted a developer tree containing large ignored `.local` environments; copying that tree exhausted temporary storage. A retry with TMPDIR inside the source was correctly refused as recursive. The successful Doctor used a clean source tree outside the repository. Do not copy development caches into a plugin candidate. These failed attempts remain in the logs rather than being passed off as product failures or successful checks.

Native code changes are limited to clearer tool descriptions; runtime execution architecture and policy are unchanged. CI now checks both the minimum supported host and current stable, and runs the actual checkout fixture. A newly configured job is not a passing CI result until its run finishes.
