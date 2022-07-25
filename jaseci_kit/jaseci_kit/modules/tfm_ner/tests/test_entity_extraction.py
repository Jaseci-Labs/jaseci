from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper
from ..tfm_ner import serv_actions
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

    def test_complete_model(self):
        # fmt: off
        # the above line of code is to disbale black linting
        # so it doesn't add a extra ',' at end of every list
        # which in turns furether create issue while parsing through fast api
        response = self.client.post(
            "/load_model/",
            json={"model_path": "prajjwal1/bert-tiny", "local_file": False}
        )
        # fmt: on
        # black linting is switched on at above line
        self.assertEqual(response.status_code, 200)

        # __________________
        response = self.client.post("/set_train_config/", json=test_train_config)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Config setup is complete.")

        # __________________
        response = self.client.post(
            "/train/",
            json={"mode": "default", "epochs": 60, "train_data": test_training_data},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "model training is completed.")

        # ________________________
        response = self.client.post("/extract_entity/", json=test_test_data)
        self.assertEqual(response.status_code, 200)
        for idx, ent in enumerate(test_entities):
            ent.pop("score")
            res_ent = response.json()[idx]
            res_ent.pop("score")
            self.assertEqual(res_ent, ent)

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
        # fmt: off
        response = self.client.post(
            "/train/",
            json={"mode": "default", "epochs": 2, "train_data": test_training_data}
        )
        # fmt: on
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "model training is completed.")

        response = self.client.post("/extract_entity/", json=test_test_data)
        self.assertEqual(response.status_code, 200)
