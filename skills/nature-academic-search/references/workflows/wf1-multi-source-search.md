# Workflow 1: Multi-Source Literature Search

**Purpose:** Search multiple academic databases in parallel, deduplicate, merge, and rank results.

**Prerequisites:** MCP tools available (PubMed, CrossRef, arXiv, and optionally Semantic Scholar / Google Scholar).

**Uses:** [Dedup Engine](../dedup-engine.md) — deduplication and merge preference logic.

## Procedure

1. **Analyze topic** — identify domain, consult [source routing](../search-strategy.md#source-selection).
2. **Select sources by tier** — follow [Source Tiers](../source-tiers.md). Always try T1 first; escalate to T2 only if T1 insufficient; use T3 as last resort with explicit user warning.
3. **Search in parallel** — call all relevant MCP search tools simultaneously:
   - Biomedical → `pubmed_search_articles`
   - Cross-disciplinary → `search_crossref`
   - Preprints → `search_arxiv` / `search_biorxiv` / `search_medrxiv`
   - Exhaustive → add `search_semantic_scholar` / `search_webofscience` / `search_scopus`
4. **Deduplicate** — apply [Dedup Engine](../dedup-engine.md) to merged result list.
5. **Merge and rank** — follow the user's relevance/date/citation preference. For claim-support work, keep relevance, evidence type and original-source access separate: an inaccessible direct study remains relevant but unverified; an accessible peripheral paper is not equivalent support. See [Result Ranking](../search-strategy.md#result-ranking).
6. **Complete the requested search** — bibliographic discovery ends with its requested records. For claim support, map each material claim to the checked original passage and its scope, or mark the specific unresolved gap. A fixed paper count, DOI match or accessible full text alone does not establish adequate support. Do not replace the research question to fit available papers. Continue useful supported work within scope, and preserve important blocked candidates and lawful fallback attempts in the result.
7. **Present results** — include source labels and verification status; for claim support also give evidence type, locator and limits. A short table is sufficient; do not require a new workflow artifact for a simple lookup.

## Output Format

```
**Title**: [Paper Title]
**Authors**: [Author list]
**Journal**: [Journal name]
**Year**: [Year]  |  **DOI**: [DOI]  |  **PMID**: [PMID]
**Citations**: [count if available]
**Abstract**: [First 200 characters...]
```

## Error Modes

- **MCP tool unavailable:** report specific failure, continue with remaining tools.
- **No results:** broaden terms per [Query Construction](../search-strategy.md#query-construction), try alternative sources, suggest user refine query.
- **All sources empty:** suggest MeSH strategy (Workflow 3) or manual query refinement.
