# Improvement plan

The missing element is a complete, memorable engineering outcome. No new dashboard, rollback engine or additional tool integration is justified before the deadline.

| Priority | Change | Judging impact | Effort / risk | Decision and evidence |
|---|---|---|---|---|
| P0 | Replace stale catalog pin with the tested candidate | Validity, reliability | 15 min / low | Prepare after implementation commit; verify exact tree before external PR. Original pin omitted recent setup and hardening. |
| P0 | Validate current stable Hermes and clean install | Reliability | 1–2 h / low | Native 0.23.0 workflow passed. Official validator and dependency install evidence must be judged separately; see checklist for actual outcome. CI now covers 0.22.7 and 0.23.0. |
| P0 | Remove ambiguity between command success, checks and receipt integrity | Reliability, honesty | 30 min / low | Native descriptions and engineering skill clarified. No claim that ShipCheck blocks arbitrary release actions. |
| P0 | Preserve submission prerequisites and disclosures | Admission | 30 min / low | Runtime remains a separate prerequisite; setup fetches 26 sources; optional service/container/browser requirements remain visible. |
| P1 | Real regression → correction → unchanged checks → both receipts | Usefulness, demo, creativity | 1–2 h / low | Implemented checkout fixture through real Hermes gate/registry and canonical Spec/Eval; repeated twice. Correction is explicitly fixture-driven, not attributed to an LLM. |
| P1 | Independent portable evidence verification | Reliability, developer handoff | 30 min / low | Standard-library helper checks both receipt digests, snapshot artifact hashes and unchanged tests. Not a new security attestation system. |
| P1 | Lead README and film with the developer outcome | Polish, clarity | 1 h + recording / low | README updated; 86-second storyboard supplied. Final autonomous chat take and edited replacement film remain separate work, not implied by the fixture. |
| P2 | Compact receipt history with operation/time labels | Daily usability | 2–4 h / moderate | Defer: useful, but new API/UI behavior is less valuable than the completed film. UUID-only lists are awkward. |
| P2 | Selective first-run source profile | Setup time | 2–4 h / moderate | Defer: preserve tested 26-source setup. Document the existing `--only` installer path. Measure before claiming faster installation. |
| P2 | Catalog cover and screenshot pair from real failure/success | Marketplace polish | 1 h / low | Use the verified fixture, not a fabricated dashboard. Optional after validation and film. |
| P3 | Global release/commit enforcement | New product capability | Days / high | Requires explicit approval and contract design. Current hooks gate Kujo executions only; don't retrofit broad blocking near submission. |
| P3 | Desktop evidence timeline, signed attestations, source-state binding | Long-term trust/UX | Days–weeks / high | Recommend investigation after hackathon. Receipt checksum alone cannot establish authorship or immutable repository state. |
| P3 | Automatic recovery / incident learning | Competitive imitation | Weeks / high | Not needed for this entry. Existing competitors already specialize here. |

## Stop conditions

Do not publish on a failed catalog validation, dependency resolution or mismatched pin. Do not hide an external blocker behind an old passing log. Do not add a feature to rescue a weak story when an existing verified workflow already tells it. Substantial additions need owner approval.

The three highest-impact remaining actions are: record the real correction workflow in Hermes; obtain a clean current-version installation/validation result at the final pin; submit the exact reviewed candidate, matching demo and disclosures before the deadline. Publication remains owner-authorized work.
