"""Module for registering CLI plugins for jaseci."""

import os
import pickle

from jaclang import jac_import
from jaclang.cli.cmdreg import cmd_registry
from jaclang.plugin.default import hookimpl
from jaclang.runtimelib.context import ExecutionContext
from jaclang.runtimelib.machine import JacMachine, JacProgram


class JacCmd:
    """Jac CLI."""

    @staticmethod
    @hookimpl
    def create_cmd() -> None:
        """Create Jac CLI cmds."""

        @cmd_registry.register
        def serve(filename: str, host: str = "0.0.0.0", port: int = 8000) -> None:
            from jac_cloud import FastAPI

            """Serve the jac application."""
            base, mod = os.path.split(filename)
            base = base if base else "./"
            mod = mod[:-4]

            FastAPI.enable()
            jctx = ExecutionContext.create()

            if filename.endswith(".jac"):
                jac_import(
                    target=mod,
                    base_path=base,
                    cachable=True,
                    override_name="__main__",
                )
            elif filename.endswith(".jir"):
                with open(filename, "rb") as f:
                    JacMachine(base).attach_program(
                        JacProgram(mod_bundle=pickle.load(f), bytecode=None)
                    )
                    jac_import(
                        target=mod,
                        base_path=base,
                        cachable=True,
                        override_name="__main__",
                    )
            else:
                jctx.close()
                JacMachine.detach()
                raise ValueError("Not a valid file!\nOnly supports `.jac` and `.jir`")

            FastAPI.start(host=host, port=port)

            jctx.close()
            JacMachine.detach()
