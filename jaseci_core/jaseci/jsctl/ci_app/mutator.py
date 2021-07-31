# Copyright 2017 Google Inc.
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

import os
import re

from . import buffer_file
from .curses_util import column_width
from . import log
from . import selectable
from . import config
# If a change is in |noOpInstructions| then it has no real effect.
noOpInstructions = set(
    [
        ("m", (0, 0, 0, 0, 0)),
    ]
)


def add_vectors(a, b):
    """Add two list-like objects, pair-wise."""
    return tuple([a[i] + b[i] for i in range(len(a))])


class Mutator(selectable.Selectable):
    """Track and enact changes to a body of text."""

    def __init__(self, program):
        selectable.Selectable.__init__(self, program)
        self.__compoundChange = []
        # |oldRedoIndex| is used to store the redo index before an action
        # occurs, so we know where to insert the compound change.
        self.oldRedoIndex = 0
        self.debugRedo = False
        self.findRe = None
        self.findBackRe = None
        self.fileExtension = None
        self.fullPath = u""
        self.fileStat = None
        self.goalCol = 0
        self.isReadOnly = False
        self.penGrammar = None
        self.relativePath = ""
        self.redo_chain = []
        # |tempChange| is used to store cursor view actions without trimming
        # redo_chain.
        self.tempChange = None
        # |processTempChange| is True if tempChange is not None and needs to be
        # processed.
        self.processTempChange = False
        # |stallNextRedo| is True if the next call to redo() should do nothing.
        self.stallNextRedo = False
        # |redoIndex| may be equal to len(self.redo_chain) (must be <=).
        self.redoIndex = 0
        # |savedAtRedoIndex| may be > len(self.redo_chain).
        self.savedAtRedoIndex = 0
        self.shouldReparse = False

    def compound_change_push(self):
        # log.info('compound_change_push')
        if self.__compoundChange:
            self.redoIndex = self.oldRedoIndex
            self.redo_chain = self.redo_chain[: self.redoIndex]
            changes = tuple(self.__compoundChange)
            change = changes[0]
            handledChange = False
            # Combine changes. Assumes d, i, n, and m consist of only 1 change.
            if (
                len(self.redo_chain)
                and self.redo_chain[-1][0][0] == change[0]
                and len(self.redo_chain[-1]) == 1
            ):
                if change[0] in ("d", "i"):
                    change = (change[0], self.redo_chain[-1][0][1] + change[1])
                    self.redo_chain[-1] = (change,)
                    handledChange = True
                elif change[0] == "f":
                    # Fences have no arguments to merge.
                    handledChange = True
                elif change[0] == "n":
                    newCursorChange = change[2]
                    newCarriageReturns = change[1]
                    oldCursorChange = self.redo_chain[-1][0][2]
                    oldCarriageReturns = self.redo_chain[-1][0][1]
                    change = (
                        change[0],
                        oldCarriageReturns + newCarriageReturns,
                        ("m", add_vectors(
                            newCursorChange[1], oldCursorChange[1])),
                    )
                    self.redo_chain[-1] = (change,)
                    handledChange = True
                elif change[0] == "m":
                    change = (
                        change[0],
                        add_vectors(self.redo_chain[-1][0][1], change[1]),
                    )
                    if change in noOpInstructions:
                        self.redoIndex -= 1
                        self.redo_chain.pop()
                    else:
                        self.redo_chain[-1] = (change,)
                    handledChange = True
            if not handledChange:
                self.redo_chain.append(changes)
                self.redoIndex += 1
        self.__compoundChange = []
        self.oldRedoIndex = self.redoIndex

    def cursor_grammar_name(self):
        """inefficient test hack. wip on parser"""
        if not self.parser:
            return "no parser"
        index = self.parser.grammar_index_from_row_col(
            self.penRow, self.penCol)
        self.penGrammar = self.parser.grammar_at_index(self.penRow, self.penCol, index)[
            0
        ]
        if self.penGrammar is None:
            return "None"
        return self.penGrammar.grammar.get("name", "unknown")

    def is_dirty(self):
        """Whether the buffer contains non-trivial changes since the last save."""
        clean = self.savedAtRedoIndex >= 0 and (
            self.savedAtRedoIndex == self.redoIndex
            or (
                self.redoIndex + 1 == self.savedAtRedoIndex
                and self.redoIndex < len(self.redo_chain)
                and self.redo_chain[self.redoIndex][0] == "m"
            )
            or (
                self.redoIndex - 1 == self.savedAtRedoIndex
                and self.redoIndex > 0
                and self.redo_chain[self.redoIndex - 1][0] == "m"
            )
        )
        return not clean

    def is_safe_to_write(self):
        """Determine whether writing the file to self.fullPath is likely to
        overwrite data.

        Returns true if the file is not yet written or if the file has not been
        changed since it was read.
        """
        if not os.path.exists(self.fullPath):
            return True
        if self.fileStat is None:
            return False
        s1 = os.stat(self.fullPath)
        s2 = self.fileStat
        if 0:
            log.info("st_mode", s1.st_mode, s2.st_mode)
            log.info("st_ino", s1.st_ino, s2.st_ino)
            log.info("st_dev", s1.st_dev, s2.st_dev)
            log.info("st_uid", s1.st_uid, s2.st_uid)
            log.info("st_gid", s1.st_gid, s2.st_gid)
            log.info("st_size", s1.st_size, s2.st_size)
            log.info("st_mtime", s1.st_mtime, s2.st_mtime)
            log.info("st_ctime", s1.st_ctime, s2.st_ctime)
        return (
            s1.st_mode == s2.st_mode
            and s1.st_ino == s2.st_ino
            and s1.st_dev == s2.st_dev
            and s1.st_uid == s2.st_uid
            and s1.st_gid == s2.st_gid
            and s1.st_size == s2.st_size
            and s1.st_mtime == s2.st_mtime
            and s1.st_ctime == s2.st_ctime
        )

    def set_file_path(self, path):
        """Set the location where this file will be written.

        `path` may be full, relative, or contain env vars.
        """
        self.fullPath = buffer_file.expand_full_path(path)

    def __do_move_lines(self, begin, end, to):
        lines = self.parser.text_range(begin, 0, end, 0)
        self.parser.delete_range(begin, 0, end, 0)
        count = end - begin
        if begin < to:
            assert end < to
            assert self.penRow < to
            to -= count
            self.penRow -= count
            if self.selectionMode != selectable.kSelectionNone:
                assert self.markerRow < to + count
                assert self.markerRow >= count
                self.markerRow -= count
        else:
            assert end > to
            assert self.penRow >= to
            self.penRow += count
            if self.selectionMode != selectable.kSelectionNone:
                assert self.markerRow >= to
                self.markerRow += count
        self.parser.insert_lines(to, 0, lines.split(u"\n"))

    def __do_vertical_insert(self, change):
        text, row, endRow, col = change[1]
        self.parser.insert_block(row, col, [text] * (endRow - row + 1))

    def __do_vertical_delete(self, change):
        text, row, endRow, col = change[1]
        self.parser.delete_block(row, col, endRow, col + len(text))

    def __redo_move(self, change):
        assert self.penRow + \
            change[1][0] >= 0, "%s %s" % (self.penRow, change[1][0])
        assert self.penCol + \
            change[1][1] >= 0, "%s %s" % (self.penCol, change[1][1])
        self.penRow += change[1][0]
        self.penCol += change[1][1]
        self.markerRow += change[1][2]
        self.markerCol += change[1][3]
        self.selectionMode += change[1][4]

    def print_redo_state(self, out):
        out(u"---- Redo State begin ----")
        out(
            u"procTemp %d temp %r"
            % (
                self.processTempChange,
                self.tempChange,
            )
        )
        out(
            u"redoIndex %3d savedAt %3d depth %3d"
            % (self.redoIndex, self.savedAtRedoIndex, len(self.redo_chain))
        )
        index = len(self.redo_chain)
        while index > 0:
            if index == self.redoIndex:
                out(u"  -----> next redo ^; next undo v")
            if index == self.savedAtRedoIndex:
                out(u"  <saved>")
            index -= 1
            out(u"    {}".format(repr(self.redo_chain[index])))
        out(u"---- Redo State end ----")

    def redo(self):
        """Replay the next action on the redo_chain."""
        assert 0 <= self.redoIndex <= len(self.redo_chain)
        if self.stallNextRedo:
            self.stallNextRedo = False
            return
        if self.processTempChange:
            self.processTempChange = False
            self.__redo_move(self.tempChange)
            self.update_basic_scroll_position()
            return
        if self.tempChange:
            self.__undo_move(self.tempChange)
            self.tempChange = None
            self.update_basic_scroll_position()
        while self.redoIndex < len(self.redo_chain):
            changes = self.redo_chain[self.redoIndex]
            self.redoIndex += 1
            for change in changes:
                self.__redo_change(change)
            # Stop redoing if we redo a non-trivial action
            if not (
                (changes[0][0] == "f" or changes[0]
                 [0] == "m") and len(changes) == 1
            ):
                self.shouldReparse = True
                break
        self.update_basic_scroll_position()

    def __redo_change(self, change):
        if change[0] == "b":  # Redo backspace.
            self.penRow, self.penCol = self.parser.backspace(
                self.penRow, self.penCol)
        elif change[0] == "bw":  # Redo backspace word.
            width = column_width(change[1])
            self.parser.delete_range(
                self.penRow, self.penCol - width, self.penRow, self.penCol
            )
            self.penCol -= width
        elif change[0] == "d":  # Redo delete character.
            self.parser.delete_char(self.penRow, self.penCol)
        elif change[0] == "dr":  # Redo delete range.
            self.do_delete(*change[1])
        elif change[0] == "ds":  # Redo delete selection.
            self.do_delete_selection()
        elif change[0] == "f":  # Redo fence.
            pass
        elif change[0] == "i":  # Redo insert.
            self.parser.insert(self.penRow, self.penCol, change[1])
            self.penCol += column_width(change[1])
            self.goalCol = self.penCol
        elif change[0] == "j":  # Redo join lines (delete \n).
            self.parser.delete_char(self.penRow, self.penCol)
        elif change[0] == "ld":  # Redo line diff.
            assert False  # Not used.
            lines = []
            index = 0
            for ii in change[1]:
                if type(ii) is type(0):
                    for line in self.parser.textLines(index, index + ii):
                        lines.append(line)
                    index += ii
                elif ii[0] == "+":
                    lines.append(ii[2:])
                elif ii[0] == "-":
                    index += 1
            self.parser.data = lines.join(u"\n")
            firstChangedRow = change[1][0] if type(
                change[1][0]) is type(0) else 0
        elif change[0] == "m":  # Redo move
            self.__redo_move(change)
        elif change[0] == "ml":  # Redo move lines
            begin, end, to = change[1]
            self.__do_move_lines(begin, end, to)
        elif change[0] == "n":  # Redo split lines (insert \n).
            self.parser.insert(self.penRow, self.penCol, u"\n")
            self.__redo_move(change[2])
        elif change[0] == "v":  # Redo paste.
            self.insert_lines(change[1])
        elif change[0] == "vb":  # Redo vertical backspace.
            assert False  # Not yet used.
            width = column_width(change[1][0])
            self.parser.delete_block(
                self.penRow,
                self.penCol - width,
                self.penRow + len(change[1]),
                self.penCol,
            )
            self.penCol -= width
        elif change[0] == "vd":  # Redo vertical delete.
            self.__do_vertical_delete(change)
        elif change[0] == "vi":  # Redo vertical insert.
            self.__do_vertical_insert(change)
        else:
            log.info("ERROR: unknown redo.")
        return False

    def redo_add_change(self, change):
        """
        Push a change onto the end of the redo_chain. Call redo() to enact the
        change.
        """
        if config.strict_debug:
            assert isinstance(change, tuple), change
        if self.debugRedo:
            log.info("redo_add_change", change)
        # Handle new trivial actions, which are defined as standalone cursor
        # moves.
        if change[0] == "m" and not self.__compoundChange:
            if self.tempChange:
                # Combine new change with the existing tempChange.
                change = (change[0], add_vectors(
                    self.tempChange[1], change[1]))
                self.__undo_change(self.tempChange)
                self.__tempChange = change
            if change in noOpInstructions:
                self.stallNextRedo = True
                self.processTempChange = False
                self.tempChange = None
                self.update_basic_scroll_position()
                return
            self.processTempChange = True
            self.tempChange = change
        else:
            # Trim and combine main redo_chain with tempChange
            # if there is a non-trivial action.
            # We may lose the saved at when trimming.
            if self.redoIndex < self.savedAtRedoIndex:
                self.savedAtRedoIndex = -1
            self.redo_chain = self.redo_chain[: self.redoIndex]
            if self.tempChange:
                # If previous action was a cursor move, we can merge it with
                # tempChange.
                if (
                    len(self.redo_chain)
                    and self.redo_chain[-1][0][0] == "m"
                    and len(self.redo_chain[-1]) == 1
                ):
                    combinedChange = (
                        "m",
                        add_vectors(
                            self.tempChange[1], self.redo_chain[-1][0][1]),
                    )
                    if combinedChange in noOpInstructions:
                        self.redo_chain.pop()
                        self.redoIndex -= 1
                        self.oldRedoIndex -= 1
                    else:
                        self.redo_chain[-1] = (combinedChange,)
                else:
                    self.redo_chain.append((self.tempChange,))
                    self.redoIndex += 1
                    self.oldRedoIndex += 1
                self.tempChange = None
            # Accumulating changes together as a unit.
            self.__compoundChange.append(change)
            self.redo_chain.append((change,))
        if self.debugRedo:
            log.info("--- redoIndex", self.redoIndex)
            for i, c in enumerate(self.redo_chain):
                log.info("%2d:" % i, repr(c))
            log.info("tempChange", repr(self.tempChange))

    def __undo_move(self, change):
        """Undo the action of a cursor move"""
        self.penRow -= change[1][0]
        self.penCol -= change[1][1]
        self.markerRow -= change[1][2]
        self.markerCol -= change[1][3]
        self.selectionMode -= change[1][4]
        assert self.penRow >= 0, self.penRow
        assert self.penCol >= 0, self.penCol

    def undo(self):
        """Undo a set of redo nodes."""
        assert 0 <= self.redoIndex <= len(self.redo_chain)
        # If tempChange is active, undo it first to fix cursor position.
        if self.tempChange:
            self.__undo_move(self.tempChange)
            self.tempChange = None
        while self.redoIndex > 0:
            self.redoIndex -= 1
            changes = self.redo_chain[self.redoIndex]
            if self.debugRedo:
                log.info("undo", self.redoIndex, repr(changes))
            if (changes[0][0] == "f" or changes[0][0] == "m") and len(changes) == 1:
                # Undo if the last edit was a cursor move.
                self.__undo_change(changes[0])
            else:
                self.shouldReparse = True
                # Undo previous non-trivial edit
                for change in reversed(changes):
                    self.__undo_change(change)
                break
        self.processTempChange = False

    def __undo_change(self, change):
        if change[0] == "b":
            self.parser.insert(self.penRow, self.penCol, change[1])
            position = self.parser.next_char_row_col(self.penRow, self.penCol)
            if position is not None:
                self.penRow += position[0]
                self.penCol += position[1]
        elif change[0] == "bw":  # Undo backspace word.
            self.parser.insert(self.penRow, self.penCol, change[1])
            self.penCol += column_width(change[1])
        elif change[0] == "d":
            self.parser.insert(self.penRow, self.penCol, change[1])
        elif change[0] == "dr":  # Undo delete range.
            self.insert_lines_at(
                change[1][0],
                change[1][1],
                change[2],
                selectable.kSelectionCharacter,
            )
        elif change[0] == "ds":  # Undo delete selection.
            self.insert_lines(change[1])
        elif change[0] == "f":  # Undo fence.
            pass
        elif change[0] == "i":  # Undo insert.
            width = column_width(change[1])
            self.parser.delete_range(
                self.penRow, self.penCol - width, self.penRow, self.penCol
            )
            self.penCol -= width
            self.goalCol = self.penCol
        elif change[0] == "j":  # Undo join lines.
            self.parser.insert(self.penRow, self.penCol, u"\n")
        elif change[0] == "ld":  # Undo line diff.
            assert False  # Not used.
            lines = []
            index = 0
            for ii in change[1]:
                if type(ii) is type(0):
                    for line in self.parser.textLines(index, index + ii):
                        lines.append(line)
                    index += ii
                elif ii[0] == "+":
                    index += 1
                elif ii[0] == "-":
                    lines.append(ii[2:])
            self.parser.data = lines.join(u"\n")
            firstChangedRow = change[1][0] if type(
                change[1][0]) is type(0) else 0
        elif change[0] == "m":
            self.__undo_move(change)
        elif change[0] == "ml":
            # Undo move lines
            begin, end, to = change[1]
            count = end - begin
            if begin < to:
                self.__do_move_lines(to - 1, to + count - 1, begin + count - 1)
            else:
                self.__do_move_lines(to, to + count, begin + count)
        elif change[0] == "n":
            # Undo split lines.
            self.__undo_move(change[2])
            self.parser.backspace(self.penRow + 1, 0)
        elif change[0] == "v":  # undo paste
            clip = change[1]
            if len(clip) == 1:
                self.parser.delete_range(
                    self.penRow,
                    self.penCol,
                    self.penRow + len(clip) - 1,
                    self.penCol + len(clip[-1]),
                )
            else:
                self.parser.delete_range(
                    self.penRow, self.penCol, self.penRow +
                    len(clip) - 1, len(clip[-1])
                )
        elif change[0] == "vb":  # Undo vertical backspace.
            assert False  # Not yet used.
            self.parser.insert_block(self.penRow, self.penCol, change[1])
            self.penCol += column_width(change[1][0])
        elif change[0] == "vd":  # Undo vertical delete
            self.__do_vertical_insert(change)
        elif change[0] == "vi":  # Undo vertical insert
            self.__do_vertical_delete(change)
        else:
            log.info("ERROR: unknown undo.")

    def update_basic_scroll_position(self):
        pass
