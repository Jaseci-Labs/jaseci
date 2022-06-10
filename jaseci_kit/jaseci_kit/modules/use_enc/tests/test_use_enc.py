from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper
from ..use_enc import serv_actions
from fastapi.testclient import TestClient

from .test_data import test_text_similarity, test_text_classify  # noqa


class use_enc_test(TestCaseHelper, TestCase):
    """Unit test for USE Encoder FastAPI server"""

    def setUp(self):
        super().setUp()
        self.client = TestClient(serv_actions())

    def tearDown(self) -> None:
        return super().tearDown()

    def test_enc_text_similarity(self):
        response = self.client.post("/text_similarity/", json=test_text_similarity)
        self.assertEqual(response.status_code, 200)

    def test_enc_text_classify(self):
        response = self.client.post("/text_classify/", json=test_text_classify)
        self.assertEqual(response.status_code, 200)

    def test_enc_get_embeddings(self):
        response = self.client.post(
            "/get_embedding/", json={"text": "Share my location with Hillary's sister"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()[0]), 512)
