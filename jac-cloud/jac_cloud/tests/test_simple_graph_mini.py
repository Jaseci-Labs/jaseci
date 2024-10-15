"""JacLang Jaseci Unit Test."""

from contextlib import suppress
from os import getenv, path
from shelve import open as shelf
from typing import Literal, overload
from unittest.async_case import IsolatedAsyncioTestCase

from httpx import get, post

from jaclang import jac_import
from jaclang.runtimelib.context import ExecutionContext

from yaml import safe_load


class SimpleGraphTest(IsolatedAsyncioTestCase):
    """JacLang Jaseci Feature Tests."""

    def __init__(self, methodName: str = "runTest") -> None:  # noqa: N803
        """Overide Init."""
        super().__init__(methodName)

        (base, ignored) = path.split(__file__)
        base = base if base else "./"

        jac_import(
            target="simple_graph_mini",
            base_path=base,
            cachable=True,
            override_name="__main__",
        )

    async def asyncSetUp(self) -> None:
        """Reset DB and wait for server."""
        self.host = "http://0.0.0.0:8001"
        self.database = getenv("DATABASE", "database")
        count = 0
        while True:
            if count > 5:
                self.check_server()
                break
            else:
                with suppress(Exception):
                    self.check_server()
                    break
            count += 1

    async def asyncTearDown(self) -> None:
        """Clean up DB."""
        self.clear_db()

    def clear_db(self) -> None:
        """Clean DB."""
        with shelf(self.database) as sh:
            sh.clear()
            sh.sync()

    @overload
    def post_api(self, api: str, json: dict | None = None) -> dict:
        pass

    @overload
    def post_api(
        self,
        api: str,
        json: dict | None = None,
        expect_error: Literal[True] = True,
    ) -> int:
        pass

    def post_api(
        self,
        api: str,
        json: dict | None = None,
        expect_error: bool = False,
    ) -> dict | int:
        """Call walker post API."""
        res = post(f"{self.host}/walker/{api}", json=json)

        if not expect_error:
            res.raise_for_status()
            return res.json()
        else:
            return res.status_code

    def check_server(self) -> None:
        """Retrieve OpenAPI Specs JSON."""
        res = get(f"{self.host}/healthz")
        res.raise_for_status()
        self.assertEqual(200, res.status_code)

    def trigger_openapi_specs_test(self) -> None:
        """Test OpenAPI Specs."""
        res = get(f"{self.host}/openapi.yaml", timeout=1)
        res.raise_for_status()

        with open("jac_cloud/tests/openapi_specs_mini.yaml") as file:
            self.assertEqual(safe_load(file), safe_load(res.text))

    def trigger_create_graph_test(self) -> None:
        """Test Graph Creation."""
        res = self.post_api("create_graph")

        self.assertEqual(200, res["status"])
        self.assertEqual(4, len(res["reports"]))

        root_node = res["reports"].pop(0)
        self.assertEqual("00000000000000000000000000000000", root_node["id"])
        self.assertEqual({}, root_node["context"])

        for idx, report in enumerate(res["reports"]):
            self.assertEqual({"val": idx}, report["context"])

    def trigger_traverse_graph_test(self) -> None:
        """Test Graph Traversion."""
        res = self.post_api("traverse_graph")

        self.assertEqual(200, res["status"])
        self.assertEqual(4, len(res["reports"]))

        root_node = res["reports"].pop(0)
        self.assertEqual("00000000000000000000000000000000", root_node["id"])
        self.assertEqual({}, root_node["context"])

        for idx, report in enumerate(res["reports"]):
            self.assertEqual({"val": idx}, report["context"])

            res = self.post_api(f"traverse_graph/{report["id"]}")
            self.assertEqual(200, res["status"])
            for _idx, report in enumerate(res["reports"]):
                self.assertEqual({"val": idx + _idx}, report["context"])

    def trigger_detach_node_test(self) -> None:
        """Test detach node."""
        res = self.post_api("detach_node")

        self.assertEqual(200, res["status"])
        self.assertEqual([True], res["reports"])

        res = self.post_api("traverse_graph")
        self.assertEqual(200, res["status"])
        self.assertEqual(3, len(res["reports"]))

        root_node = res["reports"].pop(0)
        self.assertEqual("00000000000000000000000000000000", root_node["id"])
        self.assertEqual({}, root_node["context"])

        for idx, report in enumerate(res["reports"]):
            self.assertEqual({"val": idx}, report["context"])

            res = self.post_api(f"traverse_graph/{report["id"]}")
            self.assertEqual(200, res["status"])
            for _idx, report in enumerate(res["reports"]):
                self.assertEqual({"val": idx + _idx}, report["context"])

    def trigger_update_graph_test(self) -> None:
        """Test update graph."""
        res = self.post_api("update_graph")

        self.assertEqual(200, res["status"])
        self.assertEqual(3, len(res["reports"]))

        root_node = res["reports"].pop(0)
        self.assertEqual("00000000000000000000000000000000", root_node["id"])
        self.assertEqual({}, root_node["context"])

        for idx, report in enumerate(res["reports"]):
            self.assertEqual({"val": idx + 1}, report["context"])

        res = self.post_api("traverse_graph")

        self.assertEqual(200, res["status"])
        self.assertEqual(3, len(res["reports"]))

        root_node = res["reports"].pop(0)
        self.assertEqual("00000000000000000000000000000000", root_node["id"])
        self.assertEqual({}, root_node["context"])

        for idx, report in enumerate(res["reports"]):
            self.assertEqual({"val": idx + 1}, report["context"])

            res = self.post_api(f"traverse_graph/{report["id"]}")
            self.assertEqual(200, res["status"])
            for _idx, report in enumerate(res["reports"]):
                self.assertEqual({"val": idx + _idx + 1}, report["context"])

    def trigger_create_nested_node_test(self, manual: bool = False) -> None:
        """Test create nested node."""
        res = self.post_api("create_nested_node")

        self.assertEqual(200, res["status"])
        self.assertEqual(
            {
                "val": 0,
                "arr": [],
                "json": {},
                "parent": {
                    "val": 1,
                    "arr": [1],
                    "json": {"a": 1},
                    "child": {
                        "val": 2,
                        "arr": [1, 2],
                        "json": {"a": 1, "b": 2},
                        "enum_field": "c",
                    },
                    "enum_field": "b",
                },
                "enum_field": "a",
            },
            res["reports"][0]["context"],
        )

    def trigger_update_nested_node_test(self) -> None:
        """Test update nested node."""
        for walker in ["update_nested_node", "visit_nested_node"]:
            res = self.post_api(walker)
            self.assertEqual(200, res["status"])
            self.assertEqual(
                {
                    "val": 1,
                    "arr": [1],
                    "json": {"a": 1},
                    "parent": {
                        "val": 2,
                        "arr": [1, 2],
                        "json": {"a": 1, "b": 2},
                        "child": {
                            "val": 3,
                            "arr": [1, 2, 3],
                            "json": {"a": 1, "b": 2, "c": 3},
                            "enum_field": "a",
                        },
                        "enum_field": "c",
                    },
                    "enum_field": "b",
                },
                res["reports"][0]["context"],
            )

    def trigger_detach_nested_node_test(self, manual: bool = False) -> None:
        """Test detach nested node."""
        res = self.post_api("detach_nested_node")
        self.assertEqual(200, res["status"])
        self.assertEqual([True], res["reports"])

        res = self.post_api("visit_nested_node")
        self.assertEqual(200, res["status"])
        self.assertEqual([[]], res["reports"])

    def trigger_delete_nested_node_test(self, manual: bool = False) -> None:
        """Test create nested node."""
        res = self.post_api("delete_nested_node")
        self.assertEqual(200, res["status"])
        self.assertEqual([[]], res["reports"])

        res = self.post_api("visit_nested_node")
        self.assertEqual(200, res["status"])
        self.assertEqual([[]], res["reports"])

    def trigger_delete_nested_edge_test(self, manual: bool = False) -> None:
        """Test create nested node."""
        res = self.post_api("delete_nested_edge")
        self.assertEqual(200, res["status"])
        self.assertEqual([[]], res["reports"])

        res = self.post_api("visit_nested_node")
        self.assertEqual(200, res["status"])
        self.assertEqual([[]], res["reports"])

    def nested_count_should_be(self, node: int, edge: int) -> None:
        """Test nested node count."""
        jctx = ExecutionContext.create(session=self.database)

        node_count = 0
        edge_count = 0

        for val in jctx.mem.__shelf__.values():
            if val.architype.__class__.__name__ == "Nested":
                node_count += 1
            elif (
                (source := getattr(val, "source", None))
                and (target := getattr(val, "target", None))
                and (
                    source.architype.__class__.__name__ == "Nested"
                    or target.architype.__class__.__name__ == "Nested"
                )
            ):
                edge_count += 1

        self.assertEqual(node, node_count)
        self.assertEqual(edge, edge_count)

        jctx.close()

    def trigger_custom_status_code(self) -> None:
        """Test custom status code."""
        for acceptable_code in [200, 201, 202, 203, 205, 206, 207, 208, 226]:
            res = self.post_api("custom_status_code", {"status": acceptable_code})
            self.assertEqual(acceptable_code, res["status"])
            self.assertEqual([], res["reports"])

        for error_code in [
            400,
            401,
            402,
            403,
            404,
            405,
            406,
            407,
            408,
            409,
            410,
            411,
            412,
            413,
            414,
            415,
            416,
            417,
            418,
            421,
            422,
            423,
            424,
            425,
            426,
            428,
            429,
            431,
            451,
            500,
            501,
            502,
            503,
            504,
            505,
            506,
            507,
            508,
            510,
            511,
        ]:
            self.assertEqual(
                error_code,
                self.post_api(
                    "custom_status_code", {"status": error_code}, expect_error=True
                ),
            )

        for invalid_code in [
            100,
            101,
            102,
            103,
            204,
            300,
            301,
            302,
            303,
            304,
            305,
            306,
            307,
            308,
        ]:
            self.assertRaises(
                Exception, self.post_api, "custom_status_code", {"status": invalid_code}
            )

    async def test_all_features(self) -> None:
        """Test Full Features."""
        self.trigger_openapi_specs_test()

        self.trigger_create_graph_test()
        self.trigger_traverse_graph_test()
        self.trigger_detach_node_test()
        self.trigger_update_graph_test()

        ###################################################
        #                   VIA DETACH                    #
        ###################################################

        self.clear_db()

        self.nested_count_should_be(node=0, edge=0)

        self.trigger_create_nested_node_test()
        self.nested_count_should_be(node=1, edge=1)

        self.trigger_update_nested_node_test()
        self.trigger_detach_nested_node_test()
        self.nested_count_should_be(node=0, edge=0)

        ###################################################
        #                   VIA DESTROY                   #
        ###################################################

        self.trigger_create_nested_node_test()
        self.nested_count_should_be(node=1, edge=1)

        self.trigger_delete_nested_node_test()
        self.nested_count_should_be(node=0, edge=0)

        self.trigger_create_nested_node_test()
        self.nested_count_should_be(node=1, edge=1)

        self.trigger_delete_nested_edge_test()
        self.nested_count_should_be(node=0, edge=0)

        ###################################################
        #                  CUSTOM STATUS                  #
        ###################################################

        self.trigger_custom_status_code()
