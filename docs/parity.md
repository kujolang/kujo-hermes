# Kujo CMD parity and host-specific differences

Reference: Kujo CMD 0.3.1 at `7dedc530ea004c414c561325f91d63f6c4925ee9`. All 38 reference IDs have Hermes bindings. See [per-operation evidence](abilities.md), [schemas/dependencies](ability-inventory.json), and [source provenance](provenance.json). A binding may exist without passing a real execution test.

| Reference feature | Hermes implementation | Evidence / limit |
|---|---|---|
| Discovery and registration | Six native tools; lazy bounded catalog | Real host loader and discovery |
| Input schemas | On-demand inspection, JSON Schema validation | Unit and real invalid Spec |
| Output normalization | Structured JSON once; labeled text fallback | Real tool evidence |
| Essentials/Review/Ship/Full | Same 5/18/29/38 reference sets; Full adds thirteen operations | Profile count tests |
| Workspace context | Explicit exact operator-trusted roots | Escape and untrusted-root tests |
| Permissions | Native pre-tool approval plus single-use event-backed request grant | Real denial/approval in host and in-process modes |
| Downstream Kujo permissions | Canonical restrictions remain in force | Dispatch receives no `--yes`; Muzzle cannot accept agent network bypass |
| Timeouts/cancellation | POSIX group kill; bounded output; four active jobs | Negative tests |
| Receipts | Explicit Hermes receipt schema, input/definition/argv identity and SHA-256 | Integrity/tamper tests and real retrieval |
| Canonical receipt replay | Not emulated | Product-owned receipt/replay remains authoritative; no shared global CLI replay service |
| Run/model/session correlation | Invocation/receipt identity, workspace and command | Model identity not fabricated; advanced host telemetry correlation deferred |
| Dependencies/onboarding | Pinned official source fetch helper, Hermes Python deps, explicit runtime | No binary auto-install; no other plugin dependencies |
| Doctor | Runtime, source availability, profile and trust | Native `/kujo doctor` |
| Version compatibility | Runtime range, exact source lock, Hermes floor | Tested revisions in evidence |
| Lazy context | Compact tool schemas, paged catalog/receipts | Performance measurement script |
| Mod/slash command | Native `/kujo`, bundled engineering skill | Real Hermes registration |
| Lifecycle | No implicit services; explicit jobs; on-unload cleanup | Real host unload |
| Watchdog | Explicit loopback health/metadata operations | No CMD mod telemetry lifecycle copied |
| Browser management | Canonical Lens setup remains operator-owned | No hidden Chromium installation |
| Upgrades/uninstall | Hermes plugin management; preserve durable data | No self-updater or destructive purge tool |
| Release packaging | Native manifest, source archive, submission draft | Catalog validation; no external submission |

## Broader catalog research

The canonical Ability package owns contracts, digests, profiles and the execution runtime. It explicitly does not ship a global production catalog. Its devkit provides test fixtures, not production execution. Current MCP launch metadata names CMS (6 operations), SSG (10) and MCP core (2); these producers expose application/library-specific bindings. The repository-review pack is a canonical library, not a universal command executable.

The [organization inventory](ecosystem-inventory.json) covers every repository returned by the organization listing, its checked-out interfaces, and every tracked non-fixture JSON Ability definition found under primary available checkouts. Repeated definitions retain their source attribution and do not count as unique operations. The inventory distinguishes SDKs, provider libraries and websites from developer CLIs.

CMS/SSG/MCP producer execution is not auto-enabled by scanning definitions. No authenticated application gateway was configured, and a portable definition alone supplies no executable implementation or permissions. These operations need an explicit operator-reviewed binding or future tested gateway adapter. These producer operations remain a coverage gap in Kujo Hermes.

Workcell, Loop and runtime execution are additional direct integrations. Kujo Foreman was not present as a repository or verified executable in the current organization inventory or inspected workflows; the plugin therefore exposes no `foreman` command. Agency Runner/Relay and other new applications are recorded in the organization inventory but have no execution bindings. Supporting them requires verified bindings and execution tests.
