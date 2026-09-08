---
name: literature_kb
description: Build, inspect, and query verified corpus-specific backends in the papers branch of the unified D-drive LLM knowledge-base project.
---

## Codex CLI Adaptation

This skill is the Codex-side mirror of the Claude Code `literature_kb` skill.

- Interpret Claude slash-command references such as `/literature_kb` as the Codex skill name `literature_kb`.
- Map Claude tools to Codex operations: `Read`/`Glob`/`Grep` to shell reads/searches, `Write`/`Edit` to local file edits, and `Bash` to PowerShell-compatible `shell_command`.
- Do not assume Claude Code hooks, settings, slash-command routing, or Claude-only frontmatter fields exist in Codex CLI.
- Use this skill only as local-document intelligence support; it does not replace `nature-academic-search` for topic discovery.
- Follow `C:\Users\Administrator\AGENTS.md` and project-local `AGENTS.md`.

# literature_kb

Use this skill when the user asks to build, refresh, inspect, or query the papers branch of the unified LLM knowledge-base project on D drive.

This is a local-document intelligence layer. Use a relevant registered corpus
for corpus-assisted writing and questions about its papers; supplement with
`nature-academic-search` for missing or newer literature. The local corpus does
not establish exhaustive field coverage or replace open literature discovery.

## Quick Trigger / Stop Card

- Use when: the user asks to build, refresh, inspect, health-audit, or query an existing local paper corpus, or requested writing needs evidence from a relevant registered corpus.
- Do not use as the sole owner of open-ended discovery, closest-prior coverage, novelty judgment, or acquisition of papers outside the corpus; use the corresponding research or search owner.
- Required inputs: selected `corpus_id`, source/index boundary, intended action, and a verified backend/script path.
- Output / handoff: backend and run directory, corpus boundary, retrieval candidates with source locators, quality warnings, and next owner skill; add a Retrieval QA Dossier when multiple KB papers will feed manuscript prose.
- Return / stop conditions: missing script/index -> `KB_RESOURCE_MISSING`; documented interface drift -> `KB_RESOURCE_CONTRACT_DRIFT`; missing runtime dependency -> `KB_ENVIRONMENT_MISSING`; unresolved corpus/run boundary -> `KB_CORPUS_UNBOUND`; incomplete retrieval QA for a planned manuscript claim -> `KB_RETRIEVAL_QA_INCOMPLETE`; incomplete corpus coverage -> return to `nature-academic-search` for field-level claims.
- Validation: `Test-Path`, script `--help` or AST/parser check, manifest/artifact readback, and a read-only query or explicitly scoped smoke build.

## Canonical Entry

Canonical unified LLM KB root:

```text
D:\03_claude research\01_LLM-knowledge_base
```

Knowledge branches:

```text
papers\   # research papers, PDFs, article metadata, paper RAG indexes
wiki\     # non-paper/wiki/notes/wechat/other knowledge sources
```

Project-specific paper indexes should live under:

```text
D:\03_claude research\01_LLM-knowledge_base\papers\indexes\<corpus_id>
```

Known paper corpora:

```text
green_certificate_carbon_power
  sources: D:\03_claude research\01_LLM-knowledge_base\papers\sources\green_certificate_carbon_power
  indexes: D:\03_claude research\01_LLM-knowledge_base\papers\indexes\green_certificate_carbon_power

dl_gee_literature
  sources: D:\03_claude research\01_LLM-knowledge_base\papers\sources\dl_gee_literature
  pdfs: pdfs\\
  existing chunks: derived_chunks\\parsed
  indexes: D:\03_claude research\01_LLM-knowledge_base\papers\indexes\dl_gee_literature
```


Unified PDF storage policy:

```text
D:\03_claude research\01_LLM-knowledge_base\papers\sources\<corpus_id>\pdfs
```

Keep PDFs, derived chunks, metadata, QC artifacts, and generated indexes in separate sibling directories.

## Verified Backend Routes

Select the corpus before choosing a command. Do not assume every corpus uses the same builder, retrieval backend, manifest, or quality artifact.

### DL-GEE: active Qwen3/FAISS + SQLite BM25 hybrid backend

Operational root:

```powershell
cd "D:\03_claude research\01_LLM-knowledge_base"
```

Read-only query of the hash-verified active hybrid `run_*` index:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File papers\scripts\query_dlgee_hybrid.ps1 "deep learning geospatial process extraction"
```

The launcher uses the pinned managed runtime, retrieval overlay, local model
snapshot, and offline Hugging Face cache. If any of those paths is unavailable,
return `KB_ENVIRONMENT_MISSING`; do not install or silently switch models. The
query verifies the registered manifest, health report, parent BM25 bindings,
and FAISS hash before loading the index. Use the lexical fallback explicitly
when dense retrieval is unavailable or a BM25 comparison is requested:

```powershell
python papers\scripts\query_dlgee_literature_index.py "deep learning geospatial process extraction"
```

For corpus-assisted writing, follow `docs/dlgee_writing_evidence.md` in the
verified KB project. Create an explicit query plan from the user's question;
for Chinese questions include useful English equivalents, then run the existing
hybrid launcher with `--queries-file <plan.json> --chunks-per-paper 3`.
Choose relevant passages and use
`python -B papers/scripts/read_dlgee_evidence.py --chunk-id <id> --neighbors 1`
to read complete chunks and hash-bound original PDF pages. Use its
`--paper-id <id> --list-sections` and `--section <heading>` options for needed
methods/results context. Keep the writing owner and continue after checking
support; neither a search hit nor a successful PDF read licenses a claim.
This adds no automatic API call, reranker, index refresh or mandatory Paper Card.

An explicitly requested five-paper smoke build must stay under `smoke_runs` and must not replace the production index:

```powershell
python papers\scripts\build_dlgee_literature_index.py --limit 5 --output-root "papers\indexes\dl_gee_literature\smoke_runs" --smoke-query "deep learning geospatial process extraction"
```

### Green-certificate/carbon-power: archived hybrid backend

The executable currently lives at:

```text
D:\01_research\01_green certificate-carbon coupling\tools\literature_kb\literature_kb.py
```

The project is currently archive/read-only. Before build or refresh, read its project `AGENTS.md` and `STATUS.md`; do not reopen or modify the project/configuration unless the user explicitly asks. Its bundled `default_config.yaml` and README still contain pre-migration KB paths, so they are not current execution authority.

For a read-only query of the existing relocated index, preflight both resources and dependencies, then pass the current index path explicitly:

```powershell
$toolRoot = "D:\01_research\01_green certificate-carbon coupling\tools\literature_kb"
$kbDir = "D:\03_claude research\01_LLM-knowledge_base\papers\indexes\green_certificate_carbon_power\run_20260605"
Test-Path -LiteralPath "$toolRoot\literature_kb.py"
Test-Path -LiteralPath "$kbDir\manifest.json"
python -c "import faiss, rank_bm25, pandas, numpy, fitz, yaml"
python "$toolRoot\literature_kb.py" query --kb-dir "$kbDir" --query "绿色证书 与 碳交易 电力市场联动"
```

If the dependency preflight fails, return `KB_ENVIRONMENT_MISSING`. Do not install packages or change the archived project automatically.

## Current Pipeline Contract

- Source corpus: shared KB PDFs under `D:\03_claude research\01_LLM-knowledge_base\papers\sources\green_certificate_carbon_power\papers`.
- Output root: `D:\03_claude research\01_LLM-knowledge_base\papers\indexes\green_certificate_carbon_power`.
- DL-GEE corpus: original PDFs, existing PDF chunks, metadata, extraction outputs, and QC artifacts are stored under `D:\03_claude research\01_LLM-knowledge_base\papers\sources\dl_gee_literature`; treat this as a separate corpus and do not merge it into the green-certificate/carbon-power index.
- Before build/query, verify the canonical root and selected corpus/index path exist. Treat older roots only as provenance unless the user explicitly selects them.
- DL-GEE active backend: MinerU per-paper manifests/chunks -> pinned Qwen3-Embedding-0.6B dense vectors in FAISS plus the immutable parent SQLite FTS5/BM25 run, fused at paper level with RRF. The active registry is `papers/indexes/dl_gee_literature/active_run.json`; the BM25 parent remains the explicit lexical fallback. This is hybrid retrieval, not a reranker.
- Green-certificate archived backend: MinerU/PyMuPDF extraction, semantic chunks, dense index + BM25 reciprocal-rank fusion, and section/short-chunk reranking. Its artifacts are `manifest.json`, `kb_stats.json`, `kb_quality_report.md`, `chunks.csv`, `papers.csv`, `dense.index`, and `bm25.pkl`.
- Report the selected backend and exact run directory. Do not describe the DL-GEE backend as reranked, and do not treat the archived green-certificate manifest as proof that its original source paths remain active.

## Research Workflow Integration

Use this adapter for local-PDF retrieval, corpus-supported writing or knowledge-base maintenance:

```text
literature_kb -> original-source verification -> nature-writing
Use nature-academic-search for coverage outside the corpus;
use nature-downloader for missing originals.
```

For requested writing from multiple corpus papers, load
`../shared-references/kb-to-manuscript-evidence-bridge.md`. This owner supplies
retrieval candidates; `nature-writing` owns source-grounded synthesis and prose.
Use `nature-paper-card` for a requested or necessary deep read, and
`lit_synthesis` for formal review/synthesis work. Continue the authorized task
without forcing a full Paper Card or a retired manuscript stage per citation.

Hard boundaries:

- Do not cite `chunk_id`, vector IDs, or the KB answer as evidence.
- Evidence must resolve back to DOI/title plus page, section, table, figure, equation, or snippet locator from the original paper.
- If the selected backend's quality artifact (`quality_report.md` or `kb_stats.json` / `kb_quality_report.md`) shows poor extraction quality, report the limitation before using retrieved results.
- If the local corpus has not been coverage-audited, do not use it to claim the state of the whole field.
- Keep MinerU optional; unavailable MinerU should degrade to PyMuPDF, not block ordinary literature work.

## Minimum Output

For build/refresh:

```text
KB directory:
Backend:
Papers indexed:
Chunks indexed:
Extractor used:
Quality warnings:
Next query command:
```

For query:

```text
Question:
KB used:
Backend / run directory:
Retrieval summary:
Top evidence candidates:
Limitations:
Next handoff:
```

For KB-assisted manuscript writing, append:

```text
Writing intent / target section:
Corpus inclusion and coverage boundary:
Query IDs and scientific questions:
Retrieval method / settings / source-diversity control:
Original-paper locator completeness:
Answerability: answered / partial / not enough evidence
Residual source families or contradictions:
Bridge status / failure code:
Next owner: nature-writing / nature-paper-card / lit_synthesis (as needed)
```

