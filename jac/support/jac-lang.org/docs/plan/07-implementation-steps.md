# Implementation Steps

This document provides a roadmap for implementing the type checking system in phases, serving as an educational guide for understanding the architecture and implementation of a type checker.

## Understanding Type Checker Development

Building a type checking system requires a careful balance of theoretical type system knowledge and practical engineering concerns. This guide breaks down the process into manageable phases, each focusing on a specific aspect of the type checker.

### Architectural Principles

Before diving into implementation steps, let's consider some core principles that guide type checker design:

1. **Correctness**: The type checker must accurately implement the language's type rules without false positives or negatives.

2. **Performance**: Type checking should be fast enough to run in real-time IDE scenarios while handling large codebases.

3. **Modularity**: Components should be self-contained with clear interfaces for testability and maintainability.

4. **Extensibility**: The system should accommodate new language features and type system enhancements.

5. **User Experience**: Error messages and type information should be clear, actionable, and educational for developers.

### Implementation Approach

We'll use a phased approach to build the type checker, starting with core components and gradually adding more sophisticated features:

1. Core type system and representation
2. Type inference engine
3. Type checking pipeline integration
4. Error reporting system
5. Language-specific features
6. External tool integration

This approach allows for incremental testing and early validation of core components.

## Phase 1: Core Type System

The foundation of any type checker is its type representation and relationships. This phase establishes the fundamental data structures and algorithms for representing types.

### Understanding Type Representation

Types in programming languages aren't just simple labels; they represent complex contracts and relationships. A robust type system needs to model:

1. **Basic Types**: Primitives like integers, strings, booleans
2. **Compound Types**: Arrays, records/objects, unions, intersections
3. **Function Types**: Input and output type relationships
4. **Type Relationships**: Subtyping, compatibility, equivalence
5. **Type Variables**: For generic/polymorphic types

### Implementation Steps

1. **Implement the core type classes**:

   - **Basic `Type` class and subclasses**:
     ```python
     class Type:
         """Base class for all types in the type system."""
         def __init__(self, name: str):
             self.name = name

         def is_compatible_with(self, other: 'Type') -> bool:
             """Check if this type is compatible with another type."""
             return self == other

     class PrimitiveType(Type):
         """Represents primitive types like int, float, string, etc."""
         pass

     class FunctionType(Type):
         """Represents function types with parameters and return types."""
         def __init__(self, name: str, param_types: list[Type], return_type: Type):
             super().__init__(name)
             self.param_types = param_types
             self.return_type = return_type
     ```

   - **`TypeRegistry` for type storage and lookup**:
     ```python
     class TypeRegistry:
         """Central repository for all types in the program."""
         def __init__(self):
             self.types = {}  # name -> Type
             self.initialize_primitive_types()

         def initialize_primitive_types(self):
             """Register built-in primitive types."""
             for name in ["int", "float", "str", "bool", "None"]:
                 self.register_type(PrimitiveType(name))

         def register_type(self, type_obj: Type):
             """Register a type in the registry."""
             self.types[type_obj.name] = type_obj

         def lookup_type(self, name: str) -> Optional[Type]:
             """Look up a type by name."""
             return self.types.get(name)
     ```

   - **Support for subtyping relationships**:
     ```python
     def is_subtype(sub: Type, sup: Type) -> bool:
         """Check if sub is a subtype of sup."""
         # Direct equality
         if sub == sup:
             return True

         # Built-in subtyping relationships (e.g., int is a subtype of float)
         if isinstance(sub, PrimitiveType) and isinstance(sup, PrimitiveType):
             if sub.name == "int" and sup.name == "float":
                 return True

         # Class inheritance
         if isinstance(sub, ClassType) and isinstance(sup, ClassType):
             return any(is_subtype(base, sup) for base in sub.bases)

         # Function subtyping follows contravariant parameter types and covariant return type
         if isinstance(sub, FunctionType) and isinstance(sup, FunctionType):
             if len(sub.param_types) != len(sup.param_types):
                 return False

             # Parameters are contravariant
             params_ok = all(is_subtype(sup_param, sub_param)
                           for sub_param, sup_param in zip(sub.param_types, sup.param_types))

             # Return type is covariant
             return_ok = is_subtype(sub.return_type, sup.return_type)

             return params_ok and return_ok

         return False
     ```

   - **Support for primitive types**:

     Beyond the basic primitive types, implement the operations and relationships specific to primitives:
     ```python
     class NumericType(PrimitiveType):
         """Base class for numeric types."""
         def can_perform_operation(self, op: str, other: Type) -> bool:
             """Check if this type can perform an operation with another type."""
             if op in ['+', '-', '*', '/'] and isinstance(other, NumericType):
                 return True
             return super().can_perform_operation(op, other)

     class IntType(NumericType):
         """Integer type."""
         def __init__(self):
             super().__init__("int")

     class FloatType(NumericType):
         """Float type."""
         def __init__(self):
             super().__init__("float")
     ```

2. **Integrate with Jac's AST**:

   - **Add type information to expression nodes**:

     Extend the AST node classes to include type information:
     ```python
     class ExprNode:
         """Base class for expression nodes in the AST."""
         def __init__(self):
             self.inferred_type = None  # Will be populated during type inference
     ```

   - **Set up symbol table integration**:

     Enhance the symbol table to include type information:
     ```python
     class Symbol:
         """Entry in the symbol table."""
         def __init__(self, name: str, type_: Optional[Type] = None):
             self.name = name
             self.type = type_

     class SymbolTable:
         """Tracks symbols and their types in a scope."""
         def __init__(self, parent=None):
             self.symbols = {}  # name -> Symbol
             self.parent = parent

         def define(self, name: str, type_: Optional[Type] = None) -> Symbol:
             """Define a new symbol in this scope."""
             symbol = Symbol(name, type_)
             self.symbols[name] = symbol
             return symbol

         def resolve(self, name: str) -> Optional[Symbol]:
             """Look up a symbol by name, checking parent scopes if not found."""
             if name in self.symbols:
                 return self.symbols[name]
             if self.parent:
                 return self.parent.resolve(name)
             return None
     ```

   - **Create serialization/deserialization for types**:

     Implement serialization to enable caching and persistance of type information:
     ```python
     def serialize_type(type_obj: Type) -> dict:
         """Convert a type to a JSON-serializable dictionary."""
         if isinstance(type_obj, PrimitiveType):
             return {"kind": "primitive", "name": type_obj.name}
         elif isinstance(type_obj, FunctionType):
             return {
                 "kind": "function",
                 "name": type_obj.name,
                 "params": [serialize_type(param) for param in type_obj.param_types],
                 "return": serialize_type(type_obj.return_type)
             }
         # Add other type kinds as needed

     def deserialize_type(data: dict, type_registry: TypeRegistry) -> Type:
         """Recreate a type from its serialized form."""
         kind = data["kind"]
         if kind == "primitive":
             return type_registry.lookup_type(data["name"])
         elif kind == "function":
             params = [deserialize_type(param, type_registry) for param in data["params"]]
             return_type = deserialize_type(data["return"], type_registry)
             return FunctionType(data["name"], params, return_type)
         # Add other type kinds as needed
     ```

### Key Concepts in Type System Design

When implementing a type system, consider these important concepts:

1. **Nominal vs. Structural Typing**:
   - **Nominal typing** checks compatibility based on explicit declarations (e.g., class inheritance)
   - **Structural typing** checks compatibility based on structure (e.g., duck typing)
   - Most languages use a combination of both approaches

2. **Variance**:
   - **Covariance**: If T is a subtype of U, then C[T] is a subtype of C[U]
   - **Contravariance**: If T is a subtype of U, then C[U] is a subtype of C[T]
   - **Invariance**: Neither covariant nor contravariant

3. **Type Equivalence**:
   - **Name Equivalence**: Types are equivalent if they have the same name
   - **Structural Equivalence**: Types are equivalent if they have the same structure
   - **Behavioral Equivalence**: Types are equivalent if they behave the same way

4. **Type Safety**:
   - **Progress**: Well-typed programs don't get stuck
   - **Preservation**: Reduction preserves typing

Understanding these concepts is crucial for designing a correct and effective type system.

## Phase 2: Type Inference Engine

Type inference enables a type system to determine types without requiring explicit annotations everywhere. This phase builds the infrastructure for deducing types from context.

### Understanding Type Inference

Type inference is the process of automatically determining the types of expressions based on their usage and context. It makes type systems more convenient by reducing the need for explicit type annotations.

#### Approaches to Type Inference

There are several approaches to type inference, each with different strengths:

1. **Local Type Inference**:
   - Infers types within a limited scope (e.g., a single expression)
   - Faster and simpler, but less powerful
   - Used in languages like C# (with `var`) and TypeScript

2. **Global Type Inference**:
   - Analyzes the entire program to determine types
   - More powerful but more complex and slower
   - Used in languages like Haskell and ML

3. **Bidirectional Type Checking**:
   - Combines "type checking" (from annotations to expressions) and "type synthesis" (from expressions to types)
   - Provides a balance of power and performance
   - Used in languages like Rust and Swift

4. **Constraint-Based Inference**:
   - Generates constraints about type relationships then solves them
   - Handles complex type relationships and polymorphism
   - Used in languages like Haskell, OCaml, and Rust

For Jac, we'll use a combination of bidirectional type checking and constraint-based inference to balance power and performance.

### Implementation Steps

1. **Implement constraint-based inference**:

   - **`InferenceContext` for tracking type assignments**:
     ```python
     class TypeVariable:
         """Represents a yet-to-be-determined type."""
         def __init__(self, name: str):
             self.name = name

     class InferenceContext:
         """Tracks type variables and constraints during inference."""
         def __init__(self, type_registry: TypeRegistry):
             self.type_registry = type_registry
             self.type_variables = {}  # name -> TypeVariable
             self.constraints = []  # list of Constraint objects
             self.solutions = {}  # TypeVariable -> Type

         def fresh_type_var(self, prefix: str = "T") -> TypeVariable:
             """Create a new type variable with a unique name."""
             name = f"{prefix}_{len(self.type_variables)}"
             var = TypeVariable(name)
             self.type_variables[name] = var
             return var

         def add_constraint(self, constraint: 'Constraint'):
             """Add a type constraint to be solved."""
             self.constraints.append(constraint)

         def solve(self) -> bool:
             """Attempt to solve all constraints and determine concrete types."""
             # Constraint solving algorithm goes here
             # Returns True if successful, False if constraints cannot be satisfied
             return True

         def substitute(self, type_: Type) -> Type:
             """Substitute solved type variables with their concrete types."""
             if isinstance(type_, TypeVariable):
                 if type_.name in self.solutions:
                     return self.solutions[type_.name]
                 return type_
             elif isinstance(type_, FunctionType):
                 params = [self.substitute(param) for param in type_.param_types]
                 return_type = self.substitute(type_.return_type)
                 return FunctionType(type_.name, params, return_type)
             # Handle other type kinds
             return type_
     ```

   - **Type constraints and constraint solving**:
     ```python
     class Constraint:
         """Base class for type constraints."""
         pass

     class SubtypeConstraint(Constraint):
         """Constraint that one type is a subtype of another."""
         def __init__(self, sub: Type, sup: Type):
             self.sub = sub
             self.sup = sup

         def solve(self, context: InferenceContext) -> bool:
             """Check if this constraint can be satisfied."""
             sub = context.substitute(self.sub)
             sup = context.substitute(self.sup)

             # If both are concrete types, just check subtyping
             if not isinstance(sub, TypeVariable) and not isinstance(sup, TypeVariable):
                 return is_subtype(sub, sup)

             # If sub is a type variable, it must be a subtype of sup
             if isinstance(sub, TypeVariable):
                 if sub.name in context.solutions:
                     return is_subtype(context.solutions[sub.name], sup)
                 context.solutions[sub.name] = sup
                 return True

             # If sup is a type variable, sub must be a subtype of it
             if isinstance(sup, TypeVariable):
                 if sup.name in context.solutions:
                     return is_subtype(sub, context.solutions[sup.name])
                 context.solutions[sup.name] = sub
                 return True

             return False

     class EqualityConstraint(Constraint):
         """Constraint that two types are equal."""
         def __init__(self, left: Type, right: Type):
             self.left = left
             self.right = right

         def solve(self, context: InferenceContext) -> bool:
             """Check if this constraint can be satisfied."""
             left = context.substitute(self.left)
             right = context.substitute(self.right)

             # If both are concrete types, just check equality
             if not isinstance(left, TypeVariable) and not isinstance(right, TypeVariable):
                 return left == right

             # If left is a type variable, it must equal right
             if isinstance(left, TypeVariable):
                 if left.name in context.solutions:
                     return context.solutions[left.name] == right
                 context.solutions[left.name] = right
                 return True

             # If right is a type variable, it must equal left
             if isinstance(right, TypeVariable):
                 if right.name in context.solutions:
                     return context.solutions[right.name] == left
                 context.solutions[right.name] = left
                 return True

             return False
     ```

   - **Core inference algorithms**:
     ```python
     class TypeInferer:
         """Infers types for expressions in the AST."""
         def __init__(self, type_registry: TypeRegistry):
             self.type_registry = type_registry
             self.inference_context = InferenceContext(type_registry)

         def infer_expr(self, expr: ExprNode, expected_type: Optional[Type] = None) -> Type:
             """Infer the type of an expression."""
             if hasattr(expr, 'inferred_type') and expr.inferred_type:
                 return expr.inferred_type

             # Placeholder for dispatch to specific inference methods
             if isinstance(expr, LiteralExpr):
                 return self.infer_literal(expr)
             elif isinstance(expr, BinaryExpr):
                 return self.infer_binary_expr(expr)
             elif isinstance(expr, CallExpr):
                 return self.infer_call_expr(expr)
             # etc.

             # If we have an expected type, add a constraint
             if expected_type:
                 inferred = self.inference_context.fresh_type_var()
                 self.inference_context.add_constraint(
                     SubtypeConstraint(inferred, expected_type))
                 return inferred

             return self.type_registry.lookup_type("any")  # Default to any type
     ```

2. **Add type inference rules**:

   - **Literal type inference**:
     ```python
     def infer_literal(self, expr: LiteralExpr) -> Type:
         """Infer the type of a literal expression."""
         if isinstance(expr.value, int):
             return self.type_registry.lookup_type("int")
         elif isinstance(expr.value, float):
             return self.type_registry.lookup_type("float")
         elif isinstance(expr.value, str):
             return self.type_registry.lookup_type("str")
         elif isinstance(expr.value, bool):
             return self.type_registry.lookup_type("bool")
         elif expr.value is None:
             return self.type_registry.lookup_type("None")

         # Default case
         return self.type_registry.lookup_type("any")
     ```

   - **Binary operation inference**:
     ```python
     def infer_binary_expr(self, expr: BinaryExpr) -> Type:
         """Infer the type of a binary expression."""
         # Infer operand types
         left_type = self.infer_expr(expr.left)
         right_type = self.infer_expr(expr.right)

         # Handle different operators
         if expr.op in ['+', '-', '*', '/']:
             # Numeric operations
             if is_subtype(left_type, self.type_registry.lookup_type("int")) and \
                is_subtype(right_type, self.type_registry.lookup_type("int")):
                 return self.type_registry.lookup_type("int")
             elif is_subtype(left_type, self.type_registry.lookup_type("float")) or \
                  is_subtype(right_type, self.type_registry.lookup_type("float")):
                 return self.type_registry.lookup_type("float")

         elif expr.op in ['<', '>', '<=', '>=', '==', '!=']:
             # Comparison operations always return bool
             return self.type_registry.lookup_type("bool")

         # Default case
         return self.type_registry.lookup_type("any")
     ```

   - **Function call and attribute access inference**:
     ```python
     def infer_call_expr(self, expr: CallExpr) -> Type:
         """Infer the type of a function call expression."""
         # Infer the function type
         func_type = self.infer_expr(expr.func)

         if isinstance(func_type, FunctionType):
             # Infer argument types and add constraints
             for i, arg in enumerate(expr.args):
                 if i < len(func_type.param_types):
                     arg_type = self.infer_expr(arg, func_type.param_types[i])
                     self.inference_context.add_constraint(
                         SubtypeConstraint(arg_type, func_type.param_types[i]))

             # Return the function's return type
             return func_type.return_type

         # If it's not a function type, default to any
         return self.type_registry.lookup_type("any")

     def infer_attribute_access(self, expr: AttributeExpr) -> Type:
         """Infer the type of an attribute access expression."""
         # Infer the object type
         obj_type = self.infer_expr(expr.obj)

         # Look up the attribute in the object type
         if isinstance(obj_type, ClassType):
             attr = obj_type.get_attribute(expr.attr)
             if attr:
                 return attr.type

         # Default case
         return self.type_registry.lookup_type("any")
     ```

   - **Control flow-based inference**:
     ```python
     def infer_if_expr(self, expr: IfExpr) -> Type:
         """Infer the type of an if expression."""
         # Infer the condition (should be bool)
         cond_type = self.infer_expr(expr.condition)
         self.inference_context.add_constraint(
             SubtypeConstraint(cond_type, self.type_registry.lookup_type("bool")))

         # Infer the branches
         then_type = self.infer_expr(expr.then_expr)
         else_type = self.infer_expr(expr.else_expr)

         # The result type is the common supertype of both branches
         # For simplicity, we'll use a type variable and add constraints
         result_type = self.inference_context.fresh_type_var()
         self.inference_context.add_constraint(SubtypeConstraint(then_type, result_type))
         self.inference_context.add_constraint(SubtypeConstraint(else_type, result_type))

         return result_type
     ```

### Key Concepts in Type Inference

1. **Unification**:
   - The process of finding a substitution that makes two types equal
   - Core component of many type inference algorithms
   - Basic idea: If T1 = T2, then substitute the same concrete type for both

2. **Constraint Generation and Solving**:
   - Generate constraints during traversal of the AST
   - Solve constraints to find concrete types
   - May involve multiple passes over the constraints until a fixed point is reached

3. **Type Variables and Substitution**:
   - Type variables represent unknown types
   - Substitution replaces type variables with concrete types
   - The solution is a mapping from type variables to concrete types

4. **Bidirectional Type Checking**:
   - "Type checking" mode: uses known types to check expressions
   - "Type synthesis" mode: infers types from expressions
   - Switches between modes strategically for optimal inference

Understanding these concepts provides the foundation for implementing a robust type inference system that balances power and performance.

## Phase 3: Type Checking Pipeline

With the core type system and inference engine in place, this phase focuses on integrating type checking into the compiler pipeline. This involves creating dedicated compiler passes and integrating with the existing infrastructure.

### Understanding Compiler Passes for Type Checking

Type checking typically involves multiple passes through the code, each with a specific purpose:

1. **Type Collection**: Gather declarations and build the type registry
2. **Type Resolution**: Resolve type references and build complete type definitions
3. **Type Inference**: Assign types to expressions without explicit annotations
4. **Type Validation**: Verify type compatibility and constraints

Breaking type checking into multiple passes simplifies the implementation and allows for more efficient processing, especially for languages with complex type relationships.

### Compiler Pass Architecture

Compiler passes are organized operations that transform or analyze the code. Each pass:

1. Takes a program representation as input
2. Performs a specific analysis or transformation
3. Updates the program representation or produces diagnostics
4. Passes the updated representation to the next pass

This architecture enables:
- Clear separation of concerns
- Incremental compilation
- Parallel execution of independent passes
- Reusable analysis components

### Implementation Steps

1. **Create the compiler passes**:

   - **`TypeRegistryBuildPass` for collecting types**:
     ```python
     class TypeRegistryBuildPass(CompilerPass):
         """Compiler pass that builds the type registry from declarations."""

         def __init__(self, program: JacProgram):
             super().__init__(program)
             self.type_registry = TypeRegistry()

         def process(self):
             """Process the program to build the type registry."""
             # Visit all modules in the program
             for module in self.program.modules:
                 self.visit_module(module)

             # Store the type registry in the program context
             self.program.context.type_registry = self.type_registry

         def visit_module(self, module: Module):
             """Visit a module to collect type declarations."""
             for node in module.nodes:
                 if isinstance(node, ClassDecl):
                     self.visit_class_decl(node)
                 elif isinstance(node, EnumDecl):
                     self.visit_enum_decl(node)
                 # etc.

         def visit_class_decl(self, node: ClassDecl):
             """Process a class declaration and add it to the type registry."""
             # Create a new class type
             class_type = ClassType(
                 name=node.name,
                 module=node.module_name,
                 bases=[],  # Will be filled in later during resolution
                 is_abstract=node.is_abstract
             )

             # Register the type
             self.type_registry.register_type(class_type)

             # Associate the AST node with the type
             node.defined_type = class_type
     ```

   - **`TypeResolutionPass` for resolving type references**:
     ```python
     class TypeResolutionPass(CompilerPass):
         """Compiler pass that resolves type references."""

         def __init__(self, program: JacProgram):
             super().__init__(program)
             self.type_registry = program.context.type_registry

         def process(self):
             """Process the program to resolve type references."""
             # Visit all modules in the program
             for module in self.program.modules:
                 self.visit_module(module)

         def visit_module(self, module: Module):
             """Visit a module to resolve type references."""
             for node in module.nodes:
                 if isinstance(node, ClassDecl):
                     self.resolve_class_decl(node)
                 # etc.

         def resolve_class_decl(self, node: ClassDecl):
             """Resolve type references in a class declaration."""
             class_type = node.defined_type

             # Resolve base classes
             for base_ref in node.bases:
                 base_type = self.resolve_type_reference(base_ref)
                 if base_type and isinstance(base_type, ClassType):
                     class_type.bases.append(base_type)
                 else:
                     self.program.diagnostics.report_error(
                         f"Base class '{base_ref}' is not a valid class type",
                         node.location
                     )

             # Resolve member types
             for member in node.members:
                 if isinstance(member, FieldDecl) and member.type_annotation:
                     field_type = self.resolve_type_reference(member.type_annotation)
                     if field_type:
                         class_type.add_instance_attribute(member.name, field_type)
                     else:
                         self.program.diagnostics.report_error(
                             f"Unknown type '{member.type_annotation}' for field '{member.name}'",
                             member.location
                         )
                 # Handle methods, properties, etc.

         def resolve_type_reference(self, type_ref) -> Optional[Type]:
             """Resolve a type reference to a concrete type."""
             if isinstance(type_ref, str):
                 return self.type_registry.lookup_type(type_ref)
             elif isinstance(type_ref, TypeReference):
                 # Handle qualified names, generics, etc.
                 pass
             return None
     ```

   - **`TypeInferencePass` for assigning types**:
     ```python
     class TypeInferencePass(CompilerPass):
         """Compiler pass that infers types for expressions."""

         def __init__(self, program: JacProgram):
             super().__init__(program)
             self.type_registry = program.context.type_registry
             self.inferer = TypeInferer(self.type_registry)

         def process(self):
             """Process the program to infer types."""
             # Visit all modules in the program
             for module in self.program.modules:
                 self.visit_module(module)

         def visit_module(self, module: Module):
             """Visit a module to infer types for expressions."""
             for node in module.nodes:
                 self.visit_node(node)

         def visit_node(self, node):
             """Visit a node and its children to infer types."""
             # Dispatch based on node type
             if isinstance(node, FunctionDecl):
                 self.visit_function(node)
             elif isinstance(node, ClassDecl):
                 self.visit_class(node)
             # etc.

         def visit_function(self, node: FunctionDecl):
             """Infer types for expressions in a function."""
             # Create a new inference context for this function
             self.inferer.new_context()

             # Visit the function body
             if node.body:
                 for stmt in node.body:
                     self.visit_stmt(stmt)

             # Solve the constraints
             self.inferer.solve_constraints()

         def visit_expr(self, expr: ExprNode):
             """Infer the type of an expression."""
             # Use the inferer to determine the type
             expr.inferred_type = self.inferer.infer_expr(expr)
             return expr.inferred_type
     ```

   - **`TypeCheckPass` for validating compatibility**:
     ```python
     class TypeCheckPass(CompilerPass):
         """Compiler pass that validates type compatibility."""

         def __init__(self, program: JacProgram):
             super().__init__(program)
             self.type_registry = program.context.type_registry

         def process(self):
             """Process the program to validate type compatibility."""
             # Visit all modules in the program
             for module in self.program.modules:
                 self.visit_module(module)

         def visit_module(self, module: Module):
             """Visit a module to check type compatibility."""
             for node in module.nodes:
                 self.visit_node(node)

         def visit_node(self, node):
             """Visit a node and its children to check types."""
             # Dispatch based on node type
             if isinstance(node, FunctionDecl):
                 self.check_function(node)
             elif isinstance(node, ClassDecl):
                 self.check_class(node)
             # etc.

         def check_function(self, node: FunctionDecl):
             """Check type compatibility in a function."""
             # Check return type
             if node.return_type and node.body:
                 # Find return statements
                 return_types = self.find_return_types(node.body)
                 expected_type = self.resolve_type_reference(node.return_type)

                 # Check each return value against the declared return type
                 for ret_type, location in return_types:
                     if not is_subtype(ret_type, expected_type):
                         self.program.diagnostics.report_error(
                             f"Return type '{ret_type.name}' is not compatible with declared return type '{expected_type.name}'",
                             location
                         )

             # Check parameter types, variable assignments, etc.
     ```

2. **Integrate with the existing compiler infrastructure**:

   - **Update the CompilerMode enum**:
     ```python
     class CompilerMode(Enum):
         """Enum for different compiler modes."""
         PARSE_ONLY = 1
         SYMBOL_RESOLUTION = 2
         TYPE_CHECK = 3  # New mode for type checking
         CODE_GEN = 4
     ```

   - **Modify scheduling in JacProgram**:
     ```python
     def compile(self, mode: CompilerMode = CompilerMode.CODE_GEN):
         """Compile the program to the specified stage."""
         # Run parsing passes
         self.run_parsing_passes()

         if mode == CompilerMode.PARSE_ONLY:
             return

         # Run symbol resolution passes
         self.run_symbol_resolution_passes()

         if mode == CompilerMode.SYMBOL_RESOLUTION:
             return

         # Run type checking passes (new)
         if mode >= CompilerMode.TYPE_CHECK:
             self.run_type_checking_passes()

         if mode == CompilerMode.TYPE_CHECK:
             return

         # Run code generation passes
         self.run_code_generation_passes()

     def run_type_checking_passes(self):
         """Run the type checking passes."""
         # Build the type registry
         type_registry_pass = TypeRegistryBuildPass(self)
         type_registry_pass.process()

         # Resolve type references
         type_resolution_pass = TypeResolutionPass(self)
         type_resolution_pass.process()

         # Infer types
         type_inference_pass = TypeInferencePass(self)
         type_inference_pass.process()

         # Check type compatibility
         type_check_pass = TypeCheckPass(self)
         type_check_pass.process()
     ```

   - **Add configuration options**:
     ```python
     class TypeCheckingOptions:
         """Configuration options for type checking."""

         def __init__(self):
             self.strict_mode = False  # Stricter type checking
             self.ignore_missing_imports = False  # Ignore missing imports
             self.allow_implicit_any = True  # Allow variables without type annotations
             self.check_unused_vars = True  # Check for unused variables
             self.check_null_dereference = True  # Check for potential null dereferences

     class JacProgram:
         def __init__(self, options=None):
             self.options = options or {}
             self.type_checking_options = TypeCheckingOptions()

             # Configure type checking options from program options
             if 'strict' in self.options:
                 self.type_checking_options.strict_mode = self.options['strict']
             # etc.
     ```

### Key Concepts in Compiler Pass Organization

1. **Pass Ordering**:
   - Passes must run in the correct order to ensure dependencies are satisfied
   - Some passes can run in parallel if they don't have dependencies
   - Careful ordering reduces the number of passes needed

2. **Incremental Processing**:
   - Only recompute what's necessary when code changes
   - Cache results between runs when possible
   - Use dependency tracking to determine what needs recomputation

3. **Shared Context**:
   - Passes communicate through a shared program context
   - Each pass may update different aspects of the context
   - Later passes build on information collected by earlier passes

4. **Error Recovery**:
   - Robust passes can continue despite errors
   - Errors in one pass shouldn't prevent running later passes
   - This enables reporting multiple errors at once

Understanding these concepts helps create a more maintainable and efficient type checking pipeline that integrates well with the broader compiler architecture.

## Phase 4: Error Reporting System

Effective error reporting is crucial for the usability of any type checking system. This phase focuses on designing and implementing a comprehensive diagnostic system that provides clear and actionable feedback to developers.

### Understanding Error Reporting for Type Checkers

A good error reporting system goes beyond simply detecting errors; it should:

1. **Clearly identify the problem** - Precisely indicate what is wrong
2. **Explain why it's a problem** - Provide the type checking rule that's violated
3. **Suggest how to fix it** - Give actionable guidance on resolving the issue
4. **Provide context** - Show relevant type information to understand the error
5. **Be educational** - Teach the developer about the type system through errors

Error messages are a key touchpoint between the type system and developers, and well-designed errors can significantly improve language usability and learning curve.

### Principles of Good Error Messages

1. **Locality**: Error messages should be reported where they can be fixed, not just where they're detected
2. **Specificity**: Messages should be specific about the exact type mismatch
3. **Clarity**: Use plain language that explains the issue without compiler jargon
4. **Context**: Include relevant type information to understand why there's a mismatch
5. **Actionability**: Provide clear guidance on how to resolve the issue

### Implementation Steps

1. **Design the diagnostic model**:

   - **`TypeDiagnostic` with severity, message, and location**:
     ```python
     class DiagnosticSeverity(Enum):
         """Severity levels for diagnostics."""
         ERROR = 1  # Prevents compilation
         WARNING = 2  # Suspicious but valid code
         INFO = 3  # Informational message
         HINT = 4  # Suggestions for improvement

     class SourceLocation:
         """Location in source code."""
         def __init__(self, file: str, line: int, column: int):
             self.file = file
             self.line = line
             self.column = column

     class TypeDiagnostic:
         """Diagnostic message from the type checker."""
         def __init__(
             self,
             message: str,
             location: SourceLocation,
             severity: DiagnosticSeverity = DiagnosticSeverity.ERROR,
             code: Optional[str] = None
         ):
             self.message = message
             self.location = location
             self.severity = severity
             self.code = code  # Error code for documentation reference
             self.related_info = []  # Additional context information
             self.suggestions = []  # Potential fixes

         def add_related_info(self, message: str, location: SourceLocation):
             """Add related information to provide context."""
             self.related_info.append((message, location))

         def add_suggestion(self, suggestion: str):
             """Add a suggestion for fixing the issue."""
             self.suggestions.append(suggestion)
     ```

   - **Related information for context**:
     ```python
     class TypeMismatchDiagnostic(TypeDiagnostic):
         """Specialized diagnostic for type mismatches."""
         def __init__(
             self,
             expected_type: Type,
             actual_type: Type,
             location: SourceLocation,
             context: str = ""
         ):
             message = f"Type mismatch: expected '{expected_type.name}', got '{actual_type.name}'"
             if context:
                 message = f"{context}: {message}"

             super().__init__(message, location, DiagnosticSeverity.ERROR, "E1001")

             self.expected_type = expected_type
             self.actual_type = actual_type

             # Add suggestion if there's an obvious conversion
             if has_conversion(actual_type, expected_type):
                 self.add_suggestion(f"Consider using a conversion function: {actual_type.name}_to_{expected_type.name}(...)")
     ```

   - **Suggestions for fixing issues**:
     ```python
     class DiagnosticWithFix:
         """Interface for diagnostics that can provide automated fixes."""

         def get_fix(self) -> Optional['CodeFix']:
             """Get a code fix for this diagnostic, if available."""
             return None

     class CodeFix:
         """Represents a fix for a code issue."""
         def __init__(self, description: str, edits: list['TextEdit']):
             self.description = description
             self.edits = edits

     class TextEdit:
         """Represents a text edit to apply to the source code."""
         def __init__(self, start: SourceLocation, end: SourceLocation, new_text: str):
             self.start = start
             self.end = end
             self.new_text = new_text

     class MissingImportDiagnostic(TypeDiagnostic, DiagnosticWithFix):
         """Diagnostic for a missing import."""
         def __init__(self, type_name: str, module_name: str, location: SourceLocation):
             message = f"Type '{type_name}' is not defined, but exists in module '{module_name}'"
             super().__init__(message, location, DiagnosticSeverity.ERROR, "E1002")
             self.type_name = type_name
             self.module_name = module_name

         def get_fix(self) -> Optional[CodeFix]:
             """Get a fix to add the missing import."""
             # Calculate the position for the new import (typically at the top of the file)
             import_pos = SourceLocation(self.location.file, 1, 0)

             # Create a text edit to add the import statement
             edit = TextEdit(
                 import_pos,
                 import_pos,
                 f"import {self.module_name}.{self.type_name};\n"
             )

             return CodeFix(
                 f"Import '{self.type_name}' from '{self.module_name}'",
                 [edit]
             )
     ```

2. **Implement error reporters**:

   - **Type compatibility error reporting**:
     ```python
     class TypeErrorReporter:
         """Reports type errors during type checking."""

         def __init__(self, program: JacProgram):
             self.program = program
             self.diagnostics = []

         def report_error(self, message: str, location: SourceLocation, code: Optional[str] = None):
             """Report a generic error."""
             diag = TypeDiagnostic(message, location, DiagnosticSeverity.ERROR, code)
             self.diagnostics.append(diag)
             self.program.diagnostics.add(diag)

         def report_type_mismatch(
             self,
             expected_type: Type,
             actual_type: Type,
             location: SourceLocation,
             context: str = ""
         ):
             """Report a type mismatch error."""
             diag = TypeMismatchDiagnostic(expected_type, actual_type, location, context)
             self.diagnostics.append(diag)
             self.program.diagnostics.add(diag)

             # Add related information about why types are incompatible
             if isinstance(expected_type, ClassType) and isinstance(actual_type, ClassType):
                 self.explain_class_incompatibility(diag, expected_type, actual_type)

         def explain_class_incompatibility(
             self,
             diag: TypeMismatchDiagnostic,
             expected: ClassType,
             actual: ClassType
         ):
             """Add explanations about why classes are incompatible."""
             # Check if actual is a subclass of expected
             if not any(base.name == expected.name for base in get_all_bases(actual)):
                 diag.add_related_info(
                     f"Class '{actual.name}' is not a subclass of '{expected.name}'",
                     diag.location
                 )

                 # Suggest implementing the expected interface
                 diag.add_suggestion(
                     f"Make '{actual.name}' implement or extend '{expected.name}'"
                 )

             # Check for structural compatibility (missing methods)
             for method_name, method in expected.get_methods().items():
                 if method_name not in actual.get_methods():
                     diag.add_related_info(
                         f"Class '{actual.name}' is missing method '{method_name}'",
                         diag.location
                     )

                     # Suggest adding the missing method
                     diag.add_suggestion(
                         f"Add method '{method_name}' to class '{actual.name}'"
                     )
     ```

   - **Symbol resolution error reporting**:
     ```python
     def report_unknown_symbol(self, symbol_name: str, location: SourceLocation):
         """Report an error for an unknown symbol."""
         # Basic error
         message = f"Cannot find symbol '{symbol_name}'"
         diag = TypeDiagnostic(message, location, DiagnosticSeverity.ERROR, "E1003")

         # Add context: check for similar names (potential typos)
         similar_names = self.find_similar_symbols(symbol_name)
         if similar_names:
             names_str = ", ".join(f"'{name}'" for name in similar_names[:3])
             diag.add_related_info(
                 f"Did you mean one of these: {names_str}?",
                 location
             )

             # Add fix suggestions for the most likely typo
             if len(similar_names) > 0:
                 diag.add_suggestion(f"Change '{symbol_name}' to '{similar_names[0]}'")

         # Check if it exists in another module
         external_module = self.find_external_module_with_symbol(symbol_name)
         if external_module:
             diag.add_related_info(
                 f"Symbol '{symbol_name}' exists in module '{external_module}'",
                 location
             )
             diag.add_suggestion(f"Add import for '{symbol_name}' from '{external_module}'")

         self.diagnostics.append(diag)
         self.program.diagnostics.add(diag)

     def find_similar_symbols(self, name: str) -> list[str]:
         """Find symbols with similar names (potential typos)."""
         # Simple implementation using Levenshtein distance
         all_symbols = self.collect_visible_symbols()
         return sorted(
             [sym for sym in all_symbols if levenshtein_distance(name, sym) <= 2],
             key=lambda s: levenshtein_distance(name, s)
         )
     ```

   - **Special case handlers for common mistakes**:
     ```python
     def report_property_access_on_nullable(self, obj_expr, property_name: str, location: SourceLocation):
         """Report an error for accessing a property on a potentially null object."""
         obj_type = obj_expr.inferred_type

         message = f"Property '{property_name}' accessed on potentially null value of type '{obj_type.name}'"
         diag = TypeDiagnostic(message, location, DiagnosticSeverity.ERROR, "E1004")

         # Add context about why the object might be null
         if hasattr(obj_expr, 'nullable_reason'):
             diag.add_related_info(
                 obj_expr.nullable_reason,
                 obj_expr.location
             )

         # Suggest using a null check
         diag.add_suggestion(
             f"Add a null check: if ({obj_expr.source_text} != null) {{ ... }}"
         )

         # Suggest using the null-safe operator if available in the language
         diag.add_suggestion(
             f"Use the null-safe operator: {obj_expr.source_text}?.{property_name}"
         )

         self.diagnostics.append(diag)
         self.program.diagnostics.add(diag)
     ```

### Key Concepts in Error Reporting

1. **Layered Diagnostics**:
   - **Primary message**: The main error description
   - **Related information**: Additional context about why there's an error
   - **Suggestions**: Potential ways to fix the issue

2. **Error Categorization**:
   - Organize errors by category (type mismatch, undeclared variable, etc.)
   - Assign error codes for reference and documentation
   - Group related errors to avoid cascading error reports

3. **Contextual Information**:
   - Include relevant type information in error messages
   - Show the expected vs. actual types
   - Explain subtyping relationships when relevant

4. **Automated Fixes**:
   - Provide specific, actionable fixes where possible
   - Enable IDE quick-fix functionality
   - Focus on common errors with straightforward solutions

5. **User-Centered Design**:
   - Write error messages for developers, not compiler engineers
   - Avoid compiler jargon and technical details when possible
   - Present errors in the context of the developer's code and goals

Understanding these concepts helps create a diagnostic system that not only identifies errors but also provides meaningful guidance to help developers understand and resolve type issues efficiently.

## Phase 5: Jac-Specific Features

After implementing the core type checking infrastructure, this phase focuses on extending the system to support Jac's unique language features, particularly those related to graph-oriented programming.

### Understanding Domain-Specific Type Checking

Many programming languages include domain-specific features designed for their target problem domains. Adding type checking for these specialized features presents unique challenges:

1. **Semantic Gap**: There's often a semantic gap between general-purpose type systems and domain-specific concepts
2. **Custom Rules**: Domain-specific features may require custom type checking rules that don't fit standard patterns
3. **Specialized Types**: New domain-specific types may need to be integrated with the core type system
4. **Context Sensitivity**: Domain features may have context-dependent typing behavior
5. **Special Syntax**: Custom syntax may require specialized type checking approaches

For Jac, the domain-specific features revolve around graph-oriented programming, including node and edge types, graph traversals, and walkers (agents that navigate the graph).

### Approaches to Integrating Domain Features

There are several strategies for integrating domain-specific features into a type system:

1. **Extension**: Extend the base type system with new type kinds
2. **Specialization**: Create domain-specific subtypes of existing types
3. **Context Tracking**: Add context-sensitive information to type checking
4. **Special Rules**: Implement custom type checking rules for domain operations
5. **Type-Level Semantics**: Encode domain semantics into the type system

For Jac, we'll use a combination of these approaches, with a focus on extending the type system with graph-specific types and adding specialized type checking rules for graph operations.

### Implementation Steps

1. **Add support for Jac-specific types**:

   - **Node and edge architypes**:
     ```python
     class NodeType(ClassType):
         """Type representing a node architype."""

         def __init__(self, name: str, module: str = "", bases: list[ClassType] = None, is_abstract: bool = False):
             super().__init__(name, module, bases, is_abstract)
             self.edge_connections = {}  # Maps edge names to EdgeType objects

         def add_edge_connection(self, edge_name: str, edge_type: 'EdgeType'):
             """Register a connection to an edge type."""
             self.edge_connections[edge_name] = edge_type

         def get_edge_types(self) -> list['EdgeType']:
             """Get all edge types this node can connect to."""
             return list(self.edge_connections.values())

         def can_connect_to(self, edge_type: 'EdgeType') -> bool:
             """Check if this node can connect to the given edge type."""
             return any(edge.name == edge_type.name for edge in self.get_edge_types())

     class EdgeType(ClassType):
         """Type representing an edge architype."""

         def __init__(
             self,
             name: str,
             module: str = "",
             bases: list[ClassType] = None,
             is_abstract: bool = False,
             source_type: Optional[NodeType] = None,
             target_type: Optional[NodeType] = None,
             is_directed: bool = True
         ):
             super().__init__(name, module, bases, is_abstract)
             self.source_type = source_type
             self.target_type = target_type
             self.is_directed = is_directed

         def can_connect(self, source: NodeType, target: NodeType) -> bool:
             """Check if this edge can connect the given node types."""
             if not self.source_type or not self.target_type:
                 return True  # Unspecified connection types allow any nodes

             source_ok = is_subtype(source, self.source_type)
             target_ok = is_subtype(target, self.target_type)

             if self.is_directed:
                 return source_ok and target_ok
             else:
                 # For undirected edges, either direction works
                 return (source_ok and target_ok) or (is_subtype(source, self.target_type) and is_subtype(target, self.source_type))
     ```

   - **Graph traversal operations**:
     ```python
     class TraversalType(Type):
         """Type representing a graph traversal result."""

         def __init__(self, node_type: NodeType, edge_type: Optional[EdgeType] = None, is_collection: bool = True):
             name = f"Traversal<{node_type.name}>"
             if edge_type:
                 name += f" via {edge_type.name}"
             if is_collection:
                 name = f"List<{name}>"

             super().__init__(name)
             self.node_type = node_type
             self.edge_type = edge_type
             self.is_collection = is_collection

         def get_node_type(self) -> NodeType:
             """Get the type of nodes in this traversal."""
             return self.node_type

         def with_filter(self, filter_type: Optional[Type] = None) -> 'TraversalType':
             """Apply a filter to this traversal."""
             if not filter_type:
                 return self

             if isinstance(filter_type, EdgeType):
                 # Filter by edge type, return the target node type
                 if filter_type.target_type:
                     return TraversalType(filter_type.target_type, filter_type, self.is_collection)

             # Default case: same type with filter
             return self
     ```

   - **Walker types**:
     ```python
     class WalkerType(ClassType):
         """Type representing a walker (graph traversal agent)."""

         def __init__(
             self,
             name: str,
             module: str = "",
             bases: list[ClassType] = None,
             is_abstract: bool = False
         ):
             super().__init__(name, module, bases, is_abstract)
             self.current_type = None  # The current node type (context-sensitive)

         def with_current(self, node_type: NodeType) -> 'WalkerType':
             """Create a new walker type with the specified current node type."""
             result = WalkerType(self.name, self.module, self.bases, self.is_abstract)
             result.current_type = node_type

             # Copy attributes from this walker
             for name, attr in self.instance_attrs.items():
                 result.instance_attrs[name] = attr

             return result

         def can_visit(self, node_type: NodeType) -> bool:
             """Check if this walker can visit the given node type."""
             # Walkers can visit any node by default
             # This can be specialized based on visit constraints
             return True
     ```

2. **Implement special constructors**:

   - **Connect operator typing**:
     ```python
     def check_connect_op(self, expr: ConnectExpr) -> Type:
         """Type check a connection operation."""
         # Get the types of nodes being connected
         source_type = self.check_expr(expr.source)
         target_type = self.check_expr(expr.target)

         # Check that both are node types
         if not isinstance(source_type, NodeType):
             self.error_reporter.report_error(
                 f"Source must be a node type, got '{source_type.name}'",
                 expr.source.location
             )

         if not isinstance(target_type, NodeType):
             self.error_reporter.report_error(
                 f"Target must be a node type, got '{target_type.name}'",
                 expr.target.location
             )

         # If an edge type is specified, check if it can connect these nodes
         if expr.edge_type:
             edge_type = self.resolve_type(expr.edge_type)
             if isinstance(edge_type, EdgeType):
                 if isinstance(source_type, NodeType) and isinstance(target_type, NodeType):
                     if not edge_type.can_connect(source_type, target_type):
                         self.error_reporter.report_error(
                             f"Edge type '{edge_type.name}' cannot connect '{source_type.name}' to '{target_type.name}'",
                             expr.location
                         )
                 return edge_type
             else:
                 self.error_reporter.report_error(
                     f"Expected edge type, got '{edge_type.name}'",
                     expr.edge_type.location
                 )

         # Default to a generic edge type
         return self.type_registry.lookup_base_type("Edge")
     ```

   - **Visit statement analysis**:
     ```python
     def check_visit_stmt(self, stmt: VisitStmt) -> None:
         """Type check a visit statement."""
         # The walker type comes from the current context
         walker_type = self.current_type
         if not isinstance(walker_type, WalkerType):
             self.error_reporter.report_error(
                 "Visit statement can only be used in a walker context",
                 stmt.location
             )
             return

         # Check the visited node expression
         target_type = self.check_expr(stmt.target)

         # Handle both single nodes and collections
         node_type = None
         if isinstance(target_type, NodeType):
             node_type = target_type
         elif isinstance(target_type, ListType) and isinstance(target_type.element_type, NodeType):
             node_type = target_type.element_type
         elif isinstance(target_type, TraversalType):
             node_type = target_type.get_node_type()
         else:
             self.error_reporter.report_error(
                 f"Visit target must be a node or traversal result, got '{target_type.name}'",
                 stmt.target.location
             )
             return

         # Check if the walker can visit this node type
         if not walker_type.can_visit(node_type):
             self.error_reporter.report_error(
                 f"Walker '{walker_type.name}' cannot visit node type '{node_type.name}'",
                 stmt.location
             )

         # Update the walker's current type context
         updated_walker = walker_type.with_current(node_type)

         # Create a new scope for the visit body with the updated walker type
         self.enter_scope(updated_walker)

         # Check the visit body
         for body_stmt in stmt.body:
             self.check_stmt(body_stmt)

         self.exit_scope()
     ```

   - **Special ability features**:
     ```python
     class AbilityType(FunctionType):
         """Type representing an ability (a special method in Jac)."""

         def __init__(
             self,
             name: str,
             param_types: list[Type],
             return_type: Type,
             node_context: Optional[NodeType] = None,
             is_static: bool = False
         ):
             super().__init__(name, param_types, return_type, is_static)
             self.node_context = node_context  # The node type this ability operates on

         def requires_context(self) -> bool:
             """Check if this ability requires a node context."""
             return self.node_context is not None

         def with_context(self, node_type: NodeType) -> 'AbilityType':
             """Create a new ability type with the specified node context."""
             return AbilityType(
                 self.name,
                 self.param_types,
                 self.return_type,
                 node_type,
                 self.is_static
             )

     def check_ability_call(self, expr: AbilityCallExpr) -> Type:
         """Type check an ability call."""
         # Get the ability type
         ability_type = self.check_expr(expr.ability)

         if not isinstance(ability_type, AbilityType):
             self.error_reporter.report_error(
                 f"Expected an ability, got '{ability_type.name}'",
                 expr.ability.location
             )
             return self.type_registry.lookup_base_type("any")

         # Check if a context is required
         if ability_type.requires_context():
             # Get the current context from walker or node
             context_type = self.get_current_node_context()
             if not context_type:
                 self.error_reporter.report_error(
                     f"Ability '{ability_type.name}' requires a node context",
                     expr.location
                 )
             elif not is_subtype(context_type, ability_type.node_context):
                 self.error_reporter.report_error(
                     f"Ability '{ability_type.name}' requires node type '{ability_type.node_context.name}', but is called with '{context_type.name}'",
                     expr.location
                 )

         # Check arguments
         self.check_function_args(expr.args, ability_type)

         # Return the ability's return type
         return ability_type.return_type
     ```

### Key Concepts in Type Checking for Domain-Specific Features

1. **Type Extensions vs. Library Types**:

   There are two main approaches to support domain-specific features:

   - **Native Type Extensions**: Add new type kinds directly to the type system
   - **Library Types**: Implement domain features as library types

   Jac uses native type extensions for core graph concepts (nodes, edges, walkers) to provide deeper integration and better error messages.

2. **Context-Sensitive Type Checking**:

   Walkers in Jac demonstrate context-sensitive typing, where:

   - The type information changes based on the execution context (current node)
   - Type checking must track and update this context information
   - Different rules apply in different contexts

3. **Domain-Specific Constraints**:

   Graph operations have domain-specific constraints:

   - Edges can only connect compatible node types
   - Traversals must follow valid edge connections
   - Certain operations are only valid in specific contexts

4. **Balancing Static and Dynamic Typing**:

   When type checking domain-specific features, balance:

   - **Static Safety**: Catch as many errors as possible at compile time
   - **Dynamic Flexibility**: Allow runtime dynamism where it adds value
   - **Gradual Typing**: Support both typed and untyped code

5. **Specialized Error Messages**:

   Domain-specific features need specialized error messages:

   - Use domain terminology (nodes, edges, traversals)
   - Explain domain-specific constraints
   - Suggest solutions in domain-specific terms

Understanding these concepts helps create a type system that supports domain-specific features while maintaining type safety and usability.

## Phase 6: External Integration

The final phase focuses on making the type checking system available to external tools and users. This involves creating multiple interfaces to the type checking system.

### Understanding External Integration for Type Checkers

A type checker provides the most value when it's integrated throughout the development workflow. This requires creating interfaces for different use cases:

1. **IDE Integration**: Real-time feedback while coding
2. **Command-Line Tools**: CI/CD pipeline integration
3. **Programmatic API**: Integration with other tools and frameworks

Each integration point exposes the type checker's capabilities in different ways, optimized for specific use cases.

### Implementation Steps

1. **Build the Language Server Protocol implementation**:

   The Language Server Protocol (LSP) provides a standardized way for editors and IDEs to communicate with language tools like type checkers.

   ```python
   class JacLanguageServer:
       """Language server implementation for Jac."""

       def __init__(self):
           self.workspace = None
           self.documents = {}
           self.type_checker = None

       async def initialize(self, params):
           """Initialize the language server."""
           root_path = params["rootUri"]
           self.workspace = root_path

           # Initialize the type checker
           self.program = JacProgram()
           self.program.load_workspace(root_path)
           self.type_checker = TypeChecker(self.program)

           # Return server capabilities
           return {
               "capabilities": {
                   "textDocumentSync": {
                       "openClose": True,
                       "change": 2  # Incremental sync
                   },
                   "hoverProvider": True,
                   "completionProvider": {
                       "triggerCharacters": [".", ":", "["]
                   },
                   "definitionProvider": True,
                   "referencesProvider": True,
                   "diagnosticProvider": {
                       "interFileDependencies": True,
                       "workspaceDiagnostics": True
                   }
               }
           }

       async def text_document_did_change(self, params):
           """Handle document changes."""
           uri = params["textDocument"]["uri"]
           changes = params["contentChanges"]

           # Update document content
           if uri in self.documents:
               self.documents[uri].apply_changes(changes)
           else:
               self.documents[uri] = Document(uri, changes[0]["text"])

           # Trigger incremental type checking
           await self.check_document(uri)

       async def text_document_hover(self, params):
           """Handle hover requests."""
           uri = params["textDocument"]["uri"]
           position = params["position"]

           # Get type information at position
           type_info = self.type_checker.get_type_at_position(uri, position["line"], position["character"])

           if type_info:
               return {
                   "contents": {
                       "kind": "markdown",
                       "value": f"```jac\n{type_info}\n```"
                   }
               }

           return None
   ```

2. **Create command-line interface**:

   A command-line interface allows running the type checker from scripts, build systems, and CI/CD pipelines.

   ```python
   class TypeCheckCommand:
       """Command-line interface for type checking."""

       def __init__(self):
           self.program = None
           self.type_checker = None

       def parse_args(self):
           """Parse command-line arguments."""
           parser = argparse.ArgumentParser(description="Jac Type Checker")
           parser.add_argument("files", nargs="+", help="Files or directories to check")
           parser.add_argument("--strict", action="store_true", help="Enable strict mode")
           parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
           return parser.parse_args()

       def run(self):
           """Run the command."""
           args = self.parse_args()

           # Initialize the program and type checker
           self.program = JacProgram()
           self.program.options["strict"] = args.strict

           # Load files or directories
           for path in args.files:
               if os.path.isdir(path):
                   self.program.load_directory(path)
               else:
                   self.program.load_file(path)

           # Run type checking
           self.type_checker = TypeChecker(self.program)
           success = self.type_checker.check_all()

           # Output results
           if args.format == "json":
               self.output_json()
           else:
               self.output_text()

           # Exit with appropriate code
           sys.exit(0 if success else 1)

       def output_text(self):
           """Output diagnostics in text format."""
           for file_path, diagnostics in self.program.diagnostics.items():
               if diagnostics:
                   print(f"\nFile: {file_path}")
                   for diag in diagnostics:
                       print(f"  Line {diag.location.line}, Column {diag.location.column}: {diag.message}")

       def output_json(self):
           """Output diagnostics in JSON format."""
           result = []
           for file_path, diagnostics in self.program.diagnostics.items():
               for diag in diagnostics:
                   result.append({
                       "file": file_path,
                       "line": diag.location.line,
                       "column": diag.location.column,
                       "severity": diag.severity.name,
                       "message": diag.message,
                       "code": diag.code
                   })
           print(json.dumps(result, indent=2))
   ```

3. **Expose Python API**:

   A Python API allows programmatic access to the type checker for testing, custom tools, and integration with other frameworks.

   ```python
   class TypeCheckAPI:
       """Public API for the type checker."""

       def __init__(self, options=None):
           self.options = options or {}
           self.program = JacProgram(self.options)
           self.type_checker = None

       def load_file(self, file_path: str) -> bool:
           """Load a single file for type checking."""
           return self.program.load_file(file_path)

       def load_directory(self, dir_path: str) -> bool:
           """Load all Jac files in a directory for type checking."""
           return self.program.load_directory(dir_path)

       def load_code(self, code: str, file_name: str = "<string>") -> bool:
           """Load code from a string for type checking."""
           return self.program.load_code(code, file_name)

       def check_all(self) -> bool:
           """Run type checking on all loaded files."""
           self.type_checker = TypeChecker(self.program)
           return self.type_checker.check_all()

       def get_diagnostics(self) -> dict:
           """Get all diagnostics from the type checker."""
           return self.program.diagnostics

       def get_type_at_position(self, file_path: str, line: int, column: int) -> Optional[str]:
           """Get the type of the expression at the given position."""
           if not self.type_checker:
               self.type_checker = TypeChecker(self.program)

           return self.type_checker.get_type_at_position(file_path, line, column)
   ```

### Integration Patterns and Best Practices

When creating external integrations for a type checker, consider these patterns and practices:

1. **Common Core, Multiple Interfaces**:
   - Share the same core type checking logic across all interfaces
   - Adapt the input/output formats for each interface
   - Maintain consistent behavior across interfaces

2. **Incremental Processing**:
   - For IDE integration, perform incremental analysis when files change
   - Reuse type information for unchanged files
   - Prioritize responsive feedback over completeness

3. **Error Recovery**:
   - Continue type checking despite errors
   - Provide useful information even for incomplete or incorrect code
   - Handle syntax errors gracefully

4. **Performance Optimization**:
   - Profile and optimize hotspots in the type checking process
   - Use caching to avoid redundant computation
   - Consider parallel processing for large codebases

5. **Configuration Options**:
   - Provide consistent configuration across all interfaces
   - Support both file-based and command-line configuration
   - Include sensible defaults for common use cases

By following these patterns, you can create a type checking system that integrates seamlessly into different workflows and tools.

## Testing Strategy

Testing a type checker requires a comprehensive approach that verifies both correctness and usability. This section outlines strategies for testing each aspect of the type checking system.

### Principles of Testing Type Checkers

Testing a type checker presents unique challenges:

1. **Correctness**: The type checker must correctly implement the language's type rules
2. **Completeness**: All language features must be covered
3. **Error Quality**: Error messages must be clear and actionable
4. **Performance**: Type checking must be efficient enough for real-time use
5. **Robustness**: The type checker should handle incomplete or incorrect code gracefully

A comprehensive testing strategy addresses all these aspects.

### Testing Approaches

1. **Unit Tests**:

   Unit tests focus on testing individual components in isolation. For a type checker, this includes:

   - **Type representation tests**:
     ```python
     def test_subtype_relationship():
         """Test subtyping relationships between types."""
         int_type = IntType()
         float_type = FloatType()
         number_type = NumberType()  # Base class for numeric types

         # Test basic subtyping
         assert is_subtype(int_type, int_type)  # Reflexivity
         assert is_subtype(int_type, number_type)  # Inheritance
         assert is_subtype(float_type, number_type)  # Inheritance

         # Test transitivity
         assert not is_subtype(number_type, int_type)  # Supertype is not a subtype
         assert not is_subtype(int_type, float_type)  # No relationship

         # Test function subtyping (contravariance in parameters, covariance in return)
         func1 = FunctionType([number_type], int_type)
         func2 = FunctionType([int_type], number_type)

         assert is_subtype(func2, func1)  # Contravariant parameters, covariant return
         assert not is_subtype(func1, func2)  # Not a subtype
     ```

   - **Type compatibility rules**:
     ```python
     def test_assignment_compatibility():
         """Test compatibility rules for assignments."""
         int_type = IntType()
         float_type = FloatType()
         string_type = StringType()

         # Test compatible assignments
         assert is_assignment_compatible(int_type, int_type)  # Same type
         assert is_assignment_compatible(int_type, float_type)  # Widening conversion

         # Test incompatible assignments
         assert not is_assignment_compatible(string_type, int_type)  # Different types
         assert not is_assignment_compatible(float_type, int_type)  # No implicit narrowing
     ```

   - **Inference logic**:
     ```python
     def test_literal_inference():
         """Test type inference for literals."""
         inferer = TypeInferer(TypeRegistry())

         # Create literal nodes
         int_literal = LiteralNode(42)
         float_literal = LiteralNode(3.14)
         string_literal = LiteralNode("hello")

         # Test inference
         assert isinstance(inferer.infer_expr(int_literal), IntType)
         assert isinstance(inferer.infer_expr(float_literal), FloatType)
         assert isinstance(inferer.infer_expr(string_literal), StringType)
     ```

2. **Integration Tests**:

   Integration tests verify that components work together correctly. For a type checker, this includes:

   - **Compiler pass integration**:
     ```python
     def test_type_checking_pipeline():
         """Test the complete type checking pipeline."""
         program = JacProgram()
         program.load_code("""
             node Person {
                 has name: str;
                 has age: int;
             }

             edge Friendship {
                 has since: int;
             }
         """)

         # Run the type checking passes
         type_registry_pass = TypeRegistryBuildPass(program)
         type_registry_pass.process()

         type_resolution_pass = TypeResolutionPass(program)
         type_resolution_pass.process()

         # Verify types were correctly processed
         type_registry = program.context.type_registry
         assert "Person" in type_registry.types
         assert "Friendship" in type_registry.types

         person_type = type_registry.types["Person"]
         assert isinstance(person_type, NodeType)
         assert "name" in person_type.instance_attrs
         assert isinstance(person_type.instance_attrs["name"].type, StringType)
     ```

   - **Pipeline correctness**:
     ```python
     def test_incremental_type_checking():
         """Test incremental type checking when files change."""
         program = JacProgram()
         program.load_code("let x: int = 42;", "file1.jac")

         # Initial type check
         type_checker = TypeChecker(program)
         type_checker.check_all()
         assert len(program.diagnostics.get("file1.jac", [])) == 0

         # Modify the file with an error
         program.load_code("let x: int = \"hello\";", "file1.jac")

         # Incremental type check
         type_checker.check_file("file1.jac")
         diagnostics = program.diagnostics.get("file1.jac", [])
         assert len(diagnostics) == 1
         assert "Type mismatch" in diagnostics[0].message
     ```

   - **Error reporting accuracy**:
     ```python
     def test_error_reporting():
         """Test that errors are reported accurately."""
         program = JacProgram()
         program.load_code("""
             node Person {
                 has name: str;
             }

             edge Friendship {
                 has since: int;
             }

             walker CreateRelationship {
                 can create_friendship(p1: Person, p2: Person, year: int) {
                     p1 -[Friendship(since=year)]-> p2;
                 }

                 can create_wrong(p1: Person, p2: int) {
                     p1 -[Friendship]-> p2;  # Error: p2 is not a Person
                 }
             }
         """)

         # Run type checking
         type_checker = TypeChecker(program)
         type_checker.check_all()

         # Check for errors
         diagnostics = program.diagnostics.get_all()

         # Find the error for the incorrect connection
         connection_error = None
         for diag in diagnostics:
             if "cannot connect" in diag.message:
                 connection_error = diag
                 break

         assert connection_error is not None
         assert "Person" in connection_error.message
         assert "int" in connection_error.message
     ```

3. **End-to-End Tests**:

   End-to-end tests verify the type checker works correctly on real code. This includes:

   - **Real program testing**:
     ```python
     def test_real_jac_program():
         """Test type checking a real Jac program with multiple files."""
         program = JacProgram()
         program.load_directory("examples/social_network")

         # Run type checking
         type_checker = TypeChecker(program)
         type_checker.check_all()

         # Verify no unexpected errors
         diagnostics = program.diagnostics.get_all()
         unexpected_errors = [d for d in diagnostics if d.severity == DiagnosticSeverity.ERROR and "expected_error" not in d.code]

         assert len(unexpected_errors) == 0, f"Unexpected errors: {unexpected_errors}"
     ```

   - **IDE integration**:
     ```python
     def test_language_server():
         """Test the language server protocol implementation."""
         server = JacLanguageServer()

         # Initialize the server
         init_params = {"rootUri": "file:///test/workspace"}
         init_result = server.initialize(init_params)

         # Verify capabilities
         assert "capabilities" in init_result
         assert "hoverProvider" in init_result["capabilities"]
         assert init_result["capabilities"]["hoverProvider"] is True

         # Open a document
         server.text_document_did_open({
             "textDocument": {
                 "uri": "file:///test/workspace/test.jac",
                 "languageId": "jac",
                 "version": 1,
                 "text": "node Person { has name: str; }"
             }
         })

         # Request hover information
         hover_params = {
             "textDocument": {"uri": "file:///test/workspace/test.jac"},
             "position": {"line": 0, "character": 6}  # Position at "Person"
         }
         hover_result = server.text_document_hover(hover_params)

         assert hover_result is not None
         assert "contents" in hover_result
         assert "node Person" in hover_result["contents"]["value"]
     ```

   - **Performance benchmarks**:
     ```python
     def benchmark_type_checking():
         """Benchmark type checking performance."""
         program = JacProgram()
         program.load_directory("examples/large_project")

         # Measure time to run type checking
         start_time = time.time()
         type_checker = TypeChecker(program)
         type_checker.check_all()
         end_time = time.time()

         # Calculate metrics
         elapsed_time = end_time - start_time
         file_count = len(program.files)
         loc_count = sum(file.line_count for file in program.files.values())

         print(f"Type checked {file_count} files ({loc_count} lines) in {elapsed_time:.2f} seconds")
         print(f"Average: {loc_count / elapsed_time:.2f} lines per second")

         # Assert performance meets requirements
         assert elapsed_time < loc_count * 0.01, "Type checking is too slow"
     ```

### Best Practices for Testing Type Checkers

1. **Test Positive and Negative Cases**:
   - Test that valid code passes type checking
   - Test that invalid code produces appropriate errors
   - Test edge cases and corner cases

2. **Test Incremental Changes**:
   - Verify that incremental type checking works correctly
   - Test adding, modifying, and removing type annotations
   - Test performance with incremental changes

3. **Test Error Messages**:
   - Verify that error messages are clear and actionable
   - Test that error locations are accurate
   - Test that suggested fixes are appropriate

4. **Create a Test Corpus**:
   - Build a collection of test programs
   - Include examples of all language features
   - Add regression tests for fixed bugs

5. **Use Property-Based Testing**:
   - Generate random valid and invalid programs
   - Verify that the type checker correctly accepts or rejects them
   - Test with increasingly complex programs

By following these testing strategies, you can ensure that your type checker is correct, complete, and usable.

## Milestones

Planning a type checker implementation requires breaking the work into manageable milestones. Each milestone represents a significant step toward a complete type checking system.

| Milestone | Description | Estimated Time | Key Deliverables |
|-----------|-------------|----------------|------------------|
| 1 | Core type system implementation | 2 weeks | • Type class hierarchy<br>• Type registry<br>• Subtyping relationships<br>• AST integration |
| 2 | Basic type inference for literals and expressions | 2 weeks | • Inference context<br>• Type variable handling<br>• Constraint generation<br>• Basic inference rules |
| 3 | Full type checking pipeline integration | 3 weeks | • Type registry building pass<br>• Type resolution pass<br>• Type inference pass<br>• Type checking pass |
| 4 | Error reporting and suggestions | 2 weeks | • Diagnostic model<br>• Error reporters<br>• Context information<br>• Fix suggestions |
| 5 | Jac-specific language feature support | 3 weeks | • Node and edge type checking<br>• Graph traversal type checking<br>• Walker type checking<br>• Connection operator checking |
| 6 | External integration (LSP, CLI, API) | 3 weeks | • LSP implementation<br>• Command-line interface<br>• Python API<br>• Editor integration |
| 7 | Testing and refinement | 2 weeks | • Unit tests<br>• Integration tests<br>• Performance testing<br>• Documentation |

### Milestone Progression Strategy

1. **Early Working Prototype**: Focus on getting a minimal end-to-end type checker working early
2. **Incremental Feature Addition**: Add features one by one, ensuring each works before moving on
3. **Continuous Testing**: Add tests as features are implemented
4. **Regular Usability Evaluation**: Get feedback on error messages and usability
5. **Performance Optimization**: Monitor and optimize performance throughout development

This approach ensures steady progress and allows for course correction if needed.

## Challenges and Considerations

Implementing a type checker involves several challenges that need to be addressed:

### 1. Performance

Type checking can be computationally expensive, especially for larger codebases. Performance challenges include:

- **Computational Complexity**: Some type checking operations (like subtyping) can be expensive
- **Memory Usage**: Storing type information for an entire program requires significant memory
- **Responsiveness**: IDE scenarios require near-instantaneous feedback

**Mitigation strategies**:

- **Incremental Analysis**:
  ```python
  class IncrementalTypeChecker:
      def __init__(self):
          self.file_dependencies = {}  # Track inter-file dependencies
          self.file_signatures = {}  # Track file signatures for change detection
          self.cached_types = {}  # Cache type information by file

      def check_files(self, changed_files):
          """Check only changed files and their dependents."""
          # Determine affected files
          affected_files = set(changed_files)
          for file in changed_files:
              affected_files.update(self.get_dependent_files(file))

          # Check affected files
          for file in affected_files:
              self.check_file(file)

      def get_dependent_files(self, file):
          """Get files that depend on the given file."""
          return self.file_dependencies.get(file, set())
  ```

- **Caching of Results**:
  ```python
  def type_check_function(function_node, context):
      """Type check a function with caching."""
      # Check if we have a valid cached result
      cache_key = get_cache_key(function_node)
      if cache_key in context.type_cache and not has_changed(function_node, context.type_cache[cache_key].version):
          return context.type_cache[cache_key].result

      # Perform type checking
      result = perform_type_checking(function_node, context)

      # Cache the result
      context.type_cache[cache_key] = CacheEntry(result, get_current_version(function_node))

      return result
  ```

- **Parallel Processing**:
  ```python
  def check_modules_parallel(modules, max_workers=None):
      """Check modules in parallel."""
      with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
          # Submit independent modules for parallel checking
          independent_modules = get_independent_modules(modules)
          futures = {executor.submit(check_module, module): module for module in independent_modules}

          # Process results as they complete
          for future in concurrent.futures.as_completed(futures):
              module = futures[future]
              try:
                  diagnostics = future.result()
                  process_diagnostics(module, diagnostics)
              except Exception as e:
                  handle_error(module, e)
  ```

### 2. Integration

The type checker needs to work seamlessly with the existing compiler infrastructure:

- **Compiler Compatibility**: Ensure the type checker works with the existing compiler
- **Non-Disruptive**: Add type checking without breaking existing functionality
- **Plugin Architecture**: Support extensibility for new language features

**Mitigation strategies**:

- Use a pass-based architecture that can be easily integrated with the existing compiler
- Implement feature flags to gradually enable type checking features
- Design clear interfaces between the type checker and other compiler components

### 3. Usability

Error messages must be clear and actionable to be useful for developers:

- **Clear Messages**: Error messages should clearly explain the problem
- **Actionable Suggestions**: Provide guidance on how to fix the issue
- **Context Awareness**: Show relevant information about the error context

**Mitigation strategies**:

- Design a diagnostic model that supports rich error information
- Use domain-specific language in error messages
- Provide fix suggestions where possible
- Test error messages with real users

### 4. Special Features

Jac-specific language constructs require special handling in the type system:

- **Graph Types**: Node and edge types have specialized relationships
- **Traversals**: Graph traversals have complex typing rules
- **Context Sensitivity**: Some operations have context-dependent typing

**Mitigation strategies**:

- Extend the core type system with domain-specific types
- Implement specialized type checking rules for graph operations
- Use context tracking for walker types
- Create comprehensive tests for special features

## Dependencies

The type checking system depends on several existing components of the Jac compiler infrastructure. Understanding these dependencies is crucial for successful implementation.

### Compiler Infrastructure Dependencies

The implementation depends on:

- **Existing compiler pass system**:

  The type checker will be implemented as a series of compiler passes that integrate with the existing pass system. This requires:

  - Understanding the pass scheduling mechanism
  - Implementing the pass interface correctly
  - Properly handling pass dependencies

  Example integration:
  ```python
  class TypeCheckingPass(CompilerPass):
      def __init__(self, program):
          super().__init__(program)
          self.requires = ["symbol_resolution"]  # Dependencies
          self.provides = ["type_information"]   # Outputs
  ```

- **AST structure and symbol tables**:

  The type checker builds on the abstract syntax tree (AST) and symbol tables:

  - AST nodes will be annotated with type information
  - Symbol table entries will be extended with types
  - Type checking operates on the AST structure

  These dependencies require careful coordination with the parser and symbol resolution phases.

- **Parsing infrastructure**:

  The type checker depends on the parsing infrastructure for:

  - Correctly structured AST nodes
  - Source location information for error reporting
  - Token information for context-sensitive features

  Any changes to the parser may affect type checking, so versioning and compatibility are important.

### Managing Dependencies

To manage these dependencies effectively:

1. **Minimal Coupling**: Design the type checker to minimize coupling with other components
2. **Clear Interfaces**: Define clear interfaces between the type checker and other systems
3. **Version Compatibility**: Ensure the type checker works with different versions of its dependencies
4. **Fallback Strategies**: Implement fallbacks for when dependencies are unavailable or incompatible

## Success Criteria

The type checking system will be considered successful when it meets the following criteria:

### 1. Accurately detects type errors in Jac programs

- **Correctness**: The type checker correctly implements the Jac type system rules
- **Completeness**: All language features are supported by the type checker
- **Sound but Practical**: The type system should be sound, but with practical escape hatches when needed

**Evaluation methods**:
- Comprehensive test suite covering all type rules
- Comparison with expected results on reference programs
- Formal verification of core type checking algorithms where possible

### 2. Provides clear and actionable error messages

- **Clarity**: Error messages clearly explain the problem
- **Context**: Messages include relevant context information
- **Actionability**: Messages provide guidance on how to fix the issue

**Evaluation methods**:
- User testing with developers of different experience levels
- Categorization and review of error messages
- Comparison with error messages from other type systems

### 3. Integrates seamlessly with IDEs and editors

- **LSP Support**: Full implementation of the Language Server Protocol
- **Real-time Feedback**: Type errors are reported as the user types
- **IDE Features**: Support for hover, completion, go-to-definition, etc.

**Evaluation methods**:
- Testing in multiple editors (VS Code, Vim, Emacs, etc.)
- Performance benchmarks for real-time scenarios
- User feedback on integration quality

### 4. Performs efficiently on large codebases

- **Speed**: Type checking is fast enough for interactive use
- **Scalability**: Performance scales reasonably with codebase size
- **Incremental Analysis**: Changes only trigger necessary reanalysis

**Evaluation methods**:
- Performance benchmarks on various codebase sizes
- Comparison with performance targets
- Memory usage monitoring

### 5. Supports all Jac-specific language features

- **Graph Types**: Complete support for node and edge types
- **Traversals**: Type-safe graph traversal operations
- **Walkers**: Context-sensitive typing for walkers
- **Special Constructs**: Support for all Jac-specific language constructs

**Evaluation methods**:
- Feature-specific test suites
- Real-world Jac program testing
- User feedback on domain-specific features

## Conclusion: The Path to a Robust Type Checker

Building a type checking system for Jac is a complex but rewarding endeavor. By following the phased implementation approach outlined in this document, we can create a type checker that enhances the language's safety, usability, and developer experience.

### Key Takeaways

1. **Phased Implementation**: Breaking the work into manageable phases allows for incremental progress and early validation.

2. **User-Centered Design**: Focusing on error messages and usability ensures the type checker adds value for developers.

3. **Performance First**: Designing for performance from the beginning avoids costly rewrites later.

4. **Domain-Specific Features**: Supporting Jac's graph-oriented features requires specialized type checking approaches.

5. **Comprehensive Testing**: A robust testing strategy ensures correctness, completeness, and performance.

### Next Steps

After completing the implementation phases described in this document:

1. **User Feedback**: Gather feedback from early users to refine the system
2. **Documentation**: Create comprehensive documentation for users and contributors
3. **Optimization**: Identify and optimize performance bottlenecks
4. **Extension**: Explore advanced type system features for future versions

The successful implementation of this type checking system will significantly enhance the Jac language ecosystem, providing developers with powerful tools for building safe and maintainable graph-oriented applications.