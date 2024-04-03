from typing import Optional


class SemInfo:
    def __init__(
        self, name: str, type: Optional[str] = None, semstr: Optional[str] = None
    ) -> None:
        self.name = name
        self.type = type
        self.semstr = semstr


class Scope:
    def __init__(self, scope: str, type: str, parent: Optional["Scope"] = None) -> None:
        self.parent = parent
        self.type = type
        self.scope = scope

    def __str__(self) -> str:
        if self.parent:
            return f"{self.parent}.{self.scope}({self.type})"
        return f"{self.scope}({self.type})"


class Registry:
    def __init__(self) -> None:
        self.registry: dict[Scope, list[SemInfo]] = {}

    def add(self, scope: Scope, seminfo: SemInfo) -> None:
        for k in self.registry.keys():
            if str(k) == str(scope):
                scope = k
                break
        else:
            self.registry[scope] = []
        self.registry[scope].append(seminfo)
        

    def pp(self) -> None:
        for k, v in self.registry.items():
            print(k)
            for i in v:
                print(f"  {i.name} {i.type} {i.semstr}")
