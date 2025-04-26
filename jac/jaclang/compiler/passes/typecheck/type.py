from __future__ import annotations


class JType:
    def is_assignable_from(self, other: JType) -> bool:
        return isinstance(other, self.__class__)

    def __repr__(self) -> str:
        return self.__class__.__name__.replace("J", "").replace("Type", "").lower()


class JIntType(JType):
    def is_assignable_from(self, other: JType) -> bool:
        return isinstance(other, (JIntType, JBoolType))


class JFloatType(JType):
    def is_assignable_from(self, other: JType) -> bool:
        return isinstance(other, (JFloatType, JIntType, JBoolType))


class JBoolType(JType):
    def is_assignable_from(self, other: JType) -> bool:
        return isinstance(other, (JBoolType))


class JStrType(JType):
    def is_assignable_from(self, other: JType) -> bool:
        return isinstance(other, (JStrType))


class JNoneType(JType):
    def is_assignable_from(self, other: JType) -> bool:
        return isinstance(other, (JNoneType))


class JNoType(JType):
    def is_assignable_from(self, other: JType) -> bool:
        return True
