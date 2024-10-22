"""Test utils."""

from contextlib import suppress
from os import environ
from subprocess import Popen, run
from typing import Literal, overload
from unittest import TestCase

from httpx import get, post

from yaml import safe_load


class JacCloudTest(TestCase):
    """Test Utils."""

    def run_server(
        self,
        file: str,
        port: int = 8000,
        database: str = "jaseci",
        envs: dict | None = None,
        wait: int = 5,
        mini: bool = False,
    ) -> None:
        """Run server."""
        run(["fuser", "-k", f"{port}/tcp"])
        run(["jac", "clean"])
        run(["jac", "tool", "gen_parser"])

        base_envs = environ.copy()
        base_envs["DATABASE_NAME"] = database
        base_envs.update(envs or {"DATABASE_NAME": database})

        self.server = Popen(
            ["jac", "serve", f"{file}", "--port", f"{port}"], env=base_envs
        )

        run(["sleep", f"{wait}"])

        self.host = f"http://0.0.0.0:{port}"
        self.database = database
        self.users: list[dict] = []

        self.root_id_prefix = "" if mini else "n::"

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

    def stop_server(self) -> None:
        """Stop server."""
        self.server.kill()

    def check_server(self) -> None:
        """Retrieve OpenAPI Specs JSON."""
        res = get(f"{self.host}/healthz")
        res.raise_for_status()
        self.assertEqual(200, res.status_code)

    def trigger_openapi_specs_test(self, yaml: str) -> None:
        """Test OpenAPI Specs."""
        res = get(f"{self.host}/openapi.yaml", timeout=1)
        res.raise_for_status()

        with open(yaml) as file:
            self.assertEqual(safe_load(file), safe_load(res.text))

    @overload
    def post_api(self, api: str, json: dict | None = None, user: int = 0) -> dict:
        pass

    @overload
    def post_api(
        self,
        api: str,
        json: dict | None = None,
        user: int = 0,
        expect_error: Literal[True] = True,
    ) -> int:
        pass

    def post_api(
        self,
        api: str,
        json: dict | None = None,
        user: int = 0,
        expect_error: bool = False,
    ) -> dict | int:
        """Call walker post API."""
        res = post(
            f"{self.host}/walker/{api}",
            json=json,
            headers=self.users[user]["headers"] if self.users else None,
        )

        if not expect_error:
            res.raise_for_status()
            return res.json()
        else:
            return res.status_code

    def trigger_create_user_test(self, suffix: str = "", has_name: bool = True) -> None:
        """Test User Creation."""
        email = f"user{suffix}@example.com"

        res = post(
            f"{self.host}/user/register",
            json={
                "password": "string",
                "email": email,
                "name": "string",
            },
        )
        res.raise_for_status()
        self.assertEqual({"message": "Successfully Registered!"}, res.json())

        res = post(
            f"{self.host}/user/login",
            json={"email": email, "password": "string"},
        )
        res.raise_for_status()
        body: dict = res.json()

        token = body.get("token")
        self.assertIsNotNone(token)

        user: dict = body.get("user", {})
        self.assertEqual(email, user["email"])

        if has_name:
            self.assertEqual("string", user["name"])

        self.users.append(
            {"user": user, "headers": {"Authorization": f"Bearer {token}"}}
        )

    def trigger_create_graph_test(self) -> None:
        """Test Graph Creation."""
        res = self.post_api("create_graph")

        self.assertEqual(200, res["status"])
        self.assertNotIn("returns", res)

        root_node = res["reports"].pop(0)
        self.assertTrue(root_node["id"].startswith(self.root_id_prefix))
        self.assertEqual({}, root_node["context"])

        for idx, report in enumerate(res["reports"]):
            self.assertEqual({"val": idx}, report["context"])

    def trigger_traverse_graph_test(self) -> None:
        """Test Graph Traversion."""
        res = self.post_api("traverse_graph")

        self.assertEqual(200, res["status"])
        self.assertNotIn("returns", res)

        root_node = res["reports"].pop(0)
        self.assertTrue(root_node["id"].startswith(self.root_id_prefix))
        self.assertEqual({}, root_node["context"])

        for idx, report in enumerate(res["reports"]):
            self.assertEqual({"val": idx}, report["context"])

            res = self.post_api(f"traverse_graph/{report["id"]}")
            self.assertEqual(200, res["status"])
            self.assertNotIn("returns", res)
            for _idx, report in enumerate(res["reports"]):
                self.assertEqual({"val": idx + _idx}, report["context"])

    def trigger_detach_node_test(self) -> None:
        """Test detach node."""
        res = self.post_api("detach_node")

        self.assertEqual(200, res["status"])
        self.assertEqual([True], res["returns"])
        self.assertNotIn("reports", res)

        res = self.post_api("traverse_graph")
        self.assertEqual(200, res["status"])
        self.assertNotIn("returns", res)

        root_node = res["reports"].pop(0)
        self.assertTrue(root_node["id"].startswith(self.root_id_prefix))
        self.assertEqual({}, root_node["context"])

        for idx, report in enumerate(res["reports"]):
            self.assertEqual({"val": idx}, report["context"])

            res = self.post_api(f"traverse_graph/{report["id"]}")
            self.assertEqual(200, res["status"])
            self.assertNotIn("returns", res)
            for _idx, report in enumerate(res["reports"]):
                self.assertEqual({"val": idx + _idx}, report["context"])

    def trigger_update_graph_test(self) -> None:
        """Test update graph."""
        res = self.post_api("update_graph")

        self.assertEqual(200, res["status"])
        self.assertNotIn("returns", res)

        root_node = res["reports"].pop(0)
        self.assertTrue(root_node["id"].startswith(self.root_id_prefix))
        self.assertEqual({}, root_node["context"])

        for idx, report in enumerate(res["reports"]):
            self.assertEqual({"val": idx + 1}, report["context"])

        res = self.post_api("traverse_graph")

        self.assertEqual(200, res["status"])
        self.assertNotIn("returns", res)

        root_node = res["reports"].pop(0)
        self.assertTrue(root_node["id"].startswith(self.root_id_prefix))
        self.assertEqual({}, root_node["context"])

        for idx, report in enumerate(res["reports"]):
            self.assertEqual({"val": idx + 1}, report["context"])

            res = self.post_api(f"traverse_graph/{report["id"]}")
            self.assertEqual(200, res["status"])
            self.assertNotIn("returns", res)
            for _idx, report in enumerate(res["reports"]):
                self.assertEqual({"val": idx + _idx + 1}, report["context"])

    def trigger_create_nested_node_test(self, manual: bool = False) -> None:
        """Test create nested node."""
        res = self.post_api(f"{'manual_' if manual else ""}create_nested_node", user=1)

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
                        "enum_field": "C",
                    },
                    "enum_field": "B",
                },
                "enum_field": "A",
            },
            res["returns"][0]["context"],
        )

    def trigger_update_nested_node_test(
        self, manual: bool = False, user: int = 1
    ) -> None:
        """Test update nested node."""
        for walker in [
            f"{'manual_' if manual else ""}update_nested_node",
            "visit_nested_node",
        ]:
            res = self.post_api(walker, user=user)
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
                            "enum_field": "A",
                        },
                        "enum_field": "C",
                    },
                    "enum_field": "B",
                },
                res["returns"][0]["context"],
            )

    def trigger_detach_nested_node_test(self, manual: bool = False) -> None:
        """Test detach nested node."""
        res = self.post_api(f"{'manual_' if manual else ""}detach_nested_node", user=1)
        self.assertEqual(200, res["status"])
        self.assertEqual([True], res["returns"])

        res = self.post_api("visit_nested_node", user=1)
        self.assertEqual(200, res["status"])
        self.assertEqual([[]], res["returns"])

    def trigger_delete_nested_node_test(self, manual: bool = False) -> None:
        """Test create nested node."""
        res = self.post_api(f"{'manual_' if manual else ""}delete_nested_node", user=1)
        self.assertEqual(200, res["status"])
        self.assertEqual([[]], res["reports"])

        res = self.post_api("visit_nested_node", user=1)
        self.assertEqual(200, res["status"])
        self.assertEqual([[]], res["returns"])

    def trigger_delete_nested_edge_test(self, manual: bool = False) -> None:
        """Test create nested node."""
        res = self.post_api(f"{'manual_' if manual else ""}delete_nested_edge", user=1)
        self.assertEqual(200, res["status"])
        self.assertEqual([[]], res["reports"])

        res = self.post_api("visit_nested_node", user=1)
        self.assertEqual(200, res["status"])
        self.assertEqual([[]], res["returns"])

    def trigger_access_validation_test(
        self, give_access_to_full_graph: bool, via_all: bool = False
    ) -> None:
        """Test giving access to node or full graph."""
        res = self.post_api("create_nested_node", user=1)

        nested_node = res["returns"][0]

        allow_walker_suffix = (
            "" if give_access_to_full_graph else f'/{nested_node["id"]}'
        )

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
                        "enum_field": "C",
                    },
                    "enum_field": "B",
                },
                "enum_field": "A",
            },
            nested_node["context"],
        )

        ###################################################
        #                    NO ACCESS                    #
        ###################################################

        self.assertEqual(
            403,
            self.post_api(f"visit_nested_node/{nested_node['id']}", expect_error=True),
        )

        ###################################################
        #          WITH ALLOWED ROOT READ ACCESS          #
        ###################################################

        res = self.post_api(
            f"allow_other_root_access{allow_walker_suffix}",
            json={
                "root_id": f'n::{self.users[0]["user"]["root_id"]}',
                "via_all": via_all,
            },
            user=1,
        )
        self.assertEqual(200, res["status"])

        res = self.post_api(f"update_nested_node/{nested_node['id']}")
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
                        "enum_field": "A",
                    },
                    "enum_field": "C",
                },
                "enum_field": "B",
            },
            res["returns"][0]["context"],
        )

        # ----------- NO UPDATE SHOULD HAPPEN ----------- #

        res = self.post_api(f"visit_nested_node/{nested_node['id']}")
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
                        "enum_field": "C",
                    },
                    "enum_field": "B",
                },
                "enum_field": "A",
            },
            res["returns"][0]["context"],
        )

        ###################################################
        #          WITH ALLOWED ROOT WRITE ACCESS         #
        ###################################################

        res = self.post_api(
            f"allow_other_root_access{allow_walker_suffix}",
            json={
                "root_id": f'n::{self.users[0]["user"]["root_id"]}',
                "level": "WRITE",
                "via_all": via_all,
            },
            user=1,
        )
        self.assertEqual(200, res["status"])

        res = self.post_api(f"update_nested_node/{nested_node['id']}")
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
                        "enum_field": "A",
                    },
                    "enum_field": "C",
                },
                "enum_field": "B",
            },
            res["returns"][0]["context"],
        )

        # ------------ UPDATE SHOULD REFLECT ------------ #

        res = self.post_api(f"visit_nested_node/{nested_node['id']}")
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
                        "enum_field": "A",
                    },
                    "enum_field": "C",
                },
                "enum_field": "B",
            },
            res["returns"][0]["context"],
        )

        ###################################################
        #                REMOVE ROOT ACCESS               #
        ###################################################

        res = self.post_api(
            f"disallow_other_root_access{allow_walker_suffix}",
            json={
                "root_id": f'n::{self.users[0]["user"]["root_id"]}',
                "via_all": via_all,
            },
            user=1,
        )
        self.assertEqual(200, res["status"])

        self.assertEqual(
            403,
            self.post_api(f"visit_nested_node/{nested_node['id']}", expect_error=True),
        )

    def nested_count_should_be(self, node: int, edge: int) -> None:
        """Test nested node count."""
        raise NotImplementedError(
            "nested_count_should_be is required to be implemented!"
        )

    def trigger_custom_status_code(self) -> None:
        """Test custom status code."""
        for acceptable_code in [200, 201, 202, 203, 205, 206, 207, 208, 226]:
            res = self.post_api("custom_status_code", {"status": acceptable_code})
            self.assertEqual(acceptable_code, res["status"])
            self.assertNotIn("returns", res)

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

    def trigger_custom_report(self) -> None:
        """Test custom status code."""
        res = self.post_api("custom_report")
        self.assertEqual({"testing": 1}, res)

    def trigger_upload_file(self) -> None:
        """Test upload file."""
        with open("jac_cloud/tests/simple_graph.jac", mode="br") as s:
            files = [
                ("single", ("simple_graph.jac", s)),
                ("multiple", ("simple_graph.jac", s)),
                ("multiple", ("simple_graph.jac", s)),
            ]
            res = post(
                f"{self.host}/walker/post_with_file",
                files=files,
                headers=self.users[0]["headers"] if self.users else None,
            )
            res.raise_for_status()
            data: dict = res.json()

            self.assertEqual(200, data["status"])
            self.assertEqual(
                [
                    {
                        "single": {
                            "single": {
                                "name": "simple_graph.jac",
                                "content_type": "application/octet-stream",
                                "size": 4813,
                            }
                        },
                        "multiple": [
                            {
                                "name": "simple_graph.jac",
                                "content_type": "application/octet-stream",
                                "size": 4813,
                            },
                            {
                                "name": "simple_graph.jac",
                                "content_type": "application/octet-stream",
                                "size": 4813,
                            },
                        ],
                        "singleOptional": None,
                    }
                ],
                data["reports"],
            )

    def trigger_visit_sequence(self) -> None:
        """Test visit sequence."""
        res = post(f"{self.host}/walker/visit_sequence").json()

        self.assertEqual(200, res["status"])
        self.assertEqual(
            [
                "walker entry",
                "walker enter to root",
                "a-1",
                "a-2",
                "a-3",
                "a-4",
                "a-5",
                "a-6",
                "b-1",
                "b-2",
                "b-3",
                "b-4",
                "b-5",
                "b-6",
                "c-1",
                "c-2",
                "c-3",
                "c-4",
                "c-5",
                "c-6",
                "walker exit",
            ],
            res["returns"],
        )

    def trigger_spawn_test(self) -> None:
        """Test spawn call behavior of walker."""
        res = self.post_api("WalkerTestSpawn")
        self.assertEqual(200, res["status"])
        reports = res["reports"]
        self.assertIn("Walker entry: Root()", reports[0]["message"])
        self.assertIn("Node entry: Root()", reports[1]["message"])
        for i in range(5):
            self.assertIn(f"Node exit: NodeTest(value={i})", reports[i + 2]["message"])
        self.assertIn("Walker exit: NodeTest(value=4)", reports[7]["message"])
        visitor_report = res["reports"][-1]
        visited_nodes = visitor_report["context"]["visited_nodes"]
        entry_count = visitor_report["context"]["entry_count"]
        exit_count = visitor_report["context"]["exit_count"]

        self.assertEqual(visited_nodes, [f"NodeTest(value={i})" for i in range(5)])
        self.assertEqual(entry_count, 1)
        self.assertEqual(exit_count, 1)
