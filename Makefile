CSV := sage-ar.model.csv
CONFIG := ar_config.yml
DATA := AccessRequirement Resource Study

all: collate convert generate-json build-csv

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
