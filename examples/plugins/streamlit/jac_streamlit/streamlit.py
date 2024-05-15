import os
import subprocess

from jaclang.cli.cmdreg import cmd_registry
from jaclang.plugin.default import hookimpl
from jaclang.compiler.compile import jac_str_to_pass


class JacCmd:
    """Jac CLI."""

    @staticmethod
    @hookimpl
    def create_cmd() -> None:
        """Creating Jac CLI cmds."""

        @cmd_registry.register
        def streamlit(filename: str) -> None:
            """Streamlit the specified .jac file.

            :param filename: The path to the .jac file.
            """
            if filename.endswith(".jac"):
                base, mod = os.path.split(filename)
                base = base if base else "./"
                mod = mod[:-4]
                if filename.endswith(".jac"):
                    with open(filename, "r") as f:
                        prog = jac_str_to_pass(f.read(), f"{mod}")
                py_code = prog.ir.gen.py
                py_filename = os.path.join(base, f"{mod}.py")
                with open(py_filename, "w") as py_file:
                    py_file.write(py_code)
                command = ["streamlit", "run", f"{py_filename}"]
                subprocess.run(command)
                print(f"Python code written to {py_filename}")
            else:
                print("Not a .jac file.")
