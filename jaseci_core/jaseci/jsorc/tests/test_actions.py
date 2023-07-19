from unittest import TestCase
import os
import sys
from jaseci.utils.utils import TestCaseHelper
from unittest.mock import patch
import jaseci.jsorc.live_actions as jla
import jaseci.jsorc.remote_actions as jra
from jaseci.jsorc.live_actions import (
    gen_remote_func_hook,
    load_module_actions,
    unload_module,
    act_procs,
)
from jaseci.jsorc.jsorc import JsOrc
from jaseci.prim.sentinel import Sentinel


class JacActionsTests(TestCaseHelper, TestCase):
    """Unit tests for Jac language"""

    def setUp(self):
        """
        Set up the test case by adding necessary paths to sys.path.
        """
        files = ["test_1/demo_test1.py", "test_2/demo_test2.py"]
        for file in files:
            module_dir = os.path.dirname(os.path.dirname(os.path.realpath(file)))
            if module_dir not in sys.path:
                sys.path.append(module_dir)
        super().setUp()

    def tearDown(self):
        """
        Tear down the test case.
        """
        super().tearDown()

    def test_remote_action_example(self):
        """
        Test the generation of remote actions and their parameters.
        """
        from typing import Union

        @jla.jaseci_action(
            act_group=["use"], aliases=["enc_question"], allow_remote=True
        )
        def question_encode(question: Union[str, list]):
            pass

        @jla.jaseci_action(act_group=["use"], aliases=["enc_answer"], allow_remote=True)
        def answer_encode(answer: Union[str, list], context: Union[str, list] = None):
            pass

        @jla.jaseci_action(act_group=["use"], allow_remote=True)
        def cos_sim_score(q_emb: list, a_emb: list):
            pass

        @jla.jaseci_action(act_group=["use"], aliases=["qa_score"], allow_remote=True)
        def dist_score(q_emb: list, a_emb: list):
            pass

        jra.serv_actions()
        self.assertEqual(
            jra.remote_actions,
            {
                "use.answer_encode": ["answer", "context"],
                "use.cos_sim_score": ["q_emb", "a_emb"],
                "use.dist_score": ["q_emb", "a_emb"],
                "use.enc_answer": ["answer", "context"],
                "use.enc_question": [
                    "question",
                ],
                "use.qa_score": ["q_emb", "a_emb"],
                "use.question_encode": ["question"],
            },
        )

    def test_live_action_globals(self):
        """
        Test the availability of live actions in the global namespace.
        """
        self.assertGreater(len(jla.live_actions), 25)

    @patch("requests.post")
    def test_remote_action_kwargs(self, mock_post):
        """
        Test the execution of remote actions with keyword arguments.
        """
        remote_action = gen_remote_func_hook(
            url="https://example.com/api/v1/endpoint",
            act_name="example.action",
            param_names=["param1", "param2"],
        )
        payload = {"param1": "value1"}
        remote_action(**payload)

        mock_post.assert_called_once()

        _, kwargs = mock_post.call_args

        assert kwargs["json"] == payload

    def test_setup_decorated_as_startup(self):
        """
        Test that an action decorated with 'allow_remote' is set as startup.
        """

        @jla.jaseci_action(act_group=["ex"], allow_remote=True)
        def setup(param: str = ""):
            pass

        app = jra.serv_actions()
        assert len(app.__dict__["router"].__dict__["on_startup"]) == 1

    def test_load_single_action_module(self):
        """
        Test loading a single action module.
        """
        demo_test1_jac_code = """
            walker test_demo {
                can demo_test1.action1;
                report demo_test1.action1("Hello, world!");
            }
        """
        # Load the demo_test module
        load_module_actions("test_1.demo_test1")
        # Store the initial number of subprocesses
        initial_subprocess_count = len(act_procs)
        # Perform tests for the action module
        sent = Sentinel(m_id=0, h=JsOrc.hook())
        sent.register_code(demo_test1_jac_code)
        root_node = sent.arch_ids.get_obj_by_name("root", kind="node").run()
        test_walker = sent.run_architype("test_demo")
        test_walker.prime(root_node)
        test_walker.run()
        # Unload the demo_test module
        unload_module("test_1.demo_test1")

        # Assert that the number of subprocesses has decreased
        self.assertLess(len(act_procs), initial_subprocess_count)

    def test_load_single_action_module_twice(self):
        """
        Test loading a single action module twice.
        """
        demo_test1_jac_code = """
            walker test_demo {
                can demo_test1.action1;
                report demo_test1.action1("Hello, world!");
            }
        """

        # Load the demo_test module
        load_module_actions("test_1.demo_test1")
        # Store the initial number of subprocesses
        initial_subprocess_count = len(act_procs)
        # Perform tests for the action module
        sent = Sentinel(m_id=0, h=JsOrc.hook())
        sent.register_code(demo_test1_jac_code)
        root_node = sent.arch_ids.get_obj_by_name("root", kind="node").run()
        test_walker = sent.run_architype("test_demo")
        test_walker.prime(root_node)
        test_walker.run()

        # Load the same action module again
        load_module_actions("test_1.demo_test1")

        # Assert that the number of subprocesses remains the same
        self.assertEqual(len(act_procs), initial_subprocess_count)
        # Unload the demo_test module
        unload_module("test_1.demo_test1")

    def test_load_multiple_action_modules(self):
        """
        Test loading multiple action modules.
        """
        demo_test1_jac_code = """
            walker test_demo {
                can demo_test1.action1;
                report demo_test1.action1("Hello, world!");
            }
        """
        demo_test2_jac_code = """
            walker test_demo {
                can demo_test2.action2;
                report demo_test2.action2("Hello, world!");
            }
        """
        # Load the demo_test module
        load_module_actions("test_1.demo_test1")
        # Store the initial number of subprocesses
        initial_subprocess_count = len(act_procs)
        # Perform tests for the action module
        sent = Sentinel(m_id=0, h=JsOrc.hook())
        sent.register_code(demo_test1_jac_code)
        root_node = sent.arch_ids.get_obj_by_name("root", kind="node").run()
        test_walker = sent.run_architype("test_demo")
        test_walker.prime(root_node)
        test_walker.run()

        load_module_actions("test_2.demo_test2")
        # Assert that the number of subprocesses has increased
        self.assertGreater(len(act_procs), initial_subprocess_count)
        # Perform tests for the action module
        sent = Sentinel(m_id=0, h=JsOrc.hook())
        sent.register_code(demo_test2_jac_code)
        root_node = sent.arch_ids.get_obj_by_name("root", kind="node").run()
        test_walker = sent.run_architype("test_demo")
        test_walker.prime(root_node)
        test_walker.run()
        # Unload the demo_test module
        unload_module("test_1.demo_test1")

        # Assert that the number of subprocesses has decreased
        self.assertEqual(len(act_procs), initial_subprocess_count)
        # Unload the demo_test module
        unload_module("test_2.demo_test2")

        # Assert that the number of subprocesses has decreased
        self.assertLess(len(act_procs), initial_subprocess_count)

    def test_load_unload_load_action_module(self):
        """
        Test loading, unloading, and loading again of an action module.
        """
        demo_test1_jac_code = """
            walker test_demo {
                can demo_test1.action1;
                report demo_test1.action1("Hello, world!");
            }
        """

        # Load the demo_test module
        load_module_actions("test_1.demo_test1")
        # Store the initial number of subprocesses
        initial_subprocess_count = len(act_procs)
        # Perform tests for the action module
        sent = Sentinel(m_id=0, h=JsOrc.hook())
        sent.register_code(demo_test1_jac_code)
        root_node = sent.arch_ids.get_obj_by_name("root", kind="node").run()
        test_walker = sent.run_architype("test_demo")
        test_walker.prime(root_node)
        test_walker.run()

        # Unload the action module
        unload_module("test_1.demo_test1")

        # Assert that the number of subprocesses has decreased
        self.assertLess(len(act_procs), initial_subprocess_count)

        # Load the demo_test module
        load_module_actions("test_1.demo_test1")

        # Assert that the number of subprocesses has increased
        self.assertEqual(len(act_procs), initial_subprocess_count)

        # Perform tests for the action module
        sent = Sentinel(m_id=0, h=JsOrc.hook())
        sent.register_code(demo_test1_jac_code)
        root_node = sent.arch_ids.get_obj_by_name("root", kind="node").run()
        test_walker = sent.run_architype("test_demo")
        test_walker.prime(root_node)
        test_walker.run()

        # Unload the module again
        unload_module("test_1.demo_test1")

        # Assert that the number of subprocesses has decreased again
        self.assertLess(len(act_procs), initial_subprocess_count)

    def test_load_action_module_same_act_group(self):
        """
        Test loading of an action module within the same act group.
        """
        demo_test1_jac_code = """
        walker test_demo {
                can demo_test2.action2;
                report demo_test2.action2("Hello, world!");
            }
        """
        demo_test2_jac_code = """
            walker test_demo {
                can demo_test2.action3;
                report demo_test2.action3("Hello, world!");
            }
        """
        # Load the demo_test module
        load_module_actions("test_2.demo_test2")
        # Store the initial number of subprocesses
        initial_subprocess_count = len(act_procs)
        # Perform tests for the action module
        sent = Sentinel(m_id=0, h=JsOrc.hook())
        sent.register_code(demo_test1_jac_code)
        root_node = sent.arch_ids.get_obj_by_name("root", kind="node").run()
        test_walker = sent.run_architype("test_demo")
        test_walker.prime(root_node)
        self.assertTrue(test_walker.run()["success"])

        load_module_actions("test_2.demo_test3")
        # Assert that the number of subprocesses has increased
        self.assertGreater(len(act_procs), initial_subprocess_count)
        # Perform tests for the action module
        sent = Sentinel(m_id=0, h=JsOrc.hook())
        sent.register_code(demo_test2_jac_code)
        root_node = sent.arch_ids.get_obj_by_name("root", kind="node").run()
        test_walker = sent.run_architype("test_demo")
        test_walker.prime(root_node)
        self.assertTrue(test_walker.run()["success"])
        # Unload the demo_test module
        unload_module("test_2.demo_test2")

        # Assert that the number of subprocesses has decreased
        self.assertEqual(len(act_procs), initial_subprocess_count)
        # Unload the demo_test module
        unload_module("test_2.demo_test3")

        # Assert that the number of subprocesses has decreased
        self.assertLess(len(act_procs), initial_subprocess_count)
