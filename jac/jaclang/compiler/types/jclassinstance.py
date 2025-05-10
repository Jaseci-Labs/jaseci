"""
class_instance_type.py

Defines `JClassInstanceType`, representing the type of instances of user-defined
or primitive classes in the Jac type system.

This type wraps a `JClassType` and provides instance-level behavior.
"""

from jaclang.compiler.types import JType, JClassType, JClassMember


class JClassInstanceType(JType):
    """
    Represents an instance of a class in the Jac type system.

    This wraps a `JClassType` and provides:
    - Instance-level member access
    - Assignability based on class hierarchy
    - Support for instantiation semantics

    Attributes:
        class_type (JClassType): The class this instance belongs to.
    """

    def __init__(self, class_type: JClassType):
        """
        Initialize a JClassInstanceType from a class type.

        Args:
            class_type (JClassType): The originating class type.
        """
        self.class_type = class_type
        super().__init__(name=f"instance of {class_type.name}", module=class_type.module)

    def is_instantiable(self) -> bool:
        """
        Indicates whether the instance can be created directly.

        Returns:
            bool: Always True — an instance is already instantiated.
        """
        return True

    def can_assign_from(self, other: JType) -> bool:
        """
        Check if another instance type can be assigned to this one.

        Delegates to the assignability of their respective class types.

        Args:
            other (JType): The type to compare.

        Returns:
            bool: True if assignable based on class hierarchy.
        """
        if not isinstance(other, JClassInstanceType):
            return False
        return self.class_type.can_assign_from(other.class_type)

    def get_members(self) -> dict[str, JClassMember]:
        """
        Get members accessible on the instance.

        Delegates to the instance members of the class type.

        Returns:
            dict[str, JClassMember]: Instance-level member dictionary.
        """
        return self.class_type.get_members()

    #TODO: Check this when it comes to support binary operations
    def supports_binary_op(self, op: str) -> bool:
        """
        Check whether the instance supports a binary operator.

        Delegates to the class's instance-level member list.

        Args:
            op (str): Operator symbol (e.g., '+', '==').

        Returns:
            bool: True if a corresponding method like `__add__` exists.
        """
        return False
    
    def is_callable(self) -> bool:
        """
        Indicates whether the instance can be called like a function.

        Returns:
            bool: Always False for class instances.
        """
        return False
