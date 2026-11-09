# Submission checklist

Deadline verified on the organizer's official LinkedIn announcement: **November 11, 2026, 5 PM EST (22:00 UTC)**. Recheck for updates and inspect the form before sending. [Research and source-access limits](COMPETITIVE-ANALYSIS.md).

## Product and candidate

- [x] Standalone native plugin; no other agent plugin dependency.
- [x] Public repository, MIT license, manifest and native entrypoint.
- [x] Six tools and two hooks match declared registrations.
- [x] Native commands, skill, cleanup, runtime/version checks and explicit setup documented.
- [x] Current host 0.23.0 native workflow exercised with real tools; previous minimum-version evidence retained.
- [x] Unit/security/lifecycle tests pass; actual failure/correction fixture repeats from new state.
- [x] SHA-256 receipts and artifact snapshots can be independently checked.
- [x] No global release enforcement, signature, universal correctness or all-tools-ready claim.
- [x] Candidate `6f847b98aae1260b22bff9579b341f0e11225af6` validated in CI; catalog YAML pins that exact tested implementation. Later commits record audit/validation outcomes only.
- [x] Clean Linux plugin install and complete validation at that pin passed on both supported host versions; local fresh-profile dependency preparation also passed.
- [x] Linux CI run 42637870905 passed all three jobs: unit, host 0.22.7, host 0.23.0. Logs and artifacts retained.
- [x] Catalog private-import warnings in standalone demonstration harnesses reviewed and disclosed; not claimed warning-free.

## Official catalog admission

- [ ] Copy `submission/kujo-hermes.yaml` to `NousResearch/hermes-agent/plugin-catalog/kujo-hermes.yaml` only after authorization.
- [ ] Full 40-character tested SHA, quoted version, HTTPS public repo, truthful SemVer floor and platforms.
- [x] Capabilities list matches tools/hooks; no undeclared middleware or required credentials.
- [x] Bounded Python dependency; no bundled executables, core monkey patches, runtime self-updater or credential-file reads.
- [x] Disclose source downloads, repository reads, subprocesses, possible provider calls, optional services, background jobs and local receipt storage.
- [ ] Attach exact-pin doctor/validation logs, current CI result and native workflow evidence to PR draft.
- [ ] Owner/major contributor opens PR; wait for catalog CI and answer review comments. Catalog listing requires human merge, separate from contest submission timing.

## Film and public presentation

- [x] Existing 88-second square film audited directly via decoded frames and source timing.
- [x] Replacement 86-second storyboard and real checkout fixture prepared.
- [x] README opens with concrete developer outcome; monochrome badges retained.
- [x] Recorded a real Qwen3.5 4B Hermes conversation: Spec, failing Eval, model patch, unchanged tests passing, receipt retrieval and tool discovery. See `demo/checkout-video/evidence/run-verification.json`.
- [ ] Export matching real evidence; preserve raw take and approval decisions.
- [x] Rendered 88-second square film and 480p copy; checked full screens, matching recorded subjects, complete decode and measured audio. See `demo/checkout-video/evidence/`.
- [ ] Listen to the complete final film before posting; automated checks measured audio but did not audition it.
- [x] Reused authorized music, logos and effects; new Siren V4 narration records the generation-time Creator tier and request provenance.
- [x] Final outro retains the install CTA; installation uses the native Hermes commands.
- [ ] Verify README/demo/catalog all describe the same candidate and boundaries.

## External submission — approval required

- [x] Verified official announcement: four criteria, beyond-prompts preference, November 11 deadline, working demo under 90 seconds and submission links. Recheck for late changes before posting.
- [ ] Open the authorized catalog PR; save public URL.
- [ ] Upload the approved public demo to X and tag **@NousResearch**; save post URL.
- [ ] Inspect the official form's actual fields and terms: https://form.typeform.com/to/FwJLvOln.
- [ ] Submit PR and public demo links before the deadline; save confirmation. No form submission, post, release or external PR has been made by this audit.

The local commit/push requested for development is not authorization to publish the contest entry. Evidence status and remaining actions are in [the verification ledger](evidence/VERIFICATION.md).
