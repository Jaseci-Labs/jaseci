"""Tests for Jac Loader."""
import sys

from jaclang import jac_import
from jaclang.utils.test import TestCase


class TestLoader(TestCase):
    """Test Jac self.prse."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_import_basic_python(self) -> None:
        """Test basic self loading."""
        h = jac_import("fixtures.hello_world")
        self.assertEqual(h.hello(), "Hello World!")  # type: ignore

    def test_modules_correct(self) -> None:
        """Test basic self loading."""
        jac_import("fixtures.hello_world")
        self.assertIn("module 'hello_world'", str(sys.modules))
        self.assertIn("/tests/fixtures/hello_world.jac", str(sys.modules))
