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
