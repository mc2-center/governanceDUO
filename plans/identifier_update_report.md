# Report: identifier_update.md

Companion report for [`identifier_update.md`](identifier_update.md). Moved out of
that file on 2026-09-22 (it was originally appended inline, commit `f7aad4e`) to
match this repo's plan/`_report.md` convention; content unchanged apart from
references to "this file", which now name `identifier_update.md`.

## Implementation (2026-09-04)

Added `pattern:` to all four slots, matching each target class's own `id` pattern
exactly, with a comment cross-referencing `identifier_update.md`:

| Slot | File | Pattern added | Multivalued? |
| --- | --- | --- | --- |
| `AccessRequirementKey` | `linkml/props.yaml` | `^access_requirement\.\d+$` | yes |
| `StudyKey` | `linkml/props.yaml` | `^study\.[A-Za-z0-9_-]+$` | yes |
| `ResourceKey` | `linkml/schema.yaml` | `^resource\.[A-Za-z0-9]+$` | yes |
| `SchemaKey` | `linkml/resource.yaml` | `^schema\.[A-Za-z0-9_-]+$` | no |

No import structure changed, no `range:` added — exactly the cycle-free lever the
response recommended.

### Verification — all passed

- `make linkml-lint`: exit 0, same 126 pre-existing `standard_naming` warnings as
  before this change (no regression).
- `make shacl-validate`: `Conforms: True` on both the schema build and the example
  instances — in particular, `linkml/examples/access_requirement.example.yaml`'s real
  `StudyKey: [study.mc2-jax-5xfad]` still validates against the new pattern.
- **Positive check, not just "doesn't break anything"**: ran `linkml-validate`
  directly against a deliberately corrupted copy of that same example
  (`StudyKey: [NOT-A-VALID-STUDY-ID]`) — correctly rejected: `'NOT-A-VALID-STUDY-ID'
  does not match '^study\.[A-Za-z0-9_-]+$' in /StudyKey/0`, confirming the pattern is
  applied per-item on the multivalued list (not against a concatenated string) and
  actually catches malformed values, not just a syntax check that happens to pass on
  already-good data.
- `make docs-build`: `mkdocs build --strict` passes with no broken links.

### Files touched

`linkml/props.yaml`, `linkml/schema.yaml`, `linkml/resource.yaml`,
`shapes/governance_duo.owl.ttl`, `shapes/governance_duo.shacl.ttl` (regenerated),
`docs/reference/**` (regenerated: `AccessRequirement`/`Resource`/`Schema`/`Study`
classes, `AccessRequirementKey`/`ResourceKey`/`SchemaKey`/`StudyKey` slots).