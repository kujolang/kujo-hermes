# Readiness — 2026-11-04

**Verdict: working native integration with documented coverage gaps.** The plugin has not been submitted to or approved by the marketplace. No release, external PR, X post or form submission has been made.

## Delivered

Standalone source plugin with six native Hermes tools, `/kujo`, engineering skill, 51 Ability bindings (all 38 Kujo CMD reference IDs plus 13 additional operations), four tool profiles, catalogs reviewed by the operator, exact workspace trust, native human approval, process cancellation, output limits and verifiable receipt hashes. The underlying tools own their implementations. No CommandCode or other host-plugin runtime dependency.

Architecture, exact-schema inventory, parity matrix, configuration, security notes, pinned source installer, CI, source packaging, catalog PR materials, X draft and reproducible 85-second demo are included. Research covers 104 repositories and records the source of each canonical definition. Entries based only on repository metadata say so.

## Verification evidence

| Check | Result | Evidence |
|---|---|---|
| Unit / boundary regression | 32 passed | `evidence/unit-tests.txt` |
| Real canonical operations | 45 passed, including ShipCheck, PackWrite, Eval, Spec, Scout, Dispatch, Loop, language/MCP tools | `evidence/real-tools.json` |
| Watchdog | Real SQLite service health and batch recording passed | `evidence/service-tools.json` |
| Live PackWrite | Provider-generated pack and separate validation passed | `evidence/live-packwrite.json` |
| Native Hermes | Actual v0.22.7 loader, registry, denial/approval, six-step workflow, receipt verification, failure and unload passed in host and in-process modes | `evidence/hermes-live-e2e.json`, `evidence/hermes-e2e.json` |
| Live model inside Hermes | Gemma via Ollama discovered, inspected and executed ShipCheck and retrieved its verified receipt using native deferred tools | `evidence/live-hermes-model.json` |
| Linux supported runtime | Python 3.14, clean locked Hermes dependencies, plugin dependency validation and real host workflow passed | `evidence/ci-linux.json`, `evidence/hermes-linux-e2e.json` |
| Clean independent installation | Real Git install at full SHA into a fresh Hermes home, dependencies approved and plugin left disabled | `evidence/clean-install.txt`, CI run 41925825469 |
| Reproducible demo | All five real fixture operations passed | `evidence/demo-verification.json` |
| Recorded walkthrough | Local free-model Hermes run: discovery, Spec, PackWrite, approved Eval 2/2 and verified receipt; 85-second video | `demo/walkthrough/evidence/` |
| Source installation | Exact official ShipCheck commit installed by helper | `evidence/source-install.txt` |
| Loop / PackWrite development | Actual harness gates and pack compiler used; first gate defect corrected | `.loop-engineering/`, `evidence/packwrite.log` |
| Performance | 20 local samples, serialized schema bytes and latency; no tokenizer or speedup claims | `evidence/performance.json` |

A test-only CLI callback supplies approval decisions in automated E2E tests. A separate test runs a live LLM conversation. A successful ShipCheck command can correctly report release blockers. Tests check product fields, artifacts and receipt integrity as well as exit status.

## Remaining gaps and exact next actions

- **Lens browser execution:** real launch fails because pinned Chromium headless shell build 1228 is absent. Install Lens's pinned browser through canonical setup, then rerun `scripts/optional-tools.py`. Flow validation passes; browser execution is not certified.
- **Workcell isolated execution:** real doctor/run fails because Docker's daemon socket is unavailable. Start a supported engine and make the reviewed image available locally; rerun optional checks. The plugin never pulls an image implicitly. Definition validation/inspection pass.
- **Producer catalog parity:** CMS, SSG and MCP producer-owned runtime Abilities do not have a configured application gateway here. The inventory lists their definitions, but execution needs a binding. Supply a verified operator binding or implement/test a gateway adapter. MCP profile generation is independently verified and is not a substitute for these producer handlers.
- **Foreman / other applications:** no canonical Foreman executable or repository was found. Agency Runner/Relay and additional application domains lack verified native bindings; inventory entries remain explicit gaps. No invented interface is exposed.
- **Local download failures:** local isolated-runtime downloads time out against PyPI. Fresh installation and dependency validation succeeded in Linux CI run 41925825469. Local failures remain in `evidence/git-install.txt` and `hermes-validation-final.txt`; they no longer block the clean-install acceptance criterion.
- **Compatibility:** live verification is macOS with Hermes v0.22.7 and official Kujo 1.8.0. Windows is unsupported. Linux Python 3.14 CI and canonical host E2E also pass. The local Kujo 1.9 development build lacks runtime-db; version checks alone cannot certify optional native features.
- **Marketplace / demo:** the [85-second walkthrough](../demo/walkthrough/delivery/kujo-hermes-walkthrough.mp4) is recorded; watch and listen before posting. Review the full-SHA catalog candidate and validate with dependency installation. Obtain explicit authorization before opening the catalog PR, posting the video or submitting the links. The user-provided deadline is November 11, 2026 at 5 PM EST; verify current event terms.

The verified operations are ready to use. Full tool coverage and marketplace submission still require the work listed above.

## Native setup and square film — November 5, 2026

The public plugin now registers `hermes kujo setup` and `hermes kujo doctor` in Hermes's default in-process mode. Setup verifies the installed runtime, installs 26 pinned canonical source checkouts and writes the active profile through Hermes's configuration API. Workspace trust is explicit. Existing denials, trust and unrelated settings survive. Failed new fetches leave no partial checkout. Isolated-host profiles retain manual configuration; all six native tools still pass there.

Evidence in `demo/square/evidence/` includes 61 passing unit tests, six native setup checks, the actual public GitHub install and successful setup capture, Doctor discovery of 51 bindings, and complete real-host workflows in both plugin modes plus the selected Python 3.14.9 environment. Host workflow approvals use the disclosed test callback; the film's approval excerpt comes from the original real free-model session. The supported Python run checks Scout, PackWrite summary, Spec, Eval, ShipCheck, Loop, denial, receipts and unload. This does not erase other tools' external prerequisites or the limitations above.

The square film is a separate 88-second deliverable, with matched native evidence, paired logos, ten glitch joins and an install call to action. Its review and exported-file measurements live beside the project. No npm wrapper, release publication, catalog pull request or contest submission was added.
