"""CLI for jaclang."""
# from jaclang import jac_import


# cli = jac_import("cli")
# cmds = jac_import("cmds")
from . import cli
from . import cmds

cli.cmd_registry = cmds.cmd_reg  # type: ignore
