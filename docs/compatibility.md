# Compatibility and security notes

Verified host: official Hermes tag `v0.22.7`, commit `b200f5bc60e31588ba2cb60e288029c4a54ba5fa`. The machine's previously installed Hermes checkout was also inspected but was not treated as the release source of truth. The released tag's source package metadata reports a development `0.0.0`; the plugin floor uses the actual released SemVer tag.

The adapter uses public native registration, approval-observer hooks and unload callbacks. Tests exercise both `plugins.isolation: in_process` and the default `host` process. No undocumented `request_tool_approval` import remains; catalog validation's public-surface check passes. An automatic host approval is insufficient without the observed human event, so unattended mutations fail closed. Gateway interactive prompting is not certified here.

Kujo runtime range: >=1.6,<2. Exact tool-source commits are in `catalog/sources.lock.json`. Runtime builds can omit optional features: the local 1.9.0 development build lacks `runtime-db`, so it cannot run Watchdog's SQLite service. A version alone does not prove every native feature is compiled in. Tool errors retain their exact diagnostics. The official host-independent 1.8.0 runtime binary was also tested; its SHA-256 is `979d49503d71eb87e5696aea844a51e7129e23c89e36abc8e4d4378bc78985b5` (Darwin x64). No runtime binary is committed or distributed with this plugin.

macOS POSIX process-group execution is verified. Linux follows the same implementation and is covered by unit CI configuration but has not been live-certified in this session. Windows execution is explicitly unsupported. Workcell needs the supported OCI engine and local image; browser execution needs Lens's exact bridge dependencies and browser cache. Canonical services are never automatically started by the plugin.

No claim is made that every product version in the supported runtime range works. Use the source lock; replacing sources or runtime builds requires rerunning the real integration gates. No automatic upgrades or mutable branch downloads occur.

Receipt schema is `kujo.hermes.receipt/v1`, with the canonical definition digest, input/request digests, normalized outcome, argv, workspace, approval record, timestamps and bounded artifact hashes. It is distinct from `kujo.ability.receipt/v1`. The upstream canonical Python SDK preview is used for contract checks only; the plugin does not claim to reproduce the canonical policy/idempotency/audit runtime. Host CLI receipts cannot substitute for a product's canonical evidence.

Reference schemas with host-specific defaults are transformed explicitly for Hermes: CaseFile names, Lens output directory and Tribunal's non-overlapping storage directory. `upstream_definition_digest` and `host_transformations` retain the original identity and exact delta. The active digest covers the transformed definition. Canonical Ability IDs and effects remain stable.

Local host tests used the existing Python 3.11 Hermes dependency environment against the exact released source; this demonstrates the APIs but is not a certification of the release's supported Python 3.14 runtime. CI uses Python 3.14 and upstream `uv sync --locked`, preserving Hermes's security dependency overrides. Plain `pip install -e hermes` cannot resolve its intentional Pillow override. See recorded CI results for the supported-runtime check.
