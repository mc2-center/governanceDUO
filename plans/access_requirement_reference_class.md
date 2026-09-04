Give the AccessRequirement graph-stub its own LinkML identity, closing the
hasCondition/owl:sameAs "no slot backs this" gap

Implemented (2026-09-04) — all six target changes landed as planned, no scope
deviations. See access_requirement_reference_class_report.md for what changed and
verification results.

Context

Two related audits landed on 2026-09-04 (see plans/governance_consolidation_and_drs_interop_report.md's
class_uri/slot_uri work, and this session's shapes/governance_duo.shacl.ttl vs.
shapes/governance_graph.shacl.ttl comparison). Testing directly (validate
governance_graph_export/governance_graph.ttl against shapes/governance_duo.shacl.ttl +
.owl.ttl with pySHACL, inference="none", no hand-authored shapes at all) surfaced 48
violations. Two of the six root causes are specific to one thing:
scripts/build_governance_graph.py's `gov:AccessRequirement` stub node (`gov:AR-<n>`,
minted in `add_access_requirement_association()`) has no LinkML class of its own —

- **ClassConstraintComponent (5 violations)**: every slot that actually holds this
  stub's IRI in the exported ABox (`AccessRequirementAssociation.accessRequirement`,
  `DataAccessSubmission`/`ResearchProject`/`DataAccessRequest`'s shared
  `accessRequirementId`, `AccessApproval.requirementId`) is declared `range:
  AccessRequirement` — the *real* class from access_requirement.yaml — so gen-shacl
  expects `sh:class governanceduo:AccessRequirement`, while the stub is typed
  `gov:AccessRequirement` (a different IRI in the current schema, since
  `AccessRequirement` has no `class_uri`).
- **hasCondition has no slot at all.** `add_access_requirement()`'s own docstring
  (scripts/build_governance_graph.py) explains why: the real `AccessRequirement`
  class lives in access_requirement.yaml, which governance_graph.yaml imports (not
  the other way around), so a slot declared on `AccessRequirement` could never range
  over `Condition` (defined in governance_graph.yaml) without an import cycle.
- The stub's own `owl:sameAs` link back to the real
  `governanceduo:access_requirement.<n>` individual is also a hardcoded
  `g.add((ar_node, OWL.sameAs, ...))` with no `governance_graph.yaml` slot behind it
  — same underlying cause (no class of its own to hang a `slot_uri` on).

A same-session first attempt at (1) — adding `class_uri: sagegov:AccessRequirement`
directly onto access_requirement.yaml's real `AccessRequirement` class — was tried,
fixed the 5 ClassConstraintComponent violations, then was **reverted**. Two reasons,
both confirmed empirically: it had zero effect on the pipeline that actually runs
(`make governance-graph-validate` uses the hand-authored shapes/governance_graph.shacl.ttl,
which already declares its own `gov:AccessRequirementShape` independent of
access_requirement.yaml's `class_uri`), and it silently collapsed a deliberate design
choice documented in the script itself (scripts/build_governance_graph.py, the comment
directly above `g.add((ar_node, RDF.type, GOV.AccessRequirement))`): the stub is
supposed to be a *different* type from the real `AccessRequirement`, linked only by
`owl:sameAs`, not merged with it.

This plan fixes the same three gaps without that mistake: by giving the *stub* its
own class, instead of mutating the real class's identity.

Precedent already landed this session: `IRBRequirement.studyId` (linkml/governance_graph.yaml)
now declares `slot_uri: owl:sameAs`, `range: uriorcurie` — letting
`scripts/build_governance_graph.py` resolve that cross-namespace co-reference via
`PREDICATE()` instead of a hardcoded `OWL.sameAs` constant, verified output-preserving
(the exported ABox is byte-identical) and confirmed to close the corresponding
ClosedConstraintComponent violation. `range: uriorcurie` rather than `range: Study` was
deliberate: the referenced individual is never itself typed in this ABox (its full
definition lives only in the separately-built linkml/examples/rdf/ graph), so an
`sh:class` constraint would fail even on a correct reference. The same reasoning
applies to the AR stub's `owl:sameAs` link below.

Target changes

1. New class in linkml/governance_graph.yaml: `AccessRequirementReference`.
   - Not `is_a: BaseEntity` — like `Condition`/`DataAccessSubmissionStatus`, the stub
     has no independent identifier of its own (it's a re-serialization of the real
     AccessRequirement's own id via `gov_id()`, not a new entity).
   - `class_uri: sagegov:AccessRequirement` — the exact IRI
     scripts/build_governance_graph.py already emits as `GOV.AccessRequirement`, so
     no change to what's on the wire.
   - `slots:`
     - `sameAs` — `slot_uri: owl:sameAs`, `range: uriorcurie`, `required: true`
       (every stub instance bridges to a real AccessRequirement). Same pattern as
       `IRBRequirement.studyId`.
     - `hasCondition` — `slot_uri: sagegov:hasCondition`, `range: Condition`,
       `multivalued: true`.
   - Requires no new import: `Condition` is already defined in this same file.

2. Repoint the three slots that are actually populated with the stub's IRI (not the
   real AccessRequirement's) from `range: AccessRequirement` to
   `range: AccessRequirementReference`:
   - `AccessRequirementAssociation.accessRequirement` (linkml/governance_graph.yaml:648)
   - `accessRequirementId` (shared by `DataAccessSubmission`/`ResearchProject`/
     `DataAccessRequest`; linkml/governance_graph.yaml:657)
   - `AccessApproval.requirementId` (linkml/governance_graph.yaml:811)
   Leave `slot_uri`/descriptions on all three untouched — only `range` changes.

3. scripts/build_governance_graph.py, `add_access_requirement_association()`:
   - `g.add((ar_node, RDF.type, GOV.AccessRequirement))` →
     `g.add((ar_node, RDF.type, TYPE("AccessRequirementReference")))`.
   - `g.add((ar_node, OWL.sameAs, GOVERNANCEDUO[data["accessRequirement"]]))` →
     `g.add((ar_node, PREDICATE("sameAs", "AccessRequirementReference"),
     GOVERNANCEDUO[data["accessRequirement"]]))`.
   - Rewrite the comment block above these two lines (currently explains why `ar_node`
     is deliberately *not* typed with `AccessRequirement`'s own URI) to describe the
     new `AccessRequirementReference` class instead of "a local gov:-namespace stub
     type... not a use of AccessRequirement's own declared URI" — the reasoning is
     the same, but there's now a real class backing it.

4. scripts/build_governance_graph.py, `add_access_requirement()`:
   - Replace the hardcoded `GOV.hasCondition` constant with
     `PREDICATE("hasCondition", "AccessRequirementReference")`.
   - Rewrite the docstring section explaining the import-cycle blocker — it's
     resolved now: `AccessRequirementReference` (unlike the real `AccessRequirement`)
     is owned by governance_graph.yaml, the same file that defines `Condition`, so
     there's no cross-file cycle to avoid.

5. Regenerate shapes/governance_duo.owl.ttl / shapes/governance_duo.shacl.ttl
   (`make owl shacl`). Do not touch shapes/governance_graph.owl.ttl /
   shapes/governance_graph.shacl.ttl's actual shapes — they already hand-declare
   `hasCondition` and this stub's shape correctly; only their header comments may need
   a note that these three gaps are now also schema-derivable (mirroring the header
   fix already made for the `sagegov:AccessGrant`-class-of-shapes claim), not that
   they're safe to delete.

6. Update the two places that currently document these as permanent, un-fixable
   "no slot backs this" gaps, since they no longer belong in that list:
   - docs/knowledge-graph.md's "What's still hand-written" bullet list (drop the
     hasCondition bullet and the AR-stub identity note from
     scripts/build_governance_graph.py's docstring reference; the `owl:sameAs`-only
     remaining gap becomes `IRBRequirement`'s pattern documented as *solved*, not
     outstanding).
   - shapes/governance_graph.owl.ttl / .shacl.ttl's own header comments, which
     currently list "the hasACL/hasAccessRequirement/hasApproval derived triples" and
     "Principal's bare-integer id minting" as the residual no-slot gaps —
     `hasCondition` should no longer be grouped with them.

Explicitly out of scope

- `hasACL`, `hasAccessRequirement`, `hasApproval` (derived/join-based triples on
  `SynapseEntity`/`Principal`) — genuinely different: no per-slot mapping exists for
  these even in principle (join logic / conditional emission), unlike hasCondition
  which only lacked a class to declare it on. Not addressed by this plan.

  **Reviewed**: `hasACL`/`hasAccessRequirement` aren't blocked by an import cycle
  (`SynapseEntity`/`AccessGrant`/the AR stub all live in governance_graph.yaml
  already) — they're pure inverses of already-declared slots (`AccessGrant.resource`,
  `AccessRequirementAssociation.resource`), left undeclared on purpose: an
  independent slot for a value that's always the mechanical inverse of another slot
  would itself be a new consistency risk (SHACL Core can't enforce "this triple
  exists iff its inverse does"), not a fix for one. The one legitimate, cheap
  improvement is LinkML's `inverse:` declaration (documents the `owl:inverseOf`
  relationship without requiring independent population) — real, but a different
  kind of fix than this plan's (schema self-documentation, not closing a validation
  gap), so left as its own optional future item, not folded in here.
  `hasApproval` is different again: it's conditional on a *different* record's field
  equaling `APPROVED` (`DataAccessSubmissionStatus.state` or `AccessApproval.status`)
  — `rules:`-shaped logic that `scripts/validate_graph.py`'s own docstring already
  documents `gen-shacl` doesn't compile into SHACL at all, so declaring it wouldn't
  close anything in the pipeline that actually runs. Conclusion: not valuable to fix
  as part of this plan — nothing is currently broken (the hand-written
  shapes/governance_graph.shacl.ttl already validates all three correctly).
- `Principal`'s bare-integer id minting and the `.`/`_` → `-` id-hyphenation display
  convention — same reasoning, not addressed here.
- Any change to access_requirement.yaml's real `AccessRequirement` class — this plan
  deliberately never touches it, which is the whole point versus the reverted attempt.

Verification plan

- `python3 scripts/build_governance_graph.py --examples-dir linkml/examples/governance_graph --out governance_graph_export/governance_graph.ttl`,
  then `git diff governance_graph_export/governance_graph.ttl` — must be empty
  (byte-identical output; same discipline plans/governance_consolidation_and_drs_interop_report.md
  used: "diff the regenerated ABox against the pre-change committed version — must be
  triple-set-identical").
- `make shacl-validate` and `make governance-graph-validate` — both must still report
  `Conforms: True` (these are the two pipelines that actually run in CI/local dev;
  neither should regress, and governance-graph-validate wasn't even exercising this
  code path before).
- Direct pySHACL run (the same ad hoc check used to find the 48 violations
  originally): validate governance_graph_export/governance_graph.ttl against
  shapes/governance_duo.shacl.ttl + shapes/governance_duo.owl.ttl,
  `inference="none"`. Confirm: the 5 original ClassConstraintComponent violations and
  the hasCondition/owl:sameAs-related violations on the AR stub are gone, total
  violation count drops accordingly, and — the check that caught the previous
  attempt's mistake — no *new* violations appear anywhere else in the report.
