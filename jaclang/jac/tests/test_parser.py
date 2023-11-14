"""Tests for Jac parser."""
import inspect

from jaclang.jac import jac_lark as jl
from jaclang.jac.absyntree import JacSource
from jaclang.jac.constant import Tokens
from jaclang.jac.parser import JacParser
from jaclang.utils.test import TestCaseMicroSuite


class TestLarkParser(TestCaseMicroSuite):
    """Test Jac self.prse."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_fstring_escape_brace(self) -> None:
        """Test fstring escape brace."""
        source = JacSource('glob a=f"{{}}", not_b=4;', mod_path="")
        prse = JacParser(input_ir=source)
        self.assertFalse(prse.errors_had)

    def micro_suite_test(self, filename: str) -> None:
        """Parse micro jac file."""
        prse = JacParser(
            input_ir=JacSource(self.file_to_str(filename), mod_path=filename),
        )
        self.assertFalse(prse.errors_had)

    def test_parser_fam(self) -> None:
        """Parse micro jac file."""
        prse = JacParser(input_ir=JacSource(self.load_fixture("fam.jac"), mod_path=""))
        self.assertFalse(prse.errors_had)

    def test_cli_parse(self) -> None:
        """Parse micro jac file."""
        prse = JacParser(
            input_ir=JacSource(
                self.load_fixture("../../../cli/cli_impl.jac"),
                mod_path="../../../cli/cli_impl.jac",
            )
        )
        self.assertFalse(prse.errors_had)

    def test_parser_kwesc(self) -> None:
        """Parse micro jac file."""
        prse = JacParser(
            input_ir=JacSource(self.load_fixture("kwesc.jac"), mod_path="")
        )
        self.assertFalse(prse.errors_had)

    def test_parser_mod_doc_test(self) -> None:
        """Parse micro jac file."""
        prse = JacParser(
            input_ir=JacSource(self.load_fixture("mod_doc_test.jac"), mod_path="")
        )
        self.assertFalse(prse.errors_had)

    def test_enum_matches_lark_toks(self) -> None:
        """Test that enum stays synced with lexer."""
        tokens = [x.name for x in jl.Lark_StandAlone().parser.lexer_conf.terminals]
        for token in tokens:
            self.assertIn(token, Tokens.__members__)
        for token in Tokens:
            self.assertIn(token.name, tokens)
        for token in Tokens:
            self.assertIn(token.value, tokens)

    def test_parser_impl_all_rules(self) -> None:
        """Test that enum stays synced with lexer."""
        rules = {
            x.origin.name
            for x in jl.Lark_StandAlone().parser.parser_conf.rules
            if not x.origin.name.startswith("_")
        }
        parse_funcs = []
        for name, value in inspect.getmembers(JacParser.TreeToAST):
            if inspect.isfunction(value) and not getattr(
                JacParser.TreeToAST.__base__, value.__name__, False
            ):
                parse_funcs.append(name)
        for i in rules:
            self.assertIn(i, parse_funcs)
        for i in parse_funcs:
            if i in ["binary_expr_unwind", "ice", "nu"]:
                continue
            self.assertIn(i, rules)


TestLarkParser.self_attach_micro_tests()
