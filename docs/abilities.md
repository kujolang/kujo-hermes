# Supported Ability inventory

Exact schemas, effects, dependencies and evidence: [machine-readable inventory](ability-inventory.json). All execution uses `kujo_execute`; schema inspection is on demand. `ok` reports execution success, not release readiness. Untested bindings are not certified.

| Ability | Canonical source / operation | Approval | Evidence |
|---|---|---|---|
| kujo.ability.catalog.list | native / catalog | read policy | real canonical CLI passed |
| kujo.ability.receipts.list | native / receipts | read policy | real canonical CLI passed |
| kujo.scout.repository.inspect | scout / scout | human | real canonical CLI passed |
| kujo.scent.context.pack | scent / scent | human | real canonical CLI passed |
| kujo.patchbrief.changes.summarize | patchbrief / patchbrief | read policy | real canonical CLI passed |
| kujo.changebucket.changes.measure | changebucket / changebucket | read policy | real canonical CLI passed |
| kujo.shipcheck.repository.scan | shipcheck / shipcheck | read policy | real canonical CLI passed |
| kujo.fence.architecture.check | fence / fence | read policy | real canonical CLI passed |
| kujo.spec.contract.validate | spec / spec | read policy | real canonical CLI passed |
| kujo.eval.suite.run | eval / eval | human | real canonical CLI passed |
| kujo.runledger.runs.report | runledger / runledger | read policy | real canonical CLI passed |
| kujo.dispatch.workflow.validate | dispatch / dispatch | read policy | real canonical CLI passed |
| kujo.rag.knowledge.query | rag / rag | read policy | real canonical CLI passed |
| kujo.watchdog.service.health | watchdog / watchdog | read policy | real canonical CLI passed |
| kujo.concord.artifacts.scan | concord / concord | read policy | real canonical CLI passed |
| kujo.casefile.failure.capture | casefile / casefile | human | real canonical CLI passed |
| kujo.muzzle.workflow.run | muzzle / muzzle | human | real canonical CLI passed |
| kujo.kennel.project.validate | kennel / kennel_validate | read policy | real canonical CLI passed |
| kujo.kennel.dependencies.install | kennel / kennel_install | human | real canonical CLI passed |
| kujo.dispatch.workflow.run | dispatch / dispatch_run | human | real canonical CLI passed |
| kujo.rag.knowledge.ingest | rag / rag_ingest | human | real canonical CLI passed |
| kujo.watchdog.telemetry.record | watchdog / watchdog_record | human | real canonical CLI passed |
| kujo.redact.document.scan | redact / redact_scan | human | real canonical CLI passed |
| kujo.redact.document.sanitize | redact / redact_sanitize | human | real canonical CLI passed |
| kujo.versionseal.records.validate | versionseal / versionseal_validate | read policy | real canonical CLI passed |
| kujo.packwrite.pack.validate | packwrite / packwrite_validate | read policy | real canonical CLI passed |
| kujo.packwrite.pack.summary | packwrite / packwrite_summary | read policy | real canonical CLI passed |
| kujo.packwrite.pack.init | packwrite / packwrite_init | human | real canonical CLI passed |
| kujo.runledger.runs.start | runledger / runledger_start | human | real canonical CLI passed |
| kujo.runledger.runs.finish | runledger / runledger_finish | human | real canonical CLI passed |
| kujo.tribunal.proposal.validate | tribunal / tribunal_validate | read policy | real canonical CLI passed |
| kujo.tribunal.review.mock | tribunal / tribunal_review | human | real canonical CLI passed |
| kujo.dossier.records.validate | dossier / dossier_validate | read policy | real canonical CLI passed |
| kujo.dossier.records.report | dossier / dossier_report | read policy | real canonical CLI passed |
| kujo.howl.showcase.validate | howl / howl_validate | read policy | real canonical CLI passed |
| kujo.howl.showcase.render | howl / howl_render | human | real canonical CLI passed |
| kujo.lens.flow.validate | lens / lens_flow_validate | read policy | real canonical CLI passed |
| kujo.lens.page.check | lens / lens_check | human | real canonical CLI failed: {'type': 'failed', 'message': 'Canonical command did not complete successfully'} |
| kujo.workcell.definition.validate | workcell / workcell_validate | read policy | real canonical CLI passed |
| kujo.workcell.definition.inspect | workcell / workcell_inspect | read policy | real canonical CLI passed |
| kujo.workcell.definition.run | workcell / workcell_run | human | real canonical CLI failed: {'type': 'failed', 'message': 'Canonical command did not complete successfully'} |
| kujo.workcell.runtime.doctor | workcell / workcell_doctor | read policy | real canonical CLI failed: {'type': 'failed', 'message': 'Canonical command did not complete successfully'} |
| kujo.workflows.loop.run | kujo-workflows / loop | human | real canonical CLI passed |
| kujo.runtime.version.inspect | kujo / runtime_version | read policy | real canonical CLI passed |
| kujo.runtime.source.check | kujo / runtime_check | read policy | real canonical CLI passed |
| kujo.runtime.source.run | kujo / runtime_run | human | real canonical CLI passed |
| kujo.hermes.lint.execute | kujo / lint | read policy | real canonical CLI passed |
| kujo.hermes.format.execute | kujo / format | human | real canonical CLI passed |
| kujo.hermes.lsp.diagnostics.execute | kujo / lsp_diagnostics | read policy | real canonical CLI passed |
| kujo.hermes.lsp.complete.execute | kujo / lsp_complete | read policy | real canonical CLI passed |
| kujo.hermes.mcp.make.execute | mcp / mcp_make | human | real canonical CLI passed |
