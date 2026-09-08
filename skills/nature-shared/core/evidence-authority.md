# Evidence, Authority, and Author-Control Contract

Load this contract only for claim-bearing work, mutation of an existing or
versioned research artifact, or a readiness/completion decision. It is an
author-side guardrail, not text to copy into a manuscript, review, response
letter, figure, or other clean deliverable.

## Keep authority facts separate

Record these as independent facts:

1. the artifact exists;
2. it is in a current path, registry, or package;
3. it is a working, released, archived, or other named version;
4. it has passed a stated QA check;
5. it has explicit canonical, promotion, or edit authority.

A newer timestamp, release label, current location, or `PASS` result does not
silently establish item 5. When records conflict, retain both the current
working identity and the last explicit canonical decision. Keep the artifact
non-canonical or read-only until an author-side ledger, manifest, matching hash,
or direct author decision resolves the binding.

## Separate evidence availability from claim support

Use availability states such as `AVAILABLE`, `PARTIAL`, `MISSING`,
`CONFLICTING`, or `NOT_CHECKED` separately from claim dispositions:

- `ADMIT`: checked evidence supports the claim inside an explicit boundary.
- `DOWNGRADE_WITH_BOUNDARY`: a weaker claim is supportable and the boundary
  must remain visible wherever the claim appears.
- `HOLD_FOR_EVIDENCE`: required evidence is missing, unperformed, unlocated,
  or not yet checked.
- `REJECT_OR_REMOVE`: available evidence directly contradicts the claim, or
  the proposed claim cannot be made defensibly from the verified record.

File presence, fluent prose, a search hit, a citation candidate, a successful
code run, or a rendered figure is not by itself a support verdict. Only
`ADMIT` and `DOWNGRADE_WITH_BOUNDARY` may enter clean claim-bearing prose.
Every admitted claim needs a real source, result, table, figure, code output,
or other inspectable locator.

## Preserve author control

The author decides the research question, dominant claim, rival explanations,
falsifier or change-my-mind evidence, interpretation of negative results, and
any story rebase that changes them. The agent may structure, compare, and
stress-test options, but must not silently select one.

## Bind mutations and verify completion

Before high-risk mutation, bind the exact artifact or package, file hash when
practical, working copy, editable surface, protected context, expected output,
and stop condition. A new upload, returned proof, changed hash, or newly named
canonical version requires rebind before assumptions carry over.

Keep manuscripts, reports, formal letters, and submission files clean. Put
rationale, before/after text, line maps, review notes, and change logs in a
separate author-side artifact. Claim completion, readiness, reproducibility, or
successful revision only after the relevant source readback, test, hash,
render, cross-file audit, or other executed verification has passed.
