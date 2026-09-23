"""
build_derivation_policy.py

Computes the Derivation Policy Graph -- ControlLabel and DerivationReview nodes
(linkml/graph/governance.yaml) -- from the canonical governance graph
(plans/model_refactor.md): the graph layer's own Access Requirement bindings and
provenance, not the pre-refactor Governance/Provenance Graph pair. Two explicitly
separate passes, per the note this repo's plan formalizes ("[the leakage
evaluation] has to happen at the point the derived artifact is published, as its
own step, not inferred from the graph after the fact"):

1. compute_control_labels() -- a precomputed, per-entity ControlLabel: the max
   DataTier rank across an entity's own direct Access Requirement bindings and
   its full derivation ancestry, consulting DerivationRule for an explicit
   resultingDataTier override at each join point (matched on the exact
   combination of parent tiers). An override can lower what is inherited, never
   below the entity's own direct bindings. Mirrors the note's own paragraph-18
   design: computed once, not re-walked live on every query.
2. compute_derivation_reviews() -- mints a Flagged DerivationReview for every
   multi-input Activity whose inputs' ControlLabels cite disjoint
   sourceAccessRequirements sets, and/or where a DerivationRule marks
   requiresReview/not-permitted for the inputs' tiers -- all of them, or any two
   (an Activity with three inputs carries the risk of each pair) -- the note's own
   paragraph-12 "composite risk from independent grants" case.

Fail closed: an Access Requirement with no gov:dataTier contributes the
Unclassified tier, ranked above Private, so an entity bound to it is labeled
rather than reading as unrestricted. Only an entity with neither AR bindings nor
labeled ancestry gets no label.

An entity's Access Requirements are its own gov:requiresAR edges plus those of
every ancestor reachable over gov:parent+ (the graph layer doesn't materialize
inheritance onto descendants; that's a projection's job -- see
entity_access_requirements()). An AR's tier comes from its gov:dataTier concept,
mapped back to a DataTier code through the enum's own `meaning`s
(tier_codes_by_iri()); ranks come from GraphBuilder.rank(), which reads the
DataTier concepts' own gov:rank, not a hardcoded table.

Derivation ancestry is prov:wasDerivedFrom -- projected from the qualified usages
by projections/provenance.rq, since the canonical graph records only what Synapse
says (the usages), not the implied edge -- plus every property declared
rdfs:subPropertyOf it (transitively) in the loaded graphs. sagebrain-model
declares sagebrain:derived_from rdfs:subPropertyOf prov:wasDerivedFrom in its
governance layer, so loading its ontology and ABox with --extra-graph lets labels
reach sagebrain's Associations and Samples, not just Synapse files.

Joins compare full IRIs: every cross-reference in the canonical graph is an
absolute IRI (syn: for Synapse entities, govid: for AccessRequirement and
Activity nodes -- see scripts/graph_iris.py), so no id normalization is needed.

Output IRIs are minted by graph_iris (the only IRI minter, plans/model_refactor.md
R2): ControlLabel nodes are graph_iris.control_label(subject), DerivationReview
nodes graph_iris.derivation_review(activity). The output is built through
build_graph.GraphBuilder and written with graph_rdf.to_rdf, like every other
graph-layer emitter.

DerivationRule sourcing: DerivationRule instances are loaded from
--derivation-rules (plain yaml.safe_load, same simplicity as before -- these
files are already SHACL/linkml-validate-checked elsewhere, so this script doesn't
re-validate them). They stay in the record layer (linkml/derivation_policy.yaml);
only ControlLabel/DerivationReview moved to the graph layer.

Usage:
    python scripts/build_derivation_policy.py --graph PATH [--graph PATH ...]
                                               [--extra-graph PATH ...]
                                               [--derivation-rules linkml/examples/derivation_policy]
                                               [--out derivation_policy_export/derivation_policy.ttl]

author: orion.banks
"""

import argparse
import re
from collections.abc import Callable
from itertools import combinations
from pathlib import Path

import yaml
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDFS

import graph_iris
import graph_rdf
from build_graph import GraphBuilder, warn

PROV = Namespace("http://www.w3.org/ns/prov#")
GOV = Namespace("https://w3id.org/synapse/governance#")

PROVENANCE_QUERY = "projections/provenance.rq"

DERIVATION_RULE_ID_PATTERN = re.compile(r"^derivation_rule\.[A-Za-z0-9_-]+$")

UNCLASSIFIED = "Unclassified"
NO_LABEL = {"dataTier": None, "rank": None, "sourceARs": frozenset()}

ACTIVITY_INPUTS_QUERY = """
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX gov: <https://w3id.org/synapse/governance#>
SELECT ?activity ?entity WHERE {
    ?activity prov:qualifiedUsage ?usage .
    ?usage prov:entity ?entity ;
           gov:wasExecuted false .
}
"""


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


def tier_codes_by_iri(sv) -> dict[str, str]:
    """DataTier concept IRI (as written) -> its enum code, via the enum's own
    `meaning`s (e.g. https://w3id.org/synapse/governance#ControlledTier ->
    'Controlled'). An AR's gov:dataTier is stored as the concept IRI, not the
    code, so labels read off it need this reverse lookup."""
    ns = sv.namespaces()
    return {str(ns.uri_for(pv.meaning)): code
            for code, pv in sv.get_enum("DataTier").permissible_values.items() if pv.meaning}


def derivation_properties(graph: Graph) -> set[URIRef]:
    """prov:wasDerivedFrom plus every property declared rdfs:subPropertyOf it,
    transitively, in `graph`."""
    properties = {PROV.wasDerivedFrom}
    frontier = [PROV.wasDerivedFrom]
    while frontier:
        parent = frontier.pop()
        for child in graph.subjects(RDFS.subPropertyOf, parent):
            if isinstance(child, URIRef) and child not in properties:
                properties.add(child)
                frontier.append(child)
    return properties


def load_derivation_ancestry(graph: Graph, provenance_query: str) -> dict[URIRef, set[URIRef]]:
    """direct_parents[entity] = entities it was derived from, one hop: the
    prov:wasDerivedFrom projections/provenance.rq constructs from the qualified
    usages, plus every property declared rdfs:subPropertyOf it, transitively
    (derivation_properties()) -- e.g. sagebrain-model's sagebrain:derived_from,
    asserted directly in an --extra-graph, not projected."""
    combined = Graph()
    combined += graph
    for triple in graph.query(provenance_query):
        combined.add(triple)

    direct_parents: dict[URIRef, set[URIRef]] = {}
    for prop in derivation_properties(combined):
        for s, o in combined.subject_objects(prop):
            if isinstance(s, URIRef) and isinstance(o, URIRef):
                direct_parents.setdefault(s, set()).add(o)
    return direct_parents


def load_activity_inputs(graph: Graph) -> dict[URIRef, list[URIRef]]:
    """activity -> its non-executed input entities (qualified usages with
    gov:wasExecuted false), sorted so review numbering is stable between runs."""
    activity_inputs: dict[URIRef, list[URIRef]] = {}
    for row in graph.query(ACTIVITY_INPUTS_QUERY):
        activity_inputs.setdefault(row.activity, []).append(row.entity)
    for inputs in activity_inputs.values():
        inputs.sort()
    return activity_inputs


def load_entity_structure(graph: Graph) -> tuple[dict[URIRef, URIRef], dict[URIRef, set[URIRef]]]:
    """(parent_of, requires_ar): parent_of[entity] = its gov:parent (one hop);
    requires_ar[entity] = the AccessRequirements attached directly to it
    (gov:requiresAR, one of the AR's own subjectIds -- see
    scripts/sync_governance_graph.py). Inheritance onto descendants is not
    materialized here; entity_access_requirements() walks it."""
    parent_of = {s: o for s, o in graph.subject_objects(GOV.parent)}
    requires_ar: dict[URIRef, set[URIRef]] = {}
    for s, o in graph.subject_objects(GOV.requiresAR):
        requires_ar.setdefault(s, set()).add(o)
    return parent_of, requires_ar


def make_ar_tier(graph: Graph, tier_by_iri: dict[str, str]) -> Callable[[URIRef], str]:
    """A memoized entity -> str."""
    cache: dict[URIRef, str] = {}

    def ar_tier(ar: URIRef) -> str:
        if ar not in cache:
            concept = graph.value(ar, GOV.dataTier)
            cache[ar] = tier_by_iri.get(str(concept), UNCLASSIFIED) if concept is not None else UNCLASSIFIED
        return cache[ar]

    return ar_tier


def entity_access_requirements(
    entity: URIRef,
    parent_of: dict[URIRef, URIRef],
    requires_ar: dict[URIRef, set[URIRef]],
    ar_tier: Callable[[URIRef], str],
) -> dict[URIRef, str]:
    """An entity's Access Requirements (module docstring): its own gov:requiresAR
    plus every ancestor's, walked over gov:parent+. Keyed by AR IRI -> its tier
    code (ar_tier, Unclassified when the AR carries no gov:dataTier)."""
    bindings: dict[URIRef, str] = {}
    current, seen = entity, set()
    while current is not None and current not in seen:
        seen.add(current)
        for ar in requires_ar.get(current, ()):
            bindings.setdefault(ar, ar_tier(ar))
        current = parent_of.get(current)
    return bindings


def compute_control_labels(
    entities: set[URIRef],
    direct_parents: dict[URIRef, set[URIRef]],
    ar_bindings: dict[URIRef, dict[URIRef, str]],
    graph_builder: GraphBuilder,
    derivation_rules: dict[tuple, dict],
) -> dict[URIRef, dict]:
    """Memoized per-entity ControlLabel computation -- see module docstring's
    step 1. `ar_bindings` is entity_access_requirements()'s own return shape (AR
    IRI -> its tier code, already resolved and defaulted to Unclassified)."""
    tier_enum = graph_builder.sv.get_enum("DataTier")
    rank_to_tier = {pv.rank: code for code, pv in tier_enum.permissible_values.items()}
    rank = graph_builder.rank

    labels: dict[URIRef, dict] = {}
    in_progress: set[URIRef] = set()

    def direct_rank_and_ars(entity: URIRef) -> tuple[int | None, set[URIRef]]:
        ars = ar_bindings.get(entity, {})
        ranks = [rank(tier) for tier in ars.values()]
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
            combo = tuple(sorted(rank_to_tier[pl["rank"]] for pl in parent_labels if pl["rank"] is not None))
            if combo:
                rule = derivation_rules.get(combo)

        if rule and rule.get("resultingDataTier"):
            # A rule may lower what the entity inherits, never its own direct
            # binding: an entity bound to a Private AR stays at least Private.
            rule_rank = rank(rule["resultingDataTier"])
            final_tier = rank_to_tier[max(rule_rank, own_rank if own_rank is not None else rule_rank)]
        else:
            final_tier = rank_to_tier.get(default_rank)

        all_ars = set(own_ars)
        for pl in parent_labels:
            all_ars |= pl["sourceARs"]

        result = {
            "dataTier": final_tier,
            "rank": rank(final_tier) if final_tier is not None else None,
            "sourceARs": frozenset(all_ars),
        }
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
        # Every flagging rule is reported, forbidding ones first, so a
        # permitted: false rule is never hidden behind a requiresReview one.
        flagging = [
            derivation_rules[combo]
            for combo in sorted(combos)
            if combo in derivation_rules
            and (derivation_rules[combo].get("requiresReview") or derivation_rules[combo].get("permitted") is False)
        ]
        flagging.sort(key=lambda rule: rule.get("permitted") is not False)
        rule_flags_review = bool(flagging)

        if not (disjoint or rule_flags_review):
            continue

        reasons = [
            f"DerivationRule {rule.get('id')} "
            f"{'forbids' if rule.get('permitted') is False else 'requires review of'} this combination"
            for rule in flagging
        ]
        if disjoint:
            # after any forbidding rule, so the notes lead with the strongest reason
            reasons.insert(sum(rule.get("permitted") is False for rule in flagging),
                           "inputs bound to disjoint AccessRequirements")
        reviews.append(
            {
                "activity": activity,
                "inputs": inputs,
                "input_labels": input_labels,
                "notes": "; ".join(reasons),
            }
        )
    return reviews


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Computes ControlLabel/DerivationReview from the canonical governance graph. "
            "See plans/model_refactor.md and plans/prov_o_integration.md Section 4."
        )
    )
    parser.add_argument("--graph", dest="graphs", action="append", required=True,
                        help="Canonical governance/provenance graph Turtle (repeatable).")
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
    parser.add_argument("--out", default="derivation_policy_export/derivation_policy.ttl")
    parser.add_argument("--provenance-query", default=PROVENANCE_QUERY)
    args = parser.parse_args()

    graph = Graph()
    for path in args.graphs + args.extra_graph:
        graph.parse(path, format="turtle")

    direct_parents = load_derivation_ancestry(graph, Path(args.provenance_query).read_text())
    activity_inputs = load_activity_inputs(graph)
    generated_by = {entity: activity for activity, entity in graph.subject_objects(PROV.generated)}
    parent_of, requires_ar = load_entity_structure(graph)
    derivation_rules = load_derivation_rules(Path(args.derivation_rules))

    builder = GraphBuilder()
    ar_tier = make_ar_tier(graph, tier_codes_by_iri(builder.sv))

    entities = set(requires_ar) | set(direct_parents)
    for parents in direct_parents.values():
        entities |= parents
    for inputs in activity_inputs.values():
        entities |= set(inputs)

    ar_bindings = {
        entity: entity_access_requirements(entity, parent_of, requires_ar, ar_tier) for entity in entities
    }

    labels = compute_control_labels(entities, direct_parents, ar_bindings, builder, derivation_rules)
    reviews = compute_derivation_reviews(activity_inputs, labels, derivation_rules)

    for entity in sorted(labels):
        label = labels[entity]
        if label["dataTier"] is None:
            continue
        builder.add(
            "ControlLabel",
            id=graph_iris.control_label(str(entity)),
            subject=str(entity),
            dataTier=label["dataTier"],
            sourceAccessRequirements=[str(ar) for ar in sorted(label["sourceARs"])],
            computedFrom=str(generated_by[entity]) if entity in generated_by else None,
        )
    for review in reviews:
        builder.add(
            "DerivationReview",
            id=graph_iris.derivation_review(str(review["activity"])),
            activity=str(review["activity"]),
            reviewStatus="Flagged",
            reviewNotes=review["notes"],
            inputLabels=[
                graph_iris.control_label(str(entity))
                for entity, label in zip(review["inputs"], review["input_labels"])
                if label.get("dataTier") is not None
            ],
        )

    rdf = graph_rdf.to_rdf(builder.container())
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    rdf.serialize(destination=str(out_path), format="turtle")
    labeled = sum(1 for label in labels.values() if label["dataTier"] is not None)
    print(f"Computed {labeled} ControlLabels ({len(labels)} entities considered), {len(reviews)} DerivationReviews.")
    print(f"Wrote {len(rdf)} triples to {out_path}")


if __name__ == "__main__":
    main()
