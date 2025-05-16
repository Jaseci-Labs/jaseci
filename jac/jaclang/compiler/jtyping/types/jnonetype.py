"""
Defines `JNoneType`, representing the singleton `None` type in the Jac type system.
"""

from jaclang.compiler.jtyping.types.jtype import JType


class JNoneType(JType):
    """
    Represents the `None` type in the Jac type system.

    The `None` type is a special singleton type that is not instantiable
    and can only be assigned from other `None` values.

    It is commonly used in union types to model optionality.
    """

    def __init__(self):
        super().__init__(name="None", module=None)

    def is_instantiable(self) -> bool:
        """
        Indicates whether this type can be instantiated.

        Returns:
            bool: Always False for `None`.
        """
        return False

    def can_assign_from(self, other: JType) -> bool:
        """
        Checks if a value of the given type can be assigned to `None`.

        Args:
            other (JType): The type of the value being assigned.

        Returns:
            bool: True only if `other` is also `JNoneType`.
        """
        return isinstance(other, JNoneType)

    def get_members(self) -> dict:
        """
        Returns an empty set of members — `None` has no accessible attributes.

        Returns:
            dict: Always empty.
        """
        return {}

    # TODO: Check this when it comes to support binary operations
    def supports_binary_op(self, op: str) -> bool:
        """
        Indicates whether a binary operator is supported.

        `None` does not support any meaningful binary operations.

        Args:
            op (str): Operator symbol.

        Returns:
            bool: Always False.
        """
        return False
