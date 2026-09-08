# Writing workflow

Run these steps for any drafting or restructuring task. Steps 1-3 are planning, step 3b is an alignment gate, 4-6 are drafting, 7-8 are checking, step 9 is the revision loop.

This workflow does not apply to a supplied passage whose argument, evidence,
claim strength, and paragraph order must remain fixed. Route that
`LANGUAGE_ONLY` request to `nature-polishing`; do not require an argument plan,
confirmation gate, Terminology Ledger presentation, or claim-evidence map.

## 1. Build a one-sentence argument

> In [system/problem], we show [advance] using [approach], supported by [evidence], with [boundary].

Force every section to serve this sentence. If the sentence cannot be written, the paper does not yet have an argument — surface that to the user.

## 1b. Build the Terminology Ledger

On first contact with the material, extract the recurring terms, abbreviations, notation, and proper names into a Terminology Ledger before drafting any prose. Lock the canonical forms and reuse them across every section. See `../../../nature-shared/core/terminology-ledger.md`.

## 2. Choose section architecture

Pick the section structure from the relevant `section/*.md` fragment and, if needed, deeper patterns from `references/article-architecture.md`.

## 3. Map each paragraph to one job

Each paragraph must do exactly one job from: context, gap, approach, result, comparison, mechanism, implication, limitation.

If a paragraph carries two jobs, split it before drafting.

## 3a. Allocate Results evidence before drafting

When the task includes Results, a full manuscript, main-text compression, or
main-versus-SI placement, load
`../../../nature-shared/core/main-text-discipline.md`. Classify each result as
core discovery, necessary support, qualification, robustness, heterogeneity,
provenance detail, alternative inference, or edge case. Build the shortest
sufficient main-text evidence chain and record the destination of everything
else. Do not bury conclusion-changing evidence in SI.

## 3b. Confirmation gate — align before drafting

Resolve the core claim, evidence, and boundary from supplied materials and prior
author decisions; they need not be separately restated in the latest prompt.
When these support the requested draft without a material unresolved premise,
proceed to full prose. Do not invent missing evidence or choose a new dominant claim.

If an unresolved choice changes the scientific meaning or requested deliverable,
show the one-sentence argument, the specific uncertainty, and at most 2–3 focused
questions. Await the author's decision for the affected prose. If the author
requests a scaffold despite missing evidence, use explicit placeholders.

- **Depth dial**: deliver an outline first only when the user requests staged
  review or an outline is the requested deliverable.
- **Style, not substance**: if the user says the voice or style "is not mine", do not keep guessing — ask for one short sample of their own writing, then calibrate to it. From the sample, match: typical sentence length and rhythm, hedging level (`demonstrate` vs `may` / `could`), preferred connectives and transitions, person (first-person `we` vs passive), and terminology / abbreviation choices. Match the voice, not the content — never reuse the sample's claims or facts.

## 4. Draft from evidence outward

Keep claims near the data that support them. Do not stack claims at the top of a section then leave evidence at the bottom.

## 5. Calibrate verbs to evidence strength

`show` / `demonstrate` need strong direct evidence. `suggest` / `indicate` are for trend-level or indirect evidence. `may` / `could` are for plausible but unverified mechanisms.

## 6. Remove unsupported novelty and universal claims

Sweep for `first`, `unique`, `unprecedented`, `comprehensive`, `complete`, `always`, `never`. Replace with bounded claims or delete.

## 7. Run a paragraph-flow check

- One paragraph, one message.
- The first sentence is the topic / claim.
- Each subsequent sentence has an explicit relation to the previous one (cause, comparison, restriction, example).

For full reverse-outlining, open `references/paragraph-flow.md`.

## 8. Return prose plus notes

Output the draft together with explicit notes on assumptions, missing inputs, and where evidence is needed. See `output-format.md`.

## 9. Revise by targeted edit, not full rewrite

When the user reacts to a draft, "this is not what I meant" is usually local — a wrong claim, a mis-framed paragraph, the wrong result leading. Do not silently re-draft the whole section: a full rewrite breaks the paragraphs that were already right and forces the user to re-check everything.

- Change **only** the paragraphs or claims the user flagged; keep the rest verbatim.
- If a requested fix genuinely forces a structural change (reordering sections, moving a claim across paragraphs), say so and confirm the new structure before applying it, rather than restructuring silently.
- Keep the Terminology Ledger (step 1b) stable across revisions unless the user changes a term; never let a revision reintroduce a variant of a locked term.
- After revising, re-run only the checks relevant to what changed (steps 5-7), not the whole workflow.
- If the user's redirection reveals the original premise was wrong, return to the confirmation gate (step 3b) instead of patching prose on a broken premise.
- Every proposed addition triggers the main-text deletion check: identify the
  new sentence's function, find existing text with the same function, and prefer
  replacement or compression before appending. Re-run the paragraph necessity
  and claim-repetition checks after the edit.
