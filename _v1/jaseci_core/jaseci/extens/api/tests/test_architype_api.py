from jaseci.utils.test_core import CoreTest


class ArchitypeApiTest(CoreTest):
    """Unit tests for Jac Architype APIs"""

    fixture_src = __file__

    def test_architype_register(self):
        self.call(
            self.smast,
            ["sentinel_register", {"code": self.load_jac("hello_world.jac")}],
        )

        ret = self.call(
            self.smast,
            [
                "architype_register",
                {
                    "code": self.load_jac("test_architype.jac"),
                    "encoded": False,
                },
            ],
        )

        self.assertEqual(ret["success"], True)
        self.assertEqual(ret["architype"]["name"], "test_architype")

        architype_list_ret = self.call(
            self.smast,
            ["architype_list", {"detailed": True}],
        )

        self.assertEqual(len(architype_list_ret), 7)

    def test_architype_get(self):
        self.call(
            self.smast,
            ["sentinel_register", {"code": self.load_jac("hello_world.jac")}],
        )

        ret = self.call(
            self.smast,
            [
                "architype_register",
                {
                    "code": self.load_jac("test_architype.jac"),
                    "encoded": False,
                },
            ],
        )

        architype_get_ret = self.call(
            self.smast,
            ["architype_get", {"arch": ret["architype"]["jid"]}],
        )

        architype_get_ret_code = self.call(
            self.smast,
            ["architype_get", {"arch": ret["architype"]["jid"], "mode": "code"}],
        )

        self.assertEqual(architype_get_ret["architype"]["name"], "test_architype")
        self.assertEqual(
            "walker test_architype" in architype_get_ret_code["code"], True
        )
