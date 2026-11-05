# Compatibility and security notes

Verified host: official Hermes tag `v0.22.7`, commit `b200f5bc60e31588ba2cb60e288029c4a54ba5fa`. The release's package metadata reports development version `0.0.0`, so the plugin's minimum version follows the released SemVer tag.

The adapter uses public native registration, approval-observer hooks and unload callbacks. Tests exercise both `plugins.isolation: in_process` and the default `host` process. The public-surface catalog check passes; the adapter uses no undocumented `request_tool_approval` import. Operations that change state require an observed human approval event. Automatic approval alone cannot authorize them. Gateway interactive prompting is not certified here.

Kujo runtime range: >=1.6,<2. Exact tool-source commits are in `catalog/sources.lock.json`. Runtime builds can omit optional features: the local 1.9.0 development build lacks `runtime-db`, so it cannot run Watchdog's SQLite service. A version number does not show which optional features were compiled in. Tool errors retain their exact diagnostics. The official host-independent 1.8.0 runtime binary was also tested; its SHA-256 is `979d49503d71eb87e5696aea844a51e7129e23c89e36abc8e4d4378bc78985b5` (Darwin x64). No runtime binary is committed or distributed with this plugin.

macOS POSIX process-group execution is verified. Linux unit tests and actual Hermes host E2E also pass on Python 3.14 with the official 1.8.0 Linux runtime (evidence/ci-linux.json and hermes-linux-e2e.json). Windows execution is unsupported. Workcell needs the supported OCI engine and local image; browser execution needs Lens's exact bridge dependencies and browser cache. The plugin never starts canonical services automatically.

The tests cover the pinned tool versions, not every version in the accepted runtime range. Use the source lock; replacing sources or runtime builds requires rerunning the real integration gates. No automatic upgrades or mutable branch downloads occur.

Receipt schema is `kujo.hermes.receipt/v1`, with the canonical definition digest, input/request digests, normalized outcome, argv, workspace, approval record, timestamps and bounded artifact hashes. It is distinct from `kujo.ability.receipt/v1`. The upstream Python SDK preview checks contracts only. The plugin does not implement the canonical policy, idempotency or audit runtime. Host CLI receipts cannot substitute for a product's canonical evidence.

The adapter changes host-specific defaults in the reference schemas for Hermes: CaseFile names, Lens output directory and Tribunal's non-overlapping storage directory. `upstream_definition_digest` and `host_transformations` retain the original identity and exact delta. The active digest covers the transformed definition. Canonical Ability IDs and effects remain stable.

Local host tests used the existing Python 3.11 Hermes dependency environment against the exact released source; these verify the APIs, while CI verifies the release's supported Python 3.14 runtime. CI uses Python 3.14 and upstream `uv sync --locked`, preserving Hermes's security dependency overrides. Plain `pip install -e hermes` cannot resolve its intentional Pillow override. The supported-runtime check passed in GitHub Actions run 41925825469.


Native onboarding was also exercised with Hermes's selected Python 3.14.9 environment on Intel macOS, using Kujo 1.8.0 and all 26 pinned source repositories. `demo/square/evidence/hermes-python314-e2e.json` records the actual loader, approval gate, six-tool workflow and receipt checks. Launch Hermes with its selected interpreter: retaining an older recorder's interpreter after PM installs newer binary dependencies can fail to import them. This recording issue was corrected without changing policy. The native `kujo setup` and `kujo doctor` CLI commands require in-process plugin registration; isolated-host mode skips plugin CLI commands and uses the documented manual setup.
