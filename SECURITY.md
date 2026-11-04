# Security

Report security issues privately to the repository owner through GitHub security advisories. Do not place credentials or sensitive repository contents in public issues.

The execution boundary trusts operator-selected canonical source checkouts and exact workspace roots. It is not a filesystem or network sandbox. Use Workcell for container isolation. All extension bindings require a fresh native human approval regardless of their declared effects. Profiles never grant permission. Unknown schemas, untrusted paths, missing approvals and unsupported runtimes fail closed. The plugin never enables YOLO mode or synthesizes approvals for downstream Kujo systems.

Receipts use local SHA-256 integrity checks, not digital signatures or nonrepudiation. A machine owner able to rewrite both payload and checksum can forge them. Canonical product evidence remains authoritative. Receipt retention is operator-managed; remove old plugin-data receipts explicitly when no longer needed. No telemetry runs automatically. Optional explicit Watchdog calls reach literal loopback addresses only.

Children inherit a minimal environment and an isolated HOME, with only explicitly configured secret names fetched from Hermes secret scope. Output redaction is defense in depth, not a promise that arbitrary source content contains no sensitive information. Review receipts before sharing. The plugin does not read vendor login files or refresh credentials.

Cancellation kills the POSIX process group and records cancellation; already-completed external effects cannot be rolled back. Approval binds normalized input, definition digest, workspace and argv, expires after five minutes, and is consumed once. Canonical tool policy and interactive approval restrictions remain active. Concurrent malicious filesystem modification is outside the trusted-workspace threat model.
