---
name: nature-polishing
description: Polish, restructure, or translate Chinese or English academic prose while preserving facts, evidence boundaries, terminology, claim strength, and citations. Use for 论文润色、学术改写、SCI语言编辑、Results压缩, or manuscript LaTeX layout fixes; use nature-writing when creating new arguments or sections.
---

# Nature-Style Academic Polishing — Router

This skill is split into two layers:

- A **static layer** under `static/` that holds versioned, reusable content fragments (core principles, paper-type playbooks, per-section guidance, language-specific rules, per-journal style).
- A **dynamic layer** (this file plus `manifest.yaml`) that detects the request's axes and loads only the fragments needed for the current job.

Do not try to apply the polishing logic from memory or from this router. Always load fragments from disk as described below.

## Fast-path preflight

Before the normal five-step route, check whether the request matches
`fast_paths.language_only` in [manifest.yaml](manifest.yaml). It matches only
when the user supplied the text and requested wording-level improvement while
locking argument, evidence, claim strength, and paragraph order.

If it matches, detect only the requested output language, load only the files
listed by that fast path plus the matching language fragment, apply the
Language-only contract below, and return the clean prose. Do not detect or
announce the other axes, and do not load `always_load`, paper-type, section,
journal, evidence-authority, or on-demand resources. Naming the passage as an
Abstract or Introduction does not by itself disable this fast path.

Use the normal route whenever the user asks for translation plus substantive
rewriting, target-journal conformity or word-limit work, structural
compression, argument/evidence changes, whole-manuscript consistency, or
versioned-artifact mutation.

## Routing protocol

Follow these five steps when the fast-path preflight does not apply.

### 1. Load the manifest and the core layer

Read [manifest.yaml](manifest.yaml). It declares the axes (`paper_type`, `section`, `language`, `journal`), the allowed values, and the file paths each value maps to.

Also read every file listed under `always_load`. These hold the default stance, failure-mode diagnosis, ethics, and output format that apply to every polish job.

### 2. Detect the axis values for this request

For each axis in the manifest, decide the value using the manifest's `detect:` hint and the user's input:

- `paper_type` — research / methods / hypothesis / algorithmic / review. Default: research.
- `section` — abstract / intro / results / discussion / conclusion / title / methods. May be multiple. Ask the user if it is ambiguous and matters for the polish.
- `language` — zh / en / zh-to-en. Use `zh` when Chinese should remain
  Chinese, `zh-to-en` only when Chinese should be translated into English,
  and `en` for an English source and English output.
- `journal` — nature / nat-comms / nat-mach-intell / generic. Default:
  generic. Use `nature` only for flagship Nature, `nat-comms` for Nature
  Communications and `nat-mach-intell` for Nature Machine Intelligence (NMI).
  Do not route another Nature Portfolio title through flagship Nature rules.

Keep the detected axis values internal by default. Surface only a material
ambiguity that could change the requested language, section job, or target
journal; do not expose routine router metadata.

### 3. Load the matching fragments

For each axis value, Read the file mapped in the manifest. Skip the `section` axis only if the user has supplied free-floating prose with no section context.

Do **not** read every fragment in `static/`. Load only what step 2 selected.

### 4. Polish using the loaded material

Apply the loaded fragments in this priority order, matching the `paper type -> section job -> paragraph logic -> claim/evidence/boundary -> sentence polish` rule from `core/failure-modes.md`:

1. Paper-type playbook (architecture, writing order).
2. Section-specific job and failure modes.
3. Journal-specific framing and constraints.
4. Language-specific sentence and paragraph rules (apply last).
5. Core stance and ethics throughout.

If a paragraph's structural problem cannot be fixed without inventing content, flag it instead of papering over it.

### Language-only contract

Use this fast path when the user supplies a passage and asks only for clearer,
more concise, or more fluent wording while keeping the argument and evidence
unchanged. Classify it internally as `LANGUAGE_ONLY`.

- Lock facts, claims, numbers, citations, causal direction, modality, hedges,
  paragraph functions, and paragraph order.
- Do not re-adjudicate claim support, demand external evidence locators,
  compute a hash for pasted text, or expose owner, axis, gate, mode, or
  Terminology Ledger metadata. This polish preserves the current claim state;
  it neither certifies nor invalidates the underlying science.
- For standalone pasted text, do not restore project state, scan the workspace,
  or search project memory unless the user asks or the passage depends on
  project-specific terminology that cannot otherwise be resolved.
- Do not add defensive qualifiers such as `may`, `might`, `potentially`,
  `可能`, `或许`, or `在一定程度上` merely because a separate evidence audit
  was not performed. Do not strengthen the claim either.
- Return clean prose only. Report a genuine contradiction or meaning-changing
  ambiguity separately instead of silently editing the scientific claim.

Use the fuller route below only when the user requests structural compression,
argument changes, evidence changes, a whole-manuscript consistency pass, or an
actual versioned-artifact mutation that needs authority checks.

For Results, full-main-text compression, main-versus-SI allocation, or prose
added during revision, load `../nature-shared/core/main-text-discipline.md`
before sentence polishing. Classify each result, retain the shortest sufficient
evidence chain, and require every addition to trigger a deletion or replacement
check across the affected paragraph.

For flagship Nature, Nature Communications, Nature Machine Intelligence, or
another Nature Portfolio title, load the matching shared Nature-style corpus
guidance:

- Results or Discussion →
  `../nature-shared/core/nature-results-discussion.md`
- Introduction or whole-manuscript narrative →
  `../nature-shared/core/nature-introduction.md`
- Abstract → `../nature-shared/core/nature-abstract.md`

Preserve claim escalation, the fast question funnel, Introduction–Results
alignment, discovery-centred abstract compression, evidence-bound local
interpretation, and cross-Results synthesis. These defaults were initially
distilled from published NMI papers; treat them as corpus-derived guidance, not
official policy, and obey the target journal's current rules when they differ.

### 5. Reach for references only when needed

The files under `references/` are deep references, not defaults. Open them on demand per the `references.on_demand` table in the manifest, for example when the user explicitly asks for phrasebank-style alternatives or a stricter style audit.

When the target is Nature Machine Intelligence and exact limits, availability
sections, conference-extension disclosure or production checks affect the
revision, load
`../nature-shared/journal-formats/nature-machine-intelligence.md`.

When the job is a whole manuscript rather than a passage, or the text has already been through more than one round of editing, also load `../nature-shared/core/consistency-sweep.md`. Polishing passage by passage cannot see accumulated drift: one experimental factor under several names, the same quantity in two units, a metric at two precisions, or a superlative the paper's own table contradicts. Sweep for those before working on sentences, and repeat the sweep until a pass finds nothing new.

For an actual edit to a versioned manuscript artifact, any edit that may affect
scientific meaning, claim-bearing restructuring, or a submission-readiness
statement, load `../nature-shared/core/evidence-authority.md` and bind the exact
source and editable surface. Do not load it solely because a pasted passage
came from an existing manuscript. Classify the requested mutation before
editing:

- `LANGUAGE_ONLY`: facts, claims, numbers, citations, hedges, paragraph
  functions, and order stay fixed.
- `BOUNDED_ACADEMIC_REWRITE`: sentence reconstruction is allowed inside the
  existing argument and evidence boundary.
- `ARGUMENT_OR_EVIDENCE_REWRITE`: interpretation, claim strength, evidence use,
  paragraph function/order, or story may change and therefore requires the
  applicable author/evidence gate before polishing continues.

Return clean prose as the deliverable. Keep rationale, before/after mapping,
and claim-disposition notes separate unless the user explicitly asks for them.

**Layout/typesetting (排版) requests are different.** If the user asks to fix
*placement* rather than wording — loose/sparse pages, stranded headings, figures
that don't fill the page or split across pages, "Float too large", multi-panel
arrangement, sparse Supplementary Information — skip the prose axes (paper_type,
section, language, journal) and load `references/latex-layout.md` directly. That
file is self-contained: it carries the diagnosis workflow (render → contact-sheet →
read the log), the float-glue and `[H]`/`\clearpage`/`placeins` patterns, and the
"regenerate wide figures taller at the source" rule. Always compile and visually
inspect rendered pages before and after — never judge layout from the `.tex` alone.

## Why this split

- The static layer is versioned and reviewable. Adding a new journal style or paper type is one new file plus one manifest line.
- The dynamic layer keeps each invocation cheap: only the fragments relevant to this draft enter context, instead of the full 1000-line monolith.
- The router itself is short on purpose. Update fragments, not this file, when adding scope.
