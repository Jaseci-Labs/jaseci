"""Test ast build pass module."""
import ast as ast3
import io
import sys
import types

import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes.main import PyastGenPass, SubNodeTabPass
from jaclang.compiler.transpiler import jac_file_to_pass
from jaclang.utils.test import AstSyncTestMixin, TestCaseMicroSuite


def ast_to_list(node: ast3.AST) -> list[ast3.AST]:
    """Convert ast to list."""
    nodes = [node]
    for _, value in ast3.iter_fields(node):
        if isinstance(value, list):
            for item in value:
                if isinstance(item, ast3.AST):
                    nodes.extend(ast_to_list(item))
        elif isinstance(value, ast3.AST):
            nodes.extend(ast_to_list(value))
    return nodes


class PyastGenPassTests(TestCaseMicroSuite, AstSyncTestMixin):
    """Test pass module."""

    TargetPass = PyastGenPass

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_hodge_podge(self) -> None:
        """Basic test for pass."""
        code_gen = jac_file_to_pass(
            self.fixture_abs_path("../../../../../../examples/micro/hodge_podge.jac"),
            target=PyastGenPass,
        )

        # if isinstance(code_gen.ir.gen.py_ast, ast3.AST):
        #     print(ast3.dump(code_gen.ir.gen.py_ast, indent=2))
        #     print(ast3.unparse(code_gen.ir.gen.py_ast))
        #     exec(compile(code_gen.ir.gen.py_ast, "<string>", "exec"))
        self.assertFalse(code_gen.errors_had)

    def test_circle_py_ast(self) -> None:
        """Basic test for pass."""
        code_gen = jac_file_to_pass(
            self.fixture_abs_path("../../../../../../examples/manual_code/circle.jac"),
            target=PyastGenPass,
        )
        import ast as ast3

        if isinstance(code_gen.ir.gen.py_ast, ast3.AST):
            # from_jac_str = ast3.dump(code_gen.ir.gen.py_ast, indent=2)
            # back_to_py = ast3.unparse(code_gen.ir.gen.py_ast)
            # from_py = ast3.parse(back_to_py)
            # from_py_str = ast3.dump(from_py, indent=2)
            # import difflib

            # print(
            #     "\n".join(
            #         difflib.unified_diff(
            #             from_jac_str.splitlines(), from_py_str.splitlines(), n=0
            #         )
            #     )
            # )
            prog = compile(code_gen.ir.gen.py_ast, filename="<ast>", mode="exec")
            captured_output = io.StringIO()
            sys.stdout = captured_output
            module = types.ModuleType("__main__")
            exec(prog, module.__dict__)
            sys.stdout = sys.__stdout__
            stdout_value = captured_output.getvalue()
            self.assertIn(
                "Area of a circle with radius 5 using function: 78",
                stdout_value,
            )
            self.assertIn(
                "Area of a Circle with radius 5 using class: 78",
                stdout_value,
            )

        self.assertFalse(code_gen.errors_had)

    def parent_scrub(self, node: ast.AstNode) -> bool:
        """Validate every node has parent."""
        success = True
        for i in node.kid:
            if not isinstance(i, ast.Module) and i.parent is None:
                success = False
                break
            else:
                success = self.parent_scrub(i)
        return success

    def micro_suite_test(self, filename: str) -> None:
        """Parse micro jac file."""
        code_gen = jac_file_to_pass(
            self.fixture_abs_path(filename), target=PyastGenPass
        )
        from_jac_str = ast3.dump(code_gen.ir.gen.py_ast, indent=2)
        from_jac = code_gen.ir.gen.py_ast
        try:
            # back_to_py = ast3.unparse(from_jac)
            compile(from_jac, filename="<ast>", mode="exec")
        except Exception as e:
            print(from_jac_str)
            raise e
        # from_py = ast3.parse(back_to_py)
        # from_py_str = ast3.dump(from_py, indent=2)
        # import difflib
        # print(from_jac_str)
        # print(
        #     "\n".join(
        #         difflib.unified_diff(
        #             from_jac_str.splitlines(), from_py_str.splitlines(), n=6
        #         )
        #     )
        # )
        # if len(ast_to_list(from_jac)) != len(ast_to_list(from_py)):
        #     print(
        #         f"\n{filename} - AST node length diff: {len(ast_to_list(from_jac))} vs {len(ast_to_list(from_py))}"
        #     )
        self.assertTrue(self.parent_scrub(code_gen.ir))
        self.assertGreater(len(from_jac_str), 10)


PyastGenPassTests.self_attach_micro_tests()


class ValidateTreeParentTest(TestCaseMicroSuite):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def parent_scrub(self, node: ast.AstNode) -> bool:
        """Validate every node has parent."""
        success = True
        for i in node.kid:
            if not isinstance(i, ast.Module) and i.parent is None:
                success = False
                break
            else:
                success = self.parent_scrub(i)
        return success

    def micro_suite_test(self, filename: str) -> None:
        """Parse micro jac file."""
        code_gen = jac_file_to_pass(
            self.fixture_abs_path(filename), target=SubNodeTabPass
        )
        self.assertTrue(self.parent_scrub(code_gen.ir))
        code_gen = jac_file_to_pass(
            self.fixture_abs_path(filename), target=PyastGenPass
        )
        self.assertTrue(self.parent_scrub(code_gen.ir))


ValidateTreeParentTest.self_attach_micro_tests()
