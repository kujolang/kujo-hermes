# Configuration

Settings live only in the active Hermes profile at `plugins.entries.kujo-hermes.settings`. Repository files cannot grant trust or configure executable sources. Restart/reload after changing settings; use `kujo_discover(refresh=true)` to reload catalog contents.

| Setting | Default | Meaning |
|---|---|---|
| ecosystem_root | empty | Absolute directory of canonical source checkouts named by repository |
| kujo_bin | kujo | Absolute runtime path recommended; version checked before execution |
| trusted_workspaces | [] | Exact absolute roots; descendants are not automatically separate trusted repos |
| profile | essentials | essentials, review, ship, full |
| timeout_seconds | 240 | 1–900 seconds per child process |
| max_output_bytes | 524288 | Combined stdout/stderr bound, 1024–4194304 bytes |
| extension_catalogs | [] | Absolute operator-reviewed JSON catalog files, 2 MiB each; max 1000 total entries |
| denied_abilities | [] | IDs excluded even from Full |
| secrets | [] | Explicit uppercase secret names fetched from Hermes secret scope and passed to children |

Normal installation needs only the source root, runtime path and workspace list. Optional live provider operations may require `PACKWRITE_API_KEY`, `OPENAI_API_KEY`, or `WDG_API_AUTH_TOKEN` through Hermes's profile secrets. The plugin does not inspect shell environment values, `.env`, auth JSON, keychains or CLI credential stores. Source code and repository configuration remain trusted executable material; only select tools that honor this boundary.

## Dynamic extension contract

The portable `definition` is the actual `kujo.ability/v1` contract. The `binding` below is Hermes-owned transport configuration, not a claimed universal Kujo standard. The operator supplies it outside the workspace. New definitions are available after explicit refresh in Full, without plugin code changes.

```json
[
  {
    "definition": {
      "schema": "kujo.ability/v1",
      "id": "kujo.example.repository.inspect",
      "version": "1.0.0",
      "description": "Inspect repository through an operator-installed canonical tool.",
      "input_schema": {"type":"object","properties":{},"additionalProperties":false},
      "output_schema": {"type":"object"},
      "effects": [{"kind":"read","resource":"kujo.example.repository"}],
      "idempotency": {"mode":"intrinsic"}
    },
    "binding": {"argv":["/absolute/path/to/canonical-tool","inspect","{workspace}"]}
  }
]
```

Each argument is a literal token or whole-field placeholder. Objects/lists become one JSON argument. No shell string interpolation. Unknown extensions always require human approval, irrespective of effects; adding a file is not an execution grant. Duplicate IDs, invalid definitions/schemas, remote schema references and relative executables reject the whole refresh. A failed refresh leaves the prior validated snapshot intact.

The bundled catalog records definitions absent from local installation rather than hiding missing dependencies. Installing a canonical tool at its configured source path makes its existing operation available immediately. New semantic definitions require an operator-reviewed extension binding because the canonical ecosystem has no universal production catalog/CLI protocol for all products.

## Results and lifecycle

`kujo_execute` needs `ability`, `input` and absolute `workspace`. Optional `background:true` returns an invocation ID immediately after approval. Poll `kujo_status`; set `cancel:true` to terminate the owned process group. No retries happen automatically, and no keyed-idempotency replay is claimed for CLI bindings. If an external operation times out, inspect evidence before retrying.

`kujo_receipts` without an ID lists at most 50 records. With an ID it verifies the whole record and returns `limit` characters (up to 12000), `offset`, and `next_offset`. Full evidence persists in the active profile's plugin data directory. Updates do not erase it. Canonical tools' own receipts remain in their workspace artifact directories.

## Troubleshooting

- **Unsupported runtime:** PATH may select an old Kujo; set `kujo_bin` to the intended absolute executable. Doctor reports the resolved version.
- **Missing source:** run source installer with `--only <repository>`, or correct `ecosystem_root`. Setup refuses dirty or differently pinned checkouts.
- **Untrusted workspace/path escape:** add the exact real repository root as an operator; do not broaden trust to a home directory.
- **No matching approval:** use an interactive Hermes session with manual approvals. Automatic approvals deliberately cannot authorize mutating operations.
- **Downstream approval denied:** complete that product's authorized operator setup. Hermes consent does not replace a product's own permission system.
- **PackWrite path error:** outputs must be relative within the workspace; the adapter preserves this upstream restriction.
- **Lens browser missing:** install Lens's pinned dependencies/browser using its canonical instructions; no browser download happens on plugin load.
- **Workcell cannot start:** run its doctor; install Git, jq, Docker/Podman and the approved local image. No image pull is implicit.
- **Catalog validation dependency download timeout:** retry with network access to PyPI. Source/manifest validation passing alone does not prove clean dependency installation.
