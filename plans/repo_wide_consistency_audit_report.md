# Report: Repo-wide consistency audit and fixes

Executed against [`repo_wide_consistency_audit.md`](repo_wide_consistency_audit.md). All findings from the three audit passes were fixed. One finding turned out to be significantly worse than the audit reported, caught only by actually running the code rather than trusting the audit's read-only reasoning — documented in detail below since it's the most important result of this pass.

## The one finding that mattered most: `scripts/build_owl.py`'s DUO-term stamping has never worked, at all

The scripts audit reported this as a *coverage* problem: a hardcoded `REUSED_DUO_TERMS` dict covering only 8 of the schema's 24 real DUO terms, so `governance_duo.owl.ttl` was (per the audit) "under-stamping 16 of 24 terms with no `skos:scopeNote`/`owl:versionInfo`." That framing was based on reading the code, not running it.

Before fixing anything, the rewritten version (deriving the term list from the schema via `SchemaView` instead of a hardcoded dict) was tested empirically against the real schema — and it stamped **zero** terms, not 8. Tracing why revealed the actual bug: `DUO_NS = Namespace("http://purl.obolibrary.org/obo/DUO_")` already ends in `DUO_`, but the original (and my first-draft replacement) dict keys were shaped like `"DUO_0000007"` — indexing `DUO_NS["DUO_0000007"]` produces `http://purl.obolibrary.org/obo/DUO_DUO_0000007`, a doubled, non-existent IRI that never matches anything `gen-owl` actually emits. This means **`governance_duo.owl.ttl` has never carried a single `skos:scopeNote`/`owl:versionInfo` stamp on any reused DUO term, for any version of this script** — not "16 of 24 missing," but 24 of 24, since the script was first written. The module docstring and inline comments had described this feature as working the whole time.

Fixed by (a) deriving the term list from `DataUseModifierEnum`'s `meaning:`/description pairs at build time via `SchemaView`, so the term count can't drift from the schema again, and (b) keying by the bare local suffix (`"0000007"`) that actually combines correctly with `DUO_NS`. Verified: re-running `make owl` now produces 24 `skos:scopeNote` triples (spot-checked two, content matches the schema's own descriptions exactly) where it previously produced zero.

**Lesson applied going forward:** a read-only audit that reasons from source code is a good first pass, but a claim like "this stamps N things" needs to be checked by actually running the code and counting the output, not just reading the intent. This is being logged, not just fixed silently, because the original audit's framing (in the plan file) undersold the bug — worth remembering next time a similar audit is run.

## Everything else: as found, as planned

| Fix | File(s) |
| --- | --- |
| `CredentialTypeEnum` "14" → "15" (verified by direct count: 15 `permissible_values`) | `linkml/policy_fabric.yaml`, `docs/policy-fabric.md` |
| Added missing `slot_uri: sagegov:etag` to `DataAccessSubmission`'s `slot_usage` | `linkml/governance_graph.yaml` |
| Umbrella schema description now lists all 4 covered subsystems, not just the original 4 core classes | `linkml/governance_duo.linkml.yaml` |
| `id` slot description's file list now includes `governance_graph.yaml` | `linkml/base_entity.yaml` |
| Anchored `studyProjectIdentifier`'s pattern (`'syn[0-9]+'` → `'^syn\d+$'`) — confirmed no example data used the unanchored form, so this is non-breaking | `linkml/study.yaml` |
| Reworded `AssetBinding.assetBindings`' cross-slot-rules claim for precision (distinguishes the simple "value X requires slot B" rules `GovernanceMixin` already has from the harder positional/arity correspondence this invariant would need) | `linkml/mixins.yaml` |
| Added the missing id-hyphenation bullet to the module docstring's "schema-undeclarable decisions" list, so the two inline "(see module docstring)" cross-references actually point at something | `scripts/build_governance_graph.py` |
| Corrected Usage docstring to describe the real `None`-with-fallback defaults for `--ont`/`--instances` instead of stale literal values | `scripts/validate_graph.py` |
| Corrected Usage/description docstring to match the script's actual multi-source (`paths`/`folder`/`syn_id`) `argparse` CLI instead of an early two-positional-argument description | `scripts/generate_duo_schema.py` |
| `gov:AR-123` → `gov:AR-42` in worked-example output quotes (the underlying example was repointed from `access_requirement.123` to `.42` in the prior session; two narrative quotes were missed) | `README.md`, `docs/knowledge-graph.md` |
| Added `drs_alignment.yaml` to the import-graph Mermaid diagram and module table; added `AssetBinding` to `mixins.yaml`'s table row | `docs/linkml-model.md` |
| Governance Graph section rewritten to describe the schema-URI-driven exporter and the `owl:sameAs` bridge, and to stop claiming the script's `gov:` output is "independent of the schema's prefix registry" (it now reads its predicates from that registry) | `README.md` |
| Intro prose now mentions the DRS interoperability page both files already link to elsewhere | `README.md`, `docs/index.md` |

**Deliberately not changed:** `plans/policy_fabric_alignment.md`'s own "14 real credential schemas" claim (the same wrong count, but a historical planning document — records a decision made at a point in time, not living documentation) and `scripts/build_governance_graph.py`'s module-docstring citation of the design doc's own literal `AR-123` snippet (this is a citation of the external source being compared against, correctly labeled as such, not a claim about this repo's current output).

## Tests / verification performed

| Check | Command | Result |
| --- | --- | --- |
| Lint | `make linkml-lint` | Exit 0 |
| Full validation | `make validate-all` | `Conforms: True` for all four validation passes |
| `build_owl.py` fix, isolated | Direct call to `reused_duo_terms()` against the real schema; then a full `python scripts/build_owl.py` run with a `grep -c skos:scopeNote` before/after | Before: 0 terms resolved / 0 `skos:scopeNote` triples in the committed file (confirmed the bug was present in the already-committed `governance_duo.owl.ttl`, not just introduced by editing). After: 24 terms resolved, 24 `skos:scopeNote` triples, spot-checked content against `mixins.yaml`'s descriptions |
| Docs regeneration | `make docs` (after clearing `docs/reference/` and `docs/example_instances/`) | Succeeded |
| Doc link check | Same custom link-walking script as the prior session, plus a manual check on `docs/drs-interop.md` | Zero broken links |
| Case-collision check | Directory walk over `docs/reference/` | Zero collisions |
| Stale-reference sweep | `grep -rn` for `AR-123`, `14-value`, `14 Verifiable` across `*.md`/`*.yaml`/`*.py` | Only the three deliberately-kept external-citation instances remain (see above) |

Nothing has been committed to git as part of this work; per standing instruction, commits happen only when explicitly requested, using granular per-phase commits.
