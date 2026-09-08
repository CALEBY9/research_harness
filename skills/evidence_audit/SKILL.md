---
name: evidence_audit
description: Evidence audit and reproducibility gate for environment-science claims, data, code, experiments, figures, manifests, and submission packages; formerly code_repro.
version: 2.0.1
---

Use subagents only when the user explicitly requests delegation; otherwise perform role checks locally.

# Research Evidence Audit — 环境科学

Audit the evidence chain and reproducibility of a research project from: **$ARGUMENTS**

## Role in the Research Workflow

`evidence_audit` is the evidence-chain, artifact, and reproducibility gate across execution, analysis, paper writing, and submission. It should ensure that claims, data, code, figures, tables, results, and availability statements can be traced, audited, and rerun when needed.

Compatibility: if the user or an older workflow note says `code_repro`, treat it as the old name for `evidence_audit`.

Use it for the requested audit of analysis, figures, or manuscript evidence. Coordinate with `data_analyze`, `res_analyze`, `nature-figure`, `nature-writing`, or `nature-reviewer` only where an identified issue needs that owner. Do not run a figure or paper-production chain merely to perform an audit.

For empirical, computational, or figure-bearing manuscripts, `evidence_audit` is the final evidence and artifact-manifest gate before submission packaging.

## Audit Scope and Handoff

- Required inputs: requested object, canonical source/artifact, available evidence locators, and read-only or artifact-write scope. Infer these from the request and project records when clear.
- Focused audits cover the named claim, figure, run, or section and its necessary upstream evidence. Computational content or AI assistance alone does not expand the task to the whole manuscript.
- Final submission evidence closeout requires the Final Claim Coverage gate for the complete in-scope final manuscript and artifacts. Explicit all-claim or Chain-of-Evidence requests also use it within the requested scope, including on drafts. A focused audit cannot certify whole-manuscript readiness.
- Report the object, performed checks, evidence locators, verdicts, unchecked scope, and actionable blockers. Reuse project records; paths below are defaults, not instructions to migrate directories. Do not create full-manuscript ledgers for focused work.
- Read-only requests produce findings without editing manuscript or project files. Artifact writes and reruns remain within task authorization; inaccessible evidence or an unperformed rerun stays explicitly unverified.
- Later gates and checklist items inherit this scope and their stated conditions. A blocker prevents the affected claim or final closeout; continue independent in-scope checks and hand unresolved work to its owner.

## Core Principles

| Principle | Requirement |
|-----------|-------------|
| Provenance first | Every claim, figure, and table should trace to data, code, and run outputs |
| Re-runnable workflow | Key results can be regenerated from documented commands or scripts |
| Stable artifacts | Important outputs have paths, versions, checksums or timestamps where useful |
| Open formats | Prefer NetCDF, GeoTIFF, CSV, Parquet, JSON, Markdown, LaTeX |
| Environment capture | Record Python/R/GIS/software versions and system assumptions |
| Honest availability | Do not claim public availability for restricted or licensed data |

## Canonical Project Artifacts

Recommended structure:

```text
project/
├── data/
│   ├── raw/                 # immutable source data or retrieval manifests
│   ├── interim/             # intermediate processing outputs
│   └── processed/           # analysis-ready datasets
├── experiments/
│   └── <timestamp>_<topic>_attempt_k>/
│       ├── RUN_MANIFEST.md
│       ├── config.json
│       ├── logs/
│       ├── metrics.csv
│       └── outputs/
├── results/
│   ├── data_analysis/        # data_analyze execution-stage outputs
│   ├── analysis/             # res_analyze claim-evidence outputs
│   ├── review/
│   └── review_package/
├── paper/
│   ├── PAPER_PLAN.md
│   ├── sections/
│   ├── figures/
│   ├── references.bib
│   └── main.tex
├── scripts/ or src/
├── pyproject.toml / requirements.txt / environment.yml
└── README.md
```

## Data Standards

### File Formats

| Data Type | Preferred Format | Notes |
|-----------|------------------|-------|
| Gridded climate / remote sensing | NetCDF, Zarr, GeoTIFF | Include CRS, resolution, time axis |
| Vector geospatial data | GeoPackage, GeoJSON, Shapefile only if needed | Include CRS and topology notes |
| Tables / metrics | CSV, Parquet | Include units and missing-value codes |
| Configuration | JSON, YAML, TOML | Version with runs |
| Figures | PDF/SVG for vector, PNG/TIFF for raster | Store source data when possible |

### Metadata Checklist

Each dataset should document:
- source and access date
- license or use restriction
- spatial extent and CRS
- temporal extent and resolution
- variables, units, missing-value codes
- preprocessing history
- uncertainty or quality flags
- script or command that generated it

## Run Manifest Template

For important in-scope runs, inspect the existing run manifest or create `RUN_MANIFEST.md` when artifact writes are authorized:

````markdown
# Run Manifest

## Run ID

## Scientific Claim Tested

## Input Data
| Path | Source | Version / Date | Role |
|------|--------|----------------|------|

## Configuration
- Config path:
- Random seed, if applicable:
- Model / method version:
- Software versions:

## Command or Workflow
```bash
# command used to reproduce the run
```

## Outputs
| Output | Path | Used For | Included in Paper |
|--------|------|----------|-------------------|

## Known Issues

## Reproduction Status
[Not rerun / Rerun passed / Rerun differs / Not reproducible]
````

## Artifact Manifest Template

For paper-ready outputs, create `results/review_package/ARTIFACT_MANIFEST.md`. This is the evidence handoff from analysis, figures, writing, review, and reproducibility into submission-package work owned by `nature-writing`:

```markdown
# Artifact Manifest

## Claims
| Claim ID | Claim | Verification Channel | Evidence ID / Locator | Source / Output Path | Figure/Table ID | Manuscript Location | Reproduction Command | Verification Method | Verification Verdict | Status | Blocker |
|----------|-------|----------------------|-----------------------|----------------------|-----------------|---------------------|----------------------|---------------------|----------------------|--------|---------|

## Figures
| Figure ID | Claim ID | Evidence ID / Locator | Figure Class | figure_spec.yml | Source Data / Base Layer | Script / Software | Output Path | Visual QA | Caption / Body Location | Provenance Complete | Status |
|-----------|----------|-----------------------|--------------|-----------------|--------------------------|-------------------|-------------|-----------|-------------------------|---------------------|--------|

## Tables
| Table ID | Claim ID | Evidence ID / Locator | Source Data | Script / Software | Output Path | Manuscript Location | Provenance Complete | Status |
|----------|----------|-----------------------|-------------|-------------------|-------------|---------------------|--------------------|--------|

## Revision and Review Trace
| Comment ID | Manuscript Change | Claim ID | Evidence ID / Locator | Artifact / Figure / Table | Response Status |
|------------|-------------------|----------|-----------------------|---------------------------|-----------------|

## Data and Code Availability
- Public data:
- Restricted data:
- Generated data:
- Code repository:
- Archive DOI:
- Availability boundaries:

## Workflow Dependency Trace
| Node ID | Node Type | Depends On | Produces | Linked Claim ID | Reproducibility Status | Blocker |
|---------|-----------|------------|----------|-----------------|------------------------|---------|

## AI Research Failure Mode Audit
| Claim / Result | Failure Mode Checked | Evidence / Run Locator | Verdict | Required Fix |
|----------------|----------------------|------------------------|---------|--------------|

## Search-Derived Result Audit
| Claim / Result | Search ledger | Search policy / stop rule | Intervention / application proof | Selection split | Independent validation / holdout | Baseline reproduction | Total search cost | Failed / excluded candidates documented | Score-hacking, leakage, or metric-framing risk | Verdict | Required Fix |
|----------------|---------------|---------------------------|----------------------------------|-----------------|----------------------------------|-----------------------|-------------------|-----------------------------------------|------------------------------------------------|---------|--------------|
```

Use `Workflow Dependency Trace` when flat artifact tables are not enough to explain how source data, preprocessing, analysis, figure generation, and manuscript claims depend on each other. Keep it lightweight: add only nodes needed to diagnose reproducibility or submission blockers.

## Missing Artifact Manifest Gate

If a submission package lacks `results/review_package/ARTIFACT_MANIFEST.md`, complete the manifest within the requested artifact-write scope, or report the missing traceability in read-only mode. This blocks submission-readiness certification, not ordinary manuscript drafting.

Minimum skeleton rows should be built from existing materials, not invented:
- reuse existing claim labels when available; otherwise assign provisional `C###` IDs and mark them as provisional
- map each claim to known Evidence ID / Locator, source or output path, figure/table ID, manuscript location, and reproduction command
- mark unknown evidence, provenance, manuscript locations, or commands as `Blocker` / `AUTHOR_INPUT_NEEDED`
- preserve legacy claim-matrix wording if needed, but add the missing traceability columns before submission readiness

## Final Claim Coverage / Cross-Modal Consistency Gate

Use this gate under Audit Scope and Handoff. Full final evidence closeout requires it; ordinary focused audits do not acquire a whole-manuscript ledger.

Before final verification closeout, identify every atomic externally verifiable claim in the final manuscript, captions, tables, and availability statements, including claims that never received a Claim ID upstream. Record the audit in `results/review_package/ARTIFACT_MANIFEST.md` or the reproducibility report:

```markdown
| Claim ID | Final Manuscript Locator | Atomic Claim | Verification Channel | Declared Citation / Artifact | Source / Code / Config / Run / Output Locator | Verification Performed | Verdict | Allowed Boundary | Required Action |
|----------|--------------------------|--------------|----------------------|------------------------------|------------------------------------------------|------------------------|---------|------------------|-----------------|
```

Dispatch verification by channel:

- `citation`: verify source identity and whether source text supports the specific assertion. Metadata, title, or abstract-only access cannot by itself produce `PASS`; use `ACCESS_LIMITED` or `INCONCLUSIVE` when claim-level source text cannot be checked.
- `numerical`: match the exact value, metric, unit, split, selected run or candidate, tolerance, and canonical output; rerun or recompute when the claim depends on executable artifacts.
- `methodological`: map each material method, formula, or algorithm statement to a code symbol, config, commit or version, run, log, or output. A material method-code contradiction is `BLOCK`; omitted implementation detail is acceptable only when it does not change the stated method or reproducibility.
- `derived conclusion`: trace the conclusion to upstream claims and reasoning. Only `ADMIT` or `DOWNGRADE_WITH_BOUNDARY` claims may support it; dependence on `HOLD_FOR_EVIDENCE` or `REJECT_OR_REMOVE` is `BLOCK`.

Apply four cross-cutting checks, where applicable, regardless of verification channel:

- `canonical final-artifact integrity`: when a submission DOCX/PDF is generated or assembled from LaTeX, Markdown, a builder, or staged source files, compare the canonical final artifact with a clean rebuild or a structural inventory of paragraphs, sections, tables, media relationships, and figure hashes. Any unexplained orphan text, extra image/table, stale figure, or manual tail insertion is `BLOCK`.
- `version coherence`: every manuscript claim must resolve to the declared canonical dataset, run, candidate, or an explicit version-boundary/join manifest. Silently mixing branches, or using a later prompt/code rule to describe an earlier output that was not rerun under that rule, is `BLOCK`.
- `validation-actor provenance`: verify whether each rater, reviewer, annotator, or adjudicator was a human, expert, model, agent, or mixed process, and require the corresponding returned artifact or signoff. Model/agent passes must not be described as human or expert validation; an actor-identity contradiction is `BLOCK`.
- `equation semantic integrity`: for formula-bearing submission or proof artifacts, require the exact ledger defined in `../shared-references/equation-semantic-integrity-gate.md`. Reconcile displayed equation count/number, exact symbol sets, first-use/local definitions, aliases, units, cross-references, model/code/config locators, and current artifact hashes. A stale ledger, unparsed equation, or material formula-model contradiction is `BLOCK`; successful extraction or rendering alone is not evidence of correctness.

For formula-bearing closeout, run `python <skill-directory>/../shared-references/scripts/equation_semantic_gate.py <ledger.json> --verify-files` with resolved active-platform paths and record the command/result. The script checks ledger structure and, with this flag, artifact files/hashes. Populated symbol lists or a model locator do not prove equation-to-source/model semantics; inspect those correspondences separately and record evidence before claiming semantic PASS. Unresolved manual review still blocks closeout.

In production proof mode, compare the exact accepted author source against the exact production proof and classify every requested correction as `PUBLISHER_ERROR`, `OBVIOUS_AUTHOR_ERROR`, `CLARITY_CORRECTION`, `SCIENTIFIC_DECISION_REQUIRED`, or `MODEL_OR_RESULTS_CHANGE`. Only the first three may be locally applied within an authorized editing task when a unique authoritative basis exists and model behavior/results remain unchanged. The last two require author decision and editor approval and prevent final closeout while unresolved.

For each claim's verification verdict, use only `PASS`, `PARTIAL`, `INCONCLUSIVE`, `ACCESS_LIMITED`, `BLOCK`, or `NOT_APPLICABLE`. `No flagged violation` is not equivalent to verified clean when the check was not run, the evidence is inaccessible, a known blind spot remains, or false-negative risk is unbounded.

Keep verification verdict, claim disposition, and workflow return code separate. The claim table's `Status` records `ADMIT`, `DOWNGRADE_WITH_BOUNDARY`, `HOLD_FOR_EVIDENCE`, or `REJECT_OR_REMOVE`. A numerical PASS does not admit a causal or mechanism claim: all applicable evidence channels must support the actual wording. `PARTIAL`, `INCONCLUSIVE`, or `ACCESS_LIMITED` require a demonstrably supported narrower claim or HOLD; cautious prose alone does not supply evidence. Risk-table `WARN` records a checked non-blocking concern with its impact/boundary; it cannot conceal a claim-level BLOCK or an unperformed required check. Return codes name the next action/owner, not an evidence verdict.

Build coverage from final-artifact locations before reconciling the ledger. Split independently verifiable assertions, such as a reported difference and its causal explanation. Repeated wording may share a Claim ID, but record/check every occurrence; different populations, versions, values, or strengths are separate claims. Enumerate numerical table entries by cell or an explicitly indexed batch checking every included cell. Report unique-claim and occurrence/cell counts separately, with exclusions and reasons, so batching cannot hide omissions. Reconcile added, changed, and removed occurrences after final-artifact edits.

Close with a coverage reconciliation using the declared counting unit:

```text
in_scope / tagged / pass / partial / inconclusive / access_limited / blocked / excluded_with_reason
```

The `in_scope` denominator is all atomic externally verifiable claims, not only claims already present in the ledger. Any unregistered in-scope claim is a coverage failure. A 100% coverage figure means only that the declared denominator was checked; it must not be described as zero hallucination, scientific correctness, novelty, or complete absence of audit misses.

Unsupported claims remain visible as `BLOCK`, `HOLD_FOR_EVIDENCE`, or `REJECT_OR_REMOVE`; do not silently delete them during audit. Internal claim IDs, evidence tags, verdicts, and coverage notes stay in author-side artifacts and must not leak into the clean final manuscript.

Any `BLOCK` or unregistered in-scope claim prevents final evidence closeout and returns to `nature-reviewer`, `res_analyze`, `data_analyze`, or the relevant owner skill. `PARTIAL`, `INCONCLUSIVE`, and `ACCESS_LIMITED` cannot support an unbounded strong claim unless the wording is downgraded and the boundary is explicit.

## Methods and Submission Blocker Gate

Before final reproducibility or submission readiness, scan the manuscript methods, supplements, analysis notes, and submission checklist for unresolved blockers that affect reproducibility or claim validity:
- inclusion/exclusion protocol, search query, database coverage, and de-duplication method
- model, prompt, batch, reviewer, audit, or validation protocol details
- restrictions such as SCIE/Q1 filters, domain coverage, source-attribution boundaries, or human-validation boundaries
- figure-generation commands, final figure versions, caption/body references, and table provenance
- data/code availability statements, repository DOI, license, and redistribution boundaries

If any blocker remains, return `RETURN_TO_EVIDENCE_AUDIT` or `RETURN_TO_PAPER_REVIEW` instead of polishing or packaging the manuscript.

## AI Research Failure Mode Gate

Use this gate for empirical, computational, statistical, optimization, model, or figure-bearing manuscripts before final submission readiness. It is a reproducibility check, not a manuscript-style review.

Check these failure modes:

| Failure mode | What to check | Blocking condition |
|--------------|---------------|--------------------|
| Implementation bug accepted as result | Paper-critical numbers trace to scripts/logs/notebooks with successful exits, expected inputs, and inspected warnings. Assess effects on inputs, sample inclusion, algorithm execution, convergence, and results. | No run locator, crashed run, wrong input, uninspected anomaly, or unresolved warning with material or unknown impact supports a claim. A warning is non-blocking only with evidence that it does not affect the claim. |
| Hallucinated or orphan result | Every reported effect size, percentage, ranking, map class, scenario result, or table value maps to raw/intermediate output. | The manuscript number cannot be recomputed or located in saved outputs. |
| Shortcut reliance / leakage | The result cannot be explained by an easier shortcut, data leakage, spatial/temporal leakage, proxy leakage, or stronger baseline omission. | No negative control, leakage check, or baseline audit exists for a central performance/mechanism claim. |
| Bug reframed as insight | Surprising findings from fragile/debugging runs require independent reproduction or recomputation. Literature expectations inform interpretation but do not substitute for execution checks. | A surprising result from a fragile/debugging run is written as a finding without reproduction. |
| Claim stronger than provenance | Manuscript wording matches what the reproducibility artifacts actually establish. | The artifact supports an association, ranking, or suitability result, but the text claims causality, mechanism, or general law. |

Output a compact `AI Research Failure Mode Audit` table in `ARTIFACT_MANIFEST.md` or the reproducibility report. Use `PASS`, `WARN`, `BLOCK`, or `NOT_APPLICABLE` verdicts. Any `BLOCK` must return to `data_analyze`, `res_analyze`, `nature-reviewer`, or the relevant figure skill before polish or submission packaging.

## Search-Derived Result Audit

Use this gate when a reported result comes from a scorable task, automated method search, repeated code/model improvement, hyperparameter or architecture search, LLM-assisted code generation, candidate recombination, or score-driven optimization.

Check these risks before the result supports a manuscript claim:

| Risk | What to check | Blocking condition |
|------|---------------|--------------------|
| Score hacking | The quality metric measures the scientific target rather than an exploitable proxy. | The winning candidate optimizes the metric while violating the scientific question, constraints, or deployment boundary. |
| Validation overfit | Search/training, validation, and holdout evidence are separated. | The same split was used to select, tune, and claim independent performance. |
| Candidate cherry-picking | Failed, excluded, and low-scoring candidates are visible enough to interpret the winner. | Only the best result is shown while search breadth, failures, or exclusions are hidden. |
| Recombination provenance gap | Parent methods, literature summaries, or prior candidates are traceable. | A hybrid or recombined method is reported without source/parent idea locators. |
| Search policy opacity | Candidate selection policy, parent-selection rationale, branch or backtrack provenance, manual filtering, and stop or saturation rule are recorded when a search procedure was used. | The winner is reported without enough information to understand how candidates were selected, branched, recombined, filtered, or stopped. |
| Mechanism application gap | A claimed mechanism or control-flow change is present in the active artifact, passed the relevant validation, and was activated before the scored improvement; diff/hash/snapshot/load-log evidence is traceable. | The mechanism was only proposed or generated, the active artifact stayed unchanged, validation failed or silently fell back, or the gain occurred before activation. |
| Baseline reproduction gap | Mature baselines or initial solutions were rerun or otherwise fairly compared. | The gain is claimed against a baseline that was not reproduced, versioned, or comparably evaluated. |
| Search cost boundary missing | Runtime, compute, LLM/API use, human filtering, and stop rule are recorded when material. | The result depends on a large hidden search budget or manual filtering that is absent from methods or limitations. |
| Metric-delta framing | Multiplicative improvement claims report the absolute baseline and final metric, denominator, repeats/uncertainty, metric meaning, and total search cost. | A ratio of small deltas is described as overall performance, speed, efficiency, or general capability without the absolute values, uncertainty, or cost boundary. |

Output a compact `Search-Derived Result Audit` table in `ARTIFACT_MANIFEST.md` or the reproducibility report. Use `PASS`, `WARN`, `BLOCK`, or `NOT_APPLICABLE`. A score gain alone supports only an empirical-software or model-selection claim until `res_analyze` or `nature-reviewer` justifies a mechanism, causal, or broad scientific claim. Any `BLOCK` on mechanism application invalidates attribution to that mechanism even when the score improved; equal inner-evaluation counts do not establish equal total compute or efficiency.

## Environment Capture

Minimum:
- Python/R version
- package lock file (`uv.lock`, `requirements.txt`, `renv.lock`, or `environment.yml`)
- major external software versions: ArcGIS/QGIS/ENVI/SNAP/GEE/GDAL/CDO/NCO as relevant
- operating system if relevant
- GPU/CPU only when computational results depend on hardware

## Data and Code Availability Templates

### Public Data

```text
Data availability: The public datasets used in this study are listed in Supplementary Table X with source, version, access date, and license. Processed data required to reproduce the main figures are available at [repository/DOI].
```

### Restricted Data

```text
Data availability: [Dataset] is subject to [license/access restriction] and cannot be redistributed by the authors. The processing workflow and derived non-restricted outputs needed to reproduce the reported analyses are available at [repository/DOI], subject to the stated data-use conditions.
```

### Code

```text
Code availability: Code used for data processing, analysis, and figure generation is available at [repository/DOI], with environment files and run manifests for the main analyses.
```

## Final Reproducibility Checklist

Select applicable items under Audit Scope and Handoff and record exclusions with reasons. Full final evidence closeout retains every applicable requirement below.

### Data
- [ ] Raw or source-data retrieval path is documented
- [ ] Processed data can be regenerated or is archived
- [ ] Metadata includes units, CRS, time range, missing values, and license
- [ ] Restricted data are clearly marked

### Code and Environment
- [ ] Main commands or notebooks are documented
- [ ] Dependencies and software versions are recorded
- [ ] Random seeds are fixed when stochastic components matter
- [ ] Hard-coded local paths are removed or parameterized

### Experiments
- [ ] Each key run has a manifest
- [ ] Main baselines and final method outputs are traceable
- [ ] Failed or excluded runs are documented
- [ ] Metrics can be recomputed from saved outputs
- [ ] Claimed mechanism/intervention application is proven by changed active artifacts and activation/validation logs before the reported gain
- [ ] Multiplicative improvement claims include absolute metrics, uncertainty, denominator, and total search cost
- [ ] AI research failure modes have been checked for paper-critical results

### Paper Evidence
- [ ] Each claim maps to Claim ID, Evidence ID / Locator, source/output path, and manuscript location
- [ ] All atomic externally verifiable final claims are counted in the coverage denominator; unregistered or orphan claims are flagged
- [ ] Citation, numerical, methodological, and derived-conclusion claims use the matching verification rule and verdict
- [ ] Method, formula, and algorithm claims map to code/config/version/run/output locators or an explicit evidence boundary
- [ ] Every displayed equation is present in a current equation ledger with exact symbol/local-definition parity, canonical notation, units, numbering/cross-references, and model/code locator where applicable
- [ ] Equation-ledger source hashes match the current manuscript, supplement, model/config, and production proof; no post-audit edit remains unreviewed
- [ ] Proof corrections are classified by source and scientific impact; no scientific-decision or model/results change is silently applied
- [ ] The canonical final DOCX/PDF matches its declared source/build and contains no unexplained orphan text, media, tables, sections, or stale figures
- [ ] Claims use one declared canonical dataset/run/candidate, or an explicit version-boundary/join manifest documents every mixed branch
- [ ] Human/expert/reviewer/annotator wording matches actor provenance and a returned review or signoff artifact
- [ ] Coverage reporting distinguishes `no flagged violation` from verified `PASS` and does not equate 100% coverage with zero hallucination
- [ ] Each figure/table maps to Claim ID, Evidence ID / Locator, source data or base layer, and script/software
- [ ] Main or submission figures include `figure_spec.yml`, render log, provenance, and `FIGURE_VISUAL_QA.md`
- [ ] Data-bearing figures preserve script/GIS/statistical provenance and are not hand-redrawn as scientific evidence
- [ ] Statistical values in text match analysis outputs
- [ ] Review-response changes, if any, map to comment IDs and affected artifacts
- [ ] Data/code availability statements are accurate and match `ARTIFACT_MANIFEST.md`

### Public Release Hygiene
- [ ] `.env`, credentials, tokens, private keys, local secrets, and private databases are excluded from public archives
- [ ] required environment variables are documented through `.env.example` or README text without secret values
- [ ] hard-coded API keys, passwords, private URLs, and machine-local absolute paths are removed or parameterized
- [ ] public repository or archive contents match the data/code availability statement

## Key Rules

- Do not fabricate DOIs, repository links, software versions, or availability statements.
- Do not move large data or delete outputs unless the user explicitly asks.
- Reproducibility is not just code style; it is claim-to-artifact traceability.
- `ARTIFACT_MANIFEST.md` is the canonical submission handoff; unresolved blockers should be explicit rather than hidden in notes.
- Use `Workflow Dependency Trace` for projects where claims depend on multi-step data, code, analysis, or figure-generation chains that a flat manifest cannot diagnose clearly.
- If full reproducibility is impossible due to restricted data or proprietary software, document the boundary explicitly.
