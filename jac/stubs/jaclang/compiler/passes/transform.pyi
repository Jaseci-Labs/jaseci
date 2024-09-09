import abc
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from jaclang.compiler.absyntree import AstNode as AstNode, T as T
from jaclang.compiler.codeloc import CodeLocInfo as CodeLocInfo
from jaclang.utils.log import logging as logging
from typing import Generic

class Alert:
    msg: Incomplete
    loc: Incomplete
    from_pass: Incomplete
    def __init__(
        self, msg: str, loc: CodeLocInfo, from_pass: type[Transform]
    ) -> None: ...

class Transform(ABC, Generic[T], metaclass=abc.ABCMeta):
    logger: Incomplete
    errors_had: Incomplete
    warnings_had: Incomplete
    cur_node: Incomplete
    ir: Incomplete
    def __init__(self, input_ir: T, prior: Transform | None = None) -> None: ...
    @abstractmethod
    def transform(self, ir: T) -> AstNode: ...
    def log_error(self, msg: str, node_override: AstNode | None = None) -> None: ...
    def log_warning(self, msg: str, node_override: AstNode | None = None) -> None: ...
    def log_info(self, msg: str) -> None: ...
