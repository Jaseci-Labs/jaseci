"""Test ast build pass module."""

import ast as ast3
from difflib import unified_diff


from jaclang.compiler.passes.main import PyastGenPass
from jaclang.compiler.passes.main.schedules import py_code_gen as without_format
from jaclang.compiler.passes.tool import JacFormatPass
from jaclang.compiler.program import JacProgram
from jaclang.utils.test import AstSyncTestMixin, TestCaseMicroSuite


class JacUnparseTests(TestCaseMicroSuite, AstSyncTestMixin):
    """Test pass module."""

    TargetPass = JacFormatPass

    def test_double_unparse(self) -> None:
        """Parse micro jac file."""
        try:
            prog = JacProgram(
                main_file=self.examples_abs_path("manual_code/circle.jac")
            )
            code_gen_pure = prog.jac_file_to_pass(
                target=PyastGenPass, schedule=without_format
            )
            x = code_gen_pure.ir.unparse()
            y = code_gen_pure.ir.unparse()
            self.assertEqual(x, y)
        except Exception as e:
            print("\n".join(unified_diff(x.splitlines(), y.splitlines())))
            raise e

    def micro_suite_test(self, filename: str) -> None:
        """Parse micro jac file."""
        prog = JacProgram(main_file=self.fixture_abs_path(filename))
        prog.jac_file_to_pass(
            target=PyastGenPass,
            schedule=without_format,
        )
        before = ast3.dump(
            prog.modules[self.fixture_abs_path(filename)].gen.py_ast[0], indent=2
        )
        x = prog.modules[self.fixture_abs_path(filename)].unparse()
        prog2 = JacProgram(main_file=filename)
        prog2.jac_str_to_pass(jac_str=x, target=PyastGenPass, schedule=without_format)
        after = ast3.dump(prog2.modules[filename].gen.py_ast[0], indent=2)
        if "circle_clean_tests.jac" in filename:
            self.assertEqual(
                len(
                    [
                        i
                        for i in unified_diff(
                            before.splitlines(), after.splitlines(), n=0
                        )
                        if "test" not in i
                    ]
                ),
                5,
            )
        else:
            self.assertEqual(
                len("\n".join(unified_diff(before.splitlines(), after.splitlines()))),
                0,
            )


JacUnparseTests.self_attach_micro_tests()
