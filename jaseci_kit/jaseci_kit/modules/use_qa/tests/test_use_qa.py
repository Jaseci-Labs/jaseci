from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper
from ..use_qa import serv_actions
from fastapi.testclient import TestClient
from .test_data import (  # noqa
    test_answer_similarity,
    test_question_similarity,
    test_text_classify,
    test_question_answer_similarity,
)


class use_qa_test(TestCaseHelper, TestCase):
    """Unit test for USE QA model FastAPI server"""

    def setUp(self):
        super().setUp()
        self.client = TestClient(serv_actions())

    def tearDown(self) -> None:
        return super().tearDown()

    def test_enc_question_similarity(self):
        response = self.client.post(
            "/question_similarity/", json=test_question_similarity
        )
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(round(response.json(), 2), 0.9)

    def test_enc_question_classify(self):
        response = self.client.post("/question_classify/", json=test_text_classify)
        self.assertEqual(response.status_code, 200)

    def test_enc_answer_similarity(self):
        response = self.client.post("/answer_similarity/", json=test_answer_similarity)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(round(response.json(), 2), 0.9)

    def test_enc_answer_classify(self):
        response = self.client.post("/answer_classify/", json=test_text_classify)
        self.assertEqual(response.status_code, 200)

    def test_enc_question(self):
        response = self.client.post(
            "/enc_question/",
            json={"question": "How old are you?"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()[0]), 512)

    def test_enc_answer(self):
        response = self.client.post(
            "/enc_answer/",
            json={"answer": "i am 30 years old"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()[0]), 512)

    def test_enc_qa_classify(self):
        response = self.client.post("/qa_classify/", json=test_text_classify)
        self.assertEqual(response.status_code, 200)

    def test_qa_similarity(self):
        response = self.client.post(
            "/qa_similarity/", json=test_question_answer_similarity
        )
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(round(response.json(), 2), 0.4)
