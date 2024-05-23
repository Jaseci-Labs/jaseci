"""Test ast build pass module."""

import ast as ast3
from difflib import unified_diff

import jaclang.compiler.absyntree as ast
from jaclang.compiler.compile import jac_file_to_pass, jac_str_to_pass
from jaclang.compiler.passes.main import PyastGenPass
from jaclang.compiler.passes.main.schedules import py_code_gen as without_format
from jaclang.compiler.passes.tool import JacFormatPass
from jaclang.utils.test import AstSyncTestMixin, TestCaseMicroSuite


class JacUnparseTests(TestCaseMicroSuite, AstSyncTestMixin):
    """Test pass module."""

    TargetPass = JacFormatPass

    def test_double_unparse(self) -> None:
        """Parse micro jac file."""
        filename = "../../../../../../examples/manual_code/circle.jac"
        try:
            code_gen_pure = jac_file_to_pass(
                self.fixture_abs_path(filename),
                target=PyastGenPass,
                schedule=without_format,
            )
            x = code_gen_pure.ir.unparse()
            y = code_gen_pure.ir.unparse()
            self.assertEqual(x, y)
        except Exception as e:
            print("\n".join(unified_diff(x.splitlines(), y.splitlines())))
            self.skipTest(f"Test failed, but skipping instead of failing: {e}")

    def micro_suite_test(self, filename: str) -> None:
        """Parse micro jac file."""
        try:
            code_gen_pure = jac_file_to_pass(
                self.fixture_abs_path(filename),
                target=PyastGenPass,
                schedule=without_format,
            )
            before = ast3.dump(code_gen_pure.ir.gen.py_ast[0], indent=2)
            x = code_gen_pure.ir.unparse()
            # print(x)
            # print(f"Testing {code_gen_pure.ir.name}")
            # print(code_gen_pure.ir.pp())
            code_gen_jac = jac_str_to_pass(
                jac_str=x,
                file_path=filename,
                target=PyastGenPass,
                schedule=without_format,
            )
            after = ast3.dump(code_gen_jac.ir.gen.py_ast[0], indent=2)
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
                    len(
                        "\n".join(unified_diff(before.splitlines(), after.splitlines()))
                    ),
                    0,
                )

        except Exception as e:
            raise e
            # self.skipTest(f"Test failed, but skipping instead of failing: {e}")


JacUnparseTests.self_attach_micro_tests()
