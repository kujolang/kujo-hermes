# Kujo Hermes hardening — 2026-11-04

## Scope and baseline

Fix-mode review of `kujolang/kujo-hermes`, branch `main`, starting at
`20c6873e8384833b0ba07a477831b93a72f27b1b`, initially clean. Verified ending implementation
SHA: `dd748a22bd47ef74439ad38b3d94c00e6bd71c03`; the subsequent audit commit contains only this report and evidence. This pass covers the native Python
adapter, catalogs, configuration, packaging, tests, scripts and CI; media assets
and upstream implementations are not re-engineered. No other repository was edited.

The plugin registers six Hermes tools and dispatches 51 canonical Kujo operations.
Dependencies are jsonschema, the vendored Ability contract validator, operator-owned
source checkouts and a Kujo runtime. Host verification uses released Hermes v0.22.7
(`b200f5bc60e31588ba2cb60e288029c4a54ba5fa`).

Baseline: 32 tests pass on Python 3.10.5 and, separately from an archived starting
commit, supported Python 3.11.16. Seven new behavioral tests fail on the original
implementation and pass after correction. All detailed evidence for this run is
in `evidence/hardening-2026-11-04/`; earlier evidence remains historical and unchanged.

## Finding ledger

All findings below are high confidence, reproduced by tests or directly supported
by the identified implementation. P0 denotes correctness or trust-boundary defects,
not an assertion that every item is a critical exploitable vulnerability.

| ID | Priority | Area | Finding / evidence | Action | Status |
|---|---|---|---|---|---|
| H1 | P0 | Receipt integrity | `Service.receipts` bounded reads at twice the current output limit; JSON escaping expands control bytes sixfold, and lowering configuration invalidated old receipts | Share a fixed 32 MiB write/read ceiling, independent of process configuration | Fixed; two regressions |
| H2 | P0 | Failure evidence | `_perform` validated before assigning results, losing stdout/stderr and exit code on schema failure | Retain the result before validation, preserve failure status | Fixed; regression |
| H3 | P1 | Context volume | Validation errors could repeat the entire invalid result in the inline error | Bound error messages to 8192 characters; full command result remains in the receipt | Fixed; large invalid-output regression |
| H4 | P0 | Artifact correctness | `artifact_inventory` ignored input `path`, hashing stale root artifacts instead of nested execution outputs | Resolve explicit/default artifact targets relative to selected path; retain root-relative receipt names and containment | Fixed; regression |
| H5 | P0 | Runtime contract | Doctor accepted compatible version text despite exit 17 | Require completed status and exit zero consistently for doctor and execution probes | Fixed; regression |
| H6 | P0 | Network boundary | urllib inherited host proxies despite the loopback-only Watchdog contract | Explicit empty ProxyHandler; preserve redirect refusal | Fixed; local HTTP regression with hostile proxy configuration |
| H7 | P2 | Repeated work | `Catalog.get` called `exposed()` twice, reopening profiles and filtering twice | Use one local snapshot per lookup, without adding a cache | Fixed; existing catalog/profile tests |

## Coverage: phases 0–18

| Phase | Evidence and disposition |
|---|---|
| 0: ground truth | Read adapter modules, vendored validator, manifests, profiles, source pins, scripts, tests, architecture/security/readiness and engineering skill. Public tools, approvals, subprocesses and receipts are the important boundaries. |
| 1: baseline | Existing tests, archived baseline replay and 20-sample measurement script; evidence retained separately. |
| 2: complexity | Removed duplicate exposure calculation (H7). Compact existing modules are not broadly reformatted. |
| 3: runtime | No retries or remote registration work; bounded argv subprocess execution. H7 removes one profiles read/filter per lookup. Timing below is observational, not a performance guarantee. |
| 4: resources | Process output, catalog sizes, concurrent jobs, artifact files/bytes and Watchdog responses have bounds. Receipt reads/writes corrected (H1). Receipt retention remains explicitly operator-managed. |
| 5: AI context | Six small schemas; discover → inspect → execute; full catalog schemas are not eagerly registered. No conversation replay or child-agent context duplication in this adapter. No automatic execution retries. H3 prevents large errors bypassing compact receipts. |
| 6: output | Payloads over 12000 serialized bytes return a reference; receipt pages retain evidence. Errors are now bounded; no required result data is silently truncated. |
| 7: errors | H2/H3/H5; nonzero exit, timeout, output limit, missing source and approval failure remain distinct. |
| 8: security | Reviewed exact-root trust, path resolution, argv construction, local schema references, extension approval, secret allowlist/redaction and receipt symlink rejection. H6 closes proxy-dependent routing. Concurrent malicious filesystem mutation remains outside the documented trusted-workspace model. |
| 9: state/concurrency | Four active jobs checked under a lock before insertion; process groups killed on cancellation; grants locked and consumed once. Existing cancellation/child-cleanup tests pass. No retry or idempotency redesign. |
| 10: contracts | Six tool names, 51 Ability IDs, profiles, argv shapes and receipt schema preserved. Corrections and bound change described below. |
| 11: dependencies | One Python runtime dependency, bounded version ranges; vendored MIT SDK provenance and exact source lock; CI runtime lockfile. No new dependencies. No claim of a current CVE audit. |
| 12: tests | Seven behavioral regressions, all fail before and pass after; 39 tests total. Real canonical operations, Watchdog and native Hermes checks recorded. |
| 13: CI | Existing unittest discovery automatically includes new tests. Existing Linux/Python 3.14 native host CI remains intact. No timing gate added; normal growth requires intentional tests/docs updates, not numerical performance thresholds. |
| 14: docs | Configuration, architecture, testing and security updated for corrected behavior; historical readiness evidence is not rewritten as this run. |
| 15: agent experience | Concise six-tool discovery and existing skill are sufficient; preserved actionable failures and added a reproducible audit. No additional instruction layer. |
| 16: dead weight | Generated/demo/submission assets have documented consumers; no uncertain removals. No unused dependency proven. |
| 17: implementation | H1–H7 implemented with practical regressions and affected docs. |
| 18: final verification | See receipt below; no known introduced regression. |

## Performance and efficiency

Same `python3 scripts/measure.py` on macOS, Python 3.10.5, 20 samples each:

| Metric | Before | After |
|---|---:|---:|
| Initialization median, ms | 0.1863 | 0.1940 |
| Discovery median, ms | 128.6269 | 133.1678 |
| Inspection median, ms | 0.3218 | 0.2271 |
| Native tool definition bytes | 2647 | 2647 |
| Full catalog discovery response bytes | 14700 | 14700 |

Raw samples preserve variability. These small timings are noisy; they support no
broad runtime-speed claim. The code removes one redundant profiles read per lookup.
Token counts, RSS/CPU and build time were not measured; no savings claimed.
Dependency surface is unchanged. A 300000-byte control-character output now produces
a retrievable receipt despite its JSON escaping. Inline error messages are capped
at 8192 characters while full output remains available through verified pages.

## Compatibility and security

No public tool/API names, Ability IDs, CLI bindings, schema identifiers, config
keys or environment names changed. The receipt file format is unchanged. Existing
receipts up to 32 MiB remain readable even after lowering process output limits.
New receipts over that fixed storage ceiling fail explicitly before creating a file.
Consumers now receive failed-command evidence after output schema rejection, correct
nested artifact references and a false doctor compatibility verdict on failed probes.
Watchdog intentionally ignores system/environment proxies to enforce direct literal
loopback transport. Operators relying on proxy routing for that local service must
connect directly. No migration is required for normal configured workloads.

Schema-error messages are concise diagnostics, not complete copies of schema/output;
inspect the Ability schema and retrieve the receipt for full evidence. The adapter
continues to trust operator-approved tools and workspace contents; it is not a sandbox.

## Verification receipt

Commands run from the repository root. `HPY` denotes
`/Users/robertdevore/.hermes/hermes-agent/venv/bin/python3` (Python 3.11.16).
These are local host API checks, not a new supported Python 3.14 Linux certification.

| Exact command / check | Status |
|---|---|
| `python3 -m unittest discover -s tests -v` before edits | PASS, 32 tests (Python 3.10.5, supplemental unsupported interpreter) |
| `$HPY -m unittest discover -s tests -v` in archived starting commit | PASS, 32 tests |
| `$HPY -m unittest discover -s tests -p test_hardening.py -v` with new regressions against archived starting code | Expected FAIL, seven regressions reproduced |
| `$HPY -m unittest discover -s tests -v` after edits | PASS, 39 tests |
| `python3 scripts/measure.py` before/after | PASS, 20 samples each; old performance evidence restored |
| `python3 scripts/real-tools.py --sources .. --kujo .local/runtime/kujo --output /tmp/kujo-hermes-hardening-real.json` | PASS, 45 operations and all receipt hashes |
| `python3 scripts/service-tools.py --sources .. --kujo .local/runtime/kujo` | PASS, actual Watchdog SQLite service health and telemetry |
| `PYTHONPATH=/tmp/kujo-hermes-host $HPY tests/hermes_e2e.py --sources .. --kujo .local/runtime/kujo --isolation host` | PASS, actual loader/approval/workflow/receipts/unload |
| `PYTHONPATH=/tmp/kujo-hermes-host $HPY tests/hermes_e2e.py --sources .. --kujo .local/runtime/kujo --isolation in_process` | PASS, actual loader/approval/workflow/receipts/unload |
| `python3 -m build --sdist --no-isolation --outdir /tmp/kujo-hermes-hardening-dist` | Unavailable in default interpreter: installed setuptools does not satisfy >=68,<81; isolated build retried |
| `python3 -m build --sdist --outdir /tmp/kujo-hermes-hardening-dist` | PASS with isolated declared build dependencies |
| `git diff --check` | PASS |

Actual source HEADs and dirty flags, platform and runtime hash are recorded in
`environment.json`; all 26 inspected sibling source checkouts matched their release-lock commits and were clean. Host approvals use deterministic test
callbacks, not live human consent. No live model call was needed for these changes.

## Remaining work and cross-repository boundaries

No unresolved finding from H1–H7 and no cross-repository change required.
**Needs more evidence:** fresh Linux/Python 3.14 CI for this commit; browser/container
execution and producer gateway parity remain the pre-existing certification gaps in
`docs/readiness.md`. They were not retested or claimed resolved here.
**Not worth changing:** broad formatting, speculative caches, dependency replacement,
retention automation and removal of documented release/media assets.
No new P0/P1/P2 follow-up is deferred. Existing downstream certification/submission
commitments are already documented; no duplicate SignalBox captures warranted.
