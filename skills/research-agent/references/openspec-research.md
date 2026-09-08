# OpenSpec for researcher-directed work

Use only for an explicitly requested OpenSpec task or an existing OpenSpec
project. Keep the selected Nature/local owner. OpenSpec is a planning and
execution-record tool, not scientific adjudication or a new research stage.

## Start from existing decisions

- Read the project's current authority pointers and the relevant source
  sections. Accepted scientific definitions, manuscript boundaries and author
  choices remain in their owning documents. Do not copy the whole discussion
  into a second spec or replace it with software-oriented assumptions.
- Determine the authorized work package. A request for planning alone ends
  with the plan. An existing request to implement carries through planning,
  implementation and checks without another approval solely for the transition.
  Return only unresolved scientific choices or a real scope/permission change
  to the author; continue independent authorized work.
- Inspect existing implementation and tests before proposing new files. Reuse
  an existing active change when it represents this task.

## Use the installed CLI

Run from the intended project directory using the current shell (PowerShell on
this host; upstream Bash examples are not a required shell).

```powershell
openspec list --json
openspec new change <change-name>
openspec status --change <change-name> --json
openspec instructions tasks --change <change-name> --json
openspec instructions apply --change <change-name> --json
```

Use the CLI-returned paths and instructions. In projects with the local
`research-task` schema, one `tasks.md` contains the source binding, bounded
implementation plan, acceptance observations and evidence table. There is no
`specs` artifact to merge into the scientific document. Other project schemas
remain valid; do not overwrite an existing configuration to impose this one.

## Verify the research requirement

Read the linked scientific clauses as well as the work package. For each
requirement, check the implementing path and the relevant downstream artifact;
for each changed code block, identify its requirement or necessary support.
Classify gaps as missing, partial, contradictory or unrequested. Keep actual
commands and result locators in the same work package or an existing report.

For example, a missing/unknown state must remain distinct from a negative
through derivation, denominator selection and figure export when that is the
source contract. Passing upstream tests does not establish downstream fidelity.
Expected observations come from the accepted requirement, never a desired
scientific trend. Mark a checkbox only after its stated acceptance is observed.

`openspec status` reports artifact presence and `openspec validate` checks
structure. Neither proves completed implementation or scientific validity.
Verification of a custom schema without delta specs must still inspect the
requirements and scenarios linked from `tasks.md`; do not skip correctness.
Unresolved material mismatches remain open even when the CLI reports readiness.

Archive only completed work within the current authorization. Archive is
bookkeeping, not author acceptance of a scientific conclusion. Update the
existing `.agent/NEXT.md` and `STATE.md` with pointers; do not build another
memory, automatic hook, self-editing loop or per-fix manifest system.
