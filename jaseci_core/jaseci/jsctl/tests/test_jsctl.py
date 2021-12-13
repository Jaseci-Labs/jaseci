from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper
from jaseci.jsctl import jsctl
from click.testing import CliRunner
import json


class jsctl_test(TestCaseHelper, TestCase):
    """Unit tests for Jac language"""

    def setUp(self):
        super().setUp()
        self.call(
            "sentinel register -name zsb -code "
            "jaseci/jsctl/tests/zsb.jac -set_active true")

    def call(self, cmd):
        res = CliRunner(mix_stderr=False).invoke(jsctl.cli,
                                                 ["-m"]+cmd.split(' '))
        out = res.stdout
        self.log(out)
        self.log(res.stderr)
        return out

    def call_cast(self, cmd):
        ret = self.call(cmd)
        self.log(ret)
        self.log(type(ret))
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
        self.assertIn("Group of `sentinel active` commands", r)

    def test_jsctl_create_graph_mem_only(self):
        self.assertEqual(len(self.call_cast('graph list')), 1)
        self.call('graph create')
        self.call('graph create')
        self.call('graph create')
        self.assertEqual(len(self.call_cast('graph list')), 4)

    def test_jsctl_carry_forward(self):
        self.call(
            "sentinel register -name ll -code "
            "jaseci/jsctl/tests/ll.jac -set_active true")
        self.call("graph create -set_active true")
        self.call("walker run -name init")
        self.call("walker run -name gen_rand_life")
        r = self.call_cast("walker run -name get_gen_day")
        self.assertGreater(len(r), 3)

    def test_jsctl_dot(self):
        self.call(
            "sentinel register -name ll -code "
            "jaseci/jsctl/tests/ll.jac -set_active true")
        self.call("graph create -set_active true")
        self.call("walker run -name init")
        self.call("walker run -name gen_rand_life")
        r = self.call("graph get -mode dot")
        self.assertIn("test test test", r)
        self.assertIn('"n0" -> "n', r)
        self.assertIn('week="', r)

    def test_jsctl_aliases(self):
        """Tests that alias mapping api works"""
        gph_id = self.call_cast('graph create')['jid']
        snt_id = self.call_cast('sentinel list')[0]['jid']
        self.call(f'alias register -name s -value {snt_id}')
        self.call(f'alias register -name g -value {gph_id}')
        self.assertEqual(len(self.call_cast('graph get -gph g')), 1)
        self.call(f'walker run -snt s -nd g -name init')
        self.assertEqual(len(self.call_cast('graph get -gph g')), 3)
        self.call(f'alias clear')
        self.assertEqual(len(self.call_cast(f'alias list').keys()), 0)

    def test_jsctl_auto_aliases(self):
        """Tests that auto alias mapping api works"""
        aliases = self.call_cast('alias list')
        self.assertGreater(len(aliases), 20)
        self.assertIn('zsb:architype:bot', aliases.keys())
        self.assertIn('zsb:walker:similar_questions', aliases.keys())
        self.assertIn('sentinel:zsb', aliases.keys())
        self.assertIn('zsb:walker:create_nugget', aliases.keys())

    def test_jsctl_auto_aliases_delete(self):
        """Tests that auto removing alias mapping api works"""
        num = len(self.call_cast('alias list'))
        self.call('architype delete -arch zsb:architype:bot')
        self.call('walker delete -wlk zsb:walker:similar_questions')
        self.call('walker delete -wlk zsb:walker:create_nugget')
        self.assertEqual(num-3, len(self.call_cast('alias list')))

    def test_jsctl_config_cmds(self):
        """Tests that config commands works"""
        self.call(
            f'config set -name CONFIG_EXAMPLE -value TEST -do_check False')
        self.call(f'config set -name APPLE -value Grape2 -do_check False')
        self.call(f'config set -name "Banana" -value "Grape" -do_check False')
        self.call(f'config set -name "Pear" -value "Banana" -do_check False')
        r = self.call('config get -name APPLE -do_check False')
        self.assertEqual(r.strip(), 'Grape2')
        r = self.call_cast('config list')
        self.assertEqual(len(r), 1)

    def test_jsctl_default_snt_setting(self):
        """Tests that alias mapping api works"""
        snt_id = self.call_cast('sentinel list')[0]['jid']
        self.call(f'sentinel active set -snt {snt_id}')
        self.call(f'sentinel active get')
        self.assertEqual(len(self.call_cast(f'walker list')), 22)

    def test_jsctl_init_auto_called(self):
        """Tests that alias mapping api works"""
        num = len(self.call_cast('graph get'))
        self.assertEqual(num, 3)

    def test_jsctl_master_defaults(self):
        """Tests that alias mapping api works"""
        gph_id = self.call_cast('graph create')['jid']
        snt_id = self.call_cast('sentinel list')[0]['jid']
        self.call(f'sentinel active set -snt {snt_id}')
        self.call(f'graph active set -gph {gph_id}')
        self.assertEqual(len(self.call_cast('graph get')), 1)
        self.call(f'walker run -name init')
        self.assertEqual(len(self.call_cast('graph get')), 3)

    def test_public_apis_present(self):
        r = self.call('walker --help')
        self.assertIn('summon', r)
        self.assertIn('namespace key', r)

    def test_public_apis_walker_summon_auth(self):
        r = self.call_cast('walker get -mode keys -wlk zsb:walker:pubinit')
        key = list(r.keys())[0]
        r = self.call_cast('alias list')
        walk = r['zsb:walker:pubinit']
        nd = r['active:graph']
        r = self.call_cast(f'walker summon -key {key} -wlk {walk} -nd {nd}')
        self.assertEqual(len(r), 0)
        key = 'aaaaaaaa'
        r = self.call_cast(f'walker summon -key {key} -wlk {walk} -nd {nd}')
        self.assertEqual(len(r), 1)

    def test_jsctl_import(self):
        self.call(
            "sentinel register -code "
            "jaseci/jsctl/tests/ll_base.jac -set_active true")
        self.call("walker run -name init")
        self.call("walker run -name gen_rand_life")
        r = self.call_cast("walker run -name get_gen_day")
        self.assertGreater(len(r), 3)
