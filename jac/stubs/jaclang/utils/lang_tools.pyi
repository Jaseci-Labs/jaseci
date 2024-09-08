import jaclang.compiler.absyntree as ast
from _typeshed import Incomplete
from jaclang.compiler.compile import jac_file_to_pass as jac_file_to_pass
from jaclang.compiler.passes.main.pyast_load_pass import (
    PyastBuildPass as PyastBuildPass,
)
from jaclang.compiler.passes.main.schedules import (
    py_code_gen as py_code_gen,
    py_code_gen_typed as py_code_gen_typed,
    type_checker_sched as type_checker_sched,
)
from jaclang.compiler.symtable import SymbolTable as SymbolTable
from jaclang.utils.helpers import (
    auto_generate_refs as auto_generate_refs,
    pascal_to_snake as pascal_to_snake,
)

class AstKidInfo:
    name: Incomplete
    typ: Incomplete
    default: Incomplete
    def __init__(self, name: str, typ: str, default: str | None = None) -> None: ...

class AstNodeInfo:
    type_map: dict[str, type]
    cls: Incomplete
    def __init__(self, cls: type) -> None: ...
    name: Incomplete
    doc: Incomplete
    class_name_snake: Incomplete
    init_sig: Incomplete
    kids: Incomplete
    def process(self, cls: type[ast.AstNode]) -> None: ...

class AstTool:
    ast_classes: Incomplete
    def __init__(self) -> None: ...
    def pass_template(self) -> str: ...
    def py_ast_nodes(self) -> str: ...
    def md_doc(self) -> str: ...
    def ir(self, args: list[str]) -> str: ...
    def automate_ref(self) -> str: ...
    def gen_parser(self) -> str: ...
