# Readiness — 2026-11-04

**Verdict: working native integration; partial ecosystem certification.** Not yet a submitted or marketplace-approved plugin. No release, external PR, X post or form submission was performed.

## Delivered

Standalone source plugin with six native Hermes tools, `/kujo`, engineering skill, 51 Ability bindings (all 38 Kujo CMD reference IDs plus 13 additional operations), four exposure profiles, dynamic reviewed catalogs, exact workspace trust, native human approval, process cancellation, bounded structured output and hash-verifiable receipts. Canonical implementations remain upstream. No CommandCode or other host-plugin runtime dependency.

Architecture, exact-schema inventory, parity matrix, configuration, security notes, pinned source installer, CI, source packaging, catalog PR materials, X draft and reproducible 85-second demo are included. Organization research covers 104 repositories and retains source attribution for canonical definitions; metadata-only inspections are explicitly labeled.

## Verification evidence

| Check | Result | Evidence |
|---|---|---|
| Unit / boundary regression | 32 passed | `evidence/unit-tests.txt` |
| Real canonical operations | 45 passed, including ShipCheck, PackWrite, Eval, Spec, Scout, Dispatch, Loop, language/MCP tools | `evidence/real-tools.json` |
| Watchdog | Real SQLite service health and batch recording passed | `evidence/service-tools.json` |
| Live PackWrite | Provider-generated pack and separate validation passed | `evidence/live-packwrite.json` |
| Native Hermes | Actual v0.22.7 loader, registry, denial/approval, six-step workflow, receipt verification, failure and unload passed in host and in-process modes | `evidence/hermes-live-e2e.json`, `evidence/hermes-e2e.json` |
| Live model inside Hermes | Gemma via Ollama discovered, inspected and executed ShipCheck and retrieved its verified receipt using native deferred tools | `evidence/live-hermes-model.json` |
| Reproducible demo | All five real fixture operations passed | `evidence/demo-verification.json` |
| Source installation | Exact official ShipCheck commit installed by helper | `evidence/source-install.txt` |
| Loop / PackWrite development | Actual harness gates and pack compiler used; first gate defect corrected | `.loop-engineering/`, `evidence/packwrite.log` |
| Performance | 20 local samples, serialized schema bytes and latency; no tokenizer or speedup claims | `evidence/performance.json` |

Host approval decisions in automated E2E are supplied by a test-only CLI callback. The live LLM test is separate evidence, not a relabeled callback test. A successful ShipCheck command can correctly report release blockers. Real tests assert product fields/artifacts and receipt integrity, not just exit status.

## Remaining gaps and exact next actions

- **Lens browser execution:** real launch fails because pinned Chromium headless shell build 1228 is absent. Install Lens's pinned browser through canonical setup, then rerun `scripts/optional-tools.py`. Flow validation passes; browser execution is not certified.
- **Workcell isolated execution:** real doctor/run fails because Docker's daemon socket is unavailable. Start a supported engine and make the reviewed image available locally; rerun optional checks. The plugin never pulls an image implicitly. Definition validation/inspection pass.
- **Producer catalog parity:** CMS, SSG and MCP producer-owned runtime Abilities do not have a configured application gateway here. Definitions are inventoried, not executable merely because discovered. Supply a verified operator binding or implement/test a gateway adapter. MCP profile generation is independently verified and is not a substitute for these producer handlers.
- **Foreman / other applications:** no canonical Foreman executable or repository was found. Agency Runner/Relay and additional application domains lack verified native bindings; inventory entries remain explicit gaps. No invented interface is exposed.
- **Clean dependency installation:** the official catalog validator's isolated Hermes runtime dependency download has encountered PyPI timeouts. Manifest, capabilities and public-surface validation pass on fallback; `evidence/hermes-validation-final.txt` records the final truststore download timeout and passing fallback validation. A fallback does not establish clean install success.
- **Compatibility:** live verification is macOS with Hermes v0.22.7 and official Kujo 1.8.0. Windows is unsupported. Linux CI is configured but remote results must be checked. The local Kujo 1.9 development build lacks runtime-db; version checks alone cannot certify optional native features.
- **Marketplace / demo:** record the prepared demo; review the full-SHA catalog candidate and validate with dependency installation. Obtain explicit authorization before opening the catalog PR, posting the video or submitting the links. The user-provided deadline is November 11, 2026 at 5 PM EST; verify current event terms.

These gaps prevent claiming complete ecosystem certification or marketplace readiness. They do not prevent installed, authorized users from using the verified native integration now.
