# Research Code Spec Gate

Use this contract only when Research Agent will create or materially modify
research code, scripts, notebooks, pipelines, executable queries, or
model/analysis configuration. It constrains implementation without turning
ordinary research tasks into a new workflow.

## Choose the lightest mode

| Mode | Use when | Required surface | May implementation continue? |
|---|---|---|---|
| `FORMAL` | Any high-risk trigger applies | Existing sufficient project contract or a formal Research Code Spec | Only at `SPEC_READY` |
| `MINI` | Bounded one-file script, ordinary EDA, or local bug fix with clear semantics and cheap validation | Compact objective/input/output/invariant/acceptance note | Yes after the note is fixed |
| `NOT_APPLICABLE` | Read-only inspection/explanation or behavior-preserving mechanical edit | Record the reason internally | Yes under ordinary project checks |

Do not infer risk from file count alone. Use `FORMAL` when any of these apply:

- outputs may support a paper claim, reported number, table, or final result;
- sample inclusion/exclusion, estimand, unit of analysis, split, metric,
  statistical/model choice, uncertainty, or scientific interpretation changes;
- raw or canonical data, schemas, multi-step pipelines, multiple files, or
  protected/versioned artifacts are touched;
- an external API/database, private or licensed data, a new dependency, or an
  external execution environment is required;
- execution is expensive, long-running, stochastic, search-driven, difficult
  to roll back, or likely to be reused across projects.

Use `MINI` only when the task is scientifically unambiguous, locally bounded,
cheap to verify, and does not meet a `FORMAL` trigger. Do not create a formal
artifact merely because code appears in the response.

## Reuse existing contracts

Prefer a current project contract over a duplicate. `EXPERIMENT_PLAN.md`,
`ANALYSIS_PLAN.md`, `TASK_CONTRACT.yml`, a project-local design/spec document,
or `figure_spec.yml` may satisfy `FORMAL` when it contains the required fields
below. Preserve the owning skill's stronger gates.

For figure code, `figure_spec.yml` and the figure-owner acceptance checkpoints
remain authoritative. Do not require a second Research Code Spec unless the
requested code change extends beyond that approved figure contract.

For `data_analyze`, treat a sufficiently complete `ANALYSIS_PLAN.md` as the
spec. Add missing scientific invariants or acceptance checks there instead of
creating parallel documentation.

For a task driven by an author-confirmed discussion document or TODO, bind the
current source path and section before implementation. Distinguish accepted
decisions from unresolved discussion and historical status; a newer timestamp
alone does not resolve a scientific conflict. In the existing work report,
map each in-scope requirement to implementation, acceptance check, actual
evidence and status. Review the diff in reverse too: identify changes with no
requirement or necessary supporting role, including redundant implementations
and defensive mechanisms without a concrete failure scenario. Unexecuted
checks remain unverified. Do not change scientific requirements or expected
observations merely to accommodate implementation.

When the user requests OpenSpec or the project already uses it, read
`openspec-research.md`. OpenSpec stores the work package; the existing scientific
contract and task owner remain authoritative. Simple tasks do not require it.

## Spec lifecycle

Use only the states needed for the task:

```text
SPEC_DRAFT
-> AUTHOR_DECISION_REQUIRED  # only for unresolved author-owned choices
-> SPEC_READY
-> IMPLEMENTED
-> VERIFIED
```

`NOT_APPLICABLE` is a terminal classification, not approval to skip normal
inspection or tests.

- Do not implement a `FORMAL` task while the spec is `SPEC_DRAFT` or
  `AUTHOR_DECISION_REQUIRED`.
- The agent may resolve routine technical choices when evidence and project
  conventions make them low-risk.
- Require the author for choices that change the research question, sample,
  estimand, metric, claim, negative-result interpretation, protected artifact,
  material cost, license/account use, or external authority.
- A spec authorizes only its declared editable surface and actions. It does not
  authorize package installation, external execution, uploads, or destructive
  changes unless those actions were separately approved.

## Formal Research Code Spec

A current artifact is sufficient when it fixes these fields:

```markdown
# Research Code Spec

- Status: SPEC_DRAFT / AUTHOR_DECISION_REQUIRED / SPEC_READY / IMPLEMENTED / VERIFIED
- Objective and research question:
- Selected owner and editable surface:
- Inputs, schema, units, CRS/time/scale where relevant:
- Scientific assumptions, sample/exclusion rules, estimand, split, and metric:
- Required outputs and result locators:
- Invariants and protected artifacts:
- Non-goals:
- Implementation constraints and dependency boundary:
- Acceptance tests and expected observations:
- Reproduction command or smallest verification command:
- Stop and rollback condition:
- Author decisions required:
```

Use the project's existing documentation location. If no convention exists,
keep a one-turn spec in the response; create a persistent artifact under an
existing `agent_docs/`, `.agent/`, `analysis/`, or equivalent project directory
only when project artifact writes are authorized. Do not put a new spec in the
workspace root by default.

## Mini spec

For `MINI`, fix this compact contract before coding:

```text
Objective:
Input and output:
Scientific invariant:
Editable surface / non-goal:
Acceptance command and expected observation:
```

Keep it internal or concise unless the user asks to see it or a validity issue
needs a decision. A mini spec does not require a new file.

## Implementation and verification

- Inspect the bound inputs, relevant code, project instructions, and current
  state before implementation.
- Implement only the declared editable surface; reclassify or return to the
  spec if a new scientific decision or protected artifact appears.
- Verify the acceptance checks after implementation and report actual commands
  and outcomes. A successful process exit is not enough when the expected
  scientific observation or artifact invariant was not checked.
- Keep exploratory outputs distinct from confirmatory or paper-critical
  results, and preserve raw data and declared protected artifacts.

Return codes:

- `RESEARCH_CODE_SPEC_REQUIRED`: a `FORMAL` task has no sufficient spec.
- `RESEARCH_CODE_SPEC_INCOMPLETE`: required fields or acceptance observations
  are missing.
- `AUTHOR_DECISION_REQUIRED`: an unresolved author-owned choice blocks the
  spec.
- `SPEC_IMPLEMENTATION_MISMATCH`: implementation would exceed or contradict
  the fixed spec.
- `SPEC_VERIFICATION_FAILED`: an executed acceptance check failed or did not
  verify the required observation.

Do not implement this contract as a semantic hook. Hooks may perform only
stable mechanical checks explicitly configured elsewhere.
