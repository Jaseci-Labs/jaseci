"""Test Jac Plugins."""

import os
import subprocess

from jaclang.utils.test import TestCase


class JacStreamlitPlugin(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_streamlit(self) -> None:
        """Basic test for pass."""
        directory = self.fixture_abs_path("../../../streamlit")
        os.chdir(directory)
        install_command = "pip install -e ."
        command_streamlit = "jac streamlit -h"
        command_dot_view = "jac dot_view -h"
        install_result = subprocess.run(
            install_command, shell=True, capture_output=True, text=True
        )
        result = subprocess.run(
            command_streamlit, shell=True, capture_output=True, text=True
        )
        dot_result = subprocess.run(
            command_dot_view, shell=True, capture_output=True, text=True
        )
        self.assertIn(
            "Successfully installed jac-streamlit-0.0.1", install_result.stdout
        )
        self.assertIn("Streamlit the specified .jac file", result.stdout)
        self.assertIn(
            ":param filename: The path to the .jac file.\n\npositional arguments:\n",
            result.stdout,
        )
        self.assertIn(
            "View the content of a DOT file. in Streamlit Application.",
            dot_result.stdout,
        )
