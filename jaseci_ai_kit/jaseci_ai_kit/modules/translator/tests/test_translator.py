from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module

ENG_TRANSLATION = "Hello, how are you?"
GERMAN_TRANSLATION = "Hallo, wie geht es?"


class TranslatorModule(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(TranslatorModule, cls).setUpClass()
        ret = load_module_actions("jaseci_ai_kit.translator")
        assert ret == True

    @jac_testcase("translator.jac", "test_translate_hindi_eng")
    def test_translate_hindi_eng(self, ret):
        self.assertEqual(ret["report"][0], ENG_TRANSLATION)

    @jac_testcase("translator.jac", "test_translate_eng_german")
    def test_translate_eng_german(self, ret):
        self.assertEqual(ret["report"][0], GERMAN_TRANSLATION)

    @classmethod
    def tearDownClass(cls):
        super(TranslatorModule, cls).tearDownClass()
        ret = unload_module("jaseci_ai_kit.modules.use_enc.use_enc")
        assert ret == True
