"""JacLang Jaseci Unit Test."""

from contextlib import suppress
from json import load
from os import getenv
from typing import Literal, overload
from unittest.async_case import IsolatedAsyncioTestCase

from httpx import get, post

from ..jaseci.datasources import Collection


class SimpleGraphTest(IsolatedAsyncioTestCase):
    """JacLang Jaseci Feature Tests."""

    async def asyncSetUp(self) -> None:
        """Reset DB and wait for server."""
        self.host = "http://0.0.0.0:8001"
        Collection.__client__ = None
        Collection.__database__ = None
        self.client = Collection.get_client()
        self.users: list[dict] = []
        self.database = getenv("DATABASE_NAME", "jaclang")
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
        await self.client.drop_database(self.database)

    @overload
    def post_api(self, api: str, json: dict | None = None, user: int = 0) -> dict:
        pass

    @overload
    def post_api(
        self,
        api: str,
        json: dict | None,
        user: int,
        expect_error: Literal[True],
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
            f"{self.host}/walker/{api}", json=json, headers=self.users[user]["headers"]
        )

        if not expect_error:
            res.raise_for_status()
            return res.json()
        else:
            return res.status_code

    def check_server(self) -> dict:
        """Retrieve OpenAPI Specs JSON."""
        res = get(f"{self.host}/healthz")
        res.raise_for_status()

    def trigger_openapi_specs_test(self) -> None:
        """Test OpenAPI Specs."""
        res = get(f"{self.host}/openapi.json", timeout=1)
        res.raise_for_status()

        with open("jaclang_jaseci/tests/openapi_specs.json") as file:
            self.assertEqual(load(file), res.json())

    def trigger_create_user_test(self, suffix: str = "") -> None:
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
        self.assertEqual("string", user["name"])

        self.users.append(
            {"user": user, "headers": {"Authorization": f"Bearer {token}"}}
        )

    def trigger_create_graph_test(self) -> None:
        """Test Graph Creation."""
        res = self.post_api("create_graph")

        self.assertEqual(200, res["status"])
        self.assertEqual([None], res["returns"])

        root_node = res["reports"].pop(0)
        self.assertTrue(root_node["id"].startswith("n::"))
        self.assertEqual({}, root_node["context"])

        for idx, report in enumerate(res["reports"]):
            self.assertEqual({"val": idx}, report["context"])

    def trigger_traverse_graph_test(self) -> None:
        """Test Graph Traversion."""
        res = self.post_api("traverse_graph")

        self.assertEqual(200, res["status"])
        self.assertEqual([None, None, None, None], res["returns"])

        root_node = res["reports"].pop(0)
        self.assertTrue(root_node["id"].startswith("n::"))
        self.assertEqual({}, root_node["context"])

        for idx, report in enumerate(res["reports"]):
            self.assertEqual({"val": idx}, report["context"])

            res = self.post_api(f"traverse_graph/{report["id"]}")
            self.assertEqual(200, res["status"])
            self.assertEqual([None for i in range(idx, 3)], res["returns"])
            for _idx, report in enumerate(res["reports"]):
                self.assertEqual({"val": idx + _idx}, report["context"])

    def trigger_detach_node_test(self) -> None:
        """Test detach node."""
        res = self.post_api("detach_node")

        self.assertEqual(200, res["status"])
        self.assertEqual([None, None, True], res["returns"])
        self.assertTrue("reports" not in res)

        res = self.post_api("traverse_graph")

        self.assertEqual(200, res["status"])
        self.assertEqual([None, None, None], res["returns"])

        root_node = res["reports"].pop(0)
        self.assertTrue(root_node["id"].startswith("n::"))
        self.assertEqual({}, root_node["context"])

        for idx, report in enumerate(res["reports"]):
            self.assertEqual({"val": idx}, report["context"])

            res = self.post_api(f"traverse_graph/{report["id"]}")
            self.assertEqual(200, res["status"])
            self.assertEqual([None for i in range(idx, 2)], res["returns"])
            for _idx, report in enumerate(res["reports"]):
                self.assertEqual({"val": idx + _idx}, report["context"])

    def trigger_update_graph_test(self) -> None:
        """Test update graph."""
        res = self.post_api("update_graph")

        self.assertEqual(200, res["status"])
        self.assertEqual([None, None, None], res["returns"])

        root_node = res["reports"].pop(0)
        self.assertTrue(root_node["id"].startswith("n::"))
        self.assertEqual({}, root_node["context"])

        for idx, report in enumerate(res["reports"]):
            self.assertEqual({"val": idx + 1}, report["context"])

        res = self.post_api("traverse_graph")

        self.assertEqual(200, res["status"])
        self.assertEqual([None, None, None], res["returns"])

        root_node = res["reports"].pop(0)
        self.assertTrue(root_node["id"].startswith("n::"))
        self.assertEqual({}, root_node["context"])

        for idx, report in enumerate(res["reports"]):
            self.assertEqual({"val": idx + 1}, report["context"])

            res = self.post_api(f"traverse_graph/{report["id"]}")
            self.assertEqual(200, res["status"])
            self.assertEqual([None for i in range(idx, 2)], res["returns"])
            for _idx, report in enumerate(res["reports"]):
                self.assertEqual({"val": idx + _idx + 1}, report["context"])

    def trigger_create_nested_node_test(self) -> None:
        """Test create nested node."""
        res = self.post_api("create_nested_node", user=1)

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
                    "child": {"val": 2, "arr": [1, 2], "json": {"a": 1, "b": 2}},
                },
            },
            res["returns"][0]["context"],
        )

    def trigger_update_nested_node_test(self) -> None:
        """Test update nested node."""
        for walker in ["update_nested_node", "visit_nested_node"]:
            res = self.post_api(walker, user=1)
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
                        },
                    },
                },
                res["returns"][0]["context"],
            )

    def test_all_features(self) -> None:
        """Test Full Features."""
        self.trigger_openapi_specs_test()

        self.trigger_create_user_test()
        self.trigger_create_user_test("2")

        self.trigger_create_graph_test()

        self.trigger_traverse_graph_test()

        self.trigger_detach_node_test()

        self.trigger_update_graph_test()

        self.trigger_create_nested_node_test()

        self.trigger_update_nested_node_test()
