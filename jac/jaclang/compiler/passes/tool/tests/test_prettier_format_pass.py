"""Test prettier formatter pass module."""

import os
import tempfile
from difflib import unified_diff

import jaclang.compiler.unitree as uni
from jaclang.compiler.passes.tool.formatter_manager import (
    FormatterManager,
    FormatterStyle,
)
from jaclang.compiler.passes.tool.prettier_formatter_pass import PrettierFormatPass
from jaclang.utils.test import TestCaseMicroSuite


class PrettierFormatPassTests(TestCaseMicroSuite):
    """Test prettier formatter pass."""

    def test_simple_function(self):
        """Test formatting of a simple function."""
        # Test code
        test_code = """def process_guess(guess: int) {
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
    }"""

        # Format the code
        with tempfile.NamedTemporaryFile(suffix=".jac", mode="w+") as tmp:
            tmp.write(test_code)
            tmp.flush()

            # Format using prettier formatter
            formatted_code = FormatterManager.format_jac_file(
                tmp.name, style=FormatterStyle.PRETTIER
            )

            # Check if the code was actually formatted
            self.assertNotEqual(test_code, formatted_code)

            # Basic checks on the formatted code
            self.assertIn("def process_guess", formatted_code)
            self.assertIn("if guess > self.correct_number", formatted_code)
            self.assertIn('print("Too high!")', formatted_code)
            self.assertIn("elif guess < self.correct_number", formatted_code)
            self.assertIn("self.attempts -= 1", formatted_code)

    def test_compare_formatters(self):
        """Compare the output of both formatters."""
        # Test code
        test_code = """def process_guess(guess: int) {
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
    }"""

        with tempfile.NamedTemporaryFile(suffix=".jac", mode="w+") as tmp:
            tmp.write(test_code)
            tmp.flush()

            # Format using classic formatter
            classic_formatted = FormatterManager.format_jac_file(
                tmp.name, style=FormatterStyle.CLASSIC
            )

            # Format using prettier formatter
            prettier_formatted = FormatterManager.format_jac_file(
                tmp.name, style=FormatterStyle.PRETTIER
            )

            # Both formatters should produce valid code
            self.assertIn("def process_guess", classic_formatted)
            self.assertIn("def process_guess", prettier_formatted)

            # Print the diff between the two formatters
            diff = "\n".join(
                unified_diff(
                    classic_formatted.splitlines(),
                    prettier_formatted.splitlines(),
                    fromfile="classic",
                    tofile="prettier",
                )
            )

            print(f"Differences between formatters:\n{diff}")

            # We expect the formatters to produce different output, but both should be valid
            self.assertNotEqual(classic_formatted, prettier_formatted)
