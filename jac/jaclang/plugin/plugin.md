# **Override Plugin Implementations**


## AccessValidation Related Methods
### **`allow_root`**
```python
def allow_root(
    architype: Architype,
    root_id: UUID,
    level: AccessLevel | int | str
) -> None:
    """Allow all access from target root graph to current Architype."""
```
### **`disallow_root`**
```python
def disallow_root(
    architype: Architype,
    root_id: UUID,
    level: AccessLevel | int | str
) -> None:
    """Disallow all access from target root graph to current Architype."""
```
### **`unrestrict`**
```python
def unrestrict(
    architype: Architype,
    level: AccessLevel | int | str
) -> None:
    """Allow everyone to access current Architype."""
```
### **`restrict`**
```python
def restrict(
    architype: Architype
) -> None:
    """Disallow others to access current Architype."""
```
### **`check_read_access`**
```python
def check_read_access(
    to: Anchor
) -> bool:
    """Read Access Validation."""
```
### **`check_connect_access`**
```python
def check_connect_access(
    to: Anchor
) -> bool:
    """Connect Access Validation."""
```
### **`check_write_access`**
```python
def check_write_access(
    to: Anchor
) -> bool:
    """Write Access Validation."""
```
### **`check_access_level`**
```python
def check_access_level(
    to: Anchor
) -> AccessLevel:
    """Access validation."""
```


## Node Related Methods
### **`node_dot`**
```python
def node_dot(
    node: NodeArchitype,
    dot_file: Optional[str]
) -> str:
    """Generate Dot file for visualizing nodes and edges."""
```
### **`get_edges`**
```python
def get_edges(
    node: NodeAnchor,
    dir: EdgeDir,
    filter_func: Optional[Callable[[list[EdgeArchitype]], list[EdgeArchitype]]],
    target_obj: Optional[list[NodeArchitype]],
) -> list[EdgeArchitype]:
    """Get edges connected to this node."""
```
### **`edges_to_nodes`**
```python
def edges_to_nodes(
    node: NodeAnchor,
    dir: EdgeDir,
    filter_func: Optional[Callable[[list[EdgeArchitype]], list[EdgeArchitype]]],
    target_obj: Optional[list[NodeArchitype]],
) -> list[NodeArchitype]:
    """Get set of nodes connected to this node."""
```
### **`remove_edge`**
```python
def remove_edge(
    node: NodeAnchor,
    edge: EdgeAnchor
) -> None:
    """Remove reference without checking sync status."""
```


## Edge Related Methods
### **`detach`**
```python
def detach(
    edge: EdgeAnchor
) -> None:
    """Detach edge from nodes."""
```


## Walker Related Methods
### **`visit_node`**
```python
def visit_node(
    walker: WalkerArchitype,
    expr: (
    list[NodeArchitype | EdgeArchitype]
    | list[NodeArchitype]
    | list[EdgeArchitype]
    | NodeArchitype
    | EdgeArchitype
    ),
) -> bool:
    """Include target node/edge to current walker's visit queue."""
```
### **`ignore`**
```python
def ignore(
    walker: WalkerArchitype,
    expr: (
        list[NodeArchitype | EdgeArchitype]
        | list[NodeArchitype]
        | list[EdgeArchitype]
        | NodeArchitype
        | EdgeArchitype
    ),
) -> bool:
    """Include target node/edge to current walker's ignored architype."""
```
### **`spawn_call`**
```python
def spawn_call(
    op1: Architype,
    op2: Architype
) -> WalkerArchitype:
    """Invoke data spatial call."""
```
### **`disengage`**
```python
def disengage(
    walker: WalkerArchitype
) -> bool:
    """Disengaged current walker."""
```


## Builtin Related Methods
### **`dotgen`**
```python
def dotgen(
    node: NodeArchitype,
    depth: int,
    traverse: bool,
    edge_type: Optional[list[str]],
    bfs: bool,
    edge_limit: int,
    node_limit: int,
    dot_file: Optional[str],
) -> str:
    """Print the dot graph."""
```


## Cmd Related Methods
### **`create_cmd`**
```python
def create_cmd(
) -> None:
    """Create Jac CLI cmds."""
```


## Feature Related Methods
### **`setup`**
```python
def setup(
) -> None:
    """Set Class References to Jac."""
```
### **`get_context`**
```python
def get_context(
) -> ExecutionContext:
    """Get current execution context."""
```
### **`get_object`**
```python
def get_object(
    id: str
) -> Architype | None:
    """Get object by id."""
```
### **`object_ref`**
```python
def object_ref(
    obj: Architype
) -> str:
    """Get object's id."""
```
### **`make_architype`**
```python
def make_architype(
    cls: type,
    arch_base: Type[Architype],
    on_entry: list[DSFunc],
    on_exit: list[DSFunc],
) -> Type[Architype]:
    """Create a obj architype."""
```
### **`make_obj`**
```python
def make_obj(
    on_entry: list[DSFunc],
    on_exit: list[DSFunc]
) -> Callable[[type], type]:
    """Create a obj architype."""
```
### **`make_node`**
```python
def make_node(
    on_entry: list[DSFunc],
    on_exit: list[DSFunc]
) -> Callable[[type], type]:
    """Create a node architype."""
```
### **`make_edge`**
```python
def make_edge(
    on_entry: list[DSFunc],
    on_exit: list[DSFunc]
) -> Callable[[type], type]:
    """Create a edge architype."""
```
### **`make_walker`**
```python
def make_walker(
    on_entry: list[DSFunc],
    on_exit: list[DSFunc]
) -> Callable[[type], type]:
    """Create a walker architype."""
```
### **`impl_patch_filename`**
```python
def impl_patch_filename(
    file_loc: str,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Update impl file location."""
```
### **`jac_import`**
```python
def jac_import(
    target: str,
    base_path: str,
    absorb: bool,
    cachable: bool,
    mdl_alias: Optional[str],
    override_name: Optional[str],
    lng: Optional[str],
    items: Optional[dict[str, Union[str, Optional[str]]]],
    reload_module: Optional[bool],
) -> tuple[types.ModuleType, ...]:
    """Core Import Process."""
```
### **`create_test`**
```python
def create_test(
    test_fun: Callable
) -> Callable:
    """Create a new test."""
```
### **`run_test`**
```python
def run_test(
    filepath: str,
    filter: Optional[str],
    xit: bool,
    maxfail: Optional[int],
    directory: Optional[str],
    verbose: bool,
) -> int:
    """Run the test suite in the specified .jac file."""
```
### **`elvis`**
```python
def elvis(
    op1: Optional[T],
    op2: T
) -> T:
    """Jac's elvis operator feature."""
```
### **`has_instance_default`**
```python
def has_instance_default(
    gen_func: Callable[[], T]
) -> T:
    """Jac's has container default feature."""
```
### **`report`**
```python
def report(
    expr: Any
) -> Any:
    """Jac's report stmt feature."""
```
### **`edge_ref`**
```python
def edge_ref(
    node_obj: NodeArchitype | list[NodeArchitype],
    target_obj: Optional[NodeArchitype | list[NodeArchitype]],
    dir: EdgeDir,
    filter_func: Optional[Callable[[list[EdgeArchitype]], list[EdgeArchitype]]],
    edges_only: bool,
) -> list[NodeArchitype] | list[EdgeArchitype]:
    """Jac's apply_dir stmt feature."""
```
### **`connect`**
```python
def connect(
    left: NodeArchitype | list[NodeArchitype],
    right: NodeArchitype | list[NodeArchitype],
    edge_spec: Callable[[NodeAnchor, NodeAnchor], EdgeArchitype],
    edges_only: bool,
) -> list[NodeArchitype] | list[EdgeArchitype]:
    """Jac's connect operator feature.

    Note: connect needs to call assign compr with tuple in op
    """
```
### **`disconnect`**
```python
def disconnect(
    left: NodeArchitype | list[NodeArchitype],
    right: NodeArchitype | list[NodeArchitype],
    dir: EdgeDir,
    filter_func: Optional[Callable[[list[EdgeArchitype]], list[EdgeArchitype]]],
) -> bool:
    """Jac's disconnect operator feature."""
```
### **`assign_compr`**
```python
def assign_compr(
    target: list[T],
    attr_val: tuple[tuple[str], tuple[Any]]
) -> list[T]:
    """Jac's assign comprehension feature."""
```
### **`get_root`**
```python
def get_root(
) -> Root:
    """Get current root."""
```
### **`get_root_type`**
```python
def get_root_type(
) -> Type[Root]:
    """Get root type."""
```
### **`build_edge`**
```python
def build_edge(
    is_undirected: bool,
    conn_type: Optional[Type[EdgeArchitype] | EdgeArchitype],
    conn_assign: Optional[tuple[tuple, tuple]],
) -> Callable[[NodeAnchor, NodeAnchor], EdgeArchitype]:
    """Build edge operator."""
```
### **`save`**
```python
def save(
    obj: Architype | Anchor,
) -> None:
    """Save object."""
```
### **`destroy`**
```python
def destroy(
    obj: Architype | Anchor,
) -> None:
    """Destroy object."""
```
### **`get_semstr_type`**
```python
def get_semstr_type(
    file_loc: str,
    scope: str,
    attr: str,
    return_semstr: bool
) -> Optional[str]:
    """Jac's get_semstr_type stmt feature."""
```
### **`obj_scope`**
```python
def obj_scope(
    file_loc: str,
    attr: str
) -> str:
    """Jac's get_semstr_type feature."""
```
### **`get_sem_type`**
```python
def get_sem_type(
    file_loc: str,
    attr: str
) -> tuple[str | None, str | None]:
    """Jac's get_semstr_type feature."""
```
### **`with_llm`**
```python
def with_llm(
    file_loc: str,
    model: Any,
    model_params: dict[str, Any],
    scope: str,
    incl_info: list[tuple[str, str]],
    excl_info: list[tuple[str, str]],
    inputs: list[tuple[str, str, str, Any]],
    outputs: tuple,
    action: str,
    _globals: dict,
    _locals: Mapping,
) -> Any:
    """Jac's with_llm stmt feature."""
```
### **`gen_llm_body`**
```python
def gen_llm_body(
    _pass: PyastGenPass,
    node: ast.Ability
) -> list[ast3.AST]:
    """Generate the by LLM body."""
```
### **`by_llm_call`**
```python
def by_llm_call(
    _pass: PyastGenPass,
    model: ast3.AST,
    model_params: dict[str, ast.Expr],
    scope: ast3.AST,
    inputs: Sequence[Optional[ast3.AST]],
    outputs: Sequence[Optional[ast3.AST]] | ast3.Call,
    action: Optional[ast3.AST],
    include_info: list[tuple[str, ast3.AST]],
    exclude_info: list[tuple[str, ast3.AST]],
) -> ast3.Call:
    """Return the LLM Call, e.g. _Jac.with_llm()."""
```
### **`get_by_llm_call_args`**
```python
def get_by_llm_call_args(
    _pass: PyastGenPass,
    node: ast.FuncCall
) -> dict:
    """Get the by LLM call args."""
```
