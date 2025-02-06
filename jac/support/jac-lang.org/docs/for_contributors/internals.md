# Jac Internals

This document has various notes and details related to the internal design and implementation of Jac and the Jaseci stack in general.

## Modules at Runtime

### JacMachine
`JacMachine` is responsible for managing the virtual machine (VM) functionalities for Jac. It handles the loading and execution of Jac modules, keeps track of them at runtime, and interacts with the Jac compiler to manage bytecode and program execution.

**Key Responsibilities:**
1. **Module Management**:
   - Loads Jac modules into an internal dictionary and synchronizes them with `sys.modules` for Python integration.
2. **Program Management**:
   - Attaches a `JacProgram` that handles compiled bytecode and manages module dependencies.
3. **Context Management**:
   - Utilizes a `ContextVar` to manage the current instance of the machine, allowing multiple independent Jac environments to run simultaneously.
4. **Dynamic Updates**:
   - Enables reloading and updating specific components such as walkers without the need to reload the entire module.

**Key Methods:**
- `load_module()`: Adds modules to the internal state and `sys.modules`.
- `get_bytecode()`: Fetches the compiled bytecode for a module or recompiles Jac code if necessary.
- `list_modules()`: Lists all currently loaded modules in the machine.
- `update_walker()`: Reimports and updates specific items, such as walkers, within a module.
- `get()`: Retrieves or creates a `JacMachine` instance in the current context.

### JacProgram

`JacProgram` works in tandem with `JacMachine` by storing compiled Jac modules and their bytecode. It provides methods to retrieve or recompile Jac code as needed, ensuring efficient management of compiled modules.

### Internal Interfaces for Architypes

#### Listing Architypes
  `JacMachine` offers internal interfaces for listing various types of architypes, such as walkers, nodes, and edges, within a module.
#### Replacing Walkers
One of the most powerful features of `JacMachine` is the ability to dynamically **replace walkers** at runtime. Walkers, being specialized functions that traverse and interact with nodes and edges, can be updated or modified while the program is running, without needing to reload the entire module.

**Key Concepts:**
1. **Dynamic Updates**: Through the `update_walker()` method, individual walkers can be redefined and updated during runtime. This allows developers to modify the behavior of specific walkers without disrupting the rest of the program.

2. **Selective Reimport**: Instead of reimporting the entire module, `JacMachine` focuses on reloading only the specified walker(s). This ensures minimal disruption and efficient updates. The old walker’s functionality is replaced with the new implementation.

3. **Smooth Transition**: `JacMachine` ensures that replacing a walker is seamless, meaning that running processes are not interrupted. This allows for continuous operation in long-running programs or live environments.

**Example Workflow for Replacing Walkers:**
1. **Identify the Walker**: The specific walker that needs updating is identified by its name within the module.
2. **Reimport the Module**: The module is selectively reimported, targeting the specific walker(s) to ensure only the necessary parts of the module are affected.
3. **Replace the Walker**: The old walker is swapped out for the new version, with state preserved where necessary to maintain continuity.

This capability makes `JacMachine` highly flexible, particularly useful in scenarios such as:
- **Debugging**: Fix and update walkers without halting execution.
- **Live Code Updates**: Modify behavior in real-time during active program execution.
- **Reactive Programming**: Adapt workflows dynamically based on real-time conditions.