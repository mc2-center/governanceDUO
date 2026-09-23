"""
graph_iris.py

The only place IRIs are minted for the governance graph (plans/model_refactor.md,
R2/R3/R5). Every emitter -- the examples, the Synapse syncs, the derivation
builder -- and every check builds node IRIs through these functions, so the same
thing always gets the same IRI.

- Synapse's own things use Synapse's own URLs: entities
  https://www.synapse.org/Synapse:syn<n>, users .../Profile:<n>, teams
  .../Team:<n> (R3).
- Everything the layer mints sits beside the model's namespace, not inside it
  (R2): https://w3id.org/synapse/governance/<kind>/<local>.
- One IRI per Access Requirement (R5): the curated record access_requirement.<n>
  and the graph node are both .../ar/<n> (record_iri()).

author: orion.banks
"""

import hashlib
import re

SYNAPSE = "https://www.synapse.org/"
ENTITY = f"{SYNAPSE}Synapse:"
USER = f"{SYNAPSE}Profile:"
TEAM = f"{SYNAPSE}Team:"
INSTANCE = "https://w3id.org/synapse/governance/"
RECORD = "https://w3id.org/sage-bionetworks/governance-duo/"
OBO = "http://purl.obolibrary.org/obo/"

SYN_ID = re.compile(r"^(?:syn:|https://www\.synapse\.org/Synapse:)?(syn[0-9]+)$")
CURATED_AR_ID = re.compile(r"^access_requirement\.([0-9]+)$")


def _minted(kind: str, local) -> str:
    local = str(local)
    if not local or "/" in local or " " in local:
        raise ValueError(f"not a usable {kind} id: {local!r}")
    return f"{INSTANCE}{kind}/{local}"


def slug(text: str) -> str:
    """'Mount Sinai' -> 'mount-sinai'."""
    value = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    if not value:
        raise ValueError(f"nothing to slug in {text!r}")
    return value


def synapse_id(value: str) -> str:
    """'syn123', 'syn:syn123' or the full IRI -> 'syn123'."""
    match = SYN_ID.match(str(value))
    if not match:
        raise ValueError(f"not a Synapse entity id: {value!r}")
    return match.group(1)


def entity(value: str) -> str:
    return ENTITY + synapse_id(value)


def user(principal_id) -> str:
    return f"{USER}{int(principal_id)}"


def team(principal_id) -> str:
    return f"{TEAM}{int(principal_id)}"


def principal_id(iri: str) -> int:
    """The numeric Synapse principal id at the end of a user or team IRI."""
    return int(str(iri).rsplit(":", 1)[1])


def access_requirement(requirement_id) -> str:
    return _minted("ar", int(requirement_id))


def condition(requirement_iri: str, term_curie: str) -> str:
    """The condition of an AR for one data-use term: .../ar/42/condition/DUO_0000007
    (a Sage DUOPlus term keeps its own name: .../condition/DUOPlus1)."""
    local = term_curie.replace(":", "_") if term_curie.startswith("DUO:") else term_curie
    return f"{requirement_iri}/condition/{local}"


def authorization(benefactor: str, principal) -> str:
    """One ACL entry: the benefactor's ACL, for one principal (or agent class name)."""
    return _minted("authorization", f"{synapse_id(benefactor)}-{principal}")


def approval(approval_id) -> str:
    return _minted("approval", int(approval_id))


def submission(submission_id) -> str:
    return _minted("submission", int(submission_id))


def request(request_id) -> str:
    return _minted("request", int(request_id))


def research_project(project_id) -> str:
    return _minted("research-project", int(project_id))


def site(institution: str) -> str:
    return _minted("site", slug(institution))


def program(name: str) -> str:
    return _minted("program", slug(name))


def ar_template(domain: str) -> str:
    return _minted("ar-template", slug(domain))


def irb_requirement(name: str) -> str:
    return _minted("irb-requirement", slug(name))


def activity(activity_id) -> str:
    return _minted("activity", int(activity_id))


def usage(activity_iri: str, index: int) -> str:
    return f"{activity_iri}/usage/{int(index)}"


def control_label(subject: str) -> str:
    """A label is keyed by its subject: .../control-label/syn<n> for a Synapse
    entity, .../control-label/iri-<hash> for anything else a label reaches
    (e.g. a sagebrain-model Association)."""
    if SYN_ID.match(str(subject)):
        return _minted("control-label", synapse_id(subject))
    return _minted("control-label", "iri-" + hashlib.sha1(str(subject).encode()).hexdigest()[:12])


def derivation_review(activity_iri: str) -> str:
    """A derivation review is keyed by the activity it reviews."""
    return _minted("derivation-review", activity_iri.rstrip("/").rsplit("/", 1)[1])


def record_iri(record_id: str) -> str:
    """The IRI a record-layer record is written under: a curated Access
    Requirement shares its graph node's IRI (R5); every other record keeps the
    record namespace (governanceduo:<id>)."""
    if ":" in record_id:
        raise ValueError(f"'{record_id}' already contains a colon; expected a bare dotted id")
    match = CURATED_AR_ID.match(record_id)
    if match:
        return access_requirement(match.group(1))
    return f"{RECORD}{record_id}"


def obo(curie: str) -> str:
    """'MONDO:0004975' -> http://purl.obolibrary.org/obo/MONDO_0004975."""
    prefix, _, local = curie.partition(":")
    if not prefix or not local:
        raise ValueError(f"not an OBO CURIE: {curie!r}")
    return f"{OBO}{prefix}_{local}"
