"""Type binder pass for Jac language.

This pass binds types to AST nodes based on their structure and context.
It serves as the foundation for type checking by associating each node with
a specific type from the type system.
"""

from typing import Dict, List, Optional, Set, Tuple, Union, cast

import jaclang.compiler.unitree as uni
from jaclang.compiler.passes import UniPass
from jaclang.compiler.types import (
    BUILTIN_TYPES,
    AbilityType,
    AnyType,
    ClassType,
    EdgeType,
    EnumType,
    FunctionType,
    ModuleType,
    NodeType,
    Symbol,
    Type,
    TypeCategory,
    UnboundType,
    UnionType,
    UnknownType,
    WalkerType,
    is_subtype,
)


class TypeBinderPass(UniPass):
    """Pass that binds types to AST nodes."""

    def __init__(self, ir_in: uni.UniNode, prog=None) -> None:
        """Initialize the TypeBinderPass."""
        super().__init__(ir_in, prog)
        self.type_map: Dict[uni.UniNode, Type] = {}
        self.symbol_map: Dict[uni.Symbol, Symbol] = {}
        self.module_types: Dict[str, ModuleType] = {}
        self.current_module: Optional[ModuleType] = None

    def before_pass(self) -> None:
        """Set up the pass."""
        super().before_pass()
        # Initialize the current module
        if isinstance(self.ir_out, uni.Module):
            module_name = self.ir_out.name
            if module_name not in self.module_types:
                self.module_types[module_name] = ModuleType(
                    name=module_name.split(".")[-1], fullname=module_name
                )
            self.current_module = self.module_types[module_name]

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
        return str(type_obj)

    def _get_builtin_type(self, name: str) -> Type:
        """Get a builtin type by name."""
        return BUILTIN_TYPES.get(name, UnknownType())

    # Visitor methods for literal values

    def enter_int(self, node: uni.Int) -> None:
        """Bind type for Int nodes."""
        self.bind_type(node, self._get_builtin_type("int"))

    def enter_float(self, node: uni.Float) -> None:
        """Bind type for Float nodes."""
        self.bind_type(node, self._get_builtin_type("float"))

    def enter_string(self, node: uni.String) -> None:
        """Bind type for String nodes."""
        self.bind_type(node, self._get_builtin_type("str"))

    def enter_multi_string(self, node: uni.MultiString) -> None:
        """Bind type for MultiString nodes."""
        self.bind_type(node, self._get_builtin_type("str"))

    def enter_f_string(self, node: uni.FString) -> None:
        """Bind type for FString nodes."""
        self.bind_type(node, self._get_builtin_type("str"))

    def enter_bool(self, node: uni.Bool) -> None:
        """Bind type for Bool nodes."""
        self.bind_type(node, self._get_builtin_type("bool"))

    # Visitor methods for container literals

    def enter_list_val(self, node: uni.ListVal) -> None:
        """Bind type for ListVal nodes."""
        self.bind_type(node, self._get_builtin_type("list"))

    def enter_dict_val(self, node: uni.DictVal) -> None:
        """Bind type for DictVal nodes."""
        self.bind_type(node, self._get_builtin_type("dict"))

    def enter_set_val(self, node: uni.SetVal) -> None:
        """Bind type for SetVal nodes."""
        self.bind_type(node, self._get_builtin_type("set"))

    def enter_tuple_val(self, node: uni.TupleVal) -> None:
        """Bind type for TupleVal nodes."""
        self.bind_type(node, self._get_builtin_type("tuple"))

    # Visitor methods for variables and symbols

    def enter_name(self, node: uni.NameAtom) -> None:
        """Bind type for Name nodes."""
        # Look up the symbol in the symbol table
        if node.sym:
            # Check if we already have a type for this symbol
            if node.sym in self.symbol_map:
                self.bind_type(node, self.symbol_map[node.sym].type)
                return

            # If the symbol has a type annotation, use it
            if hasattr(node.sym, "type_annotation") and node.sym.type_annotation:
                type_obj = self._resolve_type_annotation(node.sym.type_annotation)
                if type_obj:
                    self.bind_type(node, type_obj)
                    self.symbol_map[node.sym] = Symbol(node.sym_name, type_obj)
                    return

            # If the symbol is a builtin, use its type
            if node.sym_name in BUILTIN_TYPES:
                self.bind_type(node, BUILTIN_TYPES[node.sym_name])
                self.symbol_map[node.sym] = Symbol(
                    node.sym_name, BUILTIN_TYPES[node.sym_name]
                )
                return

            # Otherwise, use Unknown
            self.bind_type(node, UnknownType())
            self.symbol_map[node.sym] = Symbol(node.sym_name, UnknownType())
        else:
            # If the symbol is not found, use Unbound
            self.bind_type(node, UnboundType())

    def enter_builtin_type(self, node: uni.BuiltinType) -> None:
        """Bind type for BuiltinType nodes."""
        if node.sym_name in BUILTIN_TYPES:
            self.bind_type(node, BUILTIN_TYPES[node.sym_name])
        else:
            self.bind_type(node, UnknownType())

    def enter_special_var_ref(self, node: uni.SpecialVarRef) -> None:
        """Bind type for SpecialVarRef nodes."""
        # Handle special variables like self, here, etc.
        if node.sym_name == "self":
            # Find the enclosing class or architype
            enclosing = node.parent_of_type((uni.Architype, uni.Enum))
            if enclosing:
                if enclosing in self.type_map:
                    self.bind_type(node, self.type_map[enclosing])
                    return
        # Default to Unknown
        self.bind_type(node, UnknownType())

    # Visitor methods for function and class definitions

    def enter_ability(self, node: uni.Ability) -> None:
        """Bind type for Ability nodes."""
        # Collect parameter types
        param_types: List[Type] = []
        param_names: List[str] = []
        if node.params:
            for param in node.params.items:
                if isinstance(param, uni.ParamVar):
                    param_type = (
                        self._resolve_type_annotation(param.type_tag.items[0])
                        if param.type_tag
                        else UnknownType()
                    )
                    param_types.append(param_type)
                    param_names.append(param.sym_name)

        # Determine return type
        return_type = UnknownType()
        if hasattr(node, "return_type") and node.return_type:
            return_type = self._resolve_type_annotation(node.return_type.items[0])

        # Create the ability type
        ability_type = AbilityType(
            param_types=param_types,
            return_type=return_type,
            is_method=True,
            param_names=param_names,
        )
        self.bind_type(node, ability_type)

        # Add the ability to the symbol table
        if node.sym:
            self.symbol_map[node.sym] = Symbol(node.sym_name, ability_type)

    def enter_architype(self, node: uni.Architype) -> None:
        """Bind type for Architype nodes."""
        # Determine the base types
        base_types: List[Type] = []
        if node.base_classes:
            for base in node.base_classes.items:
                if isinstance(base, uni.NameAtom) and base.sym:
                    if base.sym in self.symbol_map:
                        base_types.append(self.symbol_map[base.sym].type)

        # Create the appropriate type based on the architype kind
        if node.arch_type.name == "walker":
            arch_type = WalkerType(
                name=node.sym_name,
                fullname=(
                    f"{self.current_module.fullname}.{node.sym_name}"
                    if self.current_module
                    else node.sym_name
                ),
                base_types=base_types,
                is_instantiated=False,
            )
        elif node.arch_type.name == "node":
            arch_type = NodeType(
                name=node.sym_name,
                fullname=(
                    f"{self.current_module.fullname}.{node.sym_name}"
                    if self.current_module
                    else node.sym_name
                ),
                base_types=base_types,
                is_instantiated=False,
            )
        elif node.arch_type.name == "edge":
            arch_type = EdgeType(
                name=node.sym_name,
                fullname=(
                    f"{self.current_module.fullname}.{node.sym_name}"
                    if self.current_module
                    else node.sym_name
                ),
                base_types=base_types,
                is_instantiated=False,
            )
        else:
            arch_type = ClassType(
                name=node.sym_name,
                fullname=(
                    f"{self.current_module.fullname}.{node.sym_name}"
                    if self.current_module
                    else node.sym_name
                ),
                base_types=base_types,
                is_instantiated=False,
            )

        self.bind_type(node, arch_type)

        # Add the architype to the symbol table
        if node.sym:
            self.symbol_map[node.sym] = Symbol(node.sym_name, arch_type)

        # Add the architype to the current module
        if self.current_module and node.sym_name:
            self.current_module.members[node.sym_name] = Symbol(
                node.sym_name, arch_type
            )

    def enter_enum(self, node: uni.Enum) -> None:
        """Bind type for Enum nodes."""
        # Determine the base types
        base_types: List[Type] = []
        if node.base_classes:
            for base in node.base_classes.items:
                if isinstance(base, uni.NameAtom) and base.sym:
                    if base.sym in self.symbol_map:
                        base_types.append(self.symbol_map[base.sym].type)

        # Create the enum type
        enum_type = EnumType(
            name=node.sym_name,
            fullname=(
                f"{self.current_module.fullname}.{node.sym_name}"
                if self.current_module
                else node.sym_name
            ),
            base_types=base_types,
            is_instantiated=False,
        )
        self.bind_type(node, enum_type)

        # Add the enum to the symbol table
        if node.sym:
            self.symbol_map[node.sym] = Symbol(node.sym_name, enum_type)

        # Add the enum to the current module
        if self.current_module and node.sym_name:
            self.current_module.members[node.sym_name] = Symbol(
                node.sym_name, enum_type
            )

    # Visitor methods for expressions

    def enter_binary_expr(self, node: uni.BinaryExpr) -> None:
        """Bind type for BinaryExpr nodes."""
        # For now, just propagate the type of the left operand
        # This will be refined in the type evaluator pass
        left_type = self.get_type(node.left)
        if left_type:
            self.bind_type(node, left_type)
        else:
            self.bind_type(node, UnknownType())

    def enter_unary_expr(self, node: uni.UnaryExpr) -> None:
        """Bind type for UnaryExpr nodes."""
        # For now, just propagate the type of the operand
        # This will be refined in the type evaluator pass
        operand_type = self.get_type(node.operand)
        if operand_type:
            self.bind_type(node, operand_type)
        else:
            self.bind_type(node, UnknownType())

    def enter_func_call(self, node: uni.FuncCall) -> None:
        """Bind type for FuncCall nodes."""
        # For now, just use Unknown
        # This will be refined in the type evaluator pass
        self.bind_type(node, UnknownType())

    def enter_atom_trailer(self, node: uni.AtomTrailer) -> None:
        """Bind type for AtomTrailer nodes."""
        # For now, just use Unknown
        # This will be refined in the type evaluator pass
        self.bind_type(node, UnknownType())

    # Helper methods

    def _resolve_type_annotation(self, annotation: uni.UniNode) -> Type:
        """Resolve a type annotation to a Type object."""
        if isinstance(annotation, uni.NameAtom):
            # Simple type name
            if annotation.sym_name in BUILTIN_TYPES:
                return BUILTIN_TYPES[annotation.sym_name]
            elif annotation.sym and annotation.sym in self.symbol_map:
                return self.symbol_map[annotation.sym].type
        elif isinstance(annotation, uni.BuiltinType):
            # Builtin type
            if annotation.sym_name in BUILTIN_TYPES:
                return BUILTIN_TYPES[annotation.sym_name]
        elif isinstance(annotation, uni.AtomTrailer):
            # Qualified type name (e.g., module.Type)
            # For now, just return Unknown
            # This will be refined in a more complete implementation
            pass

        # Default to Unknown
        return UnknownType()
