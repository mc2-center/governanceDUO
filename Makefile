# `make` with no target runs what CI runs. (The schematic-pipeline targets that
# built sage-ar-model/ were removed with it; see archive/.)
.DEFAULT_GOAL := validate-all

LINKML_SCHEMA := linkml/governance_duo.linkml.yaml

# Version of the published artifacts (see README "Release artifacts and IRI policy").
# Stamped into shapes/governance_duo.owl.ttl by `make owl`; the hand-written artifacts
# carry it in their owl:Ontology headers, and `make release-check` verifies they agree.
VERSION ?= 0.1.0

# The graph layer (plans/model_refactor.md): linkml/graph/ is the one source of
# every graph term; build_graph_tbox.py generates its one TBox and shape set.
# It runs beside the pre-refactor pipeline below until Phase 2 replaces that.
GRAPH_SCHEMA  := linkml/graph/governance.yaml
GRAPH_VERSION ?= 0.2.0
GRAPH_TBOX    := shapes/governance.owl.ttl
GRAPH_SHAPES  := shapes/governance.shacl.ttl
GRAPH_EXAMPLE_RDF := linkml/examples/graph/rdf/governance_graph.ttl

# ROBOT (https://robot.obolibrary.org) for the OWL 2 DL profile check. Fetched, not
# committed (78 MB), and pinned so the check is reproducible -- the same version and
# download rule sagebrain-model uses. Overridable: ROBOT_JAR, ROBOT_VERSION.
ROBOT_JAR     ?= tools/robot.jar
ROBOT_VERSION ?= 1.9.8
ROBOT_URL     ?= https://github.com/ontodev/robot/releases/download/v$(ROBOT_VERSION)/robot.jar

# W3C PROV-O (the 2013-04-30 Recommendation), fetched once into build/ for the
# prov: type-agreement check in owl-profile. Overridable: PROV_O, PROV_O_URL.
PROV_O        ?= build/prov-o-20130430.ttl
PROV_O_URL    ?= https://www.w3.org/ns/prov-o-20130430

# --ignore-warnings: this schema deliberately keeps the schematic CSV's camelCase
# attribute names (e.g. dataUseModifiers, StudyKey) instead of linkml-lint's preferred
# snake_case, since those names are also live Synapse annotation keys.
linkml-lint:
	linkml-lint --ignore-warnings ${LINKML_SCHEMA}
	linkml-lint --ignore-warnings $(GRAPH_SCHEMA)

owl:
	python3 scripts/build_owl.py --schema ${LINKML_SCHEMA} --out shapes/governance_duo.owl.ttl --version $(VERSION)

shacl:
	gen-shacl ${LINKML_SCHEMA} > shapes/governance_duo.shacl.ttl

$(ROBOT_JAR):
	@echo "Fetching ROBOT $(ROBOT_VERSION) (not committed -- 78 MB)"
	mkdir -p $(dir $@)
	curl -L --fail -o $@.tmp "$(ROBOT_URL)"
	mv $@.tmp $@

$(PROV_O):
	@echo "Fetching W3C PROV-O (not committed)"
	mkdir -p $(dir $@)
	curl -L --fail -H "Accept: text/turtle" -o $@.tmp "$(PROV_O_URL)"
	mv $@.tmp $@

# OWL 2 DL profile check on the record-layer TBox alone. The record OWL no
# longer shares any gov: terms with the graph TBox (linkml/graph/vocabularies.yaml's
# SKOS vocabularies are declared once, by graph-tbox, and only referenced here --
# scripts/build_owl.py's "not ours to give" rule), so there's no merged-TBox
# profile check left to run; graph-owl-profile below covers the graph TBox.
# Reports land in build/ (gitignored); the report is printed when a check fails.
# Last, every prov: term the record OWL declares (none, since Activity/Usage moved
# to the graph layer) must have the type W3C PROV-O gives it -- a mismatch is a
# pun wherever PROV-O is loaded alongside; see scripts/check_prov_alignment.py.
owl-profile: owl graph-tbox | $(ROBOT_JAR) $(PROV_O)
	mkdir -p build
	java -jar $(ROBOT_JAR) validate-profile --profile DL --input shapes/governance_duo.owl.ttl --output build/owl-profile-governance_duo.txt || (cat build/owl-profile-governance_duo.txt; exit 1)
	@echo "OWL 2 DL profile: governance_duo in profile."
	python3 scripts/check_prov_alignment.py --prov-o $(PROV_O)

graph-tbox:
	python3 scripts/build_graph_tbox.py --schema $(GRAPH_SCHEMA) --owl $(GRAPH_TBOX) --shacl $(GRAPH_SHAPES) --version $(GRAPH_VERSION)

graph-example-rdf:
	mkdir -p $(dir $(GRAPH_EXAMPLE_RDF))
	python3 scripts/graph_rdf.py linkml/examples/graph/*.example.yaml --out $(GRAPH_EXAMPLE_RDF)

# The canonical example conforms to the generated shapes, and check_graph.py
# confirms the shapes catch a set of deliberate defects and the TBox keeps the
# layer's conventions (SKOS completeness, no axioms on other vocabularies' terms).
graph-validate: graph-tbox graph-example-rdf
	python3 scripts/validate_graph.py --data $(GRAPH_EXAMPLE_RDF) --shapes $(GRAPH_SHAPES) --ont $(GRAPH_TBOX)
	python3 scripts/check_graph.py

# OWL 2 DL on the graph TBox alone and merged with every canonical ABox this
# repo produces in the graph namespace: the example graph, the derivation
# output, the projections' inputs (the same example graph, plus its
# authorizer_v1 projection), and the sync outputs when a live sync has been run
# and persisted them (governance_graph_export/*_synced.ttl) -- optional, since
# CI never runs a live sync. Replaces the old, separate owl-profile-abox
# (plans/model_refactor.md): the graph TBox no longer shares terms with the
# record layer, so there's nothing left to gain from merging the two TBoxes'
# ABoxes together.
graph-owl-profile: graph-tbox graph-example-rdf derivation-policy projections | $(ROBOT_JAR)
	mkdir -p build
	java -jar $(ROBOT_JAR) validate-profile --profile DL --input $(GRAPH_TBOX) --output build/owl-profile-governance.txt || (cat build/owl-profile-governance.txt; exit 1)
	java -jar $(ROBOT_JAR) merge --input $(GRAPH_TBOX) --input $(GRAPH_EXAMPLE_RDF) \
		--input derivation_policy_export/derivation_policy.ttl \
		--input governance_graph_export/authorizer_v1.ttl \
		$(if $(wildcard governance_graph_export/governance_graph_synced.ttl),--input governance_graph_export/governance_graph_synced.ttl,) \
		$(if $(wildcard provenance_graph_export/provenance_graph_synced.ttl),--input provenance_graph_export/provenance_graph_synced.ttl,) \
		--output build/governance_with_example.owl.ttl
	java -jar $(ROBOT_JAR) validate-profile --profile DL --input build/governance_with_example.owl.ttl --output build/owl-profile-governance-abox.txt || (cat build/owl-profile-governance-abox.txt; exit 1)
	@echo "OWL 2 DL profile: the graph TBox, alone and with every canonical ABox, in profile."

example-rdf:
	python3 scripts/convert_examples_to_rdf.py --schema ${LINKML_SCHEMA} --examples-dir linkml/examples --out-dir linkml/examples/rdf

shacl-validate: owl shacl example-rdf
	python3 scripts/validate_graph.py --data shapes/governance_duo.owl.ttl --shapes shapes/governance_duo.shacl.ttl --instances linkml/examples/rdf/all_examples.ttl

policy-fabric:
	python3 scripts/build_policy_fabric.py linkml/examples/access_requirement_policy_fabric.example.yaml --out-dir policy_fabric_export

# The worked example is built as of a fixed time (2026-01-01), inside its
# AccessApproval's validity window, so the export doesn't change as the calendar
# passes the approval's expiredOn. A live sync judges expiry as of the sync.
GOVERNANCE_GRAPH_AS_OF ?= 1767225600000

# The canonical example is the governance export (plans/model_refactor.md): built
# from linkml/examples/graph/*.example.yaml, the same source graph-example-rdf
# reads, via graph_rdf.py -- the one path from graph-layer data to Turtle.
governance-graph: graph-tbox
	mkdir -p governance_graph_export
	python3 scripts/graph_rdf.py linkml/examples/graph/*.example.yaml --out governance_graph_export/governance_graph.ttl

governance-graph-validate: governance-graph
	python3 scripts/validate_graph.py --data governance_graph_export/governance_graph.ttl --shapes $(GRAPH_SHAPES) --ont $(GRAPH_TBOX)

# Real Synapse data, not the hand-authored examples above -- requires an ACT
# (or validated-reviewer) synapseclient login. See
# plans/governance_graph_ingestion.md for the full design.
# Usage: make sync-governance-graph ENTITY_IDS="syn10081783 syn2343195"
sync-governance-graph:
	python3 scripts/sync_governance_graph.py $(ENTITY_IDS)

sync-governance-graph-validate: graph-tbox
	python3 scripts/validate_graph.py --data governance_graph_export/governance_graph_synced.ttl --shapes $(GRAPH_SHAPES) --ont $(GRAPH_TBOX)

# Derivation Policy Graph (linkml/derivation_policy.yaml) -- see
# plans/prov_o_integration.md. DerivationRule (the record-layer part that
# remains here; ControlLabel/DerivationReview moved to the graph layer,
# plans/model_refactor.md) is imported into governance_duo.linkml.yaml, so
# `make owl`/`make shacl` already regenerate its shapes as part of
# shapes/governance_duo.owl.ttl/.shacl.ttl -- no separate shapes file needed,
# only a separate example-instance/RDF/validation pass.

# Real Synapse provenance data (Activity/used/generatedBy), not the hand-authored
# examples above -- requires the same synapseclient login as sync-governance-graph.
# Usage: make sync-provenance-graph ENTITY_IDS="syn10081783 syn2343195"
sync-provenance-graph:
	python3 scripts/sync_provenance_graph.py $(ENTITY_IDS)

# Offline check of sync_governance_graph.py against a fake Synapse client (no
# network/credentials): grants, ARs, submissions, approvals, and unknown values.
# Validates its output against the one graph TBox and shape set, hence `graph-tbox`.
sync-governance-check: graph-tbox
	python3 scripts/check_sync_governance.py

# Offline regression check for sync_provenance_graph.py (fake Synapse client, no
# network or credentials) -- see scripts/check_sync_provenance.py. Validates its
# output against the one graph TBox and shape set, hence `graph-tbox`.
sync-provenance-check: graph-tbox
	python3 scripts/check_sync_provenance.py

derivation-policy-example-rdf:
	python3 scripts/convert_examples_to_rdf.py --examples-dir linkml/examples/derivation_policy --out-dir linkml/examples/derivation_policy/rdf

derivation-policy-validate: owl shacl derivation-policy-example-rdf
	python3 scripts/validate_graph.py --data shapes/governance_duo.owl.ttl --shapes shapes/governance_duo.shacl.ttl --instances linkml/examples/derivation_policy/rdf/all_examples.ttl

# Computes ControlLabel/DerivationReview from the canonical governance graph
# (plans/model_refactor.md). Defaults to the canonical example
# (linkml/examples/graph/rdf/governance_graph.ttl, built by graph-example-rdf) so
# this works with no live Synapse access; pass
# DERIVATION_POLICY_GRAPH=governance_graph_export/governance_graph_synced.ttl
# (after sync-governance-graph/sync-provenance-graph) for real data.
DERIVATION_POLICY_GRAPH := $(GRAPH_EXAMPLE_RDF)
derivation-policy: graph-example-rdf
	python3 scripts/build_derivation_policy.py --graph $(DERIVATION_POLICY_GRAPH) --derivation-rules linkml/examples/derivation_policy --out derivation_policy_export/derivation_policy.ttl

# Regression check: runs build_derivation_policy.py on the committed fixture in
# linkml/examples/derivation_policy/fixture/ and asserts its labels/reviews, and
# that its output (merged with its inputs) conforms to the one generated graph
# TBox and shape set (hence `graph-tbox`).
derivation-policy-check: graph-tbox
	python3 scripts/check_derivation_policy.py

# ISO-8601 form of GOVERNANCE_GRAPH_AS_OF (2026-01-01T00:00:00Z): projections
# (plans/model_refactor.md) bind their --as-of through SPARQL initBindings, which
# needs an xsd:dateTime, not the old builder's epoch-millisecond long.
GOVERNANCE_GRAPH_AS_OF_ISO ?= 2026-01-01T00:00:00Z

# Runs the canonical example graph through projections/authorizer_v1.rq (and,
# with TEAMS=1, authorizer_v1_teams.rq too) -> governance_graph_export/. This is
# what sagebrain-infra's authorizer actually reads (plans/model_refactor.md);
# governance-graph is the canonical export, not this projection.
projections: graph-example-rdf
	python3 scripts/project.py --graph $(GRAPH_EXAMPLE_RDF) --query projections/authorizer_v1.rq --as-of $(GOVERNANCE_GRAPH_AS_OF_ISO) --out governance_graph_export/authorizer_v1.ttl
	$(if $(TEAMS),python3 scripts/project.py --graph $(GRAPH_EXAMPLE_RDF) --query projections/authorizer_v1_teams.rq --as-of $(GOVERNANCE_GRAPH_AS_OF_ISO) --out governance_graph_export/authorizer_v1_teams.ttl,)

# Regression check for projections/authorizer_v1(_teams).rq and scripts/project.py:
# golden diff against tests/golden/governance_graph.ttl, approval expiry (replaces
# check_approval_expiry.py), team-member and descendant-grant behavior.
projections-check: graph-tbox graph-example-rdf
	python3 scripts/check_projections.py

# Contract check against sagebrain-infra's authorizer: runs its governance query
# (pinned copy in tests/infra_contract/) against the authorizer_v1 projection.
# Set SAGEBRAIN_INFRA=<infra checkout or authorize.py> to run infra's own code instead.
infra-contract-check: projections
	python3 scripts/check_infra_contract.py

# linkml-validate every example: the only enforcer of the DUO `rules:`, which
# neither the SHACL nor the OWL carries.
linkml-validate-examples:
	python3 scripts/validate_examples.py

# Committed generated artifacts must match what the schema and scripts produce.
# Regenerates everything itself; CI runs it after validate-all.
# Clears the generated directories first, so a committed file no generator
# produces any more shows up as missing.
artifact-drift-check:
	rm -rf docs/reference policy_fabric_export linkml/examples/rdf linkml/examples/derivation_policy/rdf linkml/examples/graph/rdf derivation_policy_export
	$(MAKE) owl shacl example-rdf derivation-policy-example-rdf governance-graph docs policy-fabric graph-tbox graph-example-rdf projections derivation-policy
	python3 scripts/check_artifact_drift.py

validate-all: shacl-validate governance-graph-validate derivation-policy-validate sync-provenance-check sync-governance-check derivation-policy-check infra-contract-check projections-check linkml-validate-examples owl-profile graph-validate graph-owl-profile

# Opt-in: checks this repo's governance layer works as a layer of sagebrain-model's
# graph (union OWL 2 DL, SHACL on a joined worked example, ControlLabels reaching
# sagebrain nodes). Needs a sagebrain-model checkout, so it isn't in validate-all.
# Usage: make sagebrain-contract-check SAGEBRAIN_MODEL=../sagebrain-model
sagebrain-contract-check: graph-tbox governance-graph | $(ROBOT_JAR)
	$(if $(SAGEBRAIN_MODEL),,$(error set SAGEBRAIN_MODEL=<path to a sagebrain-model checkout>))
	python3 scripts/check_sagebrain_contract.py --sagebrain-model $(SAGEBRAIN_MODEL) --robot-jar $(ROBOT_JAR)

# Pre-release gate: everything validate-all checks, plus every published artifact
# carrying its own version (VERSION for the record layer, GRAPH_VERSION for the
# graph layer -- they release independently, plans/model_refactor.md), and, with
# TAG=v<version>, the tag agreeing with VERSION.
release-check: validate-all
	python3 scripts/check_release.py --version $(VERSION) --graph-version $(GRAPH_VERSION) $(if $(TAG),--tag $(TAG))

docs-examples:
	python3 scripts/prepare_doc_examples.py --examples-dir linkml/examples --out-dir docs/example_instances

docs: docs-examples
	gen-doc ${LINKML_SCHEMA} -d docs/reference --render-imports --example-directory docs/example_instances --subfolder-type-separation

# Full docs-site preview (mkdocs + Material theme + Mermaid rendering). `docs-build`
# always regenerates docs/reference/ first (via the `docs` target) so the preview
# can't go stale relative to the schema. `site/` is gitignored build output. Narrative
# pages link out to source files (linkml/*.yaml, scripts/*.py, etc.) outside docs_dir
# via their GitHub blob URL rather than a relative path, so --strict is safe here and
# is also what .github/workflows/docs.yml runs for the published Pages site.
docs-build: docs
	mkdocs build --strict

docs-serve: docs
	mkdocs serve
