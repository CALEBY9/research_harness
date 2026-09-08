---
name: res_method
description: Refine an environmental-science idea into a problem-anchored, data-aware, implementable method proposal.
---

Use subagents only when the user explicitly requests delegation; otherwise perform role checks locally.

Refine and concretize: **$ARGUMENTS**

## Role in the Research Workflow

`res_method` is the Planning-stage method refinement gate. It turns a defensible idea into a focused proposal with clear data, model, analysis, figure, and validation implications.

Begin with the author's selected question or mature idea. Do not force discovery or a novelty-workflow run before method refinement. If a broad direction still lacks a problem anchor, use available literature and data to identify the specific unresolved scientific choice.

## Evidence needed for design

Reuse existing literature coverage, closest prior work, residual delta, hypothesis, and data feasibility evidence in any sufficient format. When novelty affects the proposed method, verify the missing evidence with `nature-academic-search`; a named legacy gate file is not a prerequisite. Separate established support, unresolved novelty, and provisional design assumptions. Do not rescue a region-only or method-only novelty claim by changing wording.

## Goal

Produce a proposal that is:

1. anchored to one scientific problem
2. testable with plausible environmental data
3. aware of mature in-domain baselines
4. explicit about any cross-domain borrowing
5. simple enough to implement and defend
6. ready for claim-driven experiment planning in `res_plan`

## Constants

| Constant | Default | Description |
|----------|---------|-------------|
| `OUTPUT_DIR` | `refine-logs/` | Directory for method refinement artifacts |
| `MAX_PRIMARY_CLAIMS` | 2 | Prefer one dominant claim plus one supporting claim |
| `MAX_METHOD_BLOCKS` | 5 | Keep the core method compact |
| `MAX_BASELINE_FAMILIES` | 3 | Prefer a few strong baselines over long lists |

## Expected Inputs

Read the most relevant available context first:

- `idea.json`
- `IDEA_REPORT.md`
- `refine-logs/LITERATURE_COVERAGE_AUDIT.md`
- `refine-logs/REVIEW_SUMMARY.md`, if a previous review exists
- `literature/` summaries or notes
- user-provided proposal, top-journal paper, dataset description, or method sketch

If no clear scientific question exists, stop and ask for the missing problem anchor instead of designing a method.

## Workflow

### Phase 0: Freeze the Problem Anchor

Define:
- environmental system
- spatial and temporal scale
- target variable, process, or mechanism
- scientific gap
- why the question matters
- minimum evidence needed to answer it

The problem anchor must remain stable through the refinement. Do not let method novelty replace the scientific question.

### Phase 1: Data Audit Gate and Domain Grounding

Before choosing methods, perform a data audit inspired by data-centric research-agent workflows. Identify:
- required observations, remote-sensing products, field measurements, model outputs, or reanalysis data
- spatial/temporal resolution and coverage
- variable semantics, units, coordinate systems, and domain meaning
- known quality issues, uncertainty, missingness, bias, and scale mismatch
- data access, licensing, privacy, and preprocessing feasibility
- dependency relationships among files, tables, rasters, vectors, models, or metadata
- mature field methods and baseline models

If the data cannot plausibly answer the frozen scientific question, stop with a data-gap report instead of designing an unsupported method.

For marine spatial co-location or offshore planning studies, extend the Data Audit Gate with a data-enhancement pass before method selection:
- download or stage public layers in a traceable `data/external/enhancement_sources/` directory;
- keep `download_manifest.json`, source URLs, access dates, licenses, file hashes, query scripts, and failed-download notes;
- prioritize real public sources such as GFW fishing effort, Bio-ORACLE/Copernicus Marine, GEBCO bathymetry, WDPA/OECM, Figshare/Zenodo aquaculture or water-quality datasets, public sea-use/project PDFs, WRI power plants, and OpenStreetMap/Overpass infrastructure proxies;
- treat login-gated, application-only, commercial, military, or privacy-sensitive data as manual acquisition items, not fabricated substitutes;
- downgrade unsupported claims when only national screening layers are available and site-level hydrodynamics, cable routes, VMS/non-AIS fishing, engineering surveys, or ecological monitoring are missing.


### Phase 2: Compare Method Routes

Compare viable routes when the method remains open or the user requests comparison. When the author has already chosen a method, refine it and its relevant baselines without forcing unrelated alternatives:

1. **Mature in-domain route** — strong established method or baseline
2. **Borrowable adjacent-domain route** — theory, model, statistic, or workflow from another domain
3. **Frontier route, if justified** — LLM/VLM/foundation model/diffusion/RL/etc. only when it directly solves the bottleneck

For every borrowed or frontier component, state:
- what is transferred
- why transfer is valid
- what evidence would prove transfer legality
- where the transfer likely fails

### Phase 3: Build the Final Method Proposal

Specify:
- dominant contribution type: `problem`, `method`, `data`, or `finding`
- core method blocks and their roles
- data-processing workflow
- model/analysis workflow
- baseline comparison set
- uncertainty and sensitivity analysis needs
- figure implications
- implementation risks

Keep the method compact. Remove components that do not defend the main claim.

### Phase 4: PI-style Reviewer Gate

Check:
- Does the method answer the frozen scientific question?
- Is the novelty more than applying method X to domain Y?
- Are the data assumptions realistic after the Data Audit Gate?
- Are mature baselines included?
- Is cross-domain transfer justified?
- Are limitations and failure boundaries explicit?
- What is the strongest reviewer objection?
- What fatal flaw would make the project not worth running?
- Should the proposal proceed, be reframed, or stop before `res_plan`?

## Canonical Output

Write or propose `refine-logs/FINAL_PROPOSAL.md` with:

```markdown
# Final Proposal

## Problem Anchor

## Scientific Question

## Knowledge Gap

## Dominant Contribution

## Data Audit Gate
| Dimension | Finding | Risk | Required Action |
|-----------|---------|------|-----------------|
| Structure |  |  |  |
| Quality |  |  |  |
| Semantics |  |  |  |
| Dependency |  |  |  |
| Access / License |  |  |  |

## Data and Study System

## Mature Baselines and Field Standards

## Method Thesis

## Method Workflow

## Cross-Domain Inspiration and Transfer Boundary

## Claim Map
| Claim | Evidence Needed | Baseline / Comparator | Risk | Planned Validation |
|-------|-----------------|-----------------------|------|--------------------|

## Data Processing Plan

## Model / Analysis Plan

## Figure Implications

## Limitations and Failure Boundaries

## Next Step
If experiment planning is included in the request, hand the completed proposal to `res_plan`; otherwise deliver the method proposal.
```

Optionally write:
- `refine-logs/REVIEW_SUMMARY.md` — reviewer critique and response notes
- `refine-logs/REFINEMENT_REPORT.md` — summary of changes across refinement rounds

## Key Rules

- Verify novelty-critical prior work and retain explicit uncertainty where coverage remains incomplete; reuse sufficient evidence without requiring legacy artifact names.
- Do not invent data availability, performance, results, or citations.
- Prefer the smallest adequate mechanism.
- Prefer strong baselines over padded comparisons.
- Make transfer legality explicit for every cross-domain or frontier component.
- Separate method design from experiment planning; detailed run order belongs in `res_plan`.
