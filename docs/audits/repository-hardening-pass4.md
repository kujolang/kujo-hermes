# Kujo Hermes hardening: fourth pass, 2026-11-04

## Scope, baseline and findings

Repository `kujolang/kujo-hermes`, branch `main`, starting SHA
`0acf4500e2a13a9a02dc49e61f771a110b8cbdca`. The branch already contained an unpushed
walkthrough commit and active untracked render artifacts; these were preserved.
Prior hardening reports remain unchanged. Verified ending implementation SHA: `816a4898536c72342622f8574de1bb64d761e56c`; the subsequent audit commit contains this report and evidence.

The six-tool Python Hermes adapter still delegates to 51 canonical Kujo operations,
using jsonschema, the vendored Ability validator and operator-owned source/runtime
installations. This pass reviews the existing adapter boundaries, concentrating new
regression probes on process setup and nested command output.

Baseline: 52 tests pass on Python 3.11.16. Two additional behavioral tests cover two
process-setup failures and output depths 128, 129 and 2000. Against archived starting
source, the failure subcases reproduce both defects (three assertion failures and
one error); depth 128 remains supported. Final suite: 54 tests pass.

| ID | Priority | Area | Finding / evidence | Action | Status / confidence |
|---|---|---|---|---|---|---|
| F1 | P0 | Resource lifecycle | Selector creation and pipe setup occurred outside process cleanup; either exception left a live child and open pipes | Put all post-spawn initialization inside try/finally; always terminate/reap child and close streams | Fixed; actual child processes with injected setup exceptions; high |
| F2 | P0 | Failure evidence | JSON parser recursion failure occurred before assigning raw result; deeper parsed output could reach recursive redaction and lose receipt persistence | Attach raw outcome before parsing; iteratively enforce a documented 128-container nesting limit before recursive processing | Fixed; actual output subprocesses and verified failure receipts; high |

P0 is the checklist's correctness/resource-integrity category, not a critical
vulnerability rating. No finding above is deferred.

## Implementation, compatibility and efficiency

Changes: `process.py`, `service.py`, two tests in `tests/test_failure_boundaries.py`,
and architecture/configuration/testing docs. No new dependency, tool registration,
Ability/CLI mapping, configuration key, environment variable or receipt schema.

Setup exceptions retain their original diagnostics while cleaning owned resources.
Structured subprocess output now supports up to 128 nested object/array containers.
Deeper valid JSON, or JSON exceeding the Python parser's recursion capacity, returns
a failed receipt with raw bounded stdout, stderr and exit code. It does not silently
truncate required evidence or pretend the canonical command itself returned nonzero.
Consumers of exceptionally deep outputs should flatten/split their structure or
emit artifact references. The command output byte limit and malformed-JSON text
fallback remain unchanged. Depth 128 has an explicit integration regression.

The iterative nesting check retains only iterators for the active path, rather than
copying all children into a work queue. This adds a correctness pass over parsed
JSON; no latency, RSS, token, binary-size or build-time improvement is claimed or
measured. Existing six tool schemas, progressive discovery and compact receipt
responses remain unchanged. There is no automatic execution retry or conversation
replay. Detailed failure evidence stays retrievable through receipts.

## Checklist coverage

| Phase | Evidence / disposition |
|---|---|
| 0: repository | Current Git state, process/service/network/evidence modules, packaging metadata and preceding verified contract reports reviewed; adapter subprocess boundary is the changed scope. |
| 1: baseline | 52 tests passed; archive replay reproduced both defects; logs preserved separately. |
| 2: complexity | Extended existing cleanup boundary; one focused iterative output-depth guard, no broad refactor. |
| 3: runtime | Setup failures no longer leave long-running children; JSON checking adds necessary bounded-depth traversal. No speed claim. |
| 4: resources | Actual child reaping and pipe closure tested for selector creation and pipe configuration failures. Depth bound protects recursive downstream processing. |
| 5: AI context | Six schemas and lazy discover/inspect remain; nested raw evidence is retained, not expanded into additional registrations or handoffs. |
| 6: output | No silent truncation; existing byte limits and receipt paging remain. Nested failure now returns a usable receipt reference. |
| 7: errors | Setup exception remains actionable; nested output is an explicit processing failure with the original command outcome preserved. |
| 8: security | Child ownership/cleanup and untrusted command output examined. Trust roots, approvals, secret redaction, loopback policy and argv-only execution retained. |
| 9: concurrency | Cleanup covers initialization as well as execution. Existing cancellation, capacity and atomic receipt tests still pass. |
| 10: contracts | Only new explicit output nesting bound; successful normal output and v1 receipt shape preserved. Migration described above. |
| 11: dependencies | No dependency or lockfile change. No new external vulnerability-database certification claimed. |
| 12: tests | Two behavioral tests with five subcases; full 54-test suite plus canonical/host integration. |
| 13: CI | Existing unittest discovery automatically runs the new tests. No flaky timing gate; assertions inspect process state and receipt content. |
| 14: docs | New nesting/cleanup behavior documented; previous reports and unrelated render assets preserved. |
| 15: agent experience | Deep output failure remains debuggable via receipt; no new tools or instructions. |
| 16: dead weight | No speculative removal; release/render artifacts have active consumers. |
| 17: fixes | F1/F2 implemented with practical regressions. |
| 18: verification | Commands below; no known introduced regression. |

## Verification receipt

`HPY=/Users/robertdevore/.hermes/hermes-agent/venv/bin/python3` (3.11.16).
Evidence directory: `evidence/hardening-2026-11-04-pass4/`.

| Command | Result |
|---|---|
| `$HPY -m unittest discover -s tests -v` before edits | PASS, 52 tests |
| `$HPY -m unittest discover -s tests -p test_failure_boundaries.py -v` against archived starting code plus new tests | Expected FAIL, both defects reproduced; baseline test cleanup reaps deliberately leaked children |
| `$HPY -m unittest discover -s tests -v` after edits | PASS, 54 tests |
| `python3 scripts/real-tools.py --sources .. --kujo .local/runtime/kujo --output /tmp/hermes-pass4-real.json` | PASS, 45 canonical operations and receipt verification |
| `PYTHONPATH=/tmp/kujo-hermes-host $HPY tests/hermes_e2e.py --sources .. --kujo .local/runtime/kujo --isolation host` | PASS |
| `PYTHONPATH=/tmp/kujo-hermes-host $HPY tests/hermes_e2e.py --sources .. --kujo .local/runtime/kujo --isolation in_process` | PASS |
| `python3 -m build --sdist --outdir /tmp/hermes-pass4-dist` | PASS |
| `git diff --check -- kujo_hermes docs tests` | PASS |

Host integration uses the previously verified released v0.22.7 source and local
Python 3.11 dependency environment, with deterministic test approval callbacks.
This does not newly certify Linux Python 3.14 or live-model consent.

## Remaining work and cross-repository boundaries

No cross-repository changes needed, no new unresolved P0–P2 finding.
**Needs more evidence:** remote CI for current revision and previously documented
browser/container/producer gateway certification gaps in `docs/readiness.md`.
**Not worth changing:** speculative caches, broad style churn, dependency replacement
or removal of active render artifacts. Unrelated render files remain outside this
pass's clean-tree claim. SignalBox: no captures warranted.
