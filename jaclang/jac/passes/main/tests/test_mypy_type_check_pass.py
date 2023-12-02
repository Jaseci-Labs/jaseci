"""Test pass module."""
from typing import List

from jaclang.jac.passes.main import MyPyTypeCheckPass
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
        MyPyTypeCheckPass.mypy_message_cb = self.__message_cb

        jac_file_to_pass(
            file_path=self.fixture_abs_path("func.jac"),
            target=MyPyTypeCheckPass,
        )

        with open(self.fixture_abs_path("func.type_errors"), "r") as f:
            content = "".join(f.readlines())

        self.assertEqual(content, "\n".join(self.__messages))
