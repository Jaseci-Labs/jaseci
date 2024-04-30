"""Overrides to mypy build manager for direct AST pass through."""

from __future__ import annotations

import ast
import os
import pathlib

import jaclang
from jaclang.compiler.absyntree import AstNode
from jaclang.compiler.passes import Pass
from jaclang.compiler.passes.main.fuse_typeinfo_pass import (
    FuseTypeInfoPass,
)  # TODO: Put in better place

import mypy.build as myb
import mypy.checkexpr as mycke
import mypy.errors as mye
import mypy.fastparse as myfp
from mypy.build import BuildSource
from mypy.build import BuildSourceSet
from mypy.build import FileSystemCache
from mypy.build import Graph
from mypy.build import ModuleNotFound
from mypy.build import PRI_INDIRECT
from mypy.build import compute_search_paths
from mypy.build import find_module_simple
from mypy.build import load_plugins
from mypy.build import process_graph
from mypy.options import Options
from mypy.semanal_main import semantic_analysis_for_scc


os.environ["MYPYPATH"] = str(
    pathlib.Path(os.path.dirname(jaclang.__file__)).parent / "stubs"
)


mypy_to_jac_node_map: dict[
    tuple[int, int | None, int | None, int | None], list[AstNode]
] = {}


class BuildManager(myb.BuildManager):
    """Overrides to mypy build manager for direct AST pass through."""

    def parse_file(
        self,
        id: str,
        path: str,
        source: str,
        ignore_errors: bool,
        options: myb.Options,
        ast_override: myb.MypyFile | None = None,
    ) -> myb.MypyFile:
        """Parse the source of a file with the given name.

        Raise CompileError if there is a parse error.
        """
        t0 = myb.time.time()
        if ignore_errors:
            self.errors.ignored_files.add(path)
        tree = (
            ast_override
            if ast_override
            else myb.parse(source, path, id, self.errors, options=options)
        )
        tree._fullname = id
        self.add_stats(
            files_parsed=1,
            modules_parsed=int(not tree.is_stub),
            stubs_parsed=int(tree.is_stub),
            parse_time=myb.time.time() - t0,
        )

        if self.errors.is_blockers():
            self.log("Bailing due to parse errors")
            self.errors.raise_error()

        self.errors.set_file_ignored_lines(path, tree.ignored_lines, ignore_errors)
        return tree


class ExpressionChecker(mycke.ExpressionChecker):
    """Overrides to mypy expression checker for direct AST pass through."""

    def __init__(
        self,
        tc: mycke.mypy.checker.TypeChecker,
        msg: mycke.MessageBuilder,
        plugin: mycke.Plugin,
        per_line_checking_time_ns: dict[int, int],
    ) -> None:
        """Override to mypy expression checker for direct AST pass through."""
        super().__init__(tc, msg, plugin, per_line_checking_time_ns)

    def visit_list_expr(self, e: mycke.ListExpr) -> mycke.Type:
        """Type check a list expression [...]."""
        out = super().visit_list_expr(e)
        FuseTypeInfoPass.node_type_hash[e] = out
        return out

    def visit_set_expr(self, e: mycke.SetExpr) -> mycke.Type:
        """Type check a set expression {...}."""
        out = super().visit_set_expr(e)
        FuseTypeInfoPass.node_type_hash[e] = out
        return out

    def visit_tuple_expr(self, e: myfp.TupleExpr) -> myb.Type:
        """Type check a tuple expression (...)."""
        out = super().visit_tuple_expr(e)
        FuseTypeInfoPass.node_type_hash[e] = out
        return out

    def visit_dict_expr(self, e: myfp.DictExpr) -> myb.Type:
        """Type check a dictionary expression {...}."""
        out = super().visit_dict_expr(e)
        FuseTypeInfoPass.node_type_hash[e] = out
        return out

    def visit_list_comprehension(self, e: myfp.ListComprehension) -> myb.Type:
        """Type check a list comprehension."""
        out = super().visit_list_comprehension(e)
        FuseTypeInfoPass.node_type_hash[e] = out
        return out

    def visit_set_comprehension(self, e: myfp.SetComprehension) -> myb.Type:
        """Type check a set comprehension."""
        out = super().visit_set_comprehension(e)
        FuseTypeInfoPass.node_type_hash[e] = out
        return out

    def visit_generator_expr(self, e: myfp.GeneratorExpr) -> myb.Type:
        """Type check a generator expression."""
        out = super().visit_generator_expr(e)
        FuseTypeInfoPass.node_type_hash[e] = out
        return out

    def visit_dictionary_comprehension(
        self, e: myfp.DictionaryComprehension
    ) -> myb.Type:
        """Type check a dict comprehension."""
        out = super().visit_dictionary_comprehension(e)
        FuseTypeInfoPass.node_type_hash[e] = out
        return out


class State(myb.State):
    """Overrides to mypy state for direct AST pass through."""

    manager: BuildManager
    tree: myb.MypyFile | None = None

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
        # If `temporary` is True, this State is being created to just
        # quickly parse/load the tree, without an intention to further
        # process it. With this flag, any changes to external state as well
        # as error reporting should be avoided.
        temporary: bool = False,
        ast_override: myb.MypyFile | None = None,
    ) -> None:
        """Override to mypy state for AST pass through."""
        if not temporary:
            assert id or path or source is not None, "Neither id, path nor source given"
        self.manager = manager
        State.order_counter += 1
        self.order = State.order_counter
        self.caller_state = caller_state
        self.caller_line = caller_line
        if caller_state:
            self.import_context = caller_state.import_context.copy()
            self.import_context.append((caller_state.xpath, caller_line))
        else:
            self.import_context = []
        self.id = id or "__main__"
        self.options = manager.options.clone_for_module(self.id)
        self.early_errors: list[myb.ErrorInfo] = []
        self._type_checker = None
        if not path and source is None:
            assert id is not None
            try:
                path, follow_imports = myb.find_module_and_diagnose(
                    manager,
                    id,
                    self.options,
                    caller_state,
                    caller_line,
                    ancestor_for,
                    root_source,
                    skip_diagnose=temporary,
                )
            except myb.ModuleNotFound:
                if not temporary:
                    manager.missing_modules.add(id)
                raise
            if follow_imports == "silent":
                self.ignore_all = True
        elif path and myb.is_silent_import_module(manager, path) and not root_source:
            self.ignore_all = True
        self.path = path
        if path:
            self.abspath = myb.os.path.abspath(path)
        self.xpath = path or "<string>"
        if path and source is None and self.manager.cache_enabled:
            self.meta = myb.find_cache_meta(self.id, path, manager)
            # TODO: Get mtime if not cached.
            if self.meta is not None:
                self.interface_hash = self.meta.interface_hash
                self.meta_source_hash = self.meta.hash
        if path and source is None and self.manager.fscache.isdir(path):
            source = ""
        self.source = source
        self.add_ancestors()
        self.per_line_checking_time_ns = myb.collections.defaultdict(int)
        t0 = myb.time.time()
        self.meta = myb.validate_meta(
            self.meta, self.id, self.path, self.ignore_all, manager
        )
        self.manager.add_stats(validate_meta_time=myb.time.time() - t0)
        if self.meta:
            # Make copies, since we may modify these and want to
            # compare them to the originals later.
            self.dependencies = list(self.meta.dependencies)
            self.dependencies_set = set(self.dependencies)
            self.suppressed = list(self.meta.suppressed)
            self.suppressed_set = set(self.suppressed)
            all_deps = self.dependencies + self.suppressed
            assert len(all_deps) == len(self.meta.dep_prios)
            self.priorities = dict(zip(all_deps, self.meta.dep_prios))

            assert len(all_deps) == len(self.meta.dep_lines)
            self.dep_line_map = dict(zip(all_deps, self.meta.dep_lines))
            if temporary:
                self.load_tree(temporary=True)
            if not manager.use_fine_grained_cache() and myb.exist_added_packages(
                self.suppressed, manager, self.options
            ):
                # Special case: if there were a previously missing package imported here
                # and it is not present, then we need to re-calculate dependencies.
                # This is to support patterns like this:
                #     from missing_package import missing_module  # type: ignore
                # At first mypy doesn't know that `missing_module` is a module
                # (it may be a variable, a class, or a function), so it is not added to
                # suppressed dependencies. Therefore, when the package with module is added,
                # we need to re-calculate dependencies.
                # NOTE: see comment below for why we skip this in fine grained mode.
                self.parse_file(
                    ast_override=ast_override
                )  # This is safe because the cache is anyway stale.
                self.compute_dependencies()
        else:
            # When doing a fine-grained cache load, pretend we only
            # know about modules that have cache information and defer
            # handling new modules until the fine-grained update.
            if manager.use_fine_grained_cache():
                manager.log(f"Deferring module to fine-grained update {path} ({id})")
                raise myb.ModuleNotFound

            # Parse the file (and then some) to get the dependencies.
            self.parse_file(temporary=temporary, ast_override=ast_override)
            self.compute_dependencies()

    def type_checker(self) -> myb.TypeChecker:
        """Return the type checker for this state."""
        if not self._type_checker:
            assert (
                self.tree is not None
            ), "Internal error: must be called on parsed file only"
            manager = self.manager
            self._type_checker = myb.TypeChecker(
                manager.errors,
                manager.modules,
                self.options,
                self.tree,
                self.xpath,
                manager.plugin,
                self.per_line_checking_time_ns,
            )
            self._type_checker.expr_checker = ExpressionChecker(
                self._type_checker,
                self._type_checker.msg,
                self._type_checker.plugin,
                self.per_line_checking_time_ns,
            )

        return self._type_checker

    def parse_file(
        self, *, temporary: bool = False, ast_override: myb.MypyFile | None = None
    ) -> None:
        """Parse file and run first pass of semantic analysis.

        Everything done here is local to the file. Don't depend on imported
        modules in any way. Also record module dependencies based on imports.
        """
        if self.tree is not None:
            # The file was already parsed (in __init__()).
            return

        manager = self.manager

        # Can we reuse a previously parsed AST? This avoids redundant work in daemon.
        cached = self.id in manager.ast_cache
        modules = manager.modules
        if not cached:
            manager.log(f"Parsing {self.xpath} ({self.id})")
        else:
            manager.log(f"Using cached AST for {self.xpath} ({self.id})")

        t0 = myb.time_ref()

        with self.wrap_context():
            source = self.source
            self.source = None  # We won't need it again.
            if self.path and source is None:
                try:
                    path = manager.maybe_swap_for_shadow_path(self.path)
                    source = myb.decode_python_encoding(manager.fscache.read(path))
                    self.source_hash = manager.fscache.hash_digest(path)
                except OSError as ioerr:
                    # ioerr.strerror differs for os.stat failures between Windows and
                    # other systems, but os.strerror(ioerr.errno) does not, so we use that.
                    # (We want the error messages to be platform-independent so that the
                    # tests have predictable output.)
                    raise myb.CompileError(
                        [
                            "mypy: can't read file '{}': {}".format(
                                self.path, myb.os.strerror(ioerr.errno)
                            )
                        ],
                        module_with_blocker=self.id,
                    ) from ioerr
                except (UnicodeDecodeError, myb.DecodeError) as decodeerr:
                    if self.path.endswith(".pyd"):
                        err = (
                            f"mypy: stubgen does not support .pyd files: '{self.path}'"
                        )
                    else:
                        err = f"mypy: can't decode file '{self.path}': {str(decodeerr)}"
                    raise myb.CompileError(
                        [err], module_with_blocker=self.id
                    ) from decodeerr
            elif self.path and self.manager.fscache.isdir(self.path):
                source = ""
                self.source_hash = ""
            else:
                assert source is not None
                self.source_hash = myb.compute_hash(source)

            self.parse_inline_configuration(source)
            if not cached:
                self.tree = manager.parse_file(
                    self.id,
                    self.xpath,
                    source,
                    self.ignore_all or self.options.ignore_errors,
                    self.options,
                    ast_override=ast_override,
                )

            else:
                # Reuse a cached AST
                self.tree = manager.ast_cache[self.id][0]
                manager.errors.set_file_ignored_lines(
                    self.xpath,
                    self.tree.ignored_lines,
                    self.ignore_all or self.options.ignore_errors,
                )

        self.time_spent_us += myb.time_spent_us(t0)

        if not cached:
            # Make a copy of any errors produced during parse time so that
            # fine-grained mode can repeat them when the module is
            # reprocessed.
            self.early_errors = list(manager.errors.error_info_map.get(self.xpath, []))
        else:
            self.early_errors = manager.ast_cache[self.id][1]

        if not temporary:
            modules[self.id] = self.tree

        if not cached:
            self.semantic_analysis_pass1()

        if not temporary:
            self.check_blockers()

        manager.ast_cache[self.id] = (self.tree, self.early_errors)


class ASTConverter(myfp.ASTConverter):
    """Overrides to mypy AST converter for direct AST pass through."""

    def visit(self, node: ast.AST | None) -> myfp.Any:  # noqa: ANN401
        """Override to mypy AST converter for direct AST pass through."""
        ret = super().visit(node)
        if node and ret:
            self.link_mypy_to_jac_node(node, ret)
        return ret

    def make_argument(
        self,
        arg: ast.arg,
        default: ast.expr | None,
        kind: myfp.ArgKind,
        no_type_check: bool,
        pos_only: bool = False,
    ) -> myfp.Argument:
        """Override to mypy AST converter for direct AST pass through."""
        ret = super().make_argument(arg, default, kind, no_type_check, pos_only)
        self.link_mypy_to_jac_node(arg, ret)
        return ret

    def link_mypy_to_jac_node(
        self, node: ast.AST, ret: myfp.Any  # noqa: ANN401
    ) -> None:
        """Link mypy AST node to Jac AST node."""
        if hasattr(node, "jac_link"):
            for i in range(len(node.jac_link)):
                node.jac_link[i].gen.mypy_ast.append(ret)
            mypy_to_jac_node_map[
                (ret.line, ret.column, ret.end_line, ret.end_column)
            ] = node.jac_link
        # else:
        #     raise Exception("AST node not linked to Jac node")


class Errors(mye.Errors):
    """Overrides to mypy errors for direct AST pass through."""

    def __init__(self, cur_pass: Pass, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """Override to mypy errors for direct AST pass through."""
        self.cur_pass = cur_pass
        super().__init__(*args, **kwargs)

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
        end_column: int | None = None,
    ) -> None:
        """Override to mypy errors for direct AST pass through."""
        super().report(
            line,
            column,
            message,
            code=code,
            blocker=blocker,
            severity=severity,
            file=file,
            only_once=only_once,
            allow_dups=allow_dups,
            origin_span=origin_span,
            offset=offset,
            end_line=end_line,
            end_column=end_column,
        )
        if (line, column, end_line, end_column) in mypy_to_jac_node_map:
            self.cur_pass.warning(
                msg=message,
                node_override=mypy_to_jac_node_map[
                    (line, column, end_line, end_column)
                ][0],
            )


def load_graph(
    sources: list[BuildSource],
    manager: BuildManager,
    old_graph: Graph | None = None,
    new_modules: list[State] | None = None,
) -> Graph:
    """Given some source files, load the full dependency graph.

    If an old_graph is passed in, it is used as the starting point and
    modified during graph loading.

    If a new_modules is passed in, any modules that are loaded are
    added to the list. This is an argument and not a return value
    so that the caller can access it even if load_graph fails.

    As this may need to parse files, this can raise CompileError in case
    there are syntax errors.
    """
    graph: Graph = old_graph if old_graph is not None else {}

    # The deque is used to implement breadth-first traversal.
    # TODO: Consider whether to go depth-first instead.  This may
    # affect the order in which we process files within import cycles.
    new = new_modules if new_modules is not None else []
    entry_points: set[str] = set()
    # Seed the graph with the initial root sources.
    for bs in sources:
        try:
            st = State(
                id=bs.module,
                path=bs.path,
                source=bs.text,
                manager=manager,
                root_source=not bs.followed,
            )
        except ModuleNotFound:
            continue
        if st.id in graph:
            manager.errors.set_file(st.xpath, st.id, manager.options)
            manager.errors.report(
                -1,
                -1,
                f'Duplicate module named "{st.id}" (also at "{graph[st.id].xpath}")',
                blocker=True,
            )
            manager.errors.report(
                -1,
                -1,
                "See https://mypy.readthedocs.io/en/stable/running_mypy.html#mapping-file-paths-to-modules "
                "for more info",
                severity="note",
            )
            manager.errors.report(
                -1,
                -1,
                "Common resolutions include: a) using `--exclude` to avoid checking one of them, "
                "b) adding `__init__.py` somewhere, c) using `--explicit-package-bases` or "
                "adjusting MYPYPATH",
                severity="note",
            )

            manager.errors.raise_error()
        graph[st.id] = st
        new.append(st)
        entry_points.add(bs.module)

    # Note: Running this each time could be slow in the daemon. If it's a problem, we
    # can do more work to maintain this incrementally.
    seen_files = {st.abspath: st for st in graph.values() if st.path}

    # Collect dependencies.  We go breadth-first.
    # More nodes might get added to new as we go, but that's fine.
    for st in new:
        assert st.ancestors is not None
        # Strip out indirect dependencies.  These will be dealt with
        # when they show up as direct dependencies, and there's a
        # scenario where they hurt:
        # - Suppose A imports B and B imports C.
        # - Suppose on the next round:
        #   - C is deleted;
        #   - B is updated to remove the dependency on C;
        #   - A is unchanged.
        # - In this case A's cached *direct* dependencies are still valid
        #   (since direct dependencies reflect the imports found in the source)
        #   but A's cached *indirect* dependency on C is wrong.
        dependencies = [
            dep
            for dep in st.dependencies
            if st.priorities.get(dep) != PRI_INDIRECT and "jaclang.vendor" not in dep
        ]
        if not manager.use_fine_grained_cache():
            # TODO: Ideally we could skip here modules that appeared in st.suppressed
            # because they are not in build with `follow-imports=skip`.
            # This way we could avoid overhead of cloning options in `State.__init__()`
            # below to get the option value. This is quite minor performance loss however.
            added = [dep for dep in st.suppressed if find_module_simple(dep, manager)]
        else:
            # During initial loading we don't care about newly added modules,
            # they will be taken care of during fine grained update. See also
            # comment about this in `State.__init__()`.
            added = []
        for dep in st.ancestors + dependencies + st.suppressed:
            ignored = dep in st.suppressed_set and dep not in entry_points
            if ignored and dep not in added:
                manager.missing_modules.add(dep)
            elif dep not in graph:
                try:
                    if dep in st.ancestors:
                        # TODO: Why not 'if dep not in st.dependencies' ?
                        # Ancestors don't have import context.
                        newst = State(
                            id=dep,
                            path=None,
                            source=None,
                            manager=manager,
                            ancestor_for=st,
                        )
                    else:
                        newst = State(
                            id=dep,
                            path=None,
                            source=None,
                            manager=manager,
                            caller_state=st,
                            caller_line=st.dep_line_map.get(dep, 1),
                        )
                except ModuleNotFound:
                    if dep in st.dependencies_set:
                        st.suppress_dependency(dep)
                else:
                    if newst.path:
                        newst_path = os.path.abspath(newst.path)

                        if newst_path in seen_files:
                            manager.errors.report(
                                -1,
                                0,
                                "Source file found twice under different module names: "
                                '"{}" and "{}"'.format(
                                    seen_files[newst_path].id, newst.id
                                ),
                                blocker=True,
                            )
                            manager.errors.report(
                                -1,
                                0,
                                "See https://mypy.readthedocs.io/en/stable/running"
                                + "_mypy.html#mapping-file-paths-to-modules "
                                "for more info",
                                severity="note",
                            )
                            manager.errors.report(
                                -1,
                                0,
                                "Common resolutions include: a) adding `__init__.py` somewhere, "
                                "b) using `--explicit-package-bases` or adjusting MYPYPATH",
                                severity="note",
                            )
                            manager.errors.raise_error()

                        seen_files[newst_path] = newst

                    assert newst.id not in graph, newst.id
                    graph[newst.id] = newst
                    new.append(newst)  # noqa: B038
            if dep in graph and dep in st.suppressed_set:
                # Previously suppressed file is now visible
                st.add_dependency(dep)
    manager.plugin.set_modules(manager.modules)
    return graph


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
