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

import re

from . import config
from . import line_buffer
from . import log
from . import regex

# No selection.
kSelectionNone = 0
# Entire document selected.
kSelectionAll = 1
# A rectangular block selection.
kSelectionBlock = 2
# Character by character selection.
kSelectionCharacter = 3
# Select whole lines.
kSelectionLine = 4
# Select whole words.
kSelectionWord = 5
# How many selection modes are there.
kSelectionModeCount = 6

kSelectionModeNames = [
    "None",
    "All",
    "Block",
    "Char",
    "Line",
    "Word",
]


class Selectable(line_buffer.LineBuffer):
    def __init__(self, program):
        line_buffer.LineBuffer.__init__(self, program)
        # When a text document is not line wrapped then each row will represent
        # one line in the document, thow rows are zero based and lines are one
        # based. With line wrapping enabled there may be more rows than lines
        # since a line may wrap into multiple rows.
        self.penRow = 0
        # When a text document contains only ascii characters then each char
        # (character) will represent one column in the text line (col is zero
        # based and the column displayed in the UI is one based). When double
        # wide character are present then a line of text will have more columns
        # than characters.
        # (penChar is not currently used).
        self.penChar = 0
        # When a text document contains only ascii characters then each column
        # will represent one column in the text line (col is zero based and
        # column displayed in the UI is one based).
        self.penCol = 0
        self.markerRow = 0
        self.markerCol = 0
        self.selectionMode = kSelectionNone

    def count_selected(self):
        lines = self.get_selected_text()
        chars = len(lines) - 1  # Count carriage returns.
        for line in lines:
            chars += len(line)
        return chars, len(lines)

    def selection(self):
        return (self.penRow, self.penCol, self.markerRow, self.markerCol)

    def selection_mode_name(self):
        return kSelectionModeNames[self.selectionMode]

    def get_selected_text(self):
        upperRow, upperCol, lowerRow, lowerCol = self.start_and_end()
        return self.get_text(upperRow, upperCol, lowerRow, lowerCol, self.selectionMode)

    def get_text(
        self, upperRow, upperCol, lowerRow, lowerCol, selectionMode=kSelectionCharacter
    ):
        if config.strict_debug:
            assert isinstance(upperRow, int)
            assert isinstance(upperCol, int)
            assert isinstance(lowerRow, int)
            assert isinstance(lowerCol, int)
            assert isinstance(selectionMode, int)
            assert upperRow <= lowerRow
            assert upperRow != lowerRow or upperCol <= lowerCol
            assert kSelectionNone <= selectionMode < kSelectionModeCount
        lines = []
        if selectionMode == kSelectionBlock:
            if lowerRow + 1 < self.parser.row_count():
                lowerRow += 1
            for i in range(upperRow, lowerRow):
                lines.append(self.parser.row_text(i, upperCol, lowerCol))
        elif (
            selectionMode == kSelectionAll
            or selectionMode == kSelectionCharacter
            or selectionMode == kSelectionLine
            or selectionMode == kSelectionWord
        ):
            if upperRow == lowerRow:
                lines.append(self.parser.row_text(
                    upperRow, upperCol, lowerCol))
            else:
                for i in range(upperRow, lowerRow + 1):
                    if i == upperRow:
                        lines.append(self.parser.row_text(i, upperCol))
                    elif i == lowerRow:
                        lines.append(self.parser.row_text(i, 0, lowerCol))
                    else:
                        lines.append(self.parser.row_text(i))
        return tuple(lines)

    def do_delete_selection(self):
        """Call do_delete() with current pen and marker values."""
        upperRow, upperCol, lowerRow, lowerCol = self.start_and_end()
        self.do_delete(upperRow, upperCol, lowerRow, lowerCol)

    def do_delete(self, upperRow, upperCol, lowerRow, lowerCol):
        """Delete characters from (upperRow, upperCol) up to (lowerRow,
        lowerCol) using the current selection mode."""
        if config.strict_debug:
            assert isinstance(upperRow, int)
            assert isinstance(upperCol, int)
            assert isinstance(lowerRow, int)
            assert isinstance(lowerCol, int)
            assert upperRow <= lowerRow
            assert upperRow != lowerRow or upperCol <= lowerCol
        if self.selectionMode == kSelectionBlock:
            self.parser.delete_block(upperRow, upperCol, lowerRow, lowerCol)
        elif (
            self.selectionMode == kSelectionNone
            or self.selectionMode == kSelectionAll
            or self.selectionMode == kSelectionCharacter
            or self.selectionMode == kSelectionLine
            or self.selectionMode == kSelectionWord
        ):
            self.parser.delete_range(upperRow, upperCol, lowerRow, lowerCol)

    def insert_lines(self, lines):
        if config.strict_debug:
            assert isinstance(lines, tuple)
        self.insert_lines_at(self.penRow, self.penCol,
                             lines, self.selectionMode)

    def insert_lines_at(self, row, col, lines, selectionMode):
        if config.strict_debug:
            assert isinstance(row, int)
            assert isinstance(col, int)
            assert isinstance(lines, tuple)
            assert isinstance(selectionMode, int)
        if len(lines) <= 1:
            if len(lines) == 0 or len(lines[0]) == 0:
                # Optimization. There's nothing to insert.
                return
        lines = list(lines)
        if selectionMode == kSelectionBlock:
            self.parser.insert_block(row, col, lines)
        elif (
            selectionMode == kSelectionNone
            or selectionMode == kSelectionAll
            or selectionMode == kSelectionCharacter
            or selectionMode == kSelectionLine
            or selectionMode == kSelectionWord
        ):
            if len(lines) == 1:
                self.parser.insert(row, col, lines[0])
            else:
                self.parser.insert_lines(row, col, lines)
        else:
            log.info("selection mode not recognized", selectionMode)

    def __extend_words(self, upperRow, upperCol, lowerRow, lowerCol):
        """Extends and existing selection to the nearest word boundaries. The
        pen and marker will be extended away from each other. The extension may
        occur in one, both, or neither direction.

        Returns: tuple of (upperCol, lowerCol).
        """
        line = self.parser.row_text(upperRow)
        for segment in re.finditer(regex.kReWordBoundary, line):
            if segment.start() <= upperCol < segment.end():
                upperCol = segment.start()
                break
        line = self.parser.row_text(lowerRow)
        for segment in re.finditer(regex.kReWordBoundary, line):
            if segment.start() < lowerCol < segment.end():
                lowerCol = segment.end()
                break
        return upperCol, lowerCol

    def extend_selection(self):
        """Expand the current selection to fit the selection mode. E.g. if the
        pen in the middle of a word, selection word will extend the selection to
        the left and right so that the whole word is selected.

        Returns: tuple of (penRow, penCol, markerRow, markerCol, selectionMode)
            which are the delta values to accomplish the selection mode.
        """
        if self.selectionMode == kSelectionNone:
            return (0, 0, -self.markerRow, -self.markerCol, 0)
        elif self.selectionMode == kSelectionAll:
            lowerRow = self.parser.row_count() - 1
            lowerCol = self.parser.row_width(-1)
            return (
                lowerRow - self.penRow,
                lowerCol - self.penCol,
                -self.markerRow,
                -self.markerCol,
                0,
            )
        elif self.selectionMode == kSelectionLine:
            return (0, -self.penCol, 0, -self.markerCol, 0)
        elif self.selectionMode == kSelectionWord:
            if self.penRow > self.markerRow or (
                self.penRow == self.markerRow and self.penCol > self.markerCol
            ):
                upperCol, lowerCol = self.__extend_words(
                    self.markerRow, self.markerCol, self.penRow, self.penCol
                )
                return (0, lowerCol - self.penCol, 0, upperCol - self.markerCol, 0)
            else:
                upperCol, lowerCol = self.__extend_words(
                    self.penRow, self.penCol, self.markerRow, self.markerCol
                )
                return (0, upperCol - self.penCol, 0, lowerCol - self.markerCol, 0)
        return (0, 0, 0, 0, 0)

    def start_and_end(self):
        """Get the marker and pen pair as the earlier of the two then the later
        of the two. The result accounts for the current selection mode."""
        upperRow = 0
        upperCol = 0
        lowerRow = 0
        lowerCol = 0
        if self.selectionMode == kSelectionNone:
            upperRow = self.penRow
            upperCol = self.penCol
            lowerRow = self.penRow
            lowerCol = self.penCol
        elif self.selectionMode == kSelectionAll:
            upperRow = 0
            upperCol = 0
            lowerRow = self.parser.row_count() - 1
            lowerCol = self.parser.row_width(-1)
        elif self.selectionMode == kSelectionBlock:
            upperRow = min(self.markerRow, self.penRow)
            upperCol = min(self.markerCol, self.penCol)
            lowerRow = max(self.markerRow, self.penRow)
            lowerCol = max(self.markerCol, self.penCol)
        elif (
            self.selectionMode == kSelectionCharacter
            or self.selectionMode == kSelectionLine
            or self.selectionMode == kSelectionWord
        ):
            upperRow = self.markerRow
            upperCol = self.markerCol
            lowerRow = self.penRow
            lowerCol = self.penCol
            if upperRow == lowerRow and upperCol > lowerCol:
                upperCol, lowerCol = lowerCol, upperCol
            elif upperRow > lowerRow:
                upperRow, lowerRow = lowerRow, upperRow
                upperCol, lowerCol = lowerCol, upperCol
        # log.detail('start and end', upperRow, upperCol, lowerRow, lowerCol)
        return (upperRow, upperCol, lowerRow, lowerCol)
