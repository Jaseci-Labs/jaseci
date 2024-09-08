import ast
import mypy.build as myb
import mypy.checkexpr as mycke
import mypy.errors as mye
import mypy.fastparse as myfp
from _typeshed import Incomplete
from jaclang.compiler.passes import Pass
from mypy.build import (
    BuildSource as BuildSource,
    BuildSourceSet as BuildSourceSet,
    FileSystemCache as FileSystemCache,
    Graph,
    compute_search_paths as compute_search_paths,
    load_plugins as load_plugins,
    process_graph as process_graph,
)
from mypy.options import Options as Options
from mypy.semanal_main import semantic_analysis_for_scc as semantic_analysis_for_scc

__all__ = [
    "BuildManager",
    "State",
    "BuildSource",
    "BuildSourceSet",
    "FileSystemCache",
    "compute_search_paths",
    "load_graph",
    "load_plugins",
    "process_graph",
    "Errors",
    "Options",
    "ASTConverter",
    "semantic_analysis_for_scc",
]

class BuildManager(myb.BuildManager):
    def parse_file(
        self,
        id: str,
        path: str,
        source: str,
        ignore_errors: bool,
        options: myb.Options,
        ast_override: myb.MypyFile | None = None,
    ) -> myb.MypyFile: ...

class ExpressionChecker(mycke.ExpressionChecker):
    def __init__(
        self,
        tc: mycke.mypy.checker.TypeChecker,
        msg: mycke.MessageBuilder,
        plugin: mycke.Plugin,
        per_line_checking_time_ns: dict[int, int],
    ) -> None: ...
    def visit_list_expr(self, e: mycke.ListExpr) -> mycke.Type: ...
    def visit_set_expr(self, e: mycke.SetExpr) -> mycke.Type: ...
    def visit_tuple_expr(self, e: myfp.TupleExpr) -> myb.Type: ...
    def visit_dict_expr(self, e: myfp.DictExpr) -> myb.Type: ...
    def visit_list_comprehension(self, e: myfp.ListComprehension) -> myb.Type: ...
    def visit_set_comprehension(self, e: myfp.SetComprehension) -> myb.Type: ...
    def visit_generator_expr(self, e: myfp.GeneratorExpr) -> myb.Type: ...
    def visit_dictionary_comprehension(
        self, e: myfp.DictionaryComprehension
    ) -> myb.Type: ...
    def visit_member_expr(
        self, e: myfp.MemberExpr, is_lvalue: bool = False
    ) -> myb.Type: ...

class State(myb.State):
    manager: BuildManager
    tree: myb.MypyFile | None
    order: Incomplete
    caller_state: Incomplete
    caller_line: Incomplete
    import_context: Incomplete
    id: Incomplete
    options: Incomplete
    early_errors: Incomplete
    ignore_all: bool
    path: Incomplete
    abspath: Incomplete
    xpath: Incomplete
    meta: Incomplete
    interface_hash: Incomplete
    meta_source_hash: Incomplete
    source: Incomplete
    per_line_checking_time_ns: Incomplete
    dependencies: Incomplete
    dependencies_set: Incomplete
    suppressed: Incomplete
    suppressed_set: Incomplete
    priorities: Incomplete
    dep_line_map: Incomplete
    def __init__(
        self,
        id: str | None,
        path: str | None,
        source: str | None,
        manager: BuildManager,
        caller_state: myb.State | None = None,
        caller_line: int = 0,
        ancestor_for: myb.State | None = None,
        root_source: bool = False,
        temporary: bool = False,
        ast_override: myb.MypyFile | None = None,
    ) -> None: ...
    def type_checker(self) -> myb.TypeChecker: ...
    source_hash: Incomplete
    def parse_file(
        self, *, temporary: bool = False, ast_override: myb.MypyFile | None = None
    ) -> None: ...

class ASTConverter(myfp.ASTConverter):
    def visit(self, node: ast.AST | None) -> myfp.Any: ...
    def make_argument(
        self,
        arg: ast.arg,
        default: ast.expr | None,
        kind: myfp.ArgKind,
        no_type_check: bool,
        pos_only: bool = False,
    ) -> myfp.Argument: ...
    def link_mypy_to_jac_node(self, node: ast.AST, ret: myfp.Any) -> None: ...

class Errors(mye.Errors):
    cur_pass: Incomplete
    def __init__(self, cur_pass: Pass, *args, **kwargs) -> None: ...
    def report(
        self,
        line: int,
        column: int | None,
        message: str,
        code: mye.ErrorCode | None = None,
        *,
        blocker: bool = False,
        severity: str = "error",
        file: str | None = None,
        only_once: bool = False,
        allow_dups: bool = False,
        origin_span: mye.Iterable[int] | None = None,
        offset: int = 0,
        end_line: int | None = None,
        end_column: int | None = None
    ) -> None: ...

def load_graph(
    sources: list[BuildSource],
    manager: BuildManager,
    old_graph: Graph | None = None,
    new_modules: list[State] | None = None,
) -> Graph: ...
