from jaseci.utils.test_core import CoreTest


class GraphApiTest(CoreTest):
    """Unit tests for Jac Walker APIs"""

    fixture_src = __file__

    def test_graph_depth(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("fam.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "create_fam"}])
        ret = self.call(self.mast, ["graph_get", {}])
        self.assertEqual(len(ret), 9)
        ret = self.call(self.mast, ["graph_get", {"depth": 2}])

        # old approach will include married edge
        # but it shouldn't since it's considered a 3rd step
        self.assertEqual(len(ret), 5)
        ret = self.call(self.mast, ["graph_get", {"depth": 1}])
        self.assertEqual(len(ret), 1)

    def test_graph_node_view(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("fam.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "create_fam"}])
        ret = self.call(self.mast, ["graph_get", {}])
        self.assertEqual(len(ret), 9)
        ret = self.call(self.mast, ["graph_node_view", {"show_edges": True}])
        self.assertEqual(len(ret), 5)
        ret = self.call(self.mast, ["graph_node_view", {}])
        self.assertEqual(len(ret), 3)

    def test_graph_node_view_filters(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("fam.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "create_fam"}])
        ret = self.call(self.mast, ["graph_node_view", {"node_type": "man"}])
        self.assertEqual(len(ret), 2)
        jid = ret[1]["jid"]
        ret = self.call(self.mast, ["graph_node_view", {"nd": jid, "show_edges": True}])
        self.assertEqual(len(ret), 7)
        ret = self.call(
            self.mast,
            [
                "graph_node_view",
                {"nd": jid, "show_edges": False, "edge_type": "married"},
            ],
        )
        self.assertEqual(len(ret), 2)
        ret = self.call(
            self.mast,
            [
                "graph_node_view",
                {"nd": jid, "show_edges": True, "edge_type": "married"},
            ],
        )
        self.assertEqual(len(ret), 3)
