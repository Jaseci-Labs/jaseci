"""Core constructs for Jac Language."""

from contextvars import ContextVar
from dataclasses import asdict, is_dataclass
from os import getenv
from typing import Any, Callable, cast

from bson import ObjectId

from fastapi import Request

from .architype import (
    AccessLevel,
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

    request: Request
    datasource: MongoDB
    reports: list
    super_root: NodeAnchor
    root: NodeAnchor
    entry: NodeAnchor

    def generate_super_root(self) -> NodeAnchor:
        """Generate default super root."""
        super_root = NodeAnchor(
            id=SUPER_ROOT, state=AnchorState(current_access_level=AccessLevel.WRITE)
        )
        architype = super_root.architype = object.__new__(Root)
        architype.__jac__ = super_root
        self.datasource.set(super_root)
        return super_root

    def generate_public_root(self) -> NodeAnchor:
        """Generate default super root."""
        public_root = NodeAnchor(
            id=PUBLIC_ROOT,
            access=Permission(all=AccessLevel.WRITE),
            state=AnchorState(current_access_level=AccessLevel.WRITE),
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
                    _anchor.state.current_access_level = AccessLevel.WRITE
                    return _anchor
            else:
                self.datasource.set(anchor)
                return anchor

        return default() if callable(default) else default

    async def validate_access(self) -> bool:
        """Validate access."""
        return await self.root.has_read_access(self.entry)

    async def close(self) -> None:
        """Clean up context."""
        await self.datasource.close()

    @staticmethod
    async def create(
        request: Request, entry: NodeAnchor | None = None
    ) -> "JaseciContext":
        """Create JacContext."""
        ctx = JaseciContext()
        ctx.request = request
        ctx.datasource = MongoDB()
        ctx.reports = []
        ctx.super_root = await ctx.load(
            NodeAnchor(id=SUPER_ROOT), ctx.generate_super_root
        )
        ctx.root = await ctx.load(
            getattr(request, "_root", None) or NodeAnchor(id=PUBLIC_ROOT),
            ctx.generate_public_root,
        )
        ctx.entry = await ctx.load(entry, ctx.root)

        if _ctx := JASECI_CONTEXT.get(None):
            await _ctx.close()
        JASECI_CONTEXT.set(ctx)

        return ctx

    @staticmethod
    def get() -> "JaseciContext":
        """Get current ExecutionContext."""
        if not isinstance(ctx := JASECI_CONTEXT.get(None), JaseciContext):
            raise Exception("JaseciContext is not yet available!")
        return ctx

    @staticmethod
    def get_datasource() -> MongoDB:
        """Get current datasource."""
        return JaseciContext.get().datasource

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
