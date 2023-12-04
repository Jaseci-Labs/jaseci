import pytest
import shutil
from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.jsorc.live_actions import load_module_actions, unload_module
from pathlib import Path


class TextParaphraserModule(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(TextParaphraserModule, cls).setUpClass()
        ret = load_module_actions("jac_nlp.paraphraser")
        assert ret == True

    @pytest.mark.order(1)
    @jac_testcase("paraphraser.jac", "test_paraphrase")
    def test_predict(self, ret):
        self.assertEqual(ret["success"], True)

    @classmethod
    def tearDownClass(cls):
        super(TextParaphraserModule, cls).tearDownClass()
        ret = unload_module("jac_nlp.paraphraser.paraphraser")
        assert ret == True
        shutil.rmtree(Path(Path.home(), ".jaseci/models/jac_nlp/paraphraser"))
