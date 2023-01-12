from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module


class TranslatorModule(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(TranslatorModule, cls).setUpClass()
        ret = load_module_actions("jac_misc.translator")
        assert ret == True

    @jac_testcase("translator.jac", "test_translate_sinhala_eng")
    def test_translate_sinhala_eng(self, ret):
        self.assertGreater(len(ret["report"][0][0]), 1)

    @jac_testcase("translator.jac", "test_translate_eng_german")
    def test_translate_eng_german(self, ret):
        self.assertGreater(len(ret["report"][0][0]), 1)

    @classmethod
    def tearDownClass(cls):
        super(TranslatorModule, cls).tearDownClass()
        ret = unload_module("jac_misc.translator.translator")
        assert ret == True
