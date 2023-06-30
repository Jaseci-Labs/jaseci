from jaseci.utils.test_core import CoreTest


class UncommonImplementationTest(CoreTest):
    """Unit tests for Uncommon Implementaion APIs"""

    fixture_src = __file__

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
