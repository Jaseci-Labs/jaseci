"""Module for registering Streamlit plugin."""

import os
import sys
import tempfile

from jaclang.cli.cmdreg import cmd_registry
from jaclang.plugin.default import hookimpl

import streamlit.web.bootstrap as bootstrap


class JacCmd:
    """Jac CLI."""

    @staticmethod
    @hookimpl
    def create_cmd() -> None:
        """Create Jac CLI cmds."""

        @cmd_registry.register
        def streamlit(filename: str) -> None:
            """Streamlit the specified .jac file.

            :param filename: The path to the .jac file.
            """
            if filename.endswith(".jac"):
                abs_path = os.path.abspath(filename)
                dirname, basename = os.path.split(abs_path)
                basename = basename.replace(".jac", "")
                assert (
                    basename not in sys.modules
                ), "Please use another name for the .jac file. It conflicts with a Python package."
                py_lines = [
                    "from jaclang import jac_import",
                    f"st_app = jac_import('{basename}', base_path='{dirname}')",
                    "st_app.main()",
                ]
                with tempfile.NamedTemporaryFile(mode="w", suffix=".py") as temp_file:
                    file_name = temp_file.name
                    temp_file.write("\n".join(py_lines))
                    bootstrap.run(file_name, is_hello=False, args=[], flag_options={})
            else:
                print("Not a .jac file.")
