"""Tests for semantic analysis for Jac statements."""

from jaclang.compiler.passes.main import DefUsePass
from jaclang.compiler.passes.typecheck import JacSemanticMessages, SemanticAnalysisPass
from jaclang.compiler.program import JacProgram
from jaclang.settings import settings
from jaclang.utils.test import TestCase


NodeLocation = str
SemanticError = tuple[JacSemanticMessages, dict[str, str]]


class TestStmtSemantics(TestCase):
    """Semantic analysis for jac statements."""

    def test_assignment_semantics(self) -> None:
        """Test basic semantic analysis for assignments & var declarations."""
        settings.enable_jac_semantics = True
        program = JacProgram()
        out = program.compile(
            self.fixture_abs_path("statements/assignment.jac"),
            target=DefUsePass,
        )
        sem_analysis_pass = SemanticAnalysisPass(out, prog=program)
        settings.enable_jac_semantics = False

        expected_errors: dict[str, SemanticError] = {
            "6:5 - 6:19": (
                JacSemanticMessages.CONFLICTING_VAR_TYPE,
                {"val_type": "float", "var_type": "int"},
            ),
            "7:5 - 7:18": (
                JacSemanticMessages.CONFLICTING_VAR_TYPE,
                {"val_type": "int", "var_type": "bool"},
            ),
            "10:5 - 10:13": (
                JacSemanticMessages.CONFLICTING_VAR_TYPE,
                {"val_type": "int", "var_type": "bool"},
            ),
            "11:5 - 11:13": (
                JacSemanticMessages.CONFLICTING_VAR_TYPE,
                {"val_type": "int", "var_type": "bool"},
            ),
        }
        expected_warnings: dict[str, SemanticError] = {}

        for msg, node, msg_frmt in sem_analysis_pass.semantic_errors:
            assert str(node.loc) in expected_errors, "Missing semantic errors"
            expected_error = expected_errors.pop(str(node.loc))
            assert msg == expected_error[0]
            assert msg_frmt == expected_error[1]
        assert len(expected_errors.items()) == 0, "Extra semantic errors"

        for msg, node, msg_frmt in sem_analysis_pass.semantic_warning:
            assert str(node.loc) in expected_warnings, "Missing semantic warning"
            expected_error = expected_warnings.pop(str(node.loc))
            assert msg == expected_error[0]
            assert msg_frmt == expected_error[1]
        assert len(expected_errors.items()) == 0, "Extra semantic warnings"

    def test_function_call_semantics(self) -> None:
        """Test basic semantic analysis for function calls."""
        settings.enable_jac_semantics = True
        program = JacProgram()
        out = program.compile(
            self.fixture_abs_path("statements/func_call.jac"),
            target=DefUsePass,
        )
        sem_analysis_pass = SemanticAnalysisPass(out, prog=program)
        settings.enable_jac_semantics = False

        # for e in sem_analysis_pass.semantic_warning:
        #     print(e[1].loc, e[0], e[2])

        expected_errors: dict[str, SemanticError] = {
            "4:5 - 4:14": (
                JacSemanticMessages.CONFLICTING_RETURN_TYPE,
                {"actual_return_type": "str", "formal_return_type": "int"},
            ),
            "11:1 - 12:2": (JacSemanticMessages.MISSING_RETURN_STATEMENT, {}),
            "21:5 - 21:25": (
                JacSemanticMessages.CONFLICTING_VAR_TYPE,
                {"val_type": "str", "var_type": "int"},
            ),
            "23:5 - 23:26": (
                JacSemanticMessages.ARG_NAME_NOT_FOUND,
                {"param_name": "c", "arg_name": "function2"},
            ),
            "24:5 - 24:26": (JacSemanticMessages.REPEATED_ARG, {"param_name": "a"}),
            "25:5 - 25:26": (
                JacSemanticMessages.CONFLICTING_ARG_TYPE,
                {"param_name": "b", "formal_type": "str", "actual_type": "int"},
            ),
            "26:5 - 26:20": (
                JacSemanticMessages.PARAM_NUMBER_MISMATCH,
                {"actual_number": "2", "passed_number": "1"},
            ),
            "27:5 - 27:26": (
                JacSemanticMessages.PARAM_NUMBER_MISMATCH,
                {"actual_number": "2", "passed_number": "3"},
            ),
            "28:5 - 28:30": (
                JacSemanticMessages.PARAM_NUMBER_MISMATCH,
                {"actual_number": "2", "passed_number": "3"},
            ),
            "30:5 - 30:26": (
                JacSemanticMessages.PARAM_NUMBER_MISMATCH,
                {"actual_number": "1", "passed_number": "3"},
            ),
            "31:5 - 31:26": (
                JacSemanticMessages.UNDEFINED_FUNCTION_NAME,
                {"func_name": "function5"},
            ),
        }
        expected_warnings: dict[str, SemanticError] = {
            "15:5 - 15:18": (JacSemanticMessages.RETURN_FOR_NONE_ABILITY, {})
        }

        for msg, node, msg_frmt in sem_analysis_pass.semantic_errors:
            assert str(node.loc) in expected_errors, "Missing semantic errors"
            expected_error = expected_errors.pop(str(node.loc))
            assert msg == expected_error[0]
            assert msg_frmt == expected_error[1]
        assert len(expected_errors.items()) == 0, "Extra semantic errors"

        for msg, node, msg_frmt in sem_analysis_pass.semantic_warning:
            assert str(node.loc) in expected_warnings, "Missing semantic warning"
            expected_error = expected_warnings.pop(str(node.loc))
            assert msg == expected_error[0]
            assert msg_frmt == expected_error[1]
        assert len(expected_errors.items()) == 0, "Extra semantic warnings"
