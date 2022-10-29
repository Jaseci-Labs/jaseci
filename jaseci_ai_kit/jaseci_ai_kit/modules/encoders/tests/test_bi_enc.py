from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module


class BiEncTest(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(BiEncTest, cls).setUpClass()
        load_module_actions("jaseci_ai_kit.bi_enc")

    @jac_testcase("bi_enc.jac", "test_bi_enc_cos_sim")
    def test_cos_sim_function(self, ret):
        print(ret)
        self.assertEqual(round(ret["report"][0], 2), 0.98)

    @jac_testcase("bi_enc.jac", "test_bi_enc_infer")
    def test_biencoder_infer(self, ret):
        self.assertEqual(ret["success"], True)

    @jac_testcase("bi_enc.jac", "test_bi_enc_context_emb")
    def test_biencoder_context_emb(self, ret):
        self.assertEqual(ret["success"], True)
        self.assertEqual(len(ret["report"][0][0]), 128)

    @jac_testcase("bi_enc.jac", "test_bi_enc_cand_emb")
    def test_biencoder_candidate_emb(self, ret):
        self.assertEqual(ret["success"], True)
        self.assertEqual(len(ret["report"][0][0]), 128)

    @jac_testcase("bi_enc.jac", "test_bi_enc_train_config")
    def test_biencoder_train_config(self, ret):
        self.assertEqual(ret["success"], True)

    @jac_testcase("bi_enc.jac", "test_bi_enc_model_config")
    def test_biencoder_model_config(self, ret):
        self.assertEqual(ret["success"], True)

    @jac_testcase("bi_enc.jac", "test_bi_enc_train")
    def test_biencoder_train(self, ret):
        self.assertEqual(ret["report"][0], "Model Training is complete.")
        self.assertEqual(ret["success"], True)

    @jac_testcase("bi_enc.jac", "test_bi_enc_save_model")
    def test_biencoder_save_model(self, ret):
        self.assertEqual(ret["success"], True)

    @jac_testcase("bi_enc.jac", "test_bi_enc_load_model")
    def test_biencoder_load_model(self, ret):
        self.assertEqual(ret["success"], True)

    @classmethod
    def tearDownClass(cls):
        super(BiEncTest, cls).tearDownClass()
        unload_module("jaseci_ai_kit.bi_enc")
