import pytest

from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.jsorc.live_actions import load_module_actions, unload_module


class TextClusterModule(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(TextClusterModule, cls).setUpClass()
        ret = load_module_actions("jac_misc.cluster")
        assert ret == True

    @jac_testcase("cluster.jac", "test_umap")
    def test_umap(self, ret):
        self.assertEqual(ret["success"], True)
        self.assertEqual(len(ret["report"][0]), 15)
        self.assertEqual(len(ret["report"][0][0]), 2)

    @jac_testcase("cluster.jac", "test_get_cluster_hbdscan")
    def test_get_clusters_hbdscan(self, ret):
        self.assertEqual(ret["success"], True)
        self.assertEqual(len(ret["report"][0]), 15)

    @jac_testcase("cluster.jac", "test_get_cluster_kmeans")
    def test_get_clusters_kmeans(self, ret):
        self.assertEqual(ret["success"], True)
        self.assertEqual(len(ret["report"][0]), 15)

    @classmethod
    def tearDownClass(cls):
        super(TextClusterModule, cls).tearDownClass()
        ret = unload_module("jac_misc.cluster.cluster")
        assert ret == True
