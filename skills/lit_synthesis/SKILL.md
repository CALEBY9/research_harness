---
name: lit_synthesis
description: Plan and write systematic reviews, meta-analyses, or scientometric environmental-science manuscripts.
---

Use subagents only when the user explicitly requests delegation; otherwise perform role checks locally.

# Literature Synthesis — 系统综述 / 元研究 / LLM 流水线综述 (v1.0)

Plan or write a synthesis manuscript for: **$ARGUMENTS**

## Quick Trigger / Stop Card

- Use when: planning or writing a systematic review, meta-analysis, scientometric/meta-research manuscript, or producing a formal cross-paper synthesis asset from a bounded corpus.
- Do not use when: the task is ordinary KB query/build, single-paper reading, open-ended discovery, or a small primary-article literature set that `nature-writing` can organize from verified evidence cards.
- Required inputs: review/synthesis question, corpus or search boundary, screening/coverage state, full-text status, synthesis-critical evidence cards, review type, and target genre.
- Output / handoff: protocol/screening assets when applicable, Review Literature Matrix, `CROSS_PAPER_SYNTHESIS_MATRIX` for KB-assisted writing, unresolved gaps, and handoff to `nature-writing`.
- Return / stop conditions: incomplete search/screening -> return to `nature-academic-search`; unverified core evidence -> `KB_EVIDENCE_PACK_INCOMPLETE` / `nature-paper-card`; unresolved disagreement or heterogeneity -> `KB_SYNTHESIS_UNRESOLVED`.
- Validation: source identity and locator coverage, contradiction retention, review-type requirements, question-driven synthesis, and no retrieval-fragment-to-prose shortcut.

## Scope

本 skill 覆盖以下三类综合研究；目标期刊是否接收相应体裁，以当前官方作者指南为准：

### Type 1 — 经典 Systematic Literature Review (SLR)
- PRISMA 2020 / PRISMA-ScR / PRISMA-EnvEvid 标准
- 主要回答 "什么是当前证据状态" 类问题
- 例: "Effects of nitrogen deposition on temperate forest carbon sequestration: a global meta-analysis"
- 投稿目标: *Nature Ecology & Evolution / Global Change Biology / Earth-Science Reviews*

### Type 2 — Meta-analysis (定量综合)
- 效应量标准化 + 异质性分析 + 发表偏倚检测
- 主要回答 "效应大小是多少 + 在什么条件下变化"
- 例: "Quantifying the impact of urban green space on PM2.5: a global meta-analysis of 1,247 studies"
- 投稿目标: *Nature Sustainability / Nature Climate Change / Environmental Science & Technology*

### Type 3 — Scientometric / Meta-research (元研究)
- 不综合科学结论本身,综合**领域如何进展**的证据
- 主要回答 "这个领域是真在突破还是结构性停滞"
- 例: "Has a rapidly expanding modelling field delivered mechanistic understanding or mainly predictive performance?"
- 投稿目标: *Nature / Science / Nature Communications* (因 broad readership)

**举例**:大规模 LLM-augmented 文献流水线 + 领域宣告框架的实证检验类研究属于 **Type 3**——这是 leverage 最大但审稿标准也最严格的体裁。项目特定案例应放在 `_project_notes/<project>/`。

---

## 为什么独立成 skill

`nature-academic-search` 是当前的多源检索、引文影响审计和参考文献导出 owner；Web of Science 只是其中一个按需来源，不再由独立本地 skill 承担。

但**综述论文本身**的写作有特殊要求:
- 方法学透明度 (PRISMA flowchart, exclusion 理由记录)
- LLM 提取的偏差量化 (本研究 inter-rater reliability with human gold standard)
- Heterogeneity / publication bias 的统计处理
- Multi-axis narrative framework 的合法性论证
- 系统综述 vs narrative review 的 editorial 差异

这些不是 retrieval skill 能 cover 的——需要独立的 synthesis methodology skill。

---

## Step 0 — 综述类型决策

进入工作流之前,先决策本综述属哪一型。错型会导致整稿不可发。

### Q1. 你的研究问题是什么?

| 问题形式 | 类型 |
|---|---|
| "X 对 Y 的效应是多少?" | Type 2 (Meta-analysis) |
| "X 与 Y 的关系如何随条件变化?" | Type 2 |
| "目前关于 X 的证据状态如何?" | Type 1 (SLR) |
| "X 的研究方法有哪些, 各自局限?" | Type 1 (Methodological SLR) |
| "X 领域过去 N 年是否有真实科学进步?" | Type 3 (Meta-research) |
| "X 领域当前是否存在结构性问题(如 publication bias / 方法集中 / 数据孤岛)?" | Type 3 |

### Q2. 核心证据是什么?

- 数值效应量(effect sizes, CIs) → Type 2 必须
- 二分类编码(method type / data type / region) → Type 1 或 Type 3
- 元层级分析(领域演化、引用网络、术语漂移) → Type 3

### Q3. 是否有 LLM 自动提取?

- 全人工提取 → 经典 SLR/Meta 路径,Cochrane 标准适用
- LLM 半自动 + 人工抽查 → **必须**额外做 inter-rater reliability + bias 报告
- LLM 全自动 → Nature 子刊**当前** (2026) 通常**不接受** main 分析全部 LLM 提取,需要 sufficient human gold standard 验证

### Q4. 论文体裁选择
- Letter / Communication: 通常不接收 SLR(篇幅不够)
- Article: SLR / Meta / Meta-research 都可以
- Perspective / Review: 邀请制, 不投递
- Analysis / Outlook (NCC, NS): 适合 Type 3 元研究

---

## Step 1 — 协议先行 (Pre-registration)

Nature 子刊近 3 年开始**强烈期待**(部分 mandatory) systematic review 与 meta-analysis 提供 pre-registered protocol。

### 协议必备项

```markdown
## SLR Protocol [DOI / OSF / PROSPERO 注册号]

### Research Question
- PICO / PECO / PIO format
- Population: ...
- Exposure / Intervention: ...
- Comparator: ...
- Outcome: ...

### Eligibility Criteria
- Inclusion:
  - Empirical study (primary data)
  - Time window: 2019-01-01 to 2025-12-31
  - Language: English
  - Document type: peer-reviewed journal article
- Exclusion:
  - Pre-prints (or include with sensitivity)
  - Conference abstracts (or include with sensitivity)
  - ...

### Information Sources
- Web of Science Core Collection
- Scopus
- Engineering Village (for engineering domains)
- 注:不要只用一个 database — Cochrane 要求 ≥ 2

### Search Strategy
- Boolean string per database
- Date of search execution
- Replicability: 提供完整 query string,不要 paraphrase

### Selection Process
- Screening: title/abstract → full-text
- Reviewers per record (建议 ≥ 2 + 第三方仲裁)
- Software (Covidence / Rayyan / 自建)

### Data Extraction
- Extracted variables list (with codebook)
- Independent extraction per record
- Inter-rater reliability: 报告 Cohen's κ 或 Krippendorff's α

### Risk of Bias Assessment
- Tool: ROBINS-I / RoB 2 / Custom (justified)
- Independent assessment per record

### Synthesis Methods
- Meta-analysis: random vs fixed effect, heterogeneity (I²), publication bias (funnel + Egger)
- Narrative: framework justification

### Deviations from Protocol
- 留这一节 — 任何与 protocol 的偏离必须显式记录
```

**关键认识**: 顶刊 reviewer 几乎一定会要 pre-registration。**如果你已经做完 review 才意识到要 pre-register, 你已经晚了** — 应在 `nature-academic-search` 检索设计阶段就 register。

---

## Step 2 — Search Strategy 的 Reproducibility

顶刊 reviewer 必查的事:
- Search string 是否完整给出(不能 paraphrase)
- Search 日期是否记录
- 不同 database 的 query 是否各自给出(语法不同)
- Search 是否在某时间窗内多次重复(避免 search drift)

### 反面例
> "We searched Web of Science for relevant studies on offshore wind and aquaculture."

**问题**: 不可复现,reviewer 重做时找不到一样数量的结果。

### 正面例
```
Database: Web of Science Core Collection (SCI-EXPANDED, SSCI)
Date of search: 2025-08-15 (re-executed 2026-01-12 to capture new publications)
Time window: 2010-01-01 to 2025-12-31
Document types: Article, Review

Query string (TS = Topic):
  TS = (("offshore wind*" OR "marine wind energ*" OR "OWF*")
        AND ("aquacultur*" OR "mariculture" OR "fish farm*" OR "shellfish")
        AND ("co-locat*" OR "multi-use" OR "integration" OR "co-existence"))

Records retrieved: 1,247
After deduplication: 1,103
After title/abstract screening: 287
After full-text screening: 86
```

---

## Step 2.5 — Screening Matrix and Completeness Stop

For systematic review, PRISMA-style screening, evidence maps, or any synthesis that claims reproducible coverage, keep a lightweight screening matrix before writing synthesis claims:

```markdown
| Title | Authors | Year | Source | DOI / PMID / arXiv | Abstract cue | Include decision | Exclusion reason | full_text_status | Notes |
|-------|---------|------|--------|--------------------|--------------|------------------|------------------|------------------|-------|
```

Rules:

- `Include decision` must be `include`, `exclude`, or `maybe`; excluded records need an explicit `Exclusion reason`.
- Deduplicate by DOI, PMID/PMCID, arXiv ID, then normalized title/year/first author.
- Record `full_text_status` for records that require full-text extraction, and do not treat paywall, anti-bot block, HTML-not-PDF, and no-open-PDF as the same failure.
- Stop before claiming systematic-review completeness if only one database was searched, search strings were not recorded, paywalled full texts block required extraction, eligibility criteria are ambiguous, or formal risk-of-bias assessment is needed but not planned.

This matrix is a gate for reproducibility, not a replacement for `nature-academic-search` coverage audit or `nature-paper-card` evidence extraction.

---

## Step 2.6 — Review Literature Matrix Handoff

For narrative reviews, methodological SLRs, scoping reviews, evidence maps, or meta-research papers, do not hand off a loose bibliography to writing. Before synthesis claims are drafted, keep a compact review literature matrix that preserves the search-to-analysis bridge:

```markdown
## Review Literature Matrix

| Field | Required content |
|-------|------------------|
| review_type | narrative / systematic / scoping / methodological SLR / meta-research |
| taxonomy | category, subcategory, rationale, and whether each category is mature or emerging |
| search_log | source, query, date, hits, screened, included |
| coverage_matrix | category, target, actual, classic papers, recent papers, gap_status |
| core_set | Top N core papers with selection rationale and full_text_status |
| deep_read_required | synthesis-critical papers that must go to `nature-paper-card` before coding |
| comparison_tables | method / data / metric / region / mechanism dimensions tied to the research question |
| unresolved_gaps | missing categories, access blockers, weak source quality, or uncertain taxonomy decisions |
```

Rules:

- Treat numeric targets such as `Top N`, per-category counts, or recent-literature ratios as review-specific calibration, not universal thresholds.
- Do not require Exa, ArXiv, Semantic Scholar, Papers With Code, Zotero, MinerU, WoS, Scopus, or any other source as a hidden default; use the sources selected by `nature-academic-search` and record unavailable sources explicitly.
- Use the matrix to decide which papers need `nature-paper-card`, which comparison tables are needed, and which taxonomy gaps block strong synthesis claims.
- For systematic-review completeness claims, this handoff supplements the screening matrix; it does not replace inclusion / exclusion reasons, full-text status, risk-of-bias planning, or protocol deviations.
- When the input is a local KB/RAG corpus and the output will feed manuscript prose, load `../shared-references/kb-to-manuscript-evidence-bridge.md`. Consume verified `KBE###`/`E###` cards and emit the bridge's `CROSS_PAPER_SYNTHESIS_MATRIX`; do not treat retrieval rank, paper count, or majority direction as consensus. Preserve contradictory evidence, contextual heterogeneity, rival explanations, and `INSUFFICIENT` rows. Return `KB_EVIDENCE_PACK_INCOMPLETE` or `KB_SYNTHESIS_UNRESOLVED` instead of drafting across a broken handoff.

---

## Step 3 — LLM 提取的特殊要求

Large-scale LLM-augmented synthesis 会被 Nature 子刊严格审查,以下 4 项**必须**有:

### 3.1 Human Gold Standard
- 抽样 N 篇(通常 100-500,根据总量),由人工提取,作为 ground truth
- 抽样必须分层(by year × domain × method),不要 random
- 抽样比例随总量递减,但绝对数量 ≥ 100
- 对 gold-standard papers 或 synthesis-critical papers，先用 `nature-paper-card` 生成 claim-level extraction 与 evidence locations，再编码进 review matrix

### 3.2 LLM-Human Agreement Quantification
- 每个提取字段单独计算 agreement
- 数值字段: MAE / MAPE / Bland-Altman
- 类别字段: Cohen's κ (binary) / Krippendorff's α (multi-class)
- 报告 per-field, **不要**只报告 overall

### 3.3 LLM Bias Audit
- Domain bias: LLM 在哪个学科表现更差?
- Year bias: 早期论文(术语不同)表现?
- Length bias: 短论文 vs 长论文?
- Language bias: 即使全英文,母语 vs 非母语作者写的论文表现差异?

### 3.4 Self-consistency Check
- 同一论文喂多次,LLM 输出是否一致?
- 报告 within-paper variance

**Reviewer 一定会问的**:
1. "如果 LLM 系统性低估了某类发现的频率,你的 narrative 还成立吗?" → 你需要做 sensitivity analysis 排除这种可能
2. "你的 inter-rater reliability 在哪里?" → 必须有
3. "你能复现 LLM 提取吗?" → API 版本、temperature、prompt 全部公开,且最好 fix-seeded

---

## Step 4 — Multi-axis Narrative Framework 的合法性

Type 3 元研究通常用 multi-axis 框架组织(例: 方法集中、数据孤岛、机制证据不足、应用场景偏置等 structural axes)。这种框架的**合法性**(顶刊接受度)取决于:

### 4.1 框架是否 falsifiable
每条 axis / 类别必须能被数据**反驳**。

- ❌ "DL 应用规模集中" — 太模糊,什么程度算集中?
- ✅ "Top 10 数据集占据 SLR 论文样本的 X%, top 10 模型架构占 Y%" — 可被反驳的具体度量

### 4.2 框架是否 pre-specified
框架在 Step 1 protocol 中明确,不是数据看完后 post-hoc 提炼出来。

post-hoc 框架不一定不合法,但**必须**显式声明 "exploratory" 而不是 "confirmatory"。

### 4.3 框架是否 mutually exclusive 或 conceptually independent
若有 3 个 axis,3 个之间是否独立?如果 axis A 必然导致 axis B,那就只是一个 axis,不是 3 个。

**原则**: 良好的 multi-axis framework 需要 conceptually orthogonal axes；例如一个 axis 描述 disciplinary depth, 另一个 axis 描述 sociological or infrastructural structure。在 Methods 中需要论证这种正交性。

### 4.4 框架是否对照 prior frameworks
顶刊审稿人会问: "为什么不用 Reichstein 2019 / Karpatne 2017 / Camps-Valls 2021 的现有框架?" → 必须有 1 段论证你的框架与 prior 的差异和必要性。

---

## Step 5 — 综述论文的 Nature 风格特殊性

### 5.1 Lead Pattern (重选,与 primary research 略不同)

- **Lead Type R-A — Field accumulation paradox**: "Despite N publications and decade of effort, [problem] remains [unresolved/contested]"
- **Lead Type R-B — Promised vs delivered**: "[Approach] has been promised to deliver [X], but synthesis of N studies shows that [actual delivered Y]"
- **Lead Type R-C — Hidden structural pattern**: "Synthesis of N studies reveals an unrecognized structural pattern: [...]"
- **Lead Type R-D — Methodological limit hit**: "Field-wide synthesis identifies a methodological constraint that no individual study could detect: [...]"

Use R-B when the paper tests a promised-versus-delivered claim; use R-C when the synthesis reveals a structural pattern that individual studies could not see.

### 5.2 Methods at the front (与 primary research 相反)
SLR / Meta 在 Nature 子刊的 Methods 通常**前置**或**与 Results 并行展开**——读者必须先信任你的方法,才会信任你的 finding。Primary research 的 Methods 在末尾不适用 SLR。

### 5.3 PRISMA flowchart 必备
作为 Fig 1 或 Extended Data Fig 1。Reviewer 不看 PRISMA flowchart 就直接 reject。

### 5.4 Display item 角色
- Fig 1: PRISMA flowchart **或** conceptual claim preview (取决于体裁)
- Fig 2: Main descriptive synthesis (e.g., 时间趋势 + 学科分布)
- Fig 3: Quantitative pattern (effect size forest plot / heterogeneity / framework projection)
- Fig 4: Counterfactual or generalization (subgroup analysis / sensitivity / displacement claim)
- Extended Data: Risk of bias, publication bias funnel, sensitivity analyses, full search strings

### 5.5 引用密度
SLR / Meta 在 Nature 子刊允许较高引用密度 (80-150 in main),不像 primary research letter 通常 ≤ 30。但**每条引用必须服务论证**——单纯堆引用 reviewer 立即 reject。

---

## Step 6 — Risk of Bias 处理

### 6.1 Internal validity (study-level)
对每篇纳入研究评估:
- Selection bias / sampling
- Measurement bias
- Confounding control
- Reporting completeness
- 工具: ROBINS-I (non-randomized), RoB 2 (RCTs), custom (justified)

### 6.2 External validity (synthesis-level)
- Geographic coverage bias (e.g., 80% 论文是欧美数据)
- Domain coverage bias (e.g., 95% 应用是 supervised learning)
- Temporal sampling bias (e.g., 跳过某些年份)

### 6.3 Publication bias
- Funnel plot (visual)
- Egger's regression test
- Trim-and-fill correction
- Note: small-study effects 可能与 publication bias 混淆

### 6.4 Pipeline-introduced bias (LLM 流水线特有)
- LLM 提取错误的 bias 方向 (是否系统性高/低估某类发现?)
- 提示工程的 framing bias (prompt 中的措辞是否引导 LLM)
- API 版本漂移 (中途换模型版本会引入 bias)

---

## Step 7 — Quantitative Synthesis (Meta-analysis 限定)

如果是 Type 2:

### 7.1 Effect size 标准化
- 选 Hedges' g / Cohen's d / log response ratio (lnRR) / 风险比
- 标准化的合理性必须论证 (不是 default)

### 7.2 异质性
- I² 报告 (low <25%, moderate 25-75%, high >75%)
- τ² 与 prediction interval (关键)
- subgroup 分析 + meta-regression

### 7.3 模型选择
- Fixed-effect: 假设单一真实效应
- Random-effects: 真实效应是分布
- 多数环境科学研究用 random-effects (推荐 default)

### 7.4 Sensitivity analyses
- Leave-one-out
- 排除高 risk-of-bias 研究后重做
- 排除 LLM-extracted records 后重做(若适用)
- 不同 effect size metrics 间一致性

---

## Step 8 — Section-by-Section 写作模板

```markdown
# Title
[12-16 词;包含 N studies, 系统综述/meta-analysis, 主 question 关键词]

# Abstract (200 词)
1. Lead pattern R-A/R-B/R-C/R-D 一句
2. Specific gap with stake (1 句)
3. 综述方法 (database, query, time window, N records → final N) (1 句)
4. Headline finding with quantitative pattern (1 句, 含数字 + CI)
5. Underlying mechanism / structural pattern (1 句)
6. Generalization boundary OR displacement claim (1 句)
7. Implication (1 句)

# Introduction
- Lead pattern 段
- Field accumulation context (N papers, time, prior frameworks)
- Specific gap (用 editorial-judgment Q1-Q5 自检)
- Approach overview (本研究方法 + 为什么这种综述类型适合)

# Methods (前置 — SLR/Meta 特殊)
- Protocol & registration
- Eligibility criteria
- Search strategy (完整 query string)
- Selection process (PRISMA flowchart 引用)
- Data extraction (codebook, LLM pipeline if any, inter-rater)
- Risk of bias assessment
- Synthesis methods (quantitative + narrative)

# Results
- PRISMA selection summary (含 Fig 1 引用)
- Descriptive synthesis (Fig 2)
- Main synthesis pattern (Fig 3) — meta-analysis pooled effect / 框架轴向投射
- Subgroup / sensitivity (Fig 4)
- Risk of bias outcomes (Extended Data)

# Discussion
- 主 finding 重述 + magnitude
- Displacement claim (本综述推翻/精化的 prior 共识)
- Mechanism / structural reasoning
- Generalization 边界 (geographic / temporal / methodological)
- Limitations
  - 包含 LLM pipeline limitations (若适用)
  - 包含 publication bias residual
  - 包含 search drift
- Implication

# Methods Online (extended)
[Detailed search strings, codebook, full statistical specifications]
```

---

## Step 9 — 项目特定建议 (此处不再嵌入)

> 项目特定的投稿目标排序、必做事项、desk reject 警告、cover letter 论点等,已**移出本通用 skill**,保存在 `_project_notes/<project>/submission_strategy.md`。
>
> Do not list project-specific cases in this generic skill.
> 新项目使用本 skill 时,在 `_project_notes/` 下新建子目录,把项目特定判断写在那里——保持本 skill 主体的研究方向无关性。

---

## 与其他 skill 的接口

按需使用 `nature-academic-search` 检索、`nature-paper-card` 核验关键原文；本 skill 负责系统综合方法与证据资产。需要形成论文时交给 `nature-writing`；审稿、语言润色和修回分别由 `nature-reviewer`、`nature-polishing` 和 `nature-response` 承担。已有充分输入时直接开始，不自动串行加载所有技能。

---

## 关键认识

> 综述论文不是"读了很多文献"的奖励,是**对一个领域的 epistemic statement**。
>
> Type 3 元研究尤其敏感:你不是在综合科学结论,是在**评判科学共同体的进展**——这意味着审稿人会同时是被你 implicit 评判的对象。Push back 必然存在,framework 的合法性必须双重稳固。
>

---

## 来源

- Page MJ et al. (2021) PRISMA 2020 statement. *BMJ* 372:n71
- Higgins JPT et al. (eds) Cochrane Handbook for Systematic Reviews of Interventions (v6.4, 2023)
- Stewart GB et al. (2023) Meta-research in environmental science: emerging standards
- Wagner S et al. (2024) Reporting standards for LLM-augmented evidence synthesis (preprint)
- Reichstein M et al. (2019) Deep learning and process understanding for data-driven Earth system science. *Nature* 566:195-204
- Project-specific LLM extraction protocols should be documented in `_project_notes/<project>/` rather than embedded in this generic skill.
