from jaseci.utils.test_core import CoreTest


class UserApiTest(CoreTest):
    """Unit tests for Jac Walker APIs"""

    fixture_src = __file__

    def test_user_create_global_init(self):
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
                "user_create",
                {
                    "name": "joe",
                    "global_init": "init",
                    "global_init_ctx": {"wrld": "jason"},
                },
            ],
        )
        self.assertEqual(
            ret["global_init"]["auto_run_result"]["report"], ["hello jason!"]
        )
        self.assertEqual(ret["user"]["name"], "joe")
