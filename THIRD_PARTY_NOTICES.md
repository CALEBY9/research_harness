# Third-party provenance and licensing

This is initially a private maintenance repository for an existing local research
skill installation. There is no blanket license grant over all bundled material.
Retain original notices and review component-specific terms before redistribution.

## Nature Skills

- Source: https://github.com/Yuan1z0825/nature-skills
- License: Apache License 2.0; original root license copied to `skills/NATURE_LICENSE`.
- Scope: the 17 `nature-*` directories imported from the Nature installation,
  plus `researchwrite`. `nature-image2-prompt` is a separate local adapter.
- These are locally enhanced installed copies, not a pristine upstream release.
  See `docs/import_manifest.json` for the initial imported files.
- Embedded assets/tools may have additional LICENSE/NOTICE files; those remain
  in their original imported directories. Root Apache metadata alone does not
  establish rights for every image or embedded third-party example.

## Humanizer

- English source: https://github.com/blader/humanizer
- MIT license retained at `skills/humanizer/LICENSE`.
- Chinese source: https://github.com/op7418/Humanizer-zh
- MIT license retained at `skills/humanizer-zh/LICENSE`.
- Current installed content and platform metadata are preserved. No upstream
  code update or fresh plugin compatibility certification is claimed.

## OpenSpec

- Official package: `@fission-ai/openspec` version `1.12.0`.
- Source: https://github.com/Fission-AI/OpenSpec/tree/v1.12.0
- License: MIT; retained at `openspec/OPENSPEC_LICENSE`.
- `.agents/skills/openspec-*` are upstream-generated project integrations. Bodies
  and notices are retained; compatibility moved into metadata and Bash-only
  allowed-tools removed for local Codex validation/shell compatibility. The CLI
  is installed separately, not vendored.
- `openspec/schemas/research-task` and Research Agent's OpenSpec reference are
  local research adaptations; they are not upstream scientific validation claims.

## Local adapter terms

Local research adapters and the router come from the user's existing installation.
Their source/provenance notes remain where supplied. In particular,
`skills/anti-defensive-writing/references/provenance.md` describes independently
written guidance distilled from cited public designs.

A public redistribution license for the user's own contributions has not been
selected. Do not assume ownership of any referenced paper, image, font, tool,
or third-party text. Private research inputs and project data are not bundled.

## Reference projects

The projects in `docs/reference_projects.md` were inspected for design ideas.
Their runtimes, credentials, datasets and skill suites were not newly imported.
That document records observed license metadata and outstanding reuse questions.
