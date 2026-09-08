---
name: nature-image2-prompt
description: Generate or audit Image 2-style prompts for academic conceptual figures from manuscripts, reviewer comments, diagnostics, or references. Use for 机制图、系统动力学图、图形摘要, workflow or SVG-style canvases, and reviewer-driven figure prompts; not for plotting data-bearing figures.
---

# Nature Image 2 Prompt

## Purpose

Generate an Image 2-ready prompt that turns manuscript content, reviewer requirements, and reference figures into a publication-style scientific figure. The prompt must specify structure, mechanisms, visual grammar, text rules, and quality checks rather than relying on vague phrases such as "make it Nature style" or "include reviewer mechanisms."

Use this skill for non-data-bearing or conceptual figures. For data-bearing maps, plots, curves, uncertainty bands, or statistics, preserve script/GIS/statistical outputs and use Image 2 only for non-data annotation drafts.

## Workflow

1. Identify the figure type:
   - **Edit existing reference figure**: preserve layout, style, and spatial organization; request local modifications only.
   - **New mechanism/workflow figure**: define visual hierarchy, modules, flows, and checks from the content.
   - **AI/CS method or model-architecture figure**: use the `AI/CS Method Figure Triage` from `fig_nature` when available; distinguish paper type, novelty locus, training/inference/evaluation lanes, module relations, and data-bearing placeholders.
   - **System dynamics canvas**: require Vensim-like stock-flow notation, curved causal arrows, stocks, flows, valves, and clouds; forbid infographic cards and decorative icons.

2. Resolve the `Logic Wireframe Intake Gate`. For a new or substantively redesigned conceptual, mechanism, method/workflow, technical-route, research-framework, or graphical-abstract figure, consume the frozen wireframe from `fig_nature` or `figure_spec_builder` before drafting prompt language.

2a. Resolve the `Visual Direction Intake and Prompt Preflight Gate`. For an applicable figure, consume only the selected direction and its visual render projection; never ask the image model to choose among unselected layouts.

3. Extract requirements into concrete drawable elements:
   - Reviewer concern or manuscript change.
   - Required visual element.
   - Required connection or causal arrow.
   - Existing label to replace or remove.
   - Failure mode if absent.

4. Convert each requirement into prompt constraints:
   - Use actual stock/flow/auxiliary labels, not only symbols or claims.
   - Specify exact arrows and whether they are solid, dashed, dotted, color-coded, or policy-switch links.
   - Specify which elements must be kept, replaced, added, or removed.
   - Include spelling-sensitive labels exactly.

5. Add anti-AI-art controls:
   - `flat vector style`, `clean academic diagram`, `white background`, `simple geometric shapes`, `consistent stroke width`, `high contrast`.
   - `no gradients`, `no shadows`, `no glow`, `no 3D`, `no texture`, `no realistic rendering`, `no decorative icons`, `no stock-photo style`.
   - For Vensim-style diagrams: also say `not an infographic`, `not a block diagram`, `not a panel-based schematic`.

6. Add a final checklist inside the prompt. The checklist must be concrete enough that a missing mechanism can be flagged without rereading the manuscript.

## Logic Wireframe Intake Gate

For an applicable figure, require the one-sentence objective, status, mainline node IDs, supporting branches, complete node table, and complete edge table before writing the final prompt. Treat these fields as frozen scientific content:

- Preserve every node ID, reader-facing label, role, input/precondition, transformation/function, output/effect, evidence/source locator, and claim/novelty role.
- Preserve every edge direction, semantic type, label, evidence/source locator, and `must_not_imply` boundary.
- Do not add, drop, merge, rename, redirect, or causally upgrade nodes or edges. Style and layout may change only within this contract.
- Mermaid, when supplied, is a secondary preview. If it conflicts with the node/edge tables, the tables control and the conflict returns to `fig_nature`.
- `LOGIC_VALIDATED` may proceed only for an exploratory prototype. A high-stakes manuscript/submission figure requires `USER_APPROVED` or `USER_WAIVED`. A bounded edit with unchanged approved structure may use `NOT_APPLICABLE`.

Failure modes:

- Missing or `DRAFT` applicable wireframe -> `LOGIC_WIREFRAME_REQUIRED` and return to `fig_nature`.
- Incomplete node/edge fields, competing mainlines, or unclear branch attachment -> `LOGIC_WIREFRAME_INCOMPLETE`.
- Unsupported or ambiguous arrow meaning, or association/sequence presented as causality -> `ARROW_SEMANTICS_UNRESOLVED`.
- High-stakes diagram lacks `USER_APPROVED` or `USER_WAIVED` -> `LOGIC_WIREFRAME_APPROVAL_REQUIRED`.

## Visual Direction Intake and Prompt Preflight Gate

For a new or substantively redesigned conceptual, mechanism, method/workflow, technical-route, research-framework, graphical-abstract, or mixed conceptual layer whose layout is not already approved, require the `selected_visual_direction`, `visual_render_projection`, `visible_text_allowlist`, `figure_caption_division`, `negative_visual_constraints`, and passing `prompt_preflight` fields from `figure_spec_builder`.

- Preserve the selected narrative strategy, layout archetype, dominant visual spine, reader path, grouping/lanes, novelty anchor, density budget, caption burden, and traits to preserve.
- Treat the Logic Wireframe as the semantic graph and the visual render projection as the only approved visible projection. The projection may place semantic content in modules, edge/port labels, attached tags/small glyphs, caption-only items, or removed items, but may not change scientific meaning.
- Draw only text in the split visible-text allowlist. Node, edge, port, lane, group, candidate, and schema IDs are control metadata and must never be visible unless the source explicitly defines the same string as a display symbol and the allowlist includes it.
- Keep non-droppable core mechanisms and required lineage visible. Caption/body prose may explain compressed detail but cannot repair a false connector, missing core step, or unsupported topology.
- Compile negative visual constraints before style language. Add style last; style may change surface treatment and spacing only, never topology, text roles, or the selected direction.
- Do not mention, blend, or generate unselected directions. Do not create a multi-candidate raster batch by default. If the user explicitly asks to draw, generate only the selected direction unless they explicitly authorize another count.

Set this gate to `NOT_APPLICABLE` for data-only figures, bounded edits with unchanged approved structure, or existing-reference edits whose layout is explicitly frozen.

Failure modes:

- Applicable prompt lacks a selected direction or has high-stakes status other than `USER_SELECTED` or `USER_WAIVED` -> `VISUAL_DIRECTION_SELECTION_REQUIRED`.
- Prompt wording blends an unselected direction or changes the selected visual spine, reader path, grouping, or semantic invariant -> `VISUAL_DIRECTION_DRIFT`.
- Visual render projection adds/drops/renames/merges nodes, redirects/upgrades edges, or turns an intermediate variable/metric into an unsupported peer module -> `VISUAL_RENDER_PROJECTION_MISMATCH`.
- Visible wording falls outside the allowlist or exposes an internal ID/schema key -> `VISIBLE_TEXT_CONTRACT_REQUIRED`.
- A core mechanism is assigned only to caption/body prose, or any preflight field is `BLOCKED` -> `PROMPT_PREFLIGHT_BLOCKED`.

## Prompt Structure

Use this order unless the user asks for another structure:

```text
Use the uploaded reference image as the base figure. [Or: Create a new figure from the following content.]

Figure objective:
[One sentence describing the scientific figure purpose.]

Frozen logic wireframe:
Status: [LOGIC_VALIDATED / USER_APPROVED / USER_WAIVED / NOT_APPLICABLE]
Mainline: [ordered node IDs]
Supporting branches: [branch IDs, attachment points, and purpose]
Required nodes: [exact node IDs, reader-facing labels, roles, input/precondition -> transformation/function -> output/effect]
Required edges: [exact source -> target, semantic type, label, and must-not-imply boundary]
Do not add, drop, merge, rename, redirect, or causally upgrade any node or edge.

Selected visual direction:
Status and selected direction ID: [AGENT_RECOMMENDED / USER_SELECTED / USER_WAIVED and ID]
Semantic graph reference: [exact Logic Wireframe]
Narrative strategy, layout archetype, dominant visual spine, and reader path: [...]
Grouping/lanes, novelty anchor, density budget, caption burden, and traits to preserve: [...]
Do not mention, blend, or render unselected directions.

Visual render projection:
Visible modules: [...]
Edge or port labels: [...]
Attached tags or small glyphs: [...]
Caption-only and removed items: [...]
Port sides and routing corridors: [...]

Visible-text allowlist:
Node labels: [...]
Edge or port labels: [...]
Legend or caption terms: [...]
No internal node, edge, port, lane, group, candidate, file, or schema IDs may be visible.

Figure-caption division:
Must be visible: [...]
Legend or caption supported: [...]
Caption only: [...]
Body only: [...]

Negative visual constraints:
Forbidden nodes or boxes: [...]
Forbidden edges or shortcuts: [...]
Forbidden layout or style: [...]
Forbidden visible text: [...]

Content-derived revision requirements:
1. [Reviewer/manuscript requirement]
   Required elements:
   Required arrows:
   Replace/remove:
   Do not:

2. ...

Scenario or policy controls:
[Only if needed. State whether they are mechanisms, switches, or result groups.]

Base-style constraints — compile last:
[Keep/edit style, canvas, typography, colors, stock-flow rules, or Nature-style vector rules. Style cannot change topology, text roles, or the selected direction.]

Final quality checklist:
1. ...
```

## AI/CS Method Diagram Prompt QA

Use this section when the prompt is for an AI/CS method figure, model architecture, agent workflow, benchmark/evaluation schematic, or technical-route diagram. Do not use a generic "data preparation -> model training -> results" pipeline unless that is actually the paper's contribution.

Before writing the final prompt, define:

- Logic Wireframe status, ordered mainline, supporting branches, exact nodes, and exact typed/directed edges;
- selected Visual Direction status/ID, semantic graph reference, narrative strategy, dominant visual spine, reader path, grouping/lanes, traits to preserve, and passing prompt preflight;
- visual render projection, split visible-text allowlist, figure-caption division, and negative visual constraints;
- paper/method type: new architecture, dataset/benchmark, application system, empirical evaluation, survey, tool/pipeline, agent/workflow, optimization/theory, or AI-enabled domain method;
- figure role: Fig. 1 method overview, model architecture, training workflow, inference/deployment workflow, evaluation protocol, graphical abstract, or mixed method-plus-result figure;
- novelty locus: module, coupling loop, representation, objective/loss, retrieval/tool-use step, data construction, evaluation protocol, deployment constraint, or cross-domain integration;
- required modules: inputs/data, preprocessing/representation, core model or algorithm blocks, training objective or feedback, inference/output, evaluation/benchmark, and optional human/tool/environment actors;
- relation grammar: sequence, hierarchy, parallel branch, feedback loop, two-lane baseline vs proposed, actor swimlane, or input/output contract;
- data-bearing boundary: any true plot, table, metric, map, curve, heatmap, benchmark result, or uncertainty display must be a placeholder unless supplied by script/statistical output.

Prompt-level checks:

- Use paper-specific module names; avoid empty labels such as "data", "model", "results", or "optimization" unless the source uses them as formal concepts.
- Separate training, inference, evaluation, and deployment when they differ; do not let arrows imply a result or causal relation that the method does not support.
- Encode the novelty locus visually through a module, connector, loop, contrast, or constraint, not only through color or a caption.
- If comparing with a baseline, show both paths or the changed module explicitly.
- Keep labels short, exact, and typo-resistant; avoid paragraphs, pseudo-code blocks, tiny formulas, dense legends, and long acronyms inside nodes.
- Keep true results as placeholders such as `script/statistical output placeholder; do not redraw`; do not invent metric values, p-values, benchmark ranks, axes, or performance curves.

Failure modes to flag in the prompt diagnosis:

- `METHOD_FIGURE_STRUCTURE_UNCLEAR`: lanes, arrows, or module order are ambiguous.
- `NOVELTY_LOCUS_UNDRAWN`: the proposed contribution is not visible as a distinct element or relation.
- `TEXT_CORRUPTION_RISK`: labels are too numerous or too long for image generation.
- `DATA_PANEL_PLACEHOLDER_REQUIRED`: the request would make the image model fabricate results.
- `GENERIC_PIPELINE_RISK`: the diagram could fit almost any method paper.

## Reviewer-Driven Figure Logic

Do not write abstract targets such as "include Reviewer 2's required mechanisms" as the only instruction. Decompose reviewer requirements into visible figure-level obligations.

For each reviewer issue, include:

```text
Reviewer concern:
Graphical response:
Required nodes:
Required arrows:
What must not be implied:
```

Example:

```text
Reviewer concern: the offset is criticized as exogenous.
Graphical response: show an endogenous price-feedback loop.
Required arrows:
- CET allowance price -> Sector green-power procurement
- TGC price -> Sector green-power procurement
- CET allowance price -> Sector offset share
- TGC price -> Sector offset share
What must not be implied: scenario switches must not be the only drivers of procurement or offset share.
```

## System Dynamics Canvas Rules

When the requested figure should resemble a Vensim model canvas:

- Preserve a white, wide horizontal canvas.
- Use stock boxes only for accumulated quantities.
- Use pipes, valves, and clouds for flows.
- Use curved causal arrows for auxiliary relationships.
- Use color to distinguish subsystems, not decoration.
- Do not use large module rectangles, numbered panels, icons, cards, or workflow lanes.
- Do not over-clean the diagram into an infographic.
- If editing a reference image, say: `Edit the uploaded system-dynamics canvas directly. Preserve its layout and Vensim-like style.`

For scenario design in a system-dynamics canvas:

- Treat scenarios as compact policy switches, not as causal mechanisms.
- Use dotted grey arrows for scenario activation.
- Do not draw result arrows directly from a scenario node to an outcome unless mediated by model variables.
- Keep scenario controls peripheral and small.

## Label and Symbol Rules

Use descriptive reader-facing labels as the main node labels. Do not use internal variable symbols as standalone nodes unless the user explicitly asks for formula notation.

If symbols are necessary, place them only as small secondary annotations under descriptive labels.

Convert symbols like this:

| Avoid as main label | Prefer as main label |
|---|---|
| `Q_green,bundled,total` | Bundled green-power transaction volume |
| `Q_TGC,dec,issued` | Decoupled certificate issuance volume |
| `Q_green,procured,s` | Sector green-power procurement |
| `Q_green,offset,s` | Credited green-power deduction volume |
| `rho_s` | Sector offset share |
| `kappa` | Deduction cap |
| `mu` | Indirect-emission boundary switch |
| `tau` | Bundled deduction switch |
| `EF_MEF` | Market-based grid emission factor |
| `CA_s` | Compensatory allocation |

For AI image prompts, include spelling checks for labels that previously rendered incorrectly:

```text
Check all text carefully. No misspelled, corrupted, or malformed labels are allowed.
The label must be exactly: "Electricity-related allowance demand".
```

## Nature/Science Style Without AI-Art Look

For conceptual or workflow figures that are not Vensim canvases:

- Use content-driven visual encoding, not decoration.
- Use at most three semantic color groups.
- Use pure white background.
- Use flat vector style and consistent stroke widths.
- Use two font sizes maximum.
- Use concise labels only; no paragraph text inside the figure.
- Use module grouping only when it clarifies function, not as decorative cards.
- Avoid gradients, shadows, glows, bokeh, 3D, textures, glossy materials, realistic renderings, and stock-style icons.

For manuscript submission readiness, prefer prompts that request an editable SVG-style output, but state that Image 2 may produce a raster draft. Recommend SVG reconstruction or vector cleanup when the final deliverable must be editable.

## Output Format

Return:

1. **Prompt diagnosis**: 3-6 bullets explaining the Logic Wireframe status, selected Visual Direction, prompt-preflight status, key figure logic, and main risks.
2. **Final Image 2 prompt**: one copy-ready fenced text block.
3. **Checklist**: concrete pass/fail items the user can use to judge the generated figure.

If the user explicitly asks to draw with Image 2, first produce the final prompt and then call the image tool with that prompt. If the user asks only for the prompt, do not call the image tool.

## Quality Gate

Before finalizing, check:

- The prompt is based on the supplied manuscript/reviewer/reference content, not a generic Nature-style template.
- Applicable figures consume a non-`DRAFT` Logic Wireframe; high-stakes diagrams have `USER_APPROVED` or `USER_WAIVED` status.
- The final prompt preserves the frozen mainline, branches, nodes, edge directions, semantic types, and `must_not_imply` boundaries with no silent additions or causal upgrades.
- Applicable prompts preserve one selected Visual Direction and its visual spine, reader path, grouping, render projection, visible-text allowlist, figure-caption division, negative constraints, and preservation traits; unselected directions are absent.
- Style instructions appear only after semantic, direction, projection, text, caption-division, and negative contracts are fixed.
- Every major reviewer concern is translated into nodes, arrows, labels, or removals.
- Endogenous mechanisms are shown with causal arrows, not merely listed.
- For AI/CS method diagrams, the paper type, novelty locus, structure archetype, training/inference/evaluation boundary, and data-bearing placeholders are explicit when relevant.
- Classification or heterogeneity is structural, not only a legend.
- Policy scenarios are drawn as switches unless the user asks for scenario results.
- Labels are descriptive, readable, and typo-resistant.
- The prompt explicitly avoids generic AI-art, infographic, and decorative styles when those would conflict with the requested figure type.
