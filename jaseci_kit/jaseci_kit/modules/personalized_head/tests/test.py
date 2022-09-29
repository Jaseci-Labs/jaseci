from distutils.command.config import config
from unittest import TestCase
import unittest
from jaseci.utils.utils import TestCaseHelper
from fastapi.testclient import TestClient
import pytest
import os

from ..main import serv_actions

# test variables
USER_CONFIG = os.path.join(os.path.dirname(
    __file__), "user_var/user_config.yaml")
USER_INPUT_IMG = os.path.join(
    os.path.dirname(__file__), "user_var/test_img.jpg")
EXPECTED_OUTPUT = 6
NEW_WEIGHTS = None


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
            "/predict/", json={"uuid": "test_head", "data": USER_INPUT_IMG})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), EXPECTED_OUTPUT)

    @unittest.skip("Issues with github action CI pipeline.")
    def test_train(self):
        response = self.client.post(
            "/train/", json={"config_file": USER_CONFIG})
        self.assertEqual(response.status_code, 200)

    @unittest.skip("Doesn't work without training")
    def test_load_weights(self):
        response = self.client.post(
            "/load_weights/", json={"uuid": "test_head", "path": NEW_WEIGHTS})
        self.assertEqual(response.status_code, 200)
