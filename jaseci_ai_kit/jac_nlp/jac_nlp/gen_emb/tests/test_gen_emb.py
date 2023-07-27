import pytest
from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.jsorc.live_actions import load_module_actions, unload_module


class GenerateEmbeddingTest(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(GenerateEmbeddingTest, cls).setUpClass()
        ret = load_module_actions("jac_nlp.gen_emb")
        assert ret is True

    @pytest.mark.order(1)
    @jac_testcase("gen_emb.jac", "test_generate_embedding_bi_enc")
    def test_generate_embedding_bi_enc(self, ret):
        assert ret["success"] is True

    @pytest.mark.order(2)
    @jac_testcase("gen_emb.jac", "test_generate_embedding_sbert_sim")
    def test_generate_embedding_sbert_sim(self, ret):
        assert ret["success"] is True

    @pytest.mark.order(3)
    @jac_testcase("gen_emb.jac", "test_generate_embedding_use_enc")
    def test_generate_embedding_use_enc(self, ret):
        assert ret["success"] is True

    @pytest.mark.order(4)
    @jac_testcase("gen_emb.jac", "test_generate_embedding_use_qa")
    def test_generate_embedding_use_qa(self, ret):
        assert ret["success"] is True

    @pytest.mark.order(3)
    @jac_testcase("gen_emb.jac", "test_generate_embedding_gpt2")
    def test_generate_embedding_gpt2(self, ret):
        assert ret["success"] is True

    @classmethod
    def tearDownClass(cls):
        super(GenerateEmbeddingTest, cls).tearDownClass()
        ret = unload_module("jac_nlp.gen_emb")
        assert ret is True
