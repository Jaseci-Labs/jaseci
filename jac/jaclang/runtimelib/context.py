"""Core constructs for Jac Language."""

from __future__ import annotations

from contextvars import ContextVar
from dataclasses import MISSING
from typing import Any, Optional, cast
from uuid import UUID

from .architype import NodeAnchor, Root
from .memory import Memory, ShelfStorage


EXECUTION_CONTEXT = ContextVar[Optional["ExecutionContext"]]("ExecutionContext")
SUPER_ROOT_UUID = UUID("00000000-0000-0000-0000-000000000000")


class ExecutionContext:
    """Execution Context."""

    mem: Memory
    reports: list[Any]
    custom: Any = MISSING
    system_root: NodeAnchor
    root: NodeAnchor
    entry_node: NodeAnchor

    def init_anchor(
        self,
        anchor_id: str | None,
        default: NodeAnchor,
    ) -> NodeAnchor:
        """Load initial anchors."""
        if anchor_id:
            if isinstance(anchor := self.mem.find_by_id(UUID(anchor_id)), NodeAnchor):
                return anchor
            raise ValueError(f"Invalid anchor id {anchor_id} !")
        return default

    def set_entry_node(self, entry_node: str | None) -> None:
        """Override entry."""
        self.entry_node = self.init_anchor(entry_node, self.root)

    def close(self) -> None:
        """Close current ExecutionContext."""
        self.mem.close()
        EXECUTION_CONTEXT.set(None)

    @staticmethod
    def create(
        session: Optional[str] = None,
        root: Optional[str] = None,
        auto_close: bool = True,
    ) -> ExecutionContext:
        """Create ExecutionContext."""

        ctx = ExecutionContext()
        ctx.mem = ShelfStorage(session)
        ctx.reports = []

        if not isinstance(
            system_root := ctx.mem.find_by_id(SUPER_ROOT_UUID), NodeAnchor
        ):
            system_root = cast(NodeAnchor, Root().__jac__)  # type: ignore[attr-defined]
            system_root.id = SUPER_ROOT_UUID
            ctx.mem.set(system_root.id, system_root)

        ctx.system_root = system_root

        ctx.entry_node = ctx.root = ctx.init_anchor(root, ctx.system_root)

        if auto_close and (old_ctx := EXECUTION_CONTEXT.get(None)):
            old_ctx.close()

        EXECUTION_CONTEXT.set(ctx)

        return ctx

    @staticmethod
    def get() -> ExecutionContext:
        """Get current ExecutionContext."""
        if ctx := EXECUTION_CONTEXT.get(None):
            return ctx
        raise Exception("ExecutionContext is not yet available!")

    @staticmethod
    def get_root() -> Root:
        """Get current root."""
        if ctx := EXECUTION_CONTEXT.get(None):
            return cast(Root, ctx.root.architype)

        return cast(Root, ExecutionContext.global_system_root().architype)

    @staticmethod
    def global_system_root() -> NodeAnchor:
        """Get global system root."""

        if not (sr_anch := getattr(ExecutionContext, "system_root", None)):
            sr_arch = Root()
            sr_anch = sr_arch.__jac__  # type: ignore[attr-defined]
            sr_anch.id = SUPER_ROOT_UUID
            sr_anch.persistent = False
            ExecutionContext.system_root = sr_anch
        return sr_anch
