"""
build_derivation_policy.py

Computes the Derivation Policy Graph (linkml/derivation_policy.yaml, Layer 4 of
plans/prov_o_integration.md) from a Provenance Graph (Layer 3, provenance.yaml) plus
the Governance Graph (governance_graph.yaml). Two explicitly separate passes, per
the note this repo's plan formalizes ("[the leakage evaluation] has to happen at
the point the derived artifact is published, as its own step, not inferred from the
graph after the fact"):

1. compute_control_labels() -- a precomputed, per-SynapseEntity ControlLabel: the
   max DataTierEnum rank across an entity's own direct AccessRequirement binding
   (Governance Graph) and its full prov:wasDerivedFrom ancestry (Provenance Graph),
   consulting DerivationRule for an explicit resultingDataTier override at each
   join point. Mirrors the note's own paragraph-18 design: computed once, not
   re-walked live on every query.
2. compute_derivation_reviews() -- mints a Flagged DerivationReview for every
   multi-input Activity whose inputs' ControlLabels cite disjoint
   sourceAccessRequirements sets, and/or whose input-tier combination a
   DerivationRule marks requiresReview/not-permitted -- the note's own
   paragraph-12 "composite risk from independent grants" case.

Cross-file id matching: provenance.yaml/derivation_policy.yaml's uriorcurie-ranged
cross-references (Usage.entity, Activity.generated, ControlLabel.subject/
sourceAccessRequirements) serialize as bare relative IRIs (see provenance.yaml's own
description for why), which rdflib resolves against each *file's own path* as base
when parsed independently -- so the same conceptual id can come back as a different
absolute URI depending on which file it was read from. local_id() strips back to
the bare trailing local name so cross-file joins compare on that instead of full
URI equality.

DerivationRule/curated-AccessRequirement sourcing: DerivationRule instances are
loaded from --derivation-rules (plain yaml.safe_load, same simplicity as
load_curated_access_requirements() below -- these files are already SHACL/
linkml-validate-checked elsewhere, so this script doesn't re-validate them).
Curated AccessRequirement dataTier values are sourced via
sync_governance_graph.load_curated_access_requirements(), reused unchanged.

Usage:
    python scripts/build_derivation_policy.py --provenance-graph PATH
                                               --governance-graph PATH
                                               [--derivation-rules linkml/examples/derivation_policy]
                                               [--access-requirement-dir linkml/examples]
                                               [--out derivation_policy_export/derivation_policy.ttl]
                                               [--schema linkml/governance_duo.linkml.yaml]

author: orion.banks
"""

import argparse
import re
import sys
from itertools import combinations
from pathlib import Path

import yaml
from rdflib import Graph, Literal
from rdflib.namespace import RDF
from linkml_runtime.utils.schemaview import SchemaView

import build_governance_graph as bgg
import sync_governance_graph as sgg
import sync_provenance_graph as spg

DATA_TIER_RANK = {"Anonymous": 0, "Open": 1, "Controlled": 2, "Private": 3}
RANK_TO_TIER = {v: k for k, v in DATA_TIER_RANK.items()}

DERIVATION_RULE_ID_PATTERN = re.compile(r"^derivation_rule\.[A-Za-z0-9_-]+$")


def warn(message: str):
    print(f"WARNING: {message}", file=sys.stderr)


def local_id(term) -> str:
    """Strips a URIRef/Literal down to its bare trailing local name, so cross-file
    joins compare on that instead of full URI equality -- see module docstring."""
    s = str(term)
    for sep in ("#", ":", "/"):
        if sep in s:
            s = s.rsplit(sep, 1)[-1]
    return s


def load_derivation_rules(directory: Path) -> dict[tuple, dict]:
    """Loads DerivationRule instances from directory/*.yaml (any file whose
    top-level id matches derivation_rule.<n>), keyed by a sorted tuple of
    inputDataTiers so lookup doesn't depend on combination order."""
    rules: dict[tuple, dict] = {}
    if not directory.exists():
        return rules
    for path in directory.glob("*.yaml"):
        try:
            data = yaml.safe_load(path.read_text())
        except yaml.YAMLError:
            continue
        if not isinstance(data, dict) or not DERIVATION_RULE_ID_PATTERN.match(str(data.get("id", ""))):
            continue
        tiers = tuple(sorted(data.get("inputDataTiers", []) or []))
        if tiers:
            rules[tiers] = data
    return rules


def load_governance_bindings(graph: Graph) -> dict[str, set[str]]:
    """Maps SynapseEntity local id -> set of real AccessRequirement local ids
    (governanceduo:access_requirement.<n>), via gov:hasAccessRequirement + the
    gov:AR-<n> stub's owl:sameAs bridge -- both real, already-emitted triples in
    governance_graph_export/governance_graph.ttl (see that file's own
    AccessRequirementReference/build_governance_graph.py design)."""
    query = """
    PREFIX gov: <https://sagebionetworks.org/governance/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT ?entity ?realAr WHERE {
        ?entity gov:hasAccessRequirement ?arStub .
        ?arStub owl:sameAs ?realAr .
    }
    """
    bindings: dict[str, set[str]] = {}
    for row in graph.query(query):
        bindings.setdefault(local_id(row.entity), set()).add(local_id(row.realAr))
    return bindings


def load_provenance_structure(graph: Graph) -> tuple[dict[str, set[str]], dict[str, list[str]]]:
    """Returns (direct_parents, activity_inputs):
    - direct_parents[entity] = set of entities it was prov:wasDerivedFrom (one hop)
    - activity_inputs[activity_local_id] = [entity, ...] non-executed input entities
    Computes prov:wasDerivedFrom fresh via sync_provenance_graph.add_was_derived_from()
    -- neither the live-synced nor example-driven Provenance Graph asserts it
    directly, see that function's own docstring."""
    spg.add_was_derived_from(graph)

    direct_parents: dict[str, set[str]] = {}
    for s, o in graph.subject_objects(spg.PROV.wasDerivedFrom):
        direct_parents.setdefault(local_id(s), set()).add(local_id(o))

    activity_inputs: dict[str, list[str]] = {}
    query = """
    PREFIX prov: <http://www.w3.org/ns/prov#>
    PREFIX sagegov: <https://sagebionetworks.org/governance/>
    SELECT ?activity ?entity WHERE {
        ?activity prov:qualifiedUsage ?usage .
        ?usage prov:entity ?entity ;
               sagegov:wasExecuted false .
    }
    """
    for row in graph.query(query):
        activity_inputs.setdefault(local_id(row.activity), []).append(local_id(row.entity))
    return direct_parents, activity_inputs


def compute_control_labels(
    entities: set[str],
    direct_parents: dict[str, set[str]],
    ar_bindings: dict[str, set[str]],
    curated_ars: dict[str, dict],
    derivation_rules: dict[tuple, dict],
) -> dict[str, dict]:
    """Memoized per-entity ControlLabel computation -- see module docstring's
    step 1. `curated_ars` is sync_governance_graph.load_curated_access_requirements()'s
    own return shape (AR id -> its full yaml dict, dataTier read off directly)."""
    labels: dict[str, dict] = {}
    in_progress: set[str] = set()

    def direct_rank_and_ars(entity: str) -> tuple[int | None, set[str]]:
        ars = ar_bindings.get(entity, set())
        ranks = [
            DATA_TIER_RANK[t]
            for ar in ars
            for t in (curated_ars.get(ar, {}) or {}).get("dataTier", []) or []
            if t in DATA_TIER_RANK
        ]
        return (max(ranks) if ranks else None), ars

    def label_for(entity: str) -> dict:
        if entity in labels:
            return labels[entity]
        if entity in in_progress:
            warn(f"Cycle detected in wasDerivedFrom ancestry at {entity!r}; treating as a root here.")
            return {"dataTier": None, "rank": None, "sourceARs": set()}
        in_progress.add(entity)

        own_rank, own_ars = direct_rank_and_ars(entity)
        parents = sorted(direct_parents.get(entity, set()))
        parent_labels = [label_for(p) for p in parents]

        all_ranks = [r for r in ([own_rank] + [pl["rank"] for pl in parent_labels]) if r is not None]
        default_rank = max(all_ranks) if all_ranks else None

        rule = None
        if len(parent_labels) >= 2:
            combo = tuple(sorted(RANK_TO_TIER[pl["rank"]] for pl in parent_labels if pl["rank"] is not None))
            if combo:
                rule = derivation_rules.get(combo)

        if rule and rule.get("resultingDataTier"):
            final_tier = rule["resultingDataTier"]
        else:
            final_tier = RANK_TO_TIER.get(default_rank)

        all_ars = set(own_ars)
        for pl in parent_labels:
            all_ars |= pl["sourceARs"]

        result = {"dataTier": final_tier, "rank": DATA_TIER_RANK.get(final_tier), "sourceARs": all_ars}
        in_progress.discard(entity)
        labels[entity] = result
        return result

    for entity in entities:
        label_for(entity)
    return labels


def compute_derivation_reviews(
    activity_inputs: dict[str, list[str]],
    labels: dict[str, dict],
    derivation_rules: dict[tuple, dict],
) -> list[dict]:
    """See module docstring's step 2. One review per flagged Activity, not per
    pairwise combination -- an Activity with 3+ disjoint inputs is one composite-
    risk event to review, not several."""
    reviews = []
    for activity, inputs in activity_inputs.items():
        if len(inputs) < 2:
            continue
        input_labels = [labels.get(e, {"dataTier": None, "rank": None, "sourceARs": set()}) for e in inputs]

        disjoint = False
        for (_, ars_a), (_, ars_b) in combinations([(e, il["sourceARs"]) for e, il in zip(inputs, input_labels)], 2):
            if ars_a and ars_b and ars_a.isdisjoint(ars_b):
                disjoint = True
                break

        combo = tuple(sorted(il["dataTier"] for il in input_labels if il["dataTier"]))
        rule = derivation_rules.get(combo) if combo else None
        rule_flags_review = bool(rule and (rule.get("requiresReview") or rule.get("permitted") is False))

        if not (disjoint or rule_flags_review):
            continue

        reasons = []
        if disjoint:
            reasons.append("inputs bound to disjoint AccessRequirements")
        if rule_flags_review:
            reasons.append(f"DerivationRule {rule.get('id')} flags this combination")
        reviews.append(
            {
                "activity": activity,
                "inputs": inputs,
                "input_labels": input_labels,
                "notes": "; ".join(reasons),
            }
        )
    return reviews


def emit_control_label(g: Graph, entity: str, label: dict, activity_hint: str | None = None):
    if label.get("dataTier") is None:
        return
    node = bgg.GOVERNANCEDUO[f"control_label.{entity}"]
    g.add((node, RDF.type, bgg.TYPE("ControlLabel")))
    g.add((node, bgg.PREDICATE("subject", "ControlLabel"), Literal(entity)))
    g.add((node, bgg.PREDICATE("dataTier", "ControlLabel"), Literal(label["dataTier"])))
    for ar in sorted(label["sourceARs"]):
        g.add((node, bgg.PREDICATE("sourceAccessRequirements", "ControlLabel"), Literal(ar)))
    if activity_hint:
        g.add((node, bgg.PREDICATE("computedFrom", "ControlLabel"), Literal(activity_hint)))


def emit_derivation_review(g: Graph, index: int, review: dict):
    node = bgg.GOVERNANCEDUO[f"derivation_review.{index:03d}"]
    g.add((node, RDF.type, bgg.TYPE("DerivationReview")))
    g.add((node, bgg.PREDICATE("activity", "DerivationReview"), Literal(review["activity"])))
    g.add((node, bgg.PREDICATE("reviewStatus", "DerivationReview"), Literal("Flagged")))
    g.add((node, bgg.PREDICATE("reviewNotes", "DerivationReview"), Literal(review["notes"])))
    for entity, label in zip(review["inputs"], review["input_labels"]):
        if label.get("dataTier") is None:
            continue
        input_node = bgg.GOVERNANCEDUO[f"control_label.{entity}"]
        g.add((node, bgg.PREDICATE("inputLabels", "DerivationReview"), input_node))


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Computes ControlLabel/DerivationReview (Derivation Policy Graph) from a "
            "Provenance Graph + Governance Graph. See plans/prov_o_integration.md "
            "Section 4."
        )
    )
    parser.add_argument("--provenance-graph", required=True)
    parser.add_argument("--governance-graph", required=True)
    parser.add_argument("--derivation-rules", default="linkml/examples/derivation_policy")
    parser.add_argument("--access-requirement-dir", default="linkml/examples")
    parser.add_argument("--out", default="derivation_policy_export/derivation_policy.ttl")
    parser.add_argument("--schema", default="linkml/governance_duo.linkml.yaml")
    args = parser.parse_args()

    bgg._schemaview = SchemaView(args.schema)

    provenance_graph = Graph()
    provenance_graph.parse(args.provenance_graph, format="turtle")
    governance_graph = Graph()
    governance_graph.parse(args.governance_graph, format="turtle")

    direct_parents, activity_inputs = load_provenance_structure(provenance_graph)
    ar_bindings = load_governance_bindings(governance_graph)
    curated_ars = sgg.load_curated_access_requirements(Path(args.access_requirement_dir))
    derivation_rules = load_derivation_rules(Path(args.derivation_rules))

    entities = set(ar_bindings) | set(direct_parents)
    for parents in direct_parents.values():
        entities |= parents
    for inputs in activity_inputs.values():
        entities |= set(inputs)

    labels = compute_control_labels(entities, direct_parents, ar_bindings, curated_ars, derivation_rules)
    reviews = compute_derivation_reviews(activity_inputs, labels, derivation_rules)

    g = Graph()
    for entity, label in labels.items():
        emit_control_label(g, entity, label)
    for i, review in enumerate(reviews, start=1):
        emit_derivation_review(g, i, review)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    g.serialize(destination=str(out_path), format="turtle")
    print(f"Computed {len(labels)} ControlLabels, {len(reviews)} DerivationReviews.")
    print(f"Wrote {len(g)} triples to {out_path}")


if __name__ == "__main__":
    main()
