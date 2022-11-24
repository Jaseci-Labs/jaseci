from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module
import pytest


class TextSegModule(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(TextSegModule, cls).setUpClass()
        ret = load_module_actions("jaseci_ai_kit.text_seg")
        assert ret == True

    @pytest.mark.order(1)
    @jac_testcase("text_seg.jac", "test_seg_load_model")
    def test_umaps(self, ret):
        self.assertEqual(ret["report"][0], "[Model Loaded] : wiki")

    @pytest.mark.order(2)
    @jac_testcase("text_seg.jac", "test_get_segments")
    def test_get_segments(self, ret):
        self.assertEqual(len(ret["report"][0]), 2)

    @classmethod
    def tearDownClass(cls):
        super(TextSegModule, cls).tearDownClass()
        ret = unload_module("jaseci_ai_kit.modules.text_seg.text_seg")
        assert ret == True
