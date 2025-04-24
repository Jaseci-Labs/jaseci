import traceback

from jaclang.compiler.absyntree import Source
from jaclang.compiler.parser import JacParser
from jaclang.compiler.program import JacProgram
from jaclang.utils.test import TestCase


class TestSliceParsing(TestCase):
    """Tests for proper slice parsing including `:-1` behavior."""

    def test_slice_with_space_parses(self) -> None:
        """Test that slice with space after colon parses correctly."""
        code = "with entry { arr = [0,1,2,3,4,5,6,7,8,9]; x = arr[5: -1]; }"
        source = Source(code, mod_path="test")
        parser = JacParser(root_ir=source, prog=JacProgram())
        self.assertFalse(parser.errors_had)

    def test_slice_no_space_debug(self) -> None:
        """Debug test to capture detailed error information for slice without space."""
        code = "with entry { arr = [0,1,2,3,4,5,6,7,8,9]; x = arr[5:-1]; }"
        source = Source(code, mod_path="test")

        # Inner function for detailed error reporting
        def debug_error_callback(e: Exception) -> bool:
            """Callback to print detailed parsing error information."""
            print("\n===== DEBUG ERROR INFORMATION =====")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")

            # Safely access error position attributes
            line = getattr(e, "line", "N/A")
            column = getattr(e, "column", "N/A")
            print(f"Error position: line {line}, column {column}")

            # Safely access position in stream for context
            pos = getattr(e, "pos_in_stream", None)
            if pos is not None:
                context_start = max(0, pos - 10)
                context_end = pos + 10
                print(f"Error context: {code[context_start:context_end]}")
                # Adjust caret position based on context window
                caret_offset = pos - context_start
                print(f"                {' ' * caret_offset}^")
            else:
                print("Error context: Position in stream not available.")

            print(f"Expected: {getattr(e, 'expected', 'N/A')}")
            print(f"Considered tokens: {getattr(e, 'considered_tokens', 'N/A')}")

            # Print the entire traceback for more context
            print("\nTraceback:")
            traceback.print_exc()

            print("===== END DEBUG INFO =====\n")
            return False  # Continue with normal error handling (don't suppress)

        # Create parser with our debug callback
        parser = JacParser(root_ir=source, prog=JacProgram())
        original_callback = parser.error_callback  # Save the original callback
        parser.error_callback = debug_error_callback

        try:
            # Attempt parsing, which might trigger our debug callback
            parser.transform(ir_in=source)
        finally:
            # Ensure the original callback is restored
            parser.error_callback = original_callback

        # Report any errors found after parsing attempt
        if parser.errors_had:
            print("\nErrors found during parsing:")
            for error in parser.errors_had:
                print(f"- {error}")
        else:
            print("\nNo parsing errors reported!")
