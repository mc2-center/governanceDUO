# DRS interoperability

This page is a **design document**, not a running integration — governanceDUO does
not expose a [GA4GH Data Repository Service (DRS)](https://ga4gh.github.io/data-repository-service-schemas/docs/)
API today. It records how the model *could* map onto DRS's object and authorization
semantics, so that work starts from an explicit crosswalk (`linkml/drs_alignment.yaml`)
rather than an ad hoc one if it's ever taken on.

## Why DRS is a good fit here

DRS's `DrsObject` (`id`, `self_uri`, `size`, `checksums`, `access_methods`, `aliases`,
...) is a standard shape for "here is a piece of data and how to fetch it." What's
more directly relevant to governanceDUO is DRS's **authorization discovery** model:

- `OPTIONS /objects/{object_id}` returns an `Authorizations` record naming which
  auth mechanisms a client may use (`None`/`BasicAuth`/`BearerAuth`/`PassportAuth`)
  and, for `PassportAuth`, a whitelist of acceptable Visa issuers
  (`passport_auth_issuers`).
- A **GA4GH Passport** is a signed JWT carrying one or more **Visa** claims — DRS
  standardizes discovering *which issuers* a server trusts and *how* the passport is
  transported, but explicitly leaves the claims-evaluation decision itself out of
  scope: *"it is not the responsibility of a DRS server to return a Passport, that is
  the responsibility of a Passport Broker and outside the scope of DRS."*

That gap is exactly what [Policy Fabric](policy-fabric.md) already fills for
governanceDUO: a Rego evaluator that checks a presented Verifiable Credential's claims
against a DUO code's declared conditions. **GA4GH Passports/Visas and Policy Fabric's
Verifiable-Credential model are structurally analogous** — both are "present a signed,
issuer-attested credential; evaluate its claims against a resource's declared
policy." A DRS server's authorization layer could plausibly *be* Policy Fabric behind
a DRS-shaped front door, with a `DataAccessSubmissionStatus.state == APPROVED` event
([Knowledge graph representation](knowledge-graph.md)) as the natural trigger for
issuing a Visa (type `ControlledAccessGrants`, value = the governed dataset's `drs://`
URI) to the approved Principal.

## The identifier mapping

governanceDUO currently has three separate ways to reference "a Synapse entity":
`AccessRequirement.entityIdList`, `PolicyFabricMixin.assetBindings[].synapseId`
(see [The LinkML model](linkml-model.md)), and `SynapseEntity.id`
([Knowledge graph representation](knowledge-graph.md)). Rather than adding a *fourth*
internal scheme for DRS, `linkml/drs_alignment.yaml`'s `DrsObjectMapping` class makes
Synapse's own id the canonical DRS identifier and uses DRS's own sanctioned
secondary-identifier field, `aliases`, to carry everything else:

- Synapse ids (`syn<n>`) already satisfy DRS's allowed id charset
  (`[A-Za-z0-9.-_~]`), so `drsId` is simply the `syn<n>` value, and `drsSelfUri` is a
  hostname-based `drs://<hostname>/syn<n>` URI.
- `aliases` carries the governanceDUO dotted id(s) that reference this same entity
  (e.g. `access_requirement.101`) and/or the corresponding `gov:`-namespace
  `SynapseEntity` individual.

## Worked example (illustrative — not generated)

Using the same `access_requirement.101` / `syn98765432` example from
[Policy Fabric integration](policy-fabric.md):

**`DrsObjectMapping`** for `syn98765432`:

```json
{
  "synapseId": "syn98765432",
  "drsId": "syn98765432",
  "drsSelfUri": "drs://drs.synapse.example.org/syn98765432",
  "aliases": ["access_requirement.101"]
}
```

**The DRS `Authorizations` record** a server would return from
`OPTIONS /objects/syn98765432`, derived from that same AccessRequirement's
`dataUseModifiers` (`DUO:0000022`, `DUO:0000028`) and `trustedIssuerDids`:

```json
{
  "drs_object_id": "syn98765432",
  "supported_types": ["PassportAuth"],
  "passport_auth_issuers": ["did:example:sage_bionetworks_issuer"]
}
```

`passport_auth_issuers` here comes straight from the example's
`trustedIssuerDids: [did:example:sage_bionetworks_issuer]` — the same DID-as-issuer
convention `linkml/drs_alignment.yaml`'s `DrsAuthorizationBinding.passportAuthIssuers`
documents.

## What this page is not

There is no `scripts/build_drs_mapping.py`, no `drs_export/` directory, and no
Makefile target — this is a schema-and-docs-only design pass. If a real DRS
integration is taken on later, `linkml/drs_alignment.yaml`'s classes are the starting
point for generating these records from real `AccessRequirement`/`SynapseEntity`/
`PolicyCardBinding` data instead of hand-writing them, the way
[`scripts/build_policy_fabric.py`](https://github.com/mc2-center/governanceDUO/blob/main/scripts/build_policy_fabric.py) already does
for Policy Fabric's own input shape.
