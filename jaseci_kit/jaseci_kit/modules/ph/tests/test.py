from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper
from fastapi.testclient import TestClient
import pytest
import os

from ..main import serv_actions

# test variables
USER_CONFIG = os.path.join(os.path.dirname(
    __file__), "config.yaml")
USER_INPUT = "Where is the nearest coffee shop?"
EXPECTED_OUTPUT = 2
TRAINED_EXPECTED_OUTPUT = 4
NEW_WEIGHTS = os.path.join(os.path.dirname(
    __file__), "saved_models/models/PersonalizedHeadTrainer/test_head/model_best.pth")


class ph_test(TestCaseHelper, TestCase):
    def setUp(self):
        super().setUp()
        self.client = TestClient(serv_actions())

    def tearDown(self) -> None:
        return super().tearDown()

    @pytest.mark.order(1)
    def test_create_head_list(self):
        response = self.client.post(
            "/create_head_list/", json={"config_file": USER_CONFIG})
        self.assertEqual(response.status_code, 200)

    @pytest.mark.order(2)
    def test_create_head(self):
        response = self.client.post(
            "/create_head/", json={"uuid": "test_head"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "test_head")

    @pytest.mark.order(3)
    def test_predict(self):
        response = self.client.post(
            "/predict/", json={"uuid": "test_head", "data": USER_INPUT})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), EXPECTED_OUTPUT)

    @pytest.mark.order(4)
    def test_train(self):
        response = self.client.post(
            "/train_head/", json={"config_file": USER_CONFIG, "uuid": "test_head"})
        self.assertEqual(response.status_code, 200)

    @pytest.mark.order(5)
    def test_load_weights(self):
        response = self.client.post(
            "/load_weights/", json={"uuid": "test_head", "path": NEW_WEIGHTS})
        self.assertEqual(response.status_code, 200)

    @pytest.mark.order(6)
    def test_predict_trained(self):
        response = self.client.post(
            "/predict/", json={"uuid": "test_head", "data": USER_INPUT})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), TRAINED_EXPECTED_OUTPUT)
