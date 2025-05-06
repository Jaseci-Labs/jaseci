"""
Defines `JFunctionType`, the representation of callable function or method signatures
in the Jac type system.

Each function signature includes a return type and a list of arguments represented by
`JFuncArgument`, which models each parameter’s name, type, optionality, and default value.

This type is used for both standalone functions and methods on classes.
"""

from __future__ import annotations
from typing import List
from jaclang.compiler.types import JType, JFuncArgument


class JFunctionType(JType):
    """
    Represents a function or method signature in the Jac type system.

    This type encapsulates the complete signature of a callable, including:
    - Parameter names and types
    - Optionality of each argument
    - Static default values (if known)
    - Return type of the function

    Attributes:
        parameters (List[JFuncArgument]): Ordered list of function arguments,
            each including name, type, optional flag, and default value (if any).
        return_type (JType): The return type of the function.
    """

    def __init__(self, parameters: List[JFuncArgument], return_type: JType):
        """
        Initialize a JFunctionType with a parameter list and a return type.

        Args:
            parameters (List[JFuncArgument]): The function's parameters.
            return_type (JType): The return type of the function.
        """
        self.parameters = parameters
        self.return_type = return_type
        sig = ", ".join(repr(p) for p in parameters)
        name = f"({sig}) -> {return_type.name}"
        super().__init__(name=name, module=None)

    def is_callable(self) -> bool:
        """
        Indicates that this type is callable.

        Returns:
            bool: Always True for function types.
        """
        return True

    def get_param_names(self) -> List[str]:
        """
        Returns the list of parameter names.

        Returns:
            List[str]: Names of the parameters in declaration order.
        """
        return [p.name for p in self.parameters]

    def get_param_types(self) -> List[JType]:
        """
        Returns the list of parameter types.

        Returns:
            List[JType]: Types of the parameters in declaration order.
        """
        return [p.type for p in self.parameters]

    def get_callable_signature(self) -> JFunctionType:
        """
        Returns the callable signature of this function type.

        For compatibility with `JType.get_callable_signature()`.

        Returns:
            JFunctionType: This instance.
        """
        return self
