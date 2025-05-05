"""This class is used as the base class for Semantic analysis tests."""

from jaclang.compiler.passes.typecheck import JacSemanticMessages, SemanticErrorObject
from jaclang.utils.test import TestCase


SemanticError = tuple[JacSemanticMessages, dict[str, str]]


class SemanticTest(TestCase):
    """Tests for semantic analysis for Jac declarations."""

    def assert_semantic_errors(
        self,
        expected_errors: dict[str, SemanticError],
        found_errors: list[SemanticErrorObject],
        is_warning: bool = False,
    ) -> None:
        """Check that the found errors are the same as the expected ones."""
        for msg, node, msg_frmt in found_errors:
            error_warrning = "warnings" if is_warning else "errors"
            assert (
                str(node.loc) in expected_errors
            ), f"Missing semantic {error_warrning}"
            expected_error = expected_errors.pop(str(node.loc))
            assert msg == expected_error[0]
            assert msg_frmt == expected_error[1]
        assert len(expected_errors.items()) == 0, f"Extra semantic {error_warrning}"
