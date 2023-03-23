from jaseci.prim.edge import Edge
from jaseci.prim.node import Node
from jaseci.utils.test_core import CoreTest


class WalkerApiTest(CoreTest):
    """Unit tests for Jac Walker APIs"""

    fixture_src = __file__

    def test_walker_yield(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("walker_yield.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield"}])
        self.assertEqual(ret["report"], ["entering", 7])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield"}])
        self.assertEqual(ret["report"], [8])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield"}])
        self.assertEqual(ret["report"], [9])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield"}])
        self.assertEqual(ret["report"], [10])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield"}])
        self.assertEqual(ret["report"], ["should start over now", "exiting"])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield"}])
        self.assertEqual(ret["report"], ["entering", 7])

    def test_walker_yield_update(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("walker_yield.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield"}])
        self.assertEqual(ret["report"], ["entering", 7])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield"}])
        self.assertEqual(ret["report"], [8])
        ret = self.call(
            self.mast, ["walker_run", {"name": "test_yield", "ctx": {"a": 2}}]
        )
        self.assertEqual(ret["report"], [3])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield"}])
        self.assertEqual(ret["report"], [4])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield"}])
        self.assertEqual(ret["report"], [5])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield"}])
        self.assertEqual(ret["report"], [6])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield"}])
        self.assertEqual(ret["report"], [7])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield"}])
        self.assertEqual(ret["report"], [8])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield"}])
        self.assertEqual(ret["report"], [9])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield"}])
        self.assertEqual(ret["report"], [10])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield"}])
        self.assertEqual(ret["report"], ["should start over now", "exiting"])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield"}])
        self.assertEqual(ret["report"], ["entering", 7])

    def test_walker_yield_report(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("walker_yield.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_report"}])
        self.assertEqual(ret["report"], [7])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_report"}])
        self.assertEqual(ret["report"], [8])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_report"}])
        self.assertEqual(ret["report"], [9])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_report"}])
        self.assertEqual(ret["report"], [10])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_report"}])
        self.assertEqual(ret["report"], ["should start over now"])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_report"}])
        self.assertEqual(ret["report"], [7])

    def test_walker_yield_disengage(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("walker_yield.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_disengage"}])
        self.assertEqual(ret["report"], [7])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_disengage"}])
        self.assertEqual(ret["report"], [8])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_disengage"}])
        self.assertEqual(ret["report"], [9])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_disengage"}])
        self.assertEqual(ret["report"], [10])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_disengage"}])
        self.assertEqual(ret["report"], ["should start over now"])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_disengage"}])
        self.assertEqual(ret["report"], [7])

    def test_walker_yield_take(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("walker_yield.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_take"}])
        self.assertEqual(ret["report"], [7, "test"])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_take"}])
        self.assertEqual(ret["report"], [8, "test"])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_take"}])
        self.assertEqual(ret["report"], [9, "test"])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_take"}])
        self.assertEqual(ret["report"], [10, "test"])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_take"}])
        self.assertEqual(ret["report"], ["should start over now"])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_take"}])
        self.assertEqual(ret["report"], [7, "test"])

    def test_walker_smart_yield(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("walker_yield.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "smart_yield"}])
        before = self.mast._h.get_object_distribution()
        ret = self.call(self.mast, ["walker_run", {"name": "smart_yield"}])
        ret = self.call(self.mast, ["walker_run", {"name": "smart_yield"}])
        ret = self.call(self.mast, ["walker_run", {"name": "smart_yield"}])
        after = self.mast._h.get_object_distribution()
        self.assertEqual(before, after)
        self.assertEqual(ret["report"], [{"id": 2}])

    def test_walker_smart_yield_no_future(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("walker_yield.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "smart_yield_no_future"}])
        before = self.mast._h.get_object_distribution()
        ret = self.call(self.mast, ["walker_run", {"name": "smart_yield_no_future"}])
        ret = self.call(self.mast, ["walker_run", {"name": "smart_yield_no_future"}])
        ret = self.call(self.mast, ["walker_run", {"name": "smart_yield_no_future"}])
        after = self.mast._h.get_object_distribution()
        self.assertEqual(before, after)
        self.assertEqual(ret["report"], [{}])

    def test_walker_deep_yield(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("walker_yield.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "deep_yield"}])
        self.assertEqual(
            ret["report"],
            [
                {},
                {"id": 0},
                {"id": 1},
                {"id": 2},
                {"id": 3},
                {"id": 4},
                {"id": 5},
                {"id": 6},
                {"id": 7},
                {"id": 8},
                {"id": 9},
                {},
                {"id": 0},
                {"id": 1},
                {"id": 2},
                11,
            ],
        )

    def test_walker_simple_yield(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("walker_yield.jac")}],
        )
        expected = [
            "entry",
            {"id": 0},
            {"id": 1},
            {"id": 2},
            {"id": 3},
            {"id": 4},
            {"id": 5},
            {"id": 6},
            {"id": 7},
            {"id": 8},
            {"id": 9},
            "entry",
            {"id": 0},
            {"id": 10},
            {"id": 1},
            {"id": 11},
        ]
        for i in range(16):
            ret = self.call(self.mast, ["walker_run", {"name": "simple_yield"}])
            self.assertEqual(ret["report"][0], expected[i])

    def test_walker_deep_yield2(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("walker_yield.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "deep_yield2"}])
        self.assertEqual(
            ret["report"],
            [
                "entry",
                {},
                {"id": 0},
                {"id": 1},
                {"id": 2},
                {"id": 3},
                {"id": 4},
                {"id": 5},
                {"id": 6},
                {"id": 7},
                {"id": 8},
                {"id": 9},
                "entry",
                {},
                {"id": 0},
                {"id": 10},
                {"id": 1},
                {"id": 11},
            ],
        )

    def test_walker_deep_yield_no_leak(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("walker_yield.jac")}],
        )
        before = self.mast._h.get_object_distribution()
        self.call(self.mast, ["walker_run", {"name": "deep_yield"}])
        self.call(self.mast, ["walker_run", {"name": "deep_yield"}])
        self.call(self.mast, ["walker_run", {"name": "deep_yield"}])
        after = self.mast._h.get_object_distribution()
        after.pop(Node)
        after.pop(Edge)
        self.assertEqual(before, after)

    def test_walker_simple_yield_skip_test(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("walker_yield.jac")}],
        )
        ret = []
        for i in range(16):
            ret += self.call(
                self.mast, ["walker_run", {"name": "simple_yield_skip_test"}]
            )["report"]
        self.assertEqual(
            ret,
            [
                "entry",
                {},
                "in_node",
                {"id": 0},
                "in_node",
                {"id": 1},
                "in_node",
                {"id": 2},
                "in_node",
                {"id": 3},
                "in_node",
                {"id": 4},
                5,
                {"id": 5},
                5,
                {"id": 6},
                5,
                {"id": 7},
                5,
                {"id": 8},
                5,
                {"id": 9},
                "entry",
                {},
                "in_node",
                {"id": 0},
                "in_node",
                {"id": 10},
                "in_node",
                {"id": 1},
                "in_node",
                {"id": 11},
            ],
        )

    def test_error_reporting_walker_only_actions(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("walker_yield.jac")}],
        )
        ret = []
        self.call(self.mast, ["walker_run", {"name": "error_walker_action"}])
        ret = self.call(self.mast, ["walker_run", {"name": "error_walker_action"}])
        self.assertIn('cannot execute the statement "disengage ; "', ret["errors"][0])

    def test_walker_stepping(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("fam.jac")}],
        )
        ret = self.call(self.mast, ["walker_spawn_create", {"name": "create_fam"}])
        jid = ret["jid"]
        ret = self.call(self.mast, ["walker_prime", {"wlk": jid}])
        ret = self.call(self.mast, ["walker_step", {"wlk": jid}])
        self.log(ret)
        self.assertEqual(len(ret["next_node_ids"]), 2)
        ret = self.call(self.mast, ["walker_step", {"wlk": jid}])
        self.assertEqual(len(ret["next_node_ids"]), 1)
        ret = self.call(self.mast, ["walker_step", {"wlk": jid}])
        self.assertEqual(len(ret["next_node_ids"]), 0)
        ret = self.call(self.mast, ["walker_step", {"wlk": jid}])
        self.assertEqual(len(ret["next_node_ids"]), 0)
