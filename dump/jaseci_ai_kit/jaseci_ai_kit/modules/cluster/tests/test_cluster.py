import pytest

from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module


class TextClusterModule(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(TextClusterModule, cls).setUpClass()
        aux_ret = load_module_actions("jaseci_ai_kit.use_enc")
        ret = load_module_actions("jaseci_ai_kit.cluster")
        assert ret == True

    @pytest.mark.order(1)
    @jac_testcase("cluster.jac", "test_umap")
    def test_umap(self, ret):
        self.assertEqual(ret["success"], True)
        self.assertEqual(len(ret["report"][0]), 15)
        self.assertEqual(len(ret["report"][0][0]), 2)

    @pytest.mark.order(2)
    @jac_testcase("cluster.jac", "test_get_cluster_hbdscan")
    def test_get_clusters(self, ret):
        self.assertEqual(ret["success"], True)
        self.assertEqual(len(ret["report"][0]), 15)

    @pytest.mark.order(3)
    @jac_testcase("cluster.jac", "test_get_cluster_kmeans")
    def test_get_clusters(self, ret):
        self.assertEqual(ret["success"], True)
        self.assertEqual(len(ret["report"][0]), 15)

    @classmethod
    def tearDownClass(cls):
        super(TextClusterModule, cls).tearDownClass()
        aux_ret = unload_module("jaseci_ai_kit.modules.use_enc.use_enc")
        ret = unload_module("jaseci_ai_kit.modules.cluster.cluster")
        assert ret == True
