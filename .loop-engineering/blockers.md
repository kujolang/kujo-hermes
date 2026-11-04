# Current external blockers

The harness appends historical classifications. This final snapshot reconciles them against docs/acceptance.md; prior classifications remain in iteration evidence. Clean installation is resolved by CI 41925825469.

blockers:
  - id: optional-browser-container-prerequisites
    status: external-blocked
    evidence: evidence/optional-tools.json
    next_action: Install the pinned Lens browser and expose an approved Workcell engine/image, then rerun optional checks.
  - id: producer-gateway-contracts
    status: needs-contract-first
    evidence: docs/parity.md
    next_action: Establish verified canonical producer bindings; do not infer a Foreman executable.
