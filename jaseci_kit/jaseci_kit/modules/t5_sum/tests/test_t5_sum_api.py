from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper
from t5_sum import serv_actions
from fastapi.testclient import TestClient
from .test_data import test_t5_sum_request


class t5_sum_test_api(TestCaseHelper, TestCase):
    def setUp(self):
        super().setUp()
        self.client = TestClient(serv_actions())

    def tearDown(self) -> None:
        return super().tearDown()

    def test_t5_sum_detection_pass(self):
        response = self.client.post("/t5_sum/", json=test_t5_sum_request)

        self.assertEqual(response.status_code, 200)
