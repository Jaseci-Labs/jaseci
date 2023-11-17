"""Test ast build pass module."""
import ast as ast3


from jaclang.jac.passes.main import PyastGenPass
from jaclang.jac.passes.main.schedules import py_code_gen as without_format
from jaclang.jac.passes.tool import JacFormatPass
from jaclang.jac.passes.tool.schedules import format_pass
from jaclang.jac.transpiler import jac_file_to_pass, jac_str_to_pass
from jaclang.utils.test import AstSyncTestMixin, TestCaseMicroSuite


class JacFormatPassTests(TestCaseMicroSuite, AstSyncTestMixin):
    """Test pass module."""

    TargetPass = JacFormatPass

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_jac_cli(self) -> None:
        """Basic test for pass."""
        code_gen = jac_file_to_pass(
            self.fixture_abs_path("base.jac"), target=JacFormatPass
        )
        self.assertFalse(code_gen.errors_had)

    def test_empty_codeblock(self) -> None:
        """Basic test for pass."""
        code_gen = jac_file_to_pass(
            self.fixture_abs_path("base.jac"), target=JacFormatPass
        )
        self.assertFalse(code_gen.errors_had)

    def micro_suite_test(self, filename: str) -> None:
        """Parse micro jac file."""
        code_gen_pure = jac_file_to_pass(
            self.fixture_abs_path(filename),
            target=PyastGenPass,
            schedule=without_format,
        )
        with_format = format_pass
        code_gen_format = jac_file_to_pass(
            self.fixture_abs_path(filename), schedule=with_format
        )
        code_gen_jac = jac_str_to_pass(
            jac_str=code_gen_format.ir.gen.jac,
            file_path=filename,
            target=PyastGenPass,
            schedule=without_format,
        )

        for i in range(len(code_gen_pure.ir.gen.py.split("\n"))):
            if "test_" in code_gen_pure.ir.gen.py.split("\n")[i]:
                continue
            try:
                self.assertEqual(
                    ast3.dump(code_gen_pure.ir.gen.py_ast, indent=2),
                    ast3.dump(code_gen_jac.ir.gen.py_ast, indent=2),
                )
            except Exception as e:
                from jaclang.utils.helpers import add_line_numbers

                print(add_line_numbers(code_gen_pure.ir.source.code))
                print(add_line_numbers(code_gen_format.ir.gen.jac))
                raise e


JacFormatPassTests.self_attach_micro_tests()
