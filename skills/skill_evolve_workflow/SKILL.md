---
name: skill_evolve_workflow
description: Conservatively improve research skills from real workflow friction, validated patterns, user-approved changes, and distilled reusable designs from good projects.
version: 1.5.2
---

Delegation follows current session authority; keep evidence, edits, validation, and completion responsibility with the parent.

# Skill Evolve Workflow — 科研技能复盘与演化

Evaluate and improve research skills from: **$ARGUMENTS**

Apply the global AGENTS authorization and audit-only rules to the operating modes below.

## Quick Trigger / Stop Card

- Use when: auditing, proposing, applying, validating, rolling back, or distilling improvements to the Research workflow, research skills, route ownership, output contracts, validation rules, or cross-CLI sync.
- Do not use when: the user is doing an ordinary research task that should route to `research-agent` or its selected Nature/local owner skill.
- Required inputs: concrete user feedback, local skill/workflow files, validation results, repeated friction, or a named external project/tool to verify live when current.
- Output / handoff: audit finding, patch proposal, minimal approved edits, validation checklist, sync ledger, semantic dry-run matrix, or rollback note.
- Return / stop conditions: return to the owner when the issue is task execution; edit only within the user's authorized scope.
- Validation: check metadata/resources, affected ownership and behavior, applicable promotion criteria, and platform sync. Detailed checks below apply to their stated triggers; do not rerun unrelated validation.


## Operating Modes

Choose the lightest mode that satisfies the request:

| Mode | Use when | Output | Editing |
|------|----------|--------|---------|
| `AUDIT_ONLY` | The user asks whether a skill/workflow is redundant, broken, outdated, or improvable | finding + evidence + priority | no |
| `PATCH_PROPOSAL` | A real gap or repeated friction likely needs a workflow/skill change | proposal + dependency trace + rollback/validation plan | no |
| `APPLY_APPROVED_PATCH` | The user requests scoped implementation or approves the proposed patch | minimal edits | within that authorization |
| `POST_APPLY_VALIDATION` | A patch was applied and must be checked | validation checklist + dry-run matrix + residual issues | no, unless fixing approved blockers |
| `ROLLBACK_OR_CLEANUP` | A change caused regression, stale references, duplicate rules, or route drift | rollback/cleanup plan, then approved minimal edits | only after approval |

## Hard Rules

- Run for requested maintenance; do not initiate scheduled or unsolicited self-edits.
- Preserve the user's authorization across plan, edit, and validation. A request to implement scoped improvements authorizes those edits; audit-only requests do not. Ask again only when a material expansion or an explicit approval boundary requires it.
- Do not preserve one-off task details as global rules.
- Do not turn temporary workarounds into permanent workflow doctrine.
- Do not invent skill behavior not supported by actual use.
- Do not duplicate existing skills instead of refining their boundaries.
- Do not add heavy external dependencies, hooks, CI, cloud services, agents, package installs, or external services as hidden/default requirements.
- Allowed tools or Codex capabilities do not imply default use; delegation must be explicitly justified by the task and permitted by current session authority or a stricter owner contract. Record a task/runtime-specific concurrency cap, iteration/tool-call or budget limit, and return/stop condition; do not import external numeric thresholds.
- Keep changes idempotent: repeating the same approved patch should not insert duplicate tables, routes, or instructions.
- Prefer stable workflow principles over case-specific hacks.
- Validate each logical edit batch under Step 6; repeat passed checks only for new edits, failures, or unresolved concerns.


## Plan / Apply / Post-Apply Protocol

### 1. PLAN_ONLY

Before editing, produce a plan that states:

- concrete evidence or user feedback that justifies the change;
- affected files and why each file owns part of the behavior;
- expected route, output-contract, dependency, safety, or readability delta;
- validation checks to run after editing;
- rollback plan.

`PLAN_ONLY` is the pre-edit phase, not a separate approval requirement. After planning, select the applicable operating mode above.

### 2. APPLY_AFTER_USER_APPROVAL

After approval:

- read every target file before editing;
- edit the smallest owning file set;
- update existing rules instead of duplicating semantically equivalent rules;
- avoid touching historical notes, backups, or unrelated skills unless the user explicitly includes them;
- preserve working content and do not rewrite for style alone.

### 3. POST_APPLY_VALIDATION

After editing:

- check registration and frontmatter when skills are added or renamed;
- select affected checks under Step 6, including routing dry-runs when routing changes;
- report blocking and non-blocking residual issues separately;
- only call the change complete when blocking issues are resolved or explicitly accepted by the user.

## Maintenance Routing Boundary

For non-maintenance research tasks, do not reproduce the research router here. Defer to `research-agent`.

Use this compact routing rule:

| Task type | Route |
|-----------|-------|
| Ordinary research task | `research-agent` or its selected owner skill |
| Workflow/skill audit | `skill_evolve_workflow` in `AUDIT_ONLY` |
| Workflow/skill improvement proposal | `skill_evolve_workflow` in `PATCH_PROPOSAL` |
| Approved workflow/skill edit | `skill_evolve_workflow` in `APPLY_APPROVED_PATCH` |
| Post-edit verification | `skill_evolve_workflow` in `POST_APPLY_VALIDATION` |
| Regression, stale reference, or duplicate-rule cleanup | `skill_evolve_workflow` in `ROLLBACK_OR_CLEANUP` |

Keep maintenance classification and route metadata internal by default. Show the following compact contract only when the user requests an audit/debug trace, a material ambiguity needs a choice, authorization is required, or a blocker or residual risk affects result validity:

```text
Intent:
Task object:
Task action:
Revision depth:
Evidence/material status:
Risk:
Selected mode:
Selected route:
Stop condition:
User input needed:
```

## Self-Optimization Audit and Anti-Bloat Gate

Before proposing a persistent change, check the affected function and its existing owner coverage. Reuse the diagnosis/plan instead of generating another full workflow audit. A bounded finding needs: source locator or reproduced failure; current coverage and counterevidence; minimal change; expected benefit and added cost; verification; Apply/Defer/Reject with reason and rollback. Audit unrelated functions only when an observed dependency or failure requires it.

Apply a change only when all of the following are true:

- It fixes a repeated friction, broken route, missing output contract, unsafe assumption, verified quality gap, or user-approved pattern.
- It improves at least one next-stage outcome: evidence confidence, routing accuracy, reproducibility, manuscript readiness, revision verification, or user recovery.
- It does not add a new default dependency, hidden hook, mandatory external service, or new long stage to common paths.
- It edits the smallest owning file set and avoids duplicating an existing skill.
- It has a simple validation check or dry-run scenario.

Defer or reject a change when it mainly adds doctrine, duplicates an existing gate, records project-specific judgment as a global rule, increases routine steps without a failure it prevents, or cannot be validated.

### Validation-Gated Skill Promotion Protocol

Use this protocol for any persistent skill change that may alter behavior, route ownership, safety, evidence handling, or output contracts. It is a local management contract and does not require an external optimizer, transcript harvester, package install, or scheduled self-editing process.

Before proposing a body edit, attribute the observed failure:

| Failure class | Meaning | Default action |
|---------------|---------|----------------|
| `SKILL_DEFECT` | A rule is missing, wrong, ambiguous, or insufficient; following the current skill would still fail | May enter a candidate skill patch |
| `EXECUTION_LAPSE` | The current skill already contains a correct rule, but the agent did not follow it | Keep the skill body unchanged; add a regression case or execution reminder only |
| `ENVIRONMENT_OR_TOOL_FAILURE` | The failure comes from dependencies, permissions, network, credentials, runtime, or unavailable tools | Repair or bound the environment; do not encode it as skill doctrine |
| `TASK_SPECIFIC_EXCEPTION` | The lesson applies only to one project, artifact, dataset, or user decision | Move it to project instructions/state or leave it local |

If attribution is unclear, use `STAGE_FOR_HUMAN_REVIEW`; do not silently classify the event as `SKILL_DEFECT`. When this skill audits itself, use the pre-edit promotion criteria; candidate instructions cannot approve themselves or turn static checks into behavioral evidence.

For an admissible candidate:

- Freeze the active skill as the baseline and create a separate candidate; never edit the only live copy to discover whether a change works.
- Default to `1-4` atomic add/delete/replace changes per iteration. A full rewrite requires explicit user approval and evidence that ownership or structure is fundamentally broken.
- Record the change hypothesis, exact diff, protected rules, edit budget, and rollback target.
- Build the smallest evaluation pack that can falsify the patch: observed probe/train cases for diagnosis, a frozen selection/regression set for promotion, and an optional final test set that is not used to design the candidate.
- Give every case a `case_id`, prompt/input, expected route or behavior, verifier or rubric, risk level, and provenance. Do not manufacture a held-out case after seeing candidate output and then call it independent.
- For qualitative research skills, use evidence locators, explicit multi-axis rubrics, and human adjudication. Model self-scores alone cannot promote claims about novelty, scientific validity, reviewer readiness, or publication quality.
- For qualitative behavior changes, normally run a 2-3 real-case shadow comparison when cases are available: include at least one observed target failure and one frozen regression case, apply the same predeclared rubric to active and candidate outputs, and record the human adjudicator and evidence locators. Static grep, readback, schema checks, and routing dry-runs prove registration/readability only; they do not prove outcome improvement.

Promotion rules:

- Any regression in safety, secrets, authority boundaries, provenance, canonical paths, route ownership, or clean-final handling is a hard rejection even if an aggregate score improves.
- For objectively scorable cases, require the candidate to beat the active skill by a predeclared margin or fix the target failure, with zero regressions on frozen selection/test cases in either path. Treat ties and changes within known run-to-run noise as insufficient evidence.
- A qualitative candidate may be promoted only after the real-case shadow pack and explicit human adjudication show that the target failure is fixed with no protected-rule regression. If fewer than the normally required cases are available, use `STAGE_FOR_HUMAN_REVIEW` or `DEFER_NOT_SCORABLE`; do not convert a rubric impression or static registration check into promotion.
- Use only `PROMOTE`, `STAGE_FOR_HUMAN_REVIEW`, `REJECT_REGRESSION`, or `DEFER_NOT_SCORABLE` as the promotion decision.
- Keep a rejected-change ledger with the candidate diff, failed cases, rejection reason, and reusable negative lesson. Rejected patches must not mutate the active or best-known skill.
- Even after `PROMOTE`, preserve the previous active file as the rollback source and require the normal approved-edit boundary before changing live files.

Minimum promotion evidence:

| Field | Required evidence |
|-------|-------------------|
| Active / candidate | Paths or hashes plus exact diff |
| Failure attribution | Class and source evidence |
| Evaluation pack | Case IDs, split role, verifier/rubric, provenance |
| Result | Active vs candidate outcome and hard-gate regressions |
| Decision | One allowed promotion status with reason |
| Recovery | Rejected-change entry or rollback source |

For objectively scorable, file-backed candidates, use `scripts/skill_promotion_gate.py` relative to this skill directory after the cases and margin are frozen:

```powershell
python scripts/skill_promotion_gate.py --self-test
python scripts/skill_promotion_gate.py --write-template promotion-manifest.json --skill my-skill
python scripts/skill_promotion_gate.py promotion-manifest.json --output promotion-report.json
```

The script uses only the Python standard library. It validates the manifest schema, change hypothesis, protected rules, active/candidate/rollback identities, failure attribution, edit budget, frozen selection/test declarations, hard-gate regressions, score margin/noise, and the four allowed decisions. For UTF-8 file-backed candidates, it derives the exact unified diff from `active.path` and `candidate.path`, rejects a supplied `candidate.diff` or `diff_sha256` that does not match, and preserves the derived diff in the report. Its report preserves the auditable case metadata and emits a rejected-change entry when regression forces rejection. It never executes research tasks, calls a model, reads transcripts, edits live skills, or adopts a candidate. Treat its `PROMOTE` result as evidence for the normal human approval boundary, not as authority to mutate live files. For qualitative research judgments or unclear failure attribution, it must return `STAGE_FOR_HUMAN_REVIEW` unless a hard regression requires rejection.

### Skill Utility and Semantic Selection Gate

Use this conditional gate for a new skill, a trigger or description change, a split or merge, a major body expansion, a claimed discovery/selection improvement, or intake of an externally sourced skill. A localized path correction, deterministic safety repair, or wording-only clarification may record `NOT_APPLICABLE` with a concrete reason instead of running this gate.

- Freeze comparable `NO_SKILL_OR_DIRECT_OWNER`, `ACTIVE`, and `CANDIDATE` arms with the same model, reasoning effort, tools, budget, and task inputs. When the workflow requires an owner skill and a true no-skill arm would be invalid, use the direct owner as the control and record why.
- Evaluate discovery, selection, execution outcome, and governance separately. Skill retrieval, selection, loading, or tool-call frequency is not evidence that the skill improved the task result.
- Include the smallest relevant set of exact-trigger, near-match boundary, and distractor-skill cases. For external skill intake or metadata/trigger changes, add a semantic supply-chain case that attempts unrelated capture, misleading selection, or authority/approval bypass.
- Hard-reject a candidate that captures unrelated requests, selects the wrong owner, weakens approval or authority boundaries, obscures provenance, or performs hidden external actions, even when downstream task scores improve.
- Keep the evaluation provider-neutral and local by default. External grader APIs may contribute evidence when already available, but must not become a mandatory dependency or promotion authority.

### Prompt Contract Hardening Pattern

When external prompt-engineering advice is proposed for Research workflow adoption, treat XML-like tags, examples, document ordering, and prompt chaining as optional prompt-contract hardening, not as new default workflow stages.

Adopt only the smallest reusable contract that improves traceability or handoff in multi-input, long-context, evidence-location, or cross-skill transfer tasks. Preferred lightweight fields are:

```text
<task>
<inputs>
<evidence_sources>
<constraints>
<output_contract>
<stop_conditions>
<uncertainty_policy>
<handoff>
```

Do not require XML-like tags for simple tasks, do not ask for exposed chain-of-thought as a default deliverable, and do not add few-shot examples unless the output format is stable enough to validate. Validate adoption with one targeted dry-run scenario showing clearer evidence locators, output contract, or handoff without lengthening the common route.

### Stronger-Model / GPT-5.6 Prompt Ablation Contract

Treat a stronger model as a reason to test and remove prompt scaffolding, not as proof that every rule is obsolete. For each candidate simplification:

- freeze a control using the current prompt with the same explicit evaluated model/route and reasoning effort; the candidate package, not this durable rule, records a GPT-5.6-specific choice;
- change one instruction group at a time and keep task cases, budget, and tool availability fixed;
- record prompt hash, loaded contracts, tokens, latency, tool calls, protected invariants, and a human judgment or explicit task rubric;
- keep optional features such as parallel agents, isolated verifiers, or external retrieval in separate ablations;
- do not promote from lower token use or faster completion alone; reject any candidate that weakens protected evidence, authority, artifact, or clean-final boundaries.

Use the workflow's canonical decisions: `PROMOTE`, `STAGE_FOR_HUMAN_REVIEW`, `REJECT_REGRESSION`, or `DEFER_NOT_SCORABLE`; never infer a universal model improvement from a small task sample.

### Workflow Design Distillation Contract

Use this contract when the user says a good project, article, repo, skill, prompt, system design, or workflow structure may help evolve the Research workflow. The job is not to praise or import the source. The job is to distill the smallest transferable workflow idea and decide whether it truly belongs in the local Research workflow.

Distill behavior and structure, not branding, code, dependency stacks, screenshots, or project-specific doctrine.

Minimum output:

```markdown
## Workflow Design Distillation
- Source / object:
- What looks useful:
- Underlying problem it solves:
- Distilled reusable contract:
- Existing owner skill / route:
- Existing coverage:
- Real workflow gap:
- Expected benefit:
- Complexity / dependency cost:
- Decision: Adopt / Defer / Reject
- Minimal patch if adopted:
- Validation:
```

Adopt only when the distilled contract improves routing accuracy, evidence traceability, output quality, reproducibility, manuscript readiness, reviewer-risk detection, user recovery, or handoff clarity. Keep the change inside the existing owner skill whenever possible. Reject or defer if the source is mainly aesthetic, tool-specific, repo-specific, already covered, dependency-heavy, or would lengthen common routes without preventing a real failure.

### Live Source Verification / Superiority Gate

When the distillation candidate is a named current project, repository, tool, article, or public skill, do live web verification unless the user explicitly provides a frozen local source package or says not to use the internet. Prefer primary sources: official repository, README, documentation, release notes, issues / PRs, paper, changelog, license, dependency manifests, and maintainer statements. Use secondary commentary only as leads.

Do not claim that the source is better than the local Research workflow until it has been compared against the current local owner skill and active route. Stars, popularity, screenshots, marketing claims, or a polished demo are not proof of workflow superiority.

Minimum live-source audit:

```markdown
## Live Source Verification
- Source URL / canonical identity:
- Access date:
- Source status: active / stale / archived / unclear
- Maintained evidence: latest commit / release / issue activity / changelog
- Documentation evidence: README / docs / paper / examples
- License and reuse boundary:
- Dependency / install / cloud / account burden:
- Actual design contract verified from source:
- Current local owner skill / route:
- Current local coverage:
- What is genuinely better than our current design:
- What is weaker, already covered, or too costly:
- Superiority verdict: SUPERIOR_CONTRACT / EQUIVALENT_ALREADY_COVERED / INTERESTING_BUT_NOT_BETTER / UNSAFE_OR_TOO_COSTLY / NOT_VERIFIED
```

If live verification is unavailable, return `NOT_VERIFIED` and do not apply or recommend a strong workflow patch based on that source alone. If the source is verified but only tool-specific, dependency-heavy, or not better than the current owner skill, distill it into a note or reject it rather than changing the workflow.

### Cross-CLI Sync Ledger

Use this ledger whenever a change touches shared Research workflow behavior, route ownership, skill triggers, failure codes, output contracts, validation rules, or long-lived maintenance doctrine. The default expectation is Codex and Claude Code stay synchronized unless the difference is explicitly platform-specific.

```markdown
## Cross-CLI Sync Ledger
| Item | Codex path | Claude path | Sync status | Reason if intentionally different | Validation |
|------|------------|-------------|-------------|-----------------------------------|------------|
```

Sync status must be one of `SYNCED`, `CODEX_ONLY`, `CLAUDE_ONLY`, `INTENTIONAL_DRIFT`, or `PENDING_SYNC`.

Rules:

- Use `SYNCED` for shared behavior that should work the same in Codex and Claude Code.
- Use `CODEX_ONLY` or `CLAUDE_ONLY` only when the capability, tool surface, plugin, or runtime exists on one side.
- Use `INTENTIONAL_DRIFT` only with a concrete platform reason, not because one side was forgotten.
- Use `PENDING_SYNC` for approved work that has not yet been mirrored; do not report the workflow as fully synced until resolved or explicitly accepted.
- For large files, compare the inserted block or anchored section rather than requiring whole-file identity.
- Check each platform's live entry, installed owner, and governing instructions before calling a difference stale. Different owner names or metadata alone do not establish drift. Align shared rules and document justified platform differences; changing another platform's router is a separate scope decision.
- Paired metadata validation is not body-equivalence or behavior validation. Compare the affected shared sections explicitly and report any intentionally different owner locators.

### Instruction Markdown Review Gate

Use this gate when the user asks to review, diagnose, simplify, or optimize high-authority instruction Markdown files, including triggers such as `review-codexmd`, `review-claudemd`, `诊断 AGENTS.md 和 CLAUDE.md`, `优化全局文档`, or `定期检查 agent instructions`.

Default mode is `AUDIT_ONLY`. Do not edit `AGENTS.md`, `CLAUDE.md`, `CODEX.md`, or project instruction files unless the user approves the concrete target files and patch scope. Do not implement this review as an automatic hook; it requires semantic judgment.

Canonical targets for the user's shared setup:

- Codex global instruction: `C:\Users\Administrator\.codex\AGENTS.md`.
- Codex workspace instruction for `C:\Users\Administrator`: `C:\Users\Administrator\AGENTS.md`.
- Claude Code global instruction: `C:\Users\Administrator\.claude\CLAUDE.md`.
- Treat `review-codexmd` as a request to review Codex instruction Markdown. Prefer `AGENTS.md` unless an actual `CODEX.md` exists in the relevant scope.
- Include project-local `AGENTS.md` or `CLAUDE.md` only when the current project is explicitly in scope or a global rule should be moved downward.

Audit each candidate rule with this disposition:

| Disposition | Meaning |
|-------------|---------|
| `KEEP_GLOBAL` | Cross-project, high-frequency, safety-critical, or tool-runtime invariant |
| `MOVE_TO_PROJECT` | Project path, dataset, experiment, manuscript, workspace, or team-specific rule |
| `MOVE_TO_SKILL` | Skill-stage procedure, route detail, output contract, or validation recipe |
| `CONDENSE` | Correct but too verbose, duplicated, or written as a case story |
| `ARCHIVE_OR_REJECT` | Stale, one-off, unverified, redundant, or harmful |

Minimum review output:

```markdown
## Instruction Markdown Review
- Scope:
- Files inspected:
- Selected mode: AUDIT_ONLY

| Finding | File | Evidence | Disposition | Minimal action |
|---------|------|----------|-------------|----------------|

## Global Minimality Check
- Rules that must remain global:
- Rules that should move to project files:
- Rules that should move to skills:
- Rules that should be removed or condensed:

## Cross-CLI Sync Check
- Shared principles to keep aligned:
- Platform-specific differences to preserve:
- Drift requiring user decision:

## Patch Proposal
- Apply now: no, unless user approves
- Target files:
- Validation:
```

Reject additions to global instruction files when they mainly record one project, one failure, one preference, or one workflow detail that belongs in a project `AGENTS.md` / `CLAUDE.md` or an owner skill. Prefer shorter global principles plus local specificity.

### Semantic Dry-Run Matrix

Run a compact semantic dry-run matrix after route changes, new/renamed skills, major owner-skill gates, or cross-CLI sync repairs. The dry run is a reasoning and grep/readback check; it does not execute expensive literature searches, agent loops, downloads, or formatting builds unless the user separately requests them. It validates registration and route coherence, not research-output quality; behavior-changing promotion still needs the applicable objective evaluation or qualitative real-case shadow pack.

Use the affected cases in `../research-agent/references/copilot-regression.json` for Research Agent routes. Add only cases needed for the current change that the pack does not cover; use current Nature/local ownership, not retired stage chains. For non-research utilities, check that the Research Agent is not invoked unnecessarily.

### Long Skill Quick Card Rule

For long skills or important multi-step instructions, keep scope, inputs, handoff, and stop conditions near the top. Length alone is not an execution defect. Move substantial conditional detail to references only when that reduces irrelevant loading, retaining essential gates and explicit read triggers in the owner; do not create a new skill merely to shorten a file.

Quick Card minimum fields:

```markdown
## Quick Trigger / Stop Card
- Use when:
- Do not use when:
- Required inputs:
- Output / handoff:
- Return / stop conditions:
- Validation:
```

This is a readability and routing-safety rule. It should summarize existing gates, not introduce new behavior.

### Validation Command Recipes

Use targeted validation commands instead of broad repository sweeps in `C:\Users\Administrator`, which is not a git repository. Adapt paths to the changed files.

Reserve the exact basename `SKILL.md` for live registered skill directories. Candidate, active-tree, blind-arm, rollback, and archive evidence kept beneath an auto-discovered skill root must use a non-discoverable name such as `SKILL.snapshot.md`, or live outside that root. Before closing an evolution package, fail with `DISCOVERY_COLLISION` if its evidence tree contains any exact-name `SKILL.md`; historical logs may retain pre-relocation paths only when a relocation map preserves provenance.

Store durable evolution evidence outside live Skill roots by default, under `C:\Users\Administrator\.codex\archives\skill-evolution\<owning-skill>\candidates\` or an equivalent verified archive root. A live `candidates/` directory may retain a small relocation map, but must not become the durable evidence store. Preserve relative paths plus a pre/post file count, byte count, and tree hash when relocating historical evidence.

```powershell
# validate the paired legacy Codex/Claude frontmatter without applying Codex-only schema rules to Claude fields
python scripts/validate_paired_skill.py --codex "C:\Users\Administrator\.codex\skills\skill_evolve_workflow\SKILL.md" --claude "C:\Users\Administrator\.claude\skills\skill_evolve_workflow\SKILL.md"

# Inspect the affected skill's declared name, then compare with its registration
# and compatibility contract; directory equality alone is not the verdict.
Select-String -LiteralPath 'C:\Users\Administrator\.codex\skills\TARGET\SKILL.md' -Pattern '^name:'

# Check the concrete evidence directory for this maintenance task only.
# Replace this example path with the resolved task archive before execution.
$evidenceRoot='C:\Users\Administrator\.codex\archives\skill-evolution\TARGET\candidates\TASK_ARCHIVE'
$collisions=@(Get-ChildItem -LiteralPath $evidenceRoot -Recurse -File -Filter 'SKILL.md')
if($collisions.Count){ throw "DISCOVERY_COLLISION: evidence contains discoverable SKILL.md files" }
# Broaden discovery checks only for a requested installation audit or observed collision.

# route pollution check for a new gate or borrowed project term
rg -n "NEW_GATE_OR_PROJECT_TERM" "C:\Users\Administrator\.codex\skills\research-agent\SKILL.md" "C:\Users\Administrator\AGENTS.md"

# Codex / Claude anchored block sync check
$codex = Get-Content -Raw -LiteralPath "C:\Users\Administrator\.codex\skills\TARGET\SKILL.md"
$claude = Get-Content -Raw -LiteralPath "C:\Users\Administrator\.claude\skills\TARGET\SKILL.md"
# Compare the inserted heading block or an anchored section, not whole files when platform text differs.
```

## Core Workflow

### Step 1: Collect Evidence

Use only concrete evidence:

- current skill files under `C:/Users/Administrator/.codex/skills/`;
- current active workflow reference files;
- user's explicit feedback;
- repeated failures or friction observed in the session;
- successful patterns the user confirmed;
- validation results from skill checks.

For each finding, distinguish a reproduced failure, a direct structural/contract defect, a plausible ambiguity, and an untested improvement hypothesis. Include the exact locator, triggering input, counterevidence/current coverage, likely impact, and smallest check that could refute it; omit irrelevant fields for trivial repairs.

When re-auditing an earlier diagnosis, verify it against current files and record Keep/Revise/Reject/Defer with a reason. Separate an actual contradiction from differently scoped rules or platform-specific behavior. A CLI flag being optional does not prove a prior run omitted it; a schema PASS does not prove source semantics. Prior model output is a lead, not independent evidence.

### Step 2: Classify Improvement Type

| Type | Meaning |
|------|---------|
| Trigger | Description or usage condition should change |
| Boundary | Skill overlaps or conflicts with another skill |
| Output contract | Paths, filenames, or templates need adjustment |
| Dependency | Tool/MCP assumptions are wrong or optional |
| Safety | Instruction could cause risky behavior |
| Quality | Prompt structure, gates, or reviewer checks need improvement |
| Lifecycle | A skill should be added, deprecated, renamed, merged, or split |
| Cleanup | Stale references, historical notes, or duplicate rules need cleanup |

### Step 3: Trace Dependencies

Use this table for new skills, route changes, renames, splits, merges, boundary changes, or cleanup that affects active routing:

```markdown
# Skill Dependency Trace

| Changed Skill / File | Upstream | Downstream | Router / Reference Files | Boundary Risk | Required Sync |
|----------------------|----------|------------|---------------------------|---------------|---------------|
```

### Step 4: Propose a Patch

Reuse the plan defined in `Plan / Apply / Post-Apply Protocol`; fill only missing
items. Its approval remains bound to the same scope, not to a new template.
Apply the editing boundary of the selected operating mode.

### Step 5: Apply Minimal Edits

When applying:

- read each target `SKILL.md` or workflow file first;
- edit existing files rather than creating new ones unless a new skill is clearly justified;
- keep directory name equal to frontmatter `name` when adding a skill;
- remove stale references to old skill names in active files;
- preserve working content when possible;
- do not touch unrelated active skills or historical notes unless approved.

### Step 6: Validate

After edits, run the validation checklist and report evidence, not impressions:

Choose checks by the changed contract. For a deterministic defect, reproduce it against baseline and candidate and retain a valid counterexample. For routing/qualitative changes, use the existing promotion rules and state which behavior was actually exercised. The paired validator covers metadata and supported Markdown template checks; its PASS does not certify shared-body equivalence, scientific judgment, or execution quality. Do not relabel a same-agent review or keyword check as independent behavioral validation.

```markdown
# Skill Evolution Validation Checklist

| Check | Pass/fail | Evidence |
|-------|-----------|----------|
| Paired platform-aware frontmatter/path validation passes for this legacy Codex/Claude owner |  |  |
| Skill appears in the available skill list, route table, or active workflow chain as appropriate |  |  |
| Main workflow route is updated when the change affects routing |  |  |
| Owning skill boundary is updated |  |  |
| Upstream and downstream skills are synced |  |  |
| Stale old route or deprecated skill-name grep is complete |  |  |
| Output contract and handoff are explicit |  |  |
| Failure / return codes exist when relevant |  |  |
| Behavior-changing patches passed the active/candidate promotion gate or returned `DEFER_NOT_SCORABLE` |  |  |
| New/rediscovered/expanded skills passed the conditional utility and semantic-selection gate, or recorded a justified `NOT_APPLICABLE` |  |  |
| Bundled promotion evaluator self-test passes when used for an objectively scorable candidate |  |  |
| No heavy default dependency, hidden hook, cloud service, agent, CI, or package install is introduced |  |  |
| No unrelated active skill or workflow file is touched |  |  |
| Routing dry-run matrix has no blocking failure |  |  |
```

Validate affected files and direct dependencies:

- Check names against their registration, installation, and declared compatibility contracts; fail undeclared differences that break discovery or invocation.
- Check affected routes, canonical paths, and optional dependency declarations.
- Preserve applicable behavior-change evaluation, active/candidate evidence, failure attribution, and promotion requirements.
- Run full registration or end-to-end checks only when the changed scope or observed failures require them.

### Step 7: Post-Patch Delta

```markdown
# Post-Patch Delta

| Dimension | Before | After | Evidence |
|-----------|--------|-------|----------|
| Route length for common tasks |  |  |  |
| Required dependencies |  |  |  |
| Missing/stale references |  |  |  |
| Output contract clarity |  |  |  |
| Validation status |  |  |  |
```

## Skill Readiness / Routing Smoke Test

Use this gate whenever adding a new research skill, renaming a skill, adding a major gate, or making a long skill carry important multi-step instructions. Its purpose is to verify that `调用 Research agent，帮我 ...` can route to the right skill and that the critical instructions are likely to be read before execution. Keep one old-phrase compatibility case when route retirement is in scope.

```markdown
# Skill Readiness / Routing Smoke Test

## Registration
| Check | Pass/fail | Evidence |
|-------|-----------|----------|
| Skill directory exists and matches frontmatter `name` |  |  |
| Skill appears in the relevant workflow chain or router |  |  |
| Skill appears in the route table / quick-start router when applicable |  |  |
| Codex and Claude Code counterparts are synced or intentionally different |  |  |

## Readability
| Check | Pass/fail | Evidence |
|-------|-----------|----------|
| `When to use` / trigger condition is in the first ~100 lines |  |  |
| Hard gates or failure codes are explicit |  |  |
| Output Contract and Handoff are explicit |  |  |
| Long examples/templates do not bury critical routing rules |  |  |

## Resource Integrity (only when auxiliary resources exist)
| Check | Pass/fail | Evidence |
|-------|-----------|----------|
| Every referenced script, template, example, reference, asset, schema, or config path exists and is readable |  |  |
| Documented commands, arguments, inputs, outputs, and schemas match the attached executable resources |  |  |
| A non-destructive `--help`, parser/compile check, self-test, or smallest fixture smoke test passes; otherwise the skipped check and residual risk are explicit |  |  |
| Required files, permissions, dependencies, and services are explicit, including optional/fallback/stop conditions |  |  |
| A text-only skill with no auxiliary resources is marked `NOT_APPLICABLE` rather than acquiring a new default step |  |  |

## Routing Dry Run Matrix
| Prompt Type | Prompt | Expected route | Required terms in response | Pass/fail |
|-------------|--------|----------------|----------------------------|-----------|
| Direct skill | /[skill-name] [minimal scenario] | target skill | trigger, output contract, stop condition |  |
| Agent indirect | 调用 Research agent，帮我 [minimal scenario] | `research-agent` -> target skill | correct owner and required boundary; route metadata only when requested or validity-relevant |  |
| Boundary case | [nearby task that should route to adjacent skill] | adjacent skill, not target skill | boundary reason, return condition |  |
```

Fail conditions:

- New skill exists only as a file but is absent from the workflow chain/router -> `ROUTING_NOT_REGISTERED`.
- Critical rule is only in a long reference file and not in the owning skill's hard gates or output contract -> `RULE_BURIED_IN_REFERENCE`.
- No dry-run prompt can trigger the intended route -> `TRIGGER_UNCLEAR`.
- Claude Code and Codex copies disagree without an explicit reason -> `CROSS_CLI_DRIFT`.
- A referenced auxiliary resource is missing or unreadable -> `RESOURCE_MISSING`.
- The documented command, interface, input, output, or schema disagrees with its executable resource -> `RESOURCE_CONTRACT_DRIFT`.
- A required resource smoke check cannot run and lacks an explicit skipped-check reason and residual-risk boundary -> `RESOURCE_SMOKE_UNVERIFIED`.

Do not add hooks, agents, or external services to solve readability by default. Prefer shorter trigger text, stronger handoff contracts, explicit failure codes, and a targeted dry-run scenario.

## Lightweight Project State Templates

Use these only when diagnosing an existing project, a dry-run, or a long writing/revision chain. Propose them in the response first; write project artifacts only when the user explicitly authorizes it.

### Project Evidence State Pack

Use this optional pack only for long projects, Research Agent runs, submission-grade manuscripts, complex experiments, or revise-and-resubmit work where claim/evidence state must survive across sessions. Prefer existing project-local `.agent/`, `paper/`, `results/`, `analysis/`, `09_state/`, or equivalent directories; do not scatter these files in a root directory.

```text
RESEARCH_QUESTION.yml: question_id, scope, rival/null explanation, falsifier, owner skill
TASK_CONTRACT.yml: objective, editable surface, frozen context, allowed actions, stop condition
CLAIM_LEDGER.yml: claim_id, claim text, type, strength, evidence object, source locator, boundary, status
EVIDENCE_GATE.yml: evidence_id, artifact/path/DOI/page/figure/table/code locator, QA status, blocking gaps
VERSION_BOUNDARY.md: current candidate, protected source, changed artifacts, rejected/held claims, next checkpoint
PROJECT_STATUS.md: current stage, last passed gate, blocker, next owner skill, human decision needed
```

Allowed claim statuses: `ADMIT`, `DOWNGRADE_WITH_BOUNDARY`, `HOLD_FOR_EVIDENCE`, and `REJECT_OR_REMOVE`. Only the first two may move into manuscript drafting or submission-facing prose.

### Project State Card

```markdown
# Research Workflow State

## Current Stage
- Stage:
- Last Passed Gate:
- Current Blocker:
- Next Skill:

## Gate Status
| Gate | Status | Evidence / Artifact | Blocker |
|------|--------|---------------------|---------|

## Claim/Evidence Status
| Claim ID | Evidence Ready | Figure Ready | Manuscript Ready | Repro Ready |
|----------|----------------|--------------|------------------|-------------|

## Next Action
```

### Version Decision Log

```markdown
# Version Decision Log

| Version | Purpose | User Feedback / External Constraint | Preserve | Do Not Repeat |
|---------|---------|-------------------------------------|----------|---------------|
```

Track decisions such as output genre, required title terms, revision scope, claims that must be bounded rather than replaced, and content that should not be expanded further.

### Workflow Effectiveness Scorecard

```markdown
# Workflow Effectiveness Scorecard

| Dimension | Score 0-2 | Evidence | Improvement Needed |
|-----------|-----------|----------|--------------------|
| Novelty defensibility |  |  |  |
| Data feasibility |  |  |  |
| Claim-evidence traceability |  |  |  |
| Figure readiness |  |  |  |
| Manuscript coherence |  |  |  |
| Reproducibility readiness |  |  |  |
| Submission readiness |  |  |  |
```

Scoring rule: `0` = blocked or missing, `1` = partially usable with explicit boundary, `2` = ready enough for the next workflow stage. Use evidence from artifacts, not general impressions.

## Skill Lifecycle Guidance

### Add a Skill When

- the workflow stage is repeated across projects;
- the task has a distinct input/output contract;
- it would otherwise bloat an existing skill;
- the user explicitly wants that capability as a reusable command.

### Update a Skill When

- the current skill is mostly right but incomplete;
- only triggers, paths, templates, safeguards, or boundaries need adjustment.

### Deprecate or Merge When

- two skills do the same job;
- a skill exists only for an old naming scheme;
- a skill assumes unavailable infrastructure as a hard dependency.

## Completion Rule

A workflow evolution task is complete only when:

- the selected operating mode was stated or clearly implied;
- user approval boundaries were respected;
- approved edits, if any, were minimal and target-scoped;
- validation evidence was reported;
- blocking and non-blocking residual issues were separated.

