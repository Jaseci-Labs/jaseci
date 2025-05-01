"""Tests for semantic analysis for Jac statements."""

from jaclang.compiler.passes.typecheck import (
    JTypeAnnotatePass,
    JacSemanticMessages,
    SemanticAnalysisPass,
)
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
            self.fixture_abs_path("statements/assignment_err.jac"),
            target=JTypeAnnotatePass,
        )
        SemanticAnalysisPass(out, prog=program)
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
            "12:5 - 12:12": (
                JacSemanticMessages.CONFLICTING_VAR_TYPE,
                {"val_type": "int", "var_type": "Callable[none, [a]]"},
            ),
            "13:5 - 13:14": (JacSemanticMessages.ASSIGN_TO_RTYPE, {"expr": "fn ( )"}),
            "13:5 - 13:0": (
                JacSemanticMessages.PARAM_NUMBER_MISMATCH,
                {"actual_number": "1", "passed_number": "0"},
            ),
            "14:5 - 14:21": (
                JacSemanticMessages.CONFLICTING_VAR_TYPE,
                {"val_type": "float", "var_type": "bool"},
            ),
        }
        expected_warnings: dict[str, SemanticError] = {
            "14:5 - 14:21": (
                JacSemanticMessages.VAR_REDEFINITION,
                {"var_name": "x1", "new_type": "float"},
            ),
            "18:5 - 18:18": (JacSemanticMessages.RETURN_FOR_NONE_ABILITY, {}),
        }

        for e in program.semantic_warnnings_had:
            print(e[1].loc, e[0], e[2])

        for msg, node, msg_frmt in program.semantic_errors_had:
            assert (
                str(node.loc) in expected_errors
            ), f"Missing semantic errors for {node.loc}"
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

    def test_function_call_semantics(self) -> None:
        """Test basic semantic analysis for function calls."""
        settings.enable_jac_semantics = True
        program = JacProgram()
        out = program.compile(
            self.fixture_abs_path("statements/func_call_err.jac"),
            target=JTypeAnnotatePass,
        )
        SemanticAnalysisPass(out, prog=program)
        settings.enable_jac_semantics = False

        for e in program.semantic_warnnings_had:
            print(e[1].loc, e[0], e[2])

        expected_errors: dict[str, SemanticError] = {
            "11:1 - 12:2": (JacSemanticMessages.MISSING_RETURN_STATEMENT, {}),
            "4:5 - 4:14": (
                JacSemanticMessages.CONFLICTING_RETURN_TYPE,
                {"actual_return_type": "str", "formal_return_type": "int"},
            ),
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
            "29:5 - 29:24": (JacSemanticMessages.REPEATED_ARG, {"param_name": "a"}),
            "31:5 - 31:26": (
                JacSemanticMessages.PARAM_NUMBER_MISMATCH,
                {"actual_number": "1", "passed_number": "3"},
            ),
            "32:5 - 32:26": (
                JacSemanticMessages.UNDEFINED_FUNCTION_NAME,
                {"func_name": "function5"},
            ),
        }
        expected_warnings: dict[str, SemanticError] = {
            "15:5 - 15:18": (JacSemanticMessages.RETURN_FOR_NONE_ABILITY, {})
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
