asked via /btw:

"related to the linkml models for Study, Resource, and AR: is the following note something to address? If yes, how so? Note: 
'Deliberately an untyped string, not range: AccessRequirement: giving it a
real typed range would require importing access_requirement.yaml into this
file, but this file (like mixins.yaml) is a leaf that imports only
linkml:types specifically so it can never import an entity file and risk an
import cycle (see the schema-level description above). governance_graph.yaml
can afford real typed ranges for its own cross-references (e.g.
accessRequirement: range: AccessRequirement) because it is a single,
later-loaded file that already imports everything it references -- this
file cannot follow that pattern without breaking its own leaf-file
guarantee. Same rationale applies to StudyKey below and to ResourceKey
(schema.yaml)/SchemaKey (resource.yaml).'"

Response:
No — this isn't the same kind of gap the session fixed with `AccessRequirementReference`, and I wouldn't recommend changing it.

The `AccessRequirementReference` fix worked because `governance_graph.yaml` is *not* a leaf — the note itself says so explicitly ("a single, later-loaded file that already imports everything it references"). It could safely mint a new class with its own identity because it already sits downstream of `access_requirement.yaml` in the import graph, so adding a typed range there costs nothing.

The file holding `AccessRequirementKey`/`StudyKey`/`ResourceKey`/`SchemaKey` is the opposite case: it's a shared leaf (like `mixins.yaml`) that multiple entity files (`access_requirement.yaml`, `study.yaml`, `resource.yaml`, `schema.yaml`) import *from*. If it tried to import any one of those back to get a typed range, that's a direct one-hop cycle — not a workaround-able inconvenience, a structural impossibility given the current layering (a leaf can't import something that imports the leaf). And there's no equivalent to the `AccessRequirementReference` trick available here: that fix worked by giving a *stub* node its own downstream-owned identity for a graph-export layer; these `*Key` slots are plain cross-reference fields on the core entity schemas themselves, with no analogous "downstream, already-importing" file to relocate the typed declaration into without picking a side (which importer wins) and losing the shared-slot reuse this file exists for in the first place.

So the note is a correctly self-documented, permanent constraint, not an unresolved gap — I wouldn't touch the import structure to "fix" it. If you want more validation than a bare untyped string gives you, the one safe, cycle-free lever is a `pattern:` regex on each `*Key` slot matching the target class's own id shape (e.g. `AccessRequirementKey` matching `^access_requirement\.\d+$`) — that catches malformed values without needing a typed `range:` at all. I can't confirm from what I already know whether that pattern is already present on these specific slots or still missing; that'd need an actual read of the file.

---

## Validation (2026-09-04)

Read all four files directly. Both halves of the `/btw` response check out.

**The import-cycle claim is correct, and stronger than the response even argued for
`ResourceKey`/`SchemaKey`.** `linkml/props.yaml` imports only `linkml:types`
(confirmed); `access_requirement.yaml`/`study.yaml`/`resource.yaml`/`schema.yaml` all
import `props` (directly, confirmed via each file's `imports:` block). If `props.yaml`
imported any one of them back to type `AccessRequirementKey`/`StudyKey`, that's a
direct one-hop cycle — not a style preference. `ResourceKey` (in `schema.yaml`) and
`SchemaKey` (in `resource.yaml`) are a sharper case than a shared-leaf import: neither
file currently imports the other, so importing *one direction* wouldn't cycle on its
own — but fixing both cross-references (which the note implies you'd want
symmetrically) requires each file to import the other, which *is* a direct mutual
cycle between two sibling entity files. There's no partial fix available here either.

**The `pattern:` gap is real, not hypothetical.** None of the four slots had a
`pattern:` constraint before this session — confirmed by reading `props.yaml`,
`schema.yaml`, and `resource.yaml` directly. Meanwhile every target class already has
its own `id` pattern declared via `slot_usage` (`AccessRequirement.id`:
`^access_requirement\.\d+$`; `Study.id`: `^study\.[A-Za-z0-9_-]+$`; `Resource.id`:
`^resource\.[A-Za-z0-9]+$`; `Schema.id`: `^schema\.[A-Za-z0-9_-]+$`), and this exact
"multivalued slot + a `pattern:` matching the referenced id shape, no typed `range:`"
combination is already precedented in this same schema —
`access_requirement.yaml`'s `entityIdList` (`multivalued: true`,
`pattern: '^syn\d+$'`) already does exactly this. Adopting it for the four `*Key`
slots isn't a new technique, just a gap where an existing one wasn't applied yet. One
correction to the `/btw` response's implicit framing: `SchemaKey` (`resource.yaml`) is
**not** multivalued (its description is singular — "the Schema id," one JSON schema
per Resource) — the other three (`AccessRequirementKey`, `StudyKey`, `ResourceKey`)
are. The fix needs a plain single-value pattern there, not a per-list-item one.

## Implementation (2026-09-04) — done

Added `pattern:` to all four slots, matching each target class's own `id` pattern
exactly, with a comment cross-referencing this file:

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