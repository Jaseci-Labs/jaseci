from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module
import pytest


class SbertSimTest(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(SbertSimTest, cls).setUpClass()
        ret = load_module_actions("jac_nlp.sbert_sim")
        assert ret is True

    @pytest.mark.order(1)
    @jac_testcase("sbert_sim.jac", "test_sbert_sim_load_model")
    def test_sbert_sim_load_model(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(2)
    @jac_testcase("sbert_sim.jac", "test_train_sbert_sim")
    def test_train_sbert_sim(self, ret):
        self.assertEqual(ret["success"], True)
        self.assertEqual(ret["report"][0], "Model Training is completed")

    @pytest.mark.order(4)
    @jac_testcase("sbert_sim.jac", "test_get_text_sim")
    def test_get_text_sim(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(5)
    @jac_testcase("sbert_sim.jac", "test_sbert_sim_get_train_config")
    def test_sbert_sim_get_train_config(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(5)
    @jac_testcase("sbert_sim.jac", "test_sbert_sim_get_cos_score")
    def test_sbert_sim_cos_score(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(5)
    @jac_testcase("sbert_sim.jac", "test_sbert_sim_get_dot_score")
    def test_sbert_sim_get_dot_score(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(5)
    @jac_testcase("sbert_sim.jac", "test_sbert_sim_get_embeddings")
    def test_sbert_sim_get_embeddings(self, ret):
        self.assertEqual(ret["success"], True)

    @classmethod
    def tearDownClass(cls):
        super(SbertSimTest, cls).tearDownClass()
        ret = unload_module("jac_nlp.sbert_sim.sbert_sim")
        assert ret is True
