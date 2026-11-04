# Kujo Hermes

Native Hermes tools for Kujo's engineering ecosystem: repository intelligence, context packs, specifications, verification, orchestration and execution evidence. Works on repositories in the languages supported by each underlying tool; Kujo language development is one part of the integration.

Kujo Hermes owns its Hermes adapter and calls canonical Kujo tools directly. It does **not** install, import or require CommandCode, Kujo CMD, Pi, OpenCode, or their plugins.

**Status:** working integration with real Hermes and canonical-tool evidence. Some ecosystem operations still require external services, credentials or container infrastructure. See the [readiness report](docs/readiness.md) and [per-Ability inventory](docs/abilities.md); complete ecosystem certification is not claimed.

## Install

Requirements: Hermes **0.22.7+**, Python 3.11+, macOS or Linux, Git, and a separately installed official Kujo runtime **>=1.6,<2** (tested with official 1.8.0; partial checks with a 1.9.0 development build). Some products have additional requirements. Hermes installs the bounded `jsonschema>=4.23,<5` Python dependency through its plugin mechanism.

```sh
hermes plugins install https://github.com/kujolang/kujo-hermes --no-enable
```

For a local checkout, use the documented directory installation:

```sh
mkdir -p ~/.hermes/plugins
cp -R /path/to/kujo-hermes ~/.hermes/plugins/kujo-hermes
hermes plugins doctor ~/.hermes/plugins/kujo-hermes
```

Install canonical sources once, or point at existing trusted checkouts. This explicit helper fetches official repositories at full commit pins, verifies the commit, and never executes downloaded code or replaces an existing checkout:

```sh
python3 ~/.hermes/plugins/kujo-hermes/scripts/install-sources.py \
  --destination ~/.local/share/kujo/hermes-sources
```

The helper is source dependency setup, not a plugin updater. It does not download a runtime or browser binaries. Install the runtime from [official Kujo](https://github.com/kujolang/kujo). Inspect the source lock before running setup. Use `--dry-run` or `--only shipcheck packwrite spec eval scout` for a smaller install.

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

Start a new Hermes conversation. Use `/kujo doctor` to check configuration and dependencies. Installation performs no repository work. An empty trust list allows discovery and diagnostics but denies execution.

## Usage

Ask Hermes:

- “Run ShipCheck and tell me what blocks release. Cite the receipt.”
- “Inspect this repository with Scout, then use PackWrite to summarize the execution pack.”
- “Validate the task specification, run Eval, and show the actual failed checks.”
- “Use Workcell to inspect this execution definition before running it.”
- “Run the Loop engineering workflow and verify its verdict.”
- “Show the receipts from the last workflow.”

Six native tools keep the model surface small: `kujo_discover`, `kujo_inspect`, `kujo_execute`, `kujo_status`, `kujo_receipts`, and `kujo_doctor`. Descriptions and input schemas load only when selected. The bundled engineering skill explains discovery and evidence use.

`kujo_execute` returns execution status and a receipt reference. Successful command execution does **not** mean ShipCheck reports release readiness or Concord reports no drift. Inspect the structured product verdict. Large results stay in receipts and can be retrieved in bounded pages. Long operations support background execution and cancellation by invocation ID.

## Profiles

Profiles preserve Kujo CMD exposure semantics without depending on its implementation:

| Profile | Abilities | Coverage |
|---|---:|---|
| essentials (default) | 5 | Catalog, receipts, Scout, PatchBrief, ShipCheck |
| review | 18 | Context, architecture, Spec, drift and artifact validation |
| ship | 29 | Eval, evidence capture, rendering and browser checks |
| full | 51 | All 38 reference capabilities plus Workcell, Loop, MCP and language tooling |

Profiles only control exposure. They never authorize execution. Missing dependencies stay visible with an actionable installation explanation. New operator-reviewed catalogs are loaded on refresh, without adding more Hermes tools. See [configuration and extensions](docs/configuration.md).

## Security and disclosure

Kujo Hermes reads trusted repositories and configured canonical source checkouts outside plugin storage. It starts local canonical processes with argument arrays, bounded time/output, and an isolated HOME. Approved Eval, Loop, Muzzle, Dispatch and runtime operations may themselves execute repository commands. These tools are not sandboxed by this plugin; use Workcell when isolation is required.

Every mutating/external operation and every extension requires a matching, fresh human Hermes approval. The adapter observes native approval events and consumes a request-bound grant once. Smart-model approval, YOLO, unattended auto-approve and an agent-supplied boolean do not create that grant. Downstream Kujo restrictions remain active. A denied downstream approval is reported, not bypassed.

No automatic telemetry, background discovery, external MCP configuration, runtime downloads or plugin self-updates. Explicit Watchdog operations use loopback HTTP. Networked canonical tools can contact their configured providers only when invoked and approved. Credentials come through explicitly named Hermes secret-scope variables; the plugin never reads provider credential stores. Receipts are local, redacted, hash-checked records, not signed attestations. See [security](SECURITY.md).

## Development and verification

```sh
python3 -m pip install -e .
python3 -m unittest discover -s tests -v
python3 scripts/real-tools.py --sources /path/to/kujo-sources --kujo /path/to/kujo
PYTHONPATH=/path/to/hermes-agent python3 tests/hermes_e2e.py \
  --sources /path/to/kujo-sources --kujo /path/to/kujo --isolation host
hermes plugins validate . --install-deps
```

The Hermes script uses the actual loader, tool registry, approval gate and canonical binaries. Its deterministic human-decision callback is test-only, is not installed, and is explicitly identified in evidence. `--interactive` lets an operator supply decisions. It is not a fabricated LLM conversation. See [testing](docs/testing.md), [architecture](docs/architecture.md), [parity](docs/parity.md), [compatibility](docs/compatibility.md), and the [demo](demo/script.md).

Updates use Hermes's normal plugin update mechanism. Disable/unload cancels owned work and unregisters tools/hooks. Receipts survive updates in Hermes's profile-scoped plugin data directory. Retention and deletion are operator-owned.
