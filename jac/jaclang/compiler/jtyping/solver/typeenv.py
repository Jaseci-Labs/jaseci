from jaclang.compiler.unitree import NameAtom
from jaclang.compiler.jtyping import JType
from jaclang.compiler.jtyping.constraint import JTypeConstraint
from jaclang.settings import settings


class JTypeEnv: 

    def __init__(self) -> None:
        self.__map: dict[NameAtom, JType] = {}
        self.__constraints: list[JTypeConstraint] = []
    
    def __debug_print(self, msg: str) -> None:
        if settings.debug_jac_typing:
            print("[JTypeEnv]", msg)
    
    def insert(self, name: NameAtom, type_: JType) -> None:
        """Insert a new type into the environment."""
        if name in self.__map:
            raise ValueError(f"Name {name} already exists in the environment.")
        self.__map[name] = type_
    
    def lookup(self, name: NameAtom) -> JType:
        """Lookup a type in the environment."""
        if name not in self.__map:
            raise KeyError(f"Name {name} not found in the environment.")
        return self.__map[name]
    
    def has(self, name: NameAtom) -> bool:
        return name in self.__map

    def insert_constraint(self, constraint: JTypeConstraint) -> None:
        self.__constraints.append(constraint)
        self.__debug_print(str(constraint))
