"""Test pass module."""

from typing import List

from jaclang.compiler.passes.main.schedules import py_code_gen_typed
from jaclang.compiler.program import JacProgram
from jaclang.utils.lang_tools import AstTool
from jaclang.utils.test import TestCase


class MypyTypeCheckPassTests(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        self.__messages: List[str] = []
        return super().setUp()

    def test_type_errors(self) -> None:
        """Basic test for pass."""
        type_checked = JacProgram().jac_file_to_pass(
            file_path=self.fixture_abs_path("func.jac"),
            schedule=py_code_gen_typed,
        )

        errs = "\n".join([i.msg for i in type_checked.warnings_had])
        files = "\n".join([i.loc.mod_path for i in type_checked.warnings_had])

        for i in [
            "func2.jac",
            "func.jac",
            '(got "int", expected "str")',
            '(got "str", expected "int")',
        ]:
            self.assertIn(i, errs + files)

    def test_imported_module_typecheck(self) -> None:
        """Basic test for pass."""
        type_checked = JacProgram().jac_file_to_pass(
            file_path=self.fixture_abs_path("game1.jac"),
            schedule=py_code_gen_typed,
        )

        errs = "\n".join([i.msg for i in type_checked.warnings_had])
        files = "\n".join([i.loc.mod_path for i in type_checked.warnings_had])

        for i in [
            'Argument 2 to "is_pressed" of "Button" has incompatible type "int"; expected "str"',
        ]:
            self.assertIn(i, errs + files)

    def test_type_coverage(self) -> None:
        """Testing for type info coverage in sym_tab via ast."""
        out = AstTool().ir(["ast", f"{self.fixture_abs_path('type_info.jac')}"])
        lis = [
            "introduce - Type: None",
            "25:30 - 25:37\t        |   |   |           +-- Name - species - Type: None",  # AtomTrailer
        ]
        self.assertIn("HasVar - species - Type: builtins.str", out)
        self.assertIn("myDog - Type: type_info.Dog", out)
        self.assertIn("Body - Type: type_info.Dog.Body", out)
        self.assertEqual(out.count("Type: builtins.str"), 35)
        for i in lis:
            self.assertNotIn(i, out)

    def test_data_spatial_type_info(self) -> None:
        """Testing for type info for dataspatial constructs."""
        out = AstTool().ir(
            ["ast", f"{self.fixture_abs_path('data_spatial_types.jac')}"]
        )
        self.assertRegex(
            out,
            r"129:22 - 129:26.*SpecialVarRef - root \- Type\: jaclang.runtimelib.architype.Root",
        )
        self.assertRegex(out, r"129:11 - 129:27.*FuncCall \- Type\: builtins\.str")
        self.assertRegex(
            out,
            r"129:13 - 129:21.*Name \- node_dot \- Type\: builtins.str",
        )

        self.assertRegex(
            out,
            r"128:5 - 128:25.*SpawnExpr \- Type\: jaclang.runtimelib.architype.WalkerArchitype",
        )

        self.assertRegex(
            out,
            r"48:11 - 48:28.*EdgeRefTrailer \- Type\: builtins.list\[jaclang.runtimelib.architype.Architype\]",
        )

        self.assertRegex(out, r"24:5 - 24:25.*BinaryExpr \- Type\: builtins.bool", out)
