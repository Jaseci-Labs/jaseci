"""Test Jac cli module."""

import contextlib
import inspect
import io
import os
import re
import subprocess
import sys
import traceback
import unittest
from jaclang.cli import cli
from jaclang.cli.cmdreg import cmd_registry, extract_param_descriptions
from jaclang.runtimelib.builtin import dotgen
from jaclang.utils.test import TestCase

from jaclang.settings import settings


class JacCliTests(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_statements_assignments(self) -> None:
        """Basic test for pass."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        sys.stderr = captured_output
        
        cli.check(self.fixture_abs_path("type_check_tests/statements/assignment_err.jac"))
        
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        stdout_value = captured_output.getvalue()

        expected_stdout_values = (
            "line 4, col 5: Error: Can't assign a value 'builtins.float' to a 'builtins.int' object",
            "line 6, col 5: Error: Can't assign a value 'builtins.bool' to a 'builtins.float' object",
            "line 10, col 5: Error: Can't assign a value 'builtins.int' to a JFunctionType[(a: instance of int) -> None] object",
            "Errors: 3, Warnings: 1",
        )
        
        for exp in expected_stdout_values:
            self.assertIn(exp, stdout_value)

    def test_statements_func_call(self) -> None:
        """Basic test for pass."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        sys.stderr = captured_output
        
        cli.check(self.fixture_abs_path("type_check_tests/statements/func_call_err.jac"))
        
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        stdout_value = captured_output.getvalue()

        expected_stdout_values = (
            "line 11, col 1: Missing return statement",
            "line 4, col 5: Ability have a return type 'builtins.str' but got assigned a type 'builtins.int'",
            "line 21, col 5: Error: Can't assign a value 'builtins.str' to a 'builtins.int' object",
            "line 25, col 5: Error: Can't assign a value 'builtins.int' to a parameter 'b' of type 'builtins.str'",
            "line 27, col 5: Error: Can't assign a value 'builtins.int' to a parameter 'b' of type 'builtins.str'",
            "line 34, col 15: Error: Can't assign a value 'builtins.str' to a parameter 'a' of type 'builtins.int'",
            "line 34, col 5: Error: Can't assign a value JNoneType[None] to a parameter 'a' of type 'builtins.int'",
            "line 38, col 5: Ability have a return type 'builtins.bool' but got assigned a type 'builtins.str'",
            "Errors: 8, Warnings: 1"
        )
        
        for exp in expected_stdout_values:
            self.assertIn(exp, stdout_value)
    
    def test_declarations_function(self) -> None:
        """Basic test for pass."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        sys.stderr = captured_output
        
        cli.check(self.fixture_abs_path("type_check_tests/declarations/function_err.jac"))
        
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        stdout_value = captured_output.getvalue()

        expected_stdout_values = (
            "line 9, col 1: Missing return statement",
            "line 17, col 5: Ability have a return type 'builtins.bool' but got assigned a type 'builtins.int'",
            "Errors: 2, Warnings: 1"
        )
        
        for exp in expected_stdout_values:
            self.assertIn(exp, stdout_value)
    
    def test_declarations_archetype(self) -> None:
        """Basic test for pass."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        sys.stderr = captured_output
        
        cli.check(self.fixture_abs_path("type_check_tests/declarations/archetype_err.jac"))
        
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        stdout_value = captured_output.getvalue()

        expected_stdout_values = (
            "line 3, col 9: 'str_obj' was defined before",
            "line 13, col 9: Error: Can't assign a value 'builtins.int' to a parameter 'str_obj' of type 'builtins.str'",
            "line 16, col 5: Error: Can't assign a value 'archetype_err.A' to a 'builtins.int' object",
            "line 17, col 5: Error: Can't assign a value 'builtins.int' to a 'archetype_err.A' object",
            "line 29, col 10: Error: Can't assign a value 'builtins.str' to a parameter 'c' of type 'builtins.int'",
            "line 30, col 10: Error: Can't assign a value 'archetype_err.B' to a parameter 'c' of type 'builtins.int'",
            "Errors: 6, Warnings: 0"
        )
        
        for exp in expected_stdout_values:
            self.assertIn(exp, stdout_value)
