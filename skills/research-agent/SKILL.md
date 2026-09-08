---
name: research-agent
description: Primary Codex entry for research tasks invoked as "调用 Research agent" or "调用Research agent". Route the task to the locally installed Nature Skills baseline and use legacy local research skills only as bounded adapters for capabilities Nature Skills do not provide.
---

# Research Agent

Select the smallest owner that completes the present request. Read its
`SKILL.md`, manifest when present, and only the triggered resources. The retired
Research workflow and its owner chain are not executable dependencies.

## Nature owners

| User task | Owner |
|---|---|
| Read or translate a paper | `nature-reader` |
| Deep-read one paper; map claims to evidence | `nature-paper-card` |
| Search literature or audit citation impact | `nature-academic-search` |
| Download lawful full text or supporting information | `nature-downloader` |
| Add claim-supporting citations without a journal-family restriction | `nature-academic-search` |
| Add citations explicitly restricted to Nature/CNS journals | `nature-citation` |
| Verify reference metadata | `nature-ref-verifier` |
| Recurring literature monitoring | `nature-literature-pipeline` |
| Build, audit, or query a local literature corpus | `literature_kb` |
| Proposal, research plan, or opening report | `researchwrite` |
| Statistical reporting | `nature-statistics` |
| Data/code availability statements | `nature-data` |
| Scientific figures | `nature-figure` |
| New manuscript content, argument restructuring, initial-submission materials | `nature-writing` |
| Graduation thesis/dissertation chapters or whole-thesis integration | `nature-writing` with `task=thesis` |
| Academic language polishing or translation | `nature-polishing` |
| Pre-submission peer review | `nature-reviewer` |
| Reviewer responses and revision correspondence | `nature-response` |
| New paper-based presentation | `nature-paper2ppt` |
| Reconstruct image-only slides as editable PPTX | `nature-image2ppt` |

Corpus hits are retrieval candidates; `literature_kb` owns corpus selection and
source binding. Claim-bearing use requires checking the original source. Missing
PDFs may use `nature-downloader`; retrieval snippets do not establish support.

When requested writing needs literature support and a known registered corpus
matches the topic, use `literature_kb` as support for the selected writing owner.
Reuse sufficient verified evidence; skip corpus retrieval for wording-only edits
and topics outside its coverage.

## Prose routing and finishing

- Ordinary wording-only requests go directly to `nature-polishing` as
  `LANGUAGE_ONLY`. Its fast path owns meaning preservation and clean prose
  delivery. For standalone pasted text, do not restore project state, scan the
  workspace, or search project memory unless unresolved project terminology
  makes that context necessary. Do not add a writing or anti-defensive pass.
- Explicit Humanizer requests use `humanizer-zh` for Chinese and
  `humanizer:humanizer` for English; match each segment of mixed-language text.
  Claim-bearing research prose stays under `nature-polishing`, with Humanizer
  as style guidance. Do not add humanization to ordinary polishing.
- For requested end-to-end Chinese-to-English humanization, use Chinese
  preprocessing only if needed, then `nature-polishing` in `zh-to-en` mode,
  English Humanizer, and the academic anti-defensive finish below.

An explicit anti-defensive rewrite of supplied academic prose is owned by
`nature-polishing`; `anti-defensive-writing` is only its post-owner finish,
never the primary owner.

Load `anti-defensive-writing` after new or substantively restructured manuscript
prose from `nature-writing`, proposal prose from `researchwrite`, an explicit
anti-defensive rewrite, or a Humanizer pass on claim-bearing academic prose.
For `nature-response`, apply it only to revised manuscript passages, not the
response letter. The finish owns its evidence-preservation rules; it must not
hide adverse evidence, replace metrics, strengthen claims, or decide the story.

For a sparse-evidence abstract that needs the earlier measured-quantity and
anti-padding checks, consult `references/abstract-final-assembly.md` after the
writing owner. It is conditional guidance, with no fixed sentence count or
length, and does not apply to `LANGUAGE_ONLY`.

## Local gaps

| Operation without a Nature owner | Adapter |
|---|---|
| Screen and rank broad research directions using literature and data | `res_find` |
| Refine an author-selected idea into an implementable method | `res_method` |
| Convert a mature method into an experiment/analysis roadmap | `res_plan` |
| Execute raw/processed research data analysis | `data_analyze` |
| Interpret completed analysis outputs as claim evidence | `res_analyze` |
| Audit claim-to-artifact traceability and reproducibility | `evidence_audit` |
| Systematic review, meta-analysis, or scientometric synthesis | `lit_synthesis` |
| Repair academic DOCX/LaTeX formatting and layout | `paper_format` |
| Draft a manuscript-grounded image-model prompt | `nature-image2-prompt` |
| Distill public scholarship into research judgment frameworks | `research-scholar-distiller` |

For a local gap, also read
`C:/Users/Administrator/.agents/skills/nature-shared/core/evidence-authority.md`.
Reuse sufficient evidence already supplied; start at the author-selected stage.
The rows are alternatives, not a required sequence.

When a source has been replaced and existing cards or claim audits are stale,
start with `evidence_audit`: bind the replacement source and revalidate the
affected derivations before current use. Preserve earlier artifacts as history.

## Scope and continuation

A single-stage request ends with that deliverable, including necessary supporting
owners such as citation verification or formatting. A new independent research
stage requires user authorization; users need not enumerate internal owner calls.
Load one owner at a time; do not preload downstream skills or spawn stage agents.

At an authorized owner transition, update the existing project state contract
with objective, artifacts consumed/produced, validation actually executed,
unresolved blockers, and next owner. Do not create a parallel state system.
Continue while scope and evidence prerequisites permit. Negative or ambiguous
results may narrow, hold, or reject support; a new research question, dominant
claim, or `STORY_REBASE` requires the author's decision.

Subagents, schedules, external messages, and external-library mutations require
explicit user authorization. Destructive or irreversible actions retain their
applicable approval boundaries; a stage transition does not renew or expand
permission.

## Research code and maintenance

For an explicitly requested OpenSpec task or a project already using OpenSpec,
read `references/openspec-research.md` while retaining the current task owner.

Before creating or materially changing research code or analysis configuration,
read `references/research-code-spec.md`. It owns `FORMAL`, `MINI`, and
`NOT_APPLICABLE` selection, existing-spec reuse, and scientific decision points.
Do not create a duplicate spec when the existing project contract suffices.

If an owner or resource is unavailable, report the specific gap and use the
smallest auditable fallback supported by the evidence; preserve completed work.
Keep internal routing and gate metadata out of routine answers and clean finals.

For route/owner maintenance only, use `references/copilot-regression.json` and
run affected cases. Static route checks do not establish prose quality.
