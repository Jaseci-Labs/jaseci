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
        life_node = self.mast._h.get_obj(self.mast._m_id, uuid.UUID(ret["final_node"]))
        life_node.context.pop("note")
        ret = self.call(self.mast, ["walker_run", {"name": "print_life_note"}])
        self.assertTrue(ret["success"])

    def test_action_module_list(self):
        ret = self.call(self.smast, ["actions_module_list", {}])
        self.assertIn("jaseci.actions.standard.rand", ret)
        self.assertIn("jaseci.actions.standard.std", ret)
        self.assertIn("jaseci.actions.standard.file", ret)

    def test_action_module_unload_reload(self):
        ret = self.call(self.smast, ["actions_module_list", {}])
        before = len(ret)
        ret = self.call(
            self.smast,
            ["actions_unload_module", {"name": "jaseci.actions.standard.rand"}],
        )
        ret = self.call(
            self.smast,
            ["actions_unload_module", {"name": "jaseci.actions.standard.file"}],
        )
        ret = self.call(self.smast, ["actions_module_list", {}])
        self.assertEqual(len(ret), before - 2)
        ret = self.call(
            self.smast,
            ["actions_load_module", {"mod": "jaseci.actions.standard.rand"}],
        )
        ret = self.call(
            self.smast,
            ["actions_load_module", {"mod": "jaseci.actions.standard.file"}],
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
            ["actions_load_module", {"mod": "jaseci.actions.standard.rand"}],
        )

    def test_action_set_unload(self):
        ret = self.call(self.smast, ["actions_module_list", {}])
        before = len(ret)
        ret = self.call(self.smast, ["actions_unload_actionset", {"name": "rand"}])
        ret = self.call(self.smast, ["actions_module_list", {}])
        self.assertEqual(len(ret), before - 1)
        ret = self.call(
            self.smast,
            ["actions_load_module", {"mod": "jaseci.actions.standard.rand"}],
        )
