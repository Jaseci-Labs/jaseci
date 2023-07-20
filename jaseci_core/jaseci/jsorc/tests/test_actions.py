from unittest import TestCase
from unittest.mock import patch
from jaseci.utils.utils import TestCaseHelper
import jaseci.jsorc.live_actions as jla
import jaseci.jsorc.remote_actions as jra
from jaseci.jsorc.live_actions import gen_remote_func_hook
from pydantic import BaseModel
from typing import Any, List, Mapping, Optional


class RequestBody(BaseModel):
    a: str
    b: str
    c: str
    d: Optional[List[Any]] = None
    e: str = None
    f: str = ""
    g: Optional[Mapping[Any, Any]] = None


def proc_req_body(route, body: RequestBody):
    if "d" in body.__dict__:
        body.__dict__["*d"] = body.__dict__.pop("d")
    if "g" in body.__dict__:
        body.__dict__["**g"] = body.__dict__.pop("g")
    return route(body)


class JacActionsTests(TestCaseHelper, TestCase):
    """Unit tests for Jac language"""

    def setUp(self):
        super().setUp()
        jra.remote_actions = {}
        jra.registered_apis = []
        jra.registered_endpoints = []

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

    @patch("requests.post")
    def test_remote_action_with_args_only(self, mock_post):
        @jla.jaseci_action(act_group=["test"], allow_remote=True)
        def args(a, b, c, *d, e=None, f=""):
            return {"a": a, "b": b, "c": c, "*d": d, "e": e, "f": f}

        app = jra.serv_actions()
        self.assertEqual(
            jra.remote_actions,
            {"test.args": ["a", "b", "c", "*d", "e", "f"]},
        )

        remote_action = gen_remote_func_hook(
            url="https://example.com/api/v1/endpoint",
            act_name="test.args",
            param_names=["a", "b", "c", "*d", "e", "f"],
        )

        #################################################
        # --------------- complete call --------------- #
        #################################################

        remote_action(
            "1",  # a
            "2",  # b
            "3",  # c
            "4",  # inside "*d": [4]
            "5",  # inside "*d": [4, 5]
            "6",  # inside "*d": [4, 5, 6]
            e="1",  # e
            f="2",  # f
        )

        self.assertEqual(
            {
                "a": "1",
                "b": "2",
                "c": "3",
                "*d": ["4", "5", "6"],
                "e": "1",
                "f": "2",
            },
            mock_post.call_args[1]["json"],
        )

        #################################################
        # ---------------- no args call --------------- #
        #################################################

        remote_action(
            "1",  # a
            "2",  # b
            "3",  # c
            e="1",  # e
            f="2",  # f
        )

        self.assertEqual(
            {
                "a": "1",
                "b": "2",
                "c": "3",
                "e": "1",
                "f": "2",
            },
            mock_post.call_args[1]["json"],
        )

        # --------------------------------------------- action call --------------------------------------------- #

        route = app.routes[-1].endpoint

        ########################################################
        # --------------- complete action call --------------- #
        ########################################################

        self.assertEqual(
            {
                "a": "1",
                "b": "2",
                "c": "3",
                "*d": ("4", "5", "6"),
                "e": "1",
                "f": "2",
            },
            proc_req_body(
                route,
                RequestBody(
                    a="1",
                    b="2",
                    c="3",
                    d=["4", "5", "6"],
                    e="1",
                    f="2",
                ),
            ),
        )

        ########################################################
        # ---------------- no args action call --------------- #
        ########################################################

        self.assertEqual(
            {
                "a": "1",
                "b": "2",
                "c": "3",
                "*d": (),
                "e": "1",
                "f": "2",
            },
            proc_req_body(
                route,
                RequestBody(
                    a="1",
                    b="2",
                    c="3",
                    e="1",
                    f="2",
                ),
            ),
        )

    @patch("requests.post")
    def test_remote_action_with_kwargs_only(self, mock_post):
        @jla.jaseci_action(act_group=["test"], allow_remote=True)
        def kwargs(a, b, c, e=None, f="", **g):
            return {"a": a, "b": b, "c": c, "e": e, "f": f, "**g": g}

        app = jra.serv_actions()
        self.assertEqual(
            jra.remote_actions,
            {"test.kwargs": ["a", "b", "c", "e", "f", "**g"]},
        )

        remote_action = gen_remote_func_hook(
            url="https://example.com/api/v1/endpoint",
            act_name="test.kwargs",
            param_names=["a", "b", "c", "e", "f", "**g"],
        )

        #################################################
        # --------------- complete call --------------- #
        #################################################

        remote_action(
            "1",  # a
            "2",  # b
            "3",  # c
            e="1",  # e
            f="2",  # f
            g="3",  # inside "**g": {"g": 3}
            h="4",  # inside "**g": {"g": 3, "h": 4}
            i="5",  # inside "**g": {"g": 3, "h": 4, "i": 5}
        )

        self.assertEqual(
            {
                "a": "1",
                "b": "2",
                "c": "3",
                "e": "1",
                "f": "2",
                "**g": {"g": "3", "h": "4", "i": "5"},
            },
            mock_post.call_args[1]["json"],
        )

        #################################################
        # --------------- no kwargs call -------------- #
        #################################################

        remote_action(
            "1",  # a
            "2",  # b
            "3",  # c
            e="1",  # e
            f="2",  # f
        )

        self.assertEqual(
            {"a": "1", "b": "2", "c": "3", "e": "1", "f": "2"},
            mock_post.call_args[1]["json"],
        )

        # --------------------------------------------- action call --------------------------------------------- #

        route = app.routes[-1].endpoint

        ########################################################
        # --------------- complete action call --------------- #
        ########################################################

        self.assertEqual(
            {
                "a": "1",
                "b": "2",
                "c": "3",
                "e": "1",
                "f": "2",
                "**g": {"g": "3", "h": "4", "i": "5"},
            },
            proc_req_body(
                route,
                RequestBody(
                    a="1",
                    b="2",
                    c="3",
                    e="1",
                    f="2",
                    g={"g": "3", "h": "4", "i": "5"},
                ),
            ),
        )

        ########################################################
        # --------------- no kwargs action call -------------- #
        ########################################################

        self.assertEqual(
            {
                "a": "1",
                "b": "2",
                "c": "3",
                "e": "1",
                "f": "2",
                "**g": {},
            },
            proc_req_body(route, RequestBody(a="1", b="2", c="3", e="1", f="2")),
        )

    @patch("requests.post")
    def test_remote_action_with_args_kwargs(self, mock_post):
        @jla.jaseci_action(act_group=["test"], allow_remote=True)
        def args_kwargs(a, b, c, *d, e=None, f="", **g):
            return {"a": a, "b": b, "c": c, "*d": d, "e": e, "f": f, "**g": g}

        app = jra.serv_actions()
        self.assertEqual(
            jra.remote_actions,
            {"test.args_kwargs": ["a", "b", "c", "*d", "e", "f", "**g"]},
        )

        remote_action = gen_remote_func_hook(
            url="https://example.com/api/v1/endpoint",
            act_name="test.args_kwargs",
            param_names=["a", "b", "c", "*d", "e", "f", "**g"],
        )

        #################################################
        # --------------- complete call --------------- #
        #################################################

        remote_action(
            "1",  # a
            "2",  # b
            "3",  # c
            "4",  # inside "*d": [4]
            "5",  # inside "*d": [4, 5]
            "6",  # inside "*d": [4, 5, 6]
            e="1",  # e
            f="2",  # f
            g="3",  # inside "**g": {"g": 3}
            h="4",  # inside "**g": {"g": 3, "h": 4}
            i="5",  # inside "**g": {"g": 3, "h": 4, "i": 5}
        )

        self.assertEqual(
            {
                "a": "1",
                "b": "2",
                "c": "3",
                "*d": ["4", "5", "6"],
                "e": "1",
                "f": "2",
                "**g": {"g": "3", "h": "4", "i": "5"},
            },
            mock_post.call_args[1]["json"],
        )

        #################################################
        # --------------- no kwargs call -------------- #
        #################################################

        remote_action(
            "1",  # a
            "2",  # b
            "3",  # c
            "4",  # inside "*d": [4]
            "5",  # inside "*d": [4, 5]
            "6",  # inside "*d": [4, 5, 6]
            e="1",  # e
            f="2",  # f
        )

        self.assertEqual(
            {"a": "1", "b": "2", "c": "3", "*d": ["4", "5", "6"], "e": "1", "f": "2"},
            mock_post.call_args[1]["json"],
        )

        #################################################
        # ---------------- no args call --------------- #
        #################################################

        remote_action(
            "1",  # a
            "2",  # b
            "3",  # c
            e="1",  # e
            f="2",  # f
            g="3",  # inside "**g": {"g": 3}
            h="4",  # inside "**g": {"g": 3, "h": 4}
            i="5",  # inside "**g": {"g": 3, "h": 4, "i": 5}
        )

        self.assertEqual(
            {
                "a": "1",
                "b": "2",
                "c": "3",
                "e": "1",
                "f": "2",
                "**g": {"g": "3", "h": "4", "i": "5"},
            },
            mock_post.call_args[1]["json"],
        )

        #################################################
        # ---------- no args and kwargs call ---------- #
        #################################################

        remote_action(
            "1",  # a
            "2",  # b
            "3",  # c
            e="1",  # e
            f="2",  # f
        )

        self.assertEqual(
            {"a": "1", "b": "2", "c": "3", "e": "1", "f": "2"},
            mock_post.call_args[1]["json"],
        )

        # --------------------------------------------- action call --------------------------------------------- #

        route = app.routes[-1].endpoint

        ########################################################
        # --------------- complete action call --------------- #
        ########################################################

        self.assertEqual(
            {
                "a": "1",
                "b": "2",
                "c": "3",
                "*d": ("4", "5", "6"),
                "e": "1",
                "f": "2",
                "**g": {"g": "3", "h": "4", "i": "5"},
            },
            proc_req_body(
                route,
                RequestBody(
                    a="1",
                    b="2",
                    c="3",
                    d=["4", "5", "6"],
                    e="1",
                    f="2",
                    g={"g": "3", "h": "4", "i": "5"},
                ),
            ),
        )

        ########################################################
        # --------------- no kwargs action call -------------- #
        ########################################################

        self.assertEqual(
            {
                "a": "1",
                "b": "2",
                "c": "3",
                "*d": ("4", "5", "6"),
                "e": "1",
                "f": "2",
                "**g": {},
            },
            proc_req_body(
                route, RequestBody(a="1", b="2", c="3", d=["4", "5", "6"], e="1", f="2")
            ),
        )

        ########################################################
        # ---------------- no args action call --------------- #
        ########################################################

        self.assertEqual(
            {
                "a": "1",
                "b": "2",
                "c": "3",
                "*d": (),
                "e": "1",
                "f": "2",
                "**g": {"g": "3", "h": "4", "i": "5"},
            },
            proc_req_body(
                route,
                RequestBody(
                    a="1",
                    b="2",
                    c="3",
                    e="1",
                    f="2",
                    g={"g": "3", "h": "4", "i": "5"},
                ),
            ),
        )

        ########################################################
        # ---------- no args and kwargs action call ---------- #
        ########################################################

        self.assertEqual(
            {
                "a": "1",
                "b": "2",
                "c": "3",
                "*d": (),
                "e": "1",
                "f": "2",
                "**g": {},
            },
            proc_req_body(route, RequestBody(a="1", b="2", c="3", e="1", f="2")),
        )

    def test_setup_decorated_as_startup(self):
        @jla.jaseci_action(act_group=["ex"], allow_remote=True)
        def setup(param: str = ""):
            pass

        app = jra.serv_actions()
        assert len(app.__dict__["router"].__dict__["on_startup"]) == 1
