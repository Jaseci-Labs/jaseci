import sys
import io
from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper
from jaseci.jsctl import jsctl


class jsctl_test(TestCaseHelper, TestCase):
    """Unit tests for Jac language"""

    def setUp(self):
        super().setUp()
        self.old_stdout = sys.stdout
        self.new_stdout = io.StringIO()
        sys.stdout = self.new_stdout

    def tearDown(self):
        sys.stdout = self.old_stdout
        super().tearDown()

    def to_screen(self):
        sys.stdout = self.old_stdout
        print("output: ", self.new_stdout.getvalue())
        sys.stdout = self.new_stdout

    def test_jsctl_main(self):
        self.logger_on()
        out = jsctl.extract_api_tree()
        self.assertIn("create", out)
        self.assertIn("get", out)
        self.assertIn("load", out)
        self.assertIn("set", out)
        self.assertNotIn("jac", out)
