from jaseci.utils.test_core import CoreTest


class GraphApiTest(CoreTest):
    """Unit tests for Jac Walker APIs"""

    fixture_src = __file__

    def test_graph_node_view(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("fam.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "create_fam"}])
        ret = self.call(self.mast, ["graph_get", {}])
        self.assertEqual(len(ret), 9)
        ret = self.call(self.mast, ["graph_node_view", {}])
        self.assertEqual(len(ret), 5)
        ret = self.call(self.mast, ["graph_node_view", {"show_edges": False}])
        self.assertEqual(len(ret), 3)
