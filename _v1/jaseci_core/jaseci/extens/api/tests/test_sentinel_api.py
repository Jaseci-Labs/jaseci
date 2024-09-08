from jaseci.utils.test_core import CoreTest


class SentinelApiTest(CoreTest):
    """Unit tests for Jac Walker APIs"""

    fixture_src = __file__

    def test_auto_run_when_synced_to_global(self):
        self.call(
            self.smast,
            ["sentinel_register", {"code": self.load_jac("hello_world.jac")}],
        )
        self.call(
            self.smast,
            ["global_sentinel_set", {}],
        )
        ret = self.call(
            self.mast,
            [
                "sentinel_active_global",
                {
                    "auto_run": "init",
                    "auto_run_ctx": {"wrld": "jason"},
                    "auto_create_graph": True,
                },
            ],
        )
        num_gphs = len(self.call(self.mast, ["graph_list", {}]))
        self.assertEqual(ret["auto_run_result"]["report"], ["hello jason!"])
        self.assertEqual(num_gphs, 1)

    def test_auto_run_when_synced_to_global_multi(self):
        self.call(
            self.smast,
            ["sentinel_register", {"code": self.load_jac("hello_world.jac")}],
        )
        self.call(
            self.smast,
            ["global_sentinel_set", {}],
        )
        self.call(
            self.mast,
            [
                "sentinel_active_global",
                {
                    "auto_run": "init",
                    "auto_run_ctx": {"wrld": "jason"},
                    "auto_create_graph": True,
                },
            ],
        )
        ret = self.call(
            self.mast,
            [
                "sentinel_active_global",
                {
                    "auto_run": "init",
                    "auto_run_ctx": {"wrld": "jason"},
                    "auto_create_graph": True,
                },
            ],
        )
        num_gphs = len(self.call(self.mast, ["graph_list", {}]))
        self.assertEqual(ret["auto_run_result"]["report"], ["hello jason!"])
        self.assertEqual(num_gphs, 2)
