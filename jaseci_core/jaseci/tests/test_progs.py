import os
import pytest
from unittest import TestCase

import jaseci.tests.jac_test_progs as jtp
from jaseci.prim.sentinel import Sentinel
from jaseci.prim.graph import Graph
from jaseci.prim.node import Node
from jaseci.utils.utils import TestCaseHelper
from jaseci.jsorc.jsorc import JsOrc
from jaseci.jsorc.jsorc_utils import State


class ProgTests(TestCaseHelper, TestCase):
    """Unit tests for Jac language"""

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_bug_check1(self):
        self.logger_on()
        sent = Sentinel(m_id=0, h=JsOrc.hook())
        gph = Graph(m_id=0, h=sent._h)
        sent.register_code(jtp.bug_check1)
        test_walker = sent.run_architype("init")
        test_walker.prime(gph)
        test_walker.run()
        report = test_walker.report
        self.assertEqual(report[0][0], "THIS IS AN INTENT_LABEL")

    def test_action_load_std_lib(self):
        mast = JsOrc.super_master()
        mast.sentinel_register(name="test", code=jtp.action_load_std_lib)
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "aload"}
        )["report"]
        self.assertEqual(report[0], True)

    def test_action_load_std_lib_only_super(self):
        mast = JsOrc.master()
        mast.sentinel_register(name="test", code=jtp.action_load_std_lib)
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "aload"}
        )
        self.assertFalse(report["success"])
        self.assertEqual(
            [
                "test:aload - line 3, col 33 - rule expr_list - Only super master can load actions."
            ],
            report["errors"],
        )

    def test_globals(self):
        sent = Sentinel(m_id=0, h=JsOrc.hook())
        gph = Graph(m_id=0, h=sent._h)
        sent.register_code(jtp.globals)
        test_walker = sent.run_architype("init")
        test_walker.prime(gph)
        test_walker.run()
        report = test_walker.report
        self.assertEqual(report, ["testing", 56])

    def test_net_root_std_lib(self):
        mast = JsOrc.master()
        mast.sentinel_register(name="test", code=jtp.net_root_std_lib)
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertEqual(report[0][0], report[0][1])
        self.assertEqual(report[0][1], report[1][1])
        self.assertNotEqual(report[1][0], report[1][1])

    def test_or_stmt(self):
        mast = JsOrc.master()
        mast.sentinel_register(name="test", code=jtp.or_stmt)
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertEqual(report, [[3.4, "Hello"]])

    def test_nd_equals(self):
        mast = JsOrc.master()
        mast.sentinel_register(name="test", code=jtp.nd_equals_error_correct_line)
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )
        self.assertIn("line 3", report["errors"][0])

    def test_strange_ability_bug(self):
        import json

        mast = JsOrc.master()
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
        mast = JsOrc.master()
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
        mast = JsOrc.master()
        mast.sentinel_register(name="test", code=jtp.inherited_ref, auto_run="")
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )
        self.assertEqual(len(report["report"]), 12)

    def test_node_inheritance_chain_check(self):
        mast = JsOrc.master()
        mast.sentinel_register(
            name="test", code=jtp.node_inheritance_chain_check, auto_run=""
        )
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )
        self.assertEqual(report["success"], False)

    def test_global_reregistering(self):
        mast = JsOrc.master()
        mast.sentinel_register(name="test", code=jtp.global_reregistering)
        self.assertTrue(mast.active_snt().is_active)
        mast.sentinel_set(snt=mast.active_snt(), code=jtp.global_reregistering)
        self.assertTrue(mast.active_snt().is_active)
        mast.sentinel_register(name="test", code=jtp.global_reregistering)
        self.assertTrue(mast.active_snt().is_active)

    def test_vector_cos_sim_check(self):
        mast = JsOrc.master()
        mast.sentinel_register(name="test", code=jtp.vector_cos_sim_check, auto_run="")
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertEqual(len(report), 1)
        self.assertEqual(type(report[0]), float)

    def test_multi_breaks(self):
        mast = JsOrc.master()
        mast.sentinel_register(name="test", code=jtp.multi_breaks, auto_run="")
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertEqual(len(report), 15)
        self.assertEqual(report[14], 180)

    def test_reffy_deref_check(self):
        mast = JsOrc.master()
        mast.sentinel_register(name="test", code=jtp.reffy_deref_check, auto_run="")
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertFalse(report[0])
        self.assertTrue(report[1])

    def test_vanishing_can_check(self):
        mast = JsOrc.super_master()
        mast.actions_load_local("jaseci/tests/infer.py")
        mast.sentinel_register(name="test", code=jtp.vanishing_can_check, auto_run="")
        mast.general_interface_to_api(api_name="walker_run", params={"name": "init"})
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertEqual(report, ["2022-01-01T00:00:00"])
        mast.propagate_access("public")
        mast2 = JsOrc.super_master(h=mast._h)
        mast.active_snt().run_architype(name="plain", kind="node", caller=mast2)
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertEqual(report, ["2022-01-01T00:00:00"])

    def test_jasecilib_alias_list(self):
        mast = JsOrc.master()
        mast.sentinel_register(name="test", code=jtp.jasecilib_alias_list, auto_run="")
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertGreater(len(report[0].keys()), 3)

    def test_jasecilib_params(self):
        mast = JsOrc.master()
        mast.sentinel_register(name="test", code=jtp.jasecilib_params, auto_run="")
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertIn("j_r_acc_ids", report[0][0].keys())

    def test_jasecilib_create_user(self):
        mast = JsOrc.master()
        mast.sentinel_register(name="test", code=jtp.jasecilib_create_user, auto_run="")
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )["report"]
        self.assertEqual(report[0]["user"]["name"], "daman@gmail.com")

    def test_root_is_node_type(self):
        mast = JsOrc.master()
        mast.sentinel_register(name="test", code=jtp.root_is_node_type, auto_run="")
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )
        self.assertEqual(report["report"][0], "JAC_TYPE.NODE")

    def test_walker_with_exit_after_node(self):
        mast = JsOrc.master()
        mast.sentinel_register(
            name="test", code=jtp.walker_with_exit_after_node, auto_run=""
        )
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )
        self.assertEqual(report["report"], [1, 1, 3, 1, 3, 1, 3, 1, 3, 43])

    def test_depth_first_take(self):
        mast = JsOrc.master()
        mast.sentinel_register(name="test", code=jtp.depth_first_take, auto_run="")
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )
        self.assertEqual(report["report"], [1, 2, 3, 4, 5, 6, 7])

    def test_breadth_first_take(self):
        mast = JsOrc.master()
        mast.sentinel_register(name="test", code=jtp.breadth_first_take, auto_run="")
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )
        self.assertEqual(report["report"], [1, 2, 5, 3, 4, 6, 7])

    def test_inheritance_override_here_check(self):
        mast = JsOrc.master()
        mast.sentinel_register(
            name="test", code=jtp.inheritance_override_here_check, auto_run=""
        )
        report = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )
        self.assertEqual(report["report"], [9, 9, 10])

    def test_dot_private_hidden(self):
        mast = JsOrc.master()
        mast.sentinel_register(name="test", code=jtp.dot_private_hidden, auto_run="")
        mast.general_interface_to_api(api_name="walker_run", params={"name": "init"})
        report = mast.general_interface_to_api(
            api_name="graph_get", params={"mode": "dot", "detailed": True}
        )
        self.assertNotIn("j=", report)

    def test_check_destroy_node_has_var(self):
        mast = JsOrc.master()
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
        mast = JsOrc.master()
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
        mast = JsOrc.master()
        mast.sentinel_register(
            name="test", code=jtp.check_dict_for_in_loop, auto_run=""
        )
        res = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "var_as_key_for_dict"}
        )

        self.assertEqual(res["report"], [{"key1": "key1", "key2": 2}])
        self.assertEqual(
            "test:var_as_key_for_dict - line 42, col 16 - rule expression - Key is not str type : <class 'int'>!",
            res["errors"][0],
        )

    def test_list_pairwise(self):
        mast = JsOrc.master()
        mast.sentinel_register(name="test", code=jtp.list_pairwise, auto_run="")

        res = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )

        self.assertEqual(
            res["report"],
            [[[1, 2], [2, 3], [3, 4]]],
        )

    def test_list_unique(self):
        mast = JsOrc.master()
        mast.sentinel_register(name="test", code=jtp.list_unique, auto_run="")

        res = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )

        self.assertEqual(
            res["report"],
            [[1, 2, 3, 4, 5]],
        )

    def test_new_additional_builtin(self):
        mast = JsOrc.master()
        mast.sentinel_register(name="test", code=jtp.check_new_builtin, auto_run="")

        res = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )

        self.assertEqual(
            res["report"],
            [{"test": "test"}, 1, "1 2 3 4", "1 2 3 4"],
        )

    def test_continue_issue(self):
        mast = JsOrc.master()
        mast.sentinel_register(name="test", code=jtp.continue_issue, auto_run="")
        res = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )
        self.assertEqual(res["report"], [1, 2, 3, 4, 5, 6, 7, 8, "apple"])

    def test_registering_dict_as_ir(self):
        mast = JsOrc.master()
        mast.sentinel_register(name="test", code=jtp.continue_issue, auto_run="")
        code_dict = mast.sentinel_get(snt=mast.active_snt(), mode="ir")
        self.assertEqual(type(code_dict), dict)
        mast.sentinel_register(name="test", code=code_dict, mode="ir", auto_run="")
        res = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )
        self.assertEqual(res["report"], [1, 2, 3, 4, 5, 6, 7, 8, "apple"])

    @pytest.mark.order(2)
    def test_async_syntax_with_celery(self):
        mast = JsOrc.master()
        if not JsOrc.svc("task").is_running():
            self.skip_test("Celery not running")
        mast.sentinel_register(name="test", code=jtp.async_syntax, auto_run="")
        res = mast.general_interface_to_api(
            api_name="walker_run",
            params={"name": "simple_async", "ctx": {"sample": "name"}},
        )

        self.assertTrue(res["is_queued"])

        res = mast.general_interface_to_api(
            api_name="walker_queue_wait",
            params={"task_id": res["result"], "timeout": 15},
        )

        self.assertEqual("test", res["result"]["anchor"])

        res = res["result"]["response"]

        # report from task1 (awaited)
        self.assertEqual(1, res["report"][0])
        self.assertEqual(2, res["report"][1])

        # task1 anchor
        self.assertEqual(1, res["report"][2])
        report4 = res["report"][4]

        res = res["report"][3]

        # no celery running
        self.assertTrue(res["is_queued"])

        res = mast.general_interface_to_api(
            api_name="walker_queue_check",
            params={"task_id": res["result"]},
        )

        self.assertEqual(report4, res)
        self.assertEqual(2, res["result"]["anchor"])
        self.assertEqual([2, 2], res["result"]["response"]["report"])

    @pytest.mark.order(3)
    def test_async_syntax_with_update_and_celery(self):
        mast = JsOrc.master()
        if not JsOrc.svc("task").is_running():
            self.skip_test("Celery not running")
        mast.sentinel_register(
            name="test", code=jtp.async_syntax_with_update, auto_run="init"
        )
        res = mast.general_interface_to_api(
            api_name="walker_run",
            params={"name": "update_value", "ctx": {}},
        )

        self.assertTrue(res["is_queued"])

        res = mast.general_interface_to_api(
            api_name="walker_queue_wait",
            params={"task_id": res["result"], "timeout": 15},
        )

        self.assertEqual("SUCCESS", res["status"])
        self.assertTrue(res["result"]["response"]["report"][0]["value"])

        # remove the node on current _h.mem and let the redis repopulate it
        mast._h.mem.pop(res["result"]["response"]["final_node"], None)

        res = mast.general_interface_to_api(
            api_name="walker_run",
            params={"name": "get_value", "ctx": {}},
        )

        self.assertTrue(res["report"][0]["value"])

    def test_async_syntax_without_celery(self):
        mast = JsOrc.master()
        JsOrc.svc("task").state = State.NOT_STARTED
        mast.sentinel_register(name="test", code=jtp.async_syntax, auto_run="")
        res = mast.general_interface_to_api(
            api_name="walker_run",
            params={"name": "simple_async", "ctx": {"sample": "name"}},
        )

        # no celery running
        self.assertFalse(res["is_queued"])

        # report from task1 (awaited)
        self.assertEqual(1, res["result"]["report"][0])
        self.assertEqual(2, res["result"]["report"][1])

        # report from task2 (async but no celery)
        self.assertEqual(2, res["result"]["report"][2])
        self.assertEqual(2, res["result"]["report"][3])

        # task1 anchor
        self.assertEqual(1, res["result"]["report"][4])

        res = res["result"]["report"][5]

        # no celery running
        self.assertFalse(res["is_queued"])
        self.assertEqual(2, res["result"])

        JsOrc.svc("task").state = State.RUNNING

    def test_async_sync_syntax_with_celery(self):
        mast = JsOrc.master()
        if not JsOrc.svc("task").is_running():
            self.skip_test("Celery not running")
        mast.sentinel_register(name="test", code=jtp.async_syntax, auto_run="")
        res = mast.general_interface_to_api(
            api_name="walker_run",
            params={"name": "simple_async_with_sync", "ctx": {"sample": "name"}},
        )

        self.assertTrue(res["is_queued"])

        res = mast.general_interface_to_api(
            api_name="walker_queue_wait",
            params={"task_id": res["result"], "timeout": 15},
        )

        self.assertEqual("test", res["result"]["anchor"])

        res = res["result"]["response"]

        # report from task1 (awaited)
        self.assertEqual(1, res["report"][0])
        self.assertEqual(2, res["report"][1])

        # task1 anchor
        self.assertEqual(1, res["report"][2])
        report4 = res["report"][4]

        res = res["report"][3]

        # no celery running
        self.assertTrue(res["is_queued"])

        res = mast.general_interface_to_api(
            api_name="walker_queue_check",
            params={"task_id": res["result"]},
        )

        self.assertEqual(report4, res)
        self.assertEqual(2, res["result"]["anchor"])
        self.assertEqual([2, 2], res["result"]["response"]["report"])

    def test_async_sync_syntax_without_celery(self):
        mast = JsOrc.master()
        JsOrc.svc("task").state = State.NOT_STARTED
        mast.sentinel_register(name="test", code=jtp.async_syntax, auto_run="")
        res = mast.general_interface_to_api(
            api_name="walker_run",
            params={"name": "simple_async_with_sync", "ctx": {"sample": "name"}},
        )

        # no celery running
        self.assertFalse(res["is_queued"])

        # report from task1 (awaited)
        self.assertEqual(1, res["result"]["report"][0])
        self.assertEqual(2, res["result"]["report"][1])

        # report from task2 (async but no celery)
        self.assertEqual(2, res["result"]["report"][2])
        self.assertEqual(2, res["result"]["report"][3])

        # task1 anchor
        self.assertEqual(1, res["result"]["report"][4])

        res = res["result"]["report"][5]

        # no celery running
        self.assertFalse(res["is_queued"])
        self.assertEqual(2, res["result"])

        JsOrc.svc("task").state = State.RUNNING

    def test_block_scope_check(self):
        mast = JsOrc.master()
        mast.sentinel_register(name="test", code=jtp.block_scope_check, auto_run="")
        res = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )
        self.assertEqual(res["report"][-1], 10)

    def test_ignore_check(self):
        mast = JsOrc.master()
        res = mast.sentinel_register(name="test", code=jtp.ignore_check, auto_run="")
        res = mast.general_interface_to_api(
            api_name="walker_run", params={"name": "init"}
        )
        self.assertEqual(len(res["report"]), 9)

    @pytest.mark.order(1)
    def test_module_on_async(self):
        mast = JsOrc.super_master()
        if not JsOrc.svc("task").is_running():
            self.skip_test("Celery not running")

        with open("jaseci/tests/fixtures/non_existing_action.py", "w") as file:
            file.write(
                "from jaseci.jsorc.live_actions import jaseci_action\n@jaseci_action(act_group=['sim1'])\ndef tester():\n\treturn 1"
            )

        mast.sentinel_register(name="test", code=jtp.async_module, auto_run="")

        # sequence is relevant
        mast.actions_load_local("jaseci/tests/fixtures/non_existing_action.py")
        mast.actions_load_local("jaseci/tests/fixtures/existing_action.py")

        res = mast.general_interface_to_api(
            api_name="walker_run",
            params={"name": "a", "ctx": {}},
        )

        self.assertTrue(res["success"])

        # will return [1,2] since all local actions are loaded on MainProcess
        self.assertEqual([1, 2], res["report"])

        os.remove("jaseci/tests/fixtures/non_existing_action.py")

        res = mast.general_interface_to_api(
            api_name="walker_run",
            params={"name": "b", "ctx": {}},
        )

        self.assertTrue(res["is_queued"])

        res = mast.general_interface_to_api(
            api_name="walker_queue_wait",
            params={"task_id": res["result"], "timeout": 15},
        )

        self.assertEqual("SUCCESS", res["status"])

        # since sim1 file is already removed
        # upon running of task with sim1 it will try to rebuild
        # but file is already been deleted
        # without the fix it will throw error and will not continue on other action_sets
        # return would be [None, None] if not yet fixed
        self.assertEqual([None, 2], res["result"]["response"]["report"])

        self.assertIn(
            "Cannot execute sim1.tester - Not Found",
            res["result"]["response"]["errors"][0],
        )

    def test_walker_run_with_null_arguments(self):
        mast = JsOrc.master()
        res = mast.sentinel_register(
            name="test", code=jtp.walker_null_args, auto_run=""
        )
        res = mast.general_interface_to_api(
            api_name="walker_run",
            params={"name": "a", "ctx": {}},
        )
        self.assertTrue(res["success"])
        self.assertTrue(res["report"], [None, None])
        self.assertIsNone(res.get("errors"))

    def test_json_casting(self):
        mast = JsOrc.master()
        mast.sentinel_register(name="test", code=jtp.json_casting, auto_run="")

        res = mast.general_interface_to_api(
            api_name="walker_run",
            params={"name": "json_casting", "ctx": {}},
        )

        self.assertTrue(res["success"])
        self.assertEqual(
            res["report"],
            ['{"test": 1}', {"test2": 2}],
        )

    def test_edge_to_node_casting(self):
        mast = JsOrc.master()
        mast.sentinel_register(name="test", code=jtp.edge_to_node_casting, auto_run="")

        res = mast.general_interface_to_api(
            api_name="walker_run",
            params={"name": "edge_to_node_casting", "ctx": {}},
        )

        self.assertTrue(res["success"])

        edges = res["report"][0]
        self.assertEqual(1, len(edges))
        self.assertEqual("edge", edges[0]["kind"])

        nodes = res["report"][1]
        self.assertEqual(2, len(nodes))

        self.assertEqual(edges[0]["to_node_id"], nodes[0]["jid"])
        self.assertEqual("a", nodes[0]["name"])
        self.assertEqual(edges[0]["from_node_id"], nodes[1]["jid"])
        self.assertEqual("root", nodes[1]["name"])
