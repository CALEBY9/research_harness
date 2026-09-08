# Nature Communications — formatting facts

Authoritative facts about Nature Communications formatting requirements. Used by both `nature-polishing` and `nature-writing` when `journal=nat-comms`. This file holds the **facts**; each skill's `static/fragments/journal/nat-comms.md` adds the **action layer**.

> Article limits and submission/policy corrections checked on 2026-09-06 against the official pages linked below. Verify the applicable content type and current requirements at submission; distinguish recommended lengths from hard maxima.

## Article types and limits

| Article item | Current guidance |
|---|---|
| Main text | Ideally 5,000 words, excluding Abstract, Methods, References and Figure legends; recommended length, not a blanket rejection cutoff |
| Abstract | At most 200 words, no references |
| Title | At most 15 words |
| Methods | Typically less than 3,000 words; preserve replication detail |
| References | As a guide, no more than 70 |
| Figures/tables | Up to 10, commensurate with length; fewer than 2,000 words: no more than 4 |
| Figure legends | At most 350 words each |

Source: [Article guidance](https://www.nature.com/ncomms/submit/article).
For other content types, use the [content-type index](https://www.nature.com/ncomms/submit/content-types);
do not extrapolate Article limits or reuse an unverified historical limit table.

### Word-count scope

Count Introduction, Results and Discussion separately from Methods. For example,
4,800 main-text words plus 1,500 Methods words is not a 6,300-word main-text
overrun. Report actual component counts before proposing any substantive cuts.

## Abstract

- Use the Article maximum above
- Unstructured single paragraph
- No citations
- Spell out abbreviations at first use
- Check requested keyword fields in the current submission system; do not infer a requirement from an old template
- Include quantitative results where possible (`94% conversion with 99% selectivity`, not `significant improvement`)
- Lead with the finding, not the background — editors triage on the abstract

## Figures and display items

- Use the length-dependent Article display guidance above (figures + tables combined).
- **No Extended Data tier** (unlike *Nature*). Additional items go into Supplementary Information (downloadable, but still peer-reviewed).

### Resolution and format

| Parameter | Requirement |
|---|---|
| Line art resolution | 1,200 dpi minimum |
| Halftone / photo resolution | 300 dpi minimum |
| Combination (line + halftone) | 600 dpi minimum |
| File formats | TIFF, EPS, PDF, or JPEG |
| Color mode | RGB (online-only journal) |
| Single-column width | 89 mm |
| Double-column width | 183 mm |
| In-figure font | Arial / Helvetica / sans-serif, 5–7 pt |
| Panel labels | Lowercase bold letters (`a`, `b`, `c`, …) |

Online-only publication means: color is free, no CMYK requirement, design for screen reading (sufficient contrast, colorblind-friendly palettes, clear labels).

### Multi-panel figures

Common and accepted. A single figure with panels `a`–`l` is normal. No formal panel cap, but readability is enforced informally — if panel labels need magnification, the figure has too many panels.

## References

- **Style**: standard Nature reference style
- **In-text**: superscript numbers, sequential by first appearance. Multiple: `^1,2`. Ranges: `^3–7`.
- **Guidance**: use the Article reference-count guidance above; check other content types separately
- **Format example**:
  ```
  1. Smith, A. B., Johnson, C. D. & Williams, E. F. Title of article. Nat. Commun. 16, 1234 (2025).
  ```
- Author names: last name, comma, initials with full stops; use all authors unless six or more, then first author followed by et al. ([How to submit](https://www.nature.com/ncomms/submit/how-to-submit))
- `&` before the last author
- Journal names abbreviated per ISO 4
- Volume in **bold**
- **Article number** (e.g., `1234`), not page range — Nature Communications is online-only
- Year in parentheses
- DOIs encouraged
- Reference list appears **before** the Methods section in the published article, even though Methods is part of the main text in the manuscript

## Supplementary Information

- Single PDF or multiple files; peer-reviewed
- Organize with a table of contents if it exceeds 10 pages
- Labels: `Supplementary Fig. 1`, `Supplementary Table 1`, `Supplementary Note 1`, `Supplementary Methods`
- Large tables → separate Excel files

## Mandatory statements

- **Data Availability statement** — required for original research. Identify the minimum supporting dataset and access conditions; provide applicable repositories/accessions. Mandatory deposition applies to specified data types. Disclose controlled-access and third-party restrictions rather than promising unauthorized public release.
- **Code availability** — describe access to custom code central to the claims, including restrictions; previously unreported central code must be available to editors/reviewers at submission. Do not treat one platform or a newly minted DOI as a universal prerequisite.
- **Author contributions** — in the manuscript after the main text
- **Competing interests** — in the manuscript
- **Reporting Summary** — complete the applicable research-reporting forms requested for the study type; use the current journal instructions and editor requests.

Sources: [Reporting standards](https://www.nature.com/ncomms/editorial-policies/reporting-standards) and [submission instructions](https://www.nature.com/ncomms/submit/how-to-submit). Neither policy authorizes the agent to upload or release data.

## Cover page elements

- **Title**: concise, informative, no abbreviations; recommended ≤ 15 words
- Author names with superscript affiliation numbers
- Affiliations with full institutional addresses
- Corresponding author(s) with email
- ORCID iDs required for corresponding author, encouraged for all

## Cover letter (separate upload)

Editors use the cover letter for triage. Do not waste it on generic statements like "broad interest." State explicitly:

1. What the finding is (one sentence)
2. What makes it new (one sentence)
3. Why it matters across multiple scientific disciplines (one sentence)

## Open access and licensing

- Fully open access — APC applies (verify current rate; substantial)
- Default license: **CC BY 4.0**
- Some funders (e.g., UKRI) require CC BY; others allow CC BY-NC — check funder requirements

## Transparent peer review

- For primary research submitted from 2022-11-01, reviewer comments and author rebuttals accompany publication. The former author opt-out belonged to the earlier scheme; do not offer it as a current default option.
- Resolve sensitive-content concerns with the editor under the current process; do not publish correspondence autonomously.
- Source: [Transparent Peer Review FAQ](https://www.nature.com/ncomms/submit/tpr-faq).

## Manuscript formats

- Initial submissions may combine text and figures in one Word, TeX/LaTeX or PDF file up to 30 MB.
- Revision text is supplied in one Word or TeX/LaTeX file; figures separately. The journal does not require a Word manuscript template.
- Standard LaTeX classes are accepted. Include the references in the submitted main .tex file; a working .bib is useful during drafting but is not the submitted reference list.
- Source: [How to submit](https://www.nature.com/ncomms/submit/how-to-submit). Do not convert a valid draft to a different template merely to satisfy an old local convention.

## Common desk-rejection / production-hold patterns

1. **Wrong word-count scope** — including Methods in the main-text count can trigger unnecessary scientific cuts
2. **Reporting Summary completed as checkbox** — vague `N/A` responses, no explanation for outlier exclusions, missing blinding info, weak power calculations → generates specific revision requests
3. **Unverifiable data access** — check required deposit/access arrangements and disclose restrictions; never fabricate an accession
4. **Generic cover letter** — fails to establish cross-disciplinary significance; signals authors haven't considered scope fit

## Transfer from Nature

Manuscripts rejected from *Nature* can transfer with reviews intact. Editors may decide on existing reviews or send for additional review. Follow the transfer/editor instructions for the current stage; Methods remains excluded from the Article main-text count.
