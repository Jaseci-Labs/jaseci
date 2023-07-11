from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper
from unittest.mock import patch
import jaseci.jsorc.live_actions as jla
import jaseci.jsorc.remote_actions as jra
from jaseci.jsorc.live_actions import (
    gen_remote_func_hook,
    # load_module_actions,
    # live_actions,
    # load_remote_actions,
    unload_module,
    act_procs,
    load_local_actions,
)

# from jaseci.utils.test_core import CoreTest
from jaseci.jsorc.jsorc import JsOrc
from jaseci.prim.sentinel import Sentinel


class JacActionsTests(TestCaseHelper, TestCase):
    """Unit tests for Jac language"""

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_load_unload_load_demo_test_module(self):
        """Test loading, unloading, and loading again of a demo_test module"""
        demo_test1_jac_code = """
            walker test_demo {
                can demo_test1.action1;
                report demo_test.action1("Hello, world!");
            }
        """
        demo_test2_jac_code = """
            walker test_demo {
                can demo_test2.action1;
                report demo_test.action1("Hello, world!");
            }
        """
        # Load the demo_test module
        load_local_actions("./test_1/demo_test1.py")
        # Store the initial number of subprocesses
        initial_subprocess_count = len(act_procs)
        # Perform tests for the action module
        sent = Sentinel(m_id=0, h=JsOrc.hook())
        sent.register_code(demo_test1_jac_code)
        root_node = sent.arch_ids.get_obj_by_name("root", kind="node").run()
        test_walker = sent.run_architype("test_demo")
        test_walker.prime(root_node)
        test_walker.run()

        load_local_actions("./test_2/demo_test2.py")
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
        # Perform additional tests after unloading the module
        # ...

        # # Load the same demo_test module again
        # load_module_actions("demo_test")

        # # Assert that the number of subprocesses has increased
        # self.assertGreater(len(jla.live_actions.act_procs), initial_subprocess_count)

    def test_remote_action_example(self):
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
        print(jra.remote_actions)
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
        self.assertGreater(len(jla.live_actions), 25)

    @patch("requests.post")
    def test_remote_action_kwargs(self, mock_post):
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
        @jla.jaseci_action(act_group=["ex"], allow_remote=True)
        def setup(param: str = ""):
            pass

        app = jra.serv_actions()
        assert len(app.__dict__["router"].__dict__["on_startup"]) == 1

    def test_load_single_action_module(self):
        """Test loading a single action module"""
        demo_test1_jac_code = """
            walker test_demo {
                can demo_test1.action1;
                report demo_test.action1("Hello, world!");
            }
        """
        # Load the demo_test module
        load_local_actions("./test_1/demo_test1.py")
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
        """Test loading a single action module"""
        demo_test1_jac_code = """
            walker test_demo {
                can demo_test1.action1;
                report demo_test.action1("Hello, world!");
            }
        """

        # Load the demo_test module
        load_local_actions("./test_1/demo_test1.py")
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
        load_local_actions("./test_1/demo_test1.py")

        # Assert that the number of subprocesses remains the same
        self.assertEqual(len(act_procs), initial_subprocess_count)
        # Unload the demo_test module
        unload_module("test_1.demo_test1")

    def test_load_multiple_action_modules(self):
        """Test loading, unloading, and loading again of a demo_test module"""
        demo_test1_jac_code = """
            walker test_demo {
                can demo_test1.action1;
                report demo_test.action1("Hello, world!");
            }
        """
        demo_test2_jac_code = """
            walker test_demo {
                can demo_test2.action1;
                report demo_test.action1("Hello, world!");
            }
        """
        # Load the demo_test module
        load_local_actions("./test_1/demo_test1.py")
        # Store the initial number of subprocesses
        initial_subprocess_count = len(act_procs)
        # Perform tests for the action module
        sent = Sentinel(m_id=0, h=JsOrc.hook())
        sent.register_code(demo_test1_jac_code)
        root_node = sent.arch_ids.get_obj_by_name("root", kind="node").run()
        test_walker = sent.run_architype("test_demo")
        test_walker.prime(root_node)
        test_walker.run()

        load_local_actions("./test_2/demo_test2.py")
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
        """Test loading, unloading, and loading again of an action module"""
        demo_test1_jac_code = """
            walker test_demo {
                can demo_test1.action1;
                report demo_test.action1("Hello, world!");
            }
        """

        # Load the demo_test module
        load_local_actions("./test_1/demo_test1.py")
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
        load_local_actions("./test_1/demo_test1.py")

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
