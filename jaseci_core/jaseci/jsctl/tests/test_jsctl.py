import sys
import io
from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper
from jaseci.jsctl import jsctl
from click.testing import CliRunner


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

    def test_jsctl_extract_tree(self):
        self.logger_on()
        out = jsctl.extract_api_tree()
        self.assertIn("create", out)
        self.assertIn("get", out)
        self.assertIn("load", out)
        self.assertIn("set", out)
        self.assertNotIn("jadc", out)

    def test_help_screen(self):
        runner = CliRunner()
        result = runner.invoke(jsctl.cli, ['--help'])
        self.assertIn('Specify filename', result.output)
        self.assertIn("Group of `list` commands", result.output)
        result = runner.invoke(jsctl.cli, ['get', 'graph', '--help'])
        self.assertIn("Group of `get graph` commands", result.output)

    def test_jsctl_create_graph_mem_only(self):
        runner = CliRunner()
        result = runner.invoke(
            jsctl.cli, ['-m', 'create', 'graph', '-name', 'test'])
        self.assertIn('test', result.output)
        result = runner.invoke(jsctl.cli, ['-m', 'list', 'graphs'])
        self.assertIn('test', result.output)
