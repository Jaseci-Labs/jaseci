test_entity_detection_request = {
    "text": "The Humboldt University of Berlin is situated in Berlin, Germany",
    "ner_labels": [
        "PREDEFINED"
    ]
}

test_entity_detection_response = {
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

test_entity_detection_request_fail_ner = {
    "text": "The Humboldt University of Berlin is situated in Berlin, Germany",
    "ner_labels": []
}

test_entity_detection_request_fail_text = {
    "text": "",
    "ner_labels": ["City", "Country"]
}


test_entity_training_pass = {
    "text": "The Humboldt University of Berlin is situated in Berlin, Germany",
    "entity": [
        {
            "entity_value": "Humboldt University of Berlin",
            "entity_name": "University",
            "start_index": 4,
            "end_index": 34
        },
        {
            "entity_value": "Berlin",
            "entity_name": "City",
            "start_index": 49,
            "end_index": 55
        },
        {
            "entity_value": "Germany",
            "entity_name": "Country",
            "start_index": 58,
            "end_index": 67

        }
    ]
}
test_entity_training_fail = {
    "text": "",
    "entity": [
        {
            "entity_value": "Shaka Khan",
            "entity_name": "PERSON"
        }
    ]
}
test_entity_training_fail2 = {
    "text": "Who is Shaka Khan",
    "entity": [
        {
            "entity_value": "",
            "entity_name": "PERSON"
        }
    ]
}

test_entity_config_setup_ner = {
    "ner_model": "ner",
    "model_type": "LSTM"
}

test_entity_config_setup_trf = {
    "ner_model": "distilbert-base-uncased",
    "model_type": "TRFMODEL"
}

test_entity_config_setup_blank = {
    "ner_model": "None",
    "model_type": "LSTM"
}
