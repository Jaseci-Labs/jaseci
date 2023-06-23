# """Test ast build pass module."""
# import inspect
# from copy import copy

# from jaclang.jac.absyntree import AstNode
# from jaclang.jac.lexer import JacLexer
# from jaclang.jac.parser import JacParser
# from jaclang.jac.passes.ast_build_pass import AstBuildPass
# from jaclang.jac.passes.blue_pygen_pass import BluePygenPass
# from jaclang.jac.utils import get_ast_nodes_as_snake_case as ast_snakes
# from jaclang.utils.test import TestCase


# class BluePygenPassTests(TestCase):
#     """Test pass module."""

#     lex = JacLexer()
#     prse = JacParser()
#     builder = AstBuildPass()
#     codegen = BluePygenPass()

#     def setUp(self) -> None:
#         """Set up test."""
#         return super().setUp()

#     def build_micro(self, filename: str) -> AstNode:
#         """Parse micro jac file."""
#         self.prse.cur_file = filename
#         tokens = self.lex.tokenize(
#             self.load_fixture(f"../../../tests/fixtures/micro/{filename}")
#         )
#         ptree = self.prse.parse(tokens=tokens)
#         build_pass = self.builder.run(node=ptoa(ptree))
#         return build_pass

#     def test_pygen_basic(self) -> None:
#         """Basic test for pass."""
#         ptree = self.prse.parse(self.lex.tokenize(self.load_fixture("fam.jac")))
#         build_pass = self.builder.run(node=ptoa(ptree))
#         code_gen = self.codegen.run(node=build_pass)
#         self.assertGreater(len(str(code_gen.to_dict())), 200)

#     def test_pygen_module_structure(self) -> None:
#         """Basic test for pass."""
#         build_pass = self.build_micro("module_structure.jac")
#         code_gen = self.codegen.run(node=build_pass)
#         self.assertGreater(len(str(code_gen.meta["py_code"])), 200)

#     def test_pygen_import_pass(self) -> None:
#         """Basic test for pass."""
#         build_pass = self.build_micro("../../../passes/import_pass.jac")
#         code_gen = self.codegen.run(node=build_pass)
#         self.assertGreater(len(str(code_gen.to_dict())), 200)

#     def test_pygen_jac_cli(self) -> None:
#         """Basic test for pass."""
#         build_pass = self.build_micro("../../../../cli/jac_cli.jac")
#         code_gen = self.codegen.run(node=build_pass)
#         print(code_gen.meta["py_code"])
#         self.assertGreater(len(str(build_pass.to_dict())), 200)

#     def test_no_typo_in_pass(self) -> None:
#         """Test for enter/exit name diffs with parser."""
#         ast_func_names = [
#             x for x in ast_snakes() if x not in ["ast_node", "o_o_p_access_node"]
#         ]
#         pygen_func_names = copy(BluePygenPass.marked_incomplete)
#         for name, value in inspect.getmembers(BluePygenPass):
#             if (
#                 (name.startswith("enter_") or name.startswith("exit_"))
#                 and inspect.isfunction(value)
#                 and not getattr(BluePygenPass.__base__, value.__name__, False)
#                 and value.__qualname__.split(".")[0]
#                 == BluePygenPass.__name__.replace("enter_", "").replace("exit_", "")
#             ):
#                 pygen_func_names.append(name.replace("enter_", "").replace("exit_", ""))
#         for name in pygen_func_names:
#             self.assertIn(name, ast_func_names)

#     def test_pass_ast_complete(self) -> None:
#         """Test for enter/exit name diffs with parser."""
#         ast_func_names = [
#             x for x in ast_snakes() if x not in ["ast_node", "o_o_p_access_node"]
#         ]
#         pygen_func_names = copy(BluePygenPass.marked_incomplete)
#         for name, value in inspect.getmembers(BluePygenPass):
#             if (
#                 (name.startswith("enter_") or name.startswith("exit_"))
#                 and inspect.isfunction(value)
#                 and not getattr(BluePygenPass.__base__, value.__name__, False)
#                 and value.__qualname__.split(".")[0]
#                 == BluePygenPass.__name__.replace("enter_", "").replace("exit_", "")
#             ):
#                 pygen_func_names.append(name.replace("enter_", "").replace("exit_", ""))
#         for name in ast_func_names:
#             self.assertIn(name, pygen_func_names)
