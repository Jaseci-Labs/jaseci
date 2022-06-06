# fmt: off
# the above line of code is to disbale black linting
# so it doesn't add a extra ',' at end of every list
# which in turns furether create issue while parsing through fast api
test_entity_detection_request = {
    "text": "The Humboldt University of Berlin is situated in Berlin, Germany",
    "ner_labels": ["PREDEFINED"]
}

test_entity_detection_valid_req = {
    "text": "what does Settlement means?",
    "ner_labels": ["Fin_Corp", "LOC", "ORG"]
}
test_entity_detection_valid = {
    "entities": [
        {
            "entity_text": "Settlement",
            "entity_value": "Fin_Corp",
            "conf_score": 0.9134525060653687,
            "start_pos": 10,
            "end_pos": 20
        }
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
        },
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
    "train_data": [
        {
            "context": "what does Settlement means?",
            "entities": [
                {
                    "entity_value": "Settlement",
                    "entity_type": "Fin_Corp",
                    "start_index": 10,
                    "end_index": 20
                }
            ]
        },
        {
            "context": "what does Home-Equity Loan means?",
            "entities": [
                {
                    "entity_value": "Home-Equity Loan",
                    "entity_type": "Fin_Corp",
                    "start_index": 10,
                    "end_index": 26
                }
            ]
        },
        {
            "context": "what does Closed-Ended Credit stands for?",
            "entities": [
                {
                    "entity_value": "Closed-Ended Credit",
                    "entity_type": "Fin_Corp",
                    "start_index": 10,
                    "end_index": 29
                }
            ]
        }
    ],
    "train_params": {"num_epoch": 2, "batch_size": 1, "LR": 0.02}
}

test_entity_training_fail = {
    "train_data": [{}],
    "train_params": {"num_epoch": 2, "batch_size": 8, "LR": 0.02}
}

test_entity_config_setup_ner = {"ner_model": "ner", "model_type": "LSTM"}

test_entity_config_setup_trf = {
    "ner_model": "prajjwal1/bert-tiny",
    "model_type": "TRFMODEL"
}

test_entity_config_setup_blank = {"ner_model": "None", "model_type": "LSTM"}
