"""Core constructs for Jac Language."""

from __future__ import annotations

from contextvars import ContextVar
from os import getenv
from typing import Any, Callable, Optional, Union, cast

from bson import ObjectId

from fastapi import Request

from .architype import Anchor, AnchorType, Architype, NodeAnchor, Root
from .memory import MongoDB


SHOW_ENDPOINT_RETURNS = getenv("SHOW_ENDPOINT_RETURNS") == "true"
JASECI_CONTEXT = ContextVar[Optional["JaseciContext"]]("JaseciContext")
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
        self.super_root: Optional[NodeAnchor] = None
        self.root: Optional[NodeAnchor] = None
        self.entry: Optional[NodeAnchor] = None

    async def build(
        self, request: Optional[Request] = None, entry: Optional[NodeAnchor] = None
    ) -> None:
        """Async build JacContext."""
        self.request = request
        self.super_root = await self.load(
            NodeAnchor(id=SUPER_ROOT), self.generate_super_root
        )
        self.root = getattr(request, "_root", None) or await self.load(
            NodeAnchor(id=PUBLIC_ROOT), self.generate_public_root
        )
        self.entry = await self.load(entry, self.root)

    def generate_super_root(self) -> NodeAnchor:
        """Generate default super root."""
        super_root = NodeAnchor(id=SUPER_ROOT, current_access_level=2)
        architype = super_root.architype = object.__new__(Root)
        architype.__jac__ = super_root
        self.datasource.set(super_root)
        return super_root

    def generate_public_root(self) -> NodeAnchor:
        """Generate default super root."""
        public_root = NodeAnchor(id=PUBLIC_ROOT, current_access_level=2)
        architype = public_root.architype = object.__new__(Root)
        architype.__jac__ = public_root
        self.datasource.set(public_root)
        return public_root

    async def load(
        self,
        anchor: Optional[NodeAnchor],
        default: Union[NodeAnchor, Callable[[], NodeAnchor]],
    ) -> NodeAnchor:
        """Load initial anchors."""
        if anchor and (
            _anchor := await self.datasource.find_one(AnchorType.node, anchor.id)
        ):
            anchor.__dict__.update(_anchor.__dict__)
            anchor.current_access_level = 2
        else:
            anchor = default() if callable(default) else default
        return anchor

    def validate_access(self) -> bool:
        """Validate access."""
        return bool(self.root and self.entry and self.root.has_read_access(self.entry))

    async def close(self) -> None:
        """Clean up context."""
        await self.datasource.close()

    @staticmethod
    def get(options: Optional[dict[str, Any]] = None) -> JaseciContext:
        """Get or create execution context."""
        if not isinstance(ctx := JASECI_CONTEXT.get(None), JaseciContext):
            JASECI_CONTEXT.set(ctx := JaseciContext(**options or {}))
        return ctx

    def response(self, returns: list[Any], status: int = 200) -> dict[str, Any]:
        """Return serialized version of reports."""
        resp = {"status": status, "returns": returns}

        if self.reports:
            for key, val in enumerate(self.reports):
                match val:
                    case Anchor():
                        self.reports[key] = val.report()
                    case Architype():
                        self.reports[key] = val.__jac__.report()
                    case _:
                        self.clean_response(key, val, self.reports)
            resp["reports"] = self.reports

        if not SHOW_ENDPOINT_RETURNS:
            resp.pop("returns")

        return resp

    def clean_response(
        self, key: Union[str, int], val: Any, obj: Union[list, dict]  # noqa: ANN401
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
            case _:
                pass
