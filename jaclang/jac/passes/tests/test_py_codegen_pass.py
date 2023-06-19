"""Test ast build pass module."""
from jaclang.jac.lexer import JacLexer
from jaclang.jac.parser import JacParser
from jaclang.jac.passes.ast_build_pass import AstBuildPass
from jaclang.jac.passes.ir_pass import parse_tree_to_ast as ptoa
from jaclang.jac.passes.py_codegen_pass import PyCodeGenPass
from jaclang.utils.test import TestCase


class PyCodeGenPassTests(TestCase):
    """Test pass module."""

    lex = JacLexer()
    prse = JacParser()
    builder = AstBuildPass()
    codegen = PyCodeGenPass()

    def setUp(self: TestCase) -> None:
        """Set up test."""
        return super().setUp()

    def build_micro(self: "PyCodeGenPassTests", filename: str) -> None:
        """Parse micro jac file."""
        self.prse.cur_file = filename
        ptree = self.prse.parse(
            self.lex.tokenize(
                self.load_fixture(f"../../../tests/fixtures/micro/{filename}")
            )
        )
        build_pass = self.builder.run(node=ptoa(ptree))
        return build_pass

    def test_pygen_basic(self: "PyCodeGenPassTests") -> None:
        """Basic test for pass."""
        ptree = self.prse.parse(self.lex.tokenize(self.load_fixture("fam.jac")))
        build_pass = self.builder.run(node=ptoa(ptree))
        code_gen = self.codegen.run(node=build_pass)
        code_gen = code_gen
        # print(code_gen.meta['py_code'])

    def test_pygen_module_structure(self: "PyCodeGenPassTests") -> None:
        """Basic test for pass."""
        build_pass = self.build_micro("module_structure.jac")
        # build_pass.print()
        self.codegen.run(node=build_pass)
        # print(code_gen.meta['py_code'])
        self.assertGreater(len(str(build_pass.to_dict())), 200)

    def test_pygen_import_pass(self: "PyCodeGenPassTests") -> None:
        """Basic test for pass."""
        build_pass = self.build_micro("../../../passes/import_pass.jac")
        # build_pass.print()
        code_gen = self.codegen.run(node=build_pass)
        print(code_gen.meta["py_code"])
        self.assertGreater(len(str(build_pass.to_dict())), 200)

    # def test_no_typo_in_pass(self: "PyCodeGenPassTests") -> None:
    #     """Test for enter/exit name diffs with parser."""
    #     from jaclang.jac.parser import JacParser

    #     parser_func_names = []
    #     for name, value in inspect.getmembers(JacParser):
    #         if (
    #             inspect.isfunction(value)
    #             and value.__qualname__.split(".")[0] == JacParser.__name__
    #         ):
    #             parser_func_names.append(name)
    #     pygen_func_names = []
    #     for name, value in inspect.getmembers(AstBuildPass):
    #         if (
    #             (name.startswith("enter_") or name.startswith("exit_"))
    #             and inspect.isfunction(value)
    #             and not getattr(AstBuildPass.__base__, value.__name__, False)
    #             and value.__qualname__.split(".")[0]
    #             == AstBuildPass.__name__.replace("enter_", "").replace("exit_", "")
    #         ):
    #             pygen_func_names.append(
    #                 name.replace("enter_", "").replace("exit_", "")
    #             )
    #     for name in pygen_func_names:
    #         self.assertIn(name, parser_func_names)

    # def test_pass_grammar_complete(self: "PyCodeGenPassTests") -> None:
    #     """Test for enter/exit name diffs with parser."""
    #     from jaclang.jac.parser import JacParser

    #     parser_func_names = []
    #     for name, value in inspect.getmembers(JacParser):
    #         if (
    #             inspect.isfunction(value)
    #             and value.__qualname__.split(".")[0] == JacParser.__name__
    #         ):
    #             parser_func_names.append(name)
    #     pygen_func_names = []
    #     for name, value in inspect.getmembers(AstBuildPass):
    #         if (
    #             (name.startswith("enter_") or name.startswith("exit_"))
    #             and inspect.isfunction(value)
    #             and not getattr(AstBuildPass.__base__, value.__name__, False)
    #             and value.__qualname__.split(".")[0]
    #             == AstBuildPass.__name__.replace("enter_", "").replace("exit_", "")
    #         ):
    #             pygen_func_names.append(
    #                 name.replace("enter_", "").replace("exit_", "")
    #             )
    #     for name in parser_func_names:
    #         self.assertIn(name, pygen_func_names)
