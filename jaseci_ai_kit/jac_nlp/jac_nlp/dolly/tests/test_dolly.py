from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.jsorc.live_actions import load_module_actions, unload_module


class DollyTests(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(DollyTests, cls).setUpClass()
        ret = load_module_actions("jac_nlp.dolly")
        assert ret == True

    @jac_testcase("dolly.jac", "test_generate")
    def test_generate(self, ret):
        self.assertEqual(ret["success"], True)

    @classmethod
    def tearDownClass(cls):
        super(DollyTests, cls).tearDownClass()
        ret = unload_module("jac_nlp.dolly.dolly")
        assert ret == True
