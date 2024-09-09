from jaseci.utils.test_core import CoreTest
import uuid


class StackTests(CoreTest):
    """Unit tests for Jac Walker APIs"""

    fixture_src = __file__

    def test_walker_yield(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("ll.jac")}],
        )
        self.call(self.mast, ["walker_run", {"name": "init"}])
        self.call(self.mast, ["walker_run", {"name": "gen_rand_life"}])
        ret = self.call(self.mast, ["walker_run", {"name": "get_gen_day"}])
        self.assertGreater(len(ret["report"]), 3)
        self.call(self.mast, ["walker_run", {"name": "get_gen_day"}])
        self.mast._h.commit()
        self.call(self.mast, ["walker_run", {"name": "get_gen_day"}])
        self.assertEqual(len(self.mast._h.save_obj_list), 0)

    def test_walker_context_auto_refresh(self):
        ret = self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("ll.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "print_life_note"}])
        life_node = self.mast._h.get_obj(self.mast._m_id, ret["final_node"])
        life_node.context.pop("note")
        ret = self.call(self.mast, ["walker_run", {"name": "print_life_note"}])
        self.assertTrue(ret["success"])

    def test_action_module_list(self):
        ret = self.call(self.smast, ["actions_module_list", {}])
        self.assertIn("jaseci.extens.act_lib.rand", ret)
        self.assertIn("jaseci.extens.act_lib.std", ret)
        self.assertIn("jaseci.extens.act_lib.file", ret)

    def test_action_module_unload_reload(self):
        ret = self.call(self.smast, ["actions_module_list", {}])
        before = len(ret)
        ret = self.call(
            self.smast,
            ["actions_unload_module", {"name": "jaseci.extens.act_lib.rand"}],
        )
        ret = self.call(
            self.smast,
            ["actions_unload_module", {"name": "jaseci.extens.act_lib.file"}],
        )
        ret = self.call(self.smast, ["actions_module_list", {}])
        self.assertEqual(len(ret), before - 2)
        ret = self.call(
            self.smast,
            ["actions_load_module", {"mod": "jaseci.extens.act_lib.rand"}],
        )
        ret = self.call(
            self.smast,
            ["actions_load_module", {"mod": "jaseci.extens.act_lib.file"}],
        )
        ret = self.call(self.smast, ["actions_module_list", {}])
        self.assertEqual(len(ret), before)

    def test_action_module_unload_reload_aliased(self):
        ret = self.call(self.smast, ["actions_module_list", {}])
        before = len(ret)
        ret = self.call(
            self.smast,
            ["actions_unload_module", {"name": "jaseci.extens.act_lib.vector"}],
        )
        ret = self.call(self.smast, ["actions_module_list", {}])
        self.assertEqual(len(ret), before - 1)
        self.assertNotIn("vector.cos_sim", self.call(self.smast, ["actions_list", {}]))
        ret = self.call(
            self.smast,
            ["actions_load_module", {"mod": "jaseci.extens.act_lib.vector"}],
        )
        ret = self.call(self.smast, ["actions_module_list", {}])
        self.assertEqual(len(ret), before)

    def test_action_unload(self):
        ret = self.call(self.smast, ["actions_module_list", {}])
        before = len(ret)
        ret = self.call(self.smast, ["actions_list", {"name": "rand"}])
        for i in ret:
            self.call(self.smast, ["actions_unload_action", {"name": i}])
        ret = self.call(self.smast, ["actions_module_list", {}])
        self.assertEqual(len(ret), before - 1)
        ret = self.call(
            self.smast,
            ["actions_load_module", {"mod": "jaseci.extens.act_lib.rand"}],
        )

    def test_action_set_unload(self):
        ret = self.call(self.smast, ["actions_module_list", {}])
        before = len(ret)
        ret = self.call(self.smast, ["actions_unload_actionset", {"name": "rand"}])
        ret = self.call(self.smast, ["actions_module_list", {}])
        self.assertEqual(len(ret), before - 1)
        ret = self.call(
            self.smast,
            ["actions_load_module", {"mod": "jaseci.extens.act_lib.rand"}],
        )

    def test_sentinel_missing_architype(self):
        """
        Test when the original sentinel is missing the corresponding architype for a
        node
        """
        ret = self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("simple.jac")}],
        )
        old_snt = ret[0]["jid"]
        ret = self.call(self.mast, ["walker_run", {"name": "init", "snt": old_snt}])
        node_id = ret["report"][0]["jid"]
        ret = self.call(self.mast, ["sentinel_delete", {"snt": old_snt}])
        ret = self.call(self.mast, ["sentinel_list", {"snt": old_snt}])
        ret = self.call(
            self.mast,
            ["graph_node_set", {"nd": node_id, "ctx": {"b": 6}}],
        )
        self.assertIn("has_var", ret["errors"][0])
        ret = self.call(
            self.mast,
            [
                "sentinel_register",
                {
                    "name": "new_snt",
                    "auto_create_graph": False,
                    "auto_run": False,
                    "set_active": True,
                    "code": self.load_jac("simple.jac"),
                },
            ],
        )
        self.mast._h._machine = None
        ret = self.call(
            self.mast,
            ["graph_node_set", {"nd": node_id, "ctx": {"b": 6}}],
        )
        self.assertEqual(ret["context"]["b"], 6)

    def test_sentinel_missing_architype_global(self):
        """
        Test when the original sentinel is missing the corresponding architype for a
        node
        """
        ret = self.call(
            self.smast,
            [
                "sentinel_register",
                {
                    "name": "new_snt",
                    "auto_create_graph": False,
                    "auto_run": False,
                    "set_active": True,
                    "code": self.load_jac("simple.jac"),
                },
            ],
        )
        glob_snt = ret[0]["jid"]
        ret = self.call(self.smast, ["global_sentinel_set", {"snt": glob_snt}])
        ret = self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("simple.jac")}],
        )
        old_snt = ret[0]["jid"]
        ret = self.call(self.mast, ["walker_run", {"name": "init", "snt": old_snt}])
        node_id = ret["report"][0]["jid"]
        ret = self.call(self.mast, ["sentinel_delete", {"snt": old_snt}])
        ret = self.call(self.mast, ["sentinel_list", {"snt": old_snt}])
        ret = self.call(
            self.mast,
            ["graph_node_set", {"nd": node_id, "ctx": {"b": 6}}],
        )
        self.assertIn("has_var", ret["errors"][0])
        ret = self.call(self.mast, ["sentinel_active_global", {}])
        self.mast._h._machine = None
        ret = self.call(
            self.mast,
            ["graph_node_set", {"nd": node_id, "ctx": {"b": 6}}],
        )
        self.assertEqual(ret["context"]["b"], 6)

    def test_interp_deep_except(self):
        ret = self.call(
            self.smast,
            [
                "sentinel_register",
                {"auto_run": "", "code": self.load_jac("simple.jac")},
            ],
        )

        ret = self.call(self.smast, ["walker_run", {"name": "deep_except"}])
        self.assertTrue(ret["success"])
        self.assertIn("xxxx.xxxx", ret["report"][2]["msg"])

    def test_dot_profiling_in_walker(self):
        ret = self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("simple.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "init", "profiling": True}])
        self.assertIn("digraph", ret["profile"]["graph"])
        self.assertIn("jaseci", ret["profile"]["graph"])
        self.assertGreater(len(ret["profile"]["graph"]), 1000)

    def test_jac_profiling_in_walker(self):
        ret = self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("simple.jac")}],
        )
        ret = self.call(
            self.mast, ["walker_run", {"name": "complex", "profiling": True}]
        )
        print(ret["profile"]["jac"])
        self.assertIn("cum_time", ret["profile"]["jac"])
        self.assertIn("run_walker", ret["profile"]["graph"])
