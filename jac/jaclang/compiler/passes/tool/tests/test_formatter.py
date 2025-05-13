"""Tests for the Jac formatter passes."""

import unittest
from pathlib import Path

import jaclang.compiler.unitree as uni
from jaclang.compiler.parser import JacParser
from jaclang.compiler.passes.tool import FuseCommentsPass, JacFormatPass, NewJacFormatPass
from jaclang.compiler.program import JacProgram
from jaclang.settings import settings


class TestFormatters(unittest.TestCase):
    """Test the Jac formatters."""

    def setUp(self) -> None:
        """Set up the test."""
        # Sample code to format - the process_guess method from the example
        self.sample_code = """
def process_guess(guess: int) {
        if guess > self.correct_number {
            print("Too high!");
        } elif guess < self.correct_number {
            print("Too low!");
        } else {
            print("Congratulations! You guessed correctly.");
            self.attempts = 0;# end the game
            self.won = True;
        }
        self.attempts -= 1;
        print(f"You have {self.attempts} attempts left.");
    }
"""
        # Create a source object
        self.source = uni.Source(self.sample_code, mod_path="test.jac")
        # Parse the source
        self.prog = JacProgram()
        self.parser = JacParser(root_ir=self.source, prog=self.prog)
        # Run FuseCommentsPass
        self.fuse_comments = FuseCommentsPass(ir_in=self.parser.ir_out, prog=self.prog)

    def test_classic_formatter(self) -> None:
        """Test the classic formatter."""
        # Set formatter type to classic
        settings.formatter_type = "classic"
        
        # Run the classic formatter
        classic_formatter = JacFormatPass(ir_in=self.fuse_comments.ir_out, prog=self.prog)
        classic_formatter.before_pass()
        classic_formatter.enter_node(self.fuse_comments.ir_out)
        classic_formatter.exit_module(self.fuse_comments.ir_out)
        
        # Get the formatted code
        formatted_code = classic_formatter.ir_out.gen.jac
        
        # Check that the formatted code is not empty
        self.assertTrue(formatted_code)
        
        # Check that the formatted code contains key elements
        self.assertIn("def process_guess", formatted_code)
        self.assertIn("if guess > self.correct_number", formatted_code)
        self.assertIn("print(f\"You have {self.attempts} attempts left.\");", formatted_code)

    def test_prettier_formatter(self) -> None:
        """Test the prettier formatter."""
        # Set formatter type to prettier
        settings.formatter_type = "prettier"
        
        # Run the prettier formatter
        prettier_formatter = NewJacFormatPass(ir_in=self.fuse_comments.ir_out, prog=self.prog)
        prettier_formatter.before_pass()
        prettier_formatter.enter_node(self.fuse_comments.ir_out)
        prettier_formatter.exit_module(self.fuse_comments.ir_out)
        
        # Get the formatted code
        formatted_code = prettier_formatter.ir_out.gen.jac
        
        # Check that the formatted code is not empty
        self.assertTrue(formatted_code)
        
        # Check that the formatted code contains key elements
        self.assertIn("def process_guess", formatted_code)
        self.assertIn("if guess > self.correct_number", formatted_code)
        self.assertIn("print(f\"You have {self.attempts} attempts left.\");", formatted_code)

    def test_formatter_selection(self) -> None:
        """Test that the formatter selection works."""
        # Test with classic formatter
        settings.formatter_type = "classic"
        self.assertEqual(
            "classic",
            settings.formatter_type,
            "Formatter type should be 'classic'",
        )
        
        # Test with prettier formatter
        settings.formatter_type = "prettier"
        self.assertEqual(
            "prettier",
            settings.formatter_type,
            "Formatter type should be 'prettier'",
        )


if __name__ == "__main__":
    unittest.main()
