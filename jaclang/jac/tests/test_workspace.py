"""Tests for Jac Workspace."""
import os

from jaclang.jac.workspace import Workspace
from jaclang.utils.test import TestCase


class TestWrokspace(TestCase):
    """Test Jac Workspace."""

    def test_workspace_basic(self) -> None:
        """Basic test of functionarlity."""
        ws = Workspace(path=os.path.join(os.path.dirname(__file__)))
        self.assertGreater(len(ws.modules.keys()), 4)
