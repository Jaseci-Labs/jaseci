from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.jsorc.live_actions import load_module_actions, unload_module
import pytest


class Speech2TextModule(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(Speech2TextModule, cls).setUpClass()
        ret = load_module_actions("jac_speech.stt")
        assert ret == True

    @pytest.mark.order(3)
    @jac_testcase("stt.jac", "test_transcribe_file")
    def test_transcribe_file(self, ret):
        self.assertGreater(len(ret["report"][0]["text"]), 5)

    @pytest.mark.order(4)
    @jac_testcase("stt.jac", "test_transcribe_url")
    def test_transcribe_url(self, ret):
        self.assertGreater(len(ret["report"][0]["text"]), 5)

    @pytest.mark.order(5)
    @jac_testcase("stt.jac", "test_translate")
    def test_translate(self, ret):
        self.assertGreater(len(ret["report"][0]["text"]), 5)

    @classmethod
    def tearDownClass(cls):
        super(Speech2TextModule, cls).tearDownClass()
        ret = unload_module("jac_speech.stt.stt")
        assert ret == True
