from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper
from jaseci.cli_tools import jsctl
from click.testing import CliRunner
import json
import os

from jaseci.jsorc.jsorc import JsOrc
from jaseci.extens.svc.redis_svc import RedisService


class JsctlTest(TestCaseHelper, TestCase):
    """Unit tests for Jac language"""

    infer_loc = (
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + "/tests/infer.py"
    )

    def setUp(self):
        super().setUp()
        JsOrc.svc("redis", RedisService).clear()

    def call(self, cmd: str):
        res = CliRunner(mix_stderr=False).invoke(jsctl.jsctl, ["-m"] + cmd.split())
        # self.log(res.stdout)
        # self.log(res.stderr)
        # self.log(res.exception)
        return res.stdout

    def jac_call(self, cmd: str):
        res = CliRunner(mix_stderr=False).invoke(jsctl.jac, cmd.split())
        return res.stdout

    def call_cast(self, cmd):
        ret = self.call(cmd)
        # self.log(ret)
        return json.loads(ret)

    def jac_call_cast(self, cmd):
        ret = self.jac_call(cmd)
        # self.log(ret)
        return json.loads(ret)

    def call_split(self, cmd):
        ret = self.call(cmd)
        # self.log(ret)
        return ret.split("\n")

    def jac_call_split(self, cmd):
        ret = self.jac_call(cmd)
        return ret.split("\n")

    def tearDown(self):
        jsctl.reset_state()
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
        r = self.call("--help")
        self.assertIn("Specify filename", r)
        self.assertIn("Group of `graph` commands", r)
        r = self.call("sentinel --help")
        self.assertIn("Group of `sentinel active` commands", r)

    def test_jsctl_create_graph_mem_only(self):
        ret = self.call(
            f"sentinel register {os.path.dirname(__file__)}/ll.jac -name ll -set_active true"
        )
        self.assertEqual(len(self.call_cast("graph list")), 1)
        self.call("graph create")
        self.call("graph create")
        self.call("graph create")
        self.assertEqual(len(self.call_cast("graph list")), 4)

    def test_jsctl_carry_forward(self):
        ret = self.call(f"actions load local {self.infer_loc}")
        ret = self.call(
            f"sentinel register {os.path.dirname(__file__)}/ll.jac -name ll -set_active true"
        )
        r = self.call("graph create -set_active true")
        r = self.call("walker run init")
        r = self.call("walker run gen_rand_life")
        r = self.call_cast("walker run get_gen_day")
        self.assertGreater(len(r["report"]), 3)

    def test_jsctl_dot(self):
        self.call(
            f"sentinel register {os.path.dirname(__file__)}/ll.jac -name ll -set_active true"
        )
        self.call("walker run init")
        self.call("walker run gen_rand_life")
        r = self.call("graph get -mode dot")
        self.assertIn('"n0" -> "n', r)
        self.assertNotIn('week="', r)

        r = self.call("graph get -mode dot -detailed true")
        self.assertIn('"n0" -> "n', r)
        self.assertIn('id="', r)

    def test_jsctl_aliases(self):
        """Tests that alias mapping api works"""
        self.call(
            f"sentinel register {os.path.dirname(__file__)}/zsb.jac -name zsb -set_active true"
        )
        gph_id = self.call_cast("graph create")["jid"]
        snt_id = self.call_cast("sentinel list")[0]["jid"]
        self.call(f"alias register s -value {snt_id}")
        self.call(f"alias register g -value {gph_id}")
        self.assertEqual(len(self.call_cast("graph get -nd g")), 1)
        self.call("walker run init -snt s -nd g")
        self.assertEqual(len(self.call_cast("graph get -nd g")), 3)
        self.call("alias clear")
        self.assertEqual(len(self.call_cast("alias list").keys()), 0)

    def test_jsctl_auto_aliases(self):
        """Tests that auto alias mapping api works"""
        self.call(
            f"sentinel register {os.path.dirname(__file__)}/zsb.jac -name zsb -set_active true"
        )
        aliases = self.call_cast("alias list")
        self.assertGreater(len(aliases), 20)
        self.assertIn("zsb:architype:bot", aliases.keys())
        self.assertIn("zsb:walker:similar_questions", aliases.keys())
        self.assertIn("sentinel:zsb", aliases.keys())
        self.assertIn("zsb:walker:create_nugget", aliases.keys())

    def test_jsctl_auto_aliases_delete(self):
        """Tests that auto removing alias mapping api works"""
        self.call(
            f"sentinel register {os.path.dirname(__file__)}/zsb.jac -name zsb -set_active true"
        )

        num = len(self.call_cast("alias list"))

        self.call("architype delete zsb:architype:bot")
        self.call("architype delete zsb:walker:similar_questions")
        self.call("architype delete zsb:walker:create_nugget")
        self.assertEqual(num - 3, len(self.call_cast("alias list")))

    def test_jsctl_config_cmds(self):
        """Tests that config commands works"""
        self.call(
            f"sentinel register {os.path.dirname(__file__)}/zsb.jac -name zsb -set_active true"
        )
        self.call('config set CONFIG_EXAMPLE -value "TEST" -do_check False')
        self.call("config set APPLE -value Grape2 -do_check False")
        self.call("config set APPLE_JSON -value '{\"test\":true}' -do_check False")
        self.call('config set "Banana" -value "Grape" -do_check False')
        self.call('config set "Pear" -value "Banana" -do_check False')
        r = self.call("config get APPLE -do_check False")
        self.assertEqual(r.strip(), "Grape2")
        r = self.call_cast("config list")

        self.assertEqual(len(r), 1)

    def test_jsctl_default_snt_setting(self):
        """Tests that alias mapping api works"""
        self.call(
            f"sentinel register {os.path.dirname(__file__)}/teststest.jac -name zsb "
            "-set_active true"
        )
        snt_id = self.call_cast("sentinel list")[0]["jid"]
        self.call(f"sentinel active set {snt_id}")
        self.call("sentinel active get")
        self.assertEqual(len(self.call_cast("walker list")), 2)

    def test_jsctl_init_auto_called(self):
        """Tests that alias mapping api works"""
        num = len(self.call_cast("graph get"))
        self.assertEqual(num, 3)

    def test_jsctl_master_defaults(self):
        """Tests that alias mapping api works"""
        self.call(
            f"sentinel register {os.path.dirname(__file__)}/zsb.jac -name zsb -set_active true"
        )
        gph_id = self.call_cast("graph create")["jid"]
        snt_id = self.call_cast("sentinel list")[0]["jid"]
        self.call(f"sentinel active set -snt {snt_id}")
        self.call(f"graph active set -gph {gph_id}")
        self.assertEqual(len(self.call_cast("graph get")), 1)
        self.call("walker run init")
        self.assertEqual(len(self.call_cast("graph get")), 3)

    def test_public_apis_present(self):
        r = self.call("walker --help")
        self.assertIn("summon", r)
        self.assertIn("namespace key", r)

    def test_public_apis_walker_summon_auth(self):
        self.call(
            f"sentinel register {os.path.dirname(__file__)}/zsb.jac -name zsb -set_active true"
        )
        wjid = self.call_cast("walker spawn create pubinit")["jid"]
        r = self.call_cast(f"walker get {wjid} -mode keys")
        key = r["anyone"]
        r = self.call_cast("alias list")
        nd = r["active:graph"]
        r = self.call_cast(f"walker summon {wjid} -key {key} -nd {nd}")
        self.assertEqual(len(r["report"]), 0)
        key = "aaaaaaaa"
        r = self.call_cast(f"walker summon {wjid} -key {key} -nd {nd}")
        self.assertFalse(r["success"])

    def test_jsctl_import(self):
        self.call(f"actions load local {self.infer_loc}")
        r = self.call_cast(
            f"sentinel register "
            f"{os.path.dirname(__file__)}/ll_base.jac -code_dir "
            f"{os.path.dirname(__file__)} -set_active true"
        )
        r = self.call_cast("walker run init")
        r = self.call_cast("walker run gen_rand_life")
        r = self.call_cast("walker run get_gen_day")
        self.assertGreater(len(r["report"]), 3)

    def test_jsctl_import_filters(self):
        self.call_cast(
            f"sentinel register {os.path.dirname(__file__)}/base.jac -set_active true"
        )
        r = self.call_cast("walker run init")
        self.assertEqual(len(r["report"]), 8)

    def test_jsctl_import_filters1(self):
        self.call(
            f"sentinel register {os.path.dirname(__file__)}/base1.jac -set_active true"
        )
        r = self.call_cast("walker run init")
        self.assertEqual(len(r["report"]), 8)

    def test_jsctl_import_filters2(self):
        self.call(
            f"sentinel register {os.path.dirname(__file__)}/base2.jac -set_active true"
        )
        r = self.call_cast("walker run init")
        self.assertEqual(len(r["report"]), 8)

    def test_jsctl_import_fails_when_incomplete(self):
        self.call(
            f"sentinel register {os.path.dirname(__file__)}/base3.jac -set_active true"
        )
        r = self.call_cast("walker run init")
        self.assertTrue("success" in r.keys())
        self.assertFalse(r["success"])

    def test_jsctl_import_globals(self):
        self.call(
            f"sentinel register "
            f"{os.path.dirname(__file__)}/base4.jac -code_dir {os.path.dirname(__file__)}/ "
            f"-set_active true"
        )
        r = self.call_cast("walker run init")
        self.assertEqual(len(r["report"]), 8)

    def test_jsctl_import_recursive(self):
        self.call(
            "sentinel register "
            f"{os.path.dirname(__file__)}/base5.jac -code_dir {os.path.dirname(__file__)}/ "
            "-set_active true"
        )
        r = self.call_cast("walker run init")
        self.assertEqual(r["report"][0], "plain")

    def test_jsctl_import_path(self):
        self.call(
            "sentinel register "
            f"{os.path.dirname(__file__)}/base6.jac -code_dir {os.path.dirname(__file__)}/ "
            "-set_active true"
        )
        r = self.call_cast("walker run init")
        self.assertEqual(r["report"][0], "plain")

    def test_jsctl_run_tests(self):
        self.call(f"sentinel register {os.path.dirname(__file__)}/teststest.jac")
        r = self.call_split("sentinel test")
        self.assertTrue(r[0].startswith("Testing assert should be"))
        self.assertTrue(r[4].startswith('  "tests": 3'))
        self.assertTrue(r[7].startswith('  "success": true'))

    def test_jsctl_run_tests_detailed(self):
        self.call(f"sentinel register {os.path.dirname(__file__)}/teststest.jac")
        r = self.call_split("sentinel test -detailed true")
        self.assertEqual(len(r), 33)

    def test_jsctl_multiple_registers_with_globals(self):
        r = self.call_cast(
            f"sentinel register {os.path.dirname(__file__)}/teststest.jir -mode ir"
        )
        r = self.call_cast(
            f"sentinel register {os.path.dirname(__file__)}/teststest.jir -mode ir"
        )
        self.assertEqual(len(r), 1)

    def test_jsctl_run_tests_with_stdout(self):
        self.call(f"sentinel register {os.path.dirname(__file__)}/teststest_stdout.jac")
        r = self.call("sentinel test -detailed true")
        self.assertIn('"stdout": "Some Output\\nSome Output\\n"', r)
        r = r.replace('"stdout": "Some Output\\nSome Output\\n"', "")
        self.assertNotIn("Some Output", r)

    def test_jsctl_jac_build(self):
        if os.path.exists(f"{os.path.dirname(__file__)}/teststest.jir"):
            os.remove(f"{os.path.dirname(__file__)}/teststest.jir")
            self.assertFalse(
                os.path.exists(f"{os.path.dirname(__file__)}/teststest.jir")
            )
        self.call(f"jac build {os.path.dirname(__file__)}/teststest.jac")
        self.assertGreater(
            os.path.getsize(f"{os.path.dirname(__file__)}/teststest.jir"), 20000
        )

    def test_jsctl_jac_build_with_action(self):
        if os.path.exists(f"{os.path.dirname(__file__)}/withaction.jir"):
            os.remove(f"{os.path.dirname(__file__)}/withaction.jir")
            self.assertFalse(
                os.path.exists(f"{os.path.dirname(__file__)}/withaction.jir")
            )
        self.call(f"jac build {os.path.dirname(__file__)}/withaction.jac")
        self.assertGreater(
            os.path.getsize(f"{os.path.dirname(__file__)}/withaction.jir"), 1000
        )
        os.remove(f"{os.path.dirname(__file__)}/withaction.jir")

    def test_jsctl_jac_test(self):
        r = self.call_split(f"jac test {os.path.dirname(__file__)}/teststest.jac")
        self.assertTrue(r[0].startswith("Testing assert should be"))
        self.assertTrue(r[4].startswith('  "tests": 3'))
        self.assertTrue(r[7].startswith('  "success": true'))

    def test_jsctl_jac_test_single(self):
        r = self.call_split(
            f"jac test {os.path.dirname(__file__)}/teststest.jac -single the_second"
        )
        self.log(r)
        self.assertTrue(r[0].startswith("Testing a second test"))
        self.assertTrue(r[2].startswith('  "tests": 1'))
        self.assertTrue(r[5].startswith('  "success": true'))

    def test_jsctl_jac_test_jir(self):
        r = self.call_split(f"jac test {os.path.dirname(__file__)}/teststest.jir")
        self.assertTrue(r[0].startswith("Testing assert should be"))
        self.assertTrue(r[4].startswith('  "tests": 3'))
        self.assertTrue(r[7].startswith('  "success": true'))

    def test_jac_long_str_build(self):
        r = self.jac_call_cast(f"run {os.path.dirname(__file__)}/longstring.jac")
        self.assertTrue(
            r["report"][0].startswith("Lorem Ipsum is simply dummy text of the")
        )
        self.assertTrue(
            r["report"][0].endswith(
                "Aldus PageMaker including versions of Lorem Ipsum."
            )
        )

    def test_jac_cli_test(self):
        r = self.jac_call_split(f"test {os.path.dirname(__file__)}/teststest.jir")
        self.assertTrue(r[0].startswith("Testing assert should be"))
        self.assertTrue(r[4].startswith('  "tests": 3'))
        self.assertTrue(r[7].startswith('  "success": true'))

    def test_jsctl_jac_disas_jir(self):
        r = self.call(f"jac disas {os.path.dirname(__file__)}/teststest.jir")
        self.assertIn("LOAD_CONST", r)
        self.assertIn("LOAD_VAR", r)

    def test_jsctl_jac_run(self):
        r = self.call_cast(f"jac run {os.path.dirname(__file__)}/teststest.jac")
        self.assertEqual(r["report"], [{}, 4])

    def test_jsctl_jac_run_jir(self):
        r = self.call_cast(f"jac run {os.path.dirname(__file__)}/teststest.jir")
        self.assertEqual(r["report"], [{}, 4])

    def test_jsctl_jac_dot_jir(self):
        r = self.call(f"jac dot {os.path.dirname(__file__)}/teststest.jir")
        self.assertEqual(r, 'strict digraph root {\n    "n0" [ label="n0:root"  ]\n}\n')

    def test_jsctl_jac_run_jir_walk(self):
        r = self.call_cast(
            f"jac run {os.path.dirname(__file__)}/teststest.jir -walk alt_init"
        )
        self.assertEqual(r["report"], [7])

    def test_jsctl_sentinel_set(self):
        self.call(
            f"sentinel register {os.path.dirname(__file__)}/teststest.jac -set_active true"
        )
        self.call(f"sentinel set {os.path.dirname(__file__)}/base.jac")
        r = self.call_cast("walker run init")
        r = self.call_cast("walker run init")
        self.assertEqual(len(r["report"]), 8)

    def test_jsctl_action_list(self):
        r = self.call_cast("actions list")
        self.assertIn("std.out", r)

    def test_jsctl_master_self(self):
        r = self.call_cast("master self")
        self.assertIn("j_type", r.keys())
        a = r["jid"]
        r = self.call_cast("master active get")
        self.assertIn("j_type", r.keys())
        b = r["jid"]
        self.assertEqual(a, b)

    def test_jsctl_graph_can(self):
        self.call(f"actions load local {self.infer_loc}")
        r = self.call(
            f"sentinel register "
            f"{os.path.dirname(__file__)}/graph_can.jac -name gc -set_active true"
        )
        r = self.call("walker run go1")
        self.assertEqual(r.split()[0], "2020-01-01T00:00:00")
        r = self.call("walker run go2")
        self.assertEqual(r.split()[0], "2020-07-01T00:00:00")
        r = self.call("walker run go3")
        self.assertEqual(r.split()[0], "2020-01-01T00:00:00")
        self.assertEqual(r.split()[1], "2020-07-01T00:00:00")
        self.assertEqual(r.split()[2], "2020-07-10T00:00:00")

    def test_jsctl_action_call(self):
        self.call(f"actions load local {self.infer_loc}")
        r = self.call(f"actions call infer.date_now")
        r = json.loads(r)
        import datetime

        date_now = datetime.datetime.utcnow().date().isoformat()
        self.assertEqual(r["result"], date_now)

    def test_jsctl_custom_report(self):
        self.call(
            f"sentinel register {os.path.dirname(__file__)}/glob_imp.jac -set_active true"
        )
        r = self.call_cast("walker run cust_report")
        self.assertEqual(r, {"a": "b"})

    def test_jsctl_custom_report_off(self):
        self.call(
            f"sentinel register {os.path.dirname(__file__)}/glob_imp.jac -set_active true"
        )
        r = self.call_cast("walker run cust_report_neutralize")
        self.assertIn("success", r.keys())

    def test_jsctl_disengage_report(self):
        self.call(
            f"sentinel register {os.path.dirname(__file__)}/glob_imp.jac -set_active true"
        )
        r = self.call_cast("walker run disengage_report")
        self.assertEqual(r, {"a": "b"})

    def test_jsctl_set_global_default_perms(self):
        self.call("object perms default public")
        self.call(
            f"sentinel register {os.path.dirname(__file__)}/zsb.jac -name zsb -set_active true"
        )
        gphs = self.call_cast("graph get -detailed true")
        for i in gphs:
            self.assertEqual(i["j_access"], "public")

    def test_jsctl_bookgen_api_cheatsheet(self):
        r = self.call("booktool cheatsheet")
        self.assertGreater(len(r), 2000)

    def test_jsctl_bookgen_std_library(self):
        r = self.call("booktool stdlib")
        self.assertGreater(len(r), 2000)

    def test_jsctl_bookgen_api_spec(self):
        r = self.call("booktool cheatsheet")
        self.assertGreater(len(r), 2000)

    def test_jsctl_print_detailed_sentinel(self):
        r = self.call_cast(
            f"sentinel register {os.path.dirname(__file__)}/teststest.jir -name test -mode ir"
        )
        r = self.call_cast("object get sentinel:test")
        before = len(r.keys())
        r = self.call_cast("object get sentinel:test -detailed true")
        after = len(r.keys())
        self.assertGreater(before, 4)
        self.assertGreater(after, before)

    def test_jsctl_script(self):
        r = self.call(f"script {os.path.dirname(__file__)}/jsctl_script")
        self.assertEqual(r, "[]\n\n[]\n\n{}\n\n")

    def test_jsctl_script_output(self):
        self.call(f"script {os.path.dirname(__file__)}/jsctl_script -o scr_out")
        with open("scr_out", "r") as f:
            s = [line.rstrip() for line in f]
        if os.path.exists("scr_out"):
            os.remove("scr_out")
        self.assertEqual(
            s,
            [
                "Multi Command Script Output:",
                "Output for sentinel list:",
                "[]",
                "Output for graph list:",
                "[]",
                "Output for alias list:",
                "{}",
            ],
        )

    def test_jsctl_pretty_profiles(self):
        self.call(f"actions load local {self.infer_loc}")
        r = self.call(
            f"sentinel register "
            f"{os.path.dirname(__file__)}/graph_can.jac -name gc -set_active true"
        )
        r = self.call("walker run go1 -profiling true")
        self.assertIn("walker::go1", r)
        self.assertIn("cumtime", r)
        self.assertIn("cum_time", r)


class JsctlTestWithSession(TestCaseHelper, TestCase):
    """Unit tests for Jac language"""

    def setUp(self):
        super().setUp()

    def call(self, cmd):
        ses = " -f {os.path.dirname(__file__)}/js.session "
        res = CliRunner(mix_stderr=False).invoke(jsctl.jsctl, (ses + cmd).split())
        return res.stdout

    def call_cast(self, cmd):
        ret = self.call(cmd)
        return json.loads(ret)

    def call_split(self, cmd):
        ret = self.call(cmd)
        return ret.split("\n")

    def tearDown(self):
        if os.path.exists(f"{os.path.dirname(__file__)}/js.session"):
            os.remove(f"{os.path.dirname(__file__)}/js.session")
        jsctl.reset_state()
        super().tearDown()

    def test_jsctl_register_with_session(self):
        self.call(f"sentinel register {os.path.dirname(__file__)}/teststest.jac")
        self.call(f"sentinel register {os.path.dirname(__file__)}/teststest.jac")
        r = self.call_cast("object get active:sentinel -detailed true")
        self.assertGreater(len(r["arch_ids"]), 3)
