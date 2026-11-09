# Plugin audit — November 9, 2026

## Verdict

The integration has the technical foundation it needs. Its strongest feature is the combination of native, request-bound approval and persistent execution evidence across canonical engineering tools. The major presentation gap is that the existing video shows already-completed passing evidence, not a consequential mistake being found and corrected.

This audit preserved the architecture. Changes clarify model-facing semantics, add a reproducible checkout regression workflow, test the current Hermes release, improve the README opening and prepare the submission. It adds no new runtime dependency or production execution tool.

## Scope and evidence

Reviewed the native entrypoint, all adapter modules, vendored Ability helpers, catalog/profiles/source lock, setup installer, engineering skill, manifest/package metadata, CI and unit/host tests. Cross-checked architecture, parity, compatibility, readiness and inventory documents. Historical 45-operation evidence is prior work, not a new certification of all 51 bindings. Current evidence lives in [evidence/](evidence/); the [verification ledger](evidence/VERIFICATION.md) distinguishes current runs, historical evidence and blockers.

The 88-second square film was decoded and its actual frames inspected at 1.6, 14, 24, 48, 76 and 85 seconds. See [contact sheet](evidence/current-demo-frames.jpg). The source storyboard, shot map and provenance disclosures were also read. This was a frame/timing audit, not a fresh full audio audition. Competitor source/claim limitations are in [competitive analysis](COMPETITIVE-ANALYSIS.md).

## What is implemented

| Area | Actual behavior | Important boundary |
|---|---|---|
| Native integration | Six native tools, two approval hooks, slash command, operator CLI, skill, unload callback | No separate Desktop dashboard; Desktop footage uses native Markdown views. |
| Discovery | Lazy bundled catalog, four exposure profiles, on-demand schemas and reviewed extension catalogs | 51 bindings are not 51 certified deployments. Newly installed arbitrary binaries are not automatically adapted. |
| Canonical routing | Direct argv/API calls into Kujo sources; full 38-ID reference CMD surface plus 13 bindings | No CMD or CommandCode dependency. Some producer catalogs lack execution bindings. |
| Inputs | JSON Schema validation, defaults revalidated, bounded inputs/catalogs, no remote schema references | Underlying tools retain their own validation and permissions. |
| Workspace policy | Exact operator-trusted roots; contained path checks; operator-only configuration | Not an OS sandbox. Approved Eval/Loop can run repository-defined code. |
| Approval | Preflight identity binds schema/input/argv/workspace to short-lived, single-use observed approval | Hooks gate `kujo_execute`, not all Hermes tool calls or `git push`. Aux-model approval cannot mint a human grant. |
| Processes | Bounded output, timeout, cancellation, POSIX process-group cleanup; four active jobs | Windows unsupported. Optional Docker/browser/service requirements remain external. |
| Results | Canonical JSON retained; text fallback; large payloads referenced via receipts | `ok` reports command execution, not every semantic check. ShipCheck may complete while findings remain. |
| Receipts | Redacted, atomic JSON, hashes, request identity and bounded artifact inventory; paged retrieval | Hash is not a signature; retrieval verifies stored receipt content, not current artifact files. No automatic Git HEAD binding. |
| Onboarding | Native install then `hermes kujo setup`; 26 pinned source checkouts; exact-root trust | Official Kujo runtime installed separately. Source setup is operator action. Host isolation skips plugin CLI registration. |
| Diagnostics | Runtime compatibility, source presence, profile, trust and receipt directory | Source presence does not prove browser/container/service readiness. Doctor `ok` is not a universal tool certification. |
| Lifecycle | No service starts on load; opt-in jobs canceled at unload; durable receipts retained | Operator manages retention. No automatic Watchdog collection. |

## Fully working versus conditional

Current native 0.23.0 execution exercised discovery, denial, approved Scout, PackWrite summary, Spec validation, Eval, ShipCheck, Loop, receipt retrieval, failed Spec and unload. The separate checkout fixture exercised a real failing Eval and a corrected passing Eval twice. PackWrite summary is a seeded pack operation, not provider generation; previous provider generation evidence is separate. The fixture needs no model or service.

Workcell bindings require an OCI daemon/image; Lens requires matching browser dependencies; provider operations require scoped credentials; Watchdog requires its configured loopback service. Tribunal's routed mock review must remain labeled mock. CMS/SSG/MCP producer gateways and Foreman are not silently supported. See [inventory](../abilities.md), [parity](../parity.md) and [readiness](../readiness.md) for exact earlier blockers.

Automatic behavior is limited to native registration, lazy discovery, approval enforcement on Kujo calls, receipt persistence and cleanup. Hermes must select the tools; the skill guides selection. There is no automatic “verify every edit,” cross-session policy learning, autonomous rollback or global release gate. Source installation and workspace trust require operator commands.

## Failure and agent experience

Failures retain status, type, bounded diagnostic text and canonical output where available. Timeout/output-limit/cancellation are distinct outcomes. Storage failures report `receipt_persisted: false`. Approval denial stops execution. The model should explain a failed check, make a scoped correction and rerun unchanged checks; it should not treat a receipt as a correctness proof or repeat a denied action.

The previous compact descriptions left this distinction too implicit. They now state command-success and receipt-integrity limits, and the skill describes before/after evidence and unchanged-test discipline. This is guidance plus the existing execution controls, not new enforcement of model reasoning.

## Independent verification

The checkout run preserves both receipts, original and corrected source snapshots, unchanged tests and canonical Eval artifacts. `python3 demo/checkout/verify.py docs/hackathon/evidence` independently checks SHA-256 using only the standard library and compares recorded artifact files. The failure receipt shows `5099 != 4500`; the second run passes all three tests. This is reproducible evidence, not proof against an attacker who can replace the receipt and its checksum together.

Receipt inventories can include existing `.bak` artifacts. Their presence proves which bytes were inventoried, not that every listed file was created by that invocation. Source dependencies are pinned during setup but are operator-controlled afterward. Stronger source-state binding, signatures and a richer history interface are useful post-hackathon work; none should be implied today.

## Current film audit

The full screen fits, monochrome branding is consistent and installation instructions are practical. But its first specific tool scene starts around 20 seconds, after logos, an abstract opening and installation. The sample calculator is already correct. Eval's two passing checks and the receipt appear as completed Markdown evidence views, not a visible debugging episode. Smaller interface text is difficult on the 480-square export even though large headings remain readable.

The edit presents eight tool concepts instead of one completed outcome. A judge may remember a tool collection, while remembering Chronos as “undo the damage” and Night Shift as “fix the incident and learn.” The new storyboard puts a $5.99 customer overcharge in the opening, shows the actual failed assertion by 29 seconds, and follows the correction with the same checks and both receipts. No new dashboard is needed.

## Submission risks

The old catalog candidate pinned a commit predating current setup and hardening. It must pin the reviewed implementation commit, not a branch or an earlier film commit. Official validation warns about private Hermes imports in demonstration drivers; these are test harness entrypoints, not plugin registration code. Disclose them rather than hiding the warning. Fresh dependency setup and host validation results must be read beyond the process exit status: Hermes can print “Validation passed” after dependency preparation fails. Keep those outcomes separate.

The current submission is promising but not yet an evidence-based first-place choice. Its technical breadth is real, but its best developer story was absent from the delivered film. The new fixture supplies that story honestly; a real model-driven recording remains the next presentation step.
