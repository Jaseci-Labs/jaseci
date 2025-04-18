from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional

import jaclang.compiler.absyntree as ast

class JType(ABC):
    def is_assignable_from(self, other: JType) -> bool:
        return isinstance(other, self.__class__)
    
    def __repr__(self):
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


def getBuiltinType(builtin_ast: ast.BuiltinType) -> Optional[JType]:
    type_map = {
        "TYP_INT": JIntType,
        "TYP_FLOAT": JFloatType,
        "TYP_STRING": JStrType,
        "TYP_BOOL": JBoolType
    }

    if builtin_ast.name in type_map:
        return type_map[builtin_ast.name]()
    else:
        return None