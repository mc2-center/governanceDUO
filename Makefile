CSV := sage-ar.model.csv

all: collate convert generate

collate:
	@echo "Collating module components..."
	head -1 model/schematic/Study.model.csv > ${CSV}
	tail -n +2 -q model/schematic/*.model.csv >> ${CSV}

convert:
	schematic schema convert ${CSV}

generate:
	schematic schema generate-jsonschema -dms ${CSV} -od .
	-rm ./*.schema.json
