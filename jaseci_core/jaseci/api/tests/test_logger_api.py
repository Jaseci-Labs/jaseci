from jaseci.utils.log_utils import parse_logs
from jaseci.utils.test_core import CoreTest
from jaseci.utils.utils import logger, app_logger


class LoggerApiTest(CoreTest):
    fixture_src = __file__

    logs = [
        "2022-11-26 21:43:55,354 - ERROR - start: Skipping MailService due to initialization failure!",
        "ConnectionRefusedError: [Errno 61] Connection refused",
    ]

    def test_parse_logs(self):
        parsed_logs = parse_logs(self.logs)

        self.assertEqual(len(parsed_logs), 2)

        self.assertEqual(parsed_logs[0]["level"], "ERROR")
        self.assertEqual(parsed_logs[1]["level"], None)

        self.assertEqual(parsed_logs[0]["date"], "2022-11-26 21:43:55")
        self.assertEqual(parsed_logs[1]["date"], None)

    def test_get_logs(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("test_logging.jac")}],
        )

        logger.warning("hello")
        app_logger.warning("hello")

        ret = self.call(self.smast, ["logger_get_logs", {}])

        print("ret", ret)
