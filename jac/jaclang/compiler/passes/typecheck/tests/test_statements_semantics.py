"""Tests for semantic analysis for Jac statements."""

from jaclang.compiler.passes.main import CompilerMode
from jaclang.compiler.passes.typecheck import JacSemanticMessages
from jaclang.compiler.passes.typecheck.tests.semantic_test import SemanticTest
from jaclang.compiler.program import JacProgram
from jaclang.settings import settings


class TestStmtSemantics(SemanticTest):
    """Semantic analysis for jac statements."""

    def test_assignment_semantics(self) -> None:
        """Test basic semantic analysis for assignments & var declarations."""
        settings.enable_jac_semantics = True
        program = JacProgram()
        program.compile(
            self.fixture_abs_path("statements/assignment_err.jac"),
            mode=CompilerMode.QUICKCHECK,
        )
        settings.enable_jac_semantics = False

        self.assert_semantic_errors(
            expected_errors={
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
                "13:5 - 13:14": (
                    JacSemanticMessages.ASSIGN_TO_RTYPE,
                    {"expr": "fn ( )"},
                ),
                "13:5 - 13:0": (
                    JacSemanticMessages.PARAM_NUMBER_MISMATCH,
                    {"actual_number": "1", "passed_number": "0"},
                ),
                "14:5 - 14:21": (
                    JacSemanticMessages.CONFLICTING_VAR_TYPE,
                    {"val_type": "float", "var_type": "bool"},
                ),
            },
            found_errors=program.semantic_errors_had,
        )

        self.assert_semantic_errors(
            expected_errors={
                "14:5 - 14:21": (
                    JacSemanticMessages.VAR_REDEFINITION,
                    {"var_name": "x1", "new_type": "float"},
                ),
                "18:5 - 18:18": (JacSemanticMessages.RETURN_FOR_NONE_ABILITY, {}),
            },
            found_errors=program.semantic_warnnings_had,
            is_warning=True,
        )

    def test_function_call_semantics(self) -> None:
        """Test basic semantic analysis for function calls."""
        settings.enable_jac_semantics = True
        program = JacProgram()
        program.compile(
            self.fixture_abs_path("statements/func_call_err.jac"),
            mode=CompilerMode.QUICKCHECK,
        )
        settings.enable_jac_semantics = False

        for e in program.semantic_errors_had:
            print(e[1].loc, e[0], e[2])

        self.assert_semantic_errors(
            expected_errors={
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
                "33:5 - 33:0": (
                    JacSemanticMessages.EXPR_NOT_CALLABLE,
                    {"expr": "9 ( )"},
                ),
                "34:5 - 34:30": (
                    JacSemanticMessages.CONFLICTING_ARG_TYPE,
                    {"param_name": "a", "formal_type": "int", "actual_type": "none"},
                ),
                "34:15 - 34:29": (
                    JacSemanticMessages.CONFLICTING_ARG_TYPE,
                    {"param_name": "a", "formal_type": "int", "actual_type": "str"},
                ),
                "38:5 - 38:24": (
                    JacSemanticMessages.CONFLICTING_RETURN_TYPE,
                    {"actual_return_type": "bool", "formal_return_type": "str"},
                ),
            },
            found_errors=program.semantic_errors_had,
        )

        self.assert_semantic_errors(
            expected_errors={
                "15:5 - 15:18": (JacSemanticMessages.RETURN_FOR_NONE_ABILITY, {})
            },
            found_errors=program.semantic_warnnings_had,
            is_warning=True,
        )
