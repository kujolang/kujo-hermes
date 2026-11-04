# Add Kujo Hermes to the plugin catalog

Kujo Hermes gives Hermes native discovery, inspection and execution of Kujo engineering tools, including ShipCheck, PackWrite, Spec, Eval, Scout and Loop, with structured results and integrity-checked receipts. It owns its Hermes adapter and has no dependency on other agent-specific Kujo integrations.

The plugin registers six tools, `pre_tool_call` and `post_approval_response` hooks, `/kujo`, a bundled engineering skill and unload cleanup. No core overrides. The catalog pin must identify the exact validated source commit.

Disclosures:

- Reads operator-trusted repositories and canonical source checkouts outside plugin data.
- Starts local CLI processes. Eval, Loop, Muzzle and other approved operations may execute repository-defined commands. Ordinary CLI execution is not sandboxed; Workcell supplies optional container isolation.
- Explicit source setup fetches only official repositories at full commit pins. It does not update the plugin or execute downloaded code.
- No telemetry on load. Explicit Watchdog calls contact loopback. Explicit provider operations can make network calls through the canonical tool.
- Secret values come only from explicitly configured Hermes secret scope; no vendor credential stores or OAuth refresh.
- Opt-in background operations have timeout, cancellation and unload cleanup. No persistent service starts automatically.
- Local receipts are redacted SHA-256 records, not signed attestations. Operators manage retention.

Validation: attach the checked commit's `hermes plugins validate --install-deps`, real host E2E, canonical integration results and readiness report. Report any dependency-network failure separately from manifest validation.

See docs/readiness.md for remaining gaps: browser and container prerequisites, producer gateways, Foreman discovery and untested deployments or platforms. No UI screenshots are required for this tool-only integration; attach the real demo if useful.
