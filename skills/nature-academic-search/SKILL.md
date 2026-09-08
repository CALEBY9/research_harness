---
name: nature-academic-search
description: >-
  Coordinate multi-source literature search, citation verification, citation-context and
  influence audits, MeSH strategies, and BibTeX/RIS/NBIB management. Use for 文献检索、
  查论文、补支撑文献、段落补引用、引文核对、严格他引、排除自引、引用影响分析或参考文献管理; not for
  deep-reading one known paper.
---

# Academic Search — Router

This skill is split into two layers:

- A **static layer** under `static/` that holds versioned, reusable content fragments (the MCP tool inventory and shared modules, and source routing plus operational rules).
- A **dynamic layer** (this file plus `manifest.yaml`) that detects which workflow the user needs and loads that workflow, reaching for shared modules and scripts only when a step needs them.

Do not try to apply the search logic from memory or from this router. Always load fragments from disk as described below.

## Routing protocol

Follow these five steps every time the skill is invoked.

### 1. Load the manifest and the core layer

Read [manifest.yaml](manifest.yaml). It declares the `workflow` axis, the allowed values, and the file paths each value maps to.

Also read every file listed under `always_load`:

- `static/core/tools.md` — the MCP tool inventory (core search, extended search, PubMed utilities) and the shared-module map.
- `static/core/routing-and-ops.md` — the T1→T2→T3 source routing quick guide, environment setup, error handling, and limitations.

### 2. Detect the workflow

Map the user's need to one or more `workflow` values:

- `multi-source-search` — find literature across sources, including support for manuscript claims without an explicit journal-family restriction.
- `citation-verification` — verify citations extracted from a document.
- `mesh-strategy` — build a MeSH/PubMed search strategy.
- `citation-file-mgmt` — convert/manage `.nbib`/`.ris`/`.bib` files.
- `reference-mgmt` — BibTeX, related-article discovery, ID conversion.
- `strict-other-citation-impact-audit` — determine strict independent other-citations, build article-level citation metric tables, identify high-profile citers (academy members, presidents/deans, talent-award holders, fellows, field leaders), and extract how they cited the target paper.

A combined request (for example search then export) may need more than one. State the detected workflow(s) in one short line before proceeding.

For supporting citations, derive queries from the actual claim and search the
relevant discipline without a publisher-family filter. Return source-specific
support or contradiction with the original locator, using the evidence boundary
below. An explicit request to restrict sources to Nature/CNS belongs to
`nature-citation`; a top-journal writing target alone does not restrict citations.

### 3. Load the matching workflow fragment(s)

Read the file mapped for each detected workflow (under `references/workflows/`). Do **not** read every workflow. Each workflow file links to the shared modules it needs.

### 4. Run the workflow using the loaded material

Apply the loaded material in this order:

1. Core tools and routing (`core/tools.md`, `core/routing-and-ops.md`) — which MCP tool for which need, and the T1→T2→T3 fallback chain that is the standard execution order across all workflows.
2. The workflow fragment — its specific steps.
3. Shared modules and scripts on demand (dedup, citation parser, search strategy, RIS/BibTeX format, format converter).

Keep discovery metadata, snippets/abstracts, full-text availability, source
verification, and claim support as separate states. For claim-bearing
synthesis or manuscript handoff, load
`../nature-shared/core/evidence-authority.md`; verify the original paper and
retain a DOI/URL plus page, section, figure, table, or equivalent locator.
Search hits and citation counts locate candidates but do not license a
scientific claim.

Report specific tool failures and continue with remaining tools; broaden terms when there are no results; fall back to manual generation from MCP-fetched metadata if a script fails twice.

### 5. Reach for references only when needed

The files under `references/` (and `scripts/`) are deep references, not defaults. Open them on demand per the `references.on_demand` table in the manifest — for example `references/source-tiers.md` for the full reliability classification, `references/dedup-engine.md` / `references/citation-parser.md` / `references/search-strategy.md` / `references/ris-bibtex-format.md` for the shared modules, and `scripts/academic_search.py` (no-MCP fallback discovery search) / `scripts/format-converter.py` / `scripts/preflight.py` for the tooling.

## Why this split

- The static layer is versioned and reviewable; the workflow files and shared modules were already factored this way.
- The dynamic layer keeps each invocation cheap: only the workflow the user needs enters context, instead of all six plus every module.
- The router itself is short on purpose. Update fragments and references, not this file, when adding scope.
- This structure mirrors the other nature-* skills (`nature-writing`, `nature-polishing`, `nature-reader`, `nature-paper2ppt`, `nature-figure`, `nature-citation`, `nature-response`, `nature-data`).
