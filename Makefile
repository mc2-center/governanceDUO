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

# --ignore-warnings: this schema deliberately keeps the schematic CSV's camelCase
# attribute names (e.g. dataUseModifiers, StudyKey) instead of linkml-lint's preferred
# snake_case, since those names are also live Synapse annotation keys.
linkml-lint:
	linkml-lint --ignore-warnings ${LINKML_SCHEMA}

owl:
	python3 scripts/build_owl.py --schema ${LINKML_SCHEMA} --out shapes/governance_duo.owl.ttl

shacl:
	gen-shacl ${LINKML_SCHEMA} > shapes/governance_duo.shacl.ttl

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

validate-all: shacl-validate governance-graph-validate

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
