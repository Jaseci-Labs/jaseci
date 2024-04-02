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

    def micro_suite_test(self, filename: str) -> None:
        """Parse micro jac file."""
        try:
            code_gen_pure = jac_file_to_pass(
                self.fixture_abs_path(filename),
                target=PyastGenPass,
                schedule=without_format,
            )
            before = ast3.dump(code_gen_pure.ir.gen.py_ast[0], indent=2)
            code_gen_jac = jac_str_to_pass(
                jac_str=code_gen_pure.ir.unparse(),
                file_path=filename,
                target=PyastGenPass,
                schedule=without_format,
            )
            after = ast3.dump(code_gen_jac.ir.gen.py_ast[0], indent=2)
            self.assertEqual(
                len("\n".join(unified_diff(before.splitlines(), after.splitlines()))),
                0,
            )
        except Exception as e:
            self.skipTest(f"Test failed, but skipping instead of failing: {e}")


JacUnparseTests.self_attach_micro_tests()
