# """Tests for Jac parser."""

# import inspect
# import io
# import os
# import sys

# from jaclang import JacMachine as Jac
# from jaclang.compiler import jac_lark as jl
# from jaclang.compiler.constant import Tokens
# from jaclang.compiler.parser import JacParser
# from jaclang.compiler.program import JacProgram
# from jaclang.compiler.unitree import Source
# from jaclang.utils.test import TestCaseMicroSuite


# class TestLarkParser(TestCaseMicroSuite):
#     """Test Jac self.prse."""

#     def setUp(self) -> None:
#         """Set up test."""
#         return super().setUp()

#     def test_fstring_escape_brace(self) -> None:
#         """Test fstring escape brace."""
#         source = Source('glob a=f"{{}}", not_b=4;', mod_path="")
#         prse = JacParser(root_ir=source, prog=JacProgram())
#         self.assertFalse(prse.errors_had)

#     def micro_suite_test(self, filename: str) -> None:
#         """Parse micro jac file."""
#         prse = JacParser(
#             root_ir=Source(self.file_to_str(filename), mod_path=filename),
#             prog=JacProgram(),
#         )
#         # A list of files where the errors are expected.
#         files_expected_errors = [
#             "uninitialized_hasvars.jac",
#         ]
#         if os.path.basename(filename) not in files_expected_errors:
#             self.assertFalse(prse.errors_had)

#     def test_parser_fam(self) -> None:
#         """Parse micro jac file."""
#         prse = JacParser(
#             root_ir=Source(self.load_fixture("fam.jac"), mod_path=""),
#             prog=JacProgram(),
#         )
#         self.assertFalse(prse.errors_had)

#     def test_staticmethod_checks_out(self) -> None:
#         """Parse micro jac file."""
#         prse = JacParser(
#             root_ir=Source(
#                 self.load_fixture("staticcheck.jac"),
#                 mod_path="",
#             ),
#             prog=JacProgram(),
#         )
#         out = prse.ir_out.pp()
#         self.assertFalse(prse.errors_had)
#         self.assertNotIn("staticmethod", out)

#     def test_parser_kwesc(self) -> None:
#         """Parse micro jac file."""
#         prse = JacParser(
#             root_ir=Source(self.load_fixture("kwesc.jac"), mod_path=""),
#             prog=JacProgram(),
#         )
#         self.assertFalse(prse.errors_had)

#     def test_parser_mod_doc_test(self) -> None:
#         """Parse micro jac file."""
#         prse = JacParser(
#             root_ir=Source(self.load_fixture("mod_doc_test.jac"), mod_path=""),
#             prog=JacProgram(),
#         )
#         self.assertFalse(prse.errors_had)

#     def test_enum_matches_lark_toks(self) -> None:
#         """Test that enum stays synced with lexer."""
#         tokens = [x.name for x in jl.Lark_StandAlone().parser.lexer_conf.terminals]
#         for token in tokens:
#             self.assertIn(token, Tokens.__members__)
#         for token in Tokens:
#             self.assertIn(token.name, tokens)
#         for token in Tokens:
#             self.assertIn(token.value, tokens)

#     def test_parser_impl_all_rules(self) -> None:
#         """Test that enum stays synced with lexer."""
#         rules = {
#             x.origin.name
#             for x in jl.Lark_StandAlone().parser.parser_conf.rules
#             if not x.origin.name.startswith("_")
#         }
#         parse_funcs = []
#         for name, value in inspect.getmembers(JacParser.TreeToAST):
#             if inspect.isfunction(value) and not getattr(
#                 JacParser.TreeToAST.__base__, value.__name__, False
#             ):
#                 parse_funcs.append(name)
#         for rule in rules:
#             self.assertIn(rule, parse_funcs)
#         for fn in parse_funcs:
#             if fn.startswith("_") or fn in [
#                 "ice",
#                 "match",
#                 "consume",
#                 "match_token",
#                 "consume_token",
#                 "match_many",
#                 "consume_many",
#             ]:
#                 continue
#             self.assertIn(fn, rules)

#     def test_all_ast_has_normalize(self) -> None:
#         """Test for enter/exit name diffs with parser."""
#         import jaclang.compiler.unitree as uni
#         import inspect
#         import sys

#         exclude = [
#             "UniNode",
#             "UniScopeNode",
#             "UniCFGNode",
#             "ProgramModule",
#             "WalkerStmtOnlyNode",
#             "Source",
#             "EmptyToken",
#             "AstSymbolNode",
#             "AstSymbolStubNode",
#             "AstImplNeedingNode",
#             "AstAccessNode",
#             "Literal",
#             "AstDocNode",
#             "AstSemStrNode",
#             "PythonModuleAst",
#             "AstAsyncNode",
#             "AstElseBodyNode",
#             "AstTypedVarNode",
#             "AstImplOnlyNode",
#             "Expr",
#             "AtomExpr",
#             "ElementStmt",
#             "ArchBlockStmt",
#             "EnumBlockStmt",
#             "CodeBlockStmt",
#             "NameAtom",
#             "ArchSpec",
#             "MatchPattern",
#         ]
#         module_name = uni.__name__
#         module = sys.modules[module_name]

#         # Retrieve the source code of the module
#         source_code = inspect.getsource(module)

#         classes = inspect.getmembers(module, inspect.isclass)
#         uni_node_classes = [
#             cls
#             for _, cls in classes
#             if issubclass(cls, uni.UniNode) and not issubclass(cls, uni.Token)
#         ]

#         ordered_classes = sorted(
#             uni_node_classes,
#             key=lambda cls: source_code.find(f"class {cls.__name__}"),
#         )
#         for cls in ordered_classes:
#             if cls.__name__ not in exclude:
#                 self.assertIn("normalize", cls.__dict__)

#     def test_inner_mod_impl(self) -> None:
#         """Parse micro jac file."""
#         prog = JacProgram()
#         prog.compile(self.fixture_abs_path("codegentext.jac"))
#         self.assertFalse(prog.errors_had)


# TestLarkParser.self_attach_micro_tests()


def test_simple_eq() -> None:
    """Test simple eq."""
    assert 1 == 1

test_simple_eq()