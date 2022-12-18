import pytest

from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module


class TestTTSModule(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(TestTTSModule, cls).setUpClass()
        ret = load_module_actions("jaseci_ai_kit.tts")
        assert ret == True

    @pytest.mark.order(1)
    @jac_testcase("tts.jac", "test_synthesize")
    def test_synthesize(self, ret):
        print(len(ret["report"][0]["audio_wave"]))
        self.assertEqual(ret["success"], True)
        self.assertIsInstance(ret["report"][0]["audio_wave"], list)

    @pytest.mark.order(2)
    @jac_testcase("tts.jac", "test_save_audio")
    def test_save_audio(self, ret):
        self.assertEqual(ret["success"], True)
        self.assertEqual(ret["report"][0]["save_status"], True)

    @classmethod
    def tearDownClass(cls):
        super(TestTTSModule, cls).tearDownClass()
        ret = unload_module("jaseci_ai_kit.modules.tts.tts")
        assert ret == True
