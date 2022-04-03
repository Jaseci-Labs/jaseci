from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper
from jaseci.jsctl import jsctl
from click.testing import CliRunner
import json


class jsctl_test(TestCaseHelper, TestCase):
    """Unit tests for Jac language"""

    def setUp(self):
        super().setUp()

    def call(self, cmd):
        res = CliRunner(mix_stderr=False).invoke(jsctl.jsctl,
                                                 ["-m"]+cmd.split(' '))
        # self.log(res.stdout)
        # self.log(res.stderr)
        # self.log(res.exception)
        return res.stdout

    def call_cast(self, cmd):
        ret = self.call(cmd)
        # self.log(ret)
        return json.loads(ret)

    def call_split(self, cmd):
        ret = self.call(cmd)
        # self.log(ret)
        return ret.split('\n')

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
        self.call(
            "sentinel register "
            "jaseci/jsctl/tests/ll.jac -name ll -set_active true")
        self.assertEqual(len(self.call_cast('graph list')), 1)
        self.call('graph create')
        self.call('graph create')
        self.call('graph create')
        self.assertEqual(len(self.call_cast('graph list')), 4)

    def test_jsctl_carry_forward(self):
        self.call(
            "actions load local ../jskit/infer.py")
        self.call(
            "sentinel register "
            "jaseci/jsctl/tests/ll.jac -name ll -set_active true")
        self.call("graph create -set_active true")
        self.call("walker run init")
        self.call("walker run gen_rand_life")
        r = self.call_cast("walker run get_gen_day")
        self.assertGreater(len(r['report']), 3)

    def test_jsctl_dot(self):
        self.call(
            "sentinel register "
            "jaseci/jsctl/tests/ll.jac -name ll -set_active true")
        self.call("graph create -set_active true")
        self.call("walker run init")
        self.call("walker run gen_rand_life")
        r = self.call("graph get -mode dot")
        self.assertIn("test test test", r)
        self.assertIn('"n0" -> "n', r)
        self.assertIn('week="', r)

    def test_jsctl_aliases(self):
        """Tests that alias mapping api works"""
        self.call(
            "sentinel register "
            "jaseci/jsctl/tests/zsb.jac -name zsb -set_active true")
        gph_id = self.call_cast('graph create')['jid']
        snt_id = self.call_cast('sentinel list')[0]['jid']
        self.call(f'alias register s -value {snt_id}')
        self.call(f'alias register g -value {gph_id}')
        self.assertEqual(len(self.call_cast('graph get -gph g')), 1)
        self.call(f'walker run init -snt s -nd g')
        self.assertEqual(len(self.call_cast('graph get -gph g')), 3)
        self.call(f'alias clear')
        self.assertEqual(len(self.call_cast(f'alias list').keys()), 0)

    def test_jsctl_auto_aliases(self):
        """Tests that auto alias mapping api works"""
        self.call(
            "sentinel register jaseci/jsctl/tests/zsb.jac -name zsb "
            "-set_active true")
        aliases = self.call_cast('alias list')
        self.assertGreater(len(aliases), 20)
        self.assertIn('zsb:architype:bot', aliases.keys())
        self.assertIn('zsb:walker:similar_questions', aliases.keys())
        self.assertIn('sentinel:zsb', aliases.keys())
        self.assertIn('zsb:walker:create_nugget', aliases.keys())

    def test_jsctl_auto_aliases_delete(self):
        """Tests that auto removing alias mapping api works"""
        self.call(
            "sentinel register jaseci/jsctl/tests/zsb.jac -name zsb "
            "-set_active true")
        num = len(self.call_cast('alias list'))

        self.call('architype delete zsb:architype:bot')
        self.call('walker delete zsb:walker:similar_questions')
        self.call('walker delete zsb:walker:create_nugget')
        self.assertEqual(num-3, len(self.call_cast('alias list')))

    def test_jsctl_config_cmds(self):
        """Tests that config commands works"""
        self.call(
            "sentinel register jaseci/jsctl/tests/zsb.jac -name zsb "
            "-set_active true")
        self.call(
            f'config set CONFIG_EXAMPLE -value TEST -do_check False')
        self.call(f'config set APPLE -value Grape2 -do_check False')
        self.call(f'config set "Banana" -value "Grape" -do_check False')
        self.call(f'config set "Pear" -value "Banana" -do_check False')
        r = self.call('config get APPLE -do_check False')
        self.assertEqual(r.strip(), 'Grape2')
        r = self.call_cast('config list')
        self.assertEqual(len(r), 1)

    def test_jsctl_default_snt_setting(self):
        """Tests that alias mapping api works"""
        self.call(
            "sentinel register jaseci/jsctl/tests/teststest.jac -name zsb "
            "-set_active true")
        snt_id = self.call_cast('sentinel list')[0]['jid']
        self.call(f'sentinel active set {snt_id}')
        self.call(f'sentinel active get')
        self.assertEqual(len(self.call_cast(f'walker list')), 2)

    def test_jsctl_init_auto_called(self):
        """Tests that alias mapping api works"""
        num = len(self.call_cast('graph get'))
        self.assertEqual(num, 3)

    def test_jsctl_master_defaults(self):
        """Tests that alias mapping api works"""
        self.call(
            "sentinel register jaseci/jsctl/tests/zsb.jac -name zsb "
            "-set_active true")
        gph_id = self.call_cast('graph create')['jid']
        snt_id = self.call_cast('sentinel list')[0]['jid']
        self.call(f'sentinel active set -snt {snt_id}')
        self.call(f'graph active set -gph {gph_id}')
        self.assertEqual(len(self.call_cast('graph get')), 1)
        self.call(f'walker run init')
        self.assertEqual(len(self.call_cast('graph get')), 3)

    def test_public_apis_present(self):
        r = self.call('walker --help')
        self.assertIn('summon', r)
        self.assertIn('namespace key', r)

    def test_public_apis_walker_summon_auth(self):
        self.call(
            "sentinel register jaseci/jsctl/tests/zsb.jac -name zsb "
            "-set_active true")
        r = self.call_cast('walker get zsb:walker:pubinit -mode keys')
        key = r['anyone']
        r = self.call_cast('alias list')
        walk = r['zsb:walker:pubinit']
        nd = r['active:graph']
        r = self.call_cast(f'walker summon {walk} -key {key} -nd {nd}')
        self.assertEqual(len(r['report']), 0)
        key = 'aaaaaaaa'
        r = self.call_cast(f'walker summon {walk} -key {key} -nd {nd}')
        self.assertFalse(r['success'])

    def test_jsctl_import(self):
        r = self.call(
            "sentinel register "
            "jaseci/jsctl/tests/ll_base.jac -code_dir "
            "jaseci/jsctl/tests -set_active true")
        self.call("walker run init")
        self.call("walker run gen_rand_life")
        r = self.call_cast("walker run get_gen_day")
        self.assertGreater(len(r['report']), 3)

    def test_jsctl_import_filters(self):
        self.call(
            "sentinel register "
            "jaseci/jsctl/tests/base.jac -set_active true")
        r = self.call_cast("walker run init")
        self.assertEqual(len(r['report']), 8)

    def test_jsctl_import_filters1(self):
        self.call(
            "sentinel register "
            "jaseci/jsctl/tests/base1.jac -set_active true")
        r = self.call_cast("walker run init")
        self.assertEqual(len(r['report']), 8)

    def test_jsctl_import_filters2(self):
        self.call(
            "sentinel register "
            "jaseci/jsctl/tests/base2.jac -set_active true")
        r = self.call_cast("walker run init")
        self.assertEqual(len(r['report']), 8)

    def test_jsctl_import_fails_when_incomplete(self):
        self.call(
            "sentinel register "
            "jaseci/jsctl/tests/base3.jac -set_active true")
        r = self.call_cast("walker run init")
        self.assertTrue('success' in r.keys())
        self.assertFalse(r['success'])

    def test_jsctl_run_tests(self):
        self.call(
            "sentinel register "
            "jaseci/jsctl/tests/teststest.jac")
        r = self.call_split("sentinel test")
        self.assertTrue(r[0].startswith('Testing "assert should be'))
        self.assertTrue(r[4].startswith('  "tests": 3'))
        self.assertTrue(r[7].startswith('  "success": true'))

    def test_jsctl_run_tests_detailed(self):
        self.call(
            "sentinel register "
            "jaseci/jsctl/tests/teststest.jac")
        r = self.call_split("sentinel test -detailed true")
        self.assertEqual(len(r), 27)

    def test_jsctl_jac_build(self):
        import os
        if(os.path.exists('jaseci/jsctl/tests/teststest.jir')):
            os.remove('jaseci/jsctl/tests/teststest.jir')
            self.assertFalse(os.path.exists(
                'jaseci/jsctl/tests/teststest.jir'))
        self.call(
            "jac build jaseci/jsctl/tests/teststest.jac")
        self.assertGreater(os.path.getsize(
            'jaseci/jsctl/tests/teststest.jir'), 50000)

    def test_jsctl_jac_test(self):
        r = self.call_split(
            "jac test jaseci/jsctl/tests/teststest.jac")
        self.assertTrue(r[0].startswith('Testing "assert should be'))
        self.assertTrue(r[4].startswith('  "tests": 3'))
        self.assertTrue(r[7].startswith('  "success": true'))

    def test_jsctl_jac_test_jir(self):
        r = self.call_split(
            "jac test jaseci/jsctl/tests/teststest.jir")
        self.assertTrue(r[0].startswith('Testing "assert should be'))
        self.assertTrue(r[4].startswith('  "tests": 3'))
        self.assertTrue(r[7].startswith('  "success": true'))

    def test_jsctl_jac_run(self):
        r = self.call_cast(
            "jac run jaseci/jsctl/tests/teststest.jac")
        self.assertEqual(r['report'], [{}, 4])

    def test_jsctl_jac_run_jir(self):
        r = self.call_cast(
            "jac run jaseci/jsctl/tests/teststest.jir")
        self.assertEqual(r['report'], [{}, 4])

    def test_jsctl_jac_run_jir_walk(self):
        r = self.call_cast(
            "jac run jaseci/jsctl/tests/teststest.jir -walk alt_init")
        self.assertEqual(r['report'], [7])

    def test_jsctl_sentinel_set(self):
        self.call(
            "sentinel register "
            "jaseci/jsctl/tests/teststest.jac -set_active true")
        self.call(
            "sentinel set "
            "jaseci/jsctl/tests/base.jac")
        r = self.call_cast("walker run init")
        r = self.call_cast("walker run init")
        self.assertEqual(len(r['report']), 8)

    def test_jsctl_action_list(self):
        r = self.call_cast(
            "actions list")
        self.assertIn("std.out", r)

    def test_jsctl_master_self(self):
        r = self.call_cast(
            "master self")
        self.assertIn("j_type", r.keys())
        a = r['jid']
        r = self.call_cast(
            "master active get")
        self.assertIn("j_type", r.keys())
        b = r['jid']
        self.assertEqual(a, b)
