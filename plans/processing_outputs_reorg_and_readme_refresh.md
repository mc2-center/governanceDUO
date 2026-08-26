# Plan: Organize processing outputs; refresh README for current repo state

## Context

Two follow-on requests after adding the GitHub Pages docs deploy workflow and fixing
`docs/`'s out-of-`docs_dir` links:

1. Several generated build artifacts and legacy hand-authored files sat loose at the
   repo root with no consistent home, unlike the already-established `*_export/`
   directory convention (`governance_graph_export/`, `policy_fabric_export/`).
2. `README.md` predates most of this repo's current state (the `linkml/` model, the
   Policy Fabric/Governance Graph work, the `docs/` site) — it needed a proper
   orientation section, and its final, now-outdated "Materials available in this
   repository" section (Synapse-submission workflow tied to an old
   `ar-dictionary-schema` branch) needed to move into a collapsed archive rather than
   be deleted outright.

## Approach

**Reorg** — classify every loose root-level file as either a current build output or
legacy content, then relocate without changing generator logic:

- `governance_duo.owl.ttl` (generated, `make owl`) → `shapes/governance_duo.owl.ttl`,
  alongside its sibling `governance_duo.shacl.ttl` and the already-precedented
  `governance_graph.{owl,shacl}.ttl` pair (`shapes/` already mixes generated + hand-
  authored TTL artifacts for the Governance Graph schema, so this matches existing
  convention rather than inventing a new one).
- `sage-ar.model.csv`, `sage-ar.model.jsonld`, `AccessRequirement_validation_schema-
  updated.json` → `sage-ar-model/`, joining the `AccessRequirement.json`/
  `Resource.json`/`Study.json` already generated there by
  `scripts/create_json_from_model.py`. All four are outputs of the same
  collate → convert → generate-json schematic pipeline sourced from
  `model/*.model.csv`; the README's own "Known follow-up" note already ties the CSV,
  JSON-LD, and validation-schema files together as one regeneration unit.
- `data dictionary table` (no extension) and `metadata structure.md` → `archive/`,
  renamed `data-dictionary-table.txt`/`metadata-structure.md`. Confirmed via
  `git log --follow` these predate the LinkML/CSV pipeline entirely (2024-era, before
  `sage-ar.model.csv` existed) and aren't referenced by any current script or doc.

Every relocated path was then grepped for across `Makefile`, `scripts/*.py`,
`docs/*.md`, and `README.md`, and each reference updated. `linkml/mixins.yaml`'s two
comments naming `sage-ar.model.csv`/`sage-ar-model/*.json` were left as-is — they name
the artifacts generically, without a root-relative path, so they stay accurate.
`plans/*_report.md` were left untouched as historical, point-in-time records.

Left alone, deliberately: `access_requirement_JSON/`'s internal layout (some per-DCC
generated schemas already live under its documented `{DCC}/dictionary/`/
`{DCC}/json_schema/` convention; others sit loose at its top level following the same
naming pattern but not the folder convention). This is a real inconsistency but a
higher-risk one to fix blind — those files may already be registered/bound in Synapse
by their current repo-relative path or reference each other via the DCC's own
`example_schema_lookup_table.csv`, and the ownership/verification context for that
pipeline wasn't available in this pass. Flagged here as a follow-up, not acted on.

## README rewrite

- Added a `# governanceDUO` title (previously missing) and a new `# Repository
  layout` section (path → contents table) right after the intro, covering every
  current top-level directory.
- Added a note in `# Documentation` about the new GitHub Pages deploy workflow and
  expected published URL.
- Left the `# LinkML representation` / `## Policy Fabric alignment` / `## Governance
  Graph alignment` sections' substance untouched (accurate, already reflects current
  state) — only fixed two path references made stale by the reorg above
  (`make owl`'s comment, the "Known follow-up" bullet).
- Wrapped everything from `# Materials available in this repository` onward (its own
  bullet list plus `## Submitting metadata to the database`, `## Creating conditional
  JSON schemas...`, `## Using schemas...`, `## Additional information`) in a single
  `<details><summary><b>Archive</b></summary>...</details>` block, with a short note
  above it explaining why (predates the current model; links to a separate branch).

## Verification

- `make shacl-validate` and `make governance-graph-validate` — both pass against the
  new `shapes/governance_duo.owl.ttl` path.
- `make docs-build` (`mkdocs build --strict`) — passes; `docs/reference/` regenerated
  byte-identical (no schema/comment content changed).
- Regenerated `shapes/governance_duo.owl.ttl` / `shapes/governance_duo.shacl.ttl`
  during testing came back with reordered-but-equivalent blank nodes (LinkML's
  generators aren't ordering-stable across runs); reset to the originally committed
  bytes at their new path rather than keep incidental reordering churn.
- `<details>`/`</details>` tag count in `README.md` balanced (7/7).

See [`processing_outputs_reorg_and_readme_refresh_report.md`](processing_outputs_reorg_and_readme_refresh_report.md)
for the full file-by-file change list.
