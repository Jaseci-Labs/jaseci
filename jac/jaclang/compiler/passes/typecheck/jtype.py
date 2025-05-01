"""Builtin types for Jac."""

from __future__ import annotations

from abc import ABC, abstractmethod


class JType(ABC):
    """Base class for jac builtin types."""

    def is_assignable_from(self, other: JType) -> bool:
        """Check if type can be assigned from another type."""
        return (
            isinstance(self, JNoType)
            or isinstance(other, self.__class__)
            or self._is_assignable_from(other)
        )

    @abstractmethod
    def _is_assignable_from(self, other: JType) -> bool:
        pass

    def __repr__(self) -> str:
        """Generate string representation of the object."""
        return self.__class__.__name__.replace("J", "").replace("Type", "").lower()


class JIntType(JType):
    """Jac int type."""

    def _is_assignable_from(self, other: JType) -> bool:
        return isinstance(other, (JIntType, JBoolType))


class JFloatType(JType):
    """Jac float type."""

    def _is_assignable_from(self, other: JType) -> bool:
        return isinstance(other, (JFloatType, JIntType, JBoolType))


class JBoolType(JType):
    """Jac bool type."""

    def _is_assignable_from(self, other: JType) -> bool:
        return isinstance(other, (JBoolType,))


class JStrType(JType):
    """Jac str type."""

    def _is_assignable_from(self, other: JType) -> bool:
        return isinstance(other, (JStrType,))


class JNoneType(JType):
    """Jac none type."""

    def _is_assignable_from(self, other: JType) -> bool:
        return isinstance(other, (JNoneType,))


class JNoType(JType):
    """Jac no type."""

    def _is_assignable_from(self, other: JType) -> bool:
        return True


class JCallableType(JType):
    """Jac functions/abilities."""

    def __init__(
        self,
        param_types: dict[str, JType],
        return_type: JType,
        is_assignable: bool = False,
    ) -> None:
        """Create a callable type for jac language."""
        self.param_types = param_types
        self.return_type = return_type
        self.is_assignable = is_assignable

    def _is_assignable_from(self, other: JType) -> bool:
        # TODO: Do we really need to support function assginments?
        return False

    def __repr__(self) -> str:
        """Generate string representation of the JCallableType object."""
        params: str = ""
        for p in self.param_types:
            params += f"{p},"
        if params.endswith(","):
            params = params[:-1]
        return f"Callable[{self.return_type}, [{params}]]"


# class JUserType(JType):
#     """User defined types & builtin types."""

#     def __init__(
#         self,
#         name: str,
#         fields: dict[str, JType],
#         methods:
#     ):
#         super().__init__()
