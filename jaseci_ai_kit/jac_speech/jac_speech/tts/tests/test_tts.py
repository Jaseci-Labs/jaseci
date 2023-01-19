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
    @jac_testcase("tts.jac", "test_synthesize_female")
    def test_synthesize_female(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(2)
    @jac_testcase("tts.jac", "test_synthesize_male")
    def test_synthesize_male(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(3)
    @jac_testcase("tts.jac", "test_clone_voice")
    def test_clone_voice(self, ret):
        self.assertEqual(ret["success"], True)

    @classmethod
    def tearDownClass(cls):
        super(TestTTSModule, cls).tearDownClass()
        ret = unload_module("jac_speech.tts.tts")
        assert ret == True
