"""CLI for jaclang."""
from jaclang import jac_import

cli = jac_import("jac_cli", save_file=True)
build = jac_import("build", save_file=True)

cli.run()
