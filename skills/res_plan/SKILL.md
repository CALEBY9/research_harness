---
name: res_plan
description: Turn a refined proposal into a claim-driven experiment, data-analysis, baseline, evaluation, and figure roadmap.
---

Use subagents only when the user explicitly requests delegation; otherwise perform role checks locally.

# Experiment Plan — Claim-Driven, Paper-Oriented Validation

Refine and concretize: **$ARGUMENTS**

## Role in the Research Workflow

`res_plan` is the Planning-stage experiment and analysis roadmap skill. It converts a final proposal into the exact evidence package needed for `data_analyze`, `res_analyze`, and `nature-writing`.

Complete the requested operation only. Use the corresponding owner for a needed handoff within the user's authorized scope; these skills are not a mandatory stage chain.

## Goal

Design a compact validation plan that proves:

1. the method or analysis answers the anchored environmental question
2. the dominant contribution is real and focused
3. mature field baselines are addressed
4. cross-domain or frontier components are justified rather than decorative
5. figures and tables needed for the paper are planned before execution

## Constants

- **OUTPUT_DIR = `refine-logs/`** — Default destination for experiment planning artifacts
- **MAX_PRIMARY_CLAIMS = 2** — Prefer one dominant claim plus one supporting claim
- **MAX_CORE_BLOCKS = 5** — Keep the must-run experimental story compact
- **MAX_BASELINE_FAMILIES = 3** — Prefer a few strong baselines over many weak ones
- **DEFAULT_SEEDS = 3** — Use 3 seeds when stochastic variance matters and budget allows

## Workflow

### Phase 0: Load Proposal Context

Read the most relevant existing files first if they exist:

- `refine-logs/FINAL_PROPOSAL.md`
- `refine-logs/REVIEW_SUMMARY.md`
- `refine-logs/REFINEMENT_REPORT.md`
- `idea.json`
- `IDEA_REPORT.md`

Extract:
- problem anchor
- dominant contribution
- optional supporting contribution
- critical reviewer concerns
- data, compute, fieldwork, software, or timeline constraints
- mature baselines and field standards
- cross-domain or frontier component, if central

If these files do not exist, derive the same information from the user's prompt.

### Phase 1: Data Audit and Freeze the Paper Claims

Before proposing experiments, confirm the data audit from `res_method` or derive a compact one from the prompt. Check:
- data structure and file organization
- data quality, missingness, uncertainty, and bias
- variable semantics, units, spatial/temporal scale, and coordinate systems
- dependencies among datasets, preprocessing steps, models, and metadata
- access, license, privacy, and reproducibility constraints
- external database/API retrieval contract when the evidence depends on public or licensed endpoints: authoritative source, target entity/identifier, filters, endpoint or access route, pagination/count reconciliation, server-side versus local filters, access date, and failure warnings

If the data cannot support the intended claim, stop with a data-gap checklist rather than planning experiments around unsupported assumptions.

External database/API retrieval is an auditable data path, not a hidden default dependency. If the source, endpoint, key, license, or pagination semantics are unavailable, record the limitation and plan the next best verifiable data route instead of drawing conclusions from partial lookups.

Then write down the claims that must be defended:

- **Primary claim**: main mechanism, method, data, or finding contribution
- **Supporting claim**: optional, only if it directly strengthens the main story
- **Anti-claim to rule out**: e.g. gain only comes from a larger search space, a simpler baseline would suffice, spatial pattern is a data artifact
- **Minimum convincing evidence**: what would make each claim believable to a strong reviewer
- **Cross-domain inspiration**: which adjacent field supplies a relevant paradigm, if any
- **Why transfer is valid**: why that paradigm should work here
- **Failure boundary**: when the transfer breaks or becomes unconvincing

### Phase 2: Build the Experimental Storyline

Default blocks; keep only those that defend a claim:

1. **Main anchor result** — does the method or analysis solve the actual environmental bottleneck?
2. **Baseline comparison** — does it outperform or clarify mature field standards?
3. **Novelty isolation** — does the dominant contribution itself matter?
4. **Transfer / frontier necessity check** — if a borrowed or frontier component is central, is it actually necessary and valid?
5. **Uncertainty, sensitivity, or failure analysis** — where does the result hold or fail?
6. **Figure-readiness block** — what must be computed for maps, diagrams, trend plots, or statistical panels?

For each block, classify it as:
- **Main paper** — essential to defend the core claims
- **Appendix** — useful but non-blocking
- **Cut** — interesting but not worth the paper budget

### Phase 3: Specify Each Experiment Block

For every kept block, specify:

- claim tested
- why this block exists
- dataset / split / region / period / task
- compared systems, baselines, ablations, or variants
- metrics or environmental indicators
- setup details: resolution, preprocessing, model settings, statistical design, seeds if needed
- success criterion
- failure interpretation
- figure/table target
- priority: MUST-RUN or NICE-TO-HAVE

Special rules:
- If the proposal uses cross-domain borrowing, include at least one transfer-legality check.
- If the proposal is intentionally non-frontier, state that and skip frontier checks.
- If professional software is needed for figures, include the intended software workflow and required intermediate data.

#### Scorable Task Eligibility Gate

Use this gate only when an experiment block may be framed as an empirical-software or candidate-search problem: the project has a clear dataset, a machine-computable quality score, candidate methods or code variants, and enough budget to run and compare alternatives.

Do not use this gate for theory-building, causal/mechanistic claims, qualitative interpretation, policy argument, field sampling design, or manuscript framing unless those tasks have an explicit executable scoring function.

```markdown
| Block / Claim ID | Scorable objective | Dataset / split | Quality score | Baseline / initial solution | Candidate source | Budget / stop rule | Leakage / score-hacking risk | Decision |
|------------------|--------------------|-----------------|---------------|-----------------------------|------------------|--------------------|------------------------------|----------|
```

Rules:
- Treat score optimization as a way to find empirical software, not as proof of genuine scientific discovery.
- Separate training/search, validation, and holdout evidence before allowing performance claims.
- Record baseline reproduction before claiming a search-derived improvement.
- If candidate recombination, LLM assistance, literature-derived method summaries, or guided retry are used, also trigger the Optional Assisted Feedback / Reward-Credit Gate.
- Hand search-derived results to `data_analyze` with a Candidate Search Ledger requirement and to `evidence_audit` with a Search-Derived Result Audit requirement.

#### Optional Assisted Feedback / Reward-Credit Gate

Use this gate only when the proposed method or experiment relies on teacher guidance, critic feedback, verifier signals, self-correction, retry loops, RL feedback, distillation, synthetic feedback, or guided search. Do not use it for ordinary statistical analysis, pure supervised baselines, or experiments where no external assistance is available during training, inference, or evaluation.

When triggered, separate assisted performance from independent performance:

| Component | Assistance source | Assistance timing | Credit / reward accounting | Independent metric | Assisted metric | Required ablation | Shortcut / reliance risk | Decision |
|-----------|-------------------|-------------------|----------------------------|--------------------|------------------|-------------------|--------------------------|----------|

Rules:
- Report independent and assisted metrics separately.
- If the claim depends on assisted performance, include assistance cost, reward discount, latency, compute, or human-effort accounting.
- Ablate both the guidance source and the credit/reward accounting rule when they are central to the claimed gain.
- If performance collapses without assistance or independent performance stagnates, downgrade the claim to assisted-system performance.
- Treat teacher, critic, or verifier access to ground truth, reference answers, future data, or labels as an oracle/leakage risk unless that access is explicitly part of deployment.
- Hand unresolved leakage, shortcut, or provenance risks to `evidence_audit` before paper-level claims are made.

### Phase 4: Execution Order

Use this milestone structure:

1. **Sanity stage** — data pipeline, metric correctness, toy region or small sample
2. **Baseline stage** — reproduce mature baseline or field-standard analysis
3. **Main method stage** — run the proposed method or analysis on the primary setting
4. **Decision stage** — decisive ablations, transfer checks, sensitivity tests
5. **Polish stage** — robustness, qualitative diagnosis, paper figures, appendix extras

For each milestone, estimate:
- compute or human effort
- stop/go decision gate
- risk and mitigation
- expected output path

### Phase 5: Write Outputs

#### `refine-logs/EXPERIMENT_PLAN.md`

```markdown
# Experiment Plan

**Problem**: [problem]
**Method Thesis**: [one-sentence thesis]
**Date**: [today]

## Data Audit Gate
| Dimension | Finding | Risk | Decision / Required Action |
|-----------|---------|------|----------------------------|
| Structure |  |  |  |
| Quality |  |  |  |
| Semantics |  |  |  |
| Dependency |  |  |  |
| Access / License |  |  |  |

## Data Source / API Retrieval Contract
| Source | Target entity / ID | Endpoint or access route | Required filters | Pagination / count check | Server-side vs local filters | Access / license | Failure warning |
|--------|--------------------|--------------------------|------------------|--------------------------|------------------------------|------------------|-----------------|

## Scorable Task Eligibility Gate
Include only when a block is a candidate-search or empirical-software task.

| Block / Claim ID | Scorable objective | Dataset / split | Quality score | Baseline / initial solution | Candidate source | Budget / stop rule | Leakage / score-hacking risk | Decision |
|------------------|--------------------|-----------------|---------------|-----------------------------|------------------|--------------------|------------------------------|----------|

## Claim Map
| Claim ID | Claim | Why It Matters | Expected Evidence ID / Locator | Minimum Convincing Evidence | Figure/Table Target | Cross-domain Inspiration | Why Transfer Is Valid | Failure Boundary | Linked Blocks |
|----------|-------|----------------|--------------------------------|-----------------------------|--------------------|--------------------------|-----------------------|------------------|---------------|

## Paper Storyline
- Main paper must prove:
- Appendix can support:
- Experiments intentionally cut:

## Experiment Blocks

### Block 1: [Name]
- Claim ID tested:
- Expected Evidence ID / Locator:
- Why this block exists:
- Dataset / split / region / period / task:
- Compared systems:
- Metrics / indicators:
- Setup details:
- Success criterion:
- Failure interpretation:
- Table / figure target:
- Expected output path:
- Priority: MUST-RUN / NICE-TO-HAVE

## Optional Assisted Feedback / Reward-Credit Gate
Include only if the method uses teacher, critic, verifier, self-correction, retry, RL feedback, distillation, synthetic feedback, or guided search.

| Component | Assistance source | Assistance timing | Credit / reward accounting | Independent metric | Assisted metric | Required ablation | Shortcut / reliance risk | Decision |
|-----------|-------------------|-------------------|----------------------------|--------------------|------------------|-------------------|--------------------------|----------|

## Run Order and Milestones
| Milestone | Goal | Runs | Decision Gate | Cost | Risk | Output Path |
|-----------|------|------|---------------|------|------|-------------|

## Compute, Data, and Software Budget
- Estimated compute:
- Data preparation needs:
- Software / professional plotting needs:
- Human evaluation or expert interpretation needs:
- Biggest bottleneck:

## Risks and Mitigations

## PI-style Critic Gate
- Fatal flaw risk:
- Strongest reviewer objection:
- Data or evidence gap that would stop the project:
- Decision: PROCEED / REVISE PLAN / RETURN TO METHOD / STOP

## Final Checklist
- [ ] Main paper tables are covered
- [ ] Main paper figures are planned
- [ ] Novelty is isolated
- [ ] Mature baselines are included
- [ ] Transfer/frontier contribution is justified or explicitly not claimed
- [ ] Scorable-task searches, if used, have explicit metrics, split boundaries, budget/stop rules, and score-hacking checks
- [ ] Assisted and independent performance are separated when external feedback or guided retry is used
- [ ] Nice-to-have runs are separated from must-run runs
```

#### `refine-logs/EXPERIMENT_TRACKER.md`

```markdown
# Experiment Tracker

| Run ID | Milestone | Claim ID | Expected Evidence ID / Locator | Purpose | System / Variant | Split / Region / Period | Metrics | Priority | Status | Output Path | Notes |
|--------|-----------|----------|--------------------------------|---------|------------------|-------------------------|---------|----------|--------|-------------|-------|
| R001   | M0        | C001     | E001 / run output              | sanity  | ...              | ...                     | ...     | MUST     | TODO   | ...         | ...   |
```

Keep the tracker compact and execution-oriented.

## Key Rules

- Every experiment must defend a Claim ID and expected Evidence ID / Locator that can be checked by `res_analyze`.
- Prefer a compact paper story over a giant benchmark wishlist.
- Prefer strong baselines over long baseline lists.
- Separate must-run from nice-to-have.
- Reuse proposal constraints; do not invent unrealistic budgets or data assumptions.
- Plan evidence; do not claim evidence.
- Detailed result interpretation belongs in `res_analyze`.
