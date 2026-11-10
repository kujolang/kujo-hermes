# Add Kujo Hermes to the plugin catalog

Kujo Hermes gives Hermes native discovery, inspection and execution of Kujo engineering tools, including ShipCheck, PackWrite, Spec, Eval, Scout and Loop, with structured results and integrity-checked receipts. It owns its Hermes adapter and has no dependency on other agent-specific Kujo integrations.

The included checkout reproduction validates a task contract, records a real failed Eval (2 passed / 1 failed), applies a disclosed one-line fixture correction, then records the same tests passing (3 / 0). A standard-library verifier checks saved receipt and artifact hashes. This deterministic driver is not presented as an autonomous model run.

The plugin registers six tools, `pre_tool_call` and `post_approval_response` hooks, `/kujo`, a bundled engineering skill and unload cleanup. No core overrides. The entry pins the exact validated source commit. Native setup is available through `hermes kujo`; the plugin adds no Desktop dashboard.

Disclosures:

- Reads operator-trusted repositories and canonical source checkouts outside plugin data.
- Starts local CLI processes. Eval, Loop, Muzzle and other approved operations may execute repository-defined commands. Ordinary CLI execution is not sandboxed; Workcell supplies optional container isolation.
- Explicit source setup fetches only official repositories at full commit pins. It does not update the plugin or execute downloaded code.
- No telemetry on load. Explicit Watchdog calls contact loopback. Explicit provider operations can make network calls through the canonical tool.
- Secret values come only from explicitly configured Hermes secret scope; no vendor credential stores or OAuth refresh.
- Opt-in background operations have timeout, cancellation and unload cleanup. No persistent service starts automatically.
- Local receipts are redacted SHA-256 records, not signed attestations. Operators manage retention.

Catalog candidate (release runtime plus corrected installation docs): `4f7b27ef0216cf6284af42fb23f5211a22befd0b`. Release-runtime CI https://github.com/kujolang/kujo-hermes/actions/runs/42742232654 passed on Hermes 0.22.7 and 0.23.0, including clean install and the native checkout correction workflow.

Validation and evidence:

- [Exact candidate CI](https://github.com/kujolang/kujo-hermes/actions/runs/42743837185): all three jobs passed, including unit/package checks and real Hermes 0.22.7/0.23.0 clean installation, Doctor, `plugins validate --install-deps`, canonical operations and checkout correction.
- [Readiness and limitations](https://github.com/kujolang/kujo-hermes/blob/4f7b27ef0216cf6284af42fb23f5211a22befd0b/docs/readiness.md): browser/container prerequisites, producer gateways, Foreman discovery and untested deployments/platforms.
- [Download the 73.2-second 1080p square demo](https://raw.githubusercontent.com/kujolang/kujo-hermes/a617957bb244604f4d536152038c6cd8263effaa/demo/checkout-video/delivery/kujo-hermes-checkout.mp4).
- [Recording provenance and verification](https://github.com/kujolang/kujo-hermes/tree/a617957bb244604f4d536152038c6cd8263effaa/demo/checkout-video).

The validator warns about private Hermes imports in standalone demo drivers, which use the real loader, registry and approval transport for reproduction. They are not imported by plugin registration. The native setup writer also depends on Hermes configuration helpers; current-host execution and the compatibility floor are tested separately. Dependency-preparation errors, if any, must be disclosed even when the validation report passes.

The accompanying 73.2-second square film uses a real Qwen3.5 4B conversation through Hermes. The model makes the code correction; source timings, approval decisions, unchanged tests and independently verified receipts are retained. Installation footage reuses the successful earlier native recording; the official release and catalog candidate have separate clean-install CI evidence. Failed fresh local captures are retained and not shown as successful.

Release: https://github.com/kujolang/kujo-hermes/releases/tag/v0.1.0

