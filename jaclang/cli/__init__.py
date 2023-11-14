"""CLI for jaclang."""
from jaclang import jac_import as jac_import


cli = jac_import("cli")
cmds = jac_import("cmds")

cli.cmd_registry = cmds.cmd_reg  # type: ignore
