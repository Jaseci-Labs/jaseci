import pytest
from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.jsorc.live_actions import load_module_actions, unload_module


class GenerateTextTest(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(GenerateTextTest, cls).setUpClass()
        ret = load_module_actions("jac_nlp.gen_text")
        assert ret is True

    @pytest.mark.order(1)
    @jac_testcase("gen_text.jac", "test_setup")
    def test_setup(self, ret):
        assert ret["success"] is True

    @pytest.mark.order(2)
    @jac_testcase("gen_text.jac", "test_generate_text")
    def test_generate_text(self, ret):
        assert ret["success"] is True
        assert len(ret["report"][0][0]) == 4

    @classmethod
    def tearDownClass(cls):
        super(GenerateTextTest, cls).tearDownClass()
        ret = unload_module("jac_nlp.gen_text.gen_text")
        assert ret is True
