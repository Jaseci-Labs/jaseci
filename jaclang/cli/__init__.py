"""CLI for jaclang."""
from jaclang import jac_import

save_file = False

cli = jac_import("cli", save_file=save_file)
cmds = jac_import("cmds", save_file=save_file)

cli.cmd_registry = cmds.cmd_reg
