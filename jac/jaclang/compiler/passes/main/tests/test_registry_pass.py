"""Test registry pass."""

import os

from jaclang.compiler.passes.main import RegistryPass
from jaclang.compiler.program import JacProgram
from jaclang.utils.test import TestCase


class RegistryPassTests(TestCase):
    """Test pass module."""

    # Need change
    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_registry_pass(self) -> None:
        """Basic test for pass."""
        state = (out := JacProgram()).compile(
            self.fixture_abs_path("registry.jac"), RegistryPass
        )
        self.assertFalse(out.errors_had)
        self.assertFalse(
            os.path.exists(
                os.path.join(
                    os.path.dirname(self.fixture_abs_path("registry.jac")),
                    "__jac_gen__",
                    "registry.registry.pkl",
                )
            )
        )
        self.assertIn("109", str(state.ir_out.to_dict()))
