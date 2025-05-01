"""Tests for semantic analysis for Jac declarations."""

from jaclang.compiler.passes.main import CompilerMode
from jaclang.compiler.passes.typecheck import JacSemanticMessages
from jaclang.compiler.program import JacProgram
from jaclang.settings import settings
from jaclang.utils.test import TestCase


NodeLocation = str
SemanticError = tuple[JacSemanticMessages, dict[str, str]]


class TestDeclSemantics(TestCase):
    """Tests for semantic analysis for Jac declarations."""

    def test_function_decl_semantics(self) -> None:
        """Test basic semantic analysis for assignments & var declarations."""
        settings.enable_jac_semantics = True
        program = JacProgram()
        program.compile(
            self.fixture_abs_path("declarations/function.jac"),
            mode=CompilerMode.QUICKCHECK,
        )
        settings.enable_jac_semantics = False

        for e in program.semantic_errors_had:
            print(e[1].loc, e[0], e[2])

        expected_errors: dict[str, SemanticError] = {
            "9:1 - 10:2": (JacSemanticMessages.MISSING_RETURN_STATEMENT, {}),
            "17:5 - 17:14": (
                JacSemanticMessages.CONFLICTING_RETURN_TYPE,
                {"actual_return_type": "bool", "formal_return_type": "int"},
            ),
        }
        expected_warnings: dict[str, SemanticError] = {
            "3:5 - 3:14": (JacSemanticMessages.RETURN_FOR_NONE_ABILITY, {})
        }

        for msg, node, msg_frmt in program.semantic_errors_had:
            assert str(node.loc) in expected_errors, "Missing semantic errors"
            expected_error = expected_errors.pop(str(node.loc))
            assert msg == expected_error[0]
            assert msg_frmt == expected_error[1]
        assert len(expected_errors.items()) == 0, "Extra semantic errors"

        for msg, node, msg_frmt in program.semantic_warnnings_had:
            assert str(node.loc) in expected_warnings, "Missing semantic warning"
            expected_error = expected_warnings.pop(str(node.loc))
            assert msg == expected_error[0]
            assert msg_frmt == expected_error[1]
        assert len(expected_errors.items()) == 0, "Extra semantic warnings"


TestDeclSemantics().test_function_decl_semantics()
