"""
build_derivation_policy.py

Computes the Derivation Policy Graph (linkml/derivation_policy.yaml, Layer 4 of
plans/prov_o_integration.md) from a Provenance Graph (Layer 3, provenance.yaml) plus
the Governance Graph (governance_graph.yaml). Two explicitly separate passes, per
the note this repo's plan formalizes ("[the leakage evaluation] has to happen at
the point the derived artifact is published, as its own step, not inferred from the
graph after the fact"):

1. compute_control_labels() -- a precomputed, per-entity ControlLabel: the max
   DataTierEnum rank across an entity's own direct AccessRequirement bindings
   (Governance Graph) and its full derivation ancestry, consulting DerivationRule
   for an explicit resultingDataTier override at each join point (matched on
   the exact combination of parent tiers). An override can lower what is
   inherited, never below the entity's own direct bindings. Mirrors the
   note's own paragraph-18 design: computed once, not re-walked live on every
   query.
2. compute_derivation_reviews() -- mints a Flagged DerivationReview for every
   multi-input Activity whose inputs' ControlLabels cite disjoint
   sourceAccessRequirements sets, and/or where a DerivationRule marks
   requiresReview/not-permitted for the inputs' tiers -- all of them, or any two
   (an Activity with three inputs carries the risk of each pair) -- the note's own
   paragraph-12 "composite risk from independent grants" case.

Fail closed: an AccessRequirement with no curated dataTier contributes the
`Unclassified` tier, ranked above Private, so an entity bound to it is labeled
rather than reading as unrestricted. Only an entity with neither AR bindings nor
labeled ancestry gets no label.

Derivation ancestry is prov:wasDerivedFrom plus every property declared
`rdfs:subPropertyOf` it (transitively) in the loaded graphs. sagebrain-model
declares `sagebrain:derived_from rdfs:subPropertyOf prov:wasDerivedFrom` in its
governance layer, so loading its ontology and ABox with --extra-graph lets labels
reach sagebrain's Associations and Samples, not just Synapse files.

Joins compare full IRIs. Every cross-reference in the provenance and governance
graphs is an absolute IRI (syn: for Synapse entities, gov: for AccessRequirement
and Activity nodes -- see scripts/graph_iris.py), so no id normalization is needed.

Output IRIs are all gov: (plans/sagebrain_contract_and_owl_dl_fixes.md decision D6):
ControlLabel nodes are gov:control-label-<subject>, DerivationReview nodes
gov:derivation-review-<n>; `subject`, `sourceAccessRequirements` (the governance
graph's gov:AR-<n> nodes) and `computedFrom` (the generating Activity) are IRIs.

DerivationRule/curated-AccessRequirement sourcing: DerivationRule instances are
loaded from --derivation-rules (plain yaml.safe_load, same simplicity as
load_curated_access_requirements() below -- these files are already SHACL/
linkml-validate-checked elsewhere, so this script doesn't re-validate them).
Curated AccessRequirement dataTier values are sourced via
sync_governance_graph.load_curated_access_requirements(), reused unchanged.

Usage:
    python scripts/build_derivation_policy.py --provenance-graph PATH
                                               --governance-graph PATH
                                               [--extra-graph PATH ...]
                                               [--derivation-rules linkml/examples/derivation_policy]
                                               [--access-requirement-dir linkml/examples]
                                               [--out derivation_policy_export/derivation_policy.ttl]
                                               [--schema linkml/governance_duo.linkml.yaml]

author: orion.banks
"""

import argparse
import hashlib
import re
import sys
from itertools import combinations
from pathlib import Path

import yaml
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, RDFS
from linkml_runtime.utils.schemaview import SchemaView

import build_governance_graph as bgg
import sync_governance_graph as sgg
import sync_provenance_graph as spg
from graph_iris import control_label_local_name, graph_curie

DATA_TIER_RANK = {"Anonymous": 0, "Open": 1, "Controlled": 2, "Private": 3, "Unclassified": 4}
RANK_TO_TIER = {v: k for k, v in DATA_TIER_RANK.items()}
UNCLASSIFIED = "Unclassified"

DERIVATION_RULE_ID_PATTERN = re.compile(r"^derivation_rule\.[A-Za-z0-9_-]+$")

NO_LABEL = {"dataTier": None, "rank": None, "sourceARs": frozenset()}


def warn(message: str):
    print(f"WARNING: {message}", file=sys.stderr)


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


def load_governance_bindings(graph: Graph) -> dict[URIRef, dict[URIRef, str | None]]:
    """Maps entity IRI -> {gov:AR-<n> node -> curated AccessRequirement record id
    (e.g. `access_requirement.42`), or None when the stub has no owl:sameAs to a
    curated record}. Both edges are real, already-emitted triples in
    governance_graph_export/governance_graph.ttl (see build_governance_graph.py's
    AccessRequirementReference design). The record id is recovered by stripping the
    known governanceduo: namespace from the owl:sameAs target."""
    query = """
    PREFIX gov: <https://sagebionetworks.org/governance/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT ?entity ?arNode ?realAr WHERE {
        ?entity gov:hasAccessRequirement ?arNode .
        OPTIONAL { ?arNode owl:sameAs ?realAr . }
    }
    """
    namespace = str(bgg.GOVERNANCEDUO)
    bindings: dict[URIRef, dict[URIRef, str | None]] = {}
    for row in graph.query(query):
        record_id = None
        if row.realAr is not None and str(row.realAr).startswith(namespace):
            record_id = str(row.realAr)[len(namespace):]
        ars = bindings.setdefault(row.entity, {})
        if record_id or row.arNode not in ars:
            ars[row.arNode] = record_id
    return bindings


def derivation_properties(graph: Graph) -> set[URIRef]:
    """prov:wasDerivedFrom plus every property declared rdfs:subPropertyOf it,
    transitively, in `graph`."""
    properties = {spg.PROV.wasDerivedFrom}
    frontier = [spg.PROV.wasDerivedFrom]
    while frontier:
        parent = frontier.pop()
        for child in graph.subjects(RDFS.subPropertyOf, parent):
            if isinstance(child, URIRef) and child not in properties:
                properties.add(child)
                frontier.append(child)
    return properties


def load_provenance_structure(
    graph: Graph,
) -> tuple[dict[URIRef, set[URIRef]], dict[URIRef, list[URIRef]], dict[URIRef, URIRef]]:
    """Returns (direct_parents, activity_inputs, generated_by):
    - direct_parents[entity] = entities it was derived from, one hop, over
      prov:wasDerivedFrom and its sub-properties (see derivation_properties())
    - activity_inputs[activity] = non-executed input entities, sorted
    - generated_by[entity] = the Activity that prov:generated it
    Computes prov:wasDerivedFrom fresh via sync_provenance_graph.add_was_derived_from()
    -- neither the live-synced nor example-driven Provenance Graph asserts it
    directly, see that function's own docstring."""
    spg.add_was_derived_from(graph)

    direct_parents: dict[URIRef, set[URIRef]] = {}
    for prop in derivation_properties(graph):
        for s, o in graph.subject_objects(prop):
            if isinstance(s, URIRef) and isinstance(o, URIRef):
                direct_parents.setdefault(s, set()).add(o)

    activity_inputs: dict[URIRef, list[URIRef]] = {}
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
        activity_inputs.setdefault(row.activity, []).append(row.entity)
    for inputs in activity_inputs.values():
        inputs.sort()

    generated_by = {entity: activity for activity, entity in graph.subject_objects(spg.PROV.generated)}
    return direct_parents, activity_inputs, generated_by


def compute_control_labels(
    entities: set[URIRef],
    direct_parents: dict[URIRef, set[URIRef]],
    ar_bindings: dict[URIRef, dict[URIRef, str | None]],
    curated_ars: dict[str, dict],
    derivation_rules: dict[tuple, dict],
) -> dict[URIRef, dict]:
    """Memoized per-entity ControlLabel computation -- see module docstring's
    step 1. `curated_ars` is sync_governance_graph.load_curated_access_requirements()'s
    own return shape (AR record id -> its full yaml dict, dataTier read off
    directly). An AR with no curated record or no dataTier contributes
    Unclassified."""
    labels: dict[URIRef, dict] = {}
    in_progress: set[URIRef] = set()

    def ar_rank(record_id: str | None) -> int:
        tiers = (curated_ars.get(record_id, {}) or {}).get("dataTier", []) if record_id else []
        ranks = [DATA_TIER_RANK[t] for t in tiers or [] if t in DATA_TIER_RANK]
        return max(ranks) if ranks else DATA_TIER_RANK[UNCLASSIFIED]

    def direct_rank_and_ars(entity: URIRef) -> tuple[int | None, set[URIRef]]:
        ars = ar_bindings.get(entity, {})
        ranks = [ar_rank(record_id) for record_id in ars.values()]
        return (max(ranks) if ranks else None), set(ars)

    def label_for(entity: URIRef) -> dict:
        if entity in labels:
            return labels[entity]
        if entity in in_progress:
            warn(f"Cycle detected in derivation ancestry at {entity}; treating as a root here.")
            return NO_LABEL
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
            # A rule may lower what the entity inherits, never its own direct
            # binding: an entity bound to a Private AR stays at least Private.
            rule_rank = DATA_TIER_RANK[rule["resultingDataTier"]]
            final_tier = RANK_TO_TIER[max(rule_rank, own_rank if own_rank is not None else rule_rank)]
        else:
            final_tier = RANK_TO_TIER.get(default_rank)

        all_ars = set(own_ars)
        for pl in parent_labels:
            all_ars |= pl["sourceARs"]

        result = {"dataTier": final_tier, "rank": DATA_TIER_RANK.get(final_tier), "sourceARs": frozenset(all_ars)}
        in_progress.discard(entity)
        labels[entity] = result
        return result

    for entity in sorted(entities):
        label_for(entity)
    return labels


def compute_derivation_reviews(
    activity_inputs: dict[URIRef, list[URIRef]],
    labels: dict[URIRef, dict],
    derivation_rules: dict[tuple, dict],
) -> list[dict]:
    """See module docstring's step 2. One review per flagged Activity, not per
    pairwise combination -- an Activity with 3+ disjoint inputs is one composite-
    risk event to review, not several. Activities are processed in IRI order so
    review numbering is stable between runs."""
    reviews = []
    for activity in sorted(activity_inputs):
        inputs = activity_inputs[activity]
        if len(inputs) < 2:
            continue
        input_labels = [labels.get(e, NO_LABEL) for e in inputs]

        disjoint = False
        for ars_a, ars_b in combinations([il["sourceARs"] for il in input_labels], 2):
            if ars_a and ars_b and ars_a.isdisjoint(ars_b):
                disjoint = True
                break

        # Rules are authored per combination of tiers, so evaluate every pair of
        # labeled inputs as well as the whole set: an Activity with three inputs
        # still carries the risk of any two of them.
        tiers = [il["dataTier"] for il in input_labels if il["dataTier"]]
        combos = {tuple(sorted(pair)) for pair in combinations(tiers, 2)} | {tuple(sorted(tiers))}
        rule = next(
            (
                derivation_rules[combo]
                for combo in sorted(combos)
                if combo in derivation_rules
                and (derivation_rules[combo].get("requiresReview") or derivation_rules[combo].get("permitted") is False)
            ),
            None,
        )
        rule_flags_review = rule is not None

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


def subject_local_name(entity: URIRef, graph: Graph) -> str:
    """Local name used to key an entity's ControlLabel node. Synapse entities use
    their bare id (`syn10081783`); other IRIs use their prefix-qualified name with
    ':' as '-' (`association-apoe-expr-samp01`) when a prefix is bound, else a
    short hash of the full IRI -- unique either way, readable where possible."""
    iri = str(entity)
    syn_namespace = str(bgg.SYN)
    if iri.startswith(syn_namespace):
        return iri[len(syn_namespace):]
    try:
        prefix, _namespace, local = graph.namespace_manager.compute_qname(iri, generate=False)
        if prefix and local:
            return f"{prefix}-{local}"
    except (KeyError, ValueError):
        pass
    return "iri-" + hashlib.sha1(iri.encode()).hexdigest()[:12]


def control_label_node(entity: URIRef, graph: Graph) -> URIRef:
    return bgg.GOV[control_label_local_name(subject_local_name(entity, graph))]


def emit_control_label(g: Graph, entity: URIRef, label: dict, context: Graph, computed_from: URIRef | None):
    if label.get("dataTier") is None:
        return
    node = control_label_node(entity, context)
    g.add((node, RDF.type, bgg.TYPE("ControlLabel")))
    g.add((node, bgg.PREDICATE("subject", "ControlLabel"), entity))
    g.add((node, bgg.PREDICATE("dataTier", "ControlLabel"), Literal(label["dataTier"])))
    for ar in sorted(label["sourceARs"]):
        g.add((node, bgg.PREDICATE("sourceAccessRequirements", "ControlLabel"), ar))
    if computed_from is not None:
        g.add((node, bgg.PREDICATE("computedFrom", "ControlLabel"), computed_from))


def emit_derivation_review(g: Graph, index: int, review: dict, context: Graph):
    curie = graph_curie(f"derivation_review.{index:03d}", bgg._schemaview.schema.default_prefix)
    node = URIRef(bgg._schemaview.expand_curie(curie))
    g.add((node, RDF.type, bgg.TYPE("DerivationReview")))
    g.add((node, bgg.PREDICATE("activity", "DerivationReview"), review["activity"]))
    g.add((node, bgg.PREDICATE("reviewStatus", "DerivationReview"), Literal("Flagged")))
    g.add((node, bgg.PREDICATE("reviewNotes", "DerivationReview"), Literal(review["notes"])))
    for entity, label in zip(review["inputs"], review["input_labels"]):
        if label.get("dataTier") is None:
            continue
        g.add((node, bgg.PREDICATE("inputLabels", "DerivationReview"), control_label_node(entity, context)))


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
    parser.add_argument(
        "--extra-graph",
        action="append",
        default=[],
        help=(
            "Additional Turtle graph merged into the derivation ancestry (repeatable), "
            "e.g. a sagebrain-model ABox plus the ontology module declaring "
            "sagebrain:derived_from rdfs:subPropertyOf prov:wasDerivedFrom."
        ),
    )
    parser.add_argument("--derivation-rules", default="linkml/examples/derivation_policy")
    parser.add_argument("--access-requirement-dir", default="linkml/examples")
    parser.add_argument("--out", default="derivation_policy_export/derivation_policy.ttl")
    parser.add_argument("--schema", default="linkml/governance_duo.linkml.yaml")
    args = parser.parse_args()

    bgg._schemaview = SchemaView(args.schema)

    provenance_graph = Graph()
    provenance_graph.parse(args.provenance_graph, format="turtle")
    for path in args.extra_graph:
        provenance_graph.parse(path, format="turtle")
    governance_graph = Graph()
    governance_graph.parse(args.governance_graph, format="turtle")

    direct_parents, activity_inputs, generated_by = load_provenance_structure(provenance_graph)
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

    context = provenance_graph + governance_graph
    g = Graph()
    g.bind("sagegov", bgg.GOV)
    g.bind("syn", bgg.SYN)
    for entity in sorted(labels):
        emit_control_label(g, entity, labels[entity], context, generated_by.get(entity))
    for i, review in enumerate(reviews, start=1):
        emit_derivation_review(g, i, review, context)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    g.serialize(destination=str(out_path), format="turtle")
    labeled = sum(1 for label in labels.values() if label["dataTier"] is not None)
    print(f"Computed {labeled} ControlLabels ({len(labels)} entities considered), {len(reviews)} DerivationReviews.")
    print(f"Wrote {len(g)} triples to {out_path}")


if __name__ == "__main__":
    main()
