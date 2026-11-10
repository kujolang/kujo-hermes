# Kujo Hermes

[![Version](https://img.shields.io/badge/version-0.1.0-black)](https://github.com/kujolang/kujo-hermes)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)
[![built with Kujo](https://img.shields.io/badge/built%20with-Kujo-white.svg)](https://github.com/kujolang/kujo)

Check Hermes's code changes against real requirements, find regressions, and keep the execution evidence. Kujo Hermes brings Spec, Eval, ShipCheck, PackWrite and other Kujo developer tools into Hermes through six native tools.

**A concrete example:** a coupon accidentally adds shipping to a customer's order. Kujo Eval reports the failing test; after the correction, the same tests pass. Both executions retain inspectable receipts. [Reproduce the checkout workflow](demo/checkout/README.md).

Kujo Hermes calls the official Kujo tools directly through its own native adapter. It requires no CommandCode, Kujo CMD, Pi or OpenCode installation or plugin.

**Status:** native workflows verified with Hermes 0.22.7 and 0.23.0 and real Kujo tools. Some operations still need external services, credentials, containers or additional bindings. See the [readiness report](docs/readiness.md) and [Ability inventory](docs/abilities.md) for tested operations and remaining gaps.

Watch the [73-second checkout showcase](demo/checkout-video/README.md): a free local model uses Kujo inside Hermes, corrects a regression, and reruns the same checks. Both receipts and the unchanged tests are independently verified. The film condenses recorded waits and includes a [480p mobile download](demo/checkout-video/delivery/kujo-hermes-checkout-480p.mp4). The [earlier tool overview](demo/square/README.md) remains available.

## Install

Requirements:

- Hermes **0.22.7+** and its supported Python runtime (3.14 for this release).
- macOS or Linux, with Git installed.
- An official Kujo runtime **>=1.6,<2**, installed separately. Tests used official 1.8.0, with partial checks on a 1.9.0 development build.

Some tools need additional dependencies. Hermes installs `jsonschema>=4.23,<5` when it installs the plugin.

With Hermes, Kujo and Git installed, run these commands from your repository:

```sh
hermes plugins install kujolang/kujo-hermes
hermes kujo setup --trust-workspace .
```

Accept Hermes's dependency-install and enable prompts. Setup fetches 26 official source repositories at verified commits, saves this Hermes profile's settings, and grants trust only to the repository you name. It selects the full catalog for a new configuration and preserves existing restrictions. No npm package is needed.

Start a new conversation, or restart a running gateway. Ask: “Run ShipCheck and show me the release-review findings.” Use `hermes kujo doctor` to inspect dependencies. Setup does not install the Kujo runtime, browser binaries, containers or service credentials; some Abilities still need those prerequisites.

Preview setup with `--dry-run`. Use `--kujo-bin /absolute/path/to/kujo`, `--sources /absolute/path/to/sources`, or `--profile review` to customize it. Omitting `--trust-workspace` adds no trust grant. Existing changed source checkouts are never overwritten.

The native CLI commands use Hermes's default `in_process` plugin mode. Profiles using `plugins.isolation: host` do not expose plugin CLI commands; use the manual configuration below without changing the isolation policy. Managed profiles require operator configuration.

Official release archives and package checks are documented in [release packaging](docs/releasing.md).

### Manual installation

To install a local checkout:

```sh
mkdir -p ~/.hermes/plugins
cp -R /path/to/kujo-hermes ~/.hermes/plugins/kujo-hermes
hermes plugins doctor ~/.hermes/plugins/kujo-hermes
```

Install the tool sources once, or use existing trusted checkouts. This helper fetches official repositories at exact commits and verifies each commit. It neither executes downloaded code nor replaces existing checkouts:

```sh
python3 ~/.hermes/plugins/kujo-hermes/scripts/install-sources.py \
  --destination ~/.local/share/kujo/hermes-sources
```

The helper installs source dependencies only. It does not update the plugin or download runtime or browser binaries. Install the runtime from [official Kujo](https://github.com/kujolang/kujo). Inspect the source lock before running setup. Use `--dry-run` or `--only shipcheck packwrite spec eval scout` for a smaller install.

Add settings under your active Hermes profile's `config.yaml` (replace every example path with an absolute path):

```yaml
plugins:
  entries:
    kujo-hermes:
      settings:
        ecosystem_root: /absolute/path/to/hermes-sources
        kujo_bin: /absolute/path/to/kujo
        trusted_workspaces:
          - /absolute/path/to/your/repository
        profile: full
```

```sh
hermes plugins enable kujo-hermes
hermes plugins doctor ~/.hermes/plugins/kujo-hermes
```

Restart Hermes after changing plugin settings, including its gateway if it is running. Start a new conversation and use `/kujo doctor` to check configuration and dependencies. Installation performs no repository work. An empty trust list allows discovery and diagnostics but denies execution.

## Usage

Ask Hermes:

- “Run ShipCheck and tell me what blocks release. Cite the receipt.”
- “Inspect this repository with Scout, then use PackWrite to summarize the execution pack.”
- “Validate the task specification, run Eval, and show the actual failed checks.”
- “Use Workcell to inspect this execution definition before running it.”
- “Run the Loop engineering workflow and verify its verdict.”
- “Show the receipts from the last workflow.”

Hermes exposes six native tools: `kujo_discover`, `kujo_inspect`, `kujo_execute`, `kujo_status`, `kujo_receipts`, and `kujo_doctor`. Descriptions and input schemas load only when selected. The bundled engineering skill explains discovery and evidence use.

`kujo_execute` returns execution status and a receipt reference. Successful command execution does **not** mean ShipCheck reports release readiness or Concord reports no drift. Inspect the structured product verdict. Retrieve large results from receipts in pages. Long operations support background execution and cancellation by invocation ID.

## Profiles

Profiles offer the same reference tool groups as Kujo CMD:

| Profile | Abilities | Coverage |
|---|---:|---|
| essentials (adapter default) | 5 | Catalog, receipts, Scout, PatchBrief, ShipCheck |
| review | 18 | Context, architecture, Spec, drift and artifact validation |
| ship | 29 | Eval, evidence capture, rendering and browser checks |
| full | 51 | All 38 reference capabilities plus Workcell, Loop, MCP and language tooling |

Profiles choose which Abilities appear; they do not grant permission to run them. Missing dependencies remain visible with installation guidance. Refresh loads new catalogs reviewed by the operator without adding more Hermes tools. See [configuration and extensions](docs/configuration.md).

## Security and disclosure

Kujo Hermes reads trusted repositories and configured canonical source checkouts outside plugin storage. It starts local tools with argument arrays, time and output limits, and an isolated HOME. Approved Eval, Loop, Muzzle, Dispatch and runtime operations may themselves execute repository commands. These tools are not sandboxed by this plugin; use Workcell when isolation is required.

Every operation that changes state or has external effects, and every extension, requires fresh human approval in Hermes. The adapter matches the approval to the exact request and accepts it once. Smart-model approval, YOLO, unattended auto-approve and an agent-supplied boolean do not create that grant. Downstream Kujo restrictions remain active. The plugin reports any denial from the underlying tool.

No automatic telemetry, background discovery, external MCP configuration, runtime downloads or plugin self-updates. Explicit Watchdog operations use loopback HTTP. Networked canonical tools can contact their configured providers only when invoked and approved. Credentials come from configured Hermes secret-scope variables; the plugin never reads provider credential stores. Receipts are local, redacted, hash-checked records, not signed attestations. See [security](SECURITY.md).

## Development and verification

```sh
python3 -m pip install -e .
python3 -m unittest discover -s tests -v
python3 scripts/real-tools.py --sources /path/to/kujo-sources --kujo /path/to/kujo
PYTHONPATH=/path/to/hermes-agent python3 tests/hermes_e2e.py \
  --sources /path/to/kujo-sources --kujo /path/to/kujo --isolation host
hermes plugins validate . --install-deps
```

The Hermes script uses the actual loader, tool registry, approval gate and canonical binaries. Automated tests supply approval decisions through a test-only callback, which the evidence identifies. Use `--interactive` to answer prompts yourself. A separate live-model test verifies a real Hermes conversation. See [testing](docs/testing.md), [architecture](docs/architecture.md), [parity](docs/parity.md), [compatibility](docs/compatibility.md), and the [demo](demo/script.md).

Updates use Hermes's normal plugin update mechanism. Disable/unload cancels owned work and unregisters tools/hooks. Receipts survive updates in the active Hermes profile's plugin data directory. The operator decides when to delete them.
