from jaseci.utils.test_core import CoreTest


class NetLibTest(CoreTest):
    """Unit tests for Jac Walker APIs"""

    fixture_src = __file__

    def test_pack(self):
        ret = self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("net_pack.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "pack_it"}])
        self.assertEqual(len(ret["report"][0]["nodes"]), 11)
        self.assertEqual(len(ret["report"][0]["edges"]), 10)

    def test_pack_subgraph(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("net_pack.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "pack_it_subgraph"}])
        self.assertEqual(len(ret["report"][0]["nodes"]), 5)
        self.assertEqual(len(ret["report"][0]["edges"]), 4)

    def test_pack_unpack(self):
        ret = self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("net_pack.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "pack_unpack"}])

        self.assertEqual(ret["report"][0], 16)

    def test_pack_unpack_terse(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("net_pack.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "pack_unpack_terse"}])
        self.assertEqual(ret["report"][0], 16)

    def test_pack_and_destroy(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("net_pack.jac")}],
        )
        before = len(self.smast._h.mem)
        ret = self.call(self.mast, ["walker_run", {"name": "pack_it_destroy"}])
        self.assertEqual(len(ret["report"]), 1)
        after = len(self.smast._h.mem)
        self.assertEqual(before, after)

    def test_pack_anc_priv(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("net_pack.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "pack_it_anc_priv"}])
        self.assertEqual(len(ret["report"]), 6)
        self.assertNotIn("priv", ret["report"][2]["context"])
