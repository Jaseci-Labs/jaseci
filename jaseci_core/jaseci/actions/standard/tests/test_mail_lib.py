from copy import copy
from unittest.mock import MagicMock, Mock

from jaseci.svc import MailService
from jaseci.svc.mail import MAIL_CONFIG
from jaseci.utils.test_core import CoreTest


class MailLibTest(CoreTest):
    """Unit tests for Jac Walker APIs"""

    fixture_src = __file__

    def __init__(self, *args, **kwargs):
        MailService.connect = MagicMock(return_value=Mock())
        super(MailLibTest, self).__init__(*args, **kwargs)

    def test_send_mail(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("mail_test.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "send_mail"}])
        self.assertTrue(ret["success"])

        ms = MailService()
        configs = copy(MAIL_CONFIG)
        configs.pop("quiet")

        self.assertEqual(ms.connect.call_args[0], (configs,))

        self.assertEqual(
            ms.app.method_calls[0].args,
            (None, ["jaseci.dev@gmail.com"], "Test Subject", ("Test", "<h1>Test</h1>")),
        )
