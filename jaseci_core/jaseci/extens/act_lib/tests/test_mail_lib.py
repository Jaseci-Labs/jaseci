from unittest.mock import MagicMock, Mock

from jaseci.jsorc.jsorc import JsOrc
from jaseci.extens.svc.mail_svc import MailService
from jaseci.utils.test_core import CoreTest


class MailLibTest(CoreTest):
    """Unit tests for Jac Walker APIs"""

    fixture_src = __file__

    def __init__(self, *args, **kwargs):
        JsOrc.settings("MAIL_CONFIG")["enabled"] = True
        MailService.connect = MagicMock(return_value=Mock())
        super(MailLibTest, self).__init__(*args, **kwargs)

    def setUp(self):
        super().setUp()

    @JsOrc.inject(services=["mail"])
    def test_send_mail(self, mail: MailService):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("mail_test.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "send_mail"}])
        self.assertTrue(ret["success"])
        self.assertTrue(mail.connect.called)
        self.assertEqual(
            mail.app.method_calls[0].args,
            (None, ["jaseci.dev@gmail.com"], "Test Subject", ("Test", "<h1>Test</h1>")),
        )
