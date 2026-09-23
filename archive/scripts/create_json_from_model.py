from synapseclient import Synapse
from synapseclient.extensions.curator import (
    bind_jsonschema,
    generate_jsonschema,
    register_jsonschema,
)
import sys

DATA_MODEL_SOURCE = "sage-ar-model/sage-ar.model.csv"
DATA_TYPE = sys.argv[1:] if len(sys.argv) > 1 else None
OUTPUT_DIRECTORY = "sage-ar-model"

syn = Synapse()
syn.login()

schemas, file_paths = generate_jsonschema(
    data_model_source=DATA_MODEL_SOURCE,
    output=OUTPUT_DIRECTORY,
    data_types=DATA_TYPE,
    synapse_client=syn,
)
