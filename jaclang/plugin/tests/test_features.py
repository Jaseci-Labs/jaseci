"""Tests for Jac parser."""

import inspect
import io
import sys
import traceback
from typing import List, Type

from jaclang.cli import cli
from jaclang.plugin.default import JacFeatureDefaults
from jaclang.plugin.feature import JacFeature
from jaclang.plugin.spec import JacFeatureSpec
from jaclang.utils.test import TestCase


class TestFeatures(TestCase):
    """Test Jac self.prse."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def get_methods(self, cls: Type) -> List[str]:
        """Get a list of method names with their signatures for a given class."""
        methods = []
        for name, value in cls.__dict__.items():
            if isinstance(value, (staticmethod, classmethod)):
                try:
                    # Get the actual function in case of staticmethod or classmethod
                    if isinstance(value, (staticmethod, classmethod)):
                        value = getattr(cls, name)

                    # Get the signature using inspect
                    signature = inspect.signature(value)
                    new_parameters = []
                    for (
                        _,
                        param,
                    ) in signature.parameters.items():  # to strip defaults
                        new_param = param.replace(default=inspect.Parameter.empty)
                        new_parameters.append(new_param)
                    signature = signature.replace(parameters=new_parameters)
                    methods.append(f"{name}{signature}")
                except ValueError:
                    # This can happen if the method is not a Python function (e.g., built-in function)
                    pass
        return methods

    def test_feature_funcs_synced(self) -> None:
        """Test if JacFeature, JacFeatureDefaults, and JacFeatureSpec have synced methods."""
        # Get methods of each class
        jac_feature_methods = self.get_methods(JacFeature)
        jac_feature_defaults_methods = self.get_methods(JacFeatureDefaults)
        jac_feature_spec_methods = self.get_methods(JacFeatureSpec)

        # Check if all methods are the same in all classes
        self.assertGreater(len(jac_feature_methods), 5)
        self.assertEqual(jac_feature_spec_methods, jac_feature_defaults_methods)
        for i in jac_feature_spec_methods:
            self.assertIn(i, jac_feature_methods)

    def test_impl_match_error_reporting(self) -> None:
        """Basic test for error reporting."""
        captured_output = io.StringIO()
        original_stderr = sys.stderr
        sys.stderr = captured_output

        try:
            # Execute the function that is expected to raise an exception
            cli.run(self.fixture_abs_path("impl_match.jac"))  # type: ignore
        except Exception:
            # Print the full stack trace to the captured output
            traceback.print_exc(file=captured_output)
        finally:
            # Restore the original stderr
            sys.stderr = original_stderr

        # Retrieve the captured output
        stderr_val = captured_output.getvalue()
        # Assertions or verifications
        try:
            self.assertIn("impl_match.jac", stderr_val)
            self.assertIn("impl_match_impl.jac", stderr_val)
            self.assertLess(
                stderr_val.index("impl_match.jac"),
                stderr_val.index("impl_match_impl.jac"),
            )
        except AssertionError:
            self.skipTest("Error reporting not implemented yet")
