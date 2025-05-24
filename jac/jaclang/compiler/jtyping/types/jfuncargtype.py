"""
Defines `JFuncArgument`, which represents a single argument in a function or method
signature in the Jac type system.

Each argument includes its name, type, optionality.
This structure is used within `JFunctionType` to model callable signatures
and validate function calls.
"""

from jaclang.compiler.jtyping.types.jtype import JType


class JFuncArgument:
    """
    Represents a single parameter in a function or method signature.

    This abstraction allows the type system to model argument names, types,
    and whether arguments are optional. It is designed
    to support call validation, overload resolution, and introspection.

    Attributes:
        name (str): The name of the parameter.
        type (JType): The type of the parameter.
        is_optional (bool): Whether the argument is optional at the call site.
    """

    def __init__(
        self,
        name: str,
        type: JType,
        is_optional: bool = False,
    ):
        """
        Initialize a JFuncArgument.

        Args:
            name (str): The parameter name.
            type (JType): The type of the parameter.
            is_optional (bool): Whether the argument is optional. Defaults to False.
        """
        self.name = name
        self.type = type
        self.is_optional = is_optional

    def __repr__(self) -> str:
        """
        Return a human-readable representation of the function argument.

        Examples:
            x: int
            y?: str = 'hello'

        Returns:
            str: Readable string representing the parameter signature.
        """
        suffix = "?" if self.is_optional else ""
        return f"{self.name}{suffix}: {self.type.name}"
