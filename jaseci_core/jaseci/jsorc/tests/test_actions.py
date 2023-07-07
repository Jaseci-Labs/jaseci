from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper
from unittest.mock import patch
import jaseci.jsorc.live_actions as jla
import jaseci.jsorc.remote_actions as jra
from jaseci.jsorc.live_actions import (
    gen_remote_func_hook,
    load_module_actions,
    # live_actions,
    # load_remote_actions,
    unload_module,
    act_procs,
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
        summarize_jac_code = """
            walker test_summarize {
                can cl_summer.summarize;
                report cl_summer.summarize("Today is a beautiful day.");
            }
        """
        # load_remote_actions("http://localhost:8001")
        # load_module_actions("jac_nlp.cl_summer")
        load_module_actions("jac_nlp.cl_summer")
        sent = Sentinel(m_id=0, h=JsOrc.hook())
        sent.register_code(summarize_jac_code)
        root_node = sent.arch_ids.get_obj_by_name("root", kind="node").run()
        test_walker = sent.run_architype("test_summarize")
        test_walker.prime(root_node)
        test_walker.run()
        print(test_walker.report)
        # self.assertEqual(test_walker.report[0][0], "Today is a beautiful day.")
        # self.call(
        #     self.mast,
        #     ["sentinel_register", {"code": self.load_jac("fixture/test_action.jac")}],
        # )

        # ret = self.call(self.mast, ["walker_run", {"name": "test_summarize"}])
        # print(ret)

    def test_load_single_action_module_twice(self):
        """Test loading a single action module"""
        summarize_jac_code = """
            walker test_summarize {
                can cl_summer.summarize;
                report cl_summer.summarize("Today is a beautiful day.");
            }
        """

        # Load the action module
        load_module_actions("jac_nlp.cl_summer")

        # Store the initial number of subprocesses
        initial_subprocess_count = len(act_procs)

        # Perform tests for the action module
        sent = Sentinel(m_id=0, h=JsOrc.hook())
        sent.register_code(summarize_jac_code)
        root_node = sent.arch_ids.get_obj_by_name("root", kind="node").run()
        test_walker = sent.run_architype("test_summarize")
        test_walker.prime(root_node)
        test_walker.run()

        # Load the same action module again
        load_module_actions("jac_nlp.cl_summer")

        # Assert that the number of subprocesses remains the same
        self.assertEqual(len(act_procs), initial_subprocess_count)

    def test_load_multiple_action_modules(self):
        """Test loading multiple different action modules"""
        summarize_jac_code = """
            walker test_summarize {
                can cl_summer.summarize;
                report cl_summer.summarize("Today is a beautiful day.");
            }
        """
        bi_enc_jac_code = """
            walker test_bi_enc {
                can bi_enc.get_context_emb;
                report bi_enc.get_context_emb(["Today is a beautiful day."]);
            }
        """
        sentiment_jac_code = """
            walker test_sentiment {
                can sentiment.predict;
                report sentiment.predict(["I'm feeling great!"]);
            }
        """

        # Load the first action module
        load_module_actions("jac_nlp.cl_summer")

        # Store the initial number of subprocesses
        initial_subprocess_count = len(act_procs)

        # Perform tests for the first action module
        sent = Sentinel(m_id=0, h=JsOrc.hook())
        sent.register_code(summarize_jac_code)
        root_node = sent.arch_ids.get_obj_by_name("root", kind="node").run()
        test_walker = sent.run_architype("test_summarize")
        test_walker.prime(root_node)
        test_walker.run()

        # Load the second action module
        load_module_actions("jac_nlp.sentiment")

        # Assert that the number of subprocesses has increased
        self.assertGreater(len(act_procs), initial_subprocess_count)

        # Perform tests for the second action module
        sent = Sentinel(m_id=0, h=JsOrc.hook())
        sent.register_code(sentiment_jac_code)
        root_node = sent.arch_ids.get_obj_by_name("root", kind="node").run()
        test_walker = sent.run_architype("test_sentiment")
        test_walker.prime(root_node)
        test_walker.run()

        # Load the third action module
        load_module_actions("jac_nlp.bi_enc")

        # Assert that the number of subprocesses has increased again
        self.assertGreater(len(act_procs), initial_subprocess_count)

        # Perform tests for the third action module
        sent = Sentinel(m_id=0, h=JsOrc.hook())
        sent.register_code(bi_enc_jac_code)
        root_node = sent.arch_ids.get_obj_by_name("root", kind="node").run()
        test_walker = sent.run_architype("test_bi_enc")
        test_walker.prime(root_node)
        test_walker.run()

        # Unload the first action module
        unload_module("jac_nlp.cl_summer")
        # Unload the second action module
        unload_module("jac_nlp.sentiment")
        # Unload the thrid action module
        unload_module("jac_nlp.bi_enc")
        # Assert that the number of subprocesses has decreased
        self.assertLess(len(act_procs), initial_subprocess_count)

    def test_load_unload_load_action_module(self):
        """Test loading, unloading, and loading again of an action module"""
        summarize_jac_code = """
            walker test_summarize {
                can cl_summer.summarize;
                report cl_summer.summarize("Today is a beautiful day.");
            }
        """

        # Load the action module
        load_module_actions("jac_nlp.cl_summer")

        # Store the initial number of subprocesses
        initial_subprocess_count = len(act_procs)

        # Perform tests for the initial loaded module
        sent = Sentinel(m_id=0, h=JsOrc.hook())
        sent.register_code(summarize_jac_code)
        root_node = sent.arch_ids.get_obj_by_name("root", kind="node").run()
        test_walker = sent.run_architype("test_summarize")
        test_walker.prime(root_node)
        test_walker.run()

        # Unload the action module
        unload_module("jac_nlp.cl_summer")

        # Assert that the number of subprocesses has decreased
        self.assertLess(len(act_procs), initial_subprocess_count)

        # Load the same action module again
        load_module_actions("jac_nlp.cl_summer")

        # Assert that the number of subprocesses has increased
        self.assertEqual(len(act_procs), initial_subprocess_count)

        # Perform tests after loading the module again
        sent = Sentinel(m_id=0, h=JsOrc.hook())
        sent.register_code(summarize_jac_code)
        root_node = sent.arch_ids.get_obj_by_name("root", kind="node").run()
        test_walker = sent.run_architype("test_summarize")
        test_walker.prime(root_node)
        test_walker.run()

        # Unload the module again
        unload_module("jac_nlp.cl_summer")

        # Assert that the number of subprocesses has decreased again
        self.assertLess(len(act_procs), initial_subprocess_count)
