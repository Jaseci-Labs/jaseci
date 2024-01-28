"""Test pass module."""
from typing import List

from jaclang.compiler.passes.main.schedules import py_code_gen_typed
from jaclang.compiler.transpiler import jac_file_to_pass
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
