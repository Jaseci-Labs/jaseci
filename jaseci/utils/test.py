"""Test case utils for Jaseci."""

import inspect
import os
from unittest import TestCase as _TestCase


class TestCase(_TestCase):
    """Base test case for Jaseci."""

    def setUp(self: "TestCase") -> None:
        """Set up test case."""
        return super().setUp()

    def tearDown(self: "TestCase") -> None:
        """Tear down test case."""
        return super().tearDown()

    def load_fixture(self: "TestCase", fixture: str) -> str:
        """Load fixture from fixtures directory."""
        fixture_src = inspect.getmodule(inspect.currentframe().f_back).__file__
        with open(f"{os.path.dirname(fixture_src)}/fixtures/{fixture}", "r") as f:
            return f.read()
