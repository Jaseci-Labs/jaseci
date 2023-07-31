import pytest

from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.jsorc.live_actions import load_module_actions, unload_module


class TextForecastModule(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(TextForecastModule, cls).setUpClass()
        ret = load_module_actions("jac_misc.forecast")
        assert ret == True

    @jac_testcase("forecast.jac", "test_preprocess")
    def test_preprocess(self, ret):
        self.assertEqual(ret["success"], True)

    @jac_testcase("forecast.jac", "test_split")
    def test_split(self, ret):
        self.assertEqual(ret["success"], True)

    @jac_testcase("forecast.jac", "test_scale")
    def test_scale(self, ret):
        self.assertEqual(ret["success"], True)

    @jac_testcase("forecast.jac", "test_create_model")
    def test_create_model(self, ret):
        self.assertEqual(ret["success"], True)

    @jac_testcase("forecast.jac", "test_train")
    def test_train(self, ret):
        self.assertEqual(ret["success"], True)

    @jac_testcase("forecast.jac", "test_evaluate")
    def test_evaluate(self, ret):
        self.assertEqual(ret["success"], True)
        self.assertIsInstance(ret["report"][0], float)

    @jac_testcase("forecast.jac", "test_predict")
    def test_predict(self, ret):
        self.assertEqual(ret["success"], True)
        self.assertEqual(len(ret["report"][0]), 2)

    @classmethod
    def tearDownClass(cls):
        super(TextForecastModule, cls).tearDownClass()
        ret = unload_module("jac_misc.forecast.forecast")
        assert ret == True
