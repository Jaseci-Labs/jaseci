from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module
import pytest

TRANSLATION = (
    "Hello, I'm Papal Christian and I'm going to tell you all the things I did."
)


class Speech2TextModule(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(Speech2TextModule, cls).setUpClass()
        ret = load_module_actions("jac_speech.stt")
        assert ret == True

    @pytest.mark.order(1)
    @jac_testcase("stt.jac", "test_audio_to_array")
    def test_audio_to_array(self, ret):
        self.assertGreater(len(ret["report"][0]), 0)

    @pytest.mark.order(2)
    @jac_testcase("stt.jac", "test_transribe_array")
    def test_transribe_array(self, ret):
        self.assertGreater(len(ret["report"][0]), 5)

    @pytest.mark.order(3)
    @jac_testcase("stt.jac", "test_transribe_file")
    def test_transribe_file(self, ret):
        self.assertGreater(len(ret["report"][0]), 5)

    @pytest.mark.order(4)
    @jac_testcase("stt.jac", "test_transribe_url")
    def test_transribe_url(self, ret):
        self.assertGreater(len(ret["report"][0]), 5)

    @pytest.mark.order(5)
    @jac_testcase("stt.jac", "test_translate")
    def test_translate(self, ret):
        self.assertIn(TRANSLATION, ret["report"][0])

    @classmethod
    def tearDownClass(cls):
        super(Speech2TextModule, cls).tearDownClass()
        ret = unload_module("jac_speech.stt.stt")
        assert ret == True
