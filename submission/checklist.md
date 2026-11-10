# Submission handoff

The plugin is released as [v0.1.0](https://github.com/kujolang/kujo-hermes/releases/tag/v0.1.0). The catalog candidate is `4f7b27ef0216cf6284af42fb23f5211a22befd0b`: the release runtime plus corrected installation documentation. Hermes requires a full SHA for `--ref`, not a tag name. The catalog file, PR draft and validation links all identify this candidate.

## Prepared locally

- `kujo-hermes.yaml`: copy into `NousResearch/hermes-agent/plugin-catalog/kujo-hermes.yaml`.
- `pull-request.md`: PR title, description, risk disclosures and verification links.
- `x-announcement.md`: post text; attach the square MP4 and tag @NousResearch.
- `../demo/checkout-video/delivery/kujo-hermes-checkout.mp4`: full-resolution submission film.
- `../demo/checkout-video/delivery/kujo-hermes-checkout-480p.mp4`: mobile download.
- `../docs/hackathon/SUBMISSION-CHECKLIST.md`: evidence and final checks.

## Owner actions still required

1. Watch and listen to the complete final film. Automated audio measurements and pronunciation controls are checked, but they do not replace listening.
2. Review [catalog PR #152397](https://github.com/NousResearch/hermes-agent/pull/152397) and respond to maintainer feedback. Authorize the X post; it has not been published.
3. Save the public PR URL and X post URL, then submit them through [the official form](https://form.typeform.com/to/FwJLvOln) before **November 11, 2026, 5 PM EST**.

The live form was opened on November 9: it has six questions and begins with a required Plugin Title. No fields were filled or sent. Later required fields and terms must be reviewed during the authorized submission. The catalog PR URL is recorded in `evidence/catalog-pr.json`; the X URL remains pending.

Official references: [catalog admission](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins/catalog-submission), [Nous announcement](https://nousresearch.net/), and [form](https://form.typeform.com/to/FwJLvOln).

Exact catalog candidate [CI 42743837185](https://github.com/kujolang/kujo-hermes/actions/runs/42743837185) passed all three jobs: unit/package checks and real Hermes 0.22.7/0.23.0 clean installation, validation and workflows.

Verification: `python3 submission/verify.py` passes; `verification.json` binds the exact CI candidate to the decoded video hashes. Loop required gates pass. The final owner listening check is intentionally open.
