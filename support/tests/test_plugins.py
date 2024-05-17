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
        """Test for streamilt plugin."""
        directory = self.fixture_abs_path("../../../support/streamlit")
        os.chdir(directory)
        install_command = "pip install -e ."
        install_result = subprocess.run(
            install_command, shell=True, capture_output=True, text=True
        )
        command = "jac streamlit -h"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        self.assertIn(
            "Successfully installed jac-streamlit-0.0.1", install_result.stdout
        )
        self.assertIn("Streamlit the specified .jac file", result.stdout)
        self.assertIn(
            ":param filename: The path to the .jac file.\n\npositional arguments:\n",
            result.stdout,
        )

        # file_name = os.path.join(self.fixture_abs_path("./"), "streamlit.jac")
        # command = f"jac streamlit {file_name}"
        # result = subprocess.Popen(
        #     command,
        #     shell=True,
        #     stdout=subprocess.PIPE,
        #     stderr=subprocess.STDOUT,
        #     universal_newlines=True,
        #     text=True,
        # )
        # out = [result.stdout.readline() for i in range(2)] if result.stdout else []
        # self.assertIn("  You can now view your Streamlit app in your browser.\n", out)
        # result.terminate()
