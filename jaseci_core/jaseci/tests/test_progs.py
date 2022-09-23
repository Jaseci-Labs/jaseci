from unittest import TestCase

import jaseci.tests.jac_test_progs as jtp
from jaseci.actor.sentinel import Sentinel
from jaseci.graph.graph import Graph
from jaseci.graph.node import Node
from jaseci.svc import MetaService
from jaseci.utils.utils import TestCaseHelper


class JacTests(TestCaseHelper, TestCase):
    """Unit tests for Jac language"""

    def setUp(self):
        super().setUp()

        self.meta = MetaService()

    def tearDown(self):
        super().tearDown()

    def test_bug_check1(self):
        sent = Sentinel(m_id="anon", h=self.meta.hook())
        gph = Graph(m_id="anon", h=sent._h)
        sent.register_code(jtp.bug_check1)
        test_walker = sent.run_architype("init")
        test_walker.prime(gph)
        test_walker.run()
        report = test_walker.report
        self.assertEqual(report[0][0], "THIS IS AN INTENT_LABEL")

    def test_action_load_std_lib(self):
        mast = self.meta.super_master()
        mast.sentinel_register(name="test", code=jtp.action_load_std_lib)
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "aload"}
        )["report"]
        self.assertEqual(report[0], True)

    def test_action_load_std_lib_only_super(self):
        mast = self.meta.master()
        mast.sentinel_register(name="test", code=jtp.action_load_std_lib)
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "aload"}
        )
        report = report["report"]
        self.assertEqual(report[0], False)

    def test_globals(self):
        sent = Sentinel(m_id="anon", h=self.meta.hook())
        gph = Graph(m_id="anon", h=sent._h)
        sent.register_code(jtp.globals)
        test_walker = sent.run_architype("init")
        test_walker.prime(gph)
        test_walker.run()
        report = test_walker.report
        self.assertEqual(report, ["testing", 56])

    def test_net_root_std_lib(self):
        mast = self.meta.master()
        mast.sentinel_register(name="test", code=jtp.net_root_std_lib)
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertEqual(report[0][0], report[0][1])
        self.assertEqual(report[0][1], report[1][1])
        self.assertNotEqual(report[1][0], report[1][1])

    def test_or_stmt(self):
        mast = self.meta.master()
        mast.sentinel_register(name="test", code=jtp.or_stmt)
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertEqual(report, [[3.4, "Hello"]])

    def test_nd_equals(self):
        mast = self.meta.master()
        mast.sentinel_register(name="test", code=jtp.nd_equals_error_correct_line)
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )
        self.assertIn("line 3", report["errors"][0])

    def test_strange_ability_bug(self):
        import json

        mast = self.meta.master()
        mast.sentinel_register(name="test", code=jtp.strange_ability_bug)
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "travel"}
        )["report"]
        mast.sentinel_register(name="test", code=jtp.strange_ability_bug, auto_run="")
        report += mast.general_interface_to_api(
            api_name="walker_run", params={"name": "travel"}
        )["report"]
        ir = mast.sentinel_get(mode="ir", snt=mast.active_snt())
        mast.sentinel_set(code=json.dumps(ir), snt=mast.active_snt(), mode="ir")
        report += mast.general_interface_to_api(
            api_name="walker_run", params={"name": "travel"}
        )["report"]
        report += mast.general_interface_to_api(
            api_name="walker_run", params={"name": "travel"}
        )["report"]
        self.assertEqual(report, ["Showing", "Showing", "Showing", "Showing"])

    def test_node_inheritance(self):
        mast = self.meta.master()
        mast.sentinel_register(name="test", code=jtp.node_inheritance, auto_run="")
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )
        del report["final_node"]
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
                "yielded": False,
            },
        )

    def test_inherited_ref(self):
        mast = self.meta.master()
        mast.sentinel_register(name="test", code=jtp.inherited_ref, auto_run="")
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )
        self.assertEqual(len(report["report"]), 12)

    def test_node_inheritance_chain_check(self):
        mast = self.meta.master()
        mast.sentinel_register(
            name="test", code=jtp.node_inheritance_chain_check, auto_run=""
        )
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )
        self.assertEqual(report["success"], False)

    def test_global_reregistering(self):
        mast = self.meta.master()
        mast.sentinel_register(name="test", code=jtp.global_reregistering)
        self.assertTrue(mast.active_snt().is_active)
        mast.sentinel_set(snt=mast.active_snt(), code=jtp.global_reregistering)
        self.assertTrue(mast.active_snt().is_active)
        mast.sentinel_register(name="test", code=jtp.global_reregistering)
        self.assertTrue(mast.active_snt().is_active)

    def test_vector_cos_sim_check(self):
        mast = self.meta.master()
        mast.sentinel_register(name="test", code=jtp.vector_cos_sim_check, auto_run="")
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertEqual(len(report), 1)
        self.assertEqual(type(report[0]), float)

    def test_multi_breaks(self):
        mast = self.meta.master()
        mast.sentinel_register(name="test", code=jtp.multi_breaks, auto_run="")
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertEqual(len(report), 15)
        self.assertEqual(report[14], 180)

    def test_reffy_deref_check(self):
        mast = self.meta.master()
        mast.sentinel_register(name="test", code=jtp.reffy_deref_check, auto_run="")
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertFalse(report[0])
        self.assertTrue(report[1])

    def test_vanishing_can_check(self):
        mast = self.meta.super_master()
        mast.actions_load_local("jaseci/tests/infer.py")
        mast.sentinel_register(name="test", code=jtp.vanishing_can_check, auto_run="")
        mast.general_interface_to_api(api_name="walker_run", params={"name": "init"})
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertEqual(report, ["2022-01-01T00:00:00"])
        mast.propagate_access("public")
        mast2 = self.meta.super_master(h=mast._h)
        mast.active_snt().run_architype(name="plain", kind="node", caller=mast2)
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertEqual(report, ["2022-01-01T00:00:00"])

    def test_jasecilib_alias_list(self):
        mast = self.meta.master()
        mast.sentinel_register(name="test", code=jtp.jasecilib_alias_list, auto_run="")
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertGreater(len(report[0].keys()), 3)

    def test_jasecilib_params(self):
        mast = self.meta.master()
        mast.sentinel_register(name="test", code=jtp.jasecilib_params, auto_run="")
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertIn("j_r_acc_ids", report[0][0].keys())

    def test_jasecilib_create_user(self):
        mast = self.meta.master()
        mast.sentinel_register(name="test", code=jtp.jasecilib_create_user, auto_run="")
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertEqual(report[0]["user"]["name"], "daman@gmail.com")

    def test_root_is_node_type(self):
        mast = self.meta.master()
        mast.sentinel_register(name="test", code=jtp.root_is_node_type, auto_run="")
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )
        self.assertEqual(report["report"][0], "JAC_TYPE.NODE")

    def test_walker_with_exit_after_node(self):
        mast = self.meta.master()
        mast.sentinel_register(
            name="test", code=jtp.walker_with_exit_after_node, auto_run=""
        )
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )
        self.assertEqual(report["report"], [1, 1, 3, 1, 3, 1, 3, 1, 3, 43])

    def test_depth_first_take(self):
        mast = self.meta.master()
        mast.sentinel_register(name="test", code=jtp.depth_first_take, auto_run="")
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )
        self.assertEqual(report["report"], [1, 2, 3, 4, 5, 6, 7])

    def test_breadth_first_take(self):
        mast = self.meta.master()
        mast.sentinel_register(name="test", code=jtp.breadth_first_take, auto_run="")
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )
        self.assertEqual(report["report"], [1, 2, 5, 3, 4, 6, 7])

    def test_inheritance_override_here_check(self):
        mast = self.meta.master()
        mast.sentinel_register(
            name="test", code=jtp.inheritance_override_here_check, auto_run=""
        )
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )
        self.assertEqual(report["report"], [9, 9, 10])

    def test_dot_private_hidden(self):
        mast = self.meta.master()
        mast.sentinel_register(name="test", code=jtp.dot_private_hidden, auto_run="")
        mast.general_interface_to_api(api_name="walker_run", params={"name": "init"})
        report = mast.general_interface_to_api(
            api_name="graph_get", params={"mode": "dot", "detailed": True}
        )
        self.assertNotIn("j=", report)

    def test_check_destroy_node_has_var(self):
        mast = self.meta.master()
        mast.sentinel_register(
            name="test", code=jtp.check_destroy_node_has_var, auto_run=""
        )
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "create"}
        )
        self.assertEqual(mast._h.get_object_distribution()[Node], 2)
        self.assertEqual(report["report"][0], "JAC_TYPE.NODE")
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "remove"}
        )
        self.assertEqual(mast._h.get_object_distribution()[Node], 1)
        self.assertEqual(report["report"][0], "JAC_TYPE.NULL")

    def test_for_loop_dict(self):
        mast = self.meta.master()
        mast.sentinel_register(
            name="test", code=jtp.check_dict_for_in_loop, auto_run=""
        )
        res = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "for_loop_dict"}
        )

        self.assertEqual(
            res["report"],
            [
                "test1 : 1",
                "test2 : 2",
                "test3 : 3",
                "test1 : 1",
                "test2 : 2",
                "test3 : 3",
                5,
                6,
                7,
                "0 : 5",
                "1 : 6",
                "2 : 7",
            ],
        )

    def test_var_as_key_for_dict(self):
        mast = self.meta.master()
        mast.sentinel_register(
            name="test", code=jtp.check_dict_for_in_loop, auto_run=""
        )
        res = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "var_as_key_for_dict"}
        )

        self.assertEqual(res["report"], [{"key1": "key1", "key2": 2}])
        self.assertIn("Key is not str type : <class 'int'>!", res["errors"][0])

    def test_new_additional_builtin(self):
        mast = self.meta.master()
        mast.sentinel_register(name="test", code=jtp.check_new_builtin, auto_run="")

        res = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )

        self.assertEqual(
            res["report"],
            [{"test": "test"}, 1, "1 2 3 4", "1 2 3 4"],
        )

    def test_continue_issue(self):
        mast = self.meta.master()
        mast.sentinel_register(name="test", code=jtp.continue_issue, auto_run="")
        res = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )
        self.assertEqual(res["report"], [1, 2, 3, 4, 5, 6, 7, 8, "apple"])
