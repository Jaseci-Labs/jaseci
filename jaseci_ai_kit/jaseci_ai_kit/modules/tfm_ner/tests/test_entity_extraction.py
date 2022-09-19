from unittest import TestCase
import unittest
from jaseci.utils.utils import TestCaseHelper
from ..tfm_ner import serv_actions
from fastapi.testclient import TestClient
from .test_data import (
    test_train_config,
    test_training_data,
    test_model_config,
    test_predict_input,
    test_predict_output,
)


class tfm_ner_test(TestCaseHelper, TestCase):
    """Unit test for EntityExtraction FastAPI server"""

    def setUp(self):
        super().setUp()
        self.client = TestClient(serv_actions())

    def tearDown(self) -> None:
        return super().tearDown()

    @unittest.skip("Issues with github action CI pipeline.")
    def test_complete_model(self):
        response = self.client.post(
            "/train/",
            json={"mode": "default", "epochs": 40, "train_data": test_training_data},
        )
        self.assertEqual(response.status_code, 200)

        # ________________________
        response = self.client.post("/extract_entity/", json=test_predict_input)
        self.assertEqual(response.status_code, 200)
        for idx, ent in enumerate(test_predict_output):
            ent.pop("conf_score")
            res_ent = response.json()[idx]
            res_ent.pop("conf_score")
            self.assertEqual(res_ent, ent)
        # ________________________
        response = self.client.post("/save_model/", json={"model_path": "mymodel"})
        self.assertEqual(response.status_code, 200)
        # ________________________
        response = self.client.post("/load_model/", json={"model_path": "mymodel"})
        self.assertEqual(response.status_code, 200)
        # ________________________
        response = self.client.post("/extract_entity/", json=test_predict_input)
        self.assertEqual(response.status_code, 200)
        print(response.json())
        for idx, ent in enumerate(test_predict_output):
            res_ent = response.json()[idx]
            res_ent.pop("conf_score")
            self.assertEqual(res_ent, ent)

    @unittest.skip("Doesn't work without training")
    def test_extract_entity(self):
        response = self.client.post("/extract_entity/", json=test_predict_input)
        self.assertEqual(response.status_code, 200)
        for idx, ent in enumerate(test_predict_output):
            ent.pop("conf_score")
            res_ent = response.json()[idx]
            res_ent.pop("conf_score")
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

    @unittest.skip("Issues with github action CI pipeline.")
    def test_train(self):
        # fmt: off
        response = self.client.post(
            "/train/",
            json={"mode": "default", "epochs": 20, "train_data": test_training_data}
        )
        # fmt: on
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "model training is completed.")

        response = self.client.post("/extract_entity/", json=test_predict_input)
        self.assertEqual(response.status_code, 200)
