"""Jac Machine module."""

from __future__ import annotations

import os
import types
from concurrent.futures import ThreadPoolExecutor
from dataclasses import MISSING
from typing import Any, Callable, Optional, cast
from uuid import UUID

from jaclang.compiler.constant import Constants as Con
from jaclang.compiler.program import JacProgram
from jaclang.runtimelib.architype import NodeAnchor, Root
from jaclang.runtimelib.memory import Memory, ShelfStorage
from jaclang.utils.log import logging

logger = logging.getLogger(__name__)


def call_jac_func_with_machine(
    mach: JacMachineState, func: Callable, *args: Any  # noqa: ANN401
) -> Any:  # noqa: ANN401
    """Call Jac function with machine context in local."""
    __jac_mach__ = mach  # noqa: F841
    return func(*args)


class ExecutionContext:
    """Execution Context."""

    mach: JacMachineState
    mem: Memory
    reports: list[Any]
    custom: Any = MISSING
    system_root: NodeAnchor
    root: NodeAnchor
    entry_node: NodeAnchor

    def __init__(
        self,
        mach: JacMachineState,
        session: Optional[str] = None,
        root: Optional[str] = None,
    ) -> None:
        """Create ExecutionContext."""
        self.mach = mach
        self.mem = ShelfStorage(session)
        self.reports = []
        sr_arch = Root()
        sr_anch = sr_arch.__jac__
        sr_anch.id = UUID(Con.SUPER_ROOT_UUID)
        sr_anch.persistent = False
        self.system_root = sr_anch
        if not isinstance(
            system_root := self.mem.find_by_id(UUID(Con.SUPER_ROOT_UUID)), NodeAnchor
        ):
            system_root = cast(NodeAnchor, Root().__jac__)  # type: ignore[attr-defined]
            system_root.id = UUID(Con.SUPER_ROOT_UUID)
            self.mem.set(system_root.id, system_root)

        self.system_root = system_root

        self.entry_node = self.root = self.init_anchor(root, self.system_root)

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
        call_jac_func_with_machine(mach=self.mach, func=self.mem.close)

    def get_root(self) -> Root:
        """Get current root."""
        return cast(Root, self.root.architype)

    def global_system_root(self) -> NodeAnchor:
        """Get global system root."""
        return self.system_root


class JacMachineState:
    """Jac Machine State."""

    def __init__(
        self,
        base_path: str = "",
        session: Optional[str] = None,
        root: Optional[str] = None,
        interp_mode: bool = False,
    ) -> None:
        """Initialize JacMachineState."""
        self.loaded_modules: dict[str, types.ModuleType] = {}
        if not base_path:
            base_path = os.getcwd()
        # Ensure the base_path is a list rather than a string
        self.base_path = base_path
        self.base_path_dir = (
            os.path.dirname(base_path)
            if not os.path.isdir(base_path)
            else os.path.abspath(base_path)
        )
        self.jac_program: JacProgram = JacProgram()
        self.interp_mode = interp_mode
        self.exec_ctx = ExecutionContext(session=session, root=root, mach=self)
        self.pool = ThreadPoolExecutor()
