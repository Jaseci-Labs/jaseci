from jaseci.utils.test_core import core_test


class interpreter_test(core_test):
    """Unit tests for Jac Interpreter / Language features"""

    fixture_src = __file__

    def test_has_var_plucking(self):
        ret = self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("lang_features.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "has_var_plucking"}])
        self.assertEqual(
            ret["report"], [["node0", "node1", "node2"], ["edge0", "edge1", "edge2"]]
        )

    def test_deref_adaptive(self):
        ret = self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("lang_features.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "deref_adaptive"}])
        self.assertTrue(ret["report"][0].startswith("junk and stuff"))
        self.assertEqual(ret["report"][1], {"name": "node0"})

    def test_deref_of_element_fails(self):
        ret = self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("lang_features.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "deref_of_element_fails"}])
        self.assertFalse(ret["success"])
