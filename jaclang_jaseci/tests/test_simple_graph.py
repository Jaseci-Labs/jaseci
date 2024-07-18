"""Temporary."""

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
                self.get_openapi_json(1)
                break
            else:
                with suppress(Exception):
                    self.get_openapi_json(1)
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

    def get_openapi_json(self, timeout: int = 0) -> dict:
        """Retrieve OpenAPI Specs JSON."""
        res = get(f"{self.host}/openapi.json", timeout=timeout)
        res.raise_for_status()
        return res.json()

    def trigger_openapi_specs_test(self) -> None:
        """Test OpenAPI Specs."""
        res = self.get_openapi_json()

        with open("jaclang_jaseci/tests/openai_specs.json") as file:
            self.assertEqual(load(file), res)

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
                    "child": {"val": 2, "arr": [2], "json": {"B": 2}},
                },
            },
            res["returns"][0]["context"],
        )

    def trigger_update_nested_node_test(self) -> None:
        """Test update nested node."""
        res = self.post_api("update_nested_node", user=1)

        self.assertEqual(200, res["status"])

        # self.assertEqual(
        #     {
        #         "val": 0,
        #         "arr": [],
        #         "json": {},
        #         "parent": {
        #             "val": 1,
        #             "arr": [1],
        #             "json": {"a": 1},
        #             "child": {"val": 2, "arr": [2], "json": {"B": 2}},
        #         },
        #     },
        #     res["returns"][0]["context"],
        # )

    def test_all_features(self) -> None:
        """Test Full Features."""
        # self.trigger_openapi_specs_test()

        self.trigger_create_user_test()
        self.trigger_create_user_test("2")

        self.trigger_create_graph_test()

        self.trigger_traverse_graph_test()

        self.trigger_detach_node_test()

        self.trigger_update_graph_test()

        self.trigger_create_nested_node_test()

        self.trigger_update_nested_node_test()
        # ############################################################
        # # ---------------------- TEST GRAPH ---------------------- #
        # ############################################################

        # res = self.post_api("update_sample_graph")
        # self.assertEqual(200, res["status"])
        # self.assertEqual([None, None], res["returns"])

        # reports = res["reports"]
        # report = reports[0]
        # self.assertTrue(report["id"].startswith("n:girl:"))
        # self.assertEqual({"val": "b"}, report["context"])

        # report = reports[1]
        # self.assertTrue(report["id"].startswith("n:girl:"))
        # self.assertEqual({"val": "new"}, report["context"])

        # res = self.post_api("visit_sample_graph")
        # self.assertEqual(200, res["status"])
        # self.assertEqual([1, 2, 3], res["returns"])

        # reports = res["reports"]
        # report = reports[0]
        # self.assertTrue(report["id"].startswith("n::"))

        # report = reports[1]
        # self.assertTrue(report["id"].startswith("n:boy:"))
        # self.assertEqual({"val1": "a", "val2": "b"}, report["context"])

        # report = reports[2]
        # self.assertTrue(report["id"].startswith("n:girl:"))
        # self.assertEqual({"val": "new"}, report["context"])

        # res = self.post_api("delete_sample_graph")
        # self.assertEqual(200, res["status"])
        # self.assertEqual([None, None], res["returns"])

        # reports = res["reports"]
        # report = reports[0]
        # self.assertTrue(report["id"].startswith("n:girl:"))
        # self.assertEqual({"val": "new"}, report["context"])

        # report = reports[1]
        # self.assertTrue(report["id"].startswith("n:girl:"))
        # self.assertEqual({"val": "latest"}, report["context"])

        # res = self.post_api("visit_sample_graph")
        # self.assertEqual(200, res["status"])
        # self.assertEqual([1, 2, 3], res["returns"])

        # reports = res["reports"]
        # report = reports[0]
        # self.assertTrue(report["id"].startswith("n::"))

        # report = reports[1]
        # self.assertTrue(report["id"].startswith("n:boy:"))
        # self.assertEqual({"val1": "a", "val2": "b"}, report["context"])

        # report = reports[2]
        # self.assertTrue(report["id"].startswith("n:girl:"))
        # self.assertEqual({"val": "latest"}, report["context"])

        # res = self.post_api("create_list_field")
        # self.assertEqual(200, res["status"])
        # self.assertEqual([None], res["returns"])

        # report = res["reports"][0]
        # self.assertTrue(report["id"].startswith("n:someone"))
        # self.assertEqual({"val": []}, report["context"])

        # first_user_node_id = report["id"]
        # res = self.post_api(f"update_list_field/{first_user_node_id}")
        # self.assertEqual(200, res["status"])
        # self.assertEqual([None], res["returns"])

        # report = res["reports"][0]
        # self.assertTrue(report["id"].startswith("n:someone"))
        # self.assertEqual({"val": [1]}, report["context"])

        # res = self.post_api(f"update_list_field/{first_user_node_id}")
        # self.assertEqual(200, res["status"])
        # self.assertEqual([None], res["returns"])

        # report = res["reports"][0]
        # self.assertTrue(report["id"].startswith("n:someone"))
        # self.assertEqual({"val": [1, 1]}, report["context"])

        # ############################################################
        # # ---------------------- OTHER USER ---------------------- #
        # ############################################################

        # res = self.post_api("create_list_field", user=1)
        # self.assertEqual(200, res["status"])
        # self.assertEqual([None], res["returns"])

        # report = res["reports"][0]
        # self.assertTrue(report["id"].startswith("n:someone"))
        # self.assertEqual({"val": []}, report["context"])

        # second_user_node_id = report["id"]

        # res = self.post_api(
        #     f"update_list_field/{second_user_node_id}", expect_error=True
        # )
        # self.assertEqual(403, res)  # forbidden

        # ############################################################
        # # -------------------- ALLOW ROOT READ ------------------- #
        # ############################################################

        # res = self.post_api(
        #     f"allow_other/{second_user_node_id}",
        #     json={"root_id": f'n::{self.users[0]["user"]["root_id"]}'},
        #     user=1,
        # )
        # self.assertEqual(200, res["status"])
        # self.assertEqual([None], res["returns"])

        # report = res["reports"][0]
        # self.assertTrue(report["id"].startswith("n:someone"))
        # self.assertEqual({"val": []}, report["context"])

        # res = self.post_api(f"update_list_field/{second_user_node_id}")
        # self.assertEqual(200, res["status"])
        # self.assertEqual([None], res["returns"])

        # report = res["reports"][0]
        # self.assertTrue(report["id"].startswith("n:someone"))
        # self.assertEqual({"val": [1]}, report["context"])

        # res = self.post_api(f"update_list_field/{second_user_node_id}")
        # self.assertEqual(200, res["status"])
        # self.assertEqual([None], res["returns"])

        # report = res["reports"][0]
        # self.assertTrue(report["id"].startswith("n:someone"))
        # self.assertEqual({"val": [1]}, report["context"])  # still based from [] not [1]

        # ############################################################
        # # ------------------- ALLOW ROOT WRITE ------------------- #
        # ############################################################

        # res = self.post_api(
        #     f"allow_other/{second_user_node_id}",
        #     json={"root_id": f'n::{self.users[0]["user"]["root_id"]}', "write": True},
        #     user=1,
        # )
        # self.assertEqual(200, res["status"])
        # self.assertEqual([None], res["returns"])

        # report = res["reports"][0]
        # self.assertTrue(report["id"].startswith("n:someone"))
        # self.assertEqual({"val": []}, report["context"])

        # res = self.post_api(f"update_list_field/{second_user_node_id}")
        # self.assertEqual(200, res["status"])
        # self.assertEqual([None], res["returns"])

        # report = res["reports"][0]
        # self.assertTrue(report["id"].startswith("n:someone"))
        # self.assertEqual({"val": [1]}, report["context"])

        # res = self.post_api(f"update_list_field/{second_user_node_id}")
        # self.assertEqual(200, res["status"])
        # self.assertEqual([None], res["returns"])

        # report = res["reports"][0]
        # self.assertTrue(report["id"].startswith("n:someone"))
        # self.assertEqual({"val": [1, 1]}, report["context"])

        # ############################################################
        # # --------------------- DISALLOW ROOT -------------------- #
        # ############################################################

        # res = self.post_api(
        #     f"disallow_other/{second_user_node_id}",
        #     json={"root_id": f'n::{self.users[0]["user"]["root_id"]}'},
        #     user=1,
        # )
        # self.assertEqual(200, res["status"])
        # self.assertEqual([None], res["returns"])

        # res = self.post_api(
        #     f"update_list_field/{second_user_node_id}", expect_error=True
        # )
        # self.assertEqual(403, res)  # forbidden

        # ############################################################
        # # -------------------- ALLOW NODE READ ------------------- #
        # ############################################################

        # res = self.post_api(
        #     f"allow_other/{second_user_node_id}",
        #     json={"node_id": first_user_node_id},
        #     user=1,
        # )
        # self.assertEqual(200, res["status"])
        # self.assertEqual([None], res["returns"])

        # report = res["reports"][0]
        # self.assertTrue(report["id"].startswith("n:someone"))
        # self.assertEqual({"val": [1, 1]}, report["context"])

        # res = self.post_api(
        #     f"connect_other_node/{first_user_node_id}",
        #     json={"node_id": second_user_node_id},
        # )
        # self.assertEqual(200, res["status"])
        # self.assertEqual([None], res["returns"])

        # report = res["reports"][0]
        # self.assertTrue(report["id"].startswith("n:someone"))
        # self.assertEqual({"val": [1, 1]}, report["context"])

        # res = self.post_api(f"update_list_field/{first_user_node_id}")
        # self.assertEqual(200, res["status"])
        # self.assertEqual([None, None], res["returns"])

        # for report in res["reports"]:
        #     self.assertTrue(report["id"].startswith("n:someone"))
        #     self.assertEqual(
        #         {"val": [1, 1, 1]}, report["context"]
        #     )  # other update will revert back to [1,1] since it doesn't have write access

        # res = self.post_api(f"get_list_field/{second_user_node_id}", user=1)

        # self.assertEqual(200, res["status"])
        # self.assertEqual([None], res["returns"])

        # report = res["reports"][0]
        # self.assertTrue(report["id"].startswith("n:someone"))
        # self.assertEqual(
        #     {"val": [1, 1]}, report["context"]
        # )  # proves that it's not updated
        # self.assertEqual([], res["reports"][1])

        # ############################################################
        # # ------------------- ALLOW NODE WRITE ------------------- #
        # ############################################################

        # res = self.post_api(
        #     f"allow_other/{second_user_node_id}",
        #     json={"node_id": first_user_node_id, "write": True},
        #     user=1,
        # )
        # self.assertEqual(200, res["status"])
        # self.assertEqual([None], res["returns"])

        # report = res["reports"][0]
        # self.assertTrue(report["id"].startswith("n:someone"))
        # self.assertEqual({"val": [1, 1]}, report["context"])

        # res = self.post_api(f"update_list_field/{first_user_node_id}")
        # self.assertEqual(200, res["status"])
        # self.assertEqual([None, None], res["returns"])

        # reports = res["reports"]
        # self.assertTrue(reports[0]["id"].startswith("n:someone"))
        # self.assertEqual({"val": [1, 1, 1, 1]}, reports[0]["context"])
        # self.assertTrue(reports[1]["id"].startswith("n:someone"))
        # self.assertEqual({"val": [1, 1, 1]}, reports[1]["context"])

        # res = self.post_api(f"get_list_field/{second_user_node_id}", user=1)
        # self.assertEqual(200, res["status"])
        # self.assertEqual([None], res["returns"])

        # report = res["reports"][0]
        # self.assertTrue(report["id"].startswith("n:someone"))
        # self.assertEqual(
        #     {"val": [1, 1, 1]}, report["context"]
        # )  # proves that it was able to update
        # self.assertEqual([], res["reports"][1])

        # res = self.post_api(f"get_list_field/{first_user_node_id}")
        # self.assertEqual(200, res["status"])
        # self.assertEqual([None], res["returns"])

        # report = res["reports"][0]
        # self.assertTrue(report["id"].startswith("n:someone"))
        # self.assertEqual(
        #     {"val": [1, 1, 1, 1]}, report["context"]
        # )  # proves that it was able to update

        # report = res["reports"][1][0]
        # self.assertTrue(report["id"].startswith("n:someone"))
        # self.assertEqual(
        #     {"val": [1, 1, 1]}, report["context"]
        # )  # proves that it was able to access by first user

        # ############################################################
        # # --------------------- DISALLOW ROOT -------------------- #
        # ############################################################

        # res = self.post_api(
        #     f"disallow_other/{second_user_node_id}",
        #     json={"node_id": first_user_node_id},
        #     user=1,
        # )
        # self.assertEqual(200, res["status"])
        # self.assertEqual([None], res["returns"])

        # res = self.post_api(f"get_list_field/{first_user_node_id}")
        # self.assertEqual(200, res["status"])
        # self.assertEqual([None], res["returns"])

        # report = res["reports"][0]
        # self.assertTrue(report["id"].startswith("n:someone"))
        # self.assertEqual({"val": [1, 1, 1, 1]}, report["context"])
        # self.assertEqual(
        #     [], res["reports"][1]
        # )  # proves that it wasn't able to access the node even it's connected

        # ############################################################
        # # ------------------ TEST NESTED WALKER ------------------ #
        # ############################################################

        # res = self.post_api("nested2")
        # self.assertEqual(
        #     {"status": 200, "returns": [None], "reports": ["nested1", "nested2"]}, res
        # )
