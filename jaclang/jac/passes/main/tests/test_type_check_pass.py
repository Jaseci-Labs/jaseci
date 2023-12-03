"""Test pass module."""
from typing import List

from jaclang.jac.passes.main import JacTypeCheckPass
from jaclang.jac.passes.main.schedules import py_code_gen_typed
from jaclang.jac.transpiler import jac_file_to_pass
from jaclang.utils.test import TestCase


class MypyTypeCheckPassTests(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        self.__messages: List[str] = []
        return super().setUp()

    def __message_cb(
        self, filename: str | None, new_messages: list[str], is_serious: bool
    ) -> None:
        for message in new_messages:
            self.__messages.append(
                message.replace(self.fixture_abs_path("func.jac"), "")
            )

    def test_type_errors(self) -> None:
        """Basic test for pass."""
        JacTypeCheckPass.message_cb = self.__message_cb

        jac_file_to_pass(
            file_path=self.fixture_abs_path("func.jac"),
            schedule=py_code_gen_typed,
        )

        errs = "\n".join(self.__messages)
        for i in [
            "File::4",
            "File::12",
            '(got "int", expected "str")',
            '(got "str", expected "int")',
        ]:
            self.assertIn(i, errs)
