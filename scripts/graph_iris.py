"""
graph_iris.py

The one place that decides which IRI a LinkML record gets when it is written into
the governance graph. Shared by scripts/convert_examples_to_rdf.py,
scripts/sync_provenance_graph.py and scripts/build_derivation_policy.py so the
example ABoxes, the live sync and the derivation builder can never mint different
IRIs for the same record.

IRI policy (see README "IRI policy" and plans/sagebrain_contract_and_owl_dl_fixes.md
decisions D4/D6):
  - graph-facing instances live in gov: (sagegov:), shaped `<kind>-<local>` to match
    the governance graph builder's existing nodes (gov:AR-42, gov:principal-<n>,
    gov:grant-001): an Activity record `activity.1001` becomes
    `sagegov:activity-1001`; a DerivationReview `derivation_review.001` becomes
    `sagegov:derivation-review-001`.
  - every other LinkML record keeps its schema-namespace CURIE
    (`access_requirement.42` -> `governanceduo:access_requirement.42`).

The stored LinkML id itself is never changed -- this module only computes the
IRI used at RDF-dump time.

author: orion.banks
"""

GOV_PREFIX = "sagegov"

# record id prefix (before the first ".") -> gov: local-name kind
GRAPH_INSTANCE_KINDS = {
    "activity": "activity",
    "derivation_review": "derivation-review",
}


def graph_curie(record_id: str, default_prefix: str) -> str:
    """Returns the CURIE a LinkML record with this bare dotted id is written under
    in the graph. Raises if the id already contains a colon -- stored ids in this
    schema never do, so that would mean a caller passed the wrong thing in."""
    if ":" in record_id:
        raise ValueError(f"'{record_id}' already contains a colon; expected a bare dotted id")
    kind, _, local = record_id.partition(".")
    if local and kind in GRAPH_INSTANCE_KINDS:
        return f"{GOV_PREFIX}:{GRAPH_INSTANCE_KINDS[kind]}-{local}"
    return f"{default_prefix}:{record_id}"


def control_label_local_name(subject_local: str) -> str:
    """gov: local name for the ControlLabel of an entity whose own local name is
    `subject_local` (e.g. `syn10081783` -> `control-label-syn10081783`). ControlLabel
    has no LinkML id of its own (see derivation_policy.yaml), so its node is keyed
    by its subject."""
    return f"control-label-{subject_local}"
