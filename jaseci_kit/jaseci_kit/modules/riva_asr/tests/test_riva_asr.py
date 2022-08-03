from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper
from ..riva_asr import serv_actions
from fastapi.testclient import TestClient
import base64
from scipy.io import wavfile


class FastText_test(TestCaseHelper, TestCase):
    """Unit test for FastText FastAPI server"""

    def setUp(self):
        super().setUp()
        self.client = TestClient(serv_actions())

    def tearDown(self) -> None:
        return super().tearDown()

    def test_STT(self):
        samplerate, data = wavfile.read("audio_req_file.wav")
        enc_data = base64.b64encode(data).decode()
        config_data = {"audio_data": enc_data, "frame_rate": samplerate}
        resp = self.client.post("/get_stt/", json=config_data)
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.json())

    def test_TTS(self):

        config_data = {
            "text": "This is a Sample text to test text to speech capability"
        }
        resp = self.client.post("/get_tts/", json=config_data)
        audio_enc_data = base64.b64decode(resp.json()["audio_data"])
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(audio_enc_data)
