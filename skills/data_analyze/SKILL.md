---
name: data_analyze
description: Execute or guide reproducible research data analysis from datasets to auditable tables, figures, diagnostics, scripts, and analysis reports.
---

Use subagents only when the user explicitly requests delegation; otherwise perform role checks locally.

# Research Data Analysis — Reproducible, Evidence-Oriented

Analyze research data from: **$ARGUMENTS**

## Role in the Research Workflow

`data_analyze` is the execution-stage data analysis skill. It turns raw, interim, or processed datasets into auditable analysis outputs: data audits, cleaning notes, exploratory summaries, statistical/model diagnostics, result tables, figures, scripts, and analysis reports.

Complete the requested operation only. Use the corresponding owner for a needed handoff within the user's authorized scope; these skills are not a mandatory stage chain.

Boundary:

- `res_plan` designs what evidence is needed.
- `data_analyze` reads, checks, transforms, analyzes, visualizes, and reports the data.
- `res_analyze` interprets completed analysis outputs as claim-evidence, uncertainty, limitations, and figure/table readiness.
- `evidence_audit` checks that data, scripts, commands, figures, tables, and claims are traceable and rerunnable.

## When to Use

Use `data_analyze` when the user asks to:

- analyze a CSV, Excel, Parquet, NetCDF, GeoTIFF, vector GIS file, model output, metrics table, or scenario result;
- inspect data quality, missingness, outliers, variable semantics, units, spatial/temporal extent, or sample structure;
- run or plan EDA, statistical tests, regression, GLM/GAM, mixed effects, time-series analysis, spatial analysis, optimization comparison, scenario comparison, sensitivity, uncertainty, or power/sample-size sanity checks;
- generate reproducible analysis scripts, tables, figures, diagnostics, and an analysis report;
- compare layouts, treatments, scenarios, baselines, models, methods, regions, periods, or ecological/energy/economic indicators.

Do not use `data_analyze` merely to polish manuscript text or judge whether a claim is manuscript-ready; route those to `nature-polishing`, `nature-reviewer`, or `res_analyze` as appropriate.

## Expected Inputs

Inspect available materials first:

- data paths or directories;
- research question, hypothesis, or comparison target;
- response variable, predictors, grouping variables, spatial unit, temporal unit, and units when available;
- existing notebooks, scripts, logs, model outputs, figures, or tables;
- constraints such as Python/R preference, no heavy dependencies, GIS software, remote-sensing workflow, privacy, licensed data, or runtime budget.

If the data path, schema, or analysis target is missing, produce a compact `AUTHOR_INPUT_NEEDED` checklist rather than inventing data or conclusions.

## Workflow

### Step 1: Data Intake and Audit

Identify:

- file format, row/column count, variables, data types, coordinate reference system, temporal range, and units when available;
- raw/interim/processed status and whether raw data must remain immutable;
- missing values, duplicated records, obvious impossible values, outliers, quality flags, class imbalance, spatial/temporal gaps, and license or access limits;
- whether the dataset can answer the stated question at the requested scale.

Stop or reframe when data are unreadable, schema is unclear, units are missing for key variables, or sample size/coverage cannot support the requested inference.

### Step 2: Cleaning and Preprocessing Plan

Specify or implement only necessary transformations:

- type conversion, unit harmonization, filtering, joins, aggregation, resampling, reprojection, normalization, feature construction, or missing-data handling;
- separation of raw, interim, processed, and derived outputs;
- provenance for every nontrivial transformation.

Never overwrite raw data. Do not silently drop records; record exclusion rules and counts.

### Step 3: Exploratory Data Analysis

Produce method-appropriate summaries:

- descriptive statistics, distributions, group summaries, trends, maps, correlations, pairwise relationships, and anomaly checks;
- sample size by group/region/period;
- preliminary plots that reveal data structure, not just publication graphics.

Mark EDA as exploratory unless a confirmatory design was specified before looking at the data.

### Step 4: Method Selection

Choose analysis methods from the data structure and question, not from keywords alone. Consider:

- tool selection: use the existing local environment first; use `pandas` for small/ordinary tables, optional `polars` lazy/streaming for large CSV/Parquet or multi-file ETL when installed or approved, and optional `statsmodels` when the question requires coefficient inference, OLS/GLM/discrete/mixed/time-series models, robust standard errors, residual diagnostics, or publication-ready statistical tables;
- group comparison: t-test, ANOVA, nonparametric alternatives, paired/repeated designs, multiple-comparison control;
- association and prediction: correlation, regression, GLM/GAM, regularized models, tree/boosting methods when justified;
- hierarchical data: mixed effects or clustered/blocked analysis;
- time series: autocorrelation, trend, seasonality, intervention, or forecasting diagnostics;
- spatial/GIS/remote sensing: CRS, scale mismatch, spatial autocorrelation, zonal statistics, raster/vector alignment, spatial cross-validation;
- scenario, layout, or optimization studies: baseline definition, objective functions, constraints, sensitivity, Pareto trade-offs, and robustness;
- Bayesian analysis only when priors, likelihood, diagnostics, and reporting boundaries can be stated.

If assumptions fail, propose or run an appropriate alternative instead of forcing a preferred test.

Do not install `polars`, `statsmodels`, or optional accelerators as hidden requirements. If they are absent and the analysis can proceed with existing tools, continue and record the tradeoff; if their absence changes correctness or feasibility, ask for approval or return `METHOD_NOT_IDENTIFIED`.

#### Small-Tabular Foundation Baseline Gate

For supervised classification or regression on a single flat table, consider a tabular foundation model such as TabPFN only as an optional rapid baseline, not as a default dependency or replacement for mature field baselines.

Run this eligibility gate before recommending or using such a model:

```markdown
| Dataset | Rows | Features | Task | TabPFN eligible? | Required baselines | Leakage / split risk | Decision |
|---------|------|----------|------|------------------|--------------------|----------------------|----------|
```

Eligibility requirements:

- the task is supervised classification or regression on structured tabular data;
- row count, feature count, class count, and hardware fit the selected checkpoint's documented limits;
- the train/test or cross-validation split is scientifically valid, with spatial, temporal, grouped, subject-level, or site-level leakage handled before model comparison;
- the analysis goal is quick feasibility screening, a strong small-data baseline, or model comparison, not causal identification or mechanism proof;
- XGBoost, CatBoost, LightGBM, random forest, linear/statistical, or other mature domain baselines remain planned when the result may support a paper claim.

If the model is actually run, record it like any other method:

```markdown
| Method | Version / checkpoint | Device | Split / CV | Metric | Runtime | Result locator | Caveat |
|--------|----------------------|--------|------------|--------|---------|----------------|--------|
```

Rules:

- Do not install `tabpfn`, use a hosted API, download model checkpoints, cache authentication tokens, or accept model licenses without explicit user approval.
- Treat TabPFN-style results as a baseline or exploratory signal until `res_analyze` and `evidence_audit` verify claim fit, leakage controls, environment, checkpoint, commands, and output locators.
- Do not generalize Nature / vendor benchmark claims beyond their stated dataset-size, task, hardware, and evaluation boundaries.
- For large tables, real-time inference, production latency, multi-table relational data, unstructured inputs, time-series dependence, spatial prediction, or causal claims, prefer the existing method-selection and diagnostic gates unless a project-specific validation justifies otherwise.

#### Candidate Search / Scored Iteration Ledger

Use this ledger when `res_plan` marks an analysis block as a scorable task, or when the user asks for automated method search, repeated code/model improvement, hyperparameter or architecture search, candidate recombination, LLM-assisted code generation, or score-driven optimization.

The ledger is not required for ordinary one-shot statistics, EDA, baseline fitting, or deterministic data cleaning.

```markdown
| Candidate ID | Parent / source idea | Intervention type | Code / config locator | Application status / proof | Dataset split | Quality score | Baseline delta | Runtime / total cost | Failure or warning | Next action |
|--------------|----------------------|-------------------|-----------------------|----------------------------|---------------|---------------|----------------|----------------------|--------------------|-------------|
```

Rules:
- Record failed, excluded, and low-scoring candidates when they affect the interpretation of the winning result.
- Classify `Intervention type` as `parameter/config`, `search-mechanism/control-flow`, `metric/evaluator`, or `environment/tool`. Repeated proposals, no new evidence, parameter fixation, or metric saturation require cause diagnosis before another search round; they do not automatically justify a mechanism-level change.
- A mechanism-level candidate is eligible only when the metric/evaluator and immutable artifacts are frozen, the baseline is reproducible, and a rollback target exists. Generated code, prompts, skills, or patches count as applied only when a diff/hash/snapshot/load log proves activation before the scored result; otherwise mark them reverted or invalid.
- Keep search/training, validation, and holdout scores separate; never select on a holdout set and then report it as independent evidence.
- Do not treat a score gain as a mechanism, causal, or general scientific claim until `res_analyze` and `evidence_audit` check the evidence boundary.
- If candidates are recombined from prior methods or literature summaries, record their parent/source idea and hand the provenance to `evidence_audit`.
- For tree search, UCB/PUCT-style selection, beam search, best-of-N, retry loops, or other branch-and-score procedures, record the search policy, parent-selection rationale, recombination parent(s), manual filtering, and saturation or stop rule; do not report only the winning candidate.
- Report total search cost when material, including runtime, compute, LLM/API use, and human filtering. Equal inner-evaluation counts do not establish equal total compute or efficiency.
- Stop or return to `res_plan` if the metric is unstable, leaks future/label information, rewards a shortcut, or lacks a meaningful baseline.

### Step 5: Diagnostics, Effect, and Uncertainty

Where applicable, check and report:

- normality, variance homogeneity, independence, residual patterns, leverage/influence, multicollinearity, autocorrelation, spatial autocorrelation, missingness mechanism, and model convergence;
- effect size or magnitude, confidence/credible intervals, variability, uncertainty bands, and sensitivity to thresholds or preprocessing choices;
- power or sample-size sanity check when null results, small samples, or underpowered comparisons would affect interpretation.

Avoid presenting p-values without effect magnitude and uncertainty when the claim depends on practical or ecological importance.

### Step 6: Generate Tables, Figures, Scripts, and Report

Default output location when writing project artifacts is authorized:

```text
results/data_analysis/
├── DATA_AUDIT.md
├── ANALYSIS_PLAN.md
├── ANALYSIS_REPORT.md
├── STATISTICAL_DIAGNOSTICS.md
├── ANALYSIS_RUN_MANIFEST.md
├── tables/
├── figures/
├── scripts/
└── logs/
```

Use lightweight scripts or notebooks as appropriate, but paper-critical results should have a rerunnable script, command, or frozen notebook with documented environment assumptions.

## Output Contracts

### `DATA_AUDIT.md`

```markdown
# Data Audit

## Inputs Reviewed
| Path | Format | Role | Rows / Size | Key Variables | Notes |
|------|--------|------|-------------|---------------|-------|

## Schema and Semantics
| Variable | Type | Unit | Meaning | Missing | Quality Issue |
|----------|------|------|---------|---------|---------------|

## Fitness for Question
- Question:
- Supported scale:
- Unsupported scale or claim:
- Decision: PROCEED / REFRAME / AUTHOR_INPUT_NEEDED / STOP
```

### `ANALYSIS_PLAN.md`

```markdown
# Analysis Plan

| Step | Purpose | Input | Method / Tool | Output | Decision Gate |
|------|---------|-------|---------------|--------|---------------|
```

### `STATISTICAL_DIAGNOSTICS.md`

```markdown
# Statistical and Model Diagnostics

| Analysis | Assumption / Diagnostic | Result | Decision | Alternative if Failed |
|----------|-------------------------|--------|----------|-----------------------|
```

### `ANALYSIS_RUN_MANIFEST.md`

```markdown
# Analysis Run Manifest

| Step | Input | Script / Command | Output | Status | Notes |
|------|-------|------------------|--------|--------|-------|
```

### `CANDIDATE_SEARCH_LEDGER.md`

Create this only for scorable-task or score-driven candidate-search analyses:

```markdown
# Candidate Search Ledger

## Search Boundary
- Claim / block:
- Metric:
- Search split:
- Validation split:
- Holdout boundary:
- Budget / stop rule:
- Stagnation / saturation criterion:
- Fixed evaluator / immutable artifacts:
- Allowed intervention levels:
- Search policy / parent-selection rule:
- Recombination or branch-source rule:

| Candidate ID | Parent / source idea | Intervention type | Code / config locator | Application status / proof | Dataset split | Quality score | Baseline delta | Runtime / total cost | Failure or warning | Next action |
|--------------|----------------------|-------------------|-----------------------|----------------------------|---------------|---------------|----------------|----------------------|--------------------|-------------|

## Selection Note
- Selected candidate:
- Why selected:
- Application-integrity evidence:
- Absolute baseline / final metric, uncertainty, and total search cost:
- Why this does not by itself prove a mechanism or broad scientific discovery:
```

### `ANALYSIS_REPORT.md`

```markdown
# Analysis Report

## Question and Data

## Data Quality and Preprocessing

## Exploratory Findings

## Methods Used and Why

## Results
| Result ID | Output | Statistic / Metric | Effect / Uncertainty | Table / Figure | Script / Command |
|-----------|--------|--------------------|----------------------|----------------|------------------|

## Diagnostics and Robustness

## Limits Before `res_analyze`

## Handoff to `res_analyze`
| Evidence ID / Locator | Output Path | Candidate Claim | Boundary Condition | Missing Check |
|-----------------------|-------------|-----------------|--------------------|---------------|
```

## Failure Codes

Use explicit failure or return codes:

- `DATA_NOT_READABLE`
- `DATA_SCHEMA_UNCLEAR`
- `AUTHOR_INPUT_NEEDED`
- `INSUFFICIENT_SAMPLE_SIZE`
- `METHOD_NOT_IDENTIFIED`
- `TABPFN_NOT_ELIGIBLE`
- `OPTIONAL_DEP_NOT_APPROVED`
- `LICENSE_OR_LOGIN_BOUNDARY`
- `LEAKAGE_RISK_UNRESOLVED`
- `SCORABLE_TASK_NOT_ELIGIBLE`
- `SEARCH_METRIC_UNSTABLE`
- `SEARCH_STAGNATION_UNDIAGNOSED`
- `MECHANISM_APPLICATION_UNVERIFIED`
- `SEARCH_COST_BOUNDARY_MISSING`
- `HOLDOUT_CONTAMINATION_RISK`
- `CANDIDATE_LEDGER_MISSING`
- `BASELINE_COMPARISON_INCOMPLETE`
- `ASSUMPTION_FAILED_NEEDS_ALTERNATIVE`
- `RESULT_NOT_REPRODUCIBLE`
- `CLAIM_REQUIRES_RES_ANALYZE`
- `RETURN_TO_RES_PLAN`

## Key Rules

- Do not fabricate data, rows, statistics, p-values, effect sizes, maps, model outputs, or significance.
- Do not overwrite raw data; write derived outputs separately.
- Prefer the smallest analysis that answers the question; do not add Airflow, Kedro, DVC, MLflow, Spark, or cloud infrastructure as default requirements.
- Use heavy tools only when the dataset or project already requires them and the user accepts the dependency.
- Do not install packages, upload data to external services, or use cloud/agent-based processing for private, licensed, or sensitive datasets without explicit user approval. Prefer existing local environments and record any dependency changes.
- Treat tabular foundation models as optional baselines with explicit eligibility, leakage, license, checkpoint, device, and reproducibility records; never make them hidden defaults.
- Keep exploratory and confirmatory analysis distinct.
- Preserve paths, commands, and assumptions so `evidence_audit` can audit them.
- Send completed analysis outputs to `res_analyze` for claim-evidence interpretation before manuscript writing.
