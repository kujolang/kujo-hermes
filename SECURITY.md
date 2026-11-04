# Security

Report security issues privately to the repository owner through GitHub security advisories. Do not place credentials or sensitive repository contents in public issues.

The plugin trusts the canonical source checkouts and exact workspace roots selected by the operator. It is not a filesystem or network sandbox. Use Workcell for container isolation. All extension bindings require a fresh native human approval regardless of their declared effects. Profiles never grant permission. Unknown schemas, untrusted paths, missing approvals and unsupported runtimes fail closed. The plugin never enables YOLO mode or invents approvals for underlying Kujo tools.

Receipts use local SHA-256 checks. They are not digitally signed and cannot prove who created them. A machine owner able to rewrite both payload and checksum can forge them. Canonical product evidence remains authoritative. Operators manage retention and can delete old plugin-data receipts when no longer needed. No telemetry runs automatically. Optional Watchdog calls reach literal loopback addresses only.

Children inherit a minimal environment and an isolated HOME, with only explicitly configured secret names fetched from Hermes secret scope. Redaction adds protection, but source content may still contain sensitive information. Review receipts before sharing. The plugin does not read vendor login files or refresh credentials.

Cancellation kills the POSIX process group and records cancellation; it cannot undo external effects that have already occurred. Approval binds normalized input, definition digest, workspace and argv, expires after five minutes, and is consumed once. Canonical tool policy and interactive approval restrictions remain active. Concurrent malicious filesystem modification is outside the trusted-workspace threat model.
