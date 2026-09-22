CSV := sage-ar-model/sage-ar.model.csv
CONFIG := ar_config.yml
DATA := AccessRequirement Resource Study

all: collate generate-json

build-csv:
	$(foreach d,$(DATA), schematic manifest -c ${CONFIG} get -dt $(d);)
	rm *.schema.json

collate:
	@echo "Collating module components..."
	head -1 model/Study.model.csv > ${CSV}
	tail -n +2 -q model/*.model.csv >> ${CSV}

convert:
	schematic schema convert ${CSV}

generate-json:
	python scripts/create_json_from_model.py ${DATA}

LINKML_SCHEMA := linkml/governance_duo.linkml.yaml

# ROBOT (https://robot.obolibrary.org) for the OWL 2 DL profile check. Fetched, not
# committed (78 MB), and pinned so the check is reproducible -- the same version and
# download rule sagebrain-model uses. Overridable: ROBOT_JAR, ROBOT_VERSION.
ROBOT_JAR     ?= tools/robot.jar
ROBOT_VERSION ?= 1.9.8
ROBOT_URL     ?= https://github.com/ontodev/robot/releases/download/v$(ROBOT_VERSION)/robot.jar

# --ignore-warnings: this schema deliberately keeps the schematic CSV's camelCase
# attribute names (e.g. dataUseModifiers, StudyKey) instead of linkml-lint's preferred
# snake_case, since those names are also live Synapse annotation keys.
linkml-lint:
	linkml-lint --ignore-warnings ${LINKML_SCHEMA}

owl:
	python3 scripts/build_owl.py --schema ${LINKML_SCHEMA} --out shapes/governance_duo.owl.ttl

shacl:
	gen-shacl ${LINKML_SCHEMA} > shapes/governance_duo.shacl.ttl

$(ROBOT_JAR):
	@echo "Fetching ROBOT $(ROBOT_VERSION) (not committed -- 78 MB)"
	mkdir -p $(dir $@)
	curl -L --fail -o $@.tmp "$(ROBOT_URL)"
	mv $@.tmp $@

# OWL 2 DL profile check: the generated TBox, the hand-written governance graph
# TBox, and their merge (they share gov: terms, so each passing alone isn't enough).
# Reports land in build/ (gitignored); the report is printed when a check fails.
owl-profile: owl | $(ROBOT_JAR)
	mkdir -p build
	java -jar $(ROBOT_JAR) validate-profile --profile DL --input shapes/governance_duo.owl.ttl --output build/owl-profile-governance_duo.txt || (cat build/owl-profile-governance_duo.txt; exit 1)
	java -jar $(ROBOT_JAR) validate-profile --profile DL --input shapes/governance_graph.owl.ttl --output build/owl-profile-governance_graph.txt || (cat build/owl-profile-governance_graph.txt; exit 1)
	java -jar $(ROBOT_JAR) merge --input shapes/governance_duo.owl.ttl --input shapes/governance_graph.owl.ttl validate-profile --profile DL --output build/owl-profile-merged.txt || (cat build/owl-profile-merged.txt; exit 1)
	@echo "OWL 2 DL profile: governance_duo, governance_graph, and their merge all in profile."

example-rdf:
	python3 scripts/convert_examples_to_rdf.py --schema ${LINKML_SCHEMA} --examples-dir linkml/examples --out-dir linkml/examples/rdf

shacl-validate: owl shacl example-rdf
	python3 scripts/validate_graph.py --data shapes/governance_duo.owl.ttl --shapes shapes/governance_duo.shacl.ttl --instances linkml/examples/rdf/all_examples.ttl

policy-fabric:
	python3 scripts/build_policy_fabric.py linkml/examples/access_requirement_policy_fabric.example.yaml --out-dir policy_fabric_export

governance-graph:
	python3 scripts/build_governance_graph.py --examples-dir linkml/examples/governance_graph --out governance_graph_export/governance_graph.ttl

governance-graph-validate: governance-graph
	python3 scripts/validate_graph.py --data governance_graph_export/governance_graph.ttl --shapes shapes/governance_graph.shacl.ttl --ont shapes/governance_graph.owl.ttl

# Real Synapse data, not the hand-authored examples above -- requires an ACT
# (or validated-reviewer) synapseclient login. See
# plans/governance_graph_ingestion.md for the full design.
# Usage: make sync-governance-graph ENTITY_IDS="syn10081783 syn2343195"
sync-governance-graph:
	python3 scripts/sync_governance_graph.py $(ENTITY_IDS)

sync-governance-graph-validate:
	python3 scripts/validate_graph.py --data governance_graph_export/governance_graph_synced.ttl --shapes shapes/governance_graph.shacl.ttl --ont shapes/governance_graph.owl.ttl

# Provenance Graph (linkml/provenance.yaml) and Derivation Policy Graph
# (linkml/derivation_policy.yaml) -- see plans/prov_o_integration.md. Both are
# imported into governance_duo.linkml.yaml (like governance_graph.yaml already is),
# so `make owl`/`make shacl` already regenerate their shapes as part of
# shapes/governance_duo.owl.ttl/.shacl.ttl -- no separate shapes files needed, only
# separate example-instance/RDF/validation passes, one per layer.
provenance-example-rdf:
	python3 scripts/convert_examples_to_rdf.py --examples-dir linkml/examples/provenance --out-dir linkml/examples/provenance/rdf

provenance-validate: owl shacl provenance-example-rdf
	python3 scripts/validate_graph.py --data shapes/governance_duo.owl.ttl --shapes shapes/governance_duo.shacl.ttl --instances linkml/examples/provenance/rdf/all_examples.ttl

# Real Synapse provenance data (Activity/used/generatedBy), not the hand-authored
# examples above -- requires the same synapseclient login as sync-governance-graph.
# Usage: make sync-provenance-graph ENTITY_IDS="syn10081783 syn2343195"
sync-provenance-graph:
	python3 scripts/sync_provenance_graph.py $(ENTITY_IDS)

# Offline regression check for sync_provenance_graph.py (fake Synapse client, no
# network or credentials) -- see scripts/check_sync_provenance.py.
sync-provenance-check:
	python3 scripts/check_sync_provenance.py

derivation-policy-example-rdf:
	python3 scripts/convert_examples_to_rdf.py --examples-dir linkml/examples/derivation_policy --out-dir linkml/examples/derivation_policy/rdf

derivation-policy-validate: owl shacl derivation-policy-example-rdf
	python3 scripts/validate_graph.py --data shapes/governance_duo.owl.ttl --shapes shapes/governance_duo.shacl.ttl --instances linkml/examples/derivation_policy/rdf/all_examples.ttl

# Computes ControlLabel/DerivationReview from a Provenance Graph + Governance Graph.
# Defaults to the illustrative example-driven builds (linkml/examples/provenance/rdf/
# all_examples.ttl + governance_graph_export/governance_graph.ttl, both built by the
# targets above/governance-graph) so this works with no live Synapse access; pass
# PROVENANCE_GRAPH=provenance_graph_export/provenance_graph_synced.ttl (after
# sync-provenance-graph) for real data.
PROVENANCE_GRAPH := linkml/examples/provenance/rdf/all_examples.ttl
GOVERNANCE_GRAPH := governance_graph_export/governance_graph.ttl
derivation-policy: provenance-example-rdf governance-graph
	python3 scripts/build_derivation_policy.py --provenance-graph $(PROVENANCE_GRAPH) --governance-graph $(GOVERNANCE_GRAPH) --derivation-rules linkml/examples/derivation_policy --out derivation_policy_export/derivation_policy.ttl

# Regression check: runs build_derivation_policy.py on the committed fixture in
# linkml/examples/derivation_policy/fixture/ and asserts its labels/reviews.
derivation-policy-check:
	python3 scripts/check_derivation_policy.py

# Contract check against sagebrain-infra's authorizer: runs its governance query
# (pinned copy in tests/infra_contract/) against the exported governance graph.
# Set SAGEBRAIN_INFRA=<infra checkout or authorize.py> to run infra's own code instead.
infra-contract-check: governance-graph
	python3 scripts/check_infra_contract.py

validate-all: shacl-validate governance-graph-validate provenance-validate derivation-policy-validate sync-provenance-check derivation-policy-check infra-contract-check owl-profile

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
