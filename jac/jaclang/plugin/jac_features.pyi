"""Jac Language Features."""

from __future__ import annotations

from typing import ClassVar, TypeAlias

class JacAccessValidation:
    """Jac Access Validation Specs."""

    @staticmethod
    def elevate_root():
        """Elevate context root to system_root."""
        ...

    @staticmethod
    def allow_root(
        architype,
        root_id,
        level,
    ):
        """Allow all access from target root graph to current Architype."""
        ...

    @staticmethod
    def disallow_root(
        architype,
        root_id,
        level,
    ):
        """Disallow all access from target root graph to current Architype."""
        ...

    @staticmethod
    def unrestrict(architype, level):
        """Allow everyone to access current Architype."""
        ...

    @staticmethod
    def restrict(architype):
        """Disallow others to access current Architype."""
        ...

    @staticmethod
    def check_read_access(to):
        """Read Access Validation."""
        ...

    @staticmethod
    def check_connect_access(to):
        """Write Access Validation."""
        ...

    @staticmethod
    def check_write_access(to):
        """Write Access Validation."""
        ...

    @staticmethod
    def check_access_level(to):
        """Access validation."""
        ...

class JacNode:
    """Jac Node Operations."""

    @staticmethod
    def node_dot(node, dot_file):
        """Generate Dot file for visualizing nodes and edges."""
        ...

    @staticmethod
    def get_edges(
        node,
        dir,
        filter_func,
        target_obj,
    ):
        """Get edges connected to this node."""
        ...

    @staticmethod
    def edges_to_nodes(
        node,
        dir,
        filter_func,
        target_obj,
    ):
        """Get set of nodes connected to this node."""
        ...

    @staticmethod
    def remove_edge(node, edge):
        """Remove reference without checking sync status."""
        ...

class JacEdge:
    """Jac Edge Operations."""

    @staticmethod
    def detach(edge):
        """Detach edge from nodes."""
        ...

class JacWalker:
    """Jac Edge Operations."""

    @staticmethod
    def visit_node(walker, expr):
        """Jac's visit stmt feature."""
        ...

    @staticmethod
    def ignore(walker, expr):
        """Jac's ignore stmt feature."""
        ...

    @staticmethod
    def spawn_call(op1, op2):
        """Jac's spawn operator feature."""
        ...

    @staticmethod
    def disengage(walker):
        """Jac's disengage stmt feature."""
        ...

class JacClassReferences:
    """Default Classes References."""

    EdgeDir: ClassVar[TypeAlias]
    DSFunc: ClassVar[TypeAlias]
    RootType: ClassVar[TypeAlias]
    Obj: ClassVar[TypeAlias]
    Node: ClassVar[TypeAlias]
    Edge: ClassVar[TypeAlias]
    Walker: ClassVar[TypeAlias]

class JacBuiltin:
    """Jac Builtins."""

    @staticmethod
    def dotgen(
        node,
        depth,
        traverse,
        edge_type,
        bfs,
        edge_limit,
        node_limit,
        dot_file,
    ):
        """Generate Dot file for visualizing nodes and edges."""
        ...

class JacCmd:
    """Jac CLI command."""

    @staticmethod
    def create_cmd():
        """Create Jac CLI cmds."""
        ...

class JacFeature(
    JacClassReferences,
    JacAccessValidation,
    JacNode,
    JacEdge,
    JacWalker,
    JacBuiltin,
    JacCmd,
):
    """Jac Feature."""

    @staticmethod
    def setup():
        """Set Class References."""
        ...

    @staticmethod
    def get_context():
        """Get current execution context."""
        ...

    @staticmethod
    def reset_graph(root):
        """Purge current or target graph."""
        ...

    @staticmethod
    def get_object(id):
        """Get object given id."""
        ...

    @staticmethod
    def get_object_func():
        """Get object given id."""
        ...

    @staticmethod
    def object_ref(obj):
        """Get object reference id."""
        ...

    @staticmethod
    def make_architype(
        cls,
        arch_base,
        on_entry,
        on_exit,
    ):
        """Create a obj architype."""
        ...

    @staticmethod
    def make_obj(on_entry, on_exit):
        """Create a obj architype."""
        ...

    @staticmethod
    def make_node(on_entry, on_exit):
        """Create a node architype."""
        ...

    @staticmethod
    def make_edge(on_entry, on_exit):
        """Create a edge architype."""
        ...

    @staticmethod
    def make_walker(on_entry, on_exit):
        """Create a walker architype."""
        ...

    @staticmethod
    def impl_patch_filename(
        file_loc,
    ):
        """Update impl file location."""
        ...

    @staticmethod
    def jac_import(
        target,
        base_path,
        absorb,
        cachable,
        mdl_alias,
        override_name,
        lng,
        items,
        reload_module,
    ):
        """Core Import Process."""
        ...

    @staticmethod
    def create_test(test_fun):
        """Create a test."""
        ...

    @staticmethod
    def run_test(
        filepath,
        filter,
        xit,
        maxfail,
        directory,
        verbose,
    ):
        """Run the test suite in the specified .jac file."""
        ...

    @staticmethod
    def elvis(op1, op2):
        """Jac's elvis operator feature."""
        ...

    @staticmethod
    def has_instance_default(gen_func):
        """Jac's has container default feature."""
        ...

    @staticmethod
    def report(expr, custom):
        """Jac's report stmt feature."""
        ...

    @staticmethod
    def edge_ref(
        node_obj,
        target_obj,
        dir,
        filter_func,
        edges_only,
    ):
        """Jac's apply_dir stmt feature."""
        ...

    @staticmethod
    def connect(
        left,
        right,
        edge_spec,
        edges_only,
    ):
        """Jac's connect operator feature.

        Note: connect needs to call assign compr with tuple in op
        """
        ...

    @staticmethod
    def disconnect(
        left,
        right,
        dir,
        filter_func,
    ):
        """Jac's disconnect operator feature."""
        ...

    @staticmethod
    def assign_compr(target, attr_val):
        """Jac's assign comprehension feature."""
        ...

    @staticmethod
    def get_root():
        """Jac's root getter."""
        ...

    @staticmethod
    def get_root_type():
        """Jac's root type getter."""
        ...

    @staticmethod
    def build_edge(
        is_undirected,
        conn_type,
        conn_assign,
    ):
        """Jac's root getter."""
        ...

    @staticmethod
    def save(
        obj,
    ):
        """Destroy object."""
        ...

    @staticmethod
    def destroy(
        obj,
    ):
        """Destroy object."""
        ...

    @staticmethod
    def get_semstr_type(file_loc, scope, attr, return_semstr):
        """Jac's get_semstr_type feature."""
        ...

    @staticmethod
    def obj_scope(file_loc, attr):
        """Jac's get_semstr_type feature."""
        ...

    @staticmethod
    def get_sem_type(file_loc, attr):
        """Jac's get_semstr_type feature."""
        ...

    @staticmethod
    def with_llm(
        file_loc,
        model,
        model_params,
        scope,
        incl_info,
        excl_info,
        inputs,
        outputs,
        action,
        _globals,
        _locals,
    ):
        """Jac's with_llm feature."""
        ...

    @staticmethod
    def gen_llm_body(_pass, node):
        """Generate the by LLM body."""
        ...

    @staticmethod
    def by_llm_call(
        _pass,
        model,
        model_params,
        scope,
        inputs,
        outputs,
        action,
        include_info,
        exclude_info,
    ):
        """Return the LLM Call, e.g. _Jac.with_llm()."""
        ...

    @staticmethod
    def get_by_llm_call_args(_pass, node):
        """Get the by LLM call args."""
        ...
