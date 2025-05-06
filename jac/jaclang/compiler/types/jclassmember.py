"""
Defines `JClassMember`, the abstraction for class members in the Jac type system.

This includes methods, fields, and properties—whether static, instance-level,
or class-level. Members also have visibility (public/private/protected) and
metadata describing their behavior.
"""

from __future__ import annotations
from enum import Enum

from jaclang.compiler.types import JType


class MemberKind(Enum):
    """
    Enumerates the kinds of class members.

    Values:
        INSTANCE: A member accessed through an instance of the class.
        STATIC: A static member accessed directly via the class, without an instance.
        CLASS: A class method accessed with the class as an implicit first argument.
    """
    INSTANCE = "instance"
    STATIC = "static"
    CLASS = "class"


class Visibility(Enum):
    """
    Enumerates visibility levels for class members.

    Values:
        PUBLIC: Accessible from anywhere.
        PRIVATE: Accessible only within the defining class.
        PROTECTED: Accessible within the defining class and subclasses.
    """
    PUBLIC = "public"
    PRIVATE = "private"
    PROTECTED = "protected"


class JClassMember:
    """
    Represents a member (field, method, or property) of a class in the Jac type system.

    Members are used in type checking, member access resolution, and callable invocation.

    Attributes:
        name (str): The member's identifier (e.g., 'foo', '__init__').
        type (JType): The type of the member (e.g., return type for methods, value type for fields).
        kind (MemberKind): Describes how the member is accessed (instance, static, class).
        visibility (Visibility): Visibility level for access control.
        is_property (bool): True if the member is a property or getter.
        is_method (bool): True if the member is callable (i.e., a method or function).
    """

    def __init__(
        self,
        name: str,
        type: JType,
        kind: MemberKind = MemberKind.INSTANCE,
        visibility: Visibility = Visibility.PUBLIC,
        is_property: bool = False,
        is_method: bool = False,
    ):
        """
        Initialize a JClassMember.

        Args:
            name (str): The name of the member.
            type (JType): The type of the member.
            kind (MemberKind): The kind of member (instance, static, class). Defaults to INSTANCE.
            visibility (Visibility): The visibility of the member. Defaults to PUBLIC.
            is_property (bool): True if the member is a property. Defaults to False.
            is_method (bool): True if the member is callable. Defaults to False.
        """
        self.name: str = name
        self.type: JType = type
        self.kind: MemberKind = kind
        self.visibility: Visibility = visibility
        self.is_property: bool = is_property
        self.is_method: bool = is_method

    def __repr__(self) -> str:
        return (
            f"JClassMember(name={self.name}, type={self.type.name}, "
            f"kind={self.kind.name}, visibility={self.visibility.name}, "
            f"is_property={self.is_property}, is_method={self.is_method})"
        )
