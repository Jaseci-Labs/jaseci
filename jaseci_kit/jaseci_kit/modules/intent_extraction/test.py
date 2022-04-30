from main import serv_actions
from fastapi.testclient import TestClient
import warnings

warnings.filterwarnings("ignore")

client = TestClient(serv_actions())


def test_health():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Health": "Ok"}


def test_intent_classification_pass():
    response = client.post(
        "/intentclassification",
        json={
            "text": "Let's go and play basketball",
            "labels": ["News", "Clothes", "information", "Sports", "Politics"],
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "input_text": "Let's go and play basketball",
        "intents": [{"intent": "Sports", "conf_score": 0.6810781359672546}],
    }


def test_intent_classification_fail_intent():
    response = client.post(
        "/intentclassification",
        json={"text": "Let's go and play basketball", "labels": []},
    )
    assert response.status_code == 400
    assert response.json() == {"Exception": "Intents are missing in request data"}


def test_intent_classification_fail_text():
    response = client.post(
        "/intentclassification",
        json={"text": "", "labels": ["Sports", "News"]},
    )
    assert response.status_code == 400
    assert response.json() == {"Exception": "Text data is missing in request data"}


def test_intent_training_pass():
    response = client.post(
        "/updateintentdataset",
        json={
            "text": "Criminals Get Nine Months in Violin Case",
            "label": "News",
            "topic": "Infomation",
        },
    )
    assert response.status_code == 200
    assert response.json() == "Model Training is started"


def test_intent_training_fail1():
    response = client.post(
        "/updateintentdataset",
        json={
            "text": "Criminals Get Nine Months in Violin Case",
            "label": "",
            "topic": "Infomation",
        },
    )
    assert response.status_code == 400
    assert response.json() == "Need Data for Text and Label"


def test_intent_training_fail2():
    response = client.post(
        "/updateintentdataset", json={"text": "", "label": "", "topic": "Infomation"}
    )
    assert response.status_code == 400
    assert response.json() == "Need Data for Text and Label"
