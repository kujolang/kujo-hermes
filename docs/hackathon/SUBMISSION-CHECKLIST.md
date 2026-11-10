# Submission checklist — November 9

Deadline: **November 11, 2026, 5 PM EST (22:00 UTC)**. The [official Nous announcement](https://nousresearch.net/) confirms usefulness, reliability, polish and creativity, with preference for functionality beyond prompts or skills. The [catalog rules](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins/catalog-submission) require a public repository, exact full SHA, loadable manifest, truthful capabilities and official validation.

## Ready product and materials

- [x] Official [v0.1.0 release](https://github.com/kujolang/kujo-hermes/releases/tag/v0.1.0), four verified downloadable assets and checksums.
- [x] Standalone native plugin; six tools, two hooks, setup/Doctor, Skill and unload cleanup.
- [x] 64 unit/regression tests, 45 canonical operations and real host workflows verified during release hardening.
- [x] Release runtime passes [Linux CI](https://github.com/kujolang/kujo-hermes/actions/runs/42742232654) on Hermes 0.22.7 and 0.23.0, including clean installation.
- [x] Catalog candidate `4f7b27ef0216cf6284af42fb23f5211a22befd0b` retains the release runtime and fixes installation documentation. See `submission/kujo-hermes.yaml`.
- [x] Source permissions, processes, network use, optional services, receipts and limits disclosed in the PR draft.
- [x] Original free-model checkout recording and independently verified failure/correction evidence preserved.
- [x] README keeps monochrome badges and concrete developer benefits.
- [x] Updated storyboard includes official release, two install commands, real workflow and install CTA.
- [x] Draft catalog YAML, PR text and X announcement prepared under `submission/`.

## Final media checks

Use `demo/checkout-video/evidence/delivery-verification.json`, `video-subject-verification.json`, `release-check.json` and the original `demo/square/evidence/installation-provenance.json` for the current rendered files. Their exact hashes must match the delivery files; do not substitute older verification reports.

- [ ] Owner watches and listens to the entire final film, including “Hermes” pronunciation and mobile readability, before posting.
- [ ] Public X URL recorded after approved publication.

The film uses Roger V4 narration, not the older Siren version. Generation receipts preserve Creator-tier licensing and pronunciation controls. Source footage and music provenance remain in the demo directory. Local installation failures are retained rather than described as successful takes. No universal correctness, global release gate or signed-attestation claim is made.

## External actions — not authorized yet

- [ ] Open a PR adding `submission/kujo-hermes.yaml` to `NousResearch/hermes-agent/plugin-catalog/kujo-hermes.yaml`; use the prepared PR body and attach exact-pin evidence.
- [ ] Confirm catalog CI and respond to review. Listing requires a maintainer merge.
- [ ] Post the reviewed under-90-second MP4 on X tagging **@NousResearch**.
- [ ] Submit the PR and X URLs through [the official form](https://form.typeform.com/to/FwJLvOln) and retain confirmation before the deadline.

The live form was inspected on November 9: six questions, starting with required Plugin Title. No fields were filled or submitted; remaining fields and terms require review during submission. The release is public, but the catalog PR, X post and contest entry have not been sent. See [the owner handoff](../../submission/checklist.md).

Exact catalog candidate [CI 42743837185](https://github.com/kujolang/kujo-hermes/actions/runs/42743837185) passed all three jobs: unit/package checks and real Hermes 0.22.7/0.23.0 clean installation, validation and workflows.
