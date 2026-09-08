# Idea Discovery - Detailed Workflow

See main `SKILL.md` for stage gates and output contracts.

---

## Phase 0: Research Direction Clarification

### Step A — Load Research Brief if Available

Check for `RESEARCH_BRIEF.md` in the project root:
- problem statement
- constraints: compute, data, timeline, venue
- prior attempts
- domain knowledge
- non-goals
- existing results

If both a brief and a one-line prompt exist, merge them, with the brief taking priority for details.

### Step B — 5W1H Clarification

When the prompt is vague, run a 5W1H pass:

- What phenomenon/process?
- Why scientifically important?
- Where and at what scale?
- Which target variable or mechanism?
- Which data could answer it?
- How would a minimal validation look?

Output a one-paragraph **Research Direction Statement** and save to `RESEARCH_BRIEF.md` only if useful and requested or needed for continuity.

---

## Phase 1: Literature and Anti-Novelty Survey

Use `lit_search` with the current canonical source order:

```text
OpenAlex -> Semantic Scholar -> Crossref/DOI -> WebSearch -> Google Scholar manual -> WoS/Scopus optional
```

Extract:

- field consensus
- closest prior work hypotheses
- recurring limitations
- mature baselines and standard models
- available datasets or data products mentioned in the literature
- adjacent-domain paradigms worth borrowing

Do not treat Zotero/local papers as the primary discovery corpus. They are known-paper context and de-duplication aids.

Checkpoint: present the landscape summary and ask whether the scope should be adjusted before generating ideas.

---

## Phase 1.5: Anti-Novelty Gate

Before generating candidate ideas, try to kill each direction with closest prior work. Run exact-claim, synonym/field-term, adjacent-domain, method-baseline, and data-source query families.

Write or propose:
- `refine-logs/LITERATURE_COVERAGE_AUDIT.md`
- `refine-logs/KILLER_PRIOR_WORK_MATRIX.md`
- `refine-logs/CLAIM_OVERLAP_SCORE.md`
- `refine-logs/REFRAME_LOG.md`
- `refine-logs/SURVIVING_IDEAS.md`

For each candidate direction, score object, method, data, and claim overlap. If overlap is high, mark `DROP` or `REFRAME`. Only residual deltas marked `SURVIVE` can enter candidate idea generation.

Hard failures:
- no literature coverage audit -> no candidate idea or strong novelty language;
- no closest prior-work matrix -> no candidate idea;
- no falsifier -> no candidate idea;
- high verified overlap -> reframe or stop;
- only region / combination / method-only delta -> weak novelty unless it creates a new question, dataset, mechanism, or finding.

---

## Phase 2: Data Grounding Pass

Before generating candidate ideas, identify plausible data foundations:

- observations, remote-sensing products, field measurements, model outputs, reanalysis data, policy datasets, or derived products
- variables, units, semantics, and expected mechanism relevance
- spatial/temporal scale and coverage
- missingness, uncertainty, bias, and scale mismatch
- access, license, privacy, and reproducibility constraints

Reject or downgrade idea directions that cannot be minimally tested with plausible data.

---

## Phase 3: Candidate Idea Generation

Generate 5-8 candidate ideas only from editorially viable residual deltas that passed Phase 1.6. Each idea must include:

- scientific question
- hypothesis
- novelty type: problem / method / data / finding
- data grounding
- minimal validation
- mature baseline
- closest prior work hypothesis
- residual delta after closest prior work
- central tension, falsifiable hypothesis, and killer figure
- journal ceiling and fatal reviewer questions
- overlap score and anti-novelty verdict
- cross-domain inspiration and transfer boundary
- what would falsify novelty
- what would falsify the scientific claim
- reviewer attack

Avoid ideas that are only “apply method X to domain Y” unless the application reveals a new scientific question, dataset, mechanism, or finding.

---

## Phase 4: PI-style Critic and Ranking

Apply a PI-style critic gate to each candidate:

- Is this question important enough?
- Is the novelty defensible?
- Can the data answer the question?
- What would a reviewer attack?
- What evidence is missing?
- Should it proceed, reframe, or stop?

Rank candidates by:

- scientific importance
- novelty defensibility
- residual delta strength after closest prior work
- editorial hypothesis strength
- overlap threat level
- data availability and quality
- methodological feasibility
- paper story potential
- transfer legality
- reviewer risk

Only the top 1-3 should proceed to `res_novelty`.

---

## Phase 5: Write Outputs

Write or propose:

- `IDEA_REPORT.md`
- `idea.json`
- optional `IDEA_CANDIDATES.md`

The output should point clearly to `res_novelty` as the next gate. Do not proceed directly to method design while novelty is uncertain.
