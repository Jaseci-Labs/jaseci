# Type Checking Architecture Proposal for Jac

## Current Architecture

The current Jac compiler uses a pass-based architecture where different passes are scheduled to run on the AST. For type checking, it currently relies on mypy:

1. `JacTypeCheckPass` - Integrates with mypy to perform type checking
2. `FuseTypeInfoPass` - Takes the type information from mypy and integrates it into Jac's AST

This approach has some limitations:
- Dependency on an external type checker (mypy)
- Need to convert between Jac's AST and mypy's AST
- Limited control over the type checking process
- Potential performance issues due to the conversion process

## Proposed Architecture

Drawing inspiration from Pyright's architecture, I propose implementing a native type checking system for Jac that eliminates the dependency on mypy. The new architecture would consist of the following components:

### 1. Type System

Create a comprehensive type system that can represent all Jac types:

```python
# jac/jaclang/compiler/types.py
from enum import Enum
from typing import Optional, List, Dict, Union, Set

class TypeCategory(Enum):
    """Categories of types in Jac."""
    UNBOUND = "UNBOUND"
    UNKNOWN = "UNKNOWN"
    ANY = "ANY"
    NEVER = "NEVER"
    FUNCTION = "FUNCTION"
    CLASS = "CLASS"
    MODULE = "MODULE"
    UNION = "UNION"
    TYPE_VAR = "TYPE_VAR"
    # Jac-specific types
    WALKER = "WALKER"
    NODE = "NODE"
    EDGE = "EDGE"
    ABILITY = "ABILITY"
    ENUM = "ENUM"

class TypeFlags(Enum):
    """Flags that can be applied to types."""
    NONE = 0
    INSTANTIABLE = 1 << 0
    INSTANCE = 1 << 1
    AMBIGUOUS = 1 << 2

class Type:
    """Base class for all types in Jac."""
    def __init__(self, category: TypeCategory, flags: int = TypeFlags.NONE.value):
        self.category = category
        self.flags = flags

class UnboundType(Type):
    """Represents a name that is not bound to a value of any type."""
    def __init__(self):
        super().__init__(TypeCategory.UNBOUND)

class UnknownType(Type):
    """Represents an implicit Any type."""
    def __init__(self):
        super().__init__(TypeCategory.UNKNOWN)

class AnyType(Type):
    """Represents a type that can be anything."""
    def __init__(self):
        super().__init__(TypeCategory.ANY)

class NeverType(Type):
    """Represents the bottom type, equivalent to an empty union."""
    def __init__(self):
        super().__init__(TypeCategory.NEVER)

class FunctionType(Type):
    """Represents a callable type."""
    def __init__(self, param_types: List[Type], return_type: Type, is_method: bool = False):
        super().__init__(TypeCategory.FUNCTION)
        self.param_types = param_types
        self.return_type = return_type
        self.is_method = is_method

class ClassType(Type):
    """Represents a class definition."""
    def __init__(self, name: str, fullname: str, base_types: List[Type] = None, 
                 is_instantiated: bool = False):
        flags = TypeFlags.INSTANTIABLE.value
        if is_instantiated:
            flags |= TypeFlags.INSTANCE.value
        super().__init__(TypeCategory.CLASS, flags)
        self.name = name
        self.fullname = fullname
        self.base_types = base_types or []
        self.members = {}  # Dict[str, Symbol]

class ModuleType(Type):
    """Represents a module instance."""
    def __init__(self, name: str, fullname: str):
        super().__init__(TypeCategory.MODULE)
        self.name = name
        self.fullname = fullname
        self.members = {}  # Dict[str, Symbol]

class UnionType(Type):
    """Represents a union of two or more other types."""
    def __init__(self, items: List[Type]):
        super().__init__(TypeCategory.UNION)
        self.items = items

class TypeVarType(Type):
    """Represents a type variable."""
    def __init__(self, name: str, fullname: str, values: List[Type] = None, 
                 upper_bound: Type = None):
        super().__init__(TypeCategory.TYPE_VAR)
        self.name = name
        self.fullname = fullname
        self.values = values
        self.upper_bound = upper_bound

# Jac-specific types
class WalkerType(ClassType):
    """Represents a walker type in Jac."""
    def __init__(self, name: str, fullname: str, base_types: List[Type] = None, 
                 is_instantiated: bool = False):
        super().__init__(name, fullname, base_types, is_instantiated)
        self.category = TypeCategory.WALKER

class NodeType(ClassType):
    """Represents a node type in Jac."""
    def __init__(self, name: str, fullname: str, base_types: List[Type] = None, 
                 is_instantiated: bool = False):
        super().__init__(name, fullname, base_types, is_instantiated)
        self.category = TypeCategory.NODE

class EdgeType(ClassType):
    """Represents an edge type in Jac."""
    def __init__(self, name: str, fullname: str, base_types: List[Type] = None, 
                 is_instantiated: bool = False):
        super().__init__(name, fullname, base_types, is_instantiated)
        self.category = TypeCategory.EDGE

class AbilityType(FunctionType):
    """Represents an ability type in Jac."""
    def __init__(self, param_types: List[Type], return_type: Type, is_method: bool = True):
        super().__init__(param_types, return_type, is_method)
        self.category = TypeCategory.ABILITY

class EnumType(ClassType):
    """Represents an enum type in Jac."""
    def __init__(self, name: str, fullname: str, base_types: List[Type] = None, 
                 is_instantiated: bool = False):
        super().__init__(name, fullname, base_types, is_instantiated)
        self.category = TypeCategory.ENUM
        self.values = {}  # Dict[str, EnumValue]
```

### 2. Type Binder

Create a binder that associates AST nodes with their types:

```python
# jac/jaclang/compiler/passes/main/type_binder_pass.py
from typing import Dict, Optional

import jaclang.compiler.unitree as uni
from jaclang.compiler.passes import UniPass
from jaclang.compiler.types import *

class TypeBinderPass(UniPass):
    """Pass that binds types to AST nodes."""
    
    def __init__(self, ir_in: uni.UniNode, prog=None) -> None:
        """Initialize the TypeBinderPass."""
        super().__init__(ir_in, prog)
        self.type_map: Dict[uni.UniNode, Type] = {}
        self.builtin_types: Dict[str, Type] = self._initialize_builtin_types()
        
    def _initialize_builtin_types(self) -> Dict[str, Type]:
        """Initialize the builtin types."""
        builtins = {}
        # Add primitive types
        builtins["int"] = ClassType("int", "builtins.int", is_instantiated=True)
        builtins["float"] = ClassType("float", "builtins.float", is_instantiated=True)
        builtins["str"] = ClassType("str", "builtins.str", is_instantiated=True)
        builtins["bool"] = ClassType("bool", "builtins.bool", is_instantiated=True)
        builtins["list"] = ClassType("list", "builtins.list", is_instantiated=True)
        builtins["dict"] = ClassType("dict", "builtins.dict", is_instantiated=True)
        builtins["set"] = ClassType("set", "builtins.set", is_instantiated=True)
        builtins["tuple"] = ClassType("tuple", "builtins.tuple", is_instantiated=True)
        builtins["None"] = ClassType("None", "builtins.None", is_instantiated=True)
        builtins["Any"] = AnyType()
        return builtins
        
    def bind_type(self, node: uni.UniNode, type_obj: Type) -> None:
        """Bind a type to a node."""
        self.type_map[node] = type_obj
        if isinstance(node, uni.AstSymbolNode):
            node.name_spec.expr_type = self._type_to_string(type_obj)
            
    def get_type(self, node: uni.UniNode) -> Optional[Type]:
        """Get the type of a node."""
        return self.type_map.get(node)
        
    def _type_to_string(self, type_obj: Type) -> str:
        """Convert a type to a string representation."""
        if isinstance(type_obj, ClassType):
            return type_obj.fullname
        elif isinstance(type_obj, FunctionType):
            return f"function[{', '.join(self._type_to_string(t) for t in type_obj.param_types)}] -> {self._type_to_string(type_obj.return_type)}"
        elif isinstance(type_obj, UnionType):
            return f"Union[{', '.join(self._type_to_string(t) for t in type_obj.items)}]"
        elif isinstance(type_obj, AnyType):
            return "Any"
        elif isinstance(type_obj, NeverType):
            return "Never"
        elif isinstance(type_obj, UnknownType):
            return "Unknown"
        elif isinstance(type_obj, UnboundType):
            return "Unbound"
        else:
            return str(type_obj.category.value)
            
    # Implement visitor methods for each node type
    def enter_int(self, node: uni.Int) -> None:
        """Bind type for Int nodes."""
        self.bind_type(node, self.builtin_types["int"])
        
    def enter_float(self, node: uni.Float) -> None:
        """Bind type for Float nodes."""
        self.bind_type(node, self.builtin_types["float"])
        
    def enter_string(self, node: uni.String) -> None:
        """Bind type for String nodes."""
        self.bind_type(node, self.builtin_types["str"])
        
    def enter_bool(self, node: uni.Bool) -> None:
        """Bind type for Bool nodes."""
        self.bind_type(node, self.builtin_types["bool"])
        
    def enter_list_val(self, node: uni.ListVal) -> None:
        """Bind type for ListVal nodes."""
        self.bind_type(node, self.builtin_types["list"])
        
    def enter_dict_val(self, node: uni.DictVal) -> None:
        """Bind type for DictVal nodes."""
        self.bind_type(node, self.builtin_types["dict"])
        
    def enter_set_val(self, node: uni.SetVal) -> None:
        """Bind type for SetVal nodes."""
        self.bind_type(node, self.builtin_types["set"])
        
    def enter_tuple_val(self, node: uni.TupleVal) -> None:
        """Bind type for TupleVal nodes."""
        self.bind_type(node, self.builtin_types["tuple"])
        
    def enter_name(self, node: uni.NameAtom) -> None:
        """Bind type for Name nodes."""
        # Look up the symbol in the symbol table
        if node.sym:
            # If the symbol has a type, use it
            if hasattr(node.sym, "type"):
                self.bind_type(node, node.sym.type)
            else:
                # Otherwise, use Unknown
                self.bind_type(node, UnknownType())
        else:
            # If the symbol is not found, use Unbound
            self.bind_type(node, UnboundType())
            
    # Add more visitor methods for other node types
```

### 3. Type Checker

Create a type checker that verifies type compatibility:

```python
# jac/jaclang/compiler/passes/main/type_checker_pass.py
from typing import Dict, List, Optional, Tuple

import jaclang.compiler.unitree as uni
from jaclang.compiler.passes import UniPass
from jaclang.compiler.types import *
from jaclang.compiler.passes.main.type_binder_pass import TypeBinderPass

class TypeCheckerPass(UniPass):
    """Pass that checks type compatibility."""
    
    def __init__(self, ir_in: uni.UniNode, prog=None) -> None:
        """Initialize the TypeCheckerPass."""
        super().__init__(ir_in, prog)
        # Run the type binder pass first to get type information
        self.binder = TypeBinderPass(ir_in, prog)
        self.binder.run()
        self.type_map = self.binder.type_map
        
    def get_type(self, node: uni.UniNode) -> Optional[Type]:
        """Get the type of a node."""
        return self.type_map.get(node)
        
    def is_compatible(self, source_type: Type, target_type: Type) -> bool:
        """Check if source_type is compatible with target_type."""
        # Any type is compatible with itself
        if source_type == target_type:
            return True
            
        # Any type is compatible with Any
        if isinstance(target_type, AnyType):
            return True
            
        # None is compatible with Optional types
        if (isinstance(source_type, ClassType) and source_type.fullname == "builtins.None" and
            isinstance(target_type, UnionType) and any(
                isinstance(t, ClassType) and t.fullname == "builtins.None" for t in target_type.items
            )):
            return True
            
        # Check class inheritance
        if (isinstance(source_type, ClassType) and isinstance(target_type, ClassType)):
            # Check if source_type is a subclass of target_type
            if source_type.fullname == target_type.fullname:
                return True
                
            # Check base classes
            for base in source_type.base_types:
                if self.is_compatible(base, target_type):
                    return True
                    
        # Check union types
        if isinstance(target_type, UnionType):
            # Source type is compatible if it's compatible with any item in the union
            return any(self.is_compatible(source_type, item) for item in target_type.items)
            
        # Check function types
        if isinstance(source_type, FunctionType) and isinstance(target_type, FunctionType):
            # Check return type
            if not self.is_compatible(source_type.return_type, target_type.return_type):
                return False
                
            # Check parameter types (contravariant)
            if len(source_type.param_types) != len(target_type.param_types):
                return False
                
            for i in range(len(source_type.param_types)):
                if not self.is_compatible(target_type.param_types[i], source_type.param_types[i]):
                    return False
                    
            return True
            
        return False
        
    def check_assignment(self, target: uni.UniNode, value: uni.UniNode) -> None:
        """Check if an assignment is type-compatible."""
        target_type = self.get_type(target)
        value_type = self.get_type(value)
        
        if target_type is None or value_type is None:
            return
            
        if not self.is_compatible(value_type, target_type):
            self.log_error(
                f"Type mismatch: Cannot assign value of type '{value_type.category.value}' to variable of type '{target_type.category.value}'",
                node_override=target
            )
            
    def enter_assignment(self, node: uni.Assignment) -> None:
        """Check type compatibility for assignments."""
        for target in node.target.items:
            self.check_assignment(target, node.value)
            
    def enter_binary_expr(self, node: uni.BinaryExpr) -> None:
        """Check type compatibility for binary expressions."""
        left_type = self.get_type(node.left)
        right_type = self.get_type(node.right)
        
        if left_type is None or right_type is None:
            return
            
        # Check operator compatibility
        if isinstance(node.op, uni.AddOp):
            # Addition is valid for numbers, strings, lists, etc.
            if (isinstance(left_type, ClassType) and isinstance(right_type, ClassType)):
                valid_types = ["builtins.int", "builtins.float", "builtins.str", "builtins.list"]
                if left_type.fullname not in valid_types or right_type.fullname not in valid_types:
                    self.log_error(
                        f"Operator '+' not supported for types '{left_type.category.value}' and '{right_type.category.value}'",
                        node_override=node
                    )
                    
                # Check that the types are the same (except for int and float)
                if (left_type.fullname != right_type.fullname and 
                    not (left_type.fullname in ["builtins.int", "builtins.float"] and 
                         right_type.fullname in ["builtins.int", "builtins.float"])):
                    self.log_error(
                        f"Cannot add values of types '{left_type.category.value}' and '{right_type.category.value}'",
                        node_override=node
                    )
        
        # Add more operator checks
        
    # Add more visitor methods for other node types
```

### 4. Type Evaluator

Create a type evaluator that infers types for expressions:

```python
# jac/jaclang/compiler/passes/main/type_evaluator_pass.py
from typing import Dict, List, Optional, Tuple

import jaclang.compiler.unitree as uni
from jaclang.compiler.passes import UniPass
from jaclang.compiler.types import *
from jaclang.compiler.passes.main.type_binder_pass import TypeBinderPass

class TypeEvaluatorPass(UniPass):
    """Pass that evaluates and infers types for expressions."""
    
    def __init__(self, ir_in: uni.UniNode, prog=None) -> None:
        """Initialize the TypeEvaluatorPass."""
        super().__init__(ir_in, prog)
        # Run the type binder pass first to get initial type information
        self.binder = TypeBinderPass(ir_in, prog)
        self.binder.run()
        self.type_map = self.binder.type_map
        self.builtin_types = self.binder.builtin_types
        
    def evaluate_type(self, node: uni.UniNode) -> Optional[Type]:
        """Evaluate the type of an expression."""
        # Check if we already have a type for this node
        if node in self.type_map:
            return self.type_map[node]
            
        # Evaluate based on node type
        if isinstance(node, uni.BinaryExpr):
            return self.evaluate_binary_expr(node)
        elif isinstance(node, uni.UnaryExpr):
            return self.evaluate_unary_expr(node)
        elif isinstance(node, uni.FuncCall):
            return self.evaluate_func_call(node)
        elif isinstance(node, uni.AtomTrailer):
            return self.evaluate_atom_trailer(node)
        # Add more cases for other expression types
        
        return None
        
    def evaluate_binary_expr(self, node: uni.BinaryExpr) -> Optional[Type]:
        """Evaluate the type of a binary expression."""
        left_type = self.evaluate_type(node.left)
        right_type = self.evaluate_type(node.right)
        
        if left_type is None or right_type is None:
            return None
            
        # Addition
        if isinstance(node.op, uni.AddOp):
            # int + int = int
            if (isinstance(left_type, ClassType) and left_type.fullname == "builtins.int" and
                isinstance(right_type, ClassType) and right_type.fullname == "builtins.int"):
                return self.builtin_types["int"]
                
            # float + float = float, int + float = float, float + int = float
            if ((isinstance(left_type, ClassType) and left_type.fullname in ["builtins.int", "builtins.float"]) and
                (isinstance(right_type, ClassType) and right_type.fullname in ["builtins.int", "builtins.float"])):
                return self.builtin_types["float"]
                
            # str + str = str
            if (isinstance(left_type, ClassType) and left_type.fullname == "builtins.str" and
                isinstance(right_type, ClassType) and right_type.fullname == "builtins.str"):
                return self.builtin_types["str"]
                
            # list + list = list
            if (isinstance(left_type, ClassType) and left_type.fullname == "builtins.list" and
                isinstance(right_type, ClassType) and right_type.fullname == "builtins.list"):
                return self.builtin_types["list"]
                
        # Comparison operators
        if isinstance(node.op, (uni.EqOp, uni.NotEqOp, uni.LtOp, uni.GtOp, uni.LtEOp, uni.GtEOp)):
            return self.builtin_types["bool"]
            
        # Add more operator cases
        
        return None
        
    def evaluate_unary_expr(self, node: uni.UnaryExpr) -> Optional[Type]:
        """Evaluate the type of a unary expression."""
        operand_type = self.evaluate_type(node.operand)
        
        if operand_type is None:
            return None
            
        # Negation
        if isinstance(node.op, uni.NegOp):
            # -int = int
            if isinstance(operand_type, ClassType) and operand_type.fullname == "builtins.int":
                return self.builtin_types["int"]
                
            # -float = float
            if isinstance(operand_type, ClassType) and operand_type.fullname == "builtins.float":
                return self.builtin_types["float"]
                
        # Not
        if isinstance(node.op, uni.NotOp):
            return self.builtin_types["bool"]
            
        # Add more operator cases
        
        return None
        
    def evaluate_func_call(self, node: uni.FuncCall) -> Optional[Type]:
        """Evaluate the type of a function call."""
        func_type = self.evaluate_type(node.target)
        
        if func_type is None:
            return None
            
        if isinstance(func_type, FunctionType):
            return func_type.return_type
            
        # Handle built-in functions with special return types
        if isinstance(node.target, uni.NameAtom):
            if node.target.sym_name == "len":
                return self.builtin_types["int"]
            elif node.target.sym_name == "str":
                return self.builtin_types["str"]
            elif node.target.sym_name == "int":
                return self.builtin_types["int"]
            elif node.target.sym_name == "float":
                return self.builtin_types["float"]
            elif node.target.sym_name == "bool":
                return self.builtin_types["bool"]
            elif node.target.sym_name == "list":
                return self.builtin_types["list"]
            elif node.target.sym_name == "dict":
                return self.builtin_types["dict"]
            elif node.target.sym_name == "set":
                return self.builtin_types["set"]
                
        return None
        
    def evaluate_atom_trailer(self, node: uni.AtomTrailer) -> Optional[Type]:
        """Evaluate the type of an atom trailer (e.g., obj.attr)."""
        target_type = self.evaluate_type(node.target)
        
        if target_type is None:
            return None
            
        if isinstance(target_type, ClassType) and isinstance(node.right, uni.NameAtom):
            # Look up the attribute in the class members
            attr_name = node.right.sym_name
            if attr_name in target_type.members:
                member_sym = target_type.members[attr_name]
                if hasattr(member_sym, "type"):
                    return member_sym.type
                    
        return None
        
    # Add more evaluation methods for other expression types
    
    def enter_node(self, node: uni.UniNode) -> None:
        """Run on entering node."""
        super().enter_node(node)
        
        # Evaluate the type of expressions
        if isinstance(node, uni.Expr):
            type_obj = self.evaluate_type(node)
            if type_obj is not None:
                self.type_map[node] = type_obj
                if isinstance(node, uni.AstSymbolNode):
                    node.name_spec.expr_type = self.binder._type_to_string(type_obj)
```

### 5. Integration with Compiler Passes

Update the compiler passes to use the new type checking system:

```python
# jac/jaclang/compiler/passes/main/schedules.py
from __future__ import annotations

from enum import Enum

from .def_impl_match_pass import DeclImplMatchPass
from .def_use_pass import DefUsePass
from .pybc_gen_pass import PyBytecodeGenPass
from .pyast_gen_pass import PyastGenPass
from .pyjac_ast_link_pass import PyJacAstLinkPass
from .access_modifier_pass import AccessCheckPass
from .inheritance_pass import InheritancePass
from .type_binder_pass import TypeBinderPass
from .type_evaluator_pass import TypeEvaluatorPass
from .type_checker_pass import TypeCheckerPass


class CompilerMode(Enum):
    """Compiler modes."""

    PARSE = "PARSE"
    COMPILE = "COMPILE"
    TYPECHECK = "TYPECHECK"


py_code_gen = [
    DeclImplMatchPass,
    DefUsePass,
    PyastGenPass,
    PyJacAstLinkPass,
    PyBytecodeGenPass,
]

type_checker_sched = [
    InheritancePass,
    TypeBinderPass,
    TypeEvaluatorPass,
    TypeCheckerPass,
    AccessCheckPass,
]

py_code_gen_typed = [*py_code_gen, *type_checker_sched]
```

Update the program.py file to use the new type checking system:

```python
# In jac/jaclang/compiler/program.py

# Replace the JacTypeCheckPass import with the new passes
from jaclang.compiler.passes.main import (
    CompilerMode,
    DefUsePass,
    JacAnnexManager,
    JacImportPass,
    TypeBinderPass,
    TypeEvaluatorPass,
    TypeCheckerPass,
    PyBytecodeGenPass,
    PyCollectDepsPass,
    PyImportPass,
    PyastBuildPass,
    SymTabBuildPass,
    py_code_gen,
    type_checker_sched,
)

# Update the run_whole_program_schedule method
def run_whole_program_schedule(
    self,
    mod_targ: uni.Module,
    mode: CompilerMode = CompilerMode.COMPILE,
) -> uni.Module:
    """Convert a Jac file to an AST."""
    for mod in self.mod.hub.values():
        SymTabLinkPass(ir_in=mod, prog=self)

    for mod in self.mod.hub.values():
        self.schedule_runner(mod, mode=CompilerMode.COMPILE)

    # Check if we need to run without type checking then just return
    if mode == CompilerMode.COMPILE:
        return mod_targ

    # Run type checking passes on all modules
    for mod in self.mod.hub.values():
        TypeBinderPass(ir_in=mod, prog=self)
        TypeEvaluatorPass(ir_in=mod, prog=self)
        TypeCheckerPass(ir_in=mod, prog=self)

    for mod in self.mod.hub.values():
        PyCollectDepsPass(mod, prog=self)

    for mod in self.mod.hub.values():
        self.last_imported.append(mod)
    # Run PyImportPass
    while len(self.last_imported) > 0:
        mod = self.last_imported.pop()
        PyImportPass(mod, prog=self)

    # Link all Jac symbol tables created
    for mod in self.mod.hub.values():
        SymTabLinkPass(ir_in=mod, prog=self)

    for mod in self.mod.hub.values():
        DefUsePass(mod, prog=self)

    for mod in self.mod.hub.values():
        self.schedule_runner(mod, mode=CompilerMode.TYPECHECK)

    return mod_targ
```

## Benefits of the New Architecture

1. **Independence from External Tools**: No dependency on mypy for type checking.

2. **Better Integration**: The type system is designed specifically for Jac, including support for Jac-specific types like walkers, nodes, and edges.

3. **Performance Improvements**: Eliminates the need to convert between Jac's AST and mypy's AST, which should improve performance.

4. **More Control**: Full control over the type checking process, allowing for more customization and better error messages.

5. **Extensibility**: The modular design makes it easy to add support for new types and type checking rules.

## Implementation Strategy

1. **Phase 1**: Implement the basic type system and type binder.
   - Create the type classes
   - Implement the type binder pass
   - Update the compiler to use the new passes

2. **Phase 2**: Implement the type evaluator and checker.
   - Implement type inference for expressions
   - Implement type compatibility checking
   - Add support for Jac-specific types

3. **Phase 3**: Enhance error reporting and add advanced features.
   - Improve error messages
   - Add support for generics
   - Add support for type aliases
   - Add support for union types

4. **Phase 4**: Remove the dependency on mypy.
   - Update all code that currently relies on mypy
   - Remove mypy-related code and dependencies

## Conclusion

This proposal outlines a comprehensive approach to implementing a native type checking system for Jac, drawing inspiration from Pyright's architecture. The new system will eliminate the dependency on mypy, provide better integration with Jac's specific features, and offer more control over the type checking process.

By implementing this architecture, Jac will have a more robust and efficient type checking system that is specifically designed for its unique features and requirements.
