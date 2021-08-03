from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper
from jaseci.jsctl import jsctl
from click.testing import CliRunner
import json


class jsctl_test(TestCaseHelper, TestCase):
    """Unit tests for Jac language"""

    def setUp(self):
        super().setUp()
        self.call("sentinel create -name zsb -code jaseci/jsctl/tests/zsb.jac")

    def call(self, cmd):
        out = CliRunner().invoke(jsctl.cli,
                                 ["-m"]+cmd.split(' ')).output
        self.log(out)
        return out

    def call_cast(self, cmd):
        ret = self.call(cmd)
        self.log(ret)
        return json.loads(ret)

    def tearDown(self):
        jsctl.session["master"]._h.clear_mem_cache()
        super().tearDown()

    def test_jsctl_extract_tree(self):
        out = jsctl.extract_api_tree()
        self.assertIn("graph", out)
        self.assertIn("walker", out)
        self.assertIn("sentinel", out)
        self.assertIn("alias", out)
        self.assertIn("config", out)
        self.assertNotIn("jadc", out)

    def test_help_screen(self):
        r = self.call('--help')
        self.assertIn('Specify filename', r)
        self.assertIn("Group of `graph` commands", r)
        r = self.call('sentinel --help')
        self.assertIn("Group of `sentinel code` commands", r)

    def test_jsctl_create_graph_mem_only(self):
        self.assertEqual(len(self.call_cast('graph list')), 0)
        self.call('graph create')
        self.call('graph create')
        self.call('graph create')
        self.assertEqual(len(self.call_cast('graph list')), 3)

    def test_jsctl_carry_forward(self):
        self.call("sentinel create -name ll -set_active true")
        self.call("sentinel code set -code jaseci/jsctl/tests/ll.jac")
        self.call("graph create -set_active true")
        self.call("walker primerun -name init")
        self.call("walker primerun -name gen_rand_life")
        r = self.call_cast("walker primerun -name get_gen_day")
        self.assertGreater(len(r), 3)

    def test_jsctl_dot(self):
        self.call("sentinel create -name ll -set_active true")
        self.call("sentinel code set -code jaseci/jsctl/tests/ll.jac")
        self.call("graph create -set_active true")
        self.call("walker primerun -name init")
        self.call("walker primerun -name gen_rand_life")
        r = self.call("graph get -dot true")
        self.assertIn("test test test", r)
        self.assertIn('"n0" -> "n', r)
        self.assertIn('week="', r)

    def test_jsctl_aliases(self):
        """Tests that alias mapping api works"""
        gph_id = self.call_cast('graph create')['jid']
        snt_id = self.call_cast('sentinel list')[0]['jid']
        self.call(f'alias create -name s -value {snt_id}')
        self.call(f'alias create -name g -value {gph_id}')
        self.assertEqual(len(self.call_cast('graph get -gph g')), 1)
        self.call(f'walker primerun -snt s -nd g -name init')
        self.assertEqual(len(self.call_cast('graph get -gph g')), 2)
        self.call(f'alias delete -all true')
        self.assertEqual(len(self.call_cast(f'alias list').keys()), 0)

    def test_jsctl_config_cmds(self):
        """Tests that config commands works"""
        self.call(f'config set -name APPLE -value TEST -do_check False')
        self.call(f'config set -name APPLE -value Grape2 -do_check False')
        self.call(f'config set -name "Banana" -value "Grape" -do_check False')
        self.call(f'config set -name "Pear" -value "Banana" -do_check False')
        r = self.call('config get -name APPLE')
        self.assertEqual(r.strip(), 'Grape2')
        r = self.call_cast('config list')
        self.assertEqual(len(r), 3)

    def test_jsctl_default_snt_setting(self):
        """Tests that alias mapping api works"""
        snt_id = self.call_cast('sentinel list')[0]['jid']
        self.call(f'sentinel active set -snt {snt_id}')
        self.call(f'sentinel active get')
        self.assertEqual(len(self.call_cast(f'walker list')), 21)

    def test_jsctl_master_defaults(self):
        """Tests that alias mapping api works"""
        gph_id = self.call_cast('graph create')['jid']
        snt_id = self.call_cast('sentinel list')[0]['jid']
        self.call(f'sentinel active set -snt {snt_id}')
        self.call(f'graph active set -gph {gph_id}')
        self.assertEqual(len(self.call_cast('graph get')), 1)
        self.call(f'walker primerun -name init')
        self.assertEqual(len(self.call_cast('graph get')), 2)
