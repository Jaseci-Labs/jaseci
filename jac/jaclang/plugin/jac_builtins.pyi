from __future__ import annotations

from typing import Optional

from jaclang.runtimelib.constructs import Architype, NodeArchitype

class Jac:
    def node_dot(
        root: any,
    ) -> str: ...
    def jid() -> str: ...
