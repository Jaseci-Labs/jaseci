"""Tests for semantic analysis for Jac declarations."""

from jaclang.compiler.passes.main import CompilerMode
from jaclang.compiler.passes.typecheck import JacSemanticMessages
from jaclang.compiler.passes.typecheck.tests.semantic_test import SemanticTest
from jaclang.compiler.program import JacProgram
from jaclang.settings import settings


class TestDeclSemantics(SemanticTest):
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

        self.assert_semantic_errors(
            {
                "9:1 - 10:2": (JacSemanticMessages.MISSING_RETURN_STATEMENT, {}),
                "17:5 - 17:14": (
                    JacSemanticMessages.CONFLICTING_RETURN_TYPE,
                    {"actual_return_type": "bool", "formal_return_type": "int"},
                ),
            },
            program.semantic_errors_had,
        )

        self.assert_semantic_errors(
            {"3:5 - 3:14": (JacSemanticMessages.RETURN_FOR_NONE_ABILITY, {})},
            program.semantic_warnnings_had,
            is_warning=True,
        )

    def test_architype_decl_semantics(self) -> None:
        """Test basic semantic analysis for assignments & var declarations."""
        settings.enable_jac_semantics = True
        program = JacProgram()
        program.compile(
            self.fixture_abs_path("declarations/architype_err.jac"),
            mode=CompilerMode.QUICKCHECK,
        )
        settings.enable_jac_semantics = False

        for e in program.semantic_errors_had:
            print(e[1].loc, e[0], e[2])

        self.assert_semantic_errors(
            {
                "3:9 - 3:23": (
                    JacSemanticMessages.CLASS_VAR_REDEFINITION,
                    {"var_name": "str_obj"},
                ),
                "13:9 - 13:14": (
                    JacSemanticMessages.PARAM_NUMBER_MISMATCH,
                    {"actual_number": "0", "passed_number": "1"},
                ),
                "16:5 - 16:16": (
                    JacSemanticMessages.CONFLICTING_VAR_TYPE,
                    {"val_type": "JInstanceOf[JClass[A]]", "var_type": "int"},
                ),
                "17:5 - 17:11": (
                    JacSemanticMessages.CONFLICTING_VAR_TYPE,
                    {"val_type": "int", "var_type": "JInstanceOf[JClass[A]]"},
                ),
                "27:10 - 27:13": (
                    JacSemanticMessages.PARAM_NUMBER_MISMATCH,
                    {"actual_number": "1", "passed_number": "0"},
                ),
                "29:10 - 29:16": (
                    JacSemanticMessages.CONFLICTING_ARG_TYPE,
                    {"param_name": "c", "formal_type": "int", "actual_type": "str"},
                ),
                "30:10 - 30:17": (
                    JacSemanticMessages.CONFLICTING_ARG_TYPE,
                    {
                        "param_name": "c",
                        "formal_type": "int",
                        "actual_type": "JInstanceOf[JClass[B]]",
                    },
                ),
            },
            program.semantic_errors_had,
        )

        self.assert_semantic_errors({}, program.semantic_warnnings_had, is_warning=True)
