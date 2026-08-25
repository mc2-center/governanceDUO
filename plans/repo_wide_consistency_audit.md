# Plan: Repo-wide consistency audit and fixes

## Context

While addressing a follow-up question about `Principal`'s deliberate omission of `BaseEntity` (see [`governance_consolidation_and_drs_interop_report.md`](governance_consolidation_and_drs_interop_report.md)), a real class of bug surfaced: a comment citing a schema-level "note" that didn't actually exist, only ever explained in a script comment. The user asked for a broader sweep of the repository for the same category of issue — stale documentation, cross-references to things that no longer exist or never did, internal contradictions, undocumented deviations from established conventions — and to fix whatever's found.

## Approach

Three parallel audit passes (forked agents, read-only), each covering a different layer of the repo:

1. **`linkml/*.yaml` schema files** — stale cross-references ("see X's own note"), stale counts in prose, outdated behavior descriptions, internal contradictions, undocumented convention deviations.
2. **`scripts/*.py`** — docstrings/comments describing behavior the code no longer has, especially after this session's rewrites to `build_governance_graph.py` and `build_policy_fabric.py`.
3. **`README.md` + `docs/*.md`** (excluding auto-generated `docs/reference/`) — claims that no longer match the current schema/script state, stale example output quoted verbatim, stale counts, broken internal links.

Findings were then triaged and fixed directly (no separate design-review step — these are documentation/consistency fixes, not architectural decisions).

## What to fix

- `linkml/policy_fabric.yaml`: `CredentialTypeEnum` description says "14," actual count is 15.
- `linkml/governance_graph.yaml`: `DataAccessSubmission.etag` slot listed but missing the `slot_uri` override its sibling `createdBy`/`createdOn` overrides have (latent — would raise if `etag` export were ever added for that class); stale top-level description omitting `policy_fabric`/`governance_graph`/`drs_alignment` from the umbrella schema's self-summary.
- `linkml/base_entity.yaml`: `id` slot description's file list omits `governance_graph.yaml`.
- `linkml/study.yaml`: `studyProjectIdentifier`'s Synapse-id pattern is unanchored (`'syn[0-9]+'`) unlike the anchored pattern used everywhere else for the same concept.
- `linkml/mixins.yaml`: `AssetBinding.assetBindings` description overstates ("this repo doesn't otherwise use cross-slot rules") when `GovernanceMixin` already has 35 cross-slot `rules:` — needs precision, not removal.
- `scripts/build_owl.py`: **real functional bug**, not just a stale comment — verify and fix before assuming the audit's framing is complete.
- `scripts/build_governance_graph.py`: `gov_id()`/`add_principal`'s "(see module docstring)" cross-reference points at a bullet list that doesn't actually cover id-hyphenation.
- `scripts/validate_graph.py`: Usage docstring shows literal default values for `--ont`/`--instances` that the code no longer has (both default to `None` with fallback logic).
- `scripts/generate_duo_schema.py`: Usage docstring describes an early, much simpler CLI than the script's actual `argparse` definition.
- `README.md` + `docs/knowledge-graph.md`: stale `gov:AR-123` in worked-example output, should be `gov:AR-42` (repointed in the prior session's Phase 1 fix, but two narrative quotes weren't updated).
- `docs/policy-fabric.md`: same 14→15 `CredentialTypeEnum` count.
- `docs/linkml-model.md`: import graph diagram and module table both omit `drs_alignment.yaml`; `mixins.yaml`'s row omits `AssetBinding`.
- `README.md`'s Governance Graph section: doesn't mention the schema-URI-driven rewrite or the `owl:sameAs` bridge, and its "independent of schema's prefix registry" claim is no longer accurate.
- `README.md` + `docs/index.md`: intro prose omits the DRS interoperability page that both already link to elsewhere.

See [`repo_wide_consistency_audit_report.md`](repo_wide_consistency_audit_report.md) for what was actually found (including one finding worse than what the audit reported) and fixed.
