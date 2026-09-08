# Idea Discovery - Templates

## IDEA_REPORT.md Template

```markdown
# IDEA_REPORT

**Direction**: [research direction]
**Date**: [today]
**Pipeline**: lit_search -> anti-novelty-gate -> editorial-hypothesis-gate -> res_find -> res_novelty -> res_method -> res_plan

## Executive Summary
[2-3 sentences: best idea, key evidence, data grounding, recommended next step]

## Literature and Gap Summary
[key findings, gaps, closest prior work hypotheses, and open problems from lit_search]

## Literature Coverage Audit
| Coverage dimension | Checked sources / query families | Missing or manual sources | Residual risk | Action |
|--------------------|----------------------------------|---------------------------|---------------|--------|

## Killer Prior Work Matrix
| Candidate direction | Killer prior work | Object overlap | Method overlap | Data overlap | Claim overlap | Threat | Verdict |
|---------------------|-------------------|----------------|----------------|--------------|---------------|--------|---------|

## Claim Overlap Score
| Claim | Must-be-new component | Strongest overlapping evidence | Overlap score | Residual delta | Verdict |
|-------|-----------------------|-------------------------------|---------------|----------------|---------|

## Reframe Log
| Original direction | Reason it failed or weakened | Reframed residual delta | Status |
|--------------------|-----------------------------|--------------------------|--------|

## Editorial Hypothesis Gate Summary
| Candidate | Central tension | Falsifiable hypothesis | Killer figure | Journal ceiling | Fatal risk | Verdict |
|-----------|-----------------|------------------------|---------------|-----------------|------------|---------|

## Search and Evidence Trace
| Source | Query / Lead | Relevant Finding | Verification Status | Notes |
|--------|--------------|------------------|---------------------|-------|

## Data Grounding Summary
| Data source / product | Variables | Scale | Quality risk | Access / license | Relevance |
|-----------------------|-----------|-------|--------------|------------------|-----------|

## Top-Journal Reproduction Opportunities
| Paper | Reproducible component | Limitation or gap | Possible extension | Data needed |
|-------|------------------------|-------------------|--------------------|-------------|

## Candidate Ideas

### Idea 1: [title] — RECOMMENDED / BACKUP / REFRAME / DROP
- Scientific question:
- Hypothesis:
- Novelty type: problem / method / data / finding
- Core environmental system:
- Data grounding:
- Data requirements:
- Mature baseline / existing model:
- Cross-domain inspiration:
- Transfer boundary:
- Experiment outline:
- Minimal validation:
- Closest prior work hypothesis:
- Residual delta after prior work:
- Anti-novelty verdict:
- Editorial hypothesis verdict:
- Central tension:
- Killer figure:
- Journal ceiling:
- Claim overlap score:
- What would falsify novelty:
- What would falsify the scientific claim:
- Feasibility risk:
- Novelty risk:
- Reviewer attack:
- Paper story:

## Candidate Evidence Table
| Idea | Residual delta | Data grounding | Minimal test | Closest prior work to check | Overlap threat | PI critic verdict |
|------|----------------|----------------|--------------|-----------------------------|----------------|-------------------|

## Ranked Recommendation
| Rank | Idea | Why now | Main risk | Required novelty check | Next skill |
|------|------|---------|-----------|------------------------|------------|

## Next Step
Run `res_novelty` on the top candidate before method design.
```

## RESEARCH_BRIEF.md Template

```markdown
# Research Brief

**Topic**: [direction]
**Created**: [date]

## Problem Statement
[What scientific or environmental problem must be solved?]

## Constraints
- **Compute**: [hardware/software constraints]
- **Data**: [available data, data needs]
- **Timeline**: [deadline, venue]
- **Venue / article type**: [target journal or manuscript type]

## Prior Attempts
[What has been tried before, and why insufficient?]

## Domain Knowledge
[Relevant background, established methods in the field]

## Non-Goals
[What is explicitly NOT the goal of this project]

## Existing Results
[Any preliminary results already obtained]

## Research Direction Statement
[One-paragraph statement anchoring all downstream phases]
```

## IDEA_CANDIDATES.md Compact Format

```markdown
# Idea Candidates

| # | Idea | Residual Delta | Central Tension | Killer Figure | Data Grounding | Overlap Threat | Minimal Test | Status |
|---|------|----------------|-----------------|---------------|----------------|----------------|--------------|--------|
| 1 | [title] | [delta] | [tension] | [figure] | [data] | [threat] | [test] | RECOMMENDED |
| 2 | [title] | [delta] | [tension] | [figure] | [data] | [threat] | [test] | BACKUP |
| 3 | [title] | [none/weak] | [none] | [none] | [data] | [high] | [test] | DROP |

## Active Idea: #1 — [title]
- Hypothesis:
- Data grounding:
- Key evidence:
- Closest prior work to check:
- Killer prior work:
- Residual delta:
- Anti-novelty verdict:
- Editorial hypothesis verdict:
- Central tension:
- Killer figure:
- Journal ceiling:
- Next step: `res_novelty`
```

## Checkpoint Templates

### After Literature and Anti-Novelty Gate
```text
Literature and anti-novelty screen complete:
- [key findings, gaps, open problems]
- Killer prior work: [list]
- Claim overlap scores: [summary]
- Surviving residual deltas: [list]
- Editorial hypotheses: [central tension + killer figure summary]
- Data products or datasets mentioned: [list]

Does this match your understanding? Should I adjust the scope before generating ideas?
```

### After Candidate Idea Gate
```text
Generated X data-grounded ideas and filtered to Y. Top results:

1. [Idea 1] — Data: [source] — Novelty risk: [risk]
2. [Idea 2] — Data: [source] — Novelty risk: [risk]
3. [Idea 3] — Reframe/drop: [reason]

Which ideas should proceed to `res_novelty`?
```

### After Method Refinement
```text
Method refined and experiment plan ready:
- Problem anchor: [anchored problem]
- Data audit verdict: [proceed / data gap]
- Method thesis: [one sentence]
- Dominant contribution: [what's new]
- Must-run experiments: [N blocks]
- PI critic risk: [risk]

Proceed to `res_plan`, or adjust the proposal?
```
