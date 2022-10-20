from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper
from ..text_seg import serv_actions
from fastapi.testclient import TestClient
from .test_data import test_segment_request


class text_segementer_test(TestCaseHelper, TestCase):
    """Unit test for Text Segementer FastAPI server"""

    def setUp(self):
        super().setUp()
        self.client = TestClient(serv_actions())

    def tearDown(self) -> None:
        return super().tearDown()

    def test_segmentation(self):
        # getting inference from the model
        response = self.client.post("/get_segments/", json=test_segment_request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 12)

    def test_load_model(self):
        # step 4: Loading the model "wiki"/"legal"
        response = self.client.post("/seg_load_model/", json={"model_name": "wiki"})
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/seg_load_model/", json={"model_name": "legal"})
        self.assertEqual(response.status_code, 200)
