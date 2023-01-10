from jaseci.utils.test_core import CoreTest


class Lang14Test(CoreTest):
    """Unit tests for Jac Walker APIs"""

    fixture_src = __file__

    def test_free_reference(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("fam.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "free_ref"}])
        self.assertTrue(ret["success"])
        self.assertEqual(len(ret["report"]), 4)
        self.assertEqual(ret["report"][0][0]["name"], "woman")
        self.assertNotEqual(ret["report"][1][0], ret["report"][2][0])
        self.assertEqual(len(ret["report"][1]), 1)
        self.assertEqual(len(ret["report"][3]), 3)
        self.assertIn(ret["report"][1][0], ret["report"][3])

    def test_kwargs(self):
        ret = self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("general.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "test_kwargs"}])
        self.assertEqual(ret["report"][0].count("."), 4)
        self.assertEqual(ret["report"][1], ret["report"][2])
        self.assertNotEqual(ret["report"][3], ret["report"][2])
