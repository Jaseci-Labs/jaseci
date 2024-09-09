from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.jsorc.live_actions import load_module_actions, unload_module


class UseEncModule(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(UseEncModule, cls).setUpClass()
        ret = load_module_actions("jac_nlp.use_enc")
        assert ret == True

    @jac_testcase("use_enc.jac", "test_enc_cos_sim_score")
    def test_enc_cos_sim_score(self, ret):
        self.assertGreaterEqual(round(ret["report"][0], 2), 0.9)

    @jac_testcase("use_enc.jac", "test_enc_text_similarity")
    def test_enc_text_similarity(self, ret):
        self.assertEqual(round(ret["report"][0], 2), 0.03)

    @jac_testcase("use_enc.jac", "test_enc_text_classify")
    def test_enc_text_classify(self, ret):
        self.assertEqual(ret["report"][0]["match"], "getdirections")

    @jac_testcase("use_enc.jac", "test_enc_get_embeddings")
    def test_enc_get_embeddings(self, ret):
        self.assertEqual(len(ret["report"][0][0]), 512)

    @classmethod
    def tearDownClass(cls):
        super(UseEncModule, cls).tearDownClass()
        ret = unload_module("jac_nlp.use_enc.use_enc")
        assert ret == True
