CSV := sage-ar.model.csv
CONFIG := ar_config.yml
DATA := AccessRequirement Resource Schema Study

all: collate convert generate-json build-csv

build-csv:
	$(foreach d,$(DATA), schematic manifest -c ${CONFIG} get -dt $(d);)
	rm *.schema.json

collate:
	@echo "Collating module components..."
	head -1 model/schematic/Study.model.csv > ${CSV}
	tail -n +2 -q model/schematic/*.model.csv >> ${CSV}

convert:
	schematic schema convert ${CSV}

generate-json:
	schematic schema generate-jsonschema -dms ${CSV} -od .
	$(foreach d,$(DATA), python scripts/update_json_conditions.py ./sage-ar.model/$(d)_validation_schema.json;)

