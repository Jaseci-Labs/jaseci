"""
Defines the abstract base class `JType` for all types in the Jac type system.

This file provides a foundational interface for representing and reasoning about
types in Jac's static analysis and type-checking pipeline. It includes support
for instantiability, assignability, member access, callability, and operator overloading.

All specific type classes (e.g., primitives, classes, unions, generics, function types)
should inherit from `JType` and implement the required interface.
"""

from __future__ import annotations

from typing import Optional
from abc import ABC, abstractmethod

import jaclang.compiler.unitree as uni


class JType(ABC):
    """
    Abstract base class for all types in the Jac type system.

    This class defines the core interface that all type representations must implement.
    It supports instantiability checks, assignment compatibility, member introspection,
    operator overloading, and function call semantics.

    Attributes:
        name (str): The type's name (e.g., 'int', 'List', 'MyClass').
        module (Optional[uni.Module]): The module where the type is defined.
            Used for resolving qualified names and generating error messages.
    """

    def __init__(self, name: str, module: Optional[uni.Module]):
        self.name: str = name
        self.module: Optional[uni.Module] = module

    def can_assign_from(self, other: JType) -> bool:
        """
        Determines whether a value of `other` type can be assigned to a variable of this type.

        By default, this method enforces nominal compatibility by checking if `other`
        is an instance of the same class. Override this in subclasses to implement
        structural typing, subtype relationships, or union compatibility.

        Args:
            other (JType): The type of the value being assigned.

        Returns:
            bool: True if assignment is allowed; False otherwise.
        """
        return isinstance(other, self.__class__)
    
    def is_callable(self) -> bool:
        """
        Indicates whether the type can be used in a function call (i.e., is callable).

        Returns:
            bool: True if callable, False otherwise. Default is False.
        """
        return False

    @abstractmethod
    def is_instantiable(self) -> bool:
        """
        Indicates whether the type can be directly instantiated at runtime.

        For example, abstract classes or interfaces would return False,
        while concrete classes and primitives would return True.

        Returns:
            bool: True if instantiable, False otherwise.
        """
        ...

    @abstractmethod
    def get_members(self) -> dict:
        """
        Returns the accessible members of the type (e.g., methods, fields, properties).

        This is used to validate member access like `obj.foo` or to inspect operator support.

        Returns:
            dict: A dictionary mapping member names to JClassMember objects (or equivalent).
        """
        ...
    
    @abstractmethod
    def supports_binary_op(self, op: str) -> bool:
        """
        Checks whether a binary operator is supported by this type.

        The operator is internally mapped to its corresponding magic method (e.g., '+' to '__add__').
        The type is considered to support the operator if the corresponding method is present
        in its member list.

        Args:
            op (str): The operator symbol (e.g., '+', '*', '==').

        Returns:
            bool: True if the operator is supported; False otherwise.
        """
        method_name = _BINARY_OPERATOR_METHODS.get(op)
        if not method_name:
            return False
        members = self.get_members()
        return method_name in members

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}[{self.name}]"


# Mapping from binary operator symbols to their corresponding magic method names
_BINARY_OPERATOR_METHODS = {
    "+": "__add__",
    "-": "__sub__",
    "*": "__mul__",
    "/": "__truediv__",
    "//": "__floordiv__",
    "%": "__mod__",
    "**": "__pow__",
    "&": "__and__",
    "|": "__or__",
    "^": "__xor__",
    "<<": "__lshift__",
    ">>": "__rshift__",
    "==": "__eq__",
    "!=": "__ne__",
    "<": "__lt__",
    "<=": "__le__",
    ">": "__gt__",
    ">=": "__ge__",
}
