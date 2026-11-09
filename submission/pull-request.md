# Add Kujo Hermes to the plugin catalog

Kujo Hermes gives Hermes native discovery, inspection and execution of Kujo engineering tools, including ShipCheck, PackWrite, Spec, Eval, Scout and Loop, with structured results and integrity-checked receipts. It owns its Hermes adapter and has no dependency on other agent-specific Kujo integrations.

The included checkout reproduction validates a task contract, records a real failed Eval (2 passed / 1 failed), applies a disclosed one-line fixture correction, then records the same tests passing (3 / 0). A standard-library verifier checks saved receipt and artifact hashes. This deterministic driver is not presented as an autonomous model run.

The plugin registers six tools, `pre_tool_call` and `post_approval_response` hooks, `/kujo`, a bundled engineering skill and unload cleanup. No core overrides. The catalog pin must identify the exact validated source commit.

Disclosures:

- Reads operator-trusted repositories and canonical source checkouts outside plugin data.
- Starts local CLI processes. Eval, Loop, Muzzle and other approved operations may execute repository-defined commands. Ordinary CLI execution is not sandboxed; Workcell supplies optional container isolation.
- Explicit source setup fetches only official repositories at full commit pins. It does not update the plugin or execute downloaded code.
- No telemetry on load. Explicit Watchdog calls contact loopback. Explicit provider operations can make network calls through the canonical tool.
- Secret values come only from explicitly configured Hermes secret scope; no vendor credential stores or OAuth refresh.
- Opt-in background operations have timeout, cancellation and unload cleanup. No persistent service starts automatically.
- Local receipts are redacted SHA-256 records, not signed attestations. Operators manage retention.

Tested candidate: `6f847b98aae1260b22bff9579b341f0e11225af6`. CI https://github.com/kujolang/kujo-hermes/actions/runs/42637870905 passed on Hermes 0.22.7 and 0.23.0, including clean install and the native checkout correction workflow.

Validation: attach the checked commit's `hermes plugins validate --install-deps`, real host E2E, canonical integration results and readiness report. Report any dependency-network failure separately from manifest validation.

See docs/readiness.md for remaining gaps: browser and container prerequisites, producer gateways, Foreman discovery and untested deployments or platforms. This tool-only integration does not add a Desktop dashboard. Attach the matching real workflow demo.

The validator warns about private Hermes imports in standalone demo drivers, which use the real loader, registry and approval transport for reproduction. They are not imported by plugin registration. The native setup writer also depends on Hermes configuration helpers; current-host execution and the compatibility floor are tested separately. Dependency-preparation errors, if any, must be disclosed even when the validation report passes.
