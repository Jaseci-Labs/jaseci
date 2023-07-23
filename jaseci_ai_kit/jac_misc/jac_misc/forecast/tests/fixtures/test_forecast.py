import pytest

from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.jsorc.live_actions import load_module_actions, unload_module


class TextForecastModule(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(TextForecastModule, cls).setUpClass()
        ret = load_module_actions("jac_misc.cluster")
        assert ret == True

    @jac_testcase("forecast.jac", "test_preprocess")
    def test_preprocess(self, ret):
        self.assertEqual(ret["success"], True)

    @classmethod
    def tearDownClass(cls):
        super(TextForecastModule, cls).tearDownClass()
        ret = unload_module("jac_misc.cluster.cluster")
        assert ret == True
