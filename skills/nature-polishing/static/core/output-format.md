# Output format

Default output is the polished text as clean plain prose, not in a code block.
Do not prepend owner, router-axis, gate, mutation-mode, or audit metadata.

Add `Revision notes:` only when the user requests an explanation, the task
includes structural or argument-level changes, or a genuine unresolved issue
requires a decision. Keep those notes separate from the clean prose and limit
them to the material changes. A `LANGUAGE_ONLY` request normally has no notes.

If the user asks for side-by-side revision, provide:

- `Original`
- `Polished`
- `Why changed`

If any paragraph's structural problem could not be fixed without inventing
content, say so separately under `Revision notes:` instead of papering over it.

When the main-text discipline is triggered, add a compact
`Main-text discipline audit:` that identifies material kept, replaced,
compressed, relocated to SI/caption, or deleted; states which descriptive and
primary inferential quantities remain in the main text; and reports the
before/after word count. Do not bury the polished prose under the audit.
