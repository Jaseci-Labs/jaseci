"""JacLang Jaseci Unit Test."""

from contextlib import suppress
from os import environ, getenv
from subprocess import Popen, run
from typing import Literal, overload
from unittest.async_case import IsolatedAsyncioTestCase

from httpx import get, post

from ..jaseci.datasources import Collection


class SimpleGraphTest(IsolatedAsyncioTestCase):
    """JacLang Jaseci Feature Tests."""

    async def asyncSetUp(self) -> None:
        """Reset DB and wait for server."""
        run(["fuser", "-k", "8002/tcp"])
        run(["jac", "clean"])
        run(["jac", "tool", "gen_parser"])
        envs = environ.copy()
        envs["DATABASE_HOST"] = "mongodb://localhost/?retryWrites=true&w=majority"
        self.server = Popen(
            [
                "jac",
                "serve",
                "jac_cloud/tests/situational_flows.jac",
                "--port",
                "8002",
            ],
            env=envs,
        )
        run(["sleep", "5"])

        self.host = "http://0.0.0.0:8002"
        Collection.__client__ = None
        Collection.__database__ = None
        self.client = Collection.get_client()
        self.q_node = Collection.get_collection("node")
        self.q_edge = Collection.get_collection("edge")
        self.users: list[dict] = []
        self.database = getenv("DATABASE_NAME", "jaseci")
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
        self.client.drop_database(self.database)
        self.server.kill()

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
            f"{self.host}/walker/{api}", json=json, headers=self.users[user]["headers"]
        )

        if not expect_error:
            res.raise_for_status()
            return res.json()
        else:
            return res.status_code

    def check_server(self) -> None:
        """Retrieve OpenAPI Specs JSON."""
        res = get(f"{self.host}/healthz", timeout=5)
        res.raise_for_status()
        self.assertEqual(200, res.status_code)

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

        self.users.append(
            {"user": user, "headers": {"Authorization": f"Bearer {token}"}}
        )

    def trigger_spawn_test(self) -> None:
        """Test spawn call behavior of walker."""
        res = self.post_api("WalkerTestSpawn", json={})
        self.assertEqual(200, res["status"])

        reports = res["reports"]
        self.assertEqual("Walker entry: Root()", reports[0])
        self.assertEqual("Node entry: Root()", reports[1])
        for i in range(5):
            self.assertEqual(f"Node exit: NodeTest(value={i})", reports[i + 2])
        self.assertEqual("Walker exit: NodeTest(value=4)", reports[7])
        visitor_report = res["reports"][-1]

        visited_nodes = visitor_report["context"]["visited_nodes"]
        entry_count = visitor_report["context"]["entry_count"]
        exit_count = visitor_report["context"]["exit_count"]

        self.assertEqual(visited_nodes, [{"value": i} for i in range(5)])
        self.assertEqual(entry_count, 1)
        self.assertEqual(exit_count, 1)

    async def test_situational_features(self) -> None:
        """Test Full Features."""
        self.trigger_create_user_test()
        self.trigger_create_user_test(suffix="2")

        self.trigger_spawn_test()
