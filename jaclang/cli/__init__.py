"""CLI for jaclang."""
from jaclang import jac_import

try:
    from jaclang.cli.__jac_gen__ import cli
    from jaclang.cli.__jac_gen__ import cmds
except Exception:
    cli = jac_import("cli")
    cmds = jac_import("cmds")

cli.cmd_registry = cmds.cmd_reg  # type: ignore
