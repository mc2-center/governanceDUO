"""
sync_provenance_graph.py

Builds provenance_graph_export/provenance_graph_synced.ttl from *real* Synapse
provenance data (Activity/Used/UsedEntity/UsedURL), for one or more explicitly
supplied entity ids -- Phase 2 of plans/prov_o_integration.md.

Unlike sync_governance_graph.py, this needs no bespoke PREDICATE()/TYPE()
reserialization: linkml/provenance.yaml's Activity/Usage classes already carry real
prov: IRIs as class_uri/slot_uri annotations (Activity -> prov:Activity, Usage ->
prov:Usage, etc.), and RDFLibDumper resolves those directly -- confirmed empirically
this session (`governanceduo:activity.<n> a prov:Activity` came out of a plain
RDFLibDumper call with no extra code). So this script just builds one
linkml_runtime Activity/Usage object per entity from the real REST response and
dumps it -- no manual triple construction the way build_governance_graph.py needs
for its gov:/syn: reserialization.

Endpoint: GET /entity/{id}/generatedBy -- confirmed to exist against
rest-docs.synapse.org this session (OAuth `view` scope, the same auth tier
sync_governance_graph.py already requires). Synapse's provenance feature is opt-in,
so most entities will 404 here -- warned and skipped, never a hard failure, same
warn-don't-block discipline as sync_governance_graph.py.

Auth: same synapseclient default credential resolution as sync_governance_graph.py
(cached session / ~/.synapseConfig / SYNAPSE_AUTH_TOKEN).

Usage:
    python scripts/sync_provenance_graph.py syn10081783 [syn2343195 ...]
                                             [--out provenance_graph_export/provenance_graph_synced.ttl]
                                             [--schema linkml/governance_duo.linkml.yaml]

author: orion.banks
"""

import argparse
import sys
from pathlib import Path

from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.dumpers.rdflib_dumper import RDFLibDumper
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.schemaview import SchemaView
from rdflib import Graph, Namespace
from synapseclient import Synapse
from synapseclient.core.exceptions import SynapseHTTPError

PROV = Namespace("http://www.w3.org/ns/prov#")
SAGEGOV = Namespace("https://sagebionetworks.org/governance/")


def warn(message: str):
    print(f"WARNING: {message}", file=sys.stderr)


def fetch_generated_by(syn: Synapse, entity_id: str) -> dict | None:
    """GET /entity/{id}/generatedBy -- returns None (warned) on 404, the expected
    outcome for the great majority of entities, since Synapse's provenance feature
    is opt-in and most files have never had it filled in (see this repo's
    plans/prov_o_integration.md Section 1's own honest gap)."""
    try:
        return syn.restGET(f"/entity/{entity_id}/generatedBy")
    except SynapseHTTPError as e:
        warn(f"{entity_id}: no Activity ({e}); skipping.")
        return None


def build_activity(module, entity_id: str, activity: dict):
    """Constructs one linkml_runtime Activity instance from a real Activity REST
    object -- id/name/description/etag/createdOn/modifiedOn/createdBy/modifiedBy/used,
    verified against org.sagebionetworks.repo.model.provenance.Activity. `generated`
    is the entity_id this Activity was fetched for; `entity`/`generated` stay bare
    Synapse ids (uriorcurie, unprefixed) -- see provenance.yaml's own description for
    why a typed SynapseEntity range isn't used here."""
    used_entries = []
    for used in activity.get("used", []) or []:
        concrete_type = used.get("concreteType", "")
        was_executed = bool(used.get("wasExecuted", False))
        if concrete_type.endswith("UsedEntity"):
            reference = used.get("reference", {}) or {}
            used_entries.append(
                module.Usage(
                    wasExecuted=was_executed,
                    entity=reference.get("targetId"),
                    entityVersionNumber=reference.get("targetVersionNumber"),
                )
            )
        elif concrete_type.endswith("UsedURL"):
            used_entries.append(
                module.Usage(
                    wasExecuted=was_executed,
                    url=used.get("url"),
                    name=used.get("name"),
                )
            )
        else:
            warn(f"{entity_id}: unrecognized Used.concreteType {concrete_type!r}; skipping that usage entry.")

    return module.Activity(
        id=f"activity.{activity['id']}",
        name=activity.get("name"),
        description=activity.get("description"),
        etag=activity.get("etag"),
        createdOn=activity.get("createdOn"),
        modifiedOn=activity.get("modifiedOn"),
        createdBy=int(activity["createdBy"]) if activity.get("createdBy") is not None else None,
        modifiedBy=int(activity["modifiedBy"]) if activity.get("modifiedBy") is not None else None,
        generated=entity_id,
        qualifiedUsage=used_entries,
    )


def add_was_derived_from(g: Graph) -> int:
    """Derives prov:wasDerivedFrom as a convenience edge -- no LinkML slot backs
    it, the same "pure inverse/join, not independently sourced" treatment
    gov:hasACL/gov:hasAccessRequirement already get in build_governance_graph.py
    (see docs/knowledge-graph.md). For every Activity A with prov:generated ?out,
    and every Usage in A's prov:qualifiedUsage with prov:entity ?in and
    sagegov:wasExecuted false (i.e. genuinely a data input, not the
    executed code/workflow), asserts `?out prov:wasDerivedFrom ?in`. Returns the
    number of triples added. Reused by build_derivation_policy.py against the
    merged provenance_graph_export/*.ttl, not just here."""
    query = """
    PREFIX prov: <http://www.w3.org/ns/prov#>
    PREFIX sagegov: <https://sagebionetworks.org/governance/>
    SELECT ?out ?in WHERE {
        ?activity prov:generated ?out ;
                  prov:qualifiedUsage ?usage .
        ?usage prov:entity ?in ;
               sagegov:wasExecuted false .
    }
    """
    added = 0
    for row in list(g.query(query)):
        g.add((row.out, PROV.wasDerivedFrom, row["in"]))
        added += 1
    return added


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Sync real Synapse provenance (Activity/used/generatedBy) into the "
            "Provenance Graph, for one or more explicit entity ids. See "
            "plans/prov_o_integration.md Sections 1/3/8 for the full design."
        )
    )
    parser.add_argument("entity_ids", nargs="+", help="Synapse entity ids to sync (e.g. syn10081783).")
    parser.add_argument("--out", default="provenance_graph_export/provenance_graph_synced.ttl")
    parser.add_argument("--schema", default="linkml/governance_duo.linkml.yaml")
    args = parser.parse_args()

    sv = SchemaView(args.schema)
    module = compile_python(PythonGenerator(args.schema).serialize())

    syn = Synapse()
    syn.login()  # default credential resolution -- see module docstring's Auth note

    merged = Graph()
    for entity_id in args.entity_ids:
        activity = fetch_generated_by(syn, entity_id)
        if activity is None:
            continue
        obj = build_activity(module, entity_id, activity)
        graph = RDFLibDumper().as_rdf_graph(obj, sv)
        for triple in graph:
            merged.add(triple)
        for prefix, namespace in graph.namespace_manager.namespaces():
            merged.bind(prefix, namespace, override=False)

    added = add_was_derived_from(merged)
    print(f"Derived {added} prov:wasDerivedFrom triples.")

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    merged.serialize(destination=str(out_path), format="turtle")
    print(f"Wrote {len(merged)} triples to {out_path}")


if __name__ == "__main__":
    main()
