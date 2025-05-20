"""Jaclang code runner for REPL/Jupyter Notebook kernel, etc."""

import ast as py_ast
import io
import marshal
from contextlib import redirect_stderr, redirect_stdout
from tempfile import NamedTemporaryFile
from typing import Any, Callable, Tuple

import jaclang.compiler.absyntree as jac_ast
from jaclang import JacMachine
from jaclang.compiler.absyntree import Module as JacModule
from jaclang.compiler.parser import JacParser
from jaclang.compiler.program import JacProgram
from jaclang.runtimelib.machinestate import JacMachineState
from jaclang.settings import settings


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
        self.notebook_repr_fn = None

    def add_stderr(self, msg: str) -> None:
        """Add message to stderr."""
        self.stderr += msg

    def compile(self, source: str) -> JacModule | None:
        """Compile Jac code to jac module."""
        # I had to do this cause the str_to_pass interface requires.
        # This must fixed from the jac compiler itself.
        tmpfile = NamedTemporaryFile(suffix=".jac")
        ret = self._redirect_exec(self.program.jac_str_to_pass, (source, tmpfile.name))

        # Since the jac_str_to_pass doesn't report error we need to handle here.
        had_syntax_error = isinstance(ret, JacParser) and len(ret.errors_had) != 0
        if had_syntax_error or not isinstance(ret.ir_out, JacModule):
            for alrt in ret.errors_had:
                self.stderr += alrt.pretty_print()
            return None

        return ret.ir_out

    def execute(self, mod: JacModule) -> None:
        """Execute Jac code."""
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
                val = self._redirect_exec(eval, (py_code, None, self.session))
                if (val is not None) and not (
                    self.notebook_repr_fn and self.notebook_repr_fn(val)
                ):
                    self.stdout += val.__repr__()
            except Exception as e:
                self.stderr += str(e)

        # Execute the bytecode.
        else:
            bytecode = marshal.loads(mod.gen.py_bytecode)
            self._redirect_exec(exec, (bytecode, None, self.session))

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
