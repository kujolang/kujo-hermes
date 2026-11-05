# Kujo Hermes hardening: second pass, 2026-11-04

## Repository and scope

Repository `kujolang/kujo-hermes`, `main`, starting SHA
`fa889919e874ba929efd48328166beeb25376229`. This is a fresh fix-mode review following
[the first pass](repository-hardening.md), whose report and evidence are preserved.
Verified ending code SHA: `5be2e9fd308167444d3c0f7dadcfe4d71df386ca`. The following audit commit contains only this report and verification evidence.

The six-tool Python Hermes adapter delegates to canonical Kujo CLIs, with jsonschema
and a vendored Ability validator. Source pins, profiles, approval semantics and
supported POSIX hosts remain unchanged. Existing, actively changing walkthrough
files were present at entry and are outside this pass; they are neither staged nor
reverted. Thus the shared working tree cannot be made clean without interfering
with unrelated work. Only this pass's files are committed.

## Baseline and findings

The supported Python 3.11.16 environment passed 39 tests before edits. Six new
lifecycle regressions were run against an archive of the starting commit: all six
failed (two assertion failures, four errors). The final suite passes 45 tests.
Evidence is under `evidence/hardening-2026-11-04-pass2/`.

| ID | Priority | Area | Finding / evidence | Action | Status / confidence |
|---|---|---|---|---|---|---|
| L1 | P0 | Cancellation | `process.run` spawned even when its cancellation event was already set, allowing effects before its loop noticed cancellation | Return cancelled before Popen with null exit code | Fixed; regression; high |
| L2 | P0 | Capacity | Thread.start failure left an inserted job marked running with an unset completion event, consuming a slot and delaying unload | Mark failed and signal completion in execution startup error cleanup | Fixed; repeated failed-start and subsequent successful-execution regression; high |
| L3 | P0 | Extension contracts | `_perform` dispatched on a copied internal operation such as catalog instead of the approved extension argv | Extensions always take argv execution path | Fixed; actual subprocess regression; high |
| L4 | P0 | Receipt integrity | Final `.json` files were visible during write/fsync and remained partial after storage failure | Write and fsync private temporary file; atomically publish via non-replacing hard link; always clean temporary file | Fixed; visibility and injected storage-failure regressions; high |
| L5 | P0 | Background failure semantics | Failed receipt persistence escaped the worker, leaving no retrievable receipt and no actionable status | Return bounded, redacted failure with invocation ID and receipt_persisted:false; retain it in current job for status lookup | Fixed; background storage-failure regression; high |

P0 follows this skill's correctness/integrity classification; it is not a claim of
critical exploit severity. No findings are deferred from this table.

## Changes, compatibility and efficiency

Implementation is confined to `process.py` and `service.py`, with six tests in
`tests/test_lifecycle.py` and updates to architecture, configuration and testing docs.

No dependency, catalog, tool-schema, config-key, environment-variable or CLI change.
Receipt JSON and hashes retain the v1 format. Process cancellation before creation
now reports `exit_code:null` because no process existed. Extension declarations may
carry old internal operation names, but execution correctly honors their reviewed
argv. Approval is still required for every extension.

Persistence failures return `ok:false`, `status:failed`, `receipt_persisted:false`, an
invocation ID and bounded/redacted storage diagnostics rather than claiming a receipt
exists. The current job exposes this failure until completed jobs are pruned by a
subsequent execution or the plugin is unloaded. This is explicitly not durable
recovery when storage is unavailable. No automatic execution/write retry is added;
canonical artifacts must be inspected before repeating potentially completed effects.

Atomic hard-link publication is supported on the documented local macOS/Linux POSIX
filesystems and refuses existing destinations, including symlinks. If the storage
filesystem disallows hard links, persistence fails explicitly. File contents are
fsynced before publication; this does not claim parent-directory durability across
power loss. Failures leave no partial final JSON or temporary file.

No timing/RSS/token improvement is claimed or benchmark gate introduced: these are
correctness changes, including an additional temporary-file publication step. Six
native tool schemas, progressive discovery, bounded output and dependency surface
are unchanged. Failed thread creation now consumes zero active slots; cancelled
before-start work launches zero subprocesses (tested). Storage failures remain concise.

## Checklist coverage

| Phase | Evidence / disposition |
|---|---|
| 0: ground truth | Re-read current service/process/approval/catalog/config/evidence and CI; checked Git status, prior report, manifests and recorded contracts from preceding pass. Native tools and canonical subprocess/receipt boundaries remain scope. |
| 1: baseline | 39 existing tests pass; six new tests fail against original archive. No pre-existing test failure. |
| 2: complexity | Targeted lifecycle changes, no broad reformatting or speculative wrappers. Existing command mapping retained. |
| 3: runtime | L1 avoids launching work already cancelled; no performance-speed claim. |
| 4: resources | L2 removes leaked active slots; L4 cleans write temporaries. Existing four-job and output limits remain. |
| 5: context | Six tool registrations, discover/inspect progression, no conversation replay or agent handoff duplication; no automatic retries. Storage failure response bounded. |
| 6: command output | Full receipt evidence remains on disk when persistence succeeds; storage failures explicitly say it did not. No silent truncation introduced. |
| 7: errors | Thread start and synchronous/background persistence failure paths now covered. |
| 8: security | Exact workspace trust, approval gate, argv-only dispatch, secret filtering and loopback transport retained. Publication cannot overwrite receipts/symlinks. L3 makes execution match reviewed argv. No new permission grants. |
| 9: concurrency/state | L1/L2/L4/L5 address startup, completion, visibility and failure state. Existing cancellation/group cleanup tests retained. |
| 10: contracts | API corrections and null exit code described above; no receipt schema migration. |
| 11: dependencies | No dependency change; source pins/CI runtime lock retained. No fresh external vulnerability-database audit claimed. |
| 12: tests | Six public-behavior regressions plus existing 39 tests; real canonical and host integration checks. |
| 13: CI | unittest discovery includes new file automatically. No flaky latency thresholds; existing Linux supported-runtime job retained. |
| 14: docs | Documented nonpersisted receipt response, retention lifetime, pre-start cancellation and atomic publication. Prior audit unchanged. |
| 15: agent experience | Status exposes actionable storage failure instead of a missing-receipt exception; no extra tool or schema registration. |
| 16: dead weight | No proven-unused code/dependencies removed; release/demo assets have consumers and concurrent changes. |
| 17: fixes | L1–L5 implemented and regression-tested. |
| 18: verification | Commands and results below; no known introduced regression. |

## Verification receipt

`HPY=/Users/robertdevore/.hermes/hermes-agent/venv/bin/python3` (3.11.16).
Commands run from the repository root, except archive replay in a temporary directory.

| Command | Result |
|---|---|
| `$HPY -m unittest discover -s tests -v` before | PASS, 39 tests |
| `$HPY -m unittest discover -s tests -p test_lifecycle.py -v` against archived starting code plus new test file | Expected FAIL, six reproduced regressions |
| `$HPY -m unittest discover -s tests -v` after | PASS, 45 tests |
| `python3 scripts/real-tools.py --sources .. --kujo .local/runtime/kujo --output /tmp/hermes-pass2-real.json` | PASS |
| `PYTHONPATH=/tmp/kujo-hermes-host $HPY tests/hermes_e2e.py --sources .. --kujo .local/runtime/kujo --isolation host` | PASS |
| `PYTHONPATH=/tmp/kujo-hermes-host $HPY tests/hermes_e2e.py --sources .. --kujo .local/runtime/kujo --isolation in_process` | PASS |
| `python3 -m build --sdist --outdir /tmp/hermes-pass2-dist` | PASS, isolated declared build dependencies |
| `git diff --check` | PASS |

Host checks use the same released Hermes v0.22.7 source as the first pass and its
local dependency environment, with test approval callbacks. They do not constitute
new Linux Python 3.14 certification or live model approval. Canonical tool outputs
are checked for product fields and every receipt hash, not exit status alone.

## Remaining work and cross-repository requirements

No other repository needs a change for these fixes. No new unresolved P0–P2 issue.
**Needs more evidence:** fresh remote CI, optional browser/container execution and
producer gateways retain the previously documented certification limits.
**Not worth changing:** timing budgets, caching, broad formatting and dependency churn.
Concurrent walkthrough work remains untouched and outside the clean-tree claim.
SignalBox: no captures warranted; no new surviving finding requiring human review.
