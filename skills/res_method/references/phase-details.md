# Research Refine - Phase Details

This document contains detailed instructions, templates, and prompts for each phase.
See the main SKILL.md for workflow summary and constants.

---

## Phase 0: Freeze the Problem Anchor

Before proposing anything, extract the user's immutable bottom-line problem.

### Output Fields

- **Bottom-line problem**: What technical problem must be solved?
- **Must-solve bottleneck**: What specific weakness in current methods is unacceptable?
- **Non-goals**: What is explicitly *not* the goal of this project?
- **Constraints**: Compute, data, time, tooling, venue, deployment limits.
- **Success condition**: What evidence would make the user say "yes, this method addresses the actual problem"?

### Checkpoint

Write `refine-logs/REFINE_STATE.json`:
```json
{
  "phase": "anchor",
  "round": 0,
  "threadId": null,
  "last_score": null,
  "last_verdict": null,
  "status": "in_progress",
  "timestamp": "<now>"
}
```

---

## Phase 1: Build the Initial Proposal

### Step 1.1: Scan Grounding Material

Use `lit_search` outputs, `refine-logs/NOVELTY_EVIDENCE_PACKAGE.md`, and known-paper context if available. Focus on:
- What mechanism do current methods use?
- Where exactly do they fail for this problem?
- Which mature in-domain methods and adjacent-domain techniques are relevant?
- What data products, variables, representations, or interfaces are reusable?
- What details distinguish a real method from a renamed high-level idea?

### Step 1.2: Identify the Technical Gap

Make the gap operational:
1. **Current pipeline failure point**: where does the baseline break?
2. **Why naive fixes are insufficient**: larger context, more data, prompting, etc.
3. **Smallest adequate intervention**: least additional mechanism that could plausibly fix the bottleneck?
4. **Frontier-native alternative**: more current route using foundation-model-era primitives?
5. **Core technical claim**: exact mechanism claim that could survive top-venue scrutiny?
6. **Required evidence**: minimum proof needed to defend that claim?

### Step 1.3: Choose the Sharpest Route

Compare two candidate routes if both are plausible:
- **Route A: Elegant minimal route** — smallest mechanism targeting the bottleneck.
- **Route B: Frontier-native route** — more modern route using LLM/VLM/Diffusion/RL if it gives a cleaner or stronger story.

Decide based on:
- Which route is more likely to become a strong paper under constraints?
- Which route has the cleaner novelty story relative to the closest work?
- Which route avoids contribution sprawl?

### Step 1.4: Concretize the Method

The proposal must answer "how would we actually build this?"

Cover:
1. One-sentence method thesis
2. Contribution focus (one dominant + at most one supporting)
3. Complexity budget (what is frozen/reused, what is new, what is excluded)
4. System graph (modules, data flow, inputs, outputs)
5. Representation design
6. Training recipe
7. Inference path
8. Why the mechanism stays small
9. Exact role of any frontier primitive
10. Failure handling

If the method is still only "add a module" or "use a planner," it is not concrete enough.

### Step 1.5: Design Minimal Claim-Driven Validation

For each core claim, define the **smallest strong experiment**:
- the claim being tested
- the necessary baseline or ablation
- the decisive metric
- the expected directional outcome

Rules:
- Ensure one experiment directly supports the Problem Anchor
- If complexity risk exists, include one simplification/deletion check
- If a frontier primitive is central, include one necessity check
- Default to 1-3 core experiment blocks

### Step 1.6: Proposal Template

Save to `refine-logs/round-0-initial-proposal.md`:

```markdown
# Research Proposal: [Title]

## Problem Anchor
- Bottom-line problem:
- Must-solve bottleneck:
- Non-goals:
- Constraints:
- Success condition:

## Technical Gap
[Why current methods fail, why naive bigger systems are not enough]

## Method Thesis
- One-sentence thesis:
- Why smallest adequate intervention:
- Why timely in foundation-model era:

## Contribution Focus
- Dominant contribution:
- Optional supporting contribution:
- Explicit non-contributions:

## Proposed Method
### Complexity Budget
- Frozen/reused backbone:
- New trainable components:
- Intentional exclusions:

### System Overview
[Pipeline or ASCII graph]

### Core Mechanism
- Input/output:
- Architecture/policy:
- Training signal/loss:
- Why main novelty:

### Training Plan
[Stagewise or joint, losses, data construction]

### Failure Modes
- [Failure mode]: [Detection] -> [Fallback]

### Novelty and Elegance Argument
[Closest work, exact difference, focused mechanism-level contribution]

## Claim-Driven Validation Sketch
### Claim 1: [Main claim]
- Minimal experiment:
- Baselines/ablations:
- Metric:
- Expected evidence:

## Compute & Timeline Estimate
- Estimated GPU-hours:
- Timeline:
```

### Checkpoint

Update `REFINE_STATE.json` with `{"phase": "proposal", "round": 0, ...}`.

---

## Phase 2: External Method Review (Round 1)

Send the full proposal to GPT-5.4 for review:

```
mcp__codex__codex:
  model: REVIEWER_MODEL
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    You are a senior ML reviewer for a top venue (NeurIPS/ICML/ICLR).
    This is an early-stage, method-first research proposal.

    Your job is NOT to reward extra modules, contribution sprawl, or benchmark checklist.
    Your job IS to stress-test whether the proposed method:
    (1) still solves the original anchored problem,
    (2) is concrete enough to implement,
    (3) presents a focused, elegant contribution,
    (4) uses foundation-model-era techniques appropriately.

    Review principles:
    - Prefer the smallest adequate mechanism over a larger system.
    - Penalize parallel contributions that make the paper feel unfocused.
    - If a modern LLM/VLM/Diffusion/RL route would clearly produce a better paper, say so concretely.
    - If the proposal is already modern enough, do NOT force trendy components.
    - Do not ask for extra experiments unless needed to prove core claims.

    Read the Problem Anchor first. If your suggested fix would change the problem being solved,
    call that out explicitly as drift instead of treating it as a normal revision.

    === PROPOSAL ===
    [Paste FULL proposal from Phase 1]
    === END PROPOSAL ===

    Score these 7 dimensions (1-10):

    1. **Problem Fidelity**: Does method still attack the original bottleneck?
    2. **Method Specificity**: Are interfaces, representations, losses, training stages concrete?
    3. **Contribution Quality**: One dominant mechanism-level contribution with real novelty?
    4. **Frontier Leverage**: Foundation-model-era primitives used appropriately?
    5. **Feasibility**: Trainable/integrable with stated resources?
    6. **Validation Focus**: Minimal but sufficient experiments?
    7. **Venue Readiness**: Sharp and timely for top venue?

    **OVERALL SCORE**: Weighted: Problem Fidelity 15%, Method Specificity 25%,
    Contribution Quality 25%, Frontier Leverage 15%, Feasibility 10%, Validation 5%, Venue 5%.

    For dimensions < 7: specific weakness + concrete fix + priority (CRITICAL/IMPORTANT/MINOR)

    Then:
    - **Simplification Opportunities**: 1-3 concrete ways to delete/merge/reuse (NONE if tight)
    - **Modernization Opportunities**: 1-3 ways to replace old-school with frontier-era (NONE if modern)
    - **Drift Warning**: NONE if still solves anchored problem
    - **Verdict**: READY / REVISE / RETHINK

    Verdict: READY if overall >= 9, no drift, one focused dominant contribution
```

**CRITICAL**: Save `threadId` and full raw response. Save to `refine-logs/round-1-review.md`.

### Checkpoint

Update `REFINE_STATE.json` with `{"phase": "review", "round": 1, "threadId": "<saved>", "last_score": <parsed>, "last_verdict": "<parsed>", ...}`.

---

## Phase 3: Parse Feedback and Revise

### Step 3.1: Parse the Review

Extract:
- All 7 dimension scores + overall
- Verdict
- Drift Warning
- Simplification/Modernization Opportunities
- Action items by priority

Update `refine-logs/score-history.md`:

```markdown
# Score Evolution

| Round | Problem Fidelity | Method Specificity | Contribution Quality | Frontier Leverage | Feasibility | Validation Focus | Venue Readiness | Overall | Verdict |
|-------|------------------|--------------------|----------------------|-------------------|-------------|------------------|-----------------|---------|---------|
| 1     | X                | X                  | X                    | X                 | X           | X                | X               | X       | REVISE  |
```

**STOP CONDITION**: If overall >= SCORE_THRESHOLD, verdict READY, no drift → skip to Phase 5.

### Step 3.2: Revise

Before changing anything:
1. Copy Problem Anchor verbatim
2. Write **Anchor Check**: Does current method still solve it? What would cause drift?
3. Write **Simplicity Check**: What is dominant contribution? What can be removed?

Process reviewer feedback:
- **Valid**: sharpen mechanism, simplify, or modernize if paper improves
- **Debatable**: revise but explain reasoning with evidence
- **Wrong/drifting/over-complicating**: push back with evidence

**Do not** add multiple parallel contributions to chase score. If reviewer requests another module, first ask whether the same gain comes from better interface/distillation/reward model.

### Revision Template

Save to `refine-logs/round-N-refinement.md`:

```markdown
# Round N Refinement

## Problem Anchor
[Copy verbatim]

## Anchor Check
- Original bottleneck:
- Why revised method still addresses it:
- Reviewer suggestions rejected as drift:

## Simplicity Check
- Dominant contribution after revision:
- Components removed/merged:
- Why remaining mechanism is smallest adequate route:

## Changes Made
### 1. [Method section]
- Reviewer said:
- Action:
- Reasoning:
- Impact:

## Revised Proposal
[Full updated proposal]
```

### Checkpoint

Update `REFINE_STATE.json` with `{"phase": "refine", "round": N, ...}`.

---

## Phase 4: Re-evaluation (Round 2+)

Send revised proposal back to GPT-5.4 in **same thread**:

```
mcp__codex__codex-reply:
  threadId: [saved from Phase 2]
  model: REVIEWER_MODEL
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    [Round N re-evaluation]

    I revised the proposal based on your feedback.
    First, check whether the original Problem Anchor is preserved.
    Second, judge whether the method is now more concrete, more focused, more current.

    Key changes:
    1. [Method change 1]
    2. [Method change 2]
    3. [Simplification / modernization / pushback]

    === REVISED PROPOSAL ===
    [Paste FULL revised proposal]
    === END REVISED PROPOSAL ===

    Re-score same 7 dimensions and overall.
    State whether Problem Anchor is preserved or drifted.
    State whether dominant contribution is sharper or still too broad.
    State whether method is simpler or still overbuilt.
    Focus new critiques on missing mechanism, weak training signal, weak integration, pseudo-novelty, unnecessary complexity.

    Same output format: 7 scores, overall, verdict, drift warning, simplification, modernization, remaining action items.
```

Save to `refine-logs/round-N-review.md`.

### Checkpoint

Update `REFINE_STATE.json` with `{"phase": "review", "round": N, "threadId": "<saved>", "last_score": <parsed>, "last_verdict": "<parsed>", ...}`.

**Loop**: Return to Phase 3 until overall >= SCORE_THRESHOLD or MAX_ROUNDS reached.

---

## Phase 5: Final Report and Logs

### Step 5.1: REVIEW_SUMMARY.md

```markdown
# Review Summary

**Problem**: [user's problem]
**Initial Approach**: [user's vague approach]
**Date**: [today]
**Rounds**: N / MAX_ROUNDS
**Final Score**: X / 10
**Final Verdict**: [READY / REVISE / RETHINK]

## Problem Anchor
[Verbatim anchor]

## Round-by-Round Resolution Log

| Round | Main Concerns | What This Round Changed | Solved? | Remaining Risk |
|-------|---------------|-------------------------|---------|----------------|
| 1     | [issues]      | [changes]               | [yes/partial/no] | [if any] |

## Final Status
- Anchor status: [preserved/corrected/unresolved]
- Focus status: [tight/slightly broad/diffuse]
- Modernity status: [appropriately frontier-aware/intentionally conservative/still old-school]
- Strongest parts:
- Remaining weaknesses:
```

### Step 5.2: FINAL_PROPOSAL.md

```markdown
# Research Proposal: [Title]

[Paste final refined proposal only - clean version without review chatter]
```

### Step 5.3: REFINEMENT_REPORT.md

```markdown
# Refinement Report

**Problem**: [user's problem]
**Initial Approach**: [user's vague approach]
**Date**: [today]
**Rounds**: N / MAX_ROUNDS
**Final Score**: X / 10
**Final Verdict**: [READY / REVISE / RETHINK]

## Output Files
- Review summary: `refine-logs/REVIEW_SUMMARY.md`
- Final proposal: `refine-logs/FINAL_PROPOSAL.md`

## Score Evolution
[Full score-history table]

## Final Proposal Snapshot
[3-5 bullet summary]

## Method Evolution Highlights
1. [Most important simplification]
2. [Most important mechanism upgrade]
3. [Most important modernization]

## Remaining Weaknesses
[Honest unresolved issues]

## Next Steps
- If READY: proceed to `/research_design_experiments`
- If REVISE: manually address remaining issues, re-run `/research_design_method`
- If RETHINK: revisit core mechanism with `/idea-creator`
```

### Step 5.4: Finalize score-history.md

Ensure complete score evolution table with all 7 dimensions.

### Step 5.5: Present Summary to User

```
Refinement complete after N rounds.
Final score: X/10 (Verdict: READY / REVISE / RETHINK)

Anchor status: [preserved/drift corrected/unresolved]
Focus status: [tight/slightly broad/still diffuse]
Modernity status: [appropriately frontier-aware/intentionally conservative/still old-school]

Key method upgrades:
- [change 1]
- [change 2]

Remaining concerns:
- [if any]

Review summary: refine-logs/REVIEW_SUMMARY.md
Full report: refine-logs/REFINEMENT_REPORT.md
Final proposal: refine-logs/FINAL_PROPOSAL.md
Next step: /research_design_experiments
```

### Checkpoint

Update `REFINE_STATE.json` with `{"phase": "done", "status": "completed", ...}`.
