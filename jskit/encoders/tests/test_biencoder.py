from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper
from bi import serv_actions, config_setup
from fastapi.testclient import TestClient
from test_data import (
    test_cos_sim_request,
    test_context_emb_request,
    test_context_emb_response,
    test_candidate_emb_request,
    test_candidate_emb_response,
    test_train_request,
    test_infer_request
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
            0.05
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
            768
        )

    def test_candidate_embedding(self):
        response = self.client.post(
            "/get_candidate_emb/",
            json=test_candidate_emb_request
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.json()),
            768
        )
