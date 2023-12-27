"""Overrides to mypy build manager for direct AST pass through."""
from __future__ import annotations

import ast

import jaclang.vendor.mypy.build as myb
import jaclang.vendor.mypy.errors as mye
import jaclang.vendor.mypy.fastparse as myfp
from jaclang.compiler.absyntree import AstNode
from jaclang.compiler.passes import Pass
from jaclang.vendor.mypy.build import BuildSource
from jaclang.vendor.mypy.build import BuildSourceSet
from jaclang.vendor.mypy.build import FileSystemCache
from jaclang.vendor.mypy.build import compute_search_paths
from jaclang.vendor.mypy.build import load_graph
from jaclang.vendor.mypy.build import load_plugins
from jaclang.vendor.mypy.build import process_graph
from jaclang.vendor.mypy.options import Options
from jaclang.vendor.mypy.semanal_main import semantic_analysis_for_scc


mypy_to_jac_node_map: dict[tuple[int, int | None, int | None, int | None], AstNode] = {}


class BuildManager(myb.BuildManager):
    """Overrides to mypy build manager for direct AST pass through."""

    def parse_file(
        self,
        id: str,
        path: str,
        source: str,
        ignore_errors: bool,
        options: myb.Options,
        ast_override: ast.AST | None = None,
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
        ast_override: ast.AST | None = None,
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

    def parse_file(
        self, *, temporary: bool = False, ast_override: ast.AST | None = None
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
        if node is None:
            return None
        typeobj = type(node)
        visitor = self.visitor_cache.get(typeobj)
        if visitor is None:
            method = "visit_" + node.__class__.__name__
            visitor = getattr(self, method)
            self.visitor_cache[typeobj] = visitor
        ret = visitor(node)
        if hasattr(node, "jac_link"):
            node.jac_link.gen.mypy_ast.append(ret)
            mypy_to_jac_node_map[
                (ret.line, ret.column, ret.end_line, ret.end_column)
            ] = node.jac_link
        else:
            raise Exception("AST node not linked to Jac node")
        return ret


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
                ],
            )


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
