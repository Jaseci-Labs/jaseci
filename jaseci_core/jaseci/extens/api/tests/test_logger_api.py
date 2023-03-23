from jaseci.utils.log_utils import LimitedSlidingBuffer, parse_logs
from jaseci.utils.test_core import CoreTest


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
        self.logger_on()
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("test_logging.jac")}],
        )
        self.logger_off()

        ret = self.call(self.smast, ["logger_get", {}])
        self.assertGreaterEqual(len(ret), 1)
        self.assertTrue(ret[-1]["log"].endswith("Hello world!"))

    def test_limited_sliding_buffer(self):
        buffer = LimitedSlidingBuffer(max_size=25)
        buffer.write("Hello world!")
        buffer.write("Hi there!")
        buffer.write("Hello world!")
        buffer.write("Hi there!")
        self.assertEqual(buffer.getvalue(), "ere!Hello world!Hi there!")
        self.assertEqual(buffer.current_size, 25)
