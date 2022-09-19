from unittest import TestCase
import unittest
from jaseci.utils.utils import TestCaseHelper
from ..fast_enc import serv_actions
from fastapi.testclient import TestClient
from .test_data import test_train_request, test_predict_request


class FastText_test(TestCaseHelper, TestCase):
    """Unit test for FastText FastAPI server"""

    def setUp(self):
        super().setUp()
        self.client = TestClient(serv_actions())

    def tearDown(self) -> None:
        return super().tearDown()

    @unittest.skip("Issues with github action CI pipeline.")
    def test_fasttext_combined(self):
        # step 1: Training the model
        response = self.client.post("/train/", json=test_train_request)
        self.assertEqual(response.status_code, 200)
        # step 2: getting inference from the model
        response = self.client.post("/predict/", json=test_predict_request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()[(list(response.json().keys())[0])][0]["intent"], "greeting"
        )
        # step 4: Saving the model
        response = self.client.post("/save_model/", json={"model_path": "samplepath"})
        self.assertEqual(response.status_code, 200)
        # step 4: Loading the model
        response = self.client.post("/load_model/", json={"model_path": "samplepath"})
        self.assertEqual(response.status_code, 200)
        # step 5: validate the model loaded
        response = self.client.post("/predict/", json=test_predict_request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()[(list(response.json().keys())[0])][0]["intent"], "greeting"
        )
