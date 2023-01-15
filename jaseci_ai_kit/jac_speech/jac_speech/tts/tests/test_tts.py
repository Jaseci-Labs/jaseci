import pytest

from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module


class TestTTSModule(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(TestTTSModule, cls).setUpClass()
        ret = load_module_actions("jac_speech.tts")
        assert ret == True

    @pytest.mark.order(1)
    @jac_testcase("tts.jac", "test_synthesize")
    def test_synthesize(self, ret):
        self.assertEqual(ret["success"], True)
        self.assertIsInstance(ret["report"][0]["audio_wave"], list)

    @pytest.mark.order(2)
    @jac_testcase("tts.jac", "test_load_vocorder_v1")
    def test_load_vocorder_v1(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(3)
    @jac_testcase("tts.jac", "test_load_seq2seq_model_v1")
    def test_load_seq2seq_model_v1(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(4)
    @jac_testcase("tts.jac", "test_save_audio")
    def test_save_audio(self, ret):
        self.assertEqual(ret["success"], True)
        self.assertEqual(ret["report"][0]["save_status"], True)

    @pytest.mark.order(5)
    @jac_testcase("tts.jac", "test_load_vocorder_v2")
    def test_load_vocorder_v2(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(6)
    @jac_testcase("tts.jac", "test_load_seq2seq_model_v2")
    def test_load_seq2seq_model_v2(self, ret):
        self.assertEqual(ret["success"], True)

    @classmethod
    def tearDownClass(cls):
        super(TestTTSModule, cls).tearDownClass()
        ret = unload_module("jac_speech.tts.tts")
        assert ret == True
