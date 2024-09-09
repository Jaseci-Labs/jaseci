"""Test registry pass."""

import os

from jaclang.compiler.compile import jac_file_to_pass
from jaclang.compiler.passes.main import RegistryPass
from jaclang.utils.test import TestCase


class RegistryPassTests(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_registry_pass(self) -> None:
        """Basic test for pass."""
        state = jac_file_to_pass(self.fixture_abs_path("registry.jac"), RegistryPass)
        self.assertFalse(state.errors_had)
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    os.path.dirname(self.fixture_abs_path("registry.jac")),
                    "__jac_gen__",
                    "registry.registry.pkl",
                )
            )
        )
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    os.path.dirname(self.fixture_abs_path("registry.jac")),
                    "__jac_gen__",
                    "fstrings.registry.pkl",
                )
            )
        )
        self.assertIn("109", str(state.ir.to_dict()))
