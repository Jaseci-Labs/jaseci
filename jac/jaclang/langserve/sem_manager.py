"""Semantic Token Manager module."""

from __future__ import annotations

from typing import List, Optional, Tuple

import jaclang.compiler.absyntree as ast
from jaclang.langserve.utils import (
    find_surrounding_tokens,
    get_line_of_code,
    get_token_start,
)

import lsprotocol.types as lspt


class SemTokManager:
    """Semantic Token Manager class."""

    def __init__(self, ir: ast.Module) -> None:
        """Initialize semantic token manager."""
        self.sem_tokens: List[int] = self.gen_sem_tokens(ir)
        self.static_sem_tokens: List[
            Tuple[lspt.Position, int, int, ast.AstSymbolNode]
        ] = self.gen_sem_tok_node(ir)

    def gen_sem_tokens(self, ir: ast.Module) -> list[int]:
        """Return semantic tokens."""
        tokens = []
        prev_line, prev_col = 0, 0
        for node in ir._in_mod_nodes:
            if isinstance(node, ast.NameAtom) and node.sem_token:
                line, col_start, col_end = (
                    node.loc.first_line - 1,
                    node.loc.col_start - 1,
                    node.loc.col_end - 1,
                )
                length = col_end - col_start
                tokens += [
                    line - prev_line,
                    col_start if line != prev_line else col_start - prev_col,
                    length,
                    *node.sem_token,
                ]
                prev_line, prev_col = line, col_start
        return tokens

    def gen_sem_tok_node(
        self, ir: ast.Module
    ) -> List[Tuple[lspt.Position, int, int, ast.AstSymbolNode]]:
        """Return semantic tokens."""
        tokens: List[Tuple[lspt.Position, int, int, ast.AstSymbolNode]] = []
        for node in ir._in_mod_nodes:
            if isinstance(node, ast.NameAtom) and node.sem_token:
                line, col_start, col_end = (
                    node.loc.first_line - 1,
                    node.loc.col_start - 1,
                    node.loc.col_end - 1,
                )
                length = col_end - col_start
                pos = lspt.Position(line, col_start)
                tokens += [(pos, col_end, length, node)]
        return tokens

    def update_sem_tokens(
        self,
        content_changes: lspt.DidChangeTextDocumentParams,
        sem_tokens: list[int],
        document_lines: List[str],
    ) -> list[int]:
        """Update semantic tokens on change."""
        import logging

        def find_token_based_on_line(line: int, sem_tokens: list[int]) -> int:
            for i, j in enumerate(
                [get_token_start(i, sem_tokens) for i in range(0, len(sem_tokens), 5)]
            ):
                if j[0] == line:
                    return i + 1
            return -1

        if len(content_changes.content_changes) == 2:

            x1 = content_changes.content_changes[0]
            x2 = content_changes.content_changes[1]
            change1_start_line = x2.range.start.line
            change2_start_line = x2.range.end.line
            last_line = x1.range.end.line
            last_last_line_token_index = (
                find_token_based_on_line(last_line + 1, sem_tokens) - 1
            )
            line_delta = change2_start_line - change1_start_line
            if change2_start_line > change1_start_line:
                first_token_index = find_token_based_on_line(
                    change1_start_line, sem_tokens
                )
                last_token_index = (
                    find_token_based_on_line(change1_start_line + 1, sem_tokens) - 1
                )
                f1 = ((first_token_index - 1) * 5) - 1
                l2 = (last_token_index * 5) - 1
                tokens_in_line = sem_tokens[f1 + 1 : l2 + 1]
                last_token_index = (
                    find_token_based_on_line(last_line + 1, sem_tokens) - 1
                )
                final_tok_index = (last_last_line_token_index) * 5
                b11 = sem_tokens[:final_tok_index]
                a11 = sem_tokens[final_tok_index:]
                sem_tokens = b11 + tokens_in_line + a11
                f11 = sem_tokens[: f1 + 1]
                l11 = sem_tokens[l2 + 1 :]
                sem_tokens = f11 + l11
                logging.info(f"semmm tok1111\n\n {sem_tokens}")
                return sem_tokens
            else:
                logging.info("Moving down")
            logging.info(f"semmm tok {sem_tokens}")
            return sem_tokens

        for change in [
            x
            for x in content_changes.content_changes
            if isinstance(x, lspt.TextDocumentContentChangeEvent_Type1)
        ]:
            change_start_line = change.range.start.line
            change_start_char = change.range.start.character
            change_end_line = change.range.end.line
            change_end_char = change.range.end.character

            is_delete = change.text == ""
            prev_token_index, next_token_index, insert_inside_token = (
                find_surrounding_tokens(
                    change_start_line,
                    change_start_char,
                    change_end_line,
                    change_end_char,
                    sem_tokens,
                )
            )
            prev_tok_pos = get_token_start(prev_token_index, sem_tokens)
            nxt_tok_pos = get_token_start(next_token_index, sem_tokens)
            changing_line_text = get_line_of_code(change_start_line, document_lines)
            if not changing_line_text:
                return sem_tokens
            is_edit_between_tokens = bool(
                (
                    change_start_line > prev_tok_pos[0]
                    or (
                        change_start_line == prev_tok_pos[0]
                        and change_start_char
                        > prev_tok_pos[1] + sem_tokens[prev_token_index + 2]
                        if prev_token_index and prev_token_index + 2 < len(sem_tokens)
                        else 0
                    )
                )
                and (
                    change_end_line < nxt_tok_pos[0]
                    or (
                        change_end_line == nxt_tok_pos[0]
                        and change_end_char < nxt_tok_pos[1]
                    )
                )
            )
            text = r"%s" % change.text
            line_delta = len(text.split("\n")) - 1

            is_multiline_insertion = line_delta > 0
            is_next_token_same_line = change_end_line == nxt_tok_pos[0]

            if is_delete:
                next_token_index = (
                    prev_token_index + 5
                    if insert_inside_token
                    and prev_token_index is not None
                    or (
                        next_token_index
                        and prev_token_index is not None
                        and next_token_index >= 10
                        and next_token_index - prev_token_index == 10
                    )
                    else next_token_index
                )
                if next_token_index is None:
                    return sem_tokens
                nxt_tok_pos = get_token_start(next_token_index, sem_tokens)
                is_single_line_change = change_end_line == change_start_line
                is_next_token_same_line = change_end_line == nxt_tok_pos[0]
                if (
                    is_single_line_change
                    and insert_inside_token
                    and prev_token_index is not None
                ):
                    sem_tokens = SemTokManager.handle_single_line_delete(
                        sem_tokens,
                        next_token_index,
                        prev_token_index,
                        is_next_token_same_line,
                        change,
                    )
                elif is_single_line_change and is_edit_between_tokens:
                    sem_tokens = SemTokManager.handle_single_line_delete_between_tokens(
                        sem_tokens,
                        next_token_index,
                        is_next_token_same_line,
                        change,
                        change_start_line,
                        change_end_line,
                    )
                else:
                    sem_tokens = SemTokManager.handle_multi_line_delete(
                        sem_tokens,
                        next_token_index,
                        nxt_tok_pos,
                        change_start_line,
                        change_end_line,
                        change_start_char,
                        change_end_char,
                        prev_tok_pos,
                        is_next_token_same_line,
                    )
                return sem_tokens

            is_token_boundary_edit = False
            if insert_inside_token and prev_token_index is not None:
                sem_tokens, is_token_boundary_edit, nxt_tok_pos, next_token_index = (
                    SemTokManager.handle_insert_inside_token(
                        change,
                        sem_tokens,
                        prev_token_index,
                        changing_line_text,
                        line_delta,
                        prev_tok_pos,
                        change_start_char,
                        change_end_char,
                        is_token_boundary_edit,
                        nxt_tok_pos,
                    )
                )
            tokens_on_same_line = prev_tok_pos[0] == nxt_tok_pos[0]
            if (
                is_edit_between_tokens
                or is_token_boundary_edit
                or is_multiline_insertion
            ) and next_token_index is not None:
                if is_multiline_insertion:
                    sem_tokens = SemTokManager.handle_multi_line_insertion(
                        sem_tokens,
                        next_token_index,
                        nxt_tok_pos,
                        change_start_line,
                        change_end_line,
                        change_end_char,
                        prev_tok_pos,
                        tokens_on_same_line,
                        changing_line_text,
                        line_delta,
                    )
                else:
                    sem_tokens = SemTokManager.handle_single_line_insertion(
                        sem_tokens,
                        next_token_index,
                        is_next_token_same_line,
                        change,
                        tokens_on_same_line,
                        nxt_tok_pos,
                        change_start_line,
                        line_delta,
                    )
        return sem_tokens

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
    ) -> list[int]:
        """Handle multi line deletion."""
        if is_next_token_same_line:
            char_del = nxt_tok_pos[1] - change_end_char
            total_char_del = change_start_char + char_del
            sem_tokens[next_token_index + 1] = (
                (total_char_del - prev_tok_pos[1])
                if prev_tok_pos[0] == change_start_line
                else total_char_del
            )
        sem_tokens[next_token_index] -= change_end_line - change_start_line
        return sem_tokens

    @staticmethod
    def handle_single_line_delete_between_tokens(
        sem_tokens: list[int],
        next_token_index: int,
        is_next_token_same_line: bool,
        change: lspt.TextDocumentContentChangeEvent_Type1,
        change_start_line: int,
        change_end_line: int,
    ) -> list[int]:
        """Handle single line deletion between tokens."""
        if is_next_token_same_line:
            sem_tokens[next_token_index + 1] -= change.range_length

        else:
            sem_tokens[next_token_index] -= change_end_line - change_start_line
        return sem_tokens

    @staticmethod
    def handle_single_line_delete(
        sem_tokens: list[int],
        next_token_index: int,
        prev_token_index: int,
        is_next_token_same_line: bool,
        change: lspt.TextDocumentContentChangeEvent_Type1,
    ) -> list[int]:
        """Handle single line deletion."""
        sem_tokens[prev_token_index + 2] -= change.range_length
        if is_next_token_same_line:
            sem_tokens[next_token_index + 1] -= change.range_length
        return sem_tokens

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
    ) -> list[int]:
        """Handle single line insertion."""
        if tokens_on_same_line:
            sem_tokens[next_token_index + 1] += len(change.text)
            sem_tokens[next_token_index] += line_delta
        else:
            is_next_token_same_line = change_start_line == nxt_tok_pos[0]
            if is_next_token_same_line:
                sem_tokens[next_token_index] += line_delta
                sem_tokens[next_token_index + 1] += len(change.text)
            else:
                sem_tokens[next_token_index] += line_delta
        return sem_tokens

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
    ) -> list[int]:
        """Handle multi line insertion."""
        if tokens_on_same_line:
            char_del = nxt_tok_pos[1] - change_end_char
            total_char_del = changing_line_text[1] + char_del

        else:
            is_prev_token_same_line = change_end_line == prev_tok_pos[0]
            is_next_token_same_line = change_start_line == nxt_tok_pos[0]
            if is_prev_token_same_line:
                total_char_del = nxt_tok_pos[1]
            elif is_next_token_same_line:
                char_del = nxt_tok_pos[1] - change_end_char
                total_char_del = changing_line_text[1] + char_del
            else:
                total_char_del = sem_tokens[next_token_index + 1]
                line_delta -= change_end_line - change_start_line
        sem_tokens[next_token_index + 1] = total_char_del
        sem_tokens[next_token_index] += line_delta
        return sem_tokens

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
    ) -> tuple[list[int], bool, tuple[int, int, int], Optional[int]]:
        """Handle insert inside token."""
        next_token_index = None
        for i in ["\n", " ", "\t"]:
            if i in change.text:
                if prev_tok_pos[1] == change_start_char:
                    if i == "\n":
                        sem_tokens[prev_token_index] += line_delta
                        sem_tokens[prev_token_index + 1] = changing_line_text[1]
                    else:
                        sem_tokens[prev_token_index + 1] += len(change.text)
                    return (
                        sem_tokens,
                        is_token_boundary_edit,
                        nxt_tok_pos,
                        next_token_index,
                    )
                else:
                    is_token_boundary_edit = True
                    next_token_index = prev_token_index + 5
                    nxt_tok_pos = get_token_start(next_token_index, sem_tokens)
                    break
        if not is_token_boundary_edit:
            selected_region = change_end_char - change_start_char
            index_offset = 2
            sem_tokens[prev_token_index + index_offset] += (
                len(change.text) - selected_region
            )
            if prev_tok_pos[0] == get_token_start(prev_token_index + 5, sem_tokens)[0]:
                sem_tokens[prev_token_index + index_offset + 4] += (
                    len(change.text) - selected_region
                )
        return sem_tokens, is_token_boundary_edit, nxt_tok_pos, next_token_index
