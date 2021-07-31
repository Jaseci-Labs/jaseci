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
"""A fake curses api intended for making tests. By creating a fake version of
the curses API the ci_edit code can be tested for various inputs and outputs.

The values of constants and function calls are bogus. This was created based on
what ci_edit uses, without regard or reference to the internals of the curses
library."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    unicode
except NameError:
    unicode = str
    unichr = chr

import inspect
import os
import signal
import sys
import time
import traceback
import types
import unicodedata

from ... import curses_util

from . import ascii
from . import constants

DEBUG_COLOR_PAIR_BASE = 256
DEBUG_COLOR_PAIR_MASK = (DEBUG_COLOR_PAIR_BASE * 2) - 1


def is_string_type(value):
    if sys.version_info[0] == 2:
        return type(value) in types.StringTypes
    return isinstance(value, str)


# Avoiding importing curses_util.
# Tuple events are preceded by an escape (27).
BRACKETED_PASTE_BEGIN = (91, 50, 48, 48, 126)  # i.e. "[200~"
BRACKETED_PASTE_END = (91, 50, 48, 49, 126)  # i.e. "[201~"
BRACKETED_PASTE = ("terminal_paste",)  # Pseudo event type.


class error(BaseException):
    def __init__(self):
        BaseException.__init__(self)


class FakeInput:
    def __init__(self, display):
        self.fakeDisplay = display
        self.set_inputs([])

    def set_inputs(self, cmdList):
        self.inputs = cmdList
        self.inputsIndex = -1
        self.inBracketedPaste = False
        self.tupleIndex = -1
        self.waitingForRefresh = True
        self.isVerbose = False
        self.bgCounter = 1
        if self.isVerbose:
            print("")

    def log(self, *msg):
        if not self.isVerbose:
            return
        functionLine = inspect.stack()[1][2]
        function = inspect.stack()[1][3]
        frame = inspect.stack()[3]
        callingFile = os.path.split(frame[1])[1]
        callingLine = frame[2]
        caller = "%16s %5s %3s %s " % (
            callingFile, callingLine, function, functionLine)
        waiting = u"waitingForRefresh" if self.waitingForRefresh else ""
        print(caller + " ".join([repr(i) for i in msg]), waiting)

    def next(self):
        self.log("start")
        if self.waitingForRefresh:
            if self.bgCounter == 0:
                self.bgCounter = 1
                self.log("    ", self.bgCounter, 0)
                return 0
            self.bgCounter -= 1
            self.log("    ", self.bgCounter, -1)
            return -1
        self.bgCounter = 1
        if not self.waitingForRefresh:
            while self.inputsIndex + 1 < len(self.inputs):
                assert not self.waitingForRefresh
                self.inputsIndex += 1
                cmd = self.inputs[self.inputsIndex]
                if isinstance(cmd, types.FunctionType):
                    result = cmd(self.fakeDisplay, self.inputsIndex)
                    if result is not None:
                        self.waitingForRefresh = True
                        self.log("next(k)", repr(cmd)[:8], repr(result))
                        return result
                    self.log("next(f)", repr(cmd)[:8], repr(result))
                elif is_string_type(cmd) and len(cmd) == 1:
                    # A single character.
                    if (not self.inBracketedPaste) and cmd != ascii.ESC:
                        self.waitingForRefresh = True
                    self.log("next(q) ", repr(cmd), ord(cmd))
                    return ord(cmd)
                elif (
                    isinstance(cmd, tuple) and len(
                        cmd) > 1 and isinstance(cmd[0], int)
                ):
                    if cmd == BRACKETED_PASTE_BEGIN:
                        self.inBracketedPaste = True
                    self.log("next(s) ", cmd, type(cmd))
                    self.tupleIndex += 1
                    if self.tupleIndex >= len(cmd):
                        self.tupleIndex = -1
                        if cmd == BRACKETED_PASTE_END:
                            self.inBracketedPaste = False
                        self.log("next(u)", cmd, type(cmd))
                        self.log("return", constants.ERR)
                        return constants.ERR
                    if self.tupleIndex + 1 == len(cmd) and cmd != BRACKETED_PASTE_BEGIN:
                        self.waitingForRefresh = True
                    self.inputsIndex -= 1
                    self.log("return", cmd[self.tupleIndex],
                             self.tupleIndex, len(cmd))
                    return cmd[self.tupleIndex]
                elif isinstance(cmd, int) or isinstance(cmd, bytes):
                    if (not self.inBracketedPaste) and cmd != ascii.ESC:
                        self.waitingForRefresh = True
                    self.log("return", cmd, type(cmd))
                    return cmd
                else:
                    assert False, (cmd, type(cmd))
        self.log("return", constants.ERR)
        return constants.ERR


def test_log(log_level, *msg):
    # Adjust constant to increase verbosity.
    if log_level >= 0:
        return
    functionLine = inspect.stack()[1][2]
    function = inspect.stack()[1][3]
    frame = inspect.stack()[2]
    callingFile = os.path.split(frame[1])[1]
    callingLine = frame[2]
    callingFunction = frame[3]
    caller = "%20s %5s %20s %3s %s " % (
        callingFile,
        callingLine,
        callingFunction,
        functionLine,
        function,
    )
    print(caller + " ".join([repr(i) for i in msg]))


getchCallback = None


def set_getch_callback(callback):
    global getchCallback
    getchCallback = callback


# Test output. Use |display| to check the screen output.
class FakeDisplay:
    def __init__(self):
        self.rows = 15
        self.cols = 40
        self.colors = {}
        self.cursorRow = 0
        self.cursorCol = 0
        self.displayStyle = None
        self.displayText = None
        self.reset()

    def check_style(self, row, col, height, width, colorPair):
        # assert (colorPair & DEBUG_COLOR_PAIR_MASK) in self.colors.values()
        assert colorPair is not None
        assert colorPair >= DEBUG_COLOR_PAIR_BASE
        assert height != 0
        assert width != 0
        for i in range(height):
            for k in range(width):
                d = self.displayStyle[row + i][col + k]
                if d != colorPair:
                    self.show()
                    return u"\n  row %s, col %s color/style mismatch '%d' != '%d'" % (
                        row + i,
                        col + k,
                        d,
                        colorPair,
                    )
        return None

    def check_text(self, row, col, lines, verbose=3):
        assert isinstance(row, int)
        assert isinstance(col, int)
        assert isinstance(lines, list)
        assert isinstance(lines[0], unicode)
        assert isinstance(verbose, int)
        for i in range(len(lines)):
            line = lines[i]
            displayCol = col
            for ch in line:
                if row + i >= self.rows:
                    return u"\n  Row %d is outside of the %d row display" % (
                        row + i,
                        self.rows,
                    )
                if displayCol >= self.cols:
                    return u"\n  Column %d is outside of the %d column display" % (
                        displayCol,
                        self.cols,
                    )
                displayCh = self.displayText[row + i][displayCol]
                if displayCh != ch:
                    # self.show()
                    result = u"\n  row %s, col %s mismatch '%s' != '%s'" % (
                        row + i,
                        displayCol,
                        displayCh,
                        ch,
                    )
                    if verbose >= 1:
                        actualLine = u"".join(self.displayText[row + i])
                        result += u"\n  actual:   |%s|" % actualLine
                    if verbose >= 2:
                        expectedText = u"".join(line)
                        result += u"\n  expected: %s|%s|" % (
                            u" " * col, expectedText)
                    if verbose >= 3:
                        result += u"\n  mismatch:  %*s^" % (displayCol, u"")
                    return result
                displayCol += curses_util.char_width(displayCh, displayCol)
        return None

    def draw(self, cursorRow, cursorCol, text, colorPair):
        # assert (colorPair & DEBUG_COLOR_PAIR_MASK) in self.colors.values()
        assert isinstance(cursorRow, int)
        assert isinstance(cursorCol, int)
        assert isinstance(text, unicode)
        assert colorPair >= DEBUG_COLOR_PAIR_BASE
        for i in text:
            if i == "\r":
                cursorCol = 0
                continue
            try:
                self.displayText[cursorRow][cursorCol] = i
                self.displayStyle[cursorRow][cursorCol] = colorPair
                cursorCol += 1
                if curses_util.char_width(i, cursorCol) > 1:
                    self.displayText[cursorRow][cursorCol] = u" "
                    self.displayStyle[cursorRow][cursorCol] = colorPair
                    cursorCol += 1
            except IndexError:
                raise error()
        return cursorRow, cursorCol

    def find_text(self, screenText):
        assert isinstance(screenText, unicode)
        for row in range(len(self.displayText)):
            line = self.displayText[row]
            col = u"".join(line).find(screenText)
            if col != -1:
                return row, col
        print(u"Error: Did not find", screenText)
        self.show()
        return -1, -1

    def get_color_pair(self, colorIndex):
        assert colorIndex < DEBUG_COLOR_PAIR_BASE
        colorPair = self.colors.setdefault(
            colorIndex, DEBUG_COLOR_PAIR_BASE + len(self.colors)
        )
        return colorPair

    def get_style(self):
        return [
            u"".join(
                [
                    unichr((c & DEBUG_COLOR_PAIR_MASK) -
                           DEBUG_COLOR_PAIR_BASE + 91)
                    for c in self.displayStyle[i]
                ]
            )
            for i in range(self.rows)
        ]

    def get_text(self):
        rows = []
        for rowIndex in range(self.rows):
            rowChars = self.displayText[rowIndex]
            line = []
            limit = len(rowChars)
            col = 0
            while col < limit:
                line.append(rowChars[col])
                col += curses_util.char_width(rowChars[col], col)
            rows.append(u"".join(line))
        return rows

    def set_screen_size(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.reset()

    def show(self):
        assert (
            self.displayStyle[0][0] != -1
        ), u"Error: showing display before drawing to it."
        print(u"   %*s   %s" % (-self.cols, u"display", u"style"))
        print(u"  +" + u"-" * self.cols + u"+ +" + u"-" * self.cols + u"+")
        for i, (line, styles) in enumerate(zip(self.get_text(), self.get_style())):
            print(u"%2d|%s| |%s|" % (i, line, styles))
        print(u"  +" + u"-" * self.cols + u"+ +" + u"-" * self.cols + u"+")

    def reset(self):
        self.displayStyle = [
            [-1 for _ in range(self.cols)] for _ in range(self.rows)]
        self.displayText = [[u"x" for _ in range(
            self.cols)] for _ in range(self.rows)]


fakeDisplay = None
fakeInput = None
mouseEvents = []


def get_fake_display():
    return fakeDisplay


def print_fake_display():
    fakeDisplay.show()


#####################################


class FakeCursesWindow:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cursorRow = 0
        self.cursorCol = 0

    def addstr(self, *args):
        test_log(4, *args)
        cursorRow = args[0]
        cursorCol = args[1]
        assert isinstance(cursorRow, int)
        assert isinstance(cursorCol, int)
        assert isinstance(args[2], bytes), repr(args[2])
        text = args[2].decode("utf-8")
        color = args[3]
        assert isinstance(cursorRow, int)
        self.cursorRow, self.cursorCol = fakeDisplay.draw(
            cursorRow, cursorCol, text, color
        )

    def getch(self):
        test_log(4)
        if 1:
            if getchCallback:
                val = getchCallback()
                return val
        val = fakeInput.next()
        if self.movie and val != constants.ERR and val != 0:
            if val == 409:
                print(u"val", val, u"mouse_info", mouseEvents[-1])
            else:
                print(u"val", val)
        return val

    def getyx(self):
        test_log(2)
        return (self.cursorRow, self.cursorCol)

    def getmaxyx(self):
        test_log(2)
        return (fakeDisplay.rows, fakeDisplay.cols)

    def keypad(self, *args):
        test_log(2, *args)

    def leaveok(self, *args):
        test_log(2, *args)

    def move(self, a, b):
        test_log(2, a, b)
        self.cursorRow = a
        self.cursorCol = b

    def noutrefresh(self):
        pass

    def refresh(self):
        test_log(2)

    def resize(self, a, b):
        test_log(2, a, b)

    def scrollok(self, *args):
        test_log(2, *args)

    def timeout(self, *args):
        test_log(2, *args)


class StandardScreen(FakeCursesWindow):
    def __init__(self):
        global fakeDisplay, fakeInput
        test_log(2)
        FakeCursesWindow.__init__(self, 0, 0)
        self.cmdCount = -1
        fakeDisplay = FakeDisplay()
        self.fakeDisplay = fakeDisplay
        fakeInput = FakeInput(fakeDisplay)
        self.fakeInput = fakeInput
        self.movie = False

    def set_fake_inputs(self, cmdList):
        self.fakeInput.set_inputs(cmdList)

    def getmaxyx(self):
        test_log(2)
        return (self.fakeDisplay.rows, self.fakeDisplay.cols)

    def refresh(self, *args):
        test_log(2, *args)

    def test_find_text(self, screenText):
        return fakeDisplay.find_text(screenText)

    def test_rendered_command_count(self, cmdCount):
        if self.cmdCount != cmdCount:
            fakeInput.waitingForRefresh = False
            self.cmdCount = cmdCount
            if self.movie:
                fakeDisplay.show()


def baudrate(*args):
    test_log(2, *args)
    return -1


def can_change_color(*args):
    test_log(2, *args)
    return 1


def color_content(*args):
    test_log(2, *args)


def color_pair(*args):
    test_log(2, *args)
    return fakeDisplay.get_color_pair(*args)


def curs_set(*args):
    test_log(2, *args)


def errorpass(*args):
    test_log(2, *args)


def getch(*args):
    test_log(2, *args)
    return constants.ERR


def add_mouse_event(mouse_event):
    test_log(2)
    return mouseEvents.append(mouse_event)


def getmouse(*args):
    test_log(2, *args)
    return mouseEvents.pop()


def has_colors(*args):
    test_log(2, *args)
    return True


def init_color(*args):
    test_log(2, *args)


def init_pair(*args):
    test_log(4, *args)


def keyname(*args):
    test_log(2, *args)
    # Raise expected exception types.
    a = int(*args)  # ValueError.
    if a >= 2 ** 31:
        raise OverflowError()
    if a < 0:
        raise ValueError()


def meta(*args):
    test_log(2, *args)


def mouseinterval(*args):
    test_log(2, *args)


def mousemask(*args):
    test_log(2, *args)


def newwin(*args):
    test_log(2, *args)
    return FakeCursesWindow(args[0], args[1])


def raw(*args):
    test_log(2, *args)


def resizeterm(*args):
    test_log(2, *args)


def start_color(*args):
    test_log(2, *args)


def ungetch(*args):
    test_log(2, *args)


def use_default_colors(*args):
    test_log(2, *args)


def get_pair(*args):
    fakeDisplay.get_color_pair(*args)
    test_log(2, *args)


def wrapper(fun, *args, **kw):
    standardScreen = StandardScreen()
    fun(standardScreen, *args, **kw)
