"""Test utils."""

from contextlib import suppress
from os import environ, getenv
from subprocess import Popen, run
from typing import Literal, overload
from unittest import TestCase

from fakeredis import FakeRedis

from httpx import get, post

from pymongo import MongoClient

from redis import Redis as RedisClient

from ..jaseci.datasources import Collection, MontyClient, Redis


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

        if getenv("DATABASE_HOST"):
            self.assertIsInstance(Collection.get_client(), MongoClient)
        else:
            self.assertIsInstance(Collection.get_client(), MontyClient)

        if getenv("REDIS_HOST"):
            self.assertIsInstance(Redis.get_rd(), RedisClient)
        else:
            self.assertIsInstance(Redis.get_rd(), FakeRedis)

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
