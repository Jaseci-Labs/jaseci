"""CLI for jaclang."""
from jaclang import jac_import

save_file = False

cli = jac_import("cli", save_file=save_file)
build = jac_import("build", save_file=save_file)

cli.command_registry = build.command_registry
