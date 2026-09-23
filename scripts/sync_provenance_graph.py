"""
sync_provenance_graph.py

Builds the canonical provenance graph from real Synapse provenance
(Activity/Used/UsedEntity/UsedURL), for one or more explicitly supplied entity
ids (plans/prov_o_integration.md; plans/model_refactor.md for the model). It
describes each Activity through build_graph.GraphBuilder and writes it with
graph_rdf: a prov:Activity with prov:generated outputs and one prov:Usage per
Used entry, each with its own IRI (.../activity/<id>/usage/<n>, in Synapse's
order), so reloads merge instead of duplicating. prov:wasDerivedFrom, which the
qualified usages imply, is left to projections/provenance.rq.

One Activity can be the generatedBy of several entities (GET
/activity/{id}/generated returns a list), so activities are collected by id
across the requested entities and each is added once, with every requested
output it generated. Outputs that weren't requested aren't fetched.

Endpoint: GET /entity/{id}/generatedBy. Synapse provenance is opt-in, so most
entities 404 here -- warned and skipped, never fatal. Auth: synapseclient's
default credential resolution.

Usage:
    python scripts/sync_provenance_graph.py syn10081783 [syn2343195 ...]
        [--out provenance_graph_export/provenance_graph_synced.ttl]

author: orion.banks
"""

import argparse
from pathlib import Path

from synapseclient import Synapse
from synapseclient.core.exceptions import SynapseHTTPError

import graph_iris
import graph_rdf
from build_graph import GraphBuilder, to_datetime, warn


def add_activity(graph: GraphBuilder, activity: dict, outputs: list[str]) -> str:
    """Adds one Synapse Activity (org.sagebionetworks.repo.model.provenance.Activity)."""
    iri = graph_iris.activity(activity["id"])
    usages = []
    # a Usage's IRI is its position in Synapse's list, so it doesn't shift when
    # an entry is left out
    for index, used in enumerate(activity.get("used") or [], start=1):
        kind = used.get("concreteType", "")
        executed = bool(used.get("wasExecuted", False))
        if kind.endswith("UsedEntity"):
            reference = used.get("reference") or {}
            target = reference.get("targetId")
            usages.append(graph.module.Usage(
                id=graph_iris.usage(iri, index), wasExecuted=executed,
                entity=graph_iris.entity(target) if target else None,
                entityVersionNumber=reference.get("targetVersionNumber"),
            ))
        elif kind.endswith("UsedURL"):
            usages.append(graph.module.Usage(
                id=graph_iris.usage(iri, index), wasExecuted=executed,
                url=used.get("url"), name=used.get("name"),
            ))
        else:
            warn(f"activity {activity['id']}: unrecognized Used.concreteType {kind!r}; leaving that entry out.")
    return graph.add(
        "Activity", id=iri, name=activity.get("name"), description=activity.get("description"),
        generated=[graph_iris.entity(e) for e in outputs], qualifiedUsage=usages,
        createdBy=graph.user(activity.get("createdBy")), createdOn=to_datetime(activity.get("createdOn")),
        modifiedBy=graph.user(activity.get("modifiedBy")), modifiedOn=to_datetime(activity.get("modifiedOn")),
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("entity_ids", nargs="+", help="Synapse entity ids to sync (e.g. syn10081783).")
    parser.add_argument("--out", default="provenance_graph_export/provenance_graph_synced.ttl")
    args = parser.parse_args()

    syn = Synapse()
    syn.login()  # default credential resolution
    activities: dict[str, dict] = {}
    outputs: dict[str, list[str]] = {}
    for entity_id in args.entity_ids:
        try:
            activity = syn.restGET(f"/entity/{entity_id}/generatedBy")
        except SynapseHTTPError as exc:
            warn(f"{entity_id}: no Activity ({exc}); skipping.")
            continue
        activities.setdefault(activity["id"], activity)
        if entity_id not in outputs.setdefault(activity["id"], []):
            outputs[activity["id"]].append(entity_id)

    graph = GraphBuilder()
    for activity_id, activity in activities.items():
        add_activity(graph, activity, outputs[activity_id])
    rdf = graph_rdf.to_rdf(graph.container())
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    rdf.serialize(destination=str(out), format="turtle")
    print(f"Wrote {len(rdf)} triples to {out}")


if __name__ == "__main__":
    main()
