---
name: res_find
description: Turn a broad environmental-science direction into a defensible, data-grounded research idea.
---

Use subagents only when the user explicitly requests delegation; otherwise perform role checks locally.

Generate environment-science research ideas from: **$ARGUMENTS**

## Role in the Research Workflow

`res_find` is the Discovery-stage orchestrator. It should produce a small set of defensible, data-grounded candidate ideas, not a finished method or paper.

Screen the current direction using the supplied evidence and targeted literature checks. Return a ranked shortlist with uncertainty; do not automatically launch method design, experiment planning, or writing. Existing novelty/editorial assessments are useful inputs, not required workflow dependencies.

SciDER-inspired principle: idea generation must be grounded in **killer prior work + residual delta + data characteristics + executable validation**, not only in abstract novelty language. The default stance is falsification-first: try to prove the idea is already done before generating candidates.

## Core Outputs

- `IDEA_REPORT.md` — ranked idea report with evidence, novelty risks, data grounding, feasibility, and next-step recommendations
- Optional `idea.json` — machine-readable idea summary when requested or useful for an authorized handoff
- Optional `IDEA_CANDIDATES.md` — compact shortlist when the user requests a lightweight handoff

Reuse available literature coverage, closest prior-work comparisons, residual deltas, hypothesis notes, and data audits in any sufficient format. Missing legacy gate files do not block screening. Missing scientific evidence limits the recommendation and must be reported; do not invent it.

## Stage Gates

### G0 — Scientific Question Gate
Extract from the request and available context; ask only for unresolved, consequential choices:
- phenomenon/process of interest
- environmental system and spatial/temporal scale
- target variable or mechanism
- why the problem matters scientifically
- what kind of evidence could answer it

### G1 — Literature and Gap Gate
Use `nature-academic-search` for missing literature evidence.
Extract:
- core-domain consensus
- unresolved scientific gaps
- source coverage, query families, de-duplication/ranking baseline, and missing or manual sources
- mature models or methods in the field
- top-journal papers worth reproducing or extending
- adjacent domains with transferable theories, data products, or methods
- closest prior work and what remains unverified

### G1.5 — Closest prior work and falsifiability

Check the proposed contribution against the closest prior work using claim, synonym, adjacent-domain, method-baseline, and data-source queries as relevant to the question. Record sources, search coverage gaps, and overlap across object, method, data, and claim.

- High verified overlap requires `REFRAME` or `DROP`; rewording is not novelty.
- Incomplete coverage cannot support an unqualified novelty claim.
- Every candidate needs a falsifier and a residual delta worth testing.
- A region, combination, or method-only delta is weak novelty unless it answers a new question or establishes a new dataset, mechanism, or finding.

### G1.6 — Scientific hypothesis and evidence test

For a recommendation, identify the central tension, prior explanation being refined, falsifiable hypothesis, mechanism chain, distinguishing figure or test, minimum evidence, and strongest reviewer objection. Assess a journal ceiling only when requested and supported. If the evidence is insufficient, return a qualified candidate or a specific evidence gap; do not require permission just to perform the requested screening.

### G2 — Data Grounding Gate
Before ranking ideas, identify the data reality behind each candidate:
- available observations, remote-sensing products, reanalysis, model outputs, field data, or derived datasets
- spatial/temporal coverage and resolution
- variables, units, semantics, and expected mechanism relevance
- obvious quality risks: missingness, bias, scale mismatch, uncertainty, licensing, reproducibility limits
- whether the idea can be minimally tested without inventing data

If no plausible data path exists, downgrade or reject the idea even if it sounds novel.

### G3 — Top-Paper Reproduction Gate
When the user provides a top-journal paper or asks for idea generation from existing work, identify:
- what can be reproduced directly
- what depends on unavailable data, code, software, or domain assumptions
- which limitation, dataset, region, mechanism, or method gap can become a new idea
- what data or experimental setup would make the extension falsifiable

### G4 — Candidate Idea Gate
Return a shortlist proportionate to the evidence and requested scope. Each recommended idea must include:
- scientific question
- hypothesis
- core novelty type: `problem`, `method`, `data`, or `finding`
- environmental domain and scale
- data grounding and data feasibility
- required data and mature baseline models
- possible cross-domain inspiration and transfer boundary
- experiment outline or minimal validation
- closest prior work hypothesis
- residual delta after closest prior work
- anti-novelty verdict: `SURVIVE`, `REFRAME`, or `DROP`
- editorial hypothesis verdict: `PROCEED`, `REFRAME`, `RETURN_TO_DATA_AUDIT`, or `ABANDON`
- central tension and killer figure
- qualitative overlap assessment and threat level; quantify only with a defined scoring basis
- novelty risk and feasibility risk
- what would falsify the novelty or scientific claim

### G5 — PI-style Critic Gate
Before recommending ideas, apply a PI-style critique:
- Is the question scientifically important or just technically convenient?
- Is the idea only "apply method X to domain Y"?
- Can the available data actually answer the question?
- What is the strongest reviewer objection?
- What would a knowledgeable non-specialist find unclear, unconvincing, or overclaimed?
- Can the question be reframed into a more testable version without inflating novelty?
- What missing evidence would stop the project?
- Should the idea proceed, be reframed, or be abandoned?

### G6 — Selection Gate
Rank candidates by:
- scientific importance
- novelty defensibility
- data availability and quality
- methodological feasibility
- paper story potential
- risk of being only "apply method X to domain Y"
- ability to survive the PI-style critic gate

Recommend the strongest supported candidates; the author chooses the research direction. Continue to another stage only when authorized.

## Output

Use one compact report with the direction, search/source trace and coverage gaps, closest prior work, candidates with the fields above, and ranked recommendations. Include reproduction opportunities only when relevant. Keep missing evidence next to the affected recommendation; use `AUTHOR_INPUT_NEEDED` only for a scientific choice or input that cannot be recovered from available sources.

Do not repeat the same candidate fields across multiple mandatory tables. Produce `idea.json` when a machine-readable handoff is useful or requested; it does not authorize a downstream workflow.

## `idea.json` Schema

```json
{
  "idea_id": "idea_001",
  "title": "",
  "scientific_question": "",
  "hypothesis": "",
  "novelty_type": "problem|method|data|finding",
  "environmental_domain": "",
  "scale": {"spatial": "", "temporal": ""},
  "data_grounding": "",
  "data_requirements": [],
  "baseline_models": [],
  "killer_prior_work": [],
  "overlap_score": null,
  "residual_delta": "",
  "anti_novelty_verdict": "SURVIVE|REFRAME|DROP",
  "editorial_hypothesis_verdict": "PROCEED|REFRAME|RETURN_TO_DATA_AUDIT|ABANDON",
  "central_tension": "",
  "killer_figure": "",
  "journal_ceiling": "",
  "closest_prior_work_to_check": [],
  "cross_domain_inspiration": [],
  "transfer_boundary": "",
  "minimal_validation": "",
  "falsifier": "",
  "reviewer_attack": "",
  "next_skill": null
}
```

## Key Rules

- Do not skip literature grounding.
- Do not generate ideas before anti-novelty and editorial-hypothesis screening when the direction is broad or top-journal oriented.
- Do not describe an idea as novel without documented search coverage, closest prior work, a falsifier, an overlap assessment, and a residual delta.
- Kill or reframe high-overlap ideas instead of rescuing them with new wording.
- Do not expand topic labels; require central tension, falsifiable hypothesis, and killer figure before recommending an idea.
- Do not generate ideas that cannot be tested with plausible data.
- Do not treat cross-domain borrowing as novelty unless the transfer boundary is explicit.
- Do not let a method idea replace the environmental science question.
- Prefer one sharp scientific question over a bundle of loosely connected improvements.
- Every recommended idea must include data grounding, a minimal validation route, and a closest-prior-work hypothesis.
- If evidence is insufficient, report the specific gap and complete the supported screening; do not invent a research story.
