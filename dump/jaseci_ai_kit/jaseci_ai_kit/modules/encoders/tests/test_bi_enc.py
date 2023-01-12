from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module
import pytest


class BiEncTest(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(BiEncTest, cls).setUpClass()
        ret = load_module_actions("jaseci_ai_kit.bi_enc")
        assert ret is True

    @pytest.mark.order(1)
    @jac_testcase("bi_enc.jac", "test_bi_enc_cos_sim")
    def test_cos_sim_function(self, ret):
        self.assertEqual(round(ret["report"][0], 2), 0.98)

    @pytest.mark.order(2)
    @jac_testcase("bi_enc.jac", "test_bi_enc_infer")
    def test_biencoder_infer(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(3)
    @jac_testcase("bi_enc.jac", "test_bi_enc_context_emb")
    def test_biencoder_context_emb(self, ret):
        self.assertEqual(ret["success"], True)
        self.assertEqual(len(ret["report"][0][0]), 128)

    @pytest.mark.order(4)
    @jac_testcase("bi_enc.jac", "test_bi_enc_cand_emb")
    def test_biencoder_candidate_emb(self, ret):
        self.assertEqual(ret["success"], True)
        self.assertEqual(len(ret["report"][0][0]), 128)

    @pytest.mark.order(5)
    @jac_testcase("bi_enc.jac", "test_bi_enc_get_train_config")
    def test_biencoder_get_train_config(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(6)
    @jac_testcase("bi_enc.jac", "test_bi_enc_get_model_config")
    def test_biencoder_get_model_config(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(7)
    @jac_testcase("bi_enc.jac", "test_bi_enc_train")
    def test_biencoder_train(self, ret):
        self.assertEqual(ret["report"][0], "Model Training is complete.")
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(8)
    @jac_testcase("bi_enc.jac", "test_bi_enc_save_model")
    def test_biencoder_save_model(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(9)
    @jac_testcase("bi_enc.jac", "test_bi_enc_load_model")
    def test_biencoder_load_model(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(10)
    @jac_testcase("bi_enc.jac", "test_bi_enc_set_model_config")
    def test_biencoder_set_model_config(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(11)
    @jac_testcase("bi_enc.jac", "test_bi_enc_set_train_config")
    def test_biencoder_set_train_config(self, ret):
        self.assertEqual(ret["success"], True)

    @classmethod
    def tearDownClass(cls):
        super(BiEncTest, cls).tearDownClass()
        ret = unload_module("jaseci_ai_kit.modules.encoders.bi_enc")
        assert ret is True
