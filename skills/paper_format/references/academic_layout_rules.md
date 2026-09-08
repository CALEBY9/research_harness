# Academic Layout Rules Baseline

Use this reference when auditing academic-paper layout. Target journal instructions or a verified template always override this baseline.

## Source Hierarchy

1. Target journal author instructions, article type, and official Word/LaTeX template.
2. Publisher style guide for the exact venue or society.
3. National or style-manual baseline:
   - GB/T 7713.2-2022, `Presentation of academic papers`, for Chinese/general academic-paper composition and layout.
   - IEEE Editorial Style Manual / IEEE MathType guide for engineering-style equation numbering and MathType use.
   - APA Style for APA manuscripts, especially paper format, headings, line spacing, and table/figure setup.
4. User project defaults when no target source is available, currently body 11 pt, captions 10 pt, line spacing 1.25.

## GB/T 7713.2 Academic-Paper Baseline

Machine-check these where the DOCX structure permits; otherwise require rendered Word/PDF inspection.

- Structure: front matter, main body, and appendices; title, author information, abstract, keywords, introduction/main body, references are core elements.
- Figures: figures should be numbered; a figure title follows the figure number and is placed below the figure. If a multi-part figure continues across pages, place the figure number/title after all parts.
- Tables: tables should be numbered; table number and title are placed above the table and should preferably be centered. Continued tables should be marked as continued and repeat the table header.
- Mathematical expressions: inline math is generally preferred when it fits in text; numbered, large, or later-referenced equations should be displayed on a separate centered line, with the equation number at the far right of the same line or the final line of a broken equation.
- Mathematical symbols: variables, subscripts/superscripts, functions, constants, operators, vectors, matrices, and explanatory text should follow the applicable quantity/unit and mathematical-symbol conventions.
- Fonts: GB/T 7713.2 Appendix B gives Chinese font-size examples; do not silently replace a journal or user requirement with these examples. In this project, only use them as evidence that captions and body text must have a deliberate hierarchy.

## IEEE / MathType Baseline

- Equation numbers should be consecutive, without repeats or missing numbers, and flush right on the line of the equation or the last line of a multi-line equation.
- For Word manuscripts using MathType, insert display equations as display equations and numbered equations with the right-numbered option where required.
- Inline equations/variables inside paragraphs should be represented as inline equation objects when the target requires MathType/Word equation compatibility; do not use manually styled plain text as a substitute.
- Avoid manual spaces to align equations or equation numbers; alignment must survive field updates and PDF export.

## Word Layout Mechanics To Verify

- Captions should use Word caption/style machinery or a stable paragraph style, not manual local formatting.
- Cross-references should be Word fields or otherwise mechanically updateable when the manuscript relies on them.
- Long tables must be checked in a rendered Word/PDF artifact. Static DOCX XML can detect repeated-header flags but cannot prove page breaks, orphaned captions, notes, or overlap.
- Header rows should repeat when a table spans pages; row-breaking behavior must match the journal/table rule.
- Clean final documents should not contain unresolved comments, tracked changes, internal TODOs, or process-language markers.

## Checker Policy

- Run `docx_layout_audit.py` with `--academic-profile gb7713` for generic Chinese/general academic-paper layout when no target journal is provided.
- Run `--academic-profile ieee` when IEEE-style equation/table/figure placement is the relevant baseline and no exact IEEE template is available.
- Run `--academic-profile journal` only when exact target instructions are being checked externally or through a template; unresolved target rules remain findings.
- Static-only audits are triage. Submission-ready approval requires Word open/export plus page-level PDF inspection.
