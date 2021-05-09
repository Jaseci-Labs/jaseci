from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper
from jaseci.jsctl import jsctl
from click.testing import CliRunner


class jsctl_test(TestCaseHelper, TestCase):
    """Unit tests for Jac language"""

    def setUp(self):
        super().setUp()
        self.call("load app -name zsb -code jsctl/tests/zsb.jac")

    def call(self, cmd):
        runner = CliRunner()
        return runner.invoke(jsctl.cli,
                             ["-m"]+cmd.split(' ')).output

    def tearDown(self):
        jsctl.session["master"]._h.mem = {}
        super().tearDown()

    def test_jsctl_extract_tree(self):
        self.logger_on()
        out = jsctl.extract_api_tree()
        self.assertIn("create", out)
        self.assertIn("get", out)
        self.assertIn("load", out)
        self.assertIn("set", out)
        self.assertNotIn("jadc", out)

    def test_help_screen(self):
        r = self.call('--help')
        self.assertIn('Specify filename', r)
        self.assertIn("Group of `list` commands", r)
        r = self.call('get --help')
        self.assertIn("Group of `get node` commands", r)

    def test_jsctl_create_graph_mem_only(self):
        r = self.call('create graph -name test')
        self.assertIn('test', r)
        r = self.call('list graphs')
        self.assertIn('test', r)

    def test_jsctl_load_app(self):
        r = self.call('list graphs')
        self.assertIn('zsb', r)
