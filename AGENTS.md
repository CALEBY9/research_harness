# Research Harness maintenance

This repository owns the versioned Research Agent source. `skills/` contains
the imported, locally enhanced installation; it is not the live skill directory.
Read `docs/architecture.md` and `.agent/NEXT.md` when resuming maintenance.

- Edit the smallest owner of an observed failure. Keep `research-agent` a router.
- Preserve Nature owner boundaries, author-controlled scientific decisions,
  bilingual prose requirements, source authority and clean-final delivery.
- Keep existing skill names, including legacy underscores and the Humanizer alias.
- Do not copy project manuscripts, corpora, session transcripts, credentials,
  global runtime configuration or private evaluation inputs into this repository.
- Keep machine paths and private evaluations in ignored `local_state/`.
- Source changes do not authorize replacing installed skills. Compare the source
  and installed version, show the affected files, then apply the authorized scope.
- Use `python scripts/harness.py validate` and the affected owner's checks.
  A structural PASS is not evidence of better writing or scientific judgment.
- For behavioral changes, follow the imported `skill_evolve_workflow` contract.
  Do not enable automatic self-editing, paid evaluations, schedules or subagents.
- Keep `.agent/STATE.md` and `.agent/NEXT.md` local and concise after implementation.

OpenSpec uses the project-local `research-task` schema and the Research Agent
reference `skills/research-agent/references/openspec-research.md`. Follow existing
authorization through implementation; planning-only requests remain planning-only.
Verify the requirements linked from tasks.md even without delta specs. Artifact
presence or checked tasks alone are not acceptance evidence. Keep project-specific
science in its owning project; archive must not rewrite scientific definitions.
