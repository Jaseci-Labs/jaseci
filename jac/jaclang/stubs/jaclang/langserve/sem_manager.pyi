import jaclang.compiler.absyntree as ast
import lsprotocol.types as lspt
from _typeshed import Incomplete
from jaclang.langserve.utils import (
    find_surrounding_tokens as find_surrounding_tokens,
    get_line_of_code as get_line_of_code,
    get_token_start as get_token_start,
)

class SemTokManager:
    sem_tokens: Incomplete
    static_sem_tokens: Incomplete
    def __init__(self, ir: ast.Module) -> None: ...
    def gen_sem_tokens(self, ir: ast.Module) -> list[int]: ...
    def gen_sem_tok_node(
        self, ir: ast.Module
    ) -> list[tuple[lspt.Position, int, int, ast.AstSymbolNode]]: ...
    def update_sem_tokens(
        self,
        content_changes: lspt.DidChangeTextDocumentParams,
        sem_tokens: list[int],
        document_lines: list[str],
    ) -> list[int]: ...
    @staticmethod
    def handle_multi_line_delete(
        sem_tokens: list[int],
        next_token_index: int,
        nxt_tok_pos: tuple[int, int, int],
        change_start_line: int,
        change_end_line: int,
        change_start_char: int,
        change_end_char: int,
        prev_tok_pos: tuple[int, int, int],
        is_next_token_same_line: bool,
    ) -> list[int]: ...
    @staticmethod
    def handle_single_line_delete_between_tokens(
        sem_tokens: list[int],
        next_token_index: int,
        is_next_token_same_line: bool,
        change: lspt.TextDocumentContentChangeEvent_Type1,
        change_start_line: int,
        change_end_line: int,
    ) -> list[int]: ...
    @staticmethod
    def handle_single_line_delete(
        sem_tokens: list[int],
        next_token_index: int,
        prev_token_index: int,
        is_next_token_same_line: bool,
        change: lspt.TextDocumentContentChangeEvent_Type1,
    ) -> list[int]: ...
    @staticmethod
    def handle_single_line_insertion(
        sem_tokens: list[int],
        next_token_index: int,
        is_next_token_same_line: bool,
        change: lspt.TextDocumentContentChangeEvent_Type1,
        tokens_on_same_line: bool,
        nxt_tok_pos: tuple[int, int, int],
        change_start_line: int,
        line_delta: int,
    ) -> list[int]: ...
    @staticmethod
    def handle_multi_line_insertion(
        sem_tokens: list[int],
        next_token_index: int,
        nxt_tok_pos: tuple[int, int, int],
        change_start_line: int,
        change_end_line: int,
        change_end_char: int,
        prev_tok_pos: tuple[int, int, int],
        tokens_on_same_line: bool,
        changing_line_text: tuple[str, int],
        line_delta: int,
    ) -> list[int]: ...
    @staticmethod
    def handle_insert_inside_token(
        change: lspt.TextDocumentContentChangeEvent_Type1,
        sem_tokens: list[int],
        prev_token_index: int,
        changing_line_text: tuple[str, int],
        line_delta: int,
        prev_tok_pos: tuple[int, int, int],
        change_start_char: int,
        change_end_char: int,
        is_token_boundary_edit: bool,
        nxt_tok_pos: tuple[int, int, int],
    ) -> tuple[list[int], bool, tuple[int, int, int], int | None]: ...
