from unittest import TestCase

from fastapi.testclient import TestClient
from jaseci.utils.utils import TestCaseHelper

from extractor import serv_actions

from .test_data import (
    test_invalid_pdf_url_payload,
    test_metadata_disabled_payload,
    test_metadata_enabled_payload,
    test_valid_pdf_url_payload,
)


class pdf_ext_test(TestCaseHelper, TestCase):
    """Unit test for test text extraction from a PDF using FastAPI server"""

    def setUp(self):
        super().setUp()
        self.client = TestClient(serv_actions())

    def tearDown(self) -> None:
        return super().tearDown()

    def test_valid_pdf_url(self):
        response = self.client.post("/extract_pdf/", json=test_valid_pdf_url_payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("content", response.json().keys())

    def test_invalid_pdf_url(self):
        response = self.client.post("/extract_pdf/", json=test_invalid_pdf_url_payload)
        self.assertEqual(response.status_code, 415)
        self.assertEqual(response.json(), {"detail": "Invalid file format"})

    def test_metadata_enabled(self):
        response = self.client.post("/extract_pdf/", json=test_metadata_enabled_payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("metadata", response.json())

    def test_metadata_disabled(self):
        response = self.client.post(
            "/extract_pdf/", json=test_metadata_disabled_payload
        )
        self.assertEqual(response.status_code, 200)
        self.assertRaises(KeyError, lambda: response.json()["metadata"])
