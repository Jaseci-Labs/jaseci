"""
Defines the JClassType class, which represents both user-defined classes and built-in
primitive types in the Jac type system.

This class supports type instantiation, inheritance, callable semantics (via constructors),
and member access resolution. It also implements assignability checks based on nominal
and inheritance relationships.
"""

from __future__ import annotations

from typing import Optional

import jaclang.compiler.unitree as uni
from jaclang.compiler.jtyping.types.jtype import JType
from jaclang.compiler.jtyping.types.jclassmember import JClassMember
from jaclang.compiler.jtyping.types.jfunctionttype import JFunctionType


class JClassType(JType):
    """
    Represents a class type in the Jac type system, including both user-defined classes
    and built-in primitives such as `int`, `str`, etc.

    This type supports inheritance, instance-level and class-level members,
    and instantiation checks. It also models callable behavior via constructors.

    Attributes:
        name (str): Name of the class (e.g., 'int', 'MyClass').
        module (Optional[uni.Module]): Module where the class is defined.
        bases (list[JClassType]): A list of base classes (superclasses).
        is_abstract (bool): Whether this class is abstract and cannot be instantiated.
        instance_members (dict[str, JClassMember]): Members available on instances of this class.
        class_members (dict[str, JClassMember]): Members available on the class object itself.
        assignable_from (list[str]): Fully qualified names of types assignable to this one.
    """

    def __init__(
        self,
        name: str,
        full_name: str,
        module: Optional[uni.Module],
        bases: Optional[list[JClassType]] = None,
        is_abstract: bool = False,
        instance_members: Optional[dict[str, JClassMember]] = None,
        class_members: Optional[dict[str, JClassMember]] = None,
        assignable_from: list[str] = []
    ):
        """
        Initializes a new JClassType instance.

        Args:
            name (str): The name of the class.
            full_name (str): The fully qualified name of the class.
            module (Optional[uni.Module]): The module where the class is defined.
            bases (Optional[list[JClassType]]): List of base classes.
            is_abstract (bool): Whether the class is abstract.
            instance_members (Optional[dict[str, JClassMember]]): Members on instances.
            class_members (Optional[dict[str, JClassMember]]): Members on the class object.
            assignable_from (list[str]): Fully qualified names of types assignable to this one.
        """
        super().__init__(name, module)
        self.full_name: str = full_name
        self.bases: list[JClassType] = bases or []
        self.is_abstract: bool = is_abstract
        self.instance_members: dict[str, JClassMember] = instance_members or {}
        self.class_members: dict[str, JClassMember] = class_members or {}
        self.assignable_from: list[str] = assignable_from

    def is_instantiable(self) -> bool:
        """
        Returns whether this class can be directly instantiated.

        Returns:
            bool: False if the class is abstract; True otherwise.
        """
        return not self.is_abstract
    
    def is_callable(self) -> bool:
        """
        Indicates that classes are callable (i.e., can be instantiated via `Class()`).

        Returns:
            bool: Always True for class types.
        """
        return True

    def can_assign_from(self, other: JType) -> bool:
        """
        Checks whether a value of `other` type can be assigned to this class type.

        This includes:
        - Nominal equality (matching name and module),
        - Any explicitly listed type in `assignable_from`,
        - Inheritance relationships via `bases`.

        Args:
            other (JType): The type to check against.

        Returns:
            bool: True if assignable; False otherwise.
        """
        if not isinstance(other, JClassType):
            return False
        if self.full_name == other.full_name:
            return True
        if other.full_name in self.assignable_from:
            return True
        return any(base.can_assign_from(other) for base in self.bases)

    def get_members(self) -> dict[str, JClassMember]:
        """
        Returns all accessible instance-level members, including inherited ones.

        Returns:
            dict[str, JClassMember]: A dictionary of member names to member definitions.
        """
        all_members = dict(self.instance_members)
        for base in self.bases:
            all_members.update(base.get_members())
        return all_members
    
    def get_callable_signature(self) -> JFunctionType:
        """
        Returns the callable signature for this class (i.e., its constructor).

        Looks for an `__init__` method among instance members. If not found,
        assumes a default constructor with no parameters.

        Returns:
            JFunctionType: The function type describing the constructor signature.
        """
        init = self.instance_members.get("__init__")
        if init and isinstance(init.type, JFunctionType):
            return init.type
        return JFunctionType([], self)
    
    def supports_binary_op(self, op):
        """
        Checks whether a binary operator is supported by this class type.

        Delegates to the class-level member list to find an appropriate method.

        Args:
            op (str): The operator symbol (e.g., '+', '==').

        Returns:
            bool: True if a corresponding method exists; False otherwise.
        """
        return op in self.class_members
