from copy import copy
from unittest.mock import Mock, MagicMock
from jaseci.svcs.mail.mail_svc import mail_svc
from jaseci.svcs.mail.mail_svc import EMAIL_CONFIG
from jaseci.utils.test_core import core_test


class mail_lib_test(core_test):
    """Unit tests for Jac Walker APIs"""

    fixture_src = __file__

    def __init__(self, *args, **kwargs):
        mail_svc.connect = MagicMock(return_value=Mock())
        super(mail_lib_test, self).__init__(*args, **kwargs)

    def test_send_mail(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("mail_test.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "send_mail"}])
        self.assertTrue(ret["success"])

        ms = mail_svc()
        configs = copy(EMAIL_CONFIG)
        configs.pop("quiet")

        self.assertEqual(ms.connect.call_args[0], (configs,))

        self.assertEqual(
            ms.app.method_calls[0].args,
            (None, ["jaseci.dev@gmail.com"], "Test Subject", ("Test", "<h1>Test</h1>")),
        )
