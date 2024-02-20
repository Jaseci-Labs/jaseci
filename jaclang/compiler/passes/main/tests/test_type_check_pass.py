"""Test pass module."""

from typing import List

from jaclang.compiler.compile import jac_file_to_pass
from jaclang.compiler.passes.main.schedules import py_code_gen_typed
from jaclang.utils.test import TestCase


class MypyTypeCheckPassTests(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        self.__messages: List[str] = []
        return super().setUp()

    def test_type_errors(self) -> None:
        """Basic test for pass."""
        type_checked = jac_file_to_pass(
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
        type_checked = jac_file_to_pass(
            file_path=self.fixture_abs_path("game1.jac"),
            schedule=py_code_gen_typed,
        )

        errs = "\n".join([i.msg for i in type_checked.warnings_had])
        files = "\n".join([i.loc.mod_path for i in type_checked.warnings_had])

        for i in [
            'Argument 2 to "is_pressed" of "Button" has incompatible type "int"; expected "str"',
        ]:
            self.assertIn(i, errs + files)
