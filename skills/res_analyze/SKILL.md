---
name: res_analyze
description: Analyze experiment outputs, observations, model comparisons, and figure-ready environmental-science evidence.
---

Use subagents only when the user explicitly requests delegation; otherwise perform role checks locally.

Analyze research results from: **$ARGUMENTS**

## Role in the Research Workflow

`res_analyze` is the Review & Analysis-stage evidence organizer. It turns completed analysis outputs into paper-ready claim evidence, uncertainty notes, limitations, and figure/table plans.

It does not own primary data cleaning, exploratory analysis, statistical/model execution, or figure/table generation. Use `data_analyze` first when datasets still need to be read, audited, transformed, analyzed, visualized, or reported.

Complete the requested operation only. Use the corresponding owner for a needed handoff within the user's authorized scope; these skills are not a mandatory stage chain.

## Expected Inputs

Inspect available materials first:

- `refine-logs/FINAL_PROPOSAL.md`
- `refine-logs/EXPERIMENT_PLAN.md`
- `refine-logs/EXPERIMENT_TRACKER.md`
- `experiments/<timestamp>_<topic>_attempt_k>/`
- completed `data_analyze` outputs such as `results/data_analysis/ANALYSIS_REPORT.md`, `DATA_AUDIT.md`, `STATISTICAL_DIAGNOSTICS.md`, `ANALYSIS_RUN_MANIFEST.md`, tables, figures, or scripts
- result CSV/JSON/NetCDF/GeoTIFF/statistical outputs
- model logs, analysis notebooks, map outputs, or figure drafts
- user-provided observation summaries or tables

If no usable result evidence exists, produce a missing-results checklist instead of inventing findings. If the blocker is missing data execution rather than result interpretation, return to `data_analyze`.

## Workflow

### Step 1: Locate and Classify Evidence

Group files by:
- run or experiment block
- dataset / region / temporal period
- baseline or model variant
- metric or response variable
- figure/table target
- claim tested

### Step 2: Build Comparison Tables

For each relevant claim, organize:
- primary metric or environmental indicator
- baseline and comparator systems
- effect size, uncertainty, confidence interval, or variability where available
- spatial/temporal pattern
- sensitivity or robustness result
- missing or failed runs

### Step 3: Interpret Results Conservatively

For every finding, separate:

1. **Observation** — what the data show, with numbers or file references
2. **Interpretation** — plausible scientific or methodological explanation
3. **Claim support** — which claim is supported, weakened, or unresolved
4. **Uncertainty** — data quality, scale mismatch, sampling, model assumptions, stochastic variance
5. **Next check** — follow-up analysis needed before paper writing

Do not upgrade correlation, map pattern, or model performance into mechanism unless the evidence supports it.

### Step 4: Produce Figure and Table Readiness Notes

For each candidate figure/table:
- purpose in the paper argument
- data provenance path
- plot type or professional software workflow
- minimum annotation needed
- whether it is main-paper, supplementary, or not ready
- missing analysis before final plotting

### Step 5: Legacy Claim Matrix Migration

If an existing project already has an older claim table such as `| Claim | Evidence | Strength | Figure/Table | Missing Check | Risk |`, do not discard it. Upgrade it minimally before downstream writing, figure freeze, or reproducibility review:
- preserve the original claim and evidence wording
- add stable or provisional `Claim ID` values
- add `Evidence ID / Locator` only when a real source, row, file, page, figure, table, or output locator exists
- add `Source / Output Path`, `Analysis provenance path`, `Figure/Table target`, and `Boundary condition`
- mark missing locators, provenance paths, and boundary conditions as blockers instead of inventing them

The migrated matrix should match the canonical Claim Support Matrix structure below before `evidence_audit` builds `ARTIFACT_MANIFEST.md`.

### Step 6: Reviewer-Style Evidence Gate

Check:
- Does the result answer the scientific question?
- Does each main claim have direct evidence?
- Are baselines and mature field standards sufficient?
- Are negative or ambiguous results acknowledged?
- Are uncertainty and limitations explicit?
- Does the interpretation clarify a flexible `So what?` significance layer rather than merely reporting an effect or significant change?
- Is cross-domain transfer validated or still assumed?

## Canonical Outputs

Write or propose files under `results/analysis/`:

```text
results/analysis/
├── ANALYSIS_SUMMARY.md
├── CLAIM_SUPPORT_MATRIX.md
├── FIGURE_TABLE_PLAN.md
└── LIMITATIONS_AND_UNCERTAINTY.md
```

Use this structure for `ANALYSIS_SUMMARY.md`:

```markdown
# Analysis Summary

## Inputs Reviewed

## Key Findings

## Claim Support Matrix
| Claim ID | Claim | Evidence ID / Locator | Source / Output Path | Analysis provenance path | Strength | Figure/Table target | Boundary condition | Missing check | Risk |
|----------|-------|-----------------------|----------------------|--------------------------|----------|---------------------|--------------------|---------------|------|

## Baseline / Comparator Summary

## Spatial and Temporal Patterns

## Uncertainty and Limitations

## Figure and Table Readiness

## Evidence Gaps Before `nature-writing`
```

## Key Rules

- Do not fabricate results or statistical significance.
- Preserve data provenance paths and carry forward Claim ID / Evidence ID / Locator from `res_plan` when available.
- Mark weak, ambiguous, or failed results explicitly.
- Separate observation from interpretation.
- Do not polish into manuscript prose here; `nature-writing` handle paper structure and drafting.
- Prefer a compact set of paper-critical findings over exhaustive log summaries.
