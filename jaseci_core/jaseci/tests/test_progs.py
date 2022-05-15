from jaseci.utils.mem_hook import mem_hook
from jaseci.actor.sentinel import sentinel
from jaseci.graph.graph import graph
from jaseci.element.super_master import super_master
from jaseci.element.master import master
from jaseci.utils.utils import TestCaseHelper
from unittest import TestCase
import jaseci.tests.jac_test_progs as jtp


class jac_tests(TestCaseHelper, TestCase):
    """Unit tests for Jac language"""

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_bug_check1(self):
        gph = graph(m_id="anon", h=mem_hook())
        sent = sentinel(m_id="anon", h=gph._h)
        sent.register_code(jtp.bug_check1)
        test_walker = sent.walker_ids.get_obj_by_name("init")
        test_walker.prime(gph)
        test_walker.run()
        report = test_walker.report
        self.assertEqual(report[0][0], "THIS IS AN INTENT_LABEL")

    def test_action_load_std_lib(self):
        mast = super_master(h=mem_hook())
        mast.sentinel_register(name="test", code=jtp.action_load_std_lib)
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "aload"}
        )["report"]
        self.assertEqual(report[0], True)

    def test_action_load_std_lib_only_super(self):
        mast = master(h=mem_hook())
        mast.sentinel_register(name="test", code=jtp.action_load_std_lib)
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "aload"}
        )
        report = report["report"]
        self.assertEqual(report[0], False)

    def test_globals(self):
        gph = graph(m_id="anon", h=mem_hook())
        sent = sentinel(m_id="anon", h=gph._h)
        sent.register_code(jtp.globals)
        test_walker = sent.walker_ids.get_obj_by_name("init")
        test_walker.prime(gph)
        test_walker.run()
        report = test_walker.report
        self.assertEqual(report, ["testing", 56])

    def test_net_root_std_lib(self):
        mast = master(h=mem_hook())
        mast.sentinel_register(name="test", code=jtp.net_root_std_lib)
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertEqual(report[0][0], report[0][1])
        self.assertEqual(report[0][1], report[1][1])
        self.assertNotEqual(report[1][0], report[1][1])

    def test_or_stmt(self):
        mast = master(h=mem_hook())
        mast.sentinel_register(name="test", code=jtp.or_stmt)
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertEqual(report, [[3.4, "Hello"]])

    def test_nd_equals(self):
        mast = master(h=mem_hook())
        mast.sentinel_register(name="test", code=jtp.nd_equals_error_correct_line)
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )
        self.assertIn("line 3", report["errors"][0])

    def test_strange_ability_bug(self):
        mast = master(h=mem_hook())
        mast.sentinel_register(name="test", code=jtp.strange_ability_bug)
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "travel"}
        )["report"]
        mast.sentinel_register(name="test", code=jtp.strange_ability_bug, auto_run="")
        report += mast.general_interface_to_api(
            api_name="walker_run", params={"name": "travel"}
        )["report"]
        ir = mast.sentinel_get(mode="ir", snt=mast.active_snt())
        mast.sentinel_set(code=ir, snt=mast.active_snt(), mode="ir")
        report += mast.general_interface_to_api(
            api_name="walker_run", params={"name": "travel"}
        )["report"]
        report += mast.general_interface_to_api(
            api_name="walker_run", params={"name": "travel"}
        )["report"]
        self.assertEqual(report, ["Showing", "Showing", "Showing", "Showing"])

    def test_node_inheritance(self):
        mast = master(h=mem_hook())
        mast.sentinel_register(name="test", code=jtp.node_inheritance, auto_run="")
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )
        self.assertEqual(
            report,
            {
                "report": [
                    "plain.x",
                    {"a": 55, "b": 7, "c": 7, "d": 80},
                    "super.x",
                    "plain2.y",
                    "super.y",
                ],
                "success": True,
            },
        )

    def test_node_inheritance_chain_check(self):
        mast = master(h=mem_hook())
        mast.sentinel_register(
            name="test", code=jtp.node_inheritance_chain_check, auto_run=""
        )
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )
        self.assertEqual(report["success"], False)

    def test_global_reregistering(self):
        mast = master(h=mem_hook())
        mast.sentinel_register(name="test", code=jtp.global_reregistering)
        self.assertTrue(mast.active_snt().is_active)
        mast.sentinel_set(snt=mast.active_snt(), code=jtp.global_reregistering)
        self.assertTrue(mast.active_snt().is_active)
        mast.sentinel_register(name="test", code=jtp.global_reregistering)
        self.assertTrue(mast.active_snt().is_active)

    def test_vector_cos_sim_check(self):
        mast = master(h=mem_hook())
        mast.sentinel_register(name="test", code=jtp.vector_cos_sim_check, auto_run="")
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertEqual(len(report), 1)
        self.assertEqual(type(report[0]), float)

    def test_multi_breaks(self):
        mast = master(h=mem_hook())
        mast.sentinel_register(name="test", code=jtp.multi_breaks, auto_run="")
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertEqual(len(report), 15)
        self.assertEqual(report[14], 180)

    def test_reffy_deref_check(self):
        mast = master(h=mem_hook())
        mast.sentinel_register(name="test", code=jtp.reffy_deref_check, auto_run="")
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertFalse(report[0])
        self.assertTrue(report[1])

    def test_vanishing_can_check(self):
        mast = super_master(h=mem_hook())
        mast.actions_load_local("jaseci/tests/infer.py")
        mast.sentinel_register(name="test", code=jtp.vanishing_can_check, auto_run="")
        mast.general_interface_to_api(api_name="walker_run", params={"name": "init"})
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertEqual(report, ["2022-01-01T00:00:00"])
        mast.propagate_access("public")
        mast2 = super_master(h=mast._h)
        mast.active_snt().run_architype(name="plain", kind="node", caller=mast2)
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertEqual(report, ["2022-01-01T00:00:00"])

    def test_jasecilib_alias_list(self):
        mast = master(h=mem_hook())
        mast.sentinel_register(name="test", code=jtp.jasecilib_alias_list, auto_run="")
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertGreater(len(report[0].keys()), 3)

    def test_jasecilib_params(self):
        mast = master(h=mem_hook())
        mast.sentinel_register(name="test", code=jtp.jasecilib_params, auto_run="")
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertIn("j_r_acc_ids", report[0][0].keys())

    def test_jasecilib_create_user(self):
        mast = master(h=mem_hook())
        mast.sentinel_register(name="test", code=jtp.jasecilib_create_user, auto_run="")
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertEqual(report[0]["name"], ("daman@gmail.com",))
