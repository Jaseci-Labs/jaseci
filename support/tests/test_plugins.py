"""Test Jac Plugins."""

import os
import subprocess

from jaclang.utils.test import TestCase


class JacPlugins(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_streamlit(self) -> None:
        """Basic test for pass."""
        directory = self.fixture_abs_path("../../../support/streamlit")
        os.chdir(directory)
        install_command = "pip install -e ."
        install_result = subprocess.run(
            install_command, shell=True, capture_output=True, text=True
        )
        command = "jac streamlit -h"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        self.assertIn(
            "Successfully uninstalled jac-streamlit-0.0.1", install_result.stdout
        )
        self.assertIn("Streamlit the specified .jac file", result.stdout)
        self.assertIn(
            ":param filename: The path to the .jac file.\n\npositional arguments:\n",
            result.stdout,
        )
