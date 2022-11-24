import pytest

from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module


class TextUmapModule(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(TextUmapModule, cls).setUpClass()
        aux_ret = load_module_actions("jaseci_ai_kit.use_enc")
        ret = load_module_actions("jaseci_ai_kit.umap_cluster")
        assert ret == True

    @pytest.mark.order(1)
    @jac_testcase("umap_cluster.jac", "test_umap")
    def test_umap(self, ret):
        self.assertEqual(ret["success"], True)
        self.assertEqual(len(ret["report"][0]), 15)
        self.assertEqual(len(ret["report"][0][0]), 2)

    @pytest.mark.order(2)
    @jac_testcase("umap_cluster.jac", "test_get_clusters")
    def test_get_clusters(self, ret):
        self.assertEqual(ret["success"], True)
        self.assertEqual(len(ret["report"][0]), 15)

    @classmethod
    def tearDownClass(cls):
        super(TextUmapModule, cls).tearDownClass()
        aux_ret = unload_module("jaseci_ai_kit.modules.use_enc.use_enc")
        ret = unload_module("jaseci_ai_kit.modules.umap_cluster.umap_cluster")
        assert ret == True
