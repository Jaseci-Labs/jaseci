"""Tests for Jac Workspace."""

import os

from jaclang.compiler.workspace import Workspace
from jaclang.utils.test import TestCase


class TestWorkspace(TestCase):
    """Test Jac Workspace."""

    def test_workspace_basic(self) -> None:
        """Basic test of functionarlity."""
        ws = Workspace(path=os.path.join(os.path.dirname(__file__)))
        self.assertGreater(len(ws.modules.keys()), 4)

    def test_dependecies_basic(self) -> None:
        """Basic test of functionarlity."""
        ws = Workspace(path=os.path.join(os.path.dirname(__file__)))
        key = [i for i in ws.modules.keys() if "fam.jac" in i][0]
        self.assertGreater(len(ws.get_dependencies(key)), 0)

    def test_symbols_basic(self) -> None:
        """Basic test of functionarlity."""
        ws = Workspace(path=os.path.join(os.path.dirname(__file__)))
        key = [i for i in ws.modules.keys() if "fam.jac" in i][0]
        self.assertGreater(len(ws.get_symbols(key)), 5)

    def test_get_defs_basic(self) -> None:
        """Basic test of functionarlity."""
        ws = Workspace(path=os.path.join(os.path.dirname(__file__)))
        key = [i for i in ws.modules.keys() if "fam.jac" in i][0]
        self.assertGreater(len(ws.get_definitions(key)), 5)

    def test_get_uses_basic(self) -> None:
        """Basic test of functionarlity."""
        ws = Workspace(path=os.path.join(os.path.dirname(__file__)))
        key = [i for i in ws.modules.keys() if "fam.jac" in i][0]
        self.assertGreater(len(ws.get_uses(key)), 5)

    def test_man_code_dir(self) -> None:
        """Test of circle workspace."""
        loc = os.path.join(os.path.dirname(__file__))
        ws = Workspace(path=loc + "/../../../examples/manual_code")
        key = [i for i in ws.modules.keys() if "circle.jac" in i][0]
        # print(ws.modules[key].ir.sym_tab.pp())
        # for i in ws.get_symbols(key):
        #     print(i.decl.pp(depth=2))
        out = ""
        for i in ws.get_uses(key):
            # print(i.pp(depth=2).strip())
            out += i.pp(depth=2)
        for i in [
            "math",
            "calculate_area",
            "RAD",
            "expected_area",
            "Circle",
            "c",
            "ShapeType",
            "float",
            "radius",
            "CIRCLE",
            "Shape",
            "__init__",
            "print",
        ]:
            self.assertIn(i, out)

    # def test_decl_impl(self) -> None:
    #     """Test of circle workspace."""
    #     loc = os.path.join(os.path.dirname(__file__))
    #     ws = Workspace(path=loc + "/../../../examples/manual_code")
    #     key = [i for i in ws.modules.keys() if "circle_clean.jac" in i][0]
    #     out = ""
    #     for i in ws.get_uses(key):
    #         out += i.pp(depth=2)
    #     for i in [
    #         "math",
    #         "calculate_area",
    #         "RAD",
    #         "expected_area",
    #         "Circle",
    #         "c",
    #         "ShapeType",
    #         "float",
    #         "radius",
    #         "CIRCLE",
    #         "Shape",
    #         "__init__",
    #         "print",
    #     ]:
    #         self.assertIn(i, out)
