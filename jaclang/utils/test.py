"""Test case utils for Jaseci."""

import inspect
import os
from unittest import TestCase as _TestCase


class TestCase(_TestCase):
    """Base test case for Jaseci."""

    def setUp(self) -> None:
        """Set up test case."""
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down test case."""
        return super().tearDown()

    def load_fixture(self, fixture: str) -> str:
        """Load fixture from fixtures directory."""
        fixture_src = inspect.getmodule(inspect.currentframe().f_back).__file__
        fixture_path = os.path.join(os.path.dirname(fixture_src), "fixtures", fixture)
        with open(fixture_path, "r") as f:
            return f.read()

    def fixture_abs_path(self, fixture: str) -> str:
        """Load fixture from fixtures directory."""
        fixture_src = inspect.getmodule(inspect.currentframe().f_back).__file__
        file_path = os.path.join(os.path.dirname(fixture_src), "fixtures", fixture)
        return os.path.abspath(file_path)
