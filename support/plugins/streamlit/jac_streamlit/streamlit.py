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
                    "from jaclang.plugin.feature import JacFeature as Jac",
                    f"Jac.context().init_memory(base_path='{dirname}')",
                    f"(st_app,) = jac_import('{basename}', base_path='{dirname}')",
                    "if hasattr(st_app, 'main'):",
                    "    st_app.main()",
                    "else:",
                    "   print('No main function found. Please define a main function in your .jac file or put in a with entrypoint block.')",  # noqa: E501
                ]
                with tempfile.NamedTemporaryFile(
                    mode="w", suffix=".py", delete=False
                ) as temp_file:
                    file_name = temp_file.name
                    print(f"Temp file: {file_name}")
                    temp_file.write("\n".join(py_lines))
                bootstrap.run(file_name, is_hello=False, args=[], flag_options={})
            else:
                print("Not a .jac file.")

        @cmd_registry.register
        def dot_view(filename: str) -> None:
            """View the content of a DOT file. in Streamlit Application.

            :param filename: The path to the DOT file that wants to be shown.
            """
            from jaclang.cli.cli import dot

            dot(filename)
            _, filename = os.path.split(filename)
            dot_file = os.path.abspath(f"{filename.replace('.jac', '.dot')}")
            dot_streamlit_view_file = os.path.join(
                os.path.dirname(__file__), "dot_viewer.py"
            )
            bootstrap.run(
                dot_streamlit_view_file,
                is_hello=False,
                args=[dot_file],
                flag_options={},
            )
