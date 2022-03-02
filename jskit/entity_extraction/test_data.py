test_entity_detection_request = {
    "text": "The Humboldt University of Berlin is situated in Berlin, Germany",
    "ner_labels": ["University", "City", "Country"]
}

test_entity_detection_response = {
    "input_text": "The Humboldt University of Berlin is situated in Berlin, Germany",
    "entities": [
        {
            "entity_text": "Humboldt University of Berlin",
            "entity_value": "University",
            "conf_score": 0.9999905824661255
        },
        {
            "entity_text": "Berlin",
            "entity_value": "City",
            "conf_score": 0.9999960660934448
        },
        {
            "entity_text": "Germany",
            "entity_value": "Country",
            "conf_score": 0.999994158744812
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
    "text": "Who is Shaka Khan?",
    "entity": [
        {
            "entity_value": "Shaka Khan",
            "entity_name": "PERSON"
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
