from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper
from entity_extraction import serv_actions
from fastapi.testclient import TestClient
from .test_data import (
    test_train_config,
    test_training_data,
    test_test_data,
    test_entities,
    test_model_config,
)


class entity_extraction_type2_test(TestCaseHelper, TestCase):
    """Unit test for EntityExtraction FastAPI server"""

    def setUp(self):
        super().setUp()
        self.client = TestClient(serv_actions())

    def tearDown(self) -> None:
        return super().tearDown()

    def test_Complete_model(self):
        response = self.client.post(
            "/load_model/",
            json={"model_path": "prajjwal1/bert-tiny", "local_file": False},
        )
        self.assertEqual(response.status_code, 200)

        # __________________
        response = self.client.post("/set_train_config/", json=test_train_config)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Config setup is complete.")

        # __________________
        response = self.client.post(
            "/train/",
            json={"mode": "default", "epochs": 80, "train_data": test_training_data},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "model training is completed.")

        # ________________________
        response = self.client.post("/extract_entity/", json=test_test_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["text"], test_entities[0]["text"])
        self.assertEqual(response.json()[0]["entity"], test_entities[0]["entity"])
        self.assertEqual(response.json()[0]["start"], test_entities[0]["start"])
        self.assertEqual(response.json()[0]["end"], test_entities[0]["end"])

    def test_get_train_config(self):
        response = self.client.post("/get_train_config/", json={})
        self.assertEqual(response.status_code, 200)

    def test_set_train_config(self):
        response = self.client.post("/set_train_config/", json=test_train_config)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Config setup is complete.")

    def test_get_model_config(self):
        response = self.client.post("/get_model_config/", json={})
        self.assertEqual(response.status_code, 200)

    def test_set_model_config(self):
        response = self.client.post("/set_model_config/", json=test_model_config)
        self.assertEqual(response.status_code, 200)

    def test_train(self):
        response = self.client.post(
            "/train/",
            json={"mode": "default", "epochs": 10, "train_data": test_training_data},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "model training is completed.")

        response = self.client.post("/extract_entity/", json=test_test_data)
        self.assertEqual(response.status_code, 200)
