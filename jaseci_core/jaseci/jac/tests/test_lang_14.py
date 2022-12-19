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
        ret = self.call(self.mast, ["graph_get", {}])
        self.assertEqual(len(ret), 9)
        ret = self.call(self.mast, ["graph_get", {"depth": 2}])

        # old approach will include married edge
        # but it shouldn't since it's considered a 3rd step
        self.assertEqual(len(ret), 5)
        ret = self.call(self.mast, ["graph_get", {"depth": 1}])
        self.assertEqual(len(ret), 1)
