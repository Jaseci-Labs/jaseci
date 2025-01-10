from __future__ import annotations

from typing import Optional, Any

from jaclang.runtimelib.constructs import Architype, NodeArchitype

class Jac:
    @staticmethod
    def node_dot(
        root: Any,
    ) -> str: ...
    @staticmethod
    def jid() -> str: ...
