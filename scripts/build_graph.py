"""
build_graph.py

Builds governance graph layer objects (linkml/graph/governance.yaml) -- the one
emitter behind every graph export (plans/model_refactor.md, Phase 2). The
Synapse syncs and the derivation builder describe what they found by calling a
GraphBuilder; graph_rdf.to_rdf() writes the result. Nothing here writes triples
or mints IRIs by hand: nodes are the schema's own classes, and IRIs come from
graph_iris.

The builder merges repeated sightings of one node (the same principal on many
ACLs, the same AR on many entities): a later sighting fills fields the earlier
one left empty and adds to multivalued ones, and never overwrites a value
already set.

author: orion.banks
"""

import sys
from datetime import datetime, timezone

from linkml_runtime.utils.schemaview import SchemaView

import graph_iris
import graph_rdf

RECORD_SCHEMA = "linkml/governance_duo.linkml.yaml"
# Synapse's own group principals for "everyone" and "every signed-in user"
# (org.sagebionetworks.repo.model.AuthorizationConstants.BOOTSTRAP_PRINCIPAL).
PUBLIC_GROUP = 273949
AUTHENTICATED_USERS_GROUP = 273948
AGENT_CLASS_FOR_GROUP = {PUBLIC_GROUP: "PUBLIC", AUTHENTICATED_USERS_GROUP: "AUTHENTICATED_USERS"}
DISEASE_TERM = "DUO:0000007"
DISEASE_SLOT = "diseaseSpecificResearch"
NOT_A_TERM = {"DUO:0000017", "Pending Annotation"}


def warn(message: str) -> None:
    print(f"WARNING: {message}", file=sys.stderr)


def to_datetime(value) -> str | None:
    """Synapse's dataaccess objects give ISO-8601 strings; entity bundles and
    older records give epoch milliseconds. Either -> an ISO-8601 UTC string."""
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        moment = datetime.fromtimestamp(value / 1000, timezone.utc)
    else:
        moment = datetime.fromisoformat(str(value).replace("Z", "+00:00")).astimezone(timezone.utc)
    return moment.strftime("%Y-%m-%dT%H:%M:%SZ") if not moment.microsecond else moment.isoformat()


class GraphBuilder:
    """Accumulates graph-layer nodes, one per IRI, into a GovernanceGraph."""

    def __init__(self, schema_path: str = graph_rdf.SCHEMA):
        self.sv, self.module = graph_rdf.schema(schema_path)
        self.nodes: dict[str, dict[str, object]] = {}
        # container slot for each node class, e.g. Authorization -> authorizations
        self.slot_for = {}
        for slot in self.sv.class_induced_slots(graph_rdf.CONTAINER):
            self.slot_for[slot.range] = slot.name
            self.nodes[slot.name] = {}

    # -- vocabulary ----------------------------------------------------------

    def known(self, enum_name: str, value, context: str) -> bool:
        """Whether `value` is a code in the vocabulary. An unknown one (a new
        Synapse ACCESS_TYPE, say) is warned and left out, never minted."""
        if value in self.sv.get_enum(enum_name).permissible_values:
            return True
        warn(f"{context}: {value!r} is not a {enum_name} value; leaving it out.")
        return False

    def rank(self, tier: str) -> int:
        return self.sv.get_enum("DataTier").permissible_values[tier].rank

    def most_restrictive(self, tiers) -> str | None:
        tiers = [t for t in tiers or [] if self.known("DataTier", t, "data tier")]
        return max(tiers, key=self.rank) if tiers else None

    def term_description(self, code: str) -> str | None:
        pv = self.sv.get_enum("DataUseTerm").permissible_values.get(code)
        return pv.description if pv else None

    # -- nodes ---------------------------------------------------------------

    def add(self, class_name: str, **fields):
        """Adds (or merges into) the node with fields['id']; returns its IRI."""
        fields = {k: v for k, v in fields.items() if v not in (None, [], "")}
        iri = fields["id"]
        bucket = self.nodes[self.slot_for[class_name]]
        existing = bucket.get(iri)
        if existing is None:
            bucket[iri] = dict(fields, _class=class_name)
            return iri
        for key, value in fields.items():
            if isinstance(value, list):
                merged = existing.setdefault(key, [])
                merged.extend(v for v in value if v not in merged)
            elif existing.get(key) in (None, "", []):
                existing[key] = value
        return iri

    def has(self, class_name: str, iri: str) -> bool:
        return iri in self.nodes[self.slot_for[class_name]]

    def container(self):
        cls = getattr(self.module, graph_rdf.CONTAINER)
        members = {}
        for slot_name, bucket in self.nodes.items():
            items = []
            for fields in sorted(bucket.values(), key=lambda f: f["id"]):
                fields = dict(fields)
                node_class = getattr(self.module, fields.pop("_class"))
                items.append(node_class(**fields))
            members[slot_name] = items
        return cls(**members)

    # -- converters shared by the emitters ------------------------------------

    def principal(self, principal_id: int, is_individual: bool, company: str | None = None) -> tuple[str, str]:
        """(slot on an Authorization, value) for a Synapse principal: a user,
        a team, or one of the two groups that stand for everyone."""
        if principal_id in AGENT_CLASS_FOR_GROUP:
            return "agentClass", AGENT_CLASS_FOR_GROUP[principal_id]
        if is_individual:
            iri = graph_iris.user(principal_id)
            self.add("User", id=iri, company=company,
                     affiliatedWith=[self.site(company)] if company else None)
            return "agent", iri
        iri = graph_iris.team(principal_id)
        self.add("Team", id=iri)
        return "agentGroup", iri

    def user(self, principal_id) -> str | None:
        """A user referenced by id (createdBy, submittedBy, ...)."""
        if principal_id in (None, ""):
            return None
        return self.add("User", id=graph_iris.user(principal_id))

    def site(self, institution: str | None) -> str | None:
        if not institution:
            return None
        return self.add("Site", id=graph_iris.site(institution), institution=institution)

    def curated_access_requirement(self, record: dict, record_rules) -> str:
        """Adds a curated record-layer AccessRequirement's graph content: one
        Condition per data-use term (its parameters from the companion fields
        the record's DUO rules name) and the AR's data tier. Returns the AR IRI,
        which the record shares (R5)."""
        requirement = graph_iris.record_iri(record["id"])
        conditions = []
        for code in record.get("dataUseModifiers") or []:
            if code in NOT_A_TERM or not self.known("DataUseTerm", code, f"{record['id']} dataUseModifiers"):
                continue
            details = []
            for rule in record_rules:
                slot_conditions = rule.preconditions.slot_conditions if rule.preconditions else {}
                pre = slot_conditions.get("dataUseModifiers")
                if pre is None or pre.equals_string != code:
                    continue
                for companion in rule.postconditions.slot_conditions:
                    if companion == DISEASE_SLOT:
                        continue
                    values = record.get(companion)
                    values = values if isinstance(values, list) else [values]
                    details += [str(v) for v in values if v not in (None, "")]
            diseases = record.get(DISEASE_SLOT) or [] if code == DISEASE_TERM else []
            conditions.append(self.add(
                "Condition",
                id=graph_iris.condition(requirement, code),
                dataUseTerm=code,
                diseaseContext=[graph_iris.obo(d) for d in diseases],
                conditionDetail=sorted(set(details)),
                description=self.term_description(code),
            ))
        tiers = record.get("dataTier") or []
        tier = self.most_restrictive(tiers if isinstance(tiers, list) else [tiers])
        if isinstance(tiers, list) and len(tiers) > 1:
            warn(f"{record['id']} lists several data tiers {tiers}; using the most restrictive, {tier}.")
        self.add(
            "AccessRequirement",
            id=requirement,
            name=record.get("name"),
            requirementType=record.get("concreteType"),
            accessType=record.get("accessType"),
            dataTier=tier,
            hasCondition=conditions,
        )
        return requirement


def record_rules(schema_path: str = RECORD_SCHEMA):
    """The record layer's DUO rules (GovernanceMixin.rules): which companion
    field carries each data-use term's parameters."""
    return SchemaView(schema_path).get_class("GovernanceMixin").rules
