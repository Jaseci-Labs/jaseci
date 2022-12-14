from unittest.mock import MagicMock, Mock, patch

from jaseci.svc import MetaService
from jaseci.svc.mail import Mailer
from jaseci.svc.mail import MAIL_CONFIG
from jaseci.utils.test_core import CoreTest


class MailLibTest(CoreTest):
    """Unit tests for Jac Walker APIs"""

    fixture_src = __file__

    def __init__(self, *args, **kwargs):
        super(MailLibTest, self).__init__(*args, **kwargs)

    def setUp(self):
        super().setUp(True)

    @patch("jaseci.svc.mail.Mailer")
    def test_send_mail(self, mailer: MagicMock):
        mail = MetaService().get_service("mail")
        mail.enabled = True
        mail.connect = MagicMock(return_value=mailer)
        mail.start()

        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("mail_test.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "send_mail"}])
        self.assertTrue(ret["success"])
        self.assertTrue(mailer.send_custom_email.called)
        self.assertEqual(
            mailer.send_custom_email.call_args.args,
            (None, ["jaseci.dev@gmail.com"], "Test Subject", ("Test", "<h1>Test</h1>")),
        )
