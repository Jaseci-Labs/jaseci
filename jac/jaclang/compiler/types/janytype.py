"""
Defines `JAnyType`, which represents the `Any` type in the Jac type system.

`Any` is a special type that disables static type checking in areas where type
information is unavailable, intentionally omitted, or too dynamic to resolve.

It is assignable to and from any type, and allows all operations without error.
This supports gradual typing, flexible inference, and integration with dynamic code.
"""

from jaclang.compiler.types import JType


class JAnyType(JType):
    """
    Represents the `Any` type in the Jac type system.

    The `Any` type is a special top type used when a variable or expression has
    unknown, unconstrained, or intentionally dynamic type. It disables type checking
    for any operations involving it and permits assignment to/from any other type.

    This is commonly used during:
    - Type inference failure
    - Unannotated function parameters or returns
    - Interaction with dynamic code or external systems

    Attributes:
        name (str): Always 'Any'.
    """

    def __init__(self):
        """
        Initialize the `Any` type.

        This type has no module and always uses the name 'Any'.
        """
        super().__init__(name="Any", module=None)

    def is_instantiable(self) -> bool:
        """
        Indicates whether this type is instantiable.

        Returns:
            bool: Always True for `Any`, since no constraint exists.
        """
        return True

    def can_assign_from(self, other: JType) -> bool:
        """
        Check whether a value of `other` can be assigned to this type.

        For `Any`, this always returns True, accepting any type.

        Args:
            other (JType): The type of the value being assigned.

        Returns:
            bool: Always True.
        """
        return True

    def get_members(self) -> dict:
        """
        Returns an empty member list.

        You may optionally override this to return all built-in methods
        if desired (like Mypy does with `Any`).

        Returns:
            dict: Always empty for now.
        """
        return {}

    def supports_binary_op(self, op: str) -> bool:
        """
        Indicates whether a binary operator is supported with this type.

        All operations are considered supported on `Any`.

        Args:
            op (str): Operator symbol (e.g., '+', '==').

        Returns:
            bool: Always True.
        """
        return True
