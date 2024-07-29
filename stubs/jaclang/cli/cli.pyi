from jaclang import jac_import as jac_import
from jaclang.cli.cmdreg import (
    CommandShell as CommandShell,
    cmd_registry as cmd_registry,
)
from jaclang.compiler.compile import jac_file_to_pass as jac_file_to_pass
from jaclang.compiler.constant import Constants as Constants
from jaclang.compiler.passes.main.pyast_load_pass import (
    PyastBuildPass as PyastBuildPass,
)
from jaclang.compiler.passes.main.schedules import (
    py_code_gen_typed as py_code_gen_typed,
)
from jaclang.compiler.passes.tool.schedules import format_pass as format_pass
from jaclang.plugin.builtin import dotgen as dotgen
from jaclang.runtimelib.constructs import Architype as Architype
from jaclang.utils.lang_tools import AstTool as AstTool

def format(path: str, outfile: str = "", debug: bool = False) -> None: ...
def run(
    filename: str,
    session: str = "",
    main: bool = True,
    cache: bool = True,
    walker: str = "",
    node: str = "",
) -> None: ...
def get_object(id: str, session: str = "") -> dict: ...
def build(filename: str) -> None: ...
def check(filename: str, print_errs: bool = True) -> None: ...
def lsp() -> None: ...
def enter(filename: str, entrypoint: str, args: list) -> None: ...
def test(
    filepath: str,
    filter: str = "",
    xit: bool = False,
    maxfail: int = None,
    directory: str = "",
    verbose: bool = False,
) -> None: ...
def tool(tool: str, args: list | None = None) -> None: ...
def clean() -> None: ...
def debug(filename: str, main: bool = True, cache: bool = False) -> None: ...
def dot(
    filename: str,
    session: str = "",
    initial: str = "",
    depth: int = -1,
    traverse: bool = False,
    connection: list[str] = [],
    bfs: bool = False,
    edge_limit: int = 512,
    node_limit: int = 512,
    saveto: str = "",
) -> None: ...
def py2jac(filename: str) -> None: ...
def jac2py(filename: str) -> None: ...
def start_cli() -> None: ...
