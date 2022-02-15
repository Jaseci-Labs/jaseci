from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper
from bi import app
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
        self.client = TestClient(app)

    def tearDown(self) -> None:
        return super().tearDown()

    def test_cos_sim_function(self):
        response = self.client.post(
            "/cos_sim_score",
            test_cos_sim_request
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"cos_score": 0.49492838978767395}
        )

    def test_biencoder_train(self):
        response = self.client.post(
            "/train",
            json=test_train_request
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            "Model Training is comnpleted"
        )

    def test_biencoder_infer(self):
        response = self.client.post(
            "/infer",
            json=test_infer_request
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"label": "BookRestaurant"}
        )

    def test_biencoder_context_emb(self):
        response = self.client.get(
            "/getcontextemb",
            json=test_context_emb_request
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            test_context_emb_response
        )

    def test_candidate_embedding(self):
        response = self.client.get(
            "/getcandidateemb",
            json=test_candidate_emb_request
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            test_candidate_emb_response
        )
