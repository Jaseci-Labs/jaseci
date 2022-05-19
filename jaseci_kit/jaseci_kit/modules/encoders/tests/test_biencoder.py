import sys
from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper
from ..bi import serv_actions, config_setup
from fastapi.testclient import TestClient

from .test_data import (
    model_config_default,
    train_config_default,
    test_infer_request,
    test_context_emb_request,
    test_candidate_emb_request,
    test_train_request,
    test_cos_sim_request,
)


class biencoder_test(TestCaseHelper, TestCase):
    """Unit test for BiEncoder FastAPI server"""

    def setUp(self):
        super().setUp()
        config_setup()
        self.client = TestClient(serv_actions())

    def tearDown(self) -> None:
        return super().tearDown()

    def test_cos_sim_function(self):
        response = self.client.post("/cosine_sim/", json=test_cos_sim_request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(round(response.json(), 2), 0.91)

    def test_biencoder_train(self):
        response = self.client.post("/train/", json=test_train_request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Model Training is complete.")

    def test_biencoder_infer(self):
        response = self.client.post("/infer/", json=test_infer_request)
        self.assertEqual(response.status_code, 200)

    def test_biencoder_context_emb(self):
        response = self.client.post("/get_context_emb/", json=test_context_emb_request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()[0]), 128)

    def test_candidate_embedding(self):
        response = self.client.post(
            "/get_candidate_emb/", json=test_candidate_emb_request
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()[0]), 128)

    def test_biencoder_train_config(self):
        response = self.client.post(
            "/set_train_config/",
            json={"training_parameters": train_config_default},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Config setup is complete.")
        response = self.client.post("/get_train_config/", json={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), train_config_default)

    def test_biencoder_model_config(self):
        response = self.client.post(
            "/set_model_config/", json={"model_parameters": model_config_default}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Config setup is complete.")
        response = self.client.post("/get_model_config/", json={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), model_config_default)

    def test_biencoder_load_model(self):
        response = self.client.post("/load_model/", json={"model_path": "modeloutput"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "[loaded model from] : modeloutput")

    def test_biencoder_save_model(self):
        response = self.client.post("/save_model/", json={"model_path": "modeloutput"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "[Saved model at] : modeloutput")

    def test_biencoder_combined(self):
        # step 1: getting Inference which is random
        response = self.client.post("/infer/", json=test_infer_request)
        self.assertEqual(response.status_code, 200)
        # assert response.json()[0] in test_infer_request['candidates']
        # step 2: setting training epoch to 10
        response = self.client.post(
            "/set_train_config/", json={"training_parameters": {"num_train_epochs": 10}}
        )
        self.assertEqual(response.status_code, 200)
        # step 3: training the model
        response = self.client.post("/train/", json=test_train_request)
        self.assertEqual(response.status_code, 200)
        # step 4: setting training config to default
        response = self.client.post(
            "/set_train_config/",
            json={"training_parameters": train_config_default},
        )
        self.assertEqual(response.status_code, 200)
        # step 5: saving the model
        response = self.client.post("/save_model/", json={"model_path": "my_path"})
        # step 6: infer to test if trained model is giving desired candidate
        response = self.client.post("/infer/", json=test_infer_request)
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.json()[0], "sharecurrentlocation")
        # step 7: loading the siamese model
        response = self.client.post(
            "/set_model_config/", json={"model_parameters": {"shared": True}}
        )
        self.assertEqual(response.status_code, 200)
        # step 8: validating the siamese model
        candiddate_list = self.client.post(
            "/get_candidate_emb/", json={"candidates": ["sharecurrentlocation"]}
        ).json()[0]
        context_list = self.client.post(
            "/get_context_emb/", json={"contexts": ["sharecurrentlocation"]}
        ).json()[0]
        assert candiddate_list == context_list
        # step 9: setting model config to default
        response = self.client.post(
            "/set_model_config/", json={"model_parameters": model_config_default}
        )
        self.assertEqual(response.status_code, 200)
        # step 10: loading the model
        response = self.client.post("/load_model/", json={"model_path": "my_path"})
        # step 11: test the model loaded
        response = self.client.post("/infer/", json=test_infer_request)
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.json()[0], "sharecurrentlocation")
