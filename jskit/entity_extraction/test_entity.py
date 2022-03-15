from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper
from entity_extraction import serv_actions
from fastapi.testclient import TestClient
from test_data import (
    test_entity_detection_request,
    test_entity_detection_response,
    test_entity_detection_request_fail_ner,
    test_entity_detection_request_fail_text,
    test_entity_training_pass,
    test_entity_training_fail,
    test_entity_training_fail2
)


class entity_extraction_test(TestCaseHelper, TestCase):
    """Unit test for EntityExtraction FastAPI server"""

    def setUp(self):
        super().setUp()
        self.client = TestClient(serv_actions())

    def tearDown(self) -> None:
        return super().tearDown()

    def test_entity_detection_pass(self):
        response = self.client.post(
            "/entity_detection/",
            json=test_entity_detection_request
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            test_entity_detection_response
        )

    def test_entity_detection_fail_ner(self):
        response = self.client.post(
            "/entity_detection/",
            json=test_entity_detection_request_fail_ner,
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {'detail': 'NER Labels are missing in request data'}
        )

    def test_entity_detection_fail_text(self):
        response = self.client.post(
            "/entity_detection/",
            json=test_entity_detection_request_fail_text,
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {'detail': 'Text data is missing in request data'}
        )

    def test_entity_training_pass(self):
        response = self.client.post(
            "/train/",
            json=test_entity_training_pass
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            "Model Training is started"
        )

    def test_entity_training_fail(self):
        response = self.client.post(
            "/train/",
            json=test_entity_training_fail)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {'detail': 'Need Data for Text and Entity'}
        )

    def test_entity_training_fail2(self):
        response = self.client.post(
            "/train/",
            json=test_entity_training_fail2)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {'detail': 'Entity Data missing in request'}
        )
