"""Module for registering Streamlit plugin."""

import os

from jaclang.cli.cmdreg import cmd_registry
from jaclang.compiler.compile import jac_str_to_pass
from jaclang.compiler.constant import Constants as Con
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
                base, mod = os.path.split(filename)
                base = base if base else "./"
                mod = mod[:-4]
                if filename.endswith(".jac"):
                    with open(filename, "r") as f:
                        prog = jac_str_to_pass(f.read(), f"{mod}")
                py_code = prog.ir.gen.py
                lines = py_code.split("\n")
                lines.insert(1, "__jac_mod_bundle__=\"__jac_mod_bundle__\"\n")
                py_code = "\n".join(lines)
                strimlit_dir = os.path.join(base, Con.JAC_GEN_DIR)
                os.makedirs(strimlit_dir, exist_ok=True) if not os.path.exists(strimlit_dir) else None
                py_filename = os.path.join(strimlit_dir, f"{mod}.py")
                with open(py_filename, "w") as py_file:
                    py_file.write(py_code)
                bootstrap.run(py_filename, is_hello=True, args=[], flag_options=None)
            else:
                print("Not a .jac file.")
