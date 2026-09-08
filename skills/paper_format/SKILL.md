---
name: paper_format
description: Audit, repair, or convert academic DOCX, LaTeX, Markdown, Quarto, or Pandoc formatting, including templates, references, headings, equations, figures, tables, captions, pagination, and page-level QA. Use for journal, thesis, or course format compliance and clean-final layout repair; not for substantive prose revision.
---

Use subagents only when the user explicitly requests delegation; otherwise perform role checks locally.

# Paper Format — 投稿前排版与格式审计

Format or audit manuscript materials for: **$ARGUMENTS**

## Quick Trigger / Stop Card

- Use when: auditing, repairing, converting, or final-QAing academic document format, DOCX/Word layout, LaTeX/Markdown/Quarto outputs, references, captions, headings, page numbers, MathType/equations, tables, blind-review metadata, or clean-final compliance.
- Do not use when: the user asks for scientific argument revision (`nature-reviewer`), manuscript drafting (`nature-writing`), language/style polish (`nature-polishing`), journal strategy (`nature-writing`), or reviewer-response prose (`nature-response`).
- Required inputs: editable source or rendered artifact, deliverable type, target authority or generic baseline, source format, output expectation, content stability, and any MathType/Word/template requirements.
- Output / handoff: format audit, edited file, clean final, marked/blind version, PDF proof, layout QA report, output index/version ledger, or blocked status with missing authority/QA.
- Return / stop conditions: return to `nature-reviewer` or `nature-writing` if scientific structure is unstable; stop before submission-ready claims until Word/PDF render QA and clean-final scanning pass.
- Validation: target-rule readback, `docx_layout_audit.py` when DOCX exists, clean-final scanner, rendered Word/PDF page inspection, figure/table body-callout coverage, display-item/caption centering, English-font hierarchy, table/heading/equation QA, and current-file existence checks for versioned outputs.

## Role in the Research Workflow

`paper_format` 是学术写作完成后的排版与格式 QA 层。它适用于 SCI/SSCI 论文、会议论文、课程汇报、课程论文、学位论文、开题报告、综述和通用学术报告；只处理格式、结构、引用样式、版式、模板合规和匿名化合规，不增强科学主张、不补造数据、不替代语言润色、课程内容评价或期刊选择。

Complete the requested operation only. Use the corresponding owner for a needed handoff within the user's authorized scope; these skills are not a mandatory stage chain.

Use `paper_format` after the manuscript content is scientifically stable and before final submission packaging.

## Required Inputs

Inspect only materials needed for the requested formatting task:

- manuscript file: `paper/main.tex`, `paper/sections/`, `.docx` export text, or pasted manuscript text
- references: `paper/references.bib`, reference list, or citation manager export
- figures/tables/captions: `paper/figures/`, figure captions, table files, supplementary materials
- target journal author guidelines, article template, or style guide if provided
- for course or thesis work: course rubric, instructor template, school thesis manual, department formatting rules, title-page requirements, TOC/list-of-figures rules, page-numbering rules, and required output format if provided
- blind-review requirements, if relevant
- for structured Word production: original `.docx`, `reference.docx` if available, `.bib` or citation export, CSL style, figure/table source files, and any journal template requirements
- for poor visual formatting: rendered PDF/DOCX, screenshots, Word style observations, compile/render logs, or user-noted defects
- for MathType-controlled Word output: MathType availability, required equation numbering style, and whether inline variables must be converted to MathType/Word equation objects
- for layout style QA: English/Latin font family, body and caption font sizes, default line spacing, figure/table object and caption alignment, body-callout coverage, table cross-page rules, and heading-level style requirements

If the target journal, course rubric, school manual, or style guide is missing and the user asks for exact formatting, ask for it or provide a clearly marked generic academic-layout checklist. Do not invent journal, course, department, or university requirements.

## Scope

适用:

- 扉页、作者信息、机构、通讯作者、基金与致谢元数据格式化
- 课程汇报、课程论文、开题报告和学位论文的封面、目录、章节层级、页眉页脚、页码、图表目录和附录格式
- 摘要字数、关键词格式、章节标题层级
- 正文引用与参考文献样式转换或审计
- 图题、表题、编号、注释、补充材料标签格式
- 统计符号、p 值、单位、数学表达式的格式一致性
- 行距、缩进、页边距、行号、页码、脚注/尾注等版式检查；用户未另行指定时默认行距为 1.25
- 双盲匿名化与隐藏元数据清理清单
- Word/DOCX 结构化重排流程，包括 Pandoc/Quarto 中间稿、`reference.docx` 样式模板、`.bib + CSL` 引用渲染、Word/PDF 页级 QA
- 排版质量诊断，包括 heading/style collapse、手动空格缩进、表格伪装成段落、公式编号漂移、caption/cross-reference 断裂、浮动体拥挤、分页和对象环绕问题
- MathType 公式排版，包括独立公式自动居中、公式编号右对齐、正文内非独立公式变量转换为 MathType/Word equation-compatible inline math objects
- 图表整合、分页与标题样式 QA，包括每个带编号的图/表是否至少在正文中引用一次，图和表对象及其图题/表题/图注是否居中，表格跨页时表头/断行/注释是否合规，以及 caption 字号是否比正文小一级；用户未另行指定且无目标模板覆盖时，英文正文按 Times New Roman 11 pt、英文图表标题/图注按 Times New Roman 10 pt 检查
- 章节标题规范 QA，包括 heading levels、编号、大小写、加粗/斜体、段前段后、keep-with-next、自动目录/导航结构和模板样式名是否一致
- 可复现渲染路径选择，包括 journal template、native Word styles、LaTeX class、Quarto/Pandoc、R Markdown/rticles、Manubot-like Markdown pipelines 的取舍

不适用:

- 改写科学结论、增强贡献表述或补充未支持声明
- 生成不存在的 DOI、页码、期号、作者信息或数据可得性声明
- 修改数值、统计结果、图表数据或单位含义
- 代替 `nature-polishing` 做语言风格润色
- 代替 `nature-writing` 做期刊选择、投稿策略或 cover letter

## Hard Constraints

- Preserve all names, affiliations, funding IDs, citations, numerical values, equations, statistics, units, and table/figure data unless the user explicitly provides a correction.
- Mark missing or ambiguous metadata for human review instead of fabricating it.
- When converting citation style, keep the citation-reference mapping intact.
- When anonymizing, remove or mask author-identifying information without deleting non-author citations or scientific content.
- If a format rule depends on current journal policy, verify from provided guidelines or web lookup; otherwise label it as unverified.
- Treat Quarto, Pandoc, rticles, Manubot, LaTeX linters, Word automation, and citation metadata tools as optional adapters. Do not add package installs, cloud services, CI, or external repositories as default requirements.
- If the user asks to improve poor formatting, do not call the result submission-ready until the final rendered artifact has been visually or mechanically inspected.
- When the user or project requires MathType formatting, do not substitute plain italic text, manually spaced formula lines, or screenshots for editable equation objects. If MathType or an equivalent Word equation-compatible path is unavailable, return `MATHTYPE_REQUIRED_BUT_UNAVAILABLE`.
- When the user or project requires MathType formatting, table symbols are in scope. Variables in table cells, symbol columns, parameter notes, and table notes must be MathType/Word equation-compatible inline objects, not plain ASCII placeholders such as `INV_natural_bio_R`, `Q_green,ded,s`, `EF_MEF`, or Greek-name strings.
- When the project or user specifies body/caption typography, check it mechanically where possible. If no verified target template overrides the workspace default, English/Latin body text is Times New Roman 11 pt and English/Latin figure/table titles, captions, and figure notes are Times New Roman 10 pt: one point smaller than body text, centered, and styled through caption/note styles rather than manual direct formatting.
- Every numbered figure and table retained in the manuscript must be cited at least once in ordinary body prose outside its caption, table cells, and lists of figures/tables. The callout must use the correct figure/table label and must connect the display item to a claim, comparison, method step, robustness check, or boundary; an uncited display item is a blocking manuscript-integration defect.
- Center the display item as well as its text: inline figure container paragraphs, Word table objects, figure/table titles, captions, and figure notes must all be centered unless a verified target template explicitly requires another alignment. Caption centering alone does not prove that the figure or table itself is centered.
- For DOCX academic manuscripts, all ordinary body-text paragraphs must be justified on both margins unless a verified target template explicitly overrides it. Headings, captions, equations, figure/table notes, references, and table cells may have role-specific alignment, but body prose must not be left-aligned by accident.
- Figure explanatory notes are not ordinary body prose: a `Note:` paragraph that explains a figure must be centered and caption/note sized unless the target template says otherwise. Table notes may follow the table-note rule, but figure notes must not be left-aligned or justified by default.
- Captions, figure notes, table notes, equation explanations, and ordinary body text must never use Heading styles or non-body outline levels. Only true section headings may appear in Word Navigation Pane / TOC. Before finalizing DOCX, verify non-heading paragraphs have body-text outline level.
- True section headings must use the template heading hierarchy, not only direct bold/spacing. In appendices and supplementary files, exact section labels such as `Appendix A.`, `A.1`, `B.2`, and `B.2.1` should be Heading/outline paragraphs; prose that merely begins with words such as `Appendix B-1 covers...` must remain body text.
- If the target journal/template does not specify line spacing, use 1.25 as the default manuscript line spacing and check it through paragraph styles where possible.
- Do not approve table layout from DOCX structure alone. Inspect the rendered Word/PDF pagination for every table, especially long tables, table notes, repeated headers, and page-break behavior.

## Workflow

### Step 0: Target Format Gate

Identify:

- deliverable type: SCI/SSCI journal manuscript, conference paper, course report, term paper, thesis/dissertation, opening report, literature review, research proposal, or generic academic report
- target journal / publisher / style guide, e.g. APA 7, Nature Portfolio, Elsevier, Springer, AGU, MDPI, journal-specific template
- target authority for non-journal work: school thesis manual, department template, course rubric, instructor requirements, provided `.docx`/`.tex` template, or generic academic baseline
- article type: research article, letter, brief communication, review, data paper, methods paper
- source format: LaTeX, Markdown, Word text, pasted sections, BibTeX, plain reference list
- output expectation: edited manuscript, checklist, annotated issues, or conversion instructions
- canonical source: the single editable source file or source directory to modify; if multiple current-looking copies exist, freeze one canonical source before editing
- content stability: content-stable, wording still changing, or structure still changing

If exact target requirements are absent, stop before editing when exact compliance is required, or ask whether to use a generic academic-layout audit. For generic academic-paper layout, use `references/academic_layout_rules.md` as the source-backed baseline rather than relying on tool documentation alone.

Academic deliverable routing:

- `Journal / conference manuscript`: prioritize official author instructions, journal/conference template, publisher style, citation style, figure/table rules, blind-review metadata, and submission-package readiness.
- `Course report / term paper / course presentation handout`: prioritize instructor rubric, required section order, readable heading hierarchy, citation consistency, figure/table captions, page limits, and clean PDF/DOCX delivery. Do not force submission-package gates such as cover letter, response letter, or journal portal checks.
- `Thesis / dissertation / graduation paper`: prioritize school/department manual, title page, abstract pages, TOC, list of figures/tables, chapter numbering, margins, page-number boundaries, headings, references, appendices, declaration pages, and long-document pagination. Do not treat a thesis as a single journal article unless the user explicitly asks for journal conversion.
- `Opening report / proposal / literature review / academic report`: prioritize the required template, heading hierarchy, citation/reference consistency, table/figure numbering, and readable layout; run scientific-structure review only if the user asks about argument quality.
- `Generic academic baseline`: use only when no authority is supplied; label the result as generic and avoid claiming exact SCI, course, or university compliance.

When web-checking layout rules, prioritize academic-paper format sources:

- GB/T 7713.2-2022 or another national/style standard for generic academic-paper layout
- exact target journal author instructions and official templates
- exact school, department, graduate-school, or course formatting instructions when the deliverable is a thesis, dissertation, course report, proposal, or opening report
- publisher/society style manuals for figures, tables, equations, references, headings, and page mechanics
- Word/PDF rendering documentation only for verifying how to implement and inspect the academic rule

### Step 0.1: Targeted Revision and Field-Aware Gate (Hard)

When formatting is part of a proof, minor/editorial revision, marked DOCX, or targeted citation/reference correction, load `../shared-references/manuscript-revision-granularity-gate.md`.

- Inherit the exact editable span, protected context, and maximum edit unit; formatting work may not widen them.
- Patch the smallest Word/XML/LaTeX range. Do not replace an enclosing paragraph, section, citation field result, bibliography field, or style-bearing object to fix a smaller defect.
- Before citation or bibliography mutation, freeze the authoritative source as embedded field code, external reference-manager library, `.bib`/CSL, or verified plain text, plus the current linkage state.
- When a reference-manager library is available, compare the affected field code/result/count/type/linkage before and after a controlled save/reopen/refresh round trip. If unavailable, preserve the field and report the blocker.
- Block on `TARGET_SPAN_AMBIGUOUS`, `REVISION_SCOPE_DRIFT`, `FIELD_RESULT_WHOLESALE_REPLACEMENT`, `WORD_REDLINE_COARSE`, `CITATION_SOURCE_OF_TRUTH_UNRESOLVED`, `REFERENCE_MANAGER_ROUNDTRIP_UNVERIFIED`, or `TRACK_CHANGES_UNVERIFIED`.

### Step 0.25: Format Engine and Visual Quality Triage Gate

Use this gate when the user says the formatting looks poor, when a conversion has degraded layout, or when the target output is a submission-ready manuscript rather than only a compliance checklist.

Select the lightest reliable engine:

- `Native journal template`: use when the journal provides a `.docx`, `.tex`, Quarto extension, R Markdown/rticles template, or publisher class that matches the article type.
- `Structured Markdown/Quarto/Pandoc`: use when the document needs reproducible front matter, citations, captions, cross-references, multiple outputs, or a controlled `reference.docx`.
- `Native Word cleanup`: use when the manuscript already lives in Word and conversion would likely damage comments, tracked changes, MathType/OMML equations, complex tables, or author metadata.
- `Native LaTeX cleanup`: use when the source already compiles from `.tex`, uses a journal class, or requires exact PDF typesetting.
- `Audit-only`: use when the user lacks a target journal/template or only needs a defect map before manual work.

For poor visual formatting, create a defect ledger before editing:

```markdown
| Defect | Evidence | Likely source | Fix route | Verification |
|--------|----------|---------------|-----------|--------------|
| Heading/style collapse | page/paragraph/style locator | lost semantic styles / direct formatting | map to template styles | render + style inspection |
| Caption/cross-ref breakage | figure/table/equation locator | field, label, or citation conversion failure | rebuild labels/fields | updated field list + PDF check |
| Table/equation layout failure | page/table/equation locator | fake tables, oversized formula, wrapping | real table / split equation / width rule | Word/PDF visual QA |
| Table pagination failure | table/page locator | row split, missing repeated header, bad note placement, orphaned caption | table property / page break / repeated header fix | Word/PDF page inspection |
| Caption style mismatch | figure/table locator | manual formatting or wrong style inheritance | apply verified caption style | style inspection + PDF check |
| Heading style mismatch | section locator | manual bold/numbering or wrong level | map to heading style hierarchy | navigation pane/TOC + PDF check |
| Line spacing mismatch | paragraph/style/page locator | direct formatting, inherited template drift, or wrong paragraph style | apply verified paragraph style | style inspection + PDF check |
```

Failure codes:

- `TARGET_STYLE_MISSING`: exact target style cannot be verified.
- `SOURCE_STRUCTURE_LOSS`: headings, captions, references, or equations cannot be preserved through the chosen conversion path.
- `RENDER_QA_FAILED`: final PDF/DOCX inspection shows unresolved layout defects.
- `CLEAN_FINAL_FAILED`: process-language, tracked changes, comments, or internal metadata remain in the clean artifact.
- `MATHTYPE_REQUIRED_BUT_UNAVAILABLE`: MathType-controlled display equations or inline variables are required but cannot be created or verified in the current environment.
- `TABLE_PAGINATION_UNVERIFIED`: table cross-page behavior was not checked in the rendered Word/PDF artifact.
- `CAPTION_STYLE_MISMATCH`: figure/table captions are not centered, not at required font size, or not using the required caption style.
- `DISPLAY_ITEM_CALLOUT_MISSING`: a numbered figure or table has no matching callout in ordinary manuscript body prose.
- `DISPLAY_ITEM_ALIGNMENT_MISMATCH`: a figure container paragraph or Word table object is not centered under the active target rule.
- `ENGLISH_FONT_MISMATCH`: English/Latin body or caption text does not use the active required font family, default Times New Roman.
- `CAPTION_FONT_HIERARCHY_MISMATCH`: a figure/table title, caption, or figure note is not one point smaller than body text under the workspace default.
- `HEADING_STYLE_MISMATCH`: section headings do not match the target hierarchy, numbering, spacing, or style-name requirements.
- `LINE_SPACING_MISMATCH`: manuscript paragraph spacing does not match target guidance or the default 1.25 line spacing.

### Step 0.5: Structured DOCX Production Gate

Use this gate when the output is a submission-ready Word manuscript or when the user asks for Word/DOCX reformatting, journal-template cleanup, or a reusable manuscript-formatting workflow.

If the user controls manuscript content and expects the project to control formatting, treat the task as format stewardship: freeze one editable canonical source, preserve the user's content edits, and route all layout, style, numbering, reference, page, and visual QA work through this gate plus the artifact lifecycle gate below.

Preferred route:

```text
original Word manuscript
-> source-normalized manuscript: Pandoc Markdown / Quarto .qmd / direct Word cleanup, chosen by Step 0.25
-> manual/LLM cleanup of heading levels, captions, formulas, tables, cross-references, and references
-> Quarto/Pandoc DOCX rendering with reference.docx, citation.bib, and CSL
-> Word inspection and correction
-> Word-to-PDF visual QA
-> submission-ready Word lock
```

Rules:

- Treat Pandoc/Quarto output as a structured draft or traceable intermediate artifact, not as final submission proof.
- Use `reference.docx` only for style control: fonts, paragraph styles, heading hierarchy, captions, references, and basic table styles. It does not fix scientific content, formula logic, floating objects, cross-reference failures, pagination, or malformed tables.
- When a custom `reference.docx` is needed, derive it from a Pandoc-produced reference document or a verified journal template; modify styles and document properties, not manuscript content.
- If the input DOCX already has meaningful custom styles, preserve or inspect them during extraction rather than flattening everything to plain Markdown.
- Prefer `.bib + CSL` for reproducible references. Do not assume Word/EndNote fields survive DOCX-Markdown-DOCX round trips unless verified.
- Preserve formulas as auditable LaTeX in Markdown/Quarto where possible. Pandoc can render Word OMML equations, but MathType compatibility must be checked in Word if the project or journal requires MathType.
- For MathType-required Word output, use MathType or Word equation objects compatible with MathType for all display equations and requested inline variables. Do not leave body variables such as model variables, Greek letters, subscripts, superscripts, or symbolic parameters as ordinary styled text when they are meant to be mathematical variables.
- Apply the same MathType rule inside tables and table notes. In notation, parameter, and variable-definition tables, symbol cells and formula-like tokens must be editable equation objects; do not treat table text as exempt from inline math conversion.
- Format display equations so the equation body is automatically centered and the equation number is right-aligned by structure, not by manual spaces. Use a verified MathType/Word equation-numbering mechanism, a stable equation paragraph style, or a borderless alignment table only if it preserves editable equation objects and passes PDF QA.
- Every display equation must have a unique number; never allow two independent equations to share one number. Split long formulas into stable labels such as `(28a)` and `(28b)` when needed.
- Verify a MathType pass by sampling display equations and inline variables in Word: equation body remains editable, numbering is right aligned after field/update/render, inline variables align with surrounding text baseline, and PDF export preserves spacing without overlap.
- Final tables must be real Word tables, not paragraph lists. Use journal-compliant table styling, including three-line tables when required, explicit widths, table notes, units, and cross-page behavior.
- Automatically inspect table pagination in the rendered Word/PDF artifact. For each table, record whether it fits on one page, crosses pages, repeats headers when needed, keeps captions and notes with the relevant table segment, avoids orphaned rows/captions, and follows the journal rule on row splitting.
- Check figure, table, and equation captions plus cross-references in Word after updating fields and lists. For every detected figure/table label, verify at least one matching callout in ordinary body prose; captions, lists of figures/tables, and table-cell text do not satisfy this requirement.
- Center and verify both the display objects and their associated text: inline figure container paragraphs, Word table objects, figure/table titles, captions, and figure notes. Unless the target journal/template specifies otherwise, use Times New Roman 11 pt for English/Latin body text and Times New Roman 10 pt for English/Latin figure/table titles, captions, and figure notes; do not leave captions in body-text size.
- Set figure explanatory `Note:` paragraphs as centered note/caption paragraphs. They must not inherit Heading styles or appear in the Word Navigation Pane.
- Apply section headings through template heading styles, not direct formatting. Verify heading levels, numbering, capitalization, spacing before/after, keep-with-next behavior, and TOC/navigation structure against the target guideline.
- Explicitly demote non-heading paragraphs to body-text outline level after formatting. This includes captions, figure notes, table notes, equation explanations, and ordinary body prose; otherwise Word may incorrectly list them as headings even if they look visually correct. Also verify the reverse: real section labels are not left as body paragraphs with only manual bold/spacing.
- Set and verify line spacing through paragraph styles. Unless the target journal/template specifies otherwise, default to 1.25 line spacing for manuscript text and flag mixed or directly formatted line spacing.
- For DOCX thesis/manuscript page numbers, verify the front-matter/body boundary in Word, not only the existence of `PAGE` fields. If front matter should be unnumbered and the body starts at the introduction, keep cover/abstract/TOC footers blank, set the introduction page to start at `1` when required, and ensure every following body page uses a centered bottom `PAGE` field with continuous numbering. Watch for the Word trap where the introduction's first-page footer has `1` but the next section's primary footer is empty or still linked to a blank previous footer.
- Page-number QA must include rendered PDF footer inspection or footer crops for boundary pages: cover/abstract/TOC, first body page, the page immediately after the first body page, and the last page. A Word field count alone is insufficient because different-first-page footers and linked section footers can hide missing page numbers.
- For long manuscripts, run a calibration render on 1-3 representative pages or sections before full conversion when feasible: title/abstract, one equation-heavy section, one table/figure-heavy section, and one references page.
- Keep QA reports, defect ledgers, and conversion notes outside the clean manuscript, using the project's existing report/check directory. For a new project, use content-specific names such as `layout_checks` or `revision_records`.
- Final acceptance requires Word-to-PDF visual QA for TOC, equation numbering, figure/table numbering, table rules, headers/footers, section breaks, page numbers, fonts, line spacing, object wrapping, and text overlap.
- Before calling a DOCX submission-ready, run the Clean-Final Language Gate in `../shared-references/clean-final-language-gate.md` and scanner `../shared-references/scripts/clean_final_scanner.py` over the clean manuscript, tables, captions, and display items. Do not rely on formatting checks alone; process-language leakage is a submission blocker.

### Step 0.52: Artifact Lifecycle and Filename Gate

Use this gate for any academic DOCX/LaTeX/Markdown formatting project with more than one generated version, or when an output folder already contains multiple candidate finals, process drafts, QA proofs, and temporary files.

Rules:

- Keep versioned manuscript files separate from process drafts, QA PDFs/PNGs, temporary files, and change notes.
- For new projects, name directories by contents using complete English word pairs, such as `manuscript_versions`, `revision_records`, and `layout_checks`; create only the directories needed. The Master Thesis Studio bridge uses `10_manuscript_versions/`, `11_revision_records/`, and `12_layout_checks/<version>/`. Follow an existing project convention, including legacy `10_output/current/`, `archive/`, `iterations/`, and `qa/`, without automatic migration. Record active/approved status in the existing index or ledger.
- Before editing a cluttered manuscript directory, identify the actual current file with filesystem checks. Do not trust stale `.agent`, changelog, or chat pointers unless the referenced file path exists.
- Maintain `09_state/output_index.md` and `09_state/version_ledger.md` when the workspace supports them. If it does not, record the final path, source file, status, QA proof, and superseded outputs in the format QA report.
- New or modified deliverables must use short lowercase version filenames: `v<major>.<minor>_<core-change>.<ext>`, for example `v3.2_abstract.docx`, `v3.3_figures.docx`, or `v4.0_final.docx`.
- Do not encode every modification point, long Chinese sentences, all-caps labels, process notes, or reviewer-response details in filenames. Put those details in the version ledger, QA summary, or a separate change note.
- A clean final must not contain internal filenames, process wording, edit rationale, change logs, or tool descriptions.

Acceptance:

- exactly one active candidate/final is recorded in the output index or QA report;
- the active file exists at the recorded path;
- superseded files are either archived or clearly marked as non-current;
- the filename follows the short version pattern unless an official template or submission portal requires otherwise.

### Step 0.53: Master Thesis Studio Bridge Adapter

Use this adapter only after `paper_format` has classified the deliverable, authority source, source format, content stability, and QA expectation. `paper_format` owns the formatting standard and final-readiness claim; the adapter executes DOCX/Word workspace operations.

Use the bridge when all or most of these are true:

- the source or target output is `.docx`;
- the deliverable is a thesis/dissertation, graduation paper, course paper/report, opening report, literature review, Chinese academic report, or generic academic Word manuscript;
- the user wants format stewardship: they edit content while the workflow owns layout;
- multi-version output governance is needed;
- Word-native QA is required for TOC, page numbers, headers/footers, EndNote/field preservation, MathType/OMML, table pagination, or final PDF proof.

Bridge target:

```text
D:\03_claude research\00_master-thesis-studio
```

Before using the bridge, verify the adapter command exists with `Test-Path "D:\03_claude research\00_master-thesis-studio\scripts\build_output.py"`. If it is missing, return `MTS_WORKSPACE_MISSING` and continue with the native `paper_format` audit/manual Word or `docx_layout_audit.py` route; do not claim bridge QA ran.

Bridge input contract:

```text
canonical source DOCX:
target authority: official rules / template / rubric / journal instructions / generic academic baseline
format rules extracted:
reference paper or sample, if any:
content stability:
workspace path:
version name: v<major>.<minor>_<core-change>
QA mode: audit-only / candidate / final
```

Preferred execution command:

```powershell
python "D:\03_claude research\00_master-thesis-studio\scripts\build_output.py" <project_dir> --format word --name v3.2_format --qa --core-change format
```

Expected bridge outputs for new workspaces (existing `10_output/` workspaces retain `current/` and `qa/` paths):

- `10_manuscript_versions/v<major>.<minor>_<core-change>.docx`
- `12_layout_checks/<version>/docx_complex_audit_report.md`
- `12_layout_checks/<version>/word_com_finalize_report.md`
- `12_layout_checks/<version>/pdf_pages/pdf_layout_qa_report.md`
- `09_state/output_index.md`
- `09_state/version_ledger.md`

Do not use the bridge when the authoritative source is a LaTeX journal class, the task is only citation metadata cleanup, the user asks only for prose polish, or the DOCX must be manually handled because required Word/MathType/EndNote components are unavailable. In those cases, stay in `paper_format` audit-only or route to the more appropriate skill.

Failure codes:

- `MTS_WORKSPACE_MISSING`: the bridge root or project workspace is absent.
- `MTS_SOURCE_NOT_FROZEN`: no single canonical source DOCX has been selected.
- `MTS_QA_NOT_RUN`: bridge output exists but `--qa` evidence is missing.
- `MTS_RENDER_QA_BLOCKED`: Word COM or PDF render QA failed; do not call the output final.
- `MTS_OUTPUT_INDEX_STALE`: recorded current output does not exist or points to a superseded file.

### Step 0.55: Runnable DOCX Layout Audit

When a `.docx` manuscript exists, run the local layout checker before any submission-ready claim:

```powershell
python C:\Users\Administrator\.codex\skills\paper_format\scripts\docx_layout_audit.py manuscript.docx --out-dir qa\layout_audit --academic-profile gb7713 --english-font-name "Times New Roman" --body-font-pt 11 --caption-font-pt 10 --caption-size-delta-pt 1 --display-item-alignment center --require-mathtype --require-inline-math --submission-ready --use-word-com --export-pdf
```

Use the flags conservatively:

- Use `--academic-profile gb7713` when no target journal is supplied and the user asks for generic academic-paper layout; use `--academic-profile ieee` for IEEE-style engineering papers; use `--academic-profile journal` only when exact journal instructions or templates are being checked separately.
- Omit `--require-mathtype` only when the target journal/project does not require MathType or Word equation-compatible objects.
- Omit `--require-inline-math` only when inline variables are explicitly allowed as ordinary formatted text.
- Omit `--use-word-com --export-pdf` only for early triage. Static-only OOXML results cannot close `TABLE_PAGINATION_UNVERIFIED`, display-equation alignment, right-aligned equation numbering, object overlap, or final page layout.
- Keep the generated `docx_layout_audit.json`, `docx_layout_audit_report.md`, and optional PDF proof outside the clean manuscript, following the report-directory convention in Step 0.52.

Checker coverage:

- English/Latin body font family and size, default Times New Roman 11 pt unless overridden
- figure/table caption detection, Times New Roman 10 pt English/Latin caption text, one-point body/caption hierarchy, centered alignment, and use of caption styles unless overridden
- every detected numbered figure/table caption label has a matching callout in ordinary body prose outside captions, lists, and table cells
- inline figure container paragraphs and Word table objects use the required display-item alignment, default centered
- academic-profile caption placement: for `gb7713` and `ieee`, figure captions/titles below figures and table captions/titles above tables
- default/body line spacing, default 1.25 unless overridden
- heading-style detection, heading-level jumps, and direct-formatting warnings
- real Word table presence, likely long tables, repeated-header hints, and render-required table pagination
- OMML/MathType-compatible equation-object detection, display-equation render QA requirement, and inline-equation object presence when requested
- comments, tracked changes, and clean-final process-language hits that would block submission

Acceptance rule:

- The checker is a gate, not a repair tool. Fix the DOCX, rerun the checker, and inspect the Word-exported PDF.
- `Submission-ready Word` requires no unresolved blocker/major findings, Word COM open/export success when DOCX finalization is available, and a human/agent page-level PDF inspection for formula alignment, table cross-page behavior, captions, object wrapping, and overlap.

Completion standard:

- `Needs major fixes`: Quarto/Pandoc rendered but Word/PDF QA has unresolved formula, caption, reference, table, or pagination problems.
- `Needs minor fixes`: remaining issues are local style or spacing corrections.
- `Submission-ready Word`: Word/PDF page-level QA completed; all formula, table, figure, numbering, citation, heading-style, caption-style, line-spacing, header/footer, and pagination problems corrected; every numbered figure/table has a matching body callout; figure paragraphs, Word tables, titles/captions, and figure notes satisfy the active alignment rule; English/Latin body and caption typography satisfy the active font/size hierarchy; all tables have verified cross-page behavior; and `../shared-references/clean-final-language-gate.md` plus the project-local denylist have 0 unresolved hits.

### Step 0.6: Optional Adapter Playbooks

Use these as patterns only when the user's files and installed tools support them.

- Quarto/Pandoc manuscript route: keep semantic source, `_quarto.yml`, bibliography, CSL, captions, cross-references, and `reference.docx` under versioned project folders; render to DOCX/PDF/HTML as proofs; inspect the rendered artifact before delivery.
- Journal-template route: prefer a journal-provided or community-maintained template only when it matches the target journal and article type; otherwise use it as a style clue, not an authority.
- R Markdown/rticles route: useful for journals covered by an existing template and when the source is already R Markdown; verify the generated PDF/DOCX against current journal instructions.
- Manubot-like route: useful as a provenance pattern for Markdown source, identifier-based bibliography, and generated HTML/PDF/DOCX outputs; do not require GitHub/CI or automatic metadata replacement for ordinary formatting tasks.
- Native LaTeX route: preserve the journal class/template, run the minimum compile cycle needed for references/cross-references, inspect log warnings that affect layout, and avoid broad source reformatting unless it fixes a real typesetting defect.
- Native Word route: repair styles, section breaks, fields, real tables, captions, comments, tracked changes, and document properties in Word-compatible structures before PDF proofing.
- MathType-heavy Word route: keep display equations and inline variables editable; use MathType auto-formatting or Word equation objects rather than screenshots; center display equations and right-align numbers structurally; re-check after Word field updates and PDF export.

### Step 1: Front Matter and Structure

Check and format:

- title capitalization and running title, if required
- author names, affiliations, superscripts, corresponding author line
- abstract length and structure
- keywords order, capitalization, separator, and count
- section heading hierarchy and numbering
- section heading style compliance: levels, numbering, capitalization, font, spacing, keep-with-next, and TOC/navigation visibility
- funding, acknowledgements, author contributions, competing interests, ethics, data/code availability statements

Output unresolved items as `Needs author confirmation`, not as guessed content.

### Step 2: Citations and References

Audit:

- in-text citation style: numeric, author-year, superscript, bracketed, Vancouver, APA-like, journal-specific
- multi-author handling, `et al.` rules, citation order, punctuation, year placement
- reference list ordering: alphabetical, citation order, grouped by type, or journal-specific
- reference fields: authors, year, title case/sentence case, journal title, volume, issue, pages, article number, DOI
- citation integrity: DOI / arXiv ID / CrossRef / DataCite / OpenAlex / Semantic Scholar title-author-year consistency where available
- citation-reference consistency: every in-text citation has a reference entry, and every retained reference is cited or explicitly justified
- claim support: classify whether each high-risk citation supports the specific sentence claim, is only topic-relevant, needs full-text checking, or requires author decision

Never invent missing DOI, issue, page range, or article number. Flag incomplete entries. Do not automatically delete suspicious references; classify them as `VERIFIED`, `METADATA_MISMATCH`, `TOPIC_RELEVANT_BUT_CLAIM_UNSUPPORTED`, `NEEDS_FULLTEXT_CHECK`, `UNRESOLVED_OR_POSSIBLY_FAKE`, or `AUTHOR_DECISION_NEEDED`.

### Step 3: Figures, Tables, Statistics, and Units

Check:

- figure/table numbering sequence and cross-references; every numbered figure/table must have at least one matching body-text callout outside captions, lists, and table cells
- figure/table object placement plus title/caption/note placement, centered alignment, label style, font family, font size, notes, abbreviations, and significance legends
- figure/table caption size relative to body text; default English/Latin check is Times New Roman body 11 pt and titles/captions/figure notes 10 pt unless target style overrides
- table pagination: whether each table crosses pages, repeats headers when needed, keeps notes/captions with the table, and avoids orphaned rows or uncontrolled row splitting
- supplementary figure/table naming and linkage
- main or submission figures have matching `figure_spec.yml`, render/provenance records, and `FIGURE_VISUAL_QA.md`
- statistical symbol formatting: italic variables where required, spacing around operators, p-value style
- MathType / equation-object consistency for display equations and inline variables when required by the project or journal
- SI units, unit spacing, pluralization, and journal-specific unit conventions
- consistency between captions, callouts, and display items

Do not alter any data value or statistical result.

### Step 4: Layout and Document Mechanics

Check:

- margins, font, line spacing, paragraph indentation, block quotes; default line spacing is 1.25 unless target guidance overrides it
- English/Latin body/caption font hierarchy, including Times New Roman body 11 pt and figure/table title/caption/figure-note text 10 pt when the workspace default applies
- section heading levels, numbering, style names, spacing before/after, and TOC/navigation behavior
- body paragraphs justified on both margins, with only role-based exceptions
- line numbers, page numbers, continuous vs section numbering, front-matter/body numbering boundaries, first-page footer settings, linked-to-previous footer state, and centered bottom page-number placement
- footnote/endnote conversion requirements
- equation numbering and placement
- MathType display-equation centering, right-aligned equation numbers, and inline-variable object consistency when required
- MathType/equation-object consistency for variables inside tables and notes when required
- file naming, figure resolution, table editability, supplementary files
- template-specific commands or style tags for LaTeX/Markdown when applicable

For Word/PDF-only requirements, provide precise instructions if direct editing is not possible.

### Step 5: Blind Review and Metadata Audit

If double-blind review is required, audit:

- title page separation or removal
- author names, affiliations, emails, acknowledgements, funding IDs if identifying
- self-citation wording and reference masking rules required by the journal
- file properties, comments, tracked changes, figure metadata, supplementary file names
- repository links, data/code availability statements, and preprint references that identify authors

Do not anonymize unless the journal requires it or the user asks for a blind-review version.

### Step 6: Output

Choose the minimal useful output:

1. **Direct edits** to manuscript/reference files when the target format is clear and files are editable.
2. **Formatting audit checklist** when requirements are unclear or manual Word/PDF actions are needed.
3. **Annotated issue list** with severity:
   - `Blocker`: likely prevents submission
   - `Major`: likely non-compliant with journal instructions
   - `Minor`: style or consistency issue
4. **Two-version output** when needed:
   - full author version
   - blind-review version
5. **Format QA report** when visual quality was poor or a conversion/render loop was performed:
    - source route and adapter used
    - defect ledger before/after
    - commands or manual checks run
    - rendered artifacts inspected
    - remaining manual actions
6. **Output index / version ledger update** for multi-version formatting work:
   - active current file path and status
   - short version filename and core change token
   - source manuscript/template/rule authority
   - QA proof path
   - archived or superseded outputs

## Default Checklist

When producing an audit, use this concise structure:

```markdown
## Formatting audit

Target: [journal/style]
Source: [files inspected]
Render route: [native Word / LaTeX / Quarto-Pandoc / rticles / audit-only]
Status: [ready / needs minor fixes / needs major fixes / blocked]

### Revision granularity and field integrity
- Editable span / maximum edit unit: [...]
- Protected context unchanged: [yes/no/not applicable]
- Citation-manager source of truth and linkage: [...]
- Field code/result/count/type round trip: [verified/blocked/not applicable]
- Track Changes exact-range QA: [passed/failed/not applicable]

### Blockers
- ...

### Major issues
- ...

### Minor issues
- ...

### Visual/layout QA
- Rendered artifact inspected: [yes/no/path]
- Pages/sections checked: [...]
- Line spacing checked: [1.25 / target override / not checked]
- Page-number boundary checked: [cover/abstract/TOC blank; first body page starts at required number; following body pages continuous; footer crops/PDF pages inspected]
- Remaining defects: [...]

### Table/caption/heading QA
- Every numbered figure/table cited in ordinary body prose: [yes/no/list missing labels]
- Figure container paragraphs and Word table objects centered: [yes/no/target override]
- All tables checked for cross-page behavior: [yes/no]
- Tables crossing pages: [none/list with page locators]
- Table headers repeated / row splits / notes verified: [yes/no/not applicable]
- Figure/table captions centered: [yes/no]
- English body / caption font checked: [Times New Roman 11 pt / Times New Roman 10 pt / target override]
- Heading hierarchy and styles checked: [yes/no]
- TOC/navigation structure checked: [yes/no/not applicable]

### MathType/equation QA
- Display equations centered automatically: [yes/no/not required]
- Equation numbers right-aligned: [yes/no/not required]
- Inline variables converted to MathType/equation-compatible objects: [yes/no/not required]
- Editable equation objects verified in Word: [yes/no/not available]

### Do not change
- numerical results, figure/table data, citation set, author metadata unless confirmed

### Next step
- ...
```

## Relationship to Other Skills

- Use `nature-writing` before this skill if the manuscript sections are not yet drafted.
- Use `nature-reviewer` before this skill if scientific structure or evidence strength is still unstable.
- Use `nature-polishing` before this skill if prose quality still needs revision.
- Use `nature-writing` after this skill for journal portal checklist, cover letter, and submission package decisions.
