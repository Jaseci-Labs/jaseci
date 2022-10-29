from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper
from ..cl_summer import serv_actions
from fastapi.testclient import TestClient
from .test_data import test_predict_request, test_predict_request_url


class Summarization_test(TestCaseHelper, TestCase):
    """Unit test for Text Summarization FastAPI server"""

    def setUp(self):
        super().setUp()
        self.client = TestClient(serv_actions())

    def tearDown(self) -> None:
        return super().tearDown()

    def test_summarizer_text(self):
        # getting inference from the model
        response = self.client.post("/summarize/", json=test_predict_request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), test_predict_request["sent_count"])

    def test_summarizer_url(self):
        # getting inference from the model
        response = self.client.post("/summarize/", json=test_predict_request_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), test_predict_request["sent_count"])
