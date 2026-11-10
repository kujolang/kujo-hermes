# Release hardening — November 9, 2026

Scope: `kujolang/kujo-hermes`, `main`, starting at `75d3f6a51e002340f096983ee37a4a83f5b74c00`, with a clean working tree. Runtime fixes are in `39463e6`; release packaging is in `ac9e7ed`. Earlier audit reports and video evidence remain unchanged. This pass uses the Kujo Hardening checklist in fix mode, with PackWrite validation and a bounded Loop run. No other repository was modified.

## Findings and corrections

| ID | Priority | Evidence and impact | Correction and status |
|---|---|---|---|
| R1 | P0: broken package contract | Baseline wheel imports failed with `FileNotFoundError` for `catalog/abilities.json` outside the checkout. Catalogs, Skill and setup installer were absent. | Bundle runtime resources in wheels; use one resource root across discovery, Skill registration and setup. A real pip installation outside the checkout discovers 51 Abilities. Fixed, high confidence. |
| R2 | P0: confidentiality | `redact({'private-token-value':'result'}, ['private-token-value'])` exposed the synthetic secret as a JSON key. The same structure could reach model output and a receipt. | Redact keys and preserve colliding values with suffixes. Regression tests run a child process with a configured secret, verify response and persisted receipt, test collision preservation and idempotence. Fixed, high confidence. |
| R3 | P1: release regression coverage | CI tested editable installs only; no compact native release artifact or installed-package gate existed. | Add wheel installation and native archive gates. Ship sorted, fixed-timestamp ZIP plus SHA-256 checksums; omit development recordings. Fixed, high confidence. |

P0 is the hardening checklist category, not a CVSS severity. R2 requires a configured secret to appear in a tool's JSON key; no real credential exposure was observed during this audit.

## Checklist coverage

| Phase | Review and evidence |
|---|---|
| 0: repository | Read runtime modules, schemas/catalogs, setup/installer, six native tools, hooks, tests, fixtures, CI, documentation and Skill. The adapter delegates functionality to canonical Kujo sources. |
| 1: baseline | 61 tests pass on supported Python 3.14.9; wheel and sdist build. Isolated wheel smoke fails as recorded. Python 3.10 also passed but is outside the supported package range. |
| 2: complexity | Preserved existing module boundaries. Centralized the three resource-location assumptions; removed the resulting unused import. No speculative architecture rewrite. |
| 3: performance | Measured 20-run startup, discovery and inspection before/after. No runtime speed improvement claimed; figures below. |
| 4: resources | Reviewed four-job bound, process-group cleanup, timeout/cancellation, catalog/input/output bounds, receipt limits and thread failure handling. Existing negative tests pass. Receipt retention remains operator-owned. |
| 5: agent context | Six compact native schemas; catalog and operation schemas load on demand. Skill separates execution success from verification verdicts. No conversation replay or automatic retries introduced. |
| 6: output | Bounded inline results and paged receipts remain intact. Evidence is retained rather than silently discarded. R2 closes key leakage without losing colliding values. |
| 7: errors | Existing tests cover missing sources, invalid input, crashes, output validation, oversized/deep output, storage failure and cleanup. Real host test includes denied and failed operations. |
| 8: security | Reviewed exact-root trust, containment, operator-only catalogs/configuration, argv execution, controlled environment, redaction, local-only telemetry and receipt symlink protection. R2 fixed. Trusted canonical tools are not sandboxed. |
| 9: concurrency/state | Single-use request-bound approval, bounded pending/grant state, atomic non-replacing receipt writes and owned child cleanup preserved. No retry/replay semantics changed. |
| 10: contracts | No native tool names, input schemas, configuration keys, CLI commands, environment keys or receipt version changed. Secret-bearing result keys now redact; colliding keys receive numeric suffixes. |
| 11: dependencies | Runtime dependency remains `jsonschema>=4.23,<5`; setuptools build dependency remains bounded. No new production dependency. Exact canonical source lock and upstream SDK provenance retained. No claim of an exhaustive external vulnerability-database audit. |
| 12: tests | Three new regressions bring the suite to 64. Installed-wheel and deterministic native-archive checks cover distribution behavior, not editable imports alone. |
| 13: CI | Python 3.11 unit/package job and real Hermes 0.22.7/0.23.0 jobs retained. New archive gate enforces a documented, reviewable 1 MiB budget. No timing threshold added. |
| 14: docs | Updated install command to pin the official release, described archive/wheel differences and build checks. Existing limitations and monochrome badges preserved. |
| 15: developer experience | Compact Skill, diagnostics, source-lock setup and concrete test commands remain authoritative. Release checks provide a short success receipt and fail on missing resources. |
| 16: dead weight | Videos and prior evidence are linked public deliverables, not proven dead files. Preserve them in Git; exclude them from the native runtime archive. |
| 17: fixes | Implemented R1–R3 only. No host-plugin dependency, new adapter or unrelated cleanup. |
| 18: final verification | Unit, build, installed-wheel, native archive, real host modes, checkout failure/correction, PackWrite and Loop evidence retained alongside this report. Release admission and CI results are recorded below. |

## Measurements and compatibility

Same machine and Python 3.10 measurement script, 20 samples per run (diagnostic measurements, not support certification): initialization median 0.267 → 0.280 ms; cold discovery 166.940 → 184.914 ms; inspection 0.312 → 0.313 ms. Native tool schema bytes remain 2,820; full discovery response remains 14,700 bytes. Token counts were not measured. Shared-machine load and dependency resolution were active during the final run. These samples do not establish an optimization or a causal performance regression; discovery algorithms were unchanged.

The baseline wheel was 25,798 bytes and omitted required resources. The corrected wheel is larger because it includes them. The native ZIP is under 1 MiB and excludes approximately 315 MiB of demo assets present in the development checkout. Exact release sizes and SHA-256 digests are in the published assets; this is an archive-size improvement, not a Git clone speed claim.

Python package support stays at >=3.11. Local tests used Python 3.11.16 and Hermes's 3.14.9 environment. Real canonical operations used official Kujo 1.8.0 and the pinned source checkouts. No upstream change or migration is required. Ordinary receipts remain local integrity evidence, not signed attestations; the plugin does not enforce a universal commit/release gate.

## Verification receipt

Evidence directory: [release-20261109](evidence/release-20261109/). Paths beginning `.local/hardening-20261109` are ignored local build state.

- Baseline: Hermes Python 3.14.9 `-m unittest discover -s tests`: 61 pass. Final: Python 3.11.16 and 3.14.9, same command: 64 pass.
- `python3 -m build --outdir .local/hardening-20261109/dist`: wheel and sdist built; the wheel was built from the sdist by the build frontend.
- `.local/hardening-20261109/venv/bin/python scripts/check-wheel.py .local/hardening-20261109/dist/kujo_hermes-0.1.0-py3-none-any.whl`: installed wheel passes outside checkout. The first local attempt lacked pip in Hermes's interpreter; a clean Python 3.11 virtual environment supplied the build-check dependencies. An initial temporary-path comparison was corrected to resolve macOS `/var` symlinks.
- `python3.11 scripts/package-release.py --output .local/hardening-20261109/dist` followed by the clean-venv `scripts/check-release.py` on the native ZIP: safe layout, 51 Abilities, size bound and byte-identical repeated packaging pass.
- `PYTHONPATH=.local/hackathon/hermes HERMES_PYTHON tests/hermes_e2e.py --sources .local/square/sources --kujo .local/runtime/kujo --isolation host --output .local/hardening-20261109/hermes-e2e.json`: passes; repeat with `in_process` passes. `HERMES_PYTHON` here denotes the supported 3.14.9 executable, not an environment variable consumed by the plugin. Actual discovery, denial, approval, Scout, PackWrite, Spec, Eval, ShipCheck, Loop, receipts, failure and unload verified. Approval decisions come from an explicit test callback, not a live user/model session.
- Same Hermes Python/source environment, `demo/checkout/run.py --sources .local/square/sources --kujo .local/runtime/kujo --output .local/hardening-20261109/checkout --test-decisions`: 2 pass/1 fail before correction, 3 pass/0 fail after, unchanged tests, independently checked receipt hashes, clean unload.
- `KUJO="$PWD/.local/runtime/kujo" ../packwrite/bin/packwrite validate`: zero warnings. `../kujo-workflows/loop-engineering/scripts/run-workflow.sh --config .local/hardening-20261109/loop/loop.yml`: success, four required gates pass, no external blocker.
- `hermes plugins doctor` against the extracted native ZIP: six tools/two hooks, pass. Running Doctor on the full development directory first exhausted local disk during a temporary copy; the native artifact avoided that unrelated source-tree footprint. No permission check was disabled.
- `git diff --check`: pass.

## Remaining limits

No unresolved P0/P1 defect was established in the plugin by this pass. P2 hypotheses such as indexing very large receipt histories need representative measurements before adding state or caches. P3 cosmetic rewrites were not pursued. External-service/provider/container operations are not newly certified; the operation inventory and prior evidence remain the authority. Windows is not supported by the POSIX process implementation. No live-model narration/video was regenerated by this hardening pass.

Official Hermes 0.23.0 `plugins validate EXTRACTED_PLUGIN --install-deps` passed in an isolated profile: manifest, dependency installation, capability probe, declared tools/hooks, collision checks, security scan and core-override checks. Host isolation correctly skips plugin CLI commands; native tools remain available. The initial full-tree validation was stopped after the disk-space failure; the archive validation completed without bypasses.
