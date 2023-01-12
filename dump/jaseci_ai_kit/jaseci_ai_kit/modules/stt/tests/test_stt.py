from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module
import pytest

TRANSCRIPTION = "Mr. Quilter is the apostle of the middle classes and we are glad to welcome his gospel."
TRANSCRIPTION_FRENCH = "Bonjour, je m'appelle Christian, j'ai en faisant, et je vais vous raconter tous les sports que j'ai fait. J'ai fait deux ans de décapalon. J'ai décapalon, en fait, c'est un peu, c'est l'accourse du multisport. J'ai fait après un an le foot. Et après, en ce moment, j'ai eu en train de faire de la gymnastique, la gymnastique, ça consiste de plusieurs agrées, et c'est là de mes sports préférés."
TRANSLATION = (
    "Hello, I'm Papal Christian and I'm going to tell you all the things I did."
)


class Speech2TextModule(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(Speech2TextModule, cls).setUpClass()
        ret = load_module_actions("jaseci_ai_kit.stt")
        assert ret == True

    @pytest.mark.order(1)
    @jac_testcase("stt.jac", "test_audio_to_array")
    def test_audio_to_array(self, ret):
        self.assertGreater(len(ret["report"][0]), 0)

    @pytest.mark.order(2)
    @jac_testcase("stt.jac", "test_transribe_array")
    def test_transribe_array(self, ret):
        self.assertEqual(ret["report"][0], TRANSCRIPTION)

    @pytest.mark.order(3)
    @jac_testcase("stt.jac", "test_transribe_file")
    def test_transribe_file(self, ret):
        self.assertEqual(ret["report"][0], TRANSCRIPTION)

    @pytest.mark.order(4)
    @jac_testcase("stt.jac", "test_transribe_url")
    def test_transribe_url(self, ret):
        self.assertEqual(ret["report"][0], TRANSCRIPTION_FRENCH)

    @pytest.mark.order(5)
    @jac_testcase("stt.jac", "test_translate")
    def test_translate(self, ret):
        self.assertIn(TRANSLATION, ret["report"][0])

    @classmethod
    def tearDownClass(cls):
        super(Speech2TextModule, cls).tearDownClass()
        ret = unload_module("jaseci_ai_kit.modules.stt.stt")
        assert ret == True
