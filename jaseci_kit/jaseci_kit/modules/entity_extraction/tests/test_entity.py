from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper
from entity_extraction import serv_actions
from fastapi.testclient import TestClient
from .test_data import (
    test_entity_detection_request,
    test_entity_detection_response,
    test_entity_detection_request_fail_ner,
    test_entity_detection_request_fail_text,
    test_entity_training_pass,
    test_entity_training_fail,
    test_entity_config_setup_blank,
    test_entity_config_setup_trf,
    test_entity_config_setup_ner,
    test_entity_detection_valid,
    test_entity_detection_valid_req,
)


class entity_extraction_test(TestCaseHelper, TestCase):
    """Unit test for EntityExtraction FastAPI server"""

    def setUp(self):
        super().setUp()
        self.client = TestClient(serv_actions())

    def tearDown(self) -> None:
        return super().tearDown()

    def test_entity_detection_pass(self):
        response = self.client.post(
            "/entity_detection/", json=test_entity_detection_request
        )
        self.assertEqual(response.status_code, 200)
        for idx, ent in enumerate(test_entity_detection_response["entities"]):
            ent.pop("conf_score")
            res_ent = response.json()["entities"][idx]
            res_ent.pop("conf_score")
            self.assertEqual(res_ent, ent)

    def test_entity_detection_fail_ner(self):
        response = self.client.post(
            "/entity_detection/",
            json=test_entity_detection_request_fail_ner,
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(), {"detail": "NER Labels are missing in request data"}
        )

    def test_entity_detection_fail_text(self):
        response = self.client.post(
            "/entity_detection/",
            json=test_entity_detection_request_fail_text,
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(), {"detail": "Text data is missing in request data"}
        )

    def test_entity_training_pass(self):
        response = self.client.post("/train/", json=test_entity_training_pass)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Model Training is Completed")

    def test_entity_training_fail(self):
        response = self.client.post("/train/", json=test_entity_training_fail)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Need Data for Text and Entity"})

    def test_entity_config_setup1(self):
        response = self.client.post("/set_config/", json=test_entity_config_setup_ner)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Config setup is complete.")

    def test_entity_config_setup2(self):
        response = self.client.post("/set_config/", json=test_entity_config_setup_trf)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Config setup is complete.")
        response = self.client.post("/set_config/", json=test_entity_config_setup_ner)
        self.assertEqual(response.status_code, 200)

    def test_entity_config_setup3(self):
        response = self.client.post("/set_config/", json=test_entity_config_setup_blank)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Config setup is complete.")
        response = self.client.post("/set_config/", json=test_entity_config_setup_ner)
        self.assertEqual(response.status_code, 200)

    def test_entity_training_validate(self):
        response = self.client.post("/set_config/", json=test_entity_config_setup_trf)
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/train/", json=test_entity_training_pass)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            "/entity_detection/", json=test_entity_detection_valid_req
        )
        self.assertEqual(response.status_code, 200)
        for idx, ent in enumerate(test_entity_detection_valid["entities"]):
            ent.pop("conf_score")
            res_ent = response.json()["entities"][idx]
            res_ent.pop("conf_score")
            self.assertEqual(res_ent, ent)
