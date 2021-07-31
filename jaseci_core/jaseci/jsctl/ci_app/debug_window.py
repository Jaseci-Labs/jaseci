# Copyright 2018 Google Inc.
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

import curses

from . import curses_util
from . import log
from . import window


class DebugWindow(window.ActiveWindow):
    def __init__(self, program, host):
        window.ActiveWindow.__init__(self, program, host)

    def debug_draw(self, program, win):
        """Draw real-time debug information to the screen."""
        textBuffer = win.textBuffer
        self.writeLineRow = 0
        intent = u"noIntent"
        if hasattr(win, u"userIntent"):
            intent = win.userIntent
        color = program.color.get(u"debug_window")
        self.write_line(
            u"   cRow %3d    cCol %2d goalCol %2d  %s"
            % (
                win.textBuffer.penRow,
                win.textBuffer.penCol,
                win.textBuffer.goalCol,
                intent,
            ),
            color,
        )
        self.write_line(
            u"   pRow %3d    pCol %2d chRow %4d"
            % (textBuffer.penRow, textBuffer.penCol, textBuffer.debugUpperChangedRow),
            color,
        )
        self.write_line(
            u" mkrRow %3d  mkrCol %2d sm %d"
            % (textBuffer.markerRow, textBuffer.markerCol, textBuffer.selectionMode),
            color,
        )
        self.write_line(
            u"scrlRow %3d scrlCol %2d lines %3d"
            % (win.scrollRow, win.scrollCol, textBuffer.parser.row_count()),
            color,
        )
        y, x = win.top, win.left
        maxRow, maxCol = win.rows, win.cols
        self.write_line(
            u"y %2d x %2d maxRow %d maxCol %d baud %d color %d"
            % (y, x, maxRow, maxCol, curses.baudrate(), curses.can_change_color()),
            color,
        )
        screenRows, screenCols = program.cursesScreen.getmaxyx()
        self.write_line(
            u"scr rows %d cols %d mlt %f/%f pt %f"
            % (
                screenRows,
                screenCols,
                program.mainLoopTime,
                program.mainLoopTimePeak,
                textBuffer.parserTime,
            ),
            color,
        )
        self.write_line(
            u"ch %3s %s"
            % (program.ch, curses_util.curses_key_name(program.ch) or u"UNKNOWN"),
            color,
        )
        self.write_line(u"win %r" % (win,), color)
        self.write_line(u"foc %r" %
                        (program.programWindow.focusedWindow,), color)
        self.write_line(u"tb %r" % (textBuffer,), color)
        (id, mouseCol, mouseRow, mouseZ, bState) = program.debugMouseEvent
        self.write_line(
            u"mouse id %d, mouseCol %d, mouseRow %d, mouseZ %d"
            % (id, mouseCol, mouseRow, mouseZ),
            color,
        )
        self.write_line(
            u"bState %s %d" % (
                curses_util.mouse_button_name(bState), bState), color
        )
        self.write_line(u"start_and_end %r" %
                        (textBuffer.start_and_end(),), color)


class DebugUndoWindow(window.ActiveWindow):
    def __init__(self, program, host):
        window.ActiveWindow.__init__(self, program, host)

    def debug_undo_draw(self, win):
        """Draw real-time debug information to the screen."""
        textBuffer = win.textBuffer
        self.writeLineRow = 0
        # Display some of the redo chain.
        colorPrefs = win.program.color
        redoColorA = colorPrefs.get(100)
        self.write_line(
            u"procTemp %d temp %r"
            % (
                textBuffer.processTempChange,
                textBuffer.tempChange,
            ),
            redoColorA,
        )
        self.write_line(
            u"redoIndex %3d savedAt %3d depth %3d"
            % (
                textBuffer.redoIndex,
                textBuffer.savedAtRedoIndex,
                len(textBuffer.redo_chain),
            ),
            redoColorA,
        )
        redoColorB = colorPrefs.get(101)
        split = 8
        for i in range(textBuffer.redoIndex - split, textBuffer.redoIndex):
            text = i >= 0 and repr(textBuffer.redo_chain[i]) or u""
            self.write_line(unicode(text), redoColorB)
        redoColorC = colorPrefs.get(1)
        for i in range(textBuffer.redoIndex, textBuffer.redoIndex + split - 1):
            text = i < len(
                textBuffer.redo_chain) and textBuffer.redo_chain[i] or ""
            self.write_line(unicode(text), redoColorC)
