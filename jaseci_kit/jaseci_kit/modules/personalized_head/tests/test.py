from unittest import TestCase
import unittest
from jaseci.utils.utils import TestCaseHelper
from fastapi.testclient import TestClient
import os

from ..main import serv_actions

# test variables
USER_CONFIG = os.path.join(os.path.dirname(__file__), "user_var/user_config.yaml")
USER_INPUT_IMG = os.path.join(os.path.dirname(__file__), "user_var/test_img.jpg")
EXPECTED_OUTPUT = 6
NEW_WEIGHTS = None


class ph_test(TestCaseHelper, TestCase):
    def setUp(self):
        super().setUp()
        self.client = TestClient(serv_actions())

    def tearDown(self) -> None:
        return super().tearDown()

    def test_create_head(self):
        response = self.client.post(
            "/create_head/", json={"config_file": USER_CONFIG, "uuid": "test_head"})
        self.assertEqual(response.status_code, 200)

    def test_predict(self):
        response = self.client.post("/predict/", json={"data": USER_INPUT_IMG})
        self.assertEqual(response.status_code, 200)
        print(response.json())
        self.assertEqual(response.json(), EXPECTED_OUTPUT)

    @unittest.skip("Issues with github action CI pipeline.")
    def test_train(self):
        response = self.client.post(
            "/train/", json={"config_file": USER_CONFIG})
        self.assertEqual(response.status_code, 200)

    @unittest.skip("Doesn't work without training")
    def test_load_weights(self):
        response = self.client.post(
            "/load_weights/", json={"path": NEW_WEIGHTS})
        self.assertEqual(response.status_code, 200)
