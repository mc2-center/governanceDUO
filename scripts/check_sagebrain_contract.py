"""
check_sagebrain_contract.py

Opt-in check that this repo's governance layer works as a layer of sagebrain-model's
graph (make sagebrain-contract-check SAGEBRAIN_MODEL=<path>). Needs a sagebrain-model
checkout, so it isn't part of validate-all; sagebrain-model runs the equivalent check
from its side. Four parts, each reported separately:

1. OWL 2 DL on the union of sagebrain-model's ontology (ontology/main, its
   ontology/imports except the vendored external vocabularies prov.ttl/duo.ttl --
   the same set its own tests/validate.py DL check merges -- plus its
   ontology/governance modules) and this repo's shapes/governance_duo.owl.ttl +
   shapes/governance_graph.owl.ttl. Merged to a file, then validated: chaining
   `robot merge ... validate-profile` in one call reports spurious violations.
2. Every prov: term this repo's two TBoxes declare has the type sagebrain-model's
   vendored ontology/imports/prov.ttl gives it (check_prov_alignment.py) -- the
   one conflict with prov.ttl that leaving it out of (1)'s union would hide.
3. SHACL on one joined worked example -- sagebrain-model's examples/AD-cohort.ttl and
   examples/pipeline_provenance.ttl, this repo's exported governance graph and
   provenance examples, and tests/sagebrain_contract/governance_binding.ttl --
   against both repos' shapes (sagebrain-model's ontology/shacl/*.ttl, this repo's
   shapes/governance_graph.shacl.ttl and shapes/provenance_layer.shacl.ttl), with
   inference off. The ont_graph is sagebrain-model's ontology plus
   shapes/governance_graph.owl.ttl -- the TBox describing the graph ABox, the same
   one make governance-graph-validate uses. shapes/governance_duo.owl.ttl
   describes LinkML records, not this graph, and mixing its ~5,000 triples into
   the data graph makes pyshacl take tens of minutes.
4. scripts/build_derivation_policy.py over that joined example, asserting
   association:apoe-expr-samp01 (sagebrain:derived_from the pipeline's output)
   receives a ControlLabel citing gov:AR-42 -- which requires sagebrain-model to
   declare sagebrain:derived_from rdfs:subPropertyOf prov:wasDerivedFrom.

Usage:
    python scripts/check_sagebrain_contract.py --sagebrain-model PATH [--robot-jar PATH]

author: orion.banks
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from pyshacl import validate
from rdflib import Graph
from rdflib.namespace import SH

from check_prov_alignment import type_mismatches

GOVERNANCE_TBOXES = ["shapes/governance_duo.owl.ttl", "shapes/governance_graph.owl.ttl"]
GOVERNANCE_SHAPES = ["shapes/governance_graph.shacl.ttl", "shapes/provenance_layer.shacl.ttl"]
GOVERNANCE_DATA = [
    "governance_graph_export/governance_graph.ttl",
    "linkml/examples/provenance/rdf/all_examples.ttl",
    "tests/sagebrain_contract/governance_binding.ttl",
]
SAGEBRAIN_EXAMPLES = ["examples/AD-cohort.ttl", "examples/pipeline_provenance.ttl"]

LABEL_QUERY = """
PREFIX sagegov: <https://sagebionetworks.org/governance/>
PREFIX association: <https://w3id.org/synapse/ad/association/>
ASK {
    ?label a sagegov:ControlLabel ;
           sagegov:subject association:apoe-expr-samp01 ;
           sagegov:sourceAccessRequirements sagegov:AR-42 .
}
"""


# Vendored external vocabularies sagebrain-model imports but doesn't DL-check
# itself (they carry their own profile issues, e.g. puns inside prov.ttl). Leaving
# prov.ttl out of the union would also hide the one conflict this repo can cause
# with it -- declaring a prov: term with a different type than PROV-O -- so that is
# checked separately, against the same prov.ttl, by check_prov_alignment().
EXTERNAL_VOCABULARIES = {"prov.ttl", "duo.ttl"}


def sagebrain_ontology_sources(root: Path) -> list[Path]:
    return sorted(
        p for folder in ("ontology/main", "ontology/imports", "ontology/governance")
        for p in (root / folder).glob("*.ttl")
        if p.name not in EXTERNAL_VOCABULARIES
    )


def check_dl(sources: list[Path], robot_jar: str, tmp: Path) -> list[str]:
    merged = tmp / "union.ttl"
    command = ["java", "-jar", robot_jar, "merge"]
    for source in sources:
        command += ["--input", str(source)]
    merge = subprocess.run([*command, "--output", str(merged)], capture_output=True, text=True)
    if merge.returncode != 0:
        return [f"robot merge failed: {merge.stderr.strip()[-400:]}"]
    report = tmp / "dl_report.txt"
    result = subprocess.run(
        ["java", "-jar", robot_jar, "validate-profile", "--profile", "DL", "--input", str(merged), "--output", str(report)],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        return []
    lines = report.read_text().splitlines() if report.exists() else [result.stderr]
    violations = [line[:240] for line in lines[1:]]
    return [f"union is not OWL 2 DL ({len(violations)} violations), first: {v}" for v in violations[:5]]


def check_prov_alignment(root: Path) -> list[str]:
    return type_mismatches(GOVERNANCE_TBOXES, Graph().parse(root / "ontology/imports/prov.ttl"))


def check_shacl(root: Path, ontology: Graph) -> list[str]:
    data = Graph()
    for path in [*(root / p for p in SAGEBRAIN_EXAMPLES), *map(Path, GOVERNANCE_DATA)]:
        data.parse(path)
    shapes = Graph()
    for path in [*sorted((root / "ontology/shacl").glob("*.ttl")), *map(Path, GOVERNANCE_SHAPES)]:
        shapes.parse(path)
    conforms, results, _ = validate(data, shacl_graph=shapes, ont_graph=ontology, inference="none")
    if conforms:
        return []
    messages = sorted({str(m) for m in results.objects(None, SH.resultMessage)})
    return [f"joined example does not conform: {m}" for m in messages]


def check_derivation(root: Path, tmp: Path) -> list[str]:
    governance = Graph()
    for path in ["governance_graph_export/governance_graph.ttl", "tests/sagebrain_contract/governance_binding.ttl"]:
        governance.parse(path)
    governance_path = tmp / "governance.ttl"
    governance.serialize(governance_path, format="turtle")
    out = tmp / "derivation_policy.ttl"
    command = [
        sys.executable, "scripts/build_derivation_policy.py",
        "--provenance-graph", "linkml/examples/provenance/rdf/all_examples.ttl",
        "--governance-graph", str(governance_path),
        "--out", str(out),
    ]
    for path in [*(root / p for p in SAGEBRAIN_EXAMPLES), *sorted((root / "ontology/governance").glob("*.ttl"))]:
        command += ["--extra-graph", str(path)]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        return [f"build_derivation_policy.py failed: {result.stderr.strip()[-400:]}"]
    if not Graph().parse(out).query(LABEL_QUERY).askAnswer:
        return [
            "association:apoe-expr-samp01 received no ControlLabel citing gov:AR-42 "
            "(is sagebrain:derived_from declared rdfs:subPropertyOf prov:wasDerivedFrom?)"
        ]
    return []


def main():
    parser = argparse.ArgumentParser(description="governanceDUO <-> sagebrain-model layer contract check.")
    parser.add_argument("--sagebrain-model", required=True)
    parser.add_argument("--robot-jar", default="tools/robot.jar")
    args = parser.parse_args()

    root = Path(args.sagebrain_model).expanduser()
    if not (root / "ontology").is_dir():
        sys.exit(f"{root} does not look like a sagebrain-model checkout (no ontology/ folder).")
    sources = sagebrain_ontology_sources(root)
    ontology = Graph()
    for path in [*sources, Path("shapes/governance_graph.owl.ttl")]:
        ontology.parse(path)

    results = {}
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp = Path(tmp_dir)
        results["OWL 2 DL (union)"] = check_dl([*sources, *map(Path, GOVERNANCE_TBOXES)], args.robot_jar, tmp)
        results["prov: types match sagebrain's prov.ttl"] = check_prov_alignment(root)
        results["SHACL (joined worked example)"] = check_shacl(root, ontology)
        results["ControlLabel reaches sagebrain Association"] = check_derivation(root, tmp)

    failed = False
    for name, failures in results.items():
        if failures:
            failed = True
            print(f"FAIL  {name}")
            for failure in failures:
                print(f"        - {failure}")
        else:
            print(f"pass  {name}")
    if failed:
        sys.exit(1)
    print(f"sagebrain contract check passed against {root}.")


if __name__ == "__main__":
    main()
