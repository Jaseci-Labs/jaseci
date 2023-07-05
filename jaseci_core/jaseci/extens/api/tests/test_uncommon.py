from jaseci.utils.test_core import CoreTest


class UncommonImplementationTest(CoreTest):
    """Unit tests for Uncommon Implementaion APIs"""

    fixture_src = __file__

    def test_overrided_action_ability(self):
        self.call(
            self.smast,
            ["sentinel_register", {"code": self.load_jac("action_override.jac")}],
        )

        reports = self.call(self.smast, ["walker_run", {"name": "check"}])["report"]
        keys = [
            "log",
            "out",
            "js_input",
            "input",
            "js_round",
            "round",
            "err",
            "sleep",
            "sort_by_col",
            "time_now",
            "set_global",
            "get_global",
            "actload_local",
            "actload_remote",
            "actload_module",
            "destroy_global",
            "set_perms",
            "get_perms",
            "grant_perms",
            "revoke_perms",
            "get_report",
            "clear_report",
            "log_activity",
        ]
        for key in keys:
            # node tester - testing first report: std should be the default
            self.assertIsInstance(reports[0][key], dict)
            self.assertEqual(reports[0][key]["name"], f"std.{key}")
            self.assertEqual(reports[0][key]["kind"], "ability")

            # walker check - tester report: std should be the default
            self.assertIsInstance(reports[3][key], dict)
            self.assertEqual(reports[3][key]["name"], f"std.{key}")
            self.assertEqual(reports[3][key]["kind"], "ability")

            # node tester - testing after std.set_global = 1
            # all actions should be the same except std.set_global
            if key != "set_global":
                self.assertIsInstance(reports[1][key], dict)
                self.assertEqual(reports[1][key]["name"], f"std.{key}")
                self.assertEqual(reports[1][key]["kind"], "ability")

        self.assertIsInstance(reports[1]["set_global"], int)
        self.assertEqual(reports[1]["set_global"], 1)

        # node tester - testing third report: std set to 1
        self.assertEqual(reports[2], 1)

    def test_node_ability_from_global_sentinel(self):
        self.call(self.mast, ["graph_create", {}])

        self.call(
            self.smast,
            ["sentinel_register", {"code": self.load_jac("uncommon_impl.jac")}],
        )

        self.call(self.smast, ["global_sentinel_set", {}])
        self.call(self.mast, ["sentinel_active_global", {}])

        res = self.call(self.smast, ["walker_run", {"name": "check_ability"}])
        self.assertEqual("super_master", res["report"][0]["j_type"])
        self.assertEqual([], res["report"][1])

        # since admin already create `with_ability` node on init,
        # it should not have `inner_node`
        res = self.call(self.smast, ["walker_run", {"name": "check_ability"}])
        self.assertEqual("super_master", res["report"][0]["j_type"])
        self.assertEqual(0, len(res["report"][1]))

        # users should be able to access their inner nodes inside ability
        res = self.call(self.mast, ["walker_run", {"name": "check_ability"}])
        # before it will return the owner of the sentinel which is the super_master
        self.assertEqual("master", res["report"][0]["j_type"])
        self.assertEqual(1, len(res["report"][1]))

    def test_existing_node_in_graph_but_not_in_sentinel(self):
        self.call(
            self.smast,
            ["sentinel_register", {"code": self.load_jac("with_node_b.jac")}],
        )

        self.call(
            self.smast,
            ["sentinel_register", {"code": self.load_jac("without_node_b.jac")}],
        )

        res = self.call(self.smast, ["walker_run", {"name": "init"}])

        self.assertTrue(res["success"])
        self.assertEqual(1, len(res["report"]))
        self.assertTrue("a", len(res["report"][0]["name"]))
