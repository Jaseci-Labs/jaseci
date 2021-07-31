# -*- coding: utf-8 -*-

# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    unicode
except NameError:
    unicode = str
    unichr = chr

import curses.ascii
import os
import re
import sys
import threading
import time
import traceback


from . import config, curses_util
from . import log
from . import regex

# Keys to tuples within |parserNodes|.
# Reference to a prefs grammar dictionary.
kGrammar = 0
# The current grammar begins at byte offset |kBegin| in the source data.
kBegin = 1
# An index into the parserNodes list to the prior (or parent) grammar.
kPrior = 2
# Some characters display wider (or narrower) than others. Visual is a running
# display offset. E.g. if the first character in some utf-8 data is a double
# width and 3 bytes long the kBegin = 0, and kVisual = 0; the second character
# will start at kBegin = 3, kVisual = 2.
kVisual = 3


class ParserNode:
    """A parser node represents a span of grammar. i.e. from this point to that
    point is HTML. Another parser node would represent the next segment, of
    grammar (maybe JavaScript, CSS, comment, or quoted string for example."""

    def __init__(self, grammar, begin, prior, visual):
        self.grammar = grammar
        # Offset from start of file.
        self.begin = begin
        # Index of prior grammar (like a stack of grammars).
        self.prior = prior
        # Visible width on screen (double wide chars, and tabs).
        self.visual = visual

    def debug_log(self, out, indent, data):
        out(
            "%sParserNode %26s prior %4s, b%4d, v%4d %s"
            % (
                indent,
                self.grammar.get("name", "None"),
                self.prior,
                self.begin,
                self.visual,
                repr(data[self.begin: self.begin + 15])[1:-1],
            )
        )


class Parser:
    """A parser generates a set of grammar segments (ParserNode objects)."""

    def __init__(self, appPrefs):
        self.appPrefs = appPrefs
        self._defaultGrammar = appPrefs.grammars["none"]
        self.data = u""
        self.emptyNode = ParserNode({}, None, None, 0)
        self.endNode = ({}, sys.maxsize, sys.maxsize, sys.maxsize)
        self.resumeAtRow = 0
        self.pauseAtRow = 0
        # A row on screen will consist of one or more ParserNodes. When a
        # ParserNode is returned from the parser it will be an instance of
        # ParserNode, but internally tuples are used in place of ParserNodes.
        # This makes for some ugly code, but the performance difference (~5%) is
        # worth it.
        self.parserNodes = [({}, 0, None, 0)]
        # Each entry in |self.rows| is an index into the |self.parserNodes|
        # array to the parerNode that begins that row.
        self.rows = [0]  # Row parserNodes index.
        log.parser("__init__")

    def backspace(self, row, col):
        """Delete the character prior to |row, col|.
        Return the new (row, col) position."""
        self._fully_parse_to(row)
        offset = self.data_offset(row, col)
        if offset == 0:
            # Top of file, nothing to do.
            return row, col
        if offset is None:
            # Bottom of file (or past end of line, but assuming end of file).
            offset = len(self.data)
        ch = self.data[offset - 1]
        if ch == u"\n":
            row -= 1
            col = self.row_width(row)
        elif ch == u"\t":
            col += self.prior_char_row_col(row, col)[1]
        elif curses_util.is_double_width(ch):
            col -= 2
        else:
            col -= 1
        self.data = self.data[: offset - 1] + self.data[offset:]
        self._begin_parsing_at(row)
        if config.strict_debug:
            assert isinstance(self.data, unicode)
            assert row >= 0
            assert col >= 0
        return row, col

    def data_offset(self, row, col):
        """Return the offset within self.data (as unicode, not utf-8) for the
        start of the character at (row, col).

        Normally this will be the character the cursor is 'on' when
        using a block cursor; or to the 'right' of the when using a vertical
        cursor. I.e. it would be the character deleted by the 'del' key.

        Returns: offset (int) into self.data buffer; or None if (row, col) is
            outside the document.
        """
        self._fully_parse_to(row)
        if row >= len(self.rows):
            return None
        rowIndex = self.rows[row]
        node = self.parserNodes[rowIndex]
        if row + 1 < len(self.rows):
            nextLineNode = self.parserNodes[self.rows[row + 1]]
            if col >= nextLineNode[kVisual] - node[kVisual]:
                # The requested column is past the end of the line.
                return None
        elif row + 1 == len(self.rows):
            # On the last row.
            if col >= self.parserNodes[-1][kVisual] - node[kVisual]:
                # The requested column is past the end of the line.
                return None
        else:
            # The requested column is past the end of the document.
            return None
        subnode = self.parserNodes[rowIndex +
                                   self.grammar_index_from_row_col(row, col)]
        subnodeCol = subnode[kVisual] - node[kVisual]
        subnodeColDelta = col - subnodeCol
        offset = subnode[kBegin]
        if self.data[offset] == u"\t":
            tabWidth = 8
            flooredTabGrammarCol = subnodeCol // tabWidth * tabWidth
            offset += (col - flooredTabGrammarCol) // tabWidth
        elif curses_util.is_double_width(self.data[offset]):
            char_width = 2
            offset += subnodeColDelta // char_width
        else:
            offset += subnodeColDelta
        return offset

    def data_offset_row_col(self, offset):
        """Get the (row, col) for the given data |offset| or None if the offset
        is beyond the file."""
        if config.strict_debug:
            assert isinstance(offset, int)
            assert offset >= 0
        # Binary search to find the row, then the col.
        nodes = self.parserNodes
        if offset >= nodes[-1][kBegin]:
            return None
        # Determine the row.
        rows = self.rows
        low = 0
        high = len(rows) - 1
        while True:
            row = (high + low) // 2
            if offset >= nodes[rows[row + 1]][kBegin]:
                low = row
            elif offset < nodes[rows[row]][kBegin]:
                high = row
            else:
                break
        # Determine the col.
        low = rows[row]
        high = rows[row + 1]
        while True:
            index = (high + low) // 2
            if offset >= nodes[index + 1][kBegin]:
                low = index
            elif offset < nodes[index][kBegin]:
                high = index
            else:
                break
        col = nodes[index][kVisual] - nodes[rows[row]][kVisual]
        remainingOffset = offset - nodes[index][kBegin]
        if remainingOffset > 0:
            ch = self.data[nodes[index][kBegin]]
            if ch == u"\t":
                tabWidth = self.appPrefs.editor.get(u"tabSize", 8)
                # Add the (potentially) fractional tab.
                col += curses_util.char_width(ch, col, tabWidth)
                # Add the remaining tabs.
                col += tabWidth * (remainingOffset - 1)
            else:
                col += curses_util.char_width(ch, col) * remainingOffset
        return row, col

    def default_grammar(self):
        return self._defaultGrammar

    def delete_block(self, upperRow, upperCol, lowerRow, lowerCol):
        for row in range(lowerRow, upperRow - 1, -1):
            begin = self.data_offset(row, upperCol)
            end = self.data_offset(row, lowerCol)
            if end is None:
                if begin is not None:
                    self.data = self.data[:begin]
            else:
                self.data = self.data[:begin] + self.data[end:]
        self._begin_parsing_at(upperRow)

    def delete_char(self, row, col):
        """Delete the character after (or "at") |row, col|."""
        self._fully_parse_to(row)
        offset = self.data_offset(row, col)
        if offset is None:
            # Bottom of file, nothing to do.
            return
        self.data = self.data[:offset] + self.data[offset + 1:]
        self._begin_parsing_at(row)

    def delete_range(self, upperRow, upperCol, lowerRow, lowerCol):
        begin = self.data_offset(upperRow, upperCol)
        end = self.data_offset(lowerRow, lowerCol)
        if end is None:
            if begin is not None:
                self.data = self.data[:begin]
        else:
            self.data = self.data[:begin] + self.data[end:]
        self._begin_parsing_at(upperRow)

    def text_range(self, upperRow, upperCol, lowerRow, lowerCol):
        begin = self.data_offset(upperRow, upperCol)
        end = self.data_offset(lowerRow, lowerCol)
        if end is None:
            if begin is not None:
                return self.data[begin:]
        return self.data[begin:end]

    def grammar_index_from_row_col(self, row, col):
        """
        tip: as an optimization, check if |col == 0| prior to calling. The
            result will always be zero (so the call can be avoided).

        Returns:
            index. |index| may then be passed to grammar_at_index().
        """
        if config.strict_debug:
            assert isinstance(row, int)
            assert isinstance(col, int)
            assert row >= 0
            assert col >= 0
        self._fully_parse_to(row)
        if config.strict_debug:
            assert row < len(self.rows), (row, len(self.rows), repr(self.data))
        if row == len(self.rows) - 1:
            # The last line.
            assert row + 1 >= len(self.rows)
            gl = self.parserNodes[self.rows[row]:] + [self.endNode]
        else:
            gl = self.parserNodes[self.rows[row]
                : self.rows[row + 1]] + [self.endNode]
        offset = gl[0][kVisual] + col
        # Binary search to find the node for the column.
        low = 0
        high = len(gl) - 1
        while True:
            index = (high + low) // 2
            if offset >= gl[index + 1][kVisual]:
                low = index
            elif offset < gl[index][kVisual]:
                high = index
            else:
                # assert index < len(gl)  # Never return index to self.endNode.
                return index

    def grammar_at(self, row, col):
        """Get the grammar at row, col.
        It's more efficient to use grammar_index_from_row_col() and grammar_at_index()
        individually if grammars are requested contiguously. This function is
        just for one-off needs.
        """
        self._fully_parse_to(row)
        grammarIndex = self.grammar_index_from_row_col(row, col)
        node, _, _, _ = self.grammar_at_index(row, col, grammarIndex)
        return node.grammar

    def grammar_at_index(self, row, col, index):
        """Call grammar_index_from_row_col() to get the index parameter.

        Returns:
            (node, preceding, remaining, eol). |proceeding| and |remaining| are
            relative to the |col| parameter.
        """
        if config.strict_debug:
            assert isinstance(row, int)
            assert isinstance(col, int)
            assert isinstance(index, int)
            assert row < len(self.rows), row
        self._fully_parse_to(row)
        eol = True
        finalResult = (self.emptyNode, 0, 0, eol)
        rowIndex = self.rows[row]
        if rowIndex + index + 1 >= len(self.parserNodes):
            return finalResult
        nextOffset = self.parserNodes[rowIndex + index + 1][kVisual]
        offset = self.parserNodes[rowIndex][kVisual] + col
        remaining = nextOffset - offset
        if remaining < 0:
            return finalResult
        node = self.parserNodes[rowIndex + index]
        eol = False
        return ParserNode(*node), offset - node[kVisual], remaining, eol

    def grammar_text_at(self, row, col):
        """Get the run of text for the given position."""
        if config.strict_debug:
            assert isinstance(row, int)
            assert isinstance(col, int)
            assert row < len(self.rows), row
        self._fully_parse_to(row)
        rowIndex = self.rows[row]
        grammarIndex = self.grammar_index_from_row_col(row, col)
        node = self.parserNodes[rowIndex + grammarIndex]
        nextNode = self.parserNodes[rowIndex + grammarIndex + 1]
        return (
            self.data[node[kBegin]: nextNode[kBegin]],
            node[kGrammar].get(u"link_type"),
        )

    def in_document(self, row, col):
        if config.strict_debug:
            assert isinstance(row, int)
            assert isinstance(col, int)
            assert row >= 0
            assert col >= 0
        self._fully_parse_to(row)
        return row < len(self.rows) and col < self.parserNodes[self.rows[row]][kVisual]

    def insert(self, row, col, text):
        if config.strict_debug:
            assert isinstance(row, int)
            assert isinstance(col, int)
            assert isinstance(text, unicode)
            assert row >= 0
            assert col >= 0
            assert len(text) > 0
        offset = self.data_offset(row, col)
        if offset is None:
            row = len(self.rows) - 1
            self.data += text
        else:
            self.data = self.data[:offset] + text + self.data[offset:]
        self._begin_parsing_at(row)

    def insert_block(self, row, col, lines):
        for i in range(len(lines) - 1, -1, -1):
            offset = self.data_offset(row + i, col)
            if offset is None:
                self.data += lines[i]
            else:
                self.data = self.data[:offset] + lines[i] + self.data[offset:]
        self._begin_parsing_at(row)

    def insert_lines(self, row, col, lines):
        if config.strict_debug:
            assert isinstance(row, int)
            assert isinstance(col, int)
            # assert isinstance(lines, tuple)
            assert row >= 0
            assert col >= 0
            assert len(lines) > 0
        text = u"\n".join(lines)
        self.insert(row, col, text)

    def next_char_row_col(self, row, col):
        """Get the next column value for the character to the right.
        Returns: None if there is no remaining characters.
                 or (row, col) deltas of the next character in the document.
        """
        if config.strict_debug:
            assert isinstance(row, int)
            assert isinstance(col, int)
            assert row >= 0
            assert col >= 0
            assert len(self.rows) > 0
        self._fully_parse_to(row)
        ch = self.char_at(row, col)
        if ch is None:
            return (1, -col) if self.in_document(row + 1, 0) else None
        return 0, curses_util.char_width(ch, col)

    def prior_char_row_col(self, row, col):
        """Get the prior column value for the character to the left.
        Returns: None if there is no remaining characters.
                 or (row, col) deltas of the next character in the document.
        """
        if config.strict_debug:
            assert isinstance(row, int)
            assert isinstance(col, int)
            assert row >= 0
            assert col >= 0
            assert len(self.rows) > 0
        self._fully_parse_to(row)
        if col == 0:
            if row == 0:
                return None
            return (-1, self.row_width(row - 1))
        return 0, curses_util.prior_char_col(col, self.row_text(row)) - col

    def parse(self, bgThread, data, grammar, beginRow, endRow):
        """
        Args:
          data (string): The file contents. The document.
          grammar (object): The initial grammar (often determined by the file
              extension). If |beginRow| is not zero then grammar is ignored.
          beginRow (int): is the first row (which is line number - 1) in data
              that is has changed since the previous parse of this data. Pass
              zero to parse the entire document. If beginRow >= len(data) then
              no parse is done.
          endRow (int): The row to stop parsing. This stops the parser from
              going over the entire file if, for example, only 100 rows out of
              a million rows are needed (which can save a lot of cpu time).
        """
        if config.strict_debug:
            assert bgThread is None or isinstance(bgThread, threading.Thread)
            assert isinstance(data, unicode), type(data)
            assert isinstance(grammar, dict)
            assert isinstance(beginRow, int)
            assert isinstance(endRow, int)
            assert beginRow >= 0
            assert endRow >= 0
            assert isinstance(self.appPrefs, prefs.Prefs)
        self._defaultGrammar = grammar
        self.emptyNode = ParserNode(grammar, None, None, 0)
        self.data = data
        self._begin_parsing_at(beginRow)
        self._fully_parse_to(endRow, bgThread)
        # self.debug_check_lines(log.parser, data)
        # startTime = time.time()
        if log.enabledChannels.get("parser", False):
            self.debug_log(log.parser, data)
        # log.startup('parsing took', time.time() - startTime)

    def _begin_parsing_at(self, beginRow):
        if config.strict_debug:
            assert isinstance(beginRow, int)
            assert beginRow >= 0, beginRow
            assert isinstance(self.resumeAtRow, int)
            assert self.resumeAtRow >= 0, self.resumeAtRow
        if beginRow > self.resumeAtRow:
            # Already beginning at an earlier row.
            return
        if beginRow > 0:
            # Trim partially parsed data.
            if beginRow < len(self.rows):
                self.parserNodes = self.parserNodes[: self.rows[beginRow]]
                self.rows = self.rows[:beginRow]
            self.resumeAtRow = len(self.rows)
        else:
            # Parse the whole file.
            self.parserNodes = [(self.default_grammar(), 0, None, 0)]
            self.rows = [0]
            self.resumeAtRow = 0

    def _fast_line_parse(self, grammar):
        """If there's not enough time to thoroughly parse the file, identify the
        lines so that the document can still be edited.
        """
        data = self.data
        offset = self.parserNodes[-1][kBegin]
        limit = len(data)
        if offset == limit:
            # Already parsed to end of data.
            return
        visual = self.parserNodes[-1][kVisual]

        # Track the |visual| value for the start of the line. The difference
        # between |visual| and |visualStartCol| is the column index of the line.
        visualStartCol = 0
        while True:
            while offset < limit and data[offset] != "\n":
                if data[offset] < u"ᄀ":
                    # The char is less than the first double width character.
                    # (An optimization to avoid calling char_width().)
                    visual += 1
                else:
                    # From here on, the width of the character is messy to
                    # determine, ask an authority.
                    visual += curses_util.char_width(
                        data[offset], visual - visualStartCol
                    )
                offset += 1
            if offset >= limit:
                # The document is missing the last new-line.
                if self.parserNodes[-1][kBegin] != limit:
                    # Add a terminating (end) node.
                    self.parserNodes.append((grammar, limit, None, visual))
                break
            visualStartCol = visual
            offset += 1
            visual += 1
            self.rows.append(len(self.parserNodes))
            self.parserNodes.append((grammar, offset, None, visual))

    def _fully_parse_to(self, endRow, bgThread=None):
        """Parse up to and including |endRow|."""
        if config.strict_debug:
            assert isinstance(endRow, int)
            assert endRow >= 0
            assert bgThread is None or isinstance(bgThread, threading.Thread)
        # To parse |endRow| go one past because of the exclusive end of range.
        self.pauseAtRow = endRow + 1
        if self.pauseAtRow <= self.resumeAtRow:
            # Already parsed to that row.
            return
        self._begin_parsing_at(self.resumeAtRow)
        if len(self.rows) <= self.pauseAtRow:
            self._build_grammar_list(bgThread)
        self._fast_line_parse(self.default_grammar())
        if config.strict_debug:
            assert self.resumeAtRow >= 0
            assert self.resumeAtRow <= len(self.rows)
            if bgThread is not None and endRow <= len(self.rows):
                assert self.resumeAtRow >= endRow + \
                    1, (self.resumeAtRow, endRow)

    def row_count(self):
        self._fast_line_parse(self.default_grammar())
        return len(self.rows)

    def row_text(self, row, beginCol=None, endCol=None):
        """Get the text for |row|.

        Args:
            row (int): row is zero based.
            beginCol (int): subindex within the row (similar to a slice).
            endCol (int): subindex within the row (similar to a slice).

        Returns:
            document text (unicode)
        """
        if config.strict_debug:
            assert isinstance(row, int)
            assert beginCol is None or isinstance(beginCol, int)
            assert endCol is None or isinstance(endCol, int)
            assert row >= 0
            assert isinstance(self.data, unicode)
        self._fully_parse_to(row)
        if beginCol is endCol is None:
            begin = self.parserNodes[self.rows[row]][kBegin]
            if row + 1 >= len(self.rows):
                return self.data[begin:]
            end = self.parserNodes[self.rows[row + 1]][kBegin]
            if len(self.data) and self.data[end - 1] == u"\n":
                end -= 1
            return self.data[begin:end]

        if beginCol >= 0:
            begin = self.data_offset(row, beginCol)
        else:
            width = self.row_width(row)
            begin = self.data_offset(row, width + beginCol)

        if begin is None:
            return u""

        if endCol is None:
            end = self.data_offset(row + 1, 0)
        elif endCol < 0:
            width = self.row_width(row)
            end = self.data_offset(row, width + endCol)
        else:
            width = self.row_width(row)
            if endCol >= width:
                endCol = width
            end = self.data_offset(row, endCol)

        if end is None:
            end = len(self.data)
        if end > 0 and self.data[end - 1] == u"\n":
            end -= 1

        return self.data[begin:end]

    def char_at(self, row, col):
        """Get the character at |row|, |col|.

        Args:
            row (int): zero based index into list of rows.
            col (int): zero based visual offset from start of line.

        Returns:
            character (unicode) or None if row, col is outside of the document.
        """
        if config.strict_debug:
            assert isinstance(row, int)
            assert isinstance(col, int)
            assert isinstance(self.data, unicode)
            assert row >= 0
            assert col >= 0
        self._fully_parse_to(row)
        if row > len(self.rows):
            return None
        string, width = self.row_text_and_width(row)
        if col > width:
            return None
        return curses_util.char_at_column(col, string)

    def row_text_and_width(self, row):
        """Get the character data and the visual/display column width of those
        characters.

        If the text is all ASCII then len(text) will equal the column width. If
        there are double wide characters (e.g. Chinese or some emoji) the column
        width may be larger than len(text).

        Args:
            row (int): the row index is zero based (so it's line number - 1).

        Returns:
            (text, column_width) (tuple)
        """
        if config.strict_debug:
            assert isinstance(row, int)
        self._fully_parse_to(row)
        begin = self.parserNodes[self.rows[row]][kBegin]
        visual = self.parserNodes[self.rows[row]][kVisual]
        if row + 1 < len(self.rows):
            end = self.parserNodes[self.rows[row + 1]][kBegin]
            visualEnd = self.parserNodes[self.rows[row + 1]][kVisual]
            if len(self.data) and self.data[end - 1] == "\n":
                end -= 1
                visualEnd -= 1
        else:
            # There is a sentinel node at the end that records the end of
            # document.
            lastNode = self.parserNodes[-1]
            end = lastNode[kBegin]
            visualEnd = lastNode[kVisual]
        return self.data[begin:end], visualEnd - visual

    def row_width(self, row):
        """Get the visual/display column width of a row.

        If the text is all ASCII then len(text) will equal the column width. If
        there are double wide characters (e.g. Chinese or some emoji) the column
        width may be larger than len(text).

        Args:
            row (int): the row index is zero based (so it's `line_number - 1`).

        Returns:
            column_width (int)
        """
        if config.strict_debug:
            assert isinstance(row, int)
        if row < 0:
            row = len(self.rows) + row
        self._fully_parse_to(row)
        visual = self.parserNodes[self.rows[row]][kVisual]
        if row + 1 < len(self.rows):
            end = self.parserNodes[self.rows[row + 1]][kBegin]
            visualEnd = self.parserNodes[self.rows[row + 1]][kVisual]
            if len(self.data) and self.data[end - 1] == "\n":
                visualEnd -= 1
        else:
            # There is a sentinel node at the end that records the end of
            # document.
            lastNode = self.parserNodes[-1]
            visualEnd = lastNode[kVisual]
        return visualEnd - visual

    def _build_grammar_list(self, bgThread):
        """The guts of the parser. This is where the heavy lifting is done.

        This code can be interrupted (by |bgThread|) and resumed (by calling it
        again).
        """
        appPrefs = self.appPrefs
        # An arbitrary limit to avoid run-away looping.
        leash = 50000
        topNode = self.parserNodes[-1]
        cursor = topNode[kBegin]
        visual = topNode[kVisual]
        # If we are at the start of a grammar, skip the 'begin' part of the
        # grammar.
        if 0:
            if (
                len(self.parserNodes) == 1
                or (topNode[kGrammar] is not self.parserNodes[-2][kGrammar])
                and topNode[kGrammar].get("end") is not None
            ):
                beginRegex = topNode[kGrammar].get("begin")
                if beginRegex is not None:
                    sre = re.match(beginRegex, self.data[cursor:])
                    if sre is not None:
                        assert False
                        cursor += sre.regs[0][1]
                        # Assumes single-wide characters.
                        visual += sre.regs[0][1]
        while len(self.rows) <= self.pauseAtRow:
            if not leash:
                # log.error('grammar likely caught in a loop')
                break
            leash -= 1
            if bgThread and bgThread.has_user_event():
                break
            subdata = self.data[cursor:]
            found = self.parserNodes[-1][kGrammar].get(
                "matchRe").search(subdata)
            if not found:
                # log.info('parser exit, match not found')
                # todo(dschuyler): mark parent grammars as unterminated (if they
                # expect be terminated). e.g. unmatched string quote or xml tag.
                if cursor != len(self.data):
                    # The last bit of the last line.
                    self.parserNodes.append(
                        (topNode[kGrammar], cursor, topNode[kPrior], visual)
                    )
                break
            index = -1
            foundGroups = found.groups()
            for k in foundGroups:
                index += 1
                if k is not None:
                    break
            reg = found.regs[index + 1]
            if index == 0:
                # Found escaped value.
                cursor += reg[1]
                visual += reg[1]
                continue
            if index == len(foundGroups) - 1:
                # Found new line.
                child = (
                    self.parserNodes[-1][kGrammar],
                    cursor + reg[1],
                    self.parserNodes[-1][kPrior],
                    visual + reg[1],
                )
                cursor += reg[1]
                visual += reg[1]
                self.rows.append(len(self.parserNodes))
            elif index == len(foundGroups) - 2:
                # Found potentially double wide characters.
                topNode = self.parserNodes[-1]
                regBegin, regEnd = reg
                width = curses_util.char_width
                if regBegin > 0:
                    # Add single wide characters.
                    self.parserNodes.append(
                        (topNode[kGrammar], cursor, topNode[kPrior], visual)
                    )
                    cursor += regBegin
                    visual += regBegin
                    regEnd -= regBegin
                    regBegin = 0
                while regBegin < regEnd:
                    # Check for zero width characters.
                    while (
                        regBegin < regEnd
                        and width(self.data[cursor + regBegin], 0) == 0
                    ):
                        regBegin += 1
                    if regBegin > 0:
                        # Add zero width characters.
                        self.parserNodes.append(
                            (topNode[kGrammar], cursor,
                             topNode[kPrior], visual)
                        )
                        cursor += regBegin
                        regEnd -= regBegin
                        regBegin = 0
                    # Check for single wide characters.
                    while (
                        regBegin < regEnd
                        and width(self.data[cursor + regBegin], 0) == 1
                    ):
                        regBegin += 1
                    if regBegin > 0:
                        # Add single wide characters.
                        self.parserNodes.append(
                            (topNode[kGrammar], cursor,
                             topNode[kPrior], visual)
                        )
                        cursor += regBegin
                        visual += regBegin
                        regEnd -= regBegin
                        regBegin = 0
                    # Check for double wide characters.
                    while (
                        regBegin < regEnd
                        and width(self.data[cursor + regBegin], 0) == 2
                    ):
                        regBegin += 1
                    if regBegin > 0:
                        # Add double wide characters.
                        self.parserNodes.append(
                            (topNode[kGrammar], cursor,
                             topNode[kPrior], visual)
                        )
                        cursor += regBegin
                        visual += regBegin * 2
                        regEnd -= regBegin
                        regBegin = 0
                continue
            elif index == len(foundGroups) - 3:
                # Found variable width (tab) character.
                topNode = self.parserNodes[-1]
                regBegin, regEnd = reg
                # First, add any preceding single wide characters.
                if regBegin > 0:
                    self.parserNodes.append(
                        (topNode[kGrammar], cursor, topNode[kPrior], visual)
                    )
                    cursor += regBegin
                    visual += regBegin
                    # Remove the regular text from reg values.
                    regEnd -= regBegin
                    regBegin = 0
                # Add tabs grammar; store the variable width characters.
                rowStart = self.parserNodes[self.rows[-1]][kVisual]
                col = visual - rowStart
                # Advance to the next tab stop.
                self.parserNodes.append(
                    (appPrefs.grammars["tabs"],
                     cursor, topNode[kPrior], visual)
                )
                cursor += regEnd
                visual = rowStart + ((col + 8) // 8 * 8)
                visual += (regEnd - 1) * 8
                # Resume current grammar; store the variable width characters.
                child = (topNode[kGrammar], cursor, topNode[kPrior], visual)
            elif index == 1:
                # Found end of current grammar section (an 'end').
                child = (
                    self.parserNodes[self.parserNodes[-1][kPrior]][kGrammar],
                    cursor + reg[1],
                    self.parserNodes[self.parserNodes[-1][kPrior]][kPrior],
                    visual + reg[1],
                )
                cursor = child[kBegin]
                visual += reg[1]
                if subdata[reg[1] - 1] == "\n":
                    # This 'end' ends with a new line.
                    self.rows.append(len(self.parserNodes))
            else:
                [
                    containsGrammarIndexLimit,
                    nextGrammarIndexLimit,
                    errorIndexLimit,
                    keywordIndexLimit,
                    typeIndexLimit,
                    specialIndexLimit,
                ] = self.parserNodes[-1][kGrammar]["indexLimits"]
                if index < containsGrammarIndexLimit:
                    # A new grammar within this grammar (a 'contains').
                    if subdata[reg[0]] == "\n":
                        # This 'begin' begins with a new line.
                        self.rows.append(len(self.parserNodes))
                    priorGrammar = self.parserNodes[-1][kGrammar].get(
                        "matchGrammars", []
                    )[index]
                    if priorGrammar["end"] is None:
                        # Found single regex match (a leaf grammar).
                        self.parserNodes.append(
                            (
                                priorGrammar,
                                cursor + reg[0],
                                len(self.parserNodes) - 1,
                                visual + reg[0],
                            )
                        )
                        # Resume the current grammar.
                        child = (
                            self.parserNodes[self.parserNodes[-1]
                                             [kPrior]][kGrammar],
                            cursor + reg[1],
                            self.parserNodes[self.parserNodes[-1]
                                             [kPrior]][kPrior],
                            visual + reg[1],
                        )
                    else:
                        if priorGrammar.get("end_key"):
                            # A dynamic end tag.
                            hereKey = re.search(
                                priorGrammar["end_key"], subdata[reg[0]:]
                            ).groups()[0]
                            markers = priorGrammar["markers"]
                            markers[1] = priorGrammar["end"].replace(
                                r"\0", re.escape(hereKey)
                            )
                            priorGrammar["matchRe"] = re.compile(
                                regex.join_re_list(markers)
                            )
                        child = (
                            priorGrammar,
                            cursor + reg[0],
                            len(self.parserNodes) - 1,
                            visual + reg[0],
                        )
                    cursor += reg[1]
                    visual += reg[1]
                elif index < nextGrammarIndexLimit:
                    # A new grammar follows this grammar (a 'begin').
                    if subdata[reg[0]] == "\n":
                        # This 'begin' begins with a new line.
                        self.rows.append(len(self.parserNodes))
                    priorGrammar = self.parserNodes[-1][kGrammar].get(
                        "matchGrammars", []
                    )[index]
                    if priorGrammar.get("end_key"):
                        # A dynamic end tag.
                        hereKey = re.search(
                            priorGrammar["end_key"], subdata[reg[0]:]
                        ).groups()[0]
                        markers = priorGrammar["markers"]
                        markers[1] = priorGrammar["end"].replace(
                            r"\0", re.escape(hereKey)
                        )
                        priorGrammar["matchRe"] = re.compile(
                            regex.join_re_list(markers)
                        )
                    child = (
                        priorGrammar,
                        cursor + reg[0],
                        len(self.parserNodes) - 2,
                        visual + reg[0],
                    )
                    cursor += reg[1]
                    visual += reg[1]
                elif index < errorIndexLimit:
                    # A special doesn't change the nodeIndex.
                    self.parserNodes.append(
                        (
                            appPrefs.grammars["error"],
                            cursor + reg[0],
                            len(self.parserNodes) - 1,
                            visual + reg[0],
                        )
                    )
                    # Resume the current grammar.
                    child = (
                        self.parserNodes[self.parserNodes[-1]
                                         [kPrior]][kGrammar],
                        cursor + reg[1],
                        self.parserNodes[self.parserNodes[-1][kPrior]][kPrior],
                        visual + reg[1],
                    )
                    cursor += reg[1]
                    visual += reg[1]
                elif index < keywordIndexLimit:
                    # A keyword doesn't change the nodeIndex.
                    self.parserNodes.append(
                        (
                            appPrefs.grammars["keyword"],
                            cursor + reg[0],
                            len(self.parserNodes) - 1,
                            visual + reg[0],
                        )
                    )
                    # Resume the current grammar.
                    child = (
                        self.parserNodes[self.parserNodes[-1]
                                         [kPrior]][kGrammar],
                        cursor + reg[1],
                        self.parserNodes[self.parserNodes[-1][kPrior]][kPrior],
                        visual + reg[1],
                    )
                    cursor += reg[1]
                    visual += reg[1]
                elif index < typeIndexLimit:
                    # A type doesn't change the nodeIndex.
                    self.parserNodes.append(
                        (
                            appPrefs.grammars["type"],
                            cursor + reg[0],
                            len(self.parserNodes) - 1,
                            visual + reg[0],
                        )
                    )
                    # Resume the current grammar.
                    child = (
                        self.parserNodes[self.parserNodes[-1]
                                         [kPrior]][kGrammar],
                        cursor + reg[1],
                        self.parserNodes[self.parserNodes[-1][kPrior]][kPrior],
                        visual + reg[1],
                    )
                    cursor += reg[1]
                    visual += reg[1]
                elif index < specialIndexLimit:
                    # A special doesn't change the nodeIndex.
                    self.parserNodes.append(
                        (
                            appPrefs.grammars["special"],
                            cursor + reg[0],
                            len(self.parserNodes) - 1,
                            visual + reg[0],
                        )
                    )
                    # Resume the current grammar.
                    child = (
                        self.parserNodes[self.parserNodes[-1]
                                         [kPrior]][kGrammar],
                        cursor + reg[1],
                        self.parserNodes[self.parserNodes[-1][kPrior]][kPrior],
                        visual + reg[1],
                    )
                    cursor += reg[1]
                    visual += reg[1]
                else:
                    log.error("invalid grammar index")
            self.parserNodes.append(child)
        self.resumeAtRow = len(self.rows)

    def _print_last_node(self, msg):
        node = self.parserNodes[-1]
        print(
            "_print_node",
            node[0]["name"],
            node[1],
            node[2],
            node[3],
            msg,
            repr(self.data),
        )

    def _print_node(self, node, msg):
        print("_print_node", node[0]["name"], node[1], node[2], node[3], msg)

    def debug_log(self, out, data):
        out("parser debug:")
        out("RowList ----------------", len(self.rows))
        for i, start in enumerate(self.rows):
            if i + 1 < len(self.rows):
                end = self.rows[i + 1]
            else:
                end = len(self.parserNodes)
            out("row", i, "(line", str(i + 1) + ") index", start, "to", end)
            for node in self.parserNodes[start:end]:
                if node is None:
                    out("a None")
                    continue
                nodeBegin = node[kBegin]
                out(
                    "  ParserNode %26s prior %4s, b%4d, v%4d, %s"
                    % (
                        node[kGrammar].get("name", "None"),
                        node[kPrior],
                        nodeBegin,
                        node[kVisual],
                        repr(data[nodeBegin: nodeBegin + 15])[1:-1],
                    )
                )

    def debug_check_lines(self, out, data):
        """Debug test that all the lines were recognized by the parser. This is
        very slow, so it's normally disabled.
        """
        # Check that all the lines got identified.
        lines = data.split(u"\n")
        if out is not None:
            out(lines)
        assert len(lines) == self.row_count()
        for i, line in enumerate(lines):
            parsedLine, column_width = self.row_text_and_width(i)
            assert line == parsedLine, "\nexpected:{}\n  actual:{}".format(
                repr(line), repr(parsedLine)
            )
            parsedLine = self.row_text(i)
            assert line == parsedLine, "\nexpected:{}\n  actual:{}".format(
                line, parsedLine
            )

            if out is not None:
                out("----------- ", line)
            piecedLine = u""
            k = 0
            grammarIndex = 0
            while True:
                node, preceding, remaining, eol = self.grammar_at_index(
                    i, k, grammarIndex
                )
                grammarIndex += 1
                piecedLine += line[k - preceding: k + remaining]
                if out is not None:
                    out(i, preceding, remaining, i, k, piecedLine)
                if eol:
                    assert piecedLine == line, "\nexpected:{}\n  actual:{}".format(
                        repr(line), repr(piecedLine)
                    )
                    break
                k += remaining
