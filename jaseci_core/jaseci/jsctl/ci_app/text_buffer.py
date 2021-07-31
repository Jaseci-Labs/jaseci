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

import curses
import re
import sys

from . import actions
from . import curses_util
from . import regex
from . import log
from . import parser
from . import selectable


class TextBuffer(actions.Actions):
    """The TextBuffer adds the drawing/rendering to the BackingTextBuffer."""

    def __init__(self, program):
        actions.Actions.__init__(self, program)
        self.lineLimitIndicator = 0
        self.highlightRe = None
        self.highlightCursorLine = False
        self.highlightTrailingWhitespace = True
        self.shouldReparse = False

    def check_scroll_to_cursor(self, window):
        """Move the selected view rectangle so that the cursor is visible."""
        maxRow, maxCol = window.rows, window.cols
        #     self.penRow >= self.view.scrollRow + maxRow 1 0
        rows = 0
        if self.view.scrollRow > self.penRow:
            rows = self.penRow - self.view.scrollRow
            log.error(
                "AAA self.view.scrollRow > self.penRow",
                self.view.scrollRow,
                self.penRow,
                self,
            )
        elif self.penRow >= self.view.scrollRow + maxRow:
            rows = self.penRow - (self.view.scrollRow + maxRow - 1)
            log.error(
                "BBB self.penRow >= self.view.scrollRow + maxRow cRow",
                self.penRow,
                "sRow",
                self.view.scrollRow,
                "maxRow",
                maxRow,
                self,
            )
        cols = 0
        if self.view.scrollCol > self.penCol:
            cols = self.penCol - self.view.scrollCol
            log.error(
                "CCC self.view.scrollCol > self.penCol",
                self.view.scrollCol,
                self.penCol,
                self,
            )
        elif self.penCol >= self.view.scrollCol + maxCol:
            cols = self.penCol - (self.view.scrollCol + maxCol - 1)
            log.error(
                "DDD self.penCol >= self.scrollCol + maxCol",
                self.penCol,
                self.view.scrollCol,
                maxCol,
                self,
            )
        assert not rows
        assert not cols
        self.update_scroll_position(rows, cols)

    def draw(self, window):
        if self.view.rows <= 0 or self.view.cols <= 0:
            return
        if not self.view.program.prefs.editor["useBgThread"]:
            if self.shouldReparse:
                self.parse_grammars()
                self.shouldReparse = False
        if self.view.hasCaptiveCursor:
            self.check_scroll_to_cursor(window)
        rows, cols = window.rows, window.cols
        color_pref = self.view.color_pref
        colorDelta = 32 * 4
        # colorDelta = 4
        if 0:
            for i in range(rows):
                window.add_str(i, 0, "?" * cols, color_pref(120))
        if 0:
            # Draw window with no concern for sub-rectangles.
            self.draw_text_area(window, 0, 0, rows, cols, 0)
        elif 1:
            splitRow = rows
            splitCol = max(0, self.lineLimitIndicator - self.view.scrollCol)
            if self.lineLimitIndicator <= 0 or splitCol >= cols:
                # Draw only left side.
                self.draw_text_area(window, 0, 0, splitRow, cols, 0)
            elif 0 < splitCol < cols:
                # Draw both sides.
                self.draw_text_area(window, 0, 0, splitRow, splitCol, 0)
                self.draw_text_area(
                    window, 0, splitCol, splitRow, cols - splitCol, colorDelta
                )
            else:
                # Draw only right side.
                assert splitCol <= 0
                self.draw_text_area(
                    window, 0, splitCol, splitRow, cols - splitCol, colorDelta
                )
        else:
            # Draw debug checker board.
            splitRow = rows // 2
            splitCol = 17
            self.draw_text_area(window, 0, 0, splitRow, splitCol, 0)
            self.draw_text_area(
                window, 0, splitCol, splitRow, cols - splitCol, colorDelta
            )
            self.draw_text_area(
                window, splitRow, 0, rows - splitRow, splitCol, colorDelta
            )
            self.draw_text_area(
                window, splitRow, splitCol, rows - splitRow, cols - splitCol, 0
            )
        # Blank screen past the end of the buffer.
        color = color_pref("outside_document")
        endOfText = min(max(self.parser.row_count() -
                        self.view.scrollRow, 0), rows)
        for i in range(endOfText, rows):
            window.add_str(i, 0, " " * cols, color)

    def draw_text_area(self, window, top, left, rows, cols, colorDelta):
        startRow = self.view.scrollRow + top
        endRow = startRow + rows
        startCol = self.view.scrollCol + left
        endCol = startCol + cols
        appPrefs = self.view.program.prefs
        defaultColor = appPrefs.color["default"]
        spellChecking = appPrefs.editor.get("spellChecking", True)
        color_pref = self.view.color_pref
        spelling = self.program.dictionary
        spelling.set_up_words_for_path(self.fullPath)
        if self.parser:
            # Highlight grammar.
            rowLimit = min(max(self.parser.row_count() - startRow, 0), rows)
            for i in range(rowLimit):
                line, renderedWidth = self.parser.row_text_and_width(
                    startRow + i)
                k = startCol
                if k == 0:
                    # When rendering from column 0 the grammar index is always
                    # zero.
                    grammarIndex = 0
                else:
                    # When starting mid-line, find starting grammar index.
                    grammarIndex = self.parser.grammar_index_from_row_col(
                        startRow + i, k
                    )
                while k < endCol:
                    (node, preceding, remaining, eol) = self.parser.grammar_at_index(
                        startRow + i, k, grammarIndex
                    )
                    grammarIndex += 1
                    if remaining == 0 and not eol:
                        continue
                    remaining = min(renderedWidth - k, remaining)
                    length = min(endCol - k, remaining)
                    color = color_pref(
                        node.grammar.get(
                            u"colorIndex", defaultColor), colorDelta
                    )
                    if eol or length <= 0:
                        window.add_str(
                            top + i, left + k - startCol, u" " *
                            (endCol - k), color
                        )
                        break
                    window.add_str(
                        top + i,
                        left + k - startCol,
                        curses_util.rendered_sub_str(line, k, k + length),
                        color,
                    )
                    subStart = k - preceding
                    subEnd = k + remaining
                    subLine = line[subStart:subEnd]
                    if spellChecking and node.grammar.get(u"spelling", True):
                        # Highlight spelling errors
                        grammarName = node.grammar.get(u"name", "unknown")
                        misspellingColor = color_pref(
                            u"misspelling", colorDelta)
                        for found in re.finditer(regex.kReSubwords, subLine):
                            reg = found.regs[0]  # Mispelllled word
                            offsetStart = subStart + reg[0]
                            offsetEnd = subStart + reg[1]
                            if startCol < offsetEnd and offsetStart < endCol:
                                word = line[offsetStart:offsetEnd]
                                if not spelling.is_correct(word, grammarName):
                                    if startCol > offsetStart:
                                        offsetStart += startCol - offsetStart
                                    wordFragment = line[
                                        offsetStart: min(endCol, offsetEnd)
                                    ]
                                    window.add_str(
                                        top + i,
                                        left + offsetStart - startCol,
                                        wordFragment,
                                        misspellingColor,
                                    )
                    k += length
        else:
            # For testing, draw without parser.
            rowLimit = min(max(self.parser.row_count() - startRow, 0), rows)
            for i in range(rowLimit):
                line = self.parser.row_text(startRow + i)[startCol:endCol]
                window.add_str(
                    top + i,
                    left,
                    line + " " * (cols - len(line)),
                    color_pref(u"default", colorDelta),
                )
        self.draw_overlays(window, top, left, rows, cols, colorDelta)
        if 0:  # Experiment: draw our own cursor.
            if startRow <= self.penRow < endRow and startCol <= self.penCol < endCol:
                window.add_str(
                    self.penRow - startRow, self.penCol - startCol, u"X", 200
                )

    def draw_overlays(self, window, top, left, maxRow, maxCol, colorDelta):
        startRow = self.view.scrollRow + top
        endRow = self.view.scrollRow + top + maxRow
        startCol = self.view.scrollCol + left
        endCol = self.view.scrollCol + left + maxCol
        rowLimit = min(max(self.parser.row_count() - startRow, 0), maxRow)
        color_pref = self.view.color_pref
        if 1:
            # Highlight brackets.
            # Highlight numbers.
            # Highlight space ending lines.
            colors = (
                color_pref(u"bracket", colorDelta),
                color_pref(u"number", colorDelta),
                color_pref(u"trailing_space", colorDelta),
            )
            for i in range(rowLimit):
                line = self.parser.row_text(startRow + i)
                highlightTrailingWhitespace = self.highlightTrailingWhitespace and not (
                    startRow + i == self.penRow and self.penCol == len(line)
                )
                for s, column, _, index in curses_util.rendered_find_iter(
                    line,
                    startCol,
                    endCol,
                    (u"[]{}()",),
                    True,
                    highlightTrailingWhitespace,
                ):
                    window.add_str(
                        top + i, column - self.view.scrollCol, s, colors[index]
                    )
        if 1:
            # Match brackets.
            if (
                self.parser.row_count() > self.penRow
                and len(self.parser.row_text(self.penRow)) > self.penCol
            ):
                ch = curses_util.char_at_column(
                    self.penCol, self.parser.row_text(self.penRow)
                )
                matchingBracketRowCol = self.get_matching_bracket_row_col()
                if matchingBracketRowCol is not None:
                    matchingBracketRow = matchingBracketRowCol[0]
                    matchingBracketCol = matchingBracketRowCol[1]
                    window.add_str(
                        top + self.penRow - startRow,
                        self.penCol - self.view.scrollCol,
                        ch,
                        color_pref(u"matching_bracket", colorDelta),
                    )
                    characterFinder = {
                        u"(": u")",
                        u"[": u"]",
                        u"{": u"}",
                        u")": u"(",
                        u"]": u"[",
                        u"}": u"{",
                    }
                    oppCharacter = characterFinder[ch]
                    window.add_str(
                        top + matchingBracketRow - startRow,
                        matchingBracketCol - self.view.scrollCol,
                        oppCharacter,
                        color_pref(u"matching_bracket", colorDelta),
                    )
        if self.highlightCursorLine:
            # Highlight the whole line at the cursor location.
            if self.view.hasFocus and startRow <= self.penRow < startRow + rowLimit:
                line = self.parser.row_text(self.penRow)[startCol:endCol]
                window.add_str(
                    top + self.penRow - startRow,
                    left,
                    line,
                    color_pref(u"current_line", colorDelta),
                )
        if self.findRe is not None:
            # Highlight find.
            for i in range(rowLimit):
                line = self.parser.row_text(startRow + i)[startCol:endCol]
                for k in self.findRe.finditer(line):
                    reg = k.regs[0]
                    # for ref in k.regs[1:]:
                    window.add_str(
                        top + i,
                        left + reg[0],
                        line[reg[0]: reg[1]],
                        color_pref("found_find", colorDelta),
                    )
        if rowLimit and self.selectionMode != selectable.kSelectionNone:
            # Highlight selected text.
            colorSelected = color_pref("selected")
            upperRow, upperCol, lowerRow, lowerCol = self.start_and_end()
            if 1:
                selStartCol = max(upperCol, startCol)
                selEndCol = min(lowerCol, endCol)
                start = max(0, min(upperRow - startRow, maxRow))
                end = max(0, min(lowerRow - startRow, maxRow))
                if self.selectionMode == selectable.kSelectionBlock:
                    if not (
                        lowerRow < startRow
                        or upperRow >= endRow
                        or lowerCol < startCol
                        or upperCol >= endCol
                    ):
                        # There is an overlap.
                        for i in range(start, end + 1):
                            line = self.parser.row_text(startRow + i)[
                                selStartCol:selEndCol
                            ]
                            window.add_str(top + i, selStartCol,
                                           line, colorSelected)
                elif (
                    self.selectionMode == selectable.kSelectionAll
                    or self.selectionMode == selectable.kSelectionCharacter
                    or self.selectionMode == selectable.kSelectionLine
                    or self.selectionMode == selectable.kSelectionWord
                ):
                    if not (lowerRow < startRow or upperRow >= endRow):
                        # There is an overlap.
                        # Go one row past the selection or to the last line.
                        for i in range(
                            start, min(
                                end + 1, self.parser.row_count() - startRow)
                        ):
                            line = self.parser.row_text(startRow + i)
                            line += " "  # Maybe do: "\\n".
                            # TODO(dschuyler): This is essentially
                            # left + (upperCol or (scrollCol + left)) -
                            #    scrollCol - left
                            # which seems like it could be simplified.
                            paneCol = left + selStartCol - startCol
                            if i == lowerRow - startRow and i == upperRow - startRow:
                                # Selection entirely on one line.
                                text = curses_util.rendered_sub_str(
                                    line, selStartCol, selEndCol
                                )
                                window.add_str(top + i, paneCol,
                                               text, colorSelected)
                            elif i == lowerRow - startRow:
                                # End of multi-line selection.
                                text = curses_util.rendered_sub_str(
                                    line, startCol, selEndCol
                                )
                                window.add_str(
                                    top + i, left, text, colorSelected)
                            elif i == upperRow - startRow:
                                # Start of multi-line selection.
                                text = curses_util.rendered_sub_str(
                                    line, selStartCol, endCol
                                )
                                window.add_str(top + i, paneCol,
                                               text, colorSelected)
                            else:
                                # Middle of multi-line selection.
                                text = curses_util.rendered_sub_str(
                                    line, startCol, endCol
                                )
                                window.add_str(
                                    top + i, left, text, colorSelected)
