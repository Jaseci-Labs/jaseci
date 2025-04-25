"""Jaclang code runner for REPL/Jupyter Notebook kernel, etc."""

import ast as py_ast
import io
import logging
import marshal
from contextlib import redirect_stderr, redirect_stdout
from tempfile import NamedTemporaryFile
from typing import Any, Callable, Tuple

import jaclang.compiler.unitree as jac_ast
from jaclang import JacMachine
from jaclang.compiler.parser import JacParser
from jaclang.compiler.program import JacProgram
from jaclang.compiler.unitree import Module as JacModule
from jaclang.runtimelib.machinestate import JacMachineState
from jaclang.settings import settings
from jaclang.utils.helpers import dump_traceback


class JacRunner:
    """Jaclang runner that preserve sessions across runs."""

    def __init__(self) -> None:
        """Initialize JacRunner object."""
        self.program = JacProgram()
        self.machine_state = JacMachineState()
        self.session: dict[str, Any] = {
            settings.pyout_jaclib_alias: JacMachine,
        }
        self.stdout = ""
        self.stderr = ""
        self.unexpected_eof = False
        self.notebook_repr_fn = None

    def add_stderr(self, msg: str) -> None:
        """Add message to stderr."""
        self.stderr += msg

    def compile(self, source: str) -> JacModule | None:
        """Compile Jac code to jac module."""
        # I had to do this cause the str_to_pass interface requires.
        # This must fixed from the jac compiler itself.
        tmpfile = NamedTemporaryFile(suffix=".jac")
        self.unexpected_eof = False
        ret = self._redirect_exec(self.program.compile_from_str, (source, tmpfile.name))

        had_syntax_error = False
        if isinstance(ret, JacParser):
            self.unexpected_eof = ret.unexpected_eof
            had_syntax_error = len(ret.errors_had) != 0

        # Since the jac_str_to_pass doesn't report error we need to handle here.
        if had_syntax_error:
            for alrt in ret.errors_had:
                self.stderr += alrt.pretty_print()
            return None

        return ret

    def execute(self, mod: JacModule) -> None:
        """Execute Jac code."""
        try:
            self._execute(mod)
        except Exception as e:
            self.add_stderr(dump_traceback(e))

    def _execute(self, mod: JacModule) -> None:
        assert isinstance(mod.body[0], jac_ast.ModuleCode)

        with_entry = mod.body[0]
        statements = with_entry.body.items

        # FIXME: Move hardcoded string to settings.
        locals()["__jac_mach__"] = self.machine_state

        # If not statements, return.
        if len(statements) == 0:
            return

        # If it's a single expression statement, just __repr__ or visualize it.
        if len(statements) == 1 and isinstance(statements[0], jac_ast.ExprStmt):
            try:
                expr = statements[0]
                py_code = py_ast.unparse(expr.gen.py_ast[0])
                val = self._redirect_exec(eval, (py_code, self.session, None))
                if (val is not None) and not (
                    self.notebook_repr_fn and self.notebook_repr_fn(val)
                ):
                    self.stdout += repr(val) + "\n"
            except Exception as e:
                self.stderr += str(e)

        # Execute the bytecode.
        else:
            bytecode = marshal.loads(mod.gen.py_bytecode)  # type: ignore
            self._redirect_exec(exec, (bytecode, self.session, None))

    # --------------------------------------------------------------------------
    # Internal methods.
    # --------------------------------------------------------------------------

    def _redirect_exec(self, fn: Callable, args: Tuple) -> Any:  # noqa: ANN401
        ret = None
        self.stdout, self.stderr = "", ""
        with io.StringIO() as out_buf, io.StringIO() as err_buf, redirect_stdout(
            out_buf
        ), redirect_stderr(err_buf):
            ret = fn(*args)
            self.stdout = out_buf.getvalue()
            self.stderr = err_buf.getvalue()
        return ret


class REPL:
    """Simple REPL for Jaclang."""

    VERSION = "jaclang v1.0.0"
    COPYRIGHT = "Copyright (c) 2025 Jaseci Labs, LLC."

    def __init__(self) -> None:
        """Initialize REPL."""
        self.runner = JacRunner()
        self.code = ""
        self.print = print
        self.input = input
        self.should_exit = False
        self.exit_code = 0

        def _exit(code:int = 0) -> None:
            self.should_exit = True
            self.exit_code = code
        self.runner.session["exit"] = _exit

        logging.disable()

    def run(self) -> int:
        """Run the REPL."""
        self._print_info()

        while not self.should_exit:
            mod: JacModule | None = None
            try:  # noqa: SIM105
                self.code += self.input(">>> " if not self.runner.unexpected_eof else "... ")
                mod = self._try_compiling()
                if mod is None and (
                    self.runner.unexpected_eof or self._check_need_more_inputs()
                ):
                    continue
            except Exception:
                pass

            self.code = ""
            if mod is None:
                self._dump_outputs()
                continue

            try:  # noqa: SIM105
                self.runner.execute(mod)
            except Exception:
                pass
            self._dump_outputs()

        return self.exit_code

    def _try_compiling(self) -> JacModule | None:
        return self.runner.compile(f"with entry {{\n\t{self.code};\n}}")

    def _check_need_more_inputs(self) -> bool:
        self.runner.compile(f"with entry {{\n\t{self.code}")
        return self.runner.unexpected_eof

    def _dump_outputs(self) -> None:
        ansi_reset = "\033[0m"
        ansi_red = "\033[31m"
        if self.runner.stdout:
            self.print(self.runner.stdout, end="", flush=True)
        if self.runner.stderr:
            self.print(f"{ansi_red}{self.runner.stderr}{ansi_reset}", end="\n", flush=True)

    def _print_info(self) -> None:
        """Print REPL info."""
        ansi_orange = "\033[38;5;214m"
        ansi_reset = "\033[0m"
        logo = r"""
    ___
   |\  \     $1
   \ \  \
 __ \ \  \   $2
|\  \\_\  \  $3
\ \________\
 \|________|
"""
        logo = logo.replace(
            "$1", f"{ansi_reset}Jaclang: Imagine, Create, Launch{ansi_orange}"
        )
        logo = logo.replace("$2", f"{ansi_reset}{REPL.COPYRIGHT}{ansi_orange}")
        logo = logo.replace("$3", f"{ansi_reset}{REPL.VERSION}{ansi_orange}")
        self.print(f"{ansi_orange}{logo}{ansi_reset}")
