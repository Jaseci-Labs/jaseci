"""Core constructs for Jac Language."""

from contextvars import ContextVar
from dataclasses import asdict, is_dataclass
from os import getenv
from typing import Any, Callable, cast

from bson import ObjectId

from fastapi import Request

from .architype import (
    Anchor,
    AnchorState,
    Architype,
    NodeAnchor,
    Permission,
    Root,
)
from .memory import MongoDB


SHOW_ENDPOINT_RETURNS = getenv("SHOW_ENDPOINT_RETURNS") == "true"
JASECI_CONTEXT = ContextVar["JaseciContext | None"]("JaseciContext")
SUPER_ROOT = ObjectId("000000000000000000000000")
PUBLIC_ROOT = ObjectId("000000000000000000000001")


class JaseciContext:
    """Execution Context."""

    def __init__(
        self,
        **ignored: Any,  # noqa: ANN401
    ) -> None:
        """Create JacContext."""
        self.datasource: MongoDB = MongoDB()
        self.reports: list[Any] = []
        self.super_root: NodeAnchor | None = None
        self.root: NodeAnchor | None = None
        self.entry: NodeAnchor | None = None

    async def build(
        self, request: Request | None = None, entry: NodeAnchor | None = None
    ) -> None:
        """Async build JacContext."""
        self.request = request
        self.super_root = await self.load(
            NodeAnchor(id=SUPER_ROOT), self.generate_super_root
        )
        self.root = await self.load(
            getattr(request, "_root", None) or NodeAnchor(id=PUBLIC_ROOT),
            self.generate_public_root,
        )
        self.entry = await self.load(entry, self.root)

    def generate_super_root(self) -> NodeAnchor:
        """Generate default super root."""
        super_root = NodeAnchor(
            id=SUPER_ROOT, state=AnchorState(current_access_level=2)
        )
        architype = super_root.architype = object.__new__(Root)
        architype.__jac__ = super_root
        self.datasource.set(super_root)
        return super_root

    def generate_public_root(self) -> NodeAnchor:
        """Generate default super root."""
        public_root = NodeAnchor(
            id=PUBLIC_ROOT,
            access=Permission(all=2),
            state=AnchorState(current_access_level=2),
        )
        architype = public_root.architype = object.__new__(Root)
        architype.__jac__ = public_root
        self.datasource.set(public_root)
        return public_root

    async def load(
        self,
        anchor: NodeAnchor | None,
        default: NodeAnchor | Callable[[], NodeAnchor],
    ) -> NodeAnchor:
        """Load initial anchors."""
        if anchor:
            if not anchor.state.connected:
                if _anchor := await self.datasource.find_one(NodeAnchor, anchor):
                    _anchor.state.current_access_level = 2
                    return _anchor
            else:
                self.datasource.set(anchor)
                return anchor

        return default() if callable(default) else default

    async def validate_access(self) -> bool:
        """Validate access."""
        return bool(
            self.root and self.entry and await self.root.has_read_access(self.entry)
        )

    async def close(self) -> None:
        """Clean up context."""
        await self.datasource.close()

    @staticmethod
    def get_or_create(options: dict[str, Any] | None = None) -> "JaseciContext":
        """Get or create execution context."""
        if not isinstance(ctx := JASECI_CONTEXT.get(None), JaseciContext):
            JASECI_CONTEXT.set(ctx := JaseciContext(**options or {}))
        return ctx

    @staticmethod
    def get_datasource() -> MongoDB:
        """Get current datasource."""
        if not isinstance(ctx := JASECI_CONTEXT.get(None), JaseciContext):
            raise Exception("Wrong usage of get_datasource!")
        return ctx.datasource

    def response(self, returns: list[Any], status: int = 200) -> dict[str, Any]:
        """Return serialized version of reports."""
        resp = {"status": status, "returns": returns}

        if self.reports:
            for key, val in enumerate(self.reports):
                self.clean_response(key, val, self.reports)
            resp["reports"] = self.reports

        for key, val in enumerate(returns):
            self.clean_response(key, val, returns)

        if not SHOW_ENDPOINT_RETURNS:
            resp.pop("returns")

        return resp

    def clean_response(
        self, key: str | int, val: Any, obj: list | dict  # noqa: ANN401
    ) -> None:
        """Cleanup and override current object."""
        match val:
            case list():
                for idx, lval in enumerate(val):
                    self.clean_response(idx, lval, val)
            case dict():
                for key, dval in val.items():
                    self.clean_response(key, dval, val)
            case Anchor():
                cast(dict, obj)[key] = val.report()
            case Architype():
                cast(dict, obj)[key] = val.__jac__.report()
            case val if is_dataclass(val) and not isinstance(val, type):
                cast(dict, obj)[key] = asdict(val)
            case _:
                pass
