from jaseci.utils.test_core import core_test


class mail_lib_test(core_test):
    """Unit tests for Jac Walker APIs"""

    fixture_src = __file__

    def test_send_mail(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("mail_test.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "send_mail"}])
        self.assertTrue(ret["success"])
