"""
sync_provenance_graph.py

Builds provenance_graph_export/provenance_graph_synced.ttl from *real* Synapse
provenance data (Activity/Used/UsedEntity/UsedURL), for one or more explicitly
supplied entity ids -- Phase 2 of plans/prov_o_integration.md.

Unlike sync_governance_graph.py, this needs no bespoke PREDICATE()/TYPE()
reserialization: linkml/provenance.yaml's Activity/Usage classes already carry real
prov: IRIs as class_uri/slot_uri annotations (Activity -> prov:Activity, Usage ->
prov:Usage, etc.), and RDFLibDumper resolves those directly. Two things the dumper
can't do on its own are handled here: the Activity's subject IRI (a bare
`activity.<n>` id makes RDFLibDumper fail with "Unknown CURIE prefix: @base", so
the id is mapped to its gov: instance CURIE, `sagegov:activity-<n>`, via
scripts/graph_iris.py at dump time -- the same policy convert_examples_to_rdf.py
uses), and entity references, which are passed as `syn:` CURIEs so they
serialize as the absolute IRIs the governance graph uses.

One Activity can be the generatedBy of several entities (confirmed in Synapse's
OpenAPI spec: GET /activity/{id}/generated returns a list). Activities are
therefore collected by id across all requested entities and each is built and
dumped once, with every requested entity it generated -- never once per entity,
which would duplicate its Usage nodes. Outputs the caller didn't request are not
fetched (no GET /activity/{id}/generated call); pass them explicitly to include
them.

Verified offline (fake REST payloads for an Activity with two outputs, a UsedURL
and a UsedEntity -- see plans/sagebrain_contract_and_owl_dl_fixes_report.md); not
yet run against live Synapse.

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

from graph_iris import graph_curie
from sync_governance_graph import to_millis

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


def syn_curie(entity_id: str) -> str:
    """`syn10081783` -> `syn:syn10081783`, the CURIE provenance.yaml's uriorcurie
    slots expect (resolves to https://www.synapse.org/Synapse:syn10081783)."""
    return f"syn:{entity_id}"


def build_activity(module, generated_ids: list[str], activity: dict):
    """Constructs one linkml_runtime Activity instance from a real Activity REST
    object -- id/name/description/etag/createdOn/modifiedOn/createdBy/modifiedBy/used,
    verified against org.sagebionetworks.repo.model.provenance.Activity.
    `generated_ids` are the requested entity ids this Activity was fetched for (one
    Activity can generate several). Entity references are syn: CURIEs -- see
    provenance.yaml's own description for why a typed SynapseEntity range isn't
    used here."""
    used_entries = []
    for used in activity.get("used", []) or []:
        concrete_type = used.get("concreteType", "")
        was_executed = bool(used.get("wasExecuted", False))
        if concrete_type.endswith("UsedEntity"):
            reference = used.get("reference", {}) or {}
            used_entries.append(
                module.Usage(
                    wasExecuted=was_executed,
                    entity=syn_curie(reference["targetId"]) if reference.get("targetId") else None,
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
            warn(f"activity {activity['id']}: unrecognized Used.concreteType {concrete_type!r}; skipping that usage entry.")

    return module.Activity(
        id=f"activity.{activity['id']}",
        name=activity.get("name"),
        description=activity.get("description"),
        etag=activity.get("etag"),
        createdOn=to_millis(activity.get("createdOn")),
        modifiedOn=to_millis(activity.get("modifiedOn")),
        createdBy=int(activity["createdBy"]) if activity.get("createdBy") is not None else None,
        modifiedBy=int(activity["modifiedBy"]) if activity.get("modifiedBy") is not None else None,
        generated=[syn_curie(e) for e in generated_ids],
        qualifiedUsage=used_entries,
    )


def dump_activity(module, sv: SchemaView, generated_ids: list[str], activity: dict) -> Graph:
    """Builds and dumps one Activity. The stored id stays the bare `activity.<n>`
    (matching provenance.yaml's id pattern); only the dump uses its gov: CURIE."""
    obj = build_activity(module, generated_ids, activity)
    obj.id = graph_curie(obj.id, sv.schema.default_prefix)
    return RDFLibDumper().as_rdf_graph(obj, sv)


def add_was_derived_from(g: Graph) -> int:
    """Derives prov:wasDerivedFrom as a convenience edge -- no LinkML slot backs
    it, the same "pure inverse/join, not independently sourced" treatment
    gov:hasACL/gov:hasAccessRequirement already get in build_governance_graph.py
    (see docs/knowledge-graph.md). For every Activity A with prov:generated ?out,
    and every Usage in A's prov:qualifiedUsage with prov:entity ?in and
    sagegov:wasExecuted false (i.e. genuinely a data input, not the
    executed code/workflow), asserts `?out prov:wasDerivedFrom ?in`. Returns the
    number of triples actually added (edges already present aren't counted).
    Reused by build_derivation_policy.py against the merged
    provenance_graph_export/*.ttl, not just here."""
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
        triple = (row.out, PROV.wasDerivedFrom, row["in"])
        if triple in g:
            continue
        g.add(triple)
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

    activities: dict[str, dict] = {}
    generated_by: dict[str, list[str]] = {}
    for entity_id in args.entity_ids:
        activity = fetch_generated_by(syn, entity_id)
        if activity is None:
            continue
        activities.setdefault(activity["id"], activity)
        outputs = generated_by.setdefault(activity["id"], [])
        if entity_id not in outputs:
            outputs.append(entity_id)

    merged = Graph()
    for activity_id, activity in activities.items():
        graph = dump_activity(module, sv, generated_by[activity_id], activity)
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
