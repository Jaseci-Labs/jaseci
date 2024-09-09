from _typeshed import Incomplete

class SemInfo:
    name: Incomplete
    type: Incomplete
    semstr: Incomplete
    def __init__(
        self, name: str, type: str | None = None, semstr: str = ""
    ) -> None: ...

class SemScope:
    parent: Incomplete
    type: Incomplete
    scope: Incomplete
    def __init__(
        self, scope: str, type: str, parent: SemScope | None = None
    ) -> None: ...
    @staticmethod
    def get_scope_from_str(scope_str: str) -> SemScope | None: ...
    @property
    def as_type_str(self) -> str | None: ...

class SemRegistry:
    registry: Incomplete
    def __init__(self) -> None: ...
    def add(self, scope: SemScope, seminfo: SemInfo) -> None: ...
    def lookup(
        self,
        scope: SemScope | None = None,
        name: str | None = None,
        type: str | None = None,
    ) -> tuple[SemScope | None, SemInfo | list[SemInfo] | None]: ...
    @property
    def module_scope(self) -> SemScope: ...
    def pp(self) -> str: ...
