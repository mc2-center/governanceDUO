# Slide: Four layers, one pipeline

**Figure:** the governance graph's four layers, redrawn as a compact layer
strip, sitting above the pipeline that builds and reads them (merges the
former layer-stack and pipeline-architecture figures:
[graph-design.md, sections 2–4](../../graph-design.md#2-where-it-sits-in-sage-brain)).

## What each layer lets the graph do

- **Governance** (W3C Web Access Control + vCard) — capture who holds which
  permission, and which Access Requirements govern an entity, direct or
  inherited through the container hierarchy. *Answers: who may do what?*
- **Conditions** (Data Use Ontology) — capture what an Access Requirement
  actually demands, as structured terms rather than free text — the one thing
  Synapse itself has no place to record, so curators author it directly.
  *Answers: what does approval actually require?*
- **Provenance** (W3C PROV-O) — capture what was computed from what, and by
  which tool, straight from Synapse's own provenance feature.
  *Answers: where did this content come from?*
- **Derivation policy** (this repo's own vocabulary) — precompute, once, what a
  derived entity inherits and flag any risky combination of independently
  approved sources, so nothing has to be re-derived by hand on every query.
  *Answers: what does derived content inherit, and is it safe to combine?*
- **Projections** — a layer derived on export for a specific consumer (e.g.
  `authorizer_v1` for sagebrain-infra), computed from the four layers above
  rather than authored or stored independently.

## The founding questions

1. **Direct access** — which principals hold which permissions on an entity, and
   which Access Requirements govern it?
2. **Conditions** — what does a given Access Requirement actually demand, as
   terms a machine can reason over?
3. **Derived access** — when content is computed from controlled data, what does
   it inherit, and does combining independently approved sources create risk
   neither approval covered on its own?

## Why the pipeline is shaped this way

- **Synapse** stays the source of truth for ACLs, Access Requirements,
  submissions, approvals, and provenance — the graph never invents facts.
- **ACT/curators** supply the one missing piece — DUO conditions and data
  tier — directly on the Access Requirement itself.
- **governanceDUO** (this repo) builds each layer on shared IRIs — Governance
  and Provenance synced from Synapse, Conditions from curator annotations,
  Derivation policy and Projections computed from the layers above — so each
  layer can be synced, authored, or computed by a different party without the
  others needing to change.
- governanceDUO publishes its layer vocabulary as versioned TBox + SHACL
  shapes (`shapes/governance.*.ttl`); sagebrain-model imports it rather than
  copying it, so the domain graph and the governance graph can't drift apart.
- **sagebrain-infra** (its Neptune-backed graph) reads the layers directly
  through its Query API, but its ReBAC authorizer never queries them
  directly for authorization decisions — it reads the purpose-built
  `authorizer_v1` projection instead, so its existing Cedar policy contract
  never has to change even as the model underneath it improves.
