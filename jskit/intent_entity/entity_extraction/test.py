from fastapi.testclient import TestClient
import warnings
warnings.filterwarnings("ignore")
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Health": "Ok"}

def test_entity_detection_pass():
    response = client.post(
        "/entitydetection",
        json={
            "text":"The Humboldt University of Berlin is situated in Berlin, Germany",
            "ner_labels" : ["University", "City", "Country"]
    },
    )
    assert response.status_code == 200
    assert response.json() == {
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

def test_entity_detection_fail_ner():
    response = client.post(
        "/entitydetection",
        json={
            "text":"The Humboldt University of Berlin is situated in Berlin, Germany",
            "ner_labels" : []
    },
    )
    assert response.status_code == 400
    assert response.json() == {"Exception": "NER Labels are missing in request data"}
def test_entity_detection_fail_text():
    response = client.post(
        "/entitydetection",
        json={
            "text":"",
            "ner_labels" : ["City","Country"]
    },
    )
    assert response.status_code == 400
    assert response.json() == {"Exception": "Text data is missing in request data"}

def test_entity_training_pass():
    response = client.post(
        "/updateentitydataset",
        json={
            "text": "Who is Shaka Khan?",
            "entity": [
            {
                "entity_value": "Shaka Khan",
                "entity_name": "PERSON"
            }
            ]
        }
    )
    assert response.status_code == 200
    assert response.json() == "Model Training is started"

def test_entity_training_fail():
    response = client.post(
        "/updateentitydataset",
        json={
            "text": "",
            "entity": [
            {
                "entity_value": "Shaka Khan",
                "entity_name": "PERSON"
            }
            ]
        }
    )
    assert response.status_code == 400
    assert response.json() == "Need Data for Text and Entity"

def test_entity_training_fail2():
    response = client.post(
        "/updateentitydataset",
        json={
            "text": "Who is Shaka Khan",
            "entity": [
            {
                "entity_value": "",
                "entity_name": "PERSON"
            }
            ]
        }
    )
    assert response.status_code == 400
    assert response.json() == "Entity Data missing in request"