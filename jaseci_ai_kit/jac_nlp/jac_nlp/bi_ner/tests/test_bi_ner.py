from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module
import pytest


class BiNERTest(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(BiNERTest, cls).setUpClass()
        ret = load_module_actions("jac_nlp.bi_ner")
        assert ret is True

    @pytest.mark.order(1)
    @jac_testcase("bi_ner.jac", "test_bi_ner_train")
    def test_ner_train(self, ret):
        print(ret)
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(2)
    @jac_testcase("bi_ner.jac", "test_bi_ner_infer")
    def test_biner_infer(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(3)
    @jac_testcase("bi_ner.jac", "test_bi_ner_save_model")
    def test_biencoder_save_model(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(4)
    @jac_testcase("bi_ner.jac", "test_bi_ner_load_model")
    def test_biencoder_load_model(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(5)
    @jac_testcase("bi_ner.jac", "test_bi_ner_set_model_config")
    def test_biencoder_set_model_config(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(6)
    @jac_testcase("bi_ner.jac", "test_bi_ner_set_train_config")
    def test_biencoder_set_train_config(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(7)
    @jac_testcase("bi_ner.jac", "test_bi_ner_get_train_config")
    def test_biencoder_get_train_config(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(8)
    @jac_testcase("bi_ner.jac", "test_bi_ner_get_model_config")
    def test_biencoder_get_model_config(self, ret):
        self.assertEqual(ret["success"], True)

    @classmethod
    def tearDownClass(cls):
        super(BiNERTest, cls).tearDownClass()
        ret = unload_module("jac_nlp.bi_ner.bi_ner")
        assert ret is True
