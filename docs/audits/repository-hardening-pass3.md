# Kujo Hermes hardening: third pass, 2026-11-04

## Scope and baseline

Repository: `kujolang/kujo-hermes`, branch `main`, starting SHA
`318e1170adfe8e3000931b12d39a3c4f282e059e`. Verified ending implementation SHA: `0ab3f84a652d6f2a1f836e1790d4228e8b67785c`; the subsequent audit commit contains only this report and evidence.
This fix-mode pass preserves the first two audits and their evidence. Existing,
actively changing `agent/HANDOFF.md` and walkthrough files are outside these fixes;
only this pass's files are staged. The shared working tree is not claimed clean.

Purpose and dependencies remain the six-tool native Hermes adapter, 51 canonical
Kujo bindings, jsonschema, vendored Ability validation and pinned tool sources.
Baseline: 45 tests passed on Python 3.11.16. Seven new normalization/approval tests
all fail against an archived starting commit (six failures, one error). Final suite:
52 passing tests. Evidence: `evidence/hardening-2026-11-04-pass3/`.

## Finding ledger

| ID | Priority | Area | Finding and evidence | Action | Status / confidence |
|---|---|---|---|---|---|---|
| N1 | P0 | JSON Schema contract | `Catalog.inputs` treated boolean property schemas as dictionaries, raising TypeError for valid schemas | Only dictionary property schemas can supply defaults | Fixed; regression; high |
| N2 | P0 | Normalization | Input was validated before defaults only; defaults could violate property types or maxProperties | Validate the normalized object whenever defaults were added | Fixed; two regressions; high |
| N3 | P1 | Input resource boundary | Execution alone checked supplied size; approval preflight accepted oversized input, and defaults could expand past the 64 KiB bound | Shared compact UTF-8 JSON size check in execution and catalog normalization, before copy and after defaults | Fixed; two regressions; high |
| N4 | P1 | Error disclosure/context | Preflight errors bypassed the redaction/8192-character bound used by tool execution | Redact and bound preflight block messages | Fixed; regression; high |
| N5 | P1 | Approval resources | 100 pending requests were bounded, but repeatedly approved unused grants accumulated without a count bound | Pending requests plus unused grants share 100 entries, checked under the existing lock | Fixed; capacity/consume recovery regression; high |

P0 refers to the checklist's correctness/contract category, not exploit severity.
All findings above are resolved; none is deferred.

## Implementation and compatibility

Changed `catalog.py`, `approval.py`, and the shared size-check import in `service.py`.
Added seven tests in `tests/test_normalization.py`; updated architecture,
configuration and testing documentation. Existing unittest CI discovers them.

Supplied input still validates before defaults, so required properties must still
be explicitly supplied. Optional top-level defaults are applied as before, but
invalid or oversized expanded objects now fail before approval/execution. Boolean
property schemas now work. Valid requests and normalized request digests are
unchanged. No tool/Ability ID, CLI mapping, receipt format, config or environment
variable changed. Operators must correct extension defaults that violate their
own schemas or exceed the existing 64 KiB input budget.

Unused approval grants now count toward the same 100-entry budget as pending
prompts. Consumption frees capacity; expired entries are pruned before admission.
One-time consumption, five-minute expiration, human-event matching and automatic
approval rejection remain unchanged. Reviewed the actual pinned Hermes approval
transport, which emits human `choice` events without a required `decided_by` field;
no incompatible human-marker requirement was added.

## Performance, context and security

No speed, RSS, build-size or token savings are claimed or measured in this pass.
Validation after defaults adds necessary correctness work; requests without inserted
defaults skip that second validation. The shared size check uses the existing compact
UTF-8 encoding convention. Six native schema registrations and progressive
find/inspect/execute disclosure remain unchanged; no extra replay, retry or handoff
payloads are introduced. Detailed evidence remains in receipts and audit artifacts.

The measurable bounds are behavioral: input <=65536 encoded bytes before and after
normalization, preflight errors <=8192 characters, pending plus unused grants <=100.
Tests exercise each boundary. No source policy, secret access, workspace authority,
network permission or command capability is broadened. Redaction remains defense in
depth, not a guarantee that arbitrary user strings contain no sensitive content.

## Checklist coverage

| Phase | Evidence / disposition |
|---|---|
| 0: repository | Current Git state, catalog, approval, plugin registration and host approval transport read; existing service/process/config/command contracts from prior passes retained. |
| 1: baseline | 45 tests pass; seven failing regressions reproduced on archived starting source. |
| 2: complexity | One shared input-size function removes separate size-policy implementations; no broad refactor. |
| 3: runtime | Required post-default validation; no second validation if no defaults inserted. No speed claim. |
| 4: resources | N3/N5 close normalized-input and grant-count gaps; process, receipt and artifact bounds retained. |
| 5: AI context | Six schemas and deferred discovery remain; no automatic replay/retry; bounded preflight errors now match execution. |
| 6: output | N4 bounds approval errors; full valid result evidence stays in receipts. |
| 7: errors | Schema and size violations fail before permission prompts/commands; blocked approvals remain actionable. |
| 8: security | Input/default trust, preflight diagnostics and approval-capacity reviewed. Exact workspace and human-grant contracts preserved. |
| 9: state/concurrency | Combined approval count checked while holding the same lock used for grant transitions/consumption. No evicting valid grants silently. |
| 10: API | Required-input semantics, valid normalized digests and six-tool contracts preserved; invalid defaults intentionally rejected. |
| 11: dependencies | No changes to jsonschema range, vendored validator, source pins or CI runtime lock. No external CVE certification claimed. |
| 12: tests | Seven behavior regressions plus existing 45 tests; real canonical and host integration. |
| 13: CI | Existing unittest discovery is the regression gate; no timing threshold or new dependency gate. |
| 14: documentation | Normalization, size, approval capacity and diagnostic limits documented. Prior reports remain immutable historical evidence. |
| 15: agent ergonomics | Oversized input rejected before prompting; clear bounded errors; no added tools/instructions. |
| 16: dead weight | No proven unused functionality removed; concurrent media and handoff work preserved. |
| 17: fixes | N1–N5 implemented with regression tests and affected docs. |
| 18: verification | Full test suite, canonical workflows and native host checks below; no known introduced regression. |

## Verification receipt

`HPY=/Users/robertdevore/.hermes/hermes-agent/venv/bin/python3` (3.11.16).
Commands run from the repository root unless explicitly described as archive replay.

| Command | Result |
|---|---|
| `$HPY -m unittest discover -s tests -v` before edits | PASS, 45 tests |
| `$HPY -m unittest discover -s tests -p test_normalization.py -v` in starting archive with new tests | Expected FAIL, seven reproduced regressions |
| `$HPY -m unittest discover -s tests -v` after edits | PASS, 52 tests |
| `python3 scripts/real-tools.py --sources .. --kujo .local/runtime/kujo --output /tmp/hermes-pass3-real.json` | PASS, 45 canonical operations and receipt integrity |
| `PYTHONPATH=/tmp/kujo-hermes-host $HPY tests/hermes_e2e.py --sources .. --kujo .local/runtime/kujo --isolation host` | PASS, native loader/approval/workflow/receipt/failure/unload |
| `PYTHONPATH=/tmp/kujo-hermes-host $HPY tests/hermes_e2e.py --sources .. --kujo .local/runtime/kujo --isolation in_process` | PASS |
| `python3 -m build --sdist --outdir /tmp/hermes-pass3-dist` | PASS |
| `git diff --check -- kujo_hermes docs tests` | PASS |

The pinned Hermes v0.22.7 local host checks use deterministic test approval callbacks;
no live-model or human-consent certification is claimed. Canonical checks verify
product output fields and receipt hashes. Linux Python 3.14 remains a remote CI check.

## Remaining work

No new unresolved P0/P1/P2 finding and no cross-repository change required.
**Needs more evidence:** fresh CI for this revision and the pre-existing optional
browser/container/producer gateway certification gaps in `docs/readiness.md`.
**Not worth changing:** unrelated formatting, speculative caches, new schemas and
removal of documented release assets. All hardening files are committed separately;
concurrent handoff/demo edits remain outside this task's clean-tree claim.
SignalBox: no captures warranted; resolved findings and existing downstream
commitments do not warrant duplicate captures.
