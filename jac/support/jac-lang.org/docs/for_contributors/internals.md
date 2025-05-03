# Jaclang Internals

This document provides a comprehensive guide to the internal design and implementation of the Jaclang compiler and runtime stack. It's intended for developers who want to contribute to the Jaclang project or understand its architecture in depth.

## Architecture Overview

Jaclang is composed of two main components:

1. **Compiler**: Transforms Jac source code into Python bytecode through a series of passes
2. **Runtime**: Provides the execution environment for compiled Jac programs

The system follows a modular design that separates concerns between compilation and execution, allowing for flexibility and extensibility.

```mermaid
flowchart LR
    A[Jac Source] --> B[Compiler]
    B --> C[Bytecode]
    C --> D[Execution]
    D --> E[Runtime]
    E --> F[Results]

    style A fill:#f9f9f9,stroke:#333,stroke-width:2px
    style B fill:#d4f1f9,stroke:#333,stroke-width:2px
    style C fill:#d4f1f9,stroke:#333,stroke-width:2px
    style D fill:#e6f3e6,stroke:#333,stroke-width:2px
    style E fill:#e6f3e6,stroke:#333,stroke-width:2px
    style F fill:#f9f9f9,stroke:#333,stroke-width:2px
```

## Compiler Components

The compiler transforms Jac source code into Python bytecode through a series of passes. Each pass performs a specific transformation on the code.

### Compilation Pipeline

The compiler transforms Jac source code into Python bytecode through a series of passes:

```mermaid
flowchart TD
    A[Jac Source Code] --> B[Parsing]
    B --> C[Symbol Table Building]
    C --> D[Import Resolution]
    D --> E[Type Checking]
    E --> F[Python AST Generation]
    F --> G[Bytecode Generation]
    G --> H[Python Bytecode]

    style A fill:#f9f9f9,stroke:#333,stroke-width:2px
    style B fill:#d4f1f9,stroke:#333,stroke-width:2px
    style C fill:#d4f1f9,stroke:#333,stroke-width:2px
    style D fill:#d4f1f9,stroke:#333,stroke-width:2px
    style E fill:#d4f1f9,stroke:#333,stroke-width:2px
    style F fill:#d4f1f9,stroke:#333,stroke-width:2px
    style G fill:#d4f1f9,stroke:#333,stroke-width:2px
    style H fill:#f9f9f9,stroke:#333,stroke-width:2px
```

1. **Parsing**: Converts Jac source code into an Abstract Syntax Tree (AST)
2. **Symbol Table Building**: Creates symbol tables for scopes and resolves symbols
3. **Import Resolution**: Processes import statements and loads external modules
4. **Type Checking**: Performs type checking and inference
5. **Python AST Generation**: Converts Jac AST to Python AST
6. **Bytecode Generation**: Generates Python bytecode from the Python AST

### Key Compiler Components

#### JacProgram

`JacProgram` is the central component that orchestrates the compilation process. It maintains a collection of modules and manages the compilation pipeline.

```python
class JacProgram:
    """JacProgram to handle the Jac program-related functionalities."""

    def __init__(self, main_mod: Optional[uni.ProgramModule] = None) -> None:
        """Initialize the JacProgram object."""
        self.mod: uni.ProgramModule = main_mod if main_mod else uni.ProgramModule()
        self.last_imported: list[Module] = []
        self.py_raise_map: dict[str, str] = {}
        self.errors_had: list[Alert] = []
        self.warnings_had: list[Alert] = []
```

Key methods:
- `get_bytecode()`: Retrieves bytecode for a specific module
- `compile()`: Compiles a Jac file to an AST
- `compile_from_str()`: Compiles Jac code from a string
- `run_pass_schedule()`: Executes the compilation passes on a module
- `run_whole_program_schedule()`: Runs passes that require whole-program analysis

#### Unitree

The `unitree` module defines the AST node types used in the compilation process. The AST is a hierarchical representation of the program's structure.

Key classes:
- `UniNode`: Base class for all AST nodes
- `UniScopeNode`: Represents a scope with a symbol table
- `Module`: Represents a Jac module
- `Architype`: Represents a Jac architype (object, node, edge, walker)
- `Ability`: Represents a Jac ability (method)

#### Compiler Components Relationship

```mermaid
classDiagram
    class JacProgram {
        +ProgramModule mod
        +list[Module] last_imported
        +dict py_raise_map
        +list errors_had
        +list warnings_had
        +get_bytecode()
        +compile()
        +compile_from_str()
        +run_pass_schedule()
        +run_whole_program_schedule()
    }

    class UniNode {
        +UniNode parent
        +list[UniNode] kid
        +CodeGenTarget gen
        +CodeLocInfo loc
    }

    class Module {
        +str name
        +Source source
        +list body
        +bool stub_only
        +list impl_mod
        +list test_mod
        +list terminals
        +PyInfo py_info
    }

    class Transform {
        +ir_in
        +ir_out
        +list errors_had
        +list warnings_had
    }

    JacProgram --> Module : manages
    Module --|> UniNode : inherits
    Transform --> UniNode : transforms

    note for JacProgram "Orchestrates the compilation process"
    note for UniNode "Base class for all AST nodes"
    note for Module "Represents a Jac module"
    note for Transform "Base class for compiler passes"
```

#### Compiler Passes

Compiler passes are transformations applied to the AST. Each pass is responsible for a specific aspect of the compilation process.

```mermaid
flowchart LR
    A[JacParser] --> B[SymTabBuildPass]
    B --> C[JacImportPass]
    C --> D[JacTypeCheckPass]
    D --> E[PyastBuildPass]
    E --> F[PyBytecodeGenPass]

    style A fill:#d4f1f9,stroke:#333,stroke-width:2px
    style B fill:#d4f1f9,stroke:#333,stroke-width:2px
    style C fill:#d4f1f9,stroke:#333,stroke-width:2px
    style D fill:#d4f1f9,stroke:#333,stroke-width:2px
    style E fill:#d4f1f9,stroke:#333,stroke-width:2px
    style F fill:#d4f1f9,stroke:#333,stroke-width:2px
```

Main passes:
- `JacParser`: Parses Jac source code into an AST
- `SymTabBuildPass`: Builds symbol tables for scopes
- `JacImportPass`: Resolves import statements
- `JacTypeCheckPass`: Performs type checking
- `PyastBuildPass`: Converts Jac AST to Python AST
- `PyBytecodeGenPass`: Generates Python bytecode

## Runtime Components

The runtime system executes compiled Jac programs and provides the necessary infrastructure for Jac's features.

```mermaid
classDiagram
    class JacMachine {
        +load_module()
        +get_bytecode()
        +list_modules()
        +update_walker()
        +get()
    }

    class JacMachineState {
        +dict loaded_modules
        +str base_path
        +str base_path_dir
        +JacProgram jac_program
        +bool interp_mode
        +ExecutionContext exec_ctx
    }

    class ExecutionContext {
        +JacMachineState mach
        +Memory mem
        +list reports
        +Any custom
        +NodeAnchor system_root
        +NodeAnchor root
        +NodeAnchor entry_node
        +init_anchor()
        +set_entry_node()
        +close()
        +get_root()
    }

    JacMachine --> JacMachineState : uses
    JacMachineState --> ExecutionContext : contains
    JacMachineState --> JacProgram : contains

    note for JacMachine "Core runtime component"
    note for JacMachineState "Maintains runtime state"
    note for ExecutionContext "Execution environment"
```

### JacMachine

`JacMachine` is the core runtime component that manages the execution environment for Jac programs. It handles module loading, execution context, and provides the runtime API for Jac features.

```python
class JacMachine(
    JacClassReferences,
    JacAccessValidation,
    JacNode,
    JacEdge,
    JacWalker,
    JacBuiltin,
    JacCmd,
    JacBasics,
    JacUtils,
):
    """Jac Feature."""
```

Key responsibilities:
1. **Module Management**: Loads and manages Jac modules
2. **Context Management**: Maintains execution context for Jac programs
3. **Runtime API**: Provides the API for Jac features like node/edge operations, walker operations, etc.
4. **Dynamic Updates**: Enables runtime updates to components like walkers

### JacMachineState

`JacMachineState` maintains the state of the Jac machine during execution. It includes loaded modules, the execution context, and the Jac program.

```python
class JacMachineState:
    """Jac Machine State."""

    def __init__(
        self,
        base_path: str = "",
        session: Optional[str] = None,
        root: Optional[str] = None,
        interp_mode: bool = False,
    ) -> None:
        """Initialize JacMachineState."""
        self.loaded_modules: dict[str, types.ModuleType] = {}
        if not base_path:
            base_path = os.getcwd()
        # Ensure the base_path is a list rather than a string
        self.base_path = base_path
        self.base_path_dir = (
            os.path.dirname(base_path)
            if not os.path.isdir(base_path)
            else os.path.abspath(base_path)
        )
        self.jac_program: JacProgram = JacProgram()
        self.interp_mode = interp_mode
        self.exec_ctx = ExecutionContext(session=session, root=root, mach=self)
```

### ExecutionContext

`ExecutionContext` represents the execution environment for a Jac program. It includes the memory, reports, and root nodes.

```python
class ExecutionContext:
    """Execution Context."""

    mach: JacMachineState
    mem: Memory
    reports: list[Any]
    custom: Any = MISSING
    system_root: NodeAnchor
    root: NodeAnchor
    entry_node: NodeAnchor
```

## Memory Management

Jaclang uses a memory management system to store and retrieve objects during execution.

### Memory

The `Memory` class is a generic memory handler that stores objects by ID. It provides methods to find, set, and remove objects.

```python
@dataclass
class Memory(Generic[ID, TANCH]):
    """Generic Memory Handler."""

    __mem__: dict[ID, TANCH] = field(default_factory=dict)
    __gc__: set[TANCH] = field(default_factory=set)
```

### ShelfStorage

`ShelfStorage` extends `Memory` to provide persistent storage using Python's `shelve` module. It synchronizes memory with disk storage.

```python
@dataclass
class ShelfStorage(Memory[UUID, Anchor]):
    """Shelf Handler."""

    __shelf__: Shelf[Anchor] | None = None
```

## Architypes and Anchors

Jaclang uses architypes and anchors to represent objects in the runtime system.

```mermaid
classDiagram
    class Architype {
        +list _jac_entry_funcs_
        +list _jac_exit_funcs_
        +Anchor __jac__
    }

    class NodeArchitype {
        +__jac_base__: bool
    }

    class EdgeArchitype {
        +__jac_base__: bool
    }

    class WalkerArchitype {
        +__jac_base__: bool
    }

    class ObjectArchitype {
        +__jac_base__: bool
    }

    class Anchor {
        +Architype architype
        +UUID id
        +UUID root
        +Permission access
        +bool persistent
        +int hash
        +is_populated()
        +make_stub()
        +populate()
    }

    class NodeAnchor {
        +NodeArchitype architype
        +list edges
    }

    class EdgeAnchor {
        +EdgeArchitype architype
        +NodeAnchor source
        +NodeAnchor target
        +bool is_undirected
    }

    class WalkerAnchor {
        +WalkerArchitype architype
        +list path
        +list next
        +list ignores
        +bool disengaged
    }

    Architype <|-- NodeArchitype : inherits
    Architype <|-- EdgeArchitype : inherits
    Architype <|-- WalkerArchitype : inherits
    Architype <|-- ObjectArchitype : inherits

    Anchor <|-- NodeAnchor : inherits
    Anchor <|-- EdgeAnchor : inherits
    Anchor <|-- WalkerAnchor : inherits

    Architype --> Anchor : has
    NodeArchitype --> NodeAnchor : has
    EdgeArchitype --> EdgeAnchor : has
    WalkerArchitype --> WalkerAnchor : has

    NodeAnchor --> EdgeAnchor : contains
    EdgeAnchor --> NodeAnchor : references
```

### Architype

`Architype` is the base class for all Jac objects. It defines the common interface for all architypes.

```python
@dataclass(eq=False, repr=False, kw_only=True)
class Architype:
    """Architype Protocol."""

    _jac_entry_funcs_: ClassVar[list[DataSpatialFunction]] = []
    _jac_exit_funcs_: ClassVar[list[DataSpatialFunction]] = []

    @cached_property
    def __jac__(self) -> Anchor:
        """Create default anchor."""
        return Anchor(architype=self)
```

Specialized architypes:
- `NodeArchitype`: Represents a node in a graph
- `EdgeArchitype`: Represents an edge in a graph
- `WalkerArchitype`: Represents a walker that traverses a graph
- `ObjectArchitype`: Represents a generic object

### Anchor

`Anchor` is a wrapper around an architype that provides additional metadata and functionality.

```python
@dataclass(eq=False, repr=False, kw_only=True)
class Anchor:
    """Object Anchor."""

    architype: Architype
    id: UUID = field(default_factory=uuid4)
    root: Optional[UUID] = None
    access: Permission = field(default_factory=Permission)
    persistent: bool = False
    hash: int = 0
```

Specialized anchors:
- `NodeAnchor`: Wraps a `NodeArchitype` and maintains a list of connected edges
- `EdgeAnchor`: Wraps an `EdgeArchitype` and maintains references to source and target nodes
- `WalkerAnchor`: Wraps a `WalkerArchitype` and maintains walker state

## Module System

Jaclang has a sophisticated module system that handles importing Jac and Python modules.

```mermaid
flowchart TD
    A[Import Request] --> B{Is Python Module?}
    B -->|Yes| C[PythonImporter]
    B -->|No| D[JacImporter]
    C --> E[importlib.import_module]
    D --> F[Resolve Module Path]
    F --> G[Create Module]
    G --> H[Compile Module]
    H --> I[Execute Module]
    I --> J[Update Module Registry]
    E --> J

    style A fill:#f9f9f9,stroke:#333,stroke-width:2px
    style B fill:#f9d9d9,stroke:#333,stroke-width:2px
    style C fill:#d4f1f9,stroke:#333,stroke-width:2px
    style D fill:#d4f1f9,stroke:#333,stroke-width:2px
    style E fill:#e6f3e6,stroke:#333,stroke-width:2px
    style F fill:#e6f3e6,stroke:#333,stroke-width:2px
    style G fill:#e6f3e6,stroke:#333,stroke-width:2px
    style H fill:#e6f3e6,stroke:#333,stroke-width:2px
    style I fill:#e6f3e6,stroke:#333,stroke-width:2px
    style J fill:#f9f9f9,stroke:#333,stroke-width:2px
```

```mermaid
classDiagram
    class Importer {
        +JacMachineState jac_machine
        +ImportReturn result
        +run_import()
    }

    class JacImporter {
        +get_sys_mod_name()
        +handle_directory()
        +create_jac_py_module()
        +run_import()
    }

    class PythonImporter {
        +run_import()
    }

    class ImportPathSpec {
        +str target
        +str base_path
        +bool absorb
        +str mdl_alias
        +str override_name
        +str language
        +dict items
        +get_caller_dir()
    }

    class ImportReturn {
        +types.ModuleType ret_mod
        +list ret_items
        +Importer importer
        +process_items()
        +load_jac_mod_as_item()
    }

    Importer <|-- JacImporter : inherits
    Importer <|-- PythonImporter : inherits
    Importer --> ImportPathSpec : uses
    Importer --> ImportReturn : returns
```

### Importers

The module system uses importers to load modules:

- `JacImporter`: Loads Jac modules
- `PythonImporter`: Loads Python modules

```python
class Importer:
    """Abstract base class for all importers."""

    def __init__(self, jac_machine: JacMachineState) -> None:
        """Initialize the Importer object."""
        self.jac_machine = jac_machine
        self.result: Optional[ImportReturn] = None

    def run_import(self, spec: ImportPathSpec) -> ImportReturn:
        """Run the import process."""
        raise NotImplementedError
```

### Import Process

The import process involves:

1. Resolving the module path
2. Loading the module
3. Compiling the module (for Jac modules)
4. Executing the module
5. Updating the module registry

## Dynamic Updates

One of the most powerful features of `JacMachine` is the ability to dynamically update components at runtime, particularly walkers.

```mermaid
sequenceDiagram
    participant User
    participant JacMachine
    participant JacImporter
    participant Module
    participant Walker

    User->>JacMachine: update_walker(module_name, items)
    JacMachine->>JacMachine: Check if module exists
    JacMachine->>JacImporter: Create importer
    JacMachine->>JacImporter: Create ImportPathSpec
    JacImporter->>JacImporter: run_import(spec, reload=True)
    JacImporter->>Module: Load updated module
    JacMachine->>Module: Get old module
    JacMachine->>Module: Update specific items
    Module->>Walker: Replace walker implementation
    JacMachine-->>User: Return updated items

    note over JacMachine,Walker: Only the specified walkers are updated, not the entire module
```

### Updating Walkers

Walkers can be updated during runtime without reloading the entire module. This is useful for debugging, live code updates, and reactive programming.

```python
@staticmethod
def update_walker(
    mach: JacMachineState,
    module_name: str,
    items: Optional[dict[str, Union[str, Optional[str]]]],
) -> tuple[types.ModuleType, ...]:
    """Reimport the module."""
    from .importer import JacImporter, ImportPathSpec

    if module_name in mach.loaded_modules:
        try:
            old_module = mach.loaded_modules[module_name]
            importer = JacImporter(mach)
            spec = ImportPathSpec(
                target=module_name,
                base_path=mach.base_path,
                absorb=False,
                mdl_alias=None,
                override_name=None,
                lng="jac",
                items=items,
            )
            import_result = importer.run_import(spec, reload=True)
            ret_items = []
            if items:
                for item_name in items:
                    if hasattr(old_module, item_name):
                        new_attr = getattr(import_result.ret_mod, item_name, None)
                        if new_attr:
                            ret_items.append(new_attr)
                            setattr(
                                old_module,
                                item_name,
                                new_attr,
                            )
            return (old_module,) if not items else tuple(ret_items)
        except Exception as e:
            logger.error(f"Failed to update module {module_name}: {e}")
    else:
        logger.warning(f"Module {module_name} not found in loaded modules.")
    return ()
```

## Access Control

Jaclang has a sophisticated access control system that manages permissions for objects.

```mermaid
classDiagram
    class AccessLevel {
        <<enumeration>>
        NO_ACCESS
        READ
        CONNECT
        WRITE
        +cast()
    }

    class Access {
        +dict anchors
        +check()
    }

    class Permission {
        +AccessLevel all
        +Access roots
    }

    class Anchor {
        +Permission access
    }

    Permission --> AccessLevel : uses
    Permission --> Access : contains
    Anchor --> Permission : has

    note for AccessLevel "Defines access levels"
    note for Access "Maps anchors to access levels"
    note for Permission "Defines permissions for an anchor"
```

```mermaid
flowchart TD
    A[Access Request] --> B{Check Access Level}
    B --> C{Is System Root?}
    C -->|Yes| D[Grant WRITE Access]
    C -->|No| E{Is Same Root?}
    E -->|Yes| D
    E -->|No| F{Is Target Anchor?}
    F -->|Yes| D
    F -->|No| G{Check access.all}
    G --> H{Check target root's access.all}
    H --> I{Check target root's allowed roots}
    I --> J{Check target's allowed roots}
    J --> K[Return Final Access Level]

    style A fill:#f9f9f9,stroke:#333,stroke-width:2px
    style B fill:#f9d9d9,stroke:#333,stroke-width:2px
    style C fill:#f9d9d9,stroke:#333,stroke-width:2px
    style D fill:#e6f3e6,stroke:#333,stroke-width:2px
    style E fill:#f9d9d9,stroke:#333,stroke-width:2px
    style F fill:#f9d9d9,stroke:#333,stroke-width:2px
    style G fill:#f9d9d9,stroke:#333,stroke-width:2px
    style H fill:#f9d9d9,stroke:#333,stroke-width:2px
    style I fill:#f9d9d9,stroke:#333,stroke-width:2px
    style J fill:#f9d9d9,stroke:#333,stroke-width:2px
    style K fill:#f9f9f9,stroke:#333,stroke-width:2px
```

### Permission

The `Permission` class defines access levels for objects:

```python
@dataclass
class Permission:
    """Anchor Access Handler."""

    all: AccessLevel = AccessLevel.NO_ACCESS
    roots: Access = field(default_factory=Access)
```

### AccessLevel

`AccessLevel` defines the levels of access:

```python
class AccessLevel(IntEnum):
    """Access level enum."""

    NO_ACCESS = -1
    READ = 0
    CONNECT = 1
    WRITE = 2
```

## Contributing to Jaclang

### Understanding the Codebase

The Jaclang codebase is organized into several key directories:

```mermaid
graph TD
    A[jaclang] --> B[compiler]
    A --> C[runtimelib]
    A --> D[utils]
    A --> E[cli]
    A --> F[langserve]

    B --> B1[passes]
    B --> B2[unitree.py]
    B --> B3[program.py]
    B --> B4[parser.py]

    C --> C1[architype.py]
    C --> C2[machine.py]
    C --> C3[memory.py]
    C --> C4[importer.py]

    style A fill:#f9f9f9,stroke:#333,stroke-width:2px
    style B fill:#d4f1f9,stroke:#333,stroke-width:2px
    style C fill:#e6f3e6,stroke:#333,stroke-width:2px
    style D fill:#f9d9d9,stroke:#333,stroke-width:2px
    style E fill:#f9d9d9,stroke:#333,stroke-width:2px
    style F fill:#f9d9d9,stroke:#333,stroke-width:2px
```

- `jaclang/compiler`: Contains the compiler components
- `jaclang/runtimelib`: Contains the runtime components
- `jaclang/utils`: Contains utility functions
- `jaclang/cli`: Contains the command-line interface
- `jaclang/langserve`: Contains the language server components

### Development Workflow

```mermaid
flowchart LR
    A[Setup] --> B[Testing]
    B --> C[Implementation]
    C --> D[Documentation]
    D --> E[Pull Request]
    E --> F[Code Review]
    F --> G[Merge]

    style A fill:#f9f9f9,stroke:#333,stroke-width:2px
    style B fill:#d4f1f9,stroke:#333,stroke-width:2px
    style C fill:#d4f1f9,stroke:#333,stroke-width:2px
    style D fill:#d4f1f9,stroke:#333,stroke-width:2px
    style E fill:#e6f3e6,stroke:#333,stroke-width:2px
    style F fill:#e6f3e6,stroke:#333,stroke-width:2px
    style G fill:#e6f3e6,stroke:#333,stroke-width:2px
```

1. **Setup**: Clone the repository and install dependencies
2. **Testing**: Run tests to ensure your changes don't break existing functionality
3. **Implementation**: Make your changes following the project's coding standards
4. **Documentation**: Update documentation to reflect your changes
5. **Pull Request**: Submit a pull request with your changes

### Best Practices

- Follow the existing code style and architecture
- Write tests for new functionality
- Document your code with docstrings
- Keep changes focused and minimal
- Discuss major changes with the community before implementation

## Conclusion

This document provides an overview of the Jaclang internals. For more detailed information, refer to the source code and other documentation. If you have questions or need help, feel free to reach out to the Jaclang community.
