import json
import os


test_entity_extraction_request = {
    "text": "The Humboldt University of Berlin is situated in Berlin, Germany",
    "ner_labels": [
        "PREDEFINED"
    ]
}

test_entity_extraction_response = {
    "entities": [
        {
            "entity_text": "Humboldt University of Berlin",
            "entity_value": "ORG",
            "conf_score": 0.9708927571773529,
            "start_pos": 4,
            "end_pos": 33
        },
        {
            "entity_text": "Berlin",
            "entity_value": "LOC",
            "conf_score": 0.9977847933769226,
            "start_pos": 49,
            "end_pos": 55
        },
        {
            "entity_text": "Germany",
            "entity_value": "LOC",
            "conf_score": 0.9997479319572449,
            "start_pos": 57,
            "end_pos": 64
        }
    ]
}

test_train_config = {
  "training_parameters": {"EPOCHS": 50}
}

test_model_config = {
    "model_parameters": {
        "model_save_path": "modeloutput1"
    }
}


test_test_data = {
    "text": "what Homeowners Warranty Program means,what it applies to, \
what is its purpose?"
}

test_entities = [
  {
    "text": "homeowners warranty program",
    "entity": "Fin_Corp",
    "start": 5,
    "end": 32
  }
]

# Reading training data from json file
dirname = os.path.dirname(__file__)
fname = os.path.join(dirname, "test_train_data.json")
f = open(fname)
test_training_data = json.load(f)
f.close()
