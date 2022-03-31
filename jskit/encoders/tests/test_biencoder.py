from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper
from bi import serv_actions, config_setup
from fastapi.testclient import TestClient
from .test_data import (
    test_cos_sim_request,
    test_context_emb_request,
    test_candidate_emb_request,
    test_train_request,
    test_infer_request,
    train_config_response_default,
    model_config_response_default,
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
        response = self.client.post(
            "/cosine_sim/",
            json=test_cos_sim_request
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            round(response.json(), 2),
            0.91
        )

    def test_biencoder_train(self):
        response = self.client.post(
            "/train/",
            json=test_train_request
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            "Model Training is complete."
        )

    def test_biencoder_infer(self):
        response = self.client.post(
            "/infer/",
            json=test_infer_request
        )
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(
        #     response.json(),
        #     "BookRestaurant"
        # )

    def test_biencoder_context_emb(self):
        response = self.client.post(
            "/get_context_emb/",
            json=test_context_emb_request
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.json()),
            128
        )

    def test_candidate_embedding(self):
        response = self.client.post(
            "/get_candidate_emb/",
            json=test_candidate_emb_request
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.json()[0]),
            128
        )

    def test_biencoder_get_train_config(self):
        response = self.client.post(
            "/get_train_config/",
            json={}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), train_config_response_default)

    def test_biencoder_get_model_config(self):
        response = self.client.post(
            "/get_model_config/",
            json={}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), model_config_response_default)

    def test_biencoder_set_train_config(self):
        response = self.client.post(
            "/set_train_config/",
            json={
                "training_parameters": {"seed": 12345}
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Config setup is complete.")

    def test_biencoder_set_model_config(self):
        response = self.client.post(
            "/set_model_config/",
            json={
                "model_parameters": {"shared": False}
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Config setup is complete.")

    def test_biencoder_load_model(self):
        response = self.client.post(
            "/load_model/",
            json={
                "model_path": "modeloutput"
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "[loaded model from] : modeloutput")

    def test_biencoder_save_model(self):
        response = self.client.post(
            "/save_model/",
            json={
                "model_path": "modeloutput"
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "[Saved model at] : modeloutput")
