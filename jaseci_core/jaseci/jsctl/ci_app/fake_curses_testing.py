# -*- coding: latin-1 -*-

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
import inspect
import os
import sys
import tempfile
import unittest

from . import ci_program
from . import curses_util

# from .curses_util import *


def debug_print_stack(*args):
    stack = inspect.stack()[1:]
    stack.reverse()
    lines = []
    for i, frame in enumerate(stack):
        lines.append(
            u"stack %2d %14s %4s %s"
            % (i, os.path.split(frame[1])[1], frame[2], frame[3])
        )
    print(u"\n".join(lines))


class FakeCursesTestCase(unittest.TestCase):
    def set_up(self):
        self.cursesScreen = curses.StandardScreen()
        self.prg = ci_program.CiProgram()
        self.prg.set_up_curses(self.cursesScreen)
        # For testing, use the internal clipboard. Using the system clipboard
        # can create races between tests running in parallel.
        self.prg.clipboard.set_os_handlers(None, None)

    def find_text_and_click(self, timeStamp, screenText, bState):
        caller = inspect.stack()[1]
        callerText = u"\n  %s:%s:%s(): " % (
            os.path.split(caller[1])[1],
            caller[2],
            caller[3],
        )

        def create_event(display, cmdIndex):
            row, col = self.find_text(screenText)
            if row < 0:
                output = u"%s at index %d, did not find %r" % (
                    callerText,
                    cmdIndex,
                    screenText,
                )
                if self.cursesScreen.movie:
                    print(output)
                else:
                    self.fail(output)
            # Note that the mouse info is x,y (col, row).
            info = (timeStamp, col, row, 0, bState)
            curses.add_mouse_event(info)
            return curses.KEY_MOUSE

        return create_event

    def mouse_event(self, timeStamp, mouseRow, mouseCol, bState):
        """
        bState may be a logical or of:
          curses.BUTTON1_PRESSED;
          curses.BUTTON1_RELEASED;
          ...
          curses.BUTTON_SHIFT
          curses.BUTTON_CTRL
          curses.BUTTON_ALT
        """
        assert isinstance(timeStamp, int)
        assert isinstance(mouseRow, int)
        assert isinstance(mouseCol, int)
        assert isinstance(bState, int)
        # Note that the mouse info is x,y (col, row).
        info = (timeStamp, mouseCol, mouseRow, 0, bState)

        def create_event(display, cmdIndex):
            curses.add_mouse_event(info)
            return curses.KEY_MOUSE

        return create_event

    def add_mouse_info(self, timeStamp, mouseRow, mouseCol, bState):
        """
        bState may be a logical or of:
          curses.BUTTON1_PRESSED;
          curses.BUTTON1_RELEASED;
          ...
          curses.BUTTON_SHIFT
          curses.BUTTON_CTRL
          curses.BUTTON_ALT
        """
        assert isinstance(timeStamp, int)
        assert isinstance(mouseRow, int)
        assert isinstance(mouseCol, int)
        assert isinstance(bState, int)
        # Note that the mouse info is x,y (col, row).
        info = (timeStamp, mouseCol, mouseRow, 0, bState)

        def create_event(display, cmdIndex):
            curses.add_mouse_event(info)
            return None

        return create_event

    def call(self, *args):
        """Call arbitrary function as a 'fake input'."""
        caller = inspect.stack()[1]
        callerText = u"\n  %s:%s:%s(): " % (
            os.path.split(caller[1])[1],
            caller[2],
            caller[3],
        )

        def caller(display, cmdIndex):
            try:
                args[0](*args[1:])
            except Exception as e:
                output = callerText + u" at index " + str(cmdIndex)
                print(output)
                self.fail(e)
            return None

        return caller

    def display_check(self, *args):
        assert isinstance(args[0], int)
        assert isinstance(args[1], int)
        assert isinstance(args[2], list)
        caller = inspect.stack()[1]
        callerText = u"\n  %s:%s:%s(): " % (
            os.path.split(caller[1])[1],
            caller[2],
            caller[3],
        )

        def display_checker(display, cmdIndex):
            result = display.check_text(*args)
            if result is not None:
                output = callerText + u" at index " + str(cmdIndex) + result
                if self.cursesScreen.movie:
                    print(output)
                else:
                    self.fail(output)
            return None

        return display_checker

    def display_find_check(self, *args):
        """
        Args:
            find_string (unicode): locate this string.
            check_string (unicode): verify this follows |find_string|.
        """
        assert len(args) == 2
        assert isinstance(args[0], unicode)
        assert isinstance(args[1], unicode)
        caller = inspect.stack()[1]
        callerText = u"\n  %s:%s:%s(): " % (
            os.path.split(caller[1])[1],
            caller[2],
            caller[3],
        )

        def display_find_checker(display, cmdIndex):
            find_string, check_string = args
            row, col = display.find_text(find_string)
            result = display.check_text(
                row, col + len(find_string), [check_string])
            if result is not None:
                output = callerText + u" at index " + str(cmdIndex) + result
                if self.cursesScreen.movie:
                    print(output)
                else:
                    self.fail(output)
            return None

        return display_find_checker

    def display_check_not(self, *args):
        """
        Verify that the display does not match.
        """
        assert isinstance(args[0], int)
        caller = inspect.stack()[1]
        callerText = "\n  %s:%s:%s(): " % (
            os.path.split(caller[1])[1],
            caller[2],
            caller[3],
        )

        def display_checker_not(display, cmdIndex):
            result = display.check_text(*args)
            if result is None:
                output = callerText + u" at index " + str(cmdIndex)
                if self.cursesScreen.movie:
                    print(output)
                else:
                    self.fail(output)
            return None

        return display_checker_not

    def display_check_style(self, *args):
        """*args are (row, col, height, width, colorPair)."""
        (row, col, height, width, colorPair) = args
        assert height != 0
        assert width != 0
        assert colorPair is not None
        caller = inspect.stack()[1]
        callerText = u"\n  %s:%s:%s(): " % (
            os.path.split(caller[1])[1],
            caller[2],
            caller[3],
        )

        def display_style_checker(display, cmdIndex):
            result = display.check_style(*args)
            if result is not None:
                output = callerText + u" at index " + str(cmdIndex) + result
                if self.cursesScreen.movie:
                    print(output)
                else:
                    self.fail(output)
            return None

        return display_style_checker

    def find_text(self, screenText):
        """Locate |screenText| on the display, returning row, col."""
        return self.cursesScreen.test_find_text(screenText)

    def cursor_check(self, expectedRow, expectedCol):
        assert isinstance(expectedRow, int)
        assert isinstance(expectedCol, int)
        caller = inspect.stack()[1]
        callerText = u"in %s:%s:%s(): " % (
            os.path.split(caller[1])[1],
            caller[2],
            caller[3],
        )

        def cursor_checker(display, cmdIndex):
            if self.cursesScreen.movie:
                return None
            win = self.prg.programWindow.focusedWindow
            tb = win.textBuffer
            screenRow, screenCol = self.cursesScreen.getyx()
            self.assertEqual(
                (
                    win.top + tb.penRow - win.scrollRow,
                    win.left + tb.penCol - win.scrollCol,
                ),
                (screenRow, screenCol),
                callerText + u"internal mismatch",
            )
            self.assertEqual(
                (expectedRow, expectedCol), (screenRow, screenCol), callerText
            )
            return None

        return cursor_checker

    def path_to_sample(self, relPath):
        path = os.path.dirname(os.path.dirname(__file__))
        return os.path.join(path, u"sample", relPath)

    def pref_check(self, *args):
        assert isinstance(args[0], unicode)
        assert isinstance(args[1], unicode)
        assert isinstance(args[2], (int, bool))
        caller = inspect.stack()[1]
        callerText = u"\n  %s:%s:%s(): " % (
            os.path.split(caller[1])[1],
            caller[2],
            caller[3],
        )

        def pref_checker(display, cmdIndex):
            result = self.prg.prefs.category(args[0])[args[1]]
            if result != args[2]:
                output = u"%s at index %s, expected %r, found %r" % (
                    callerText,
                    unicode(cmdIndex),
                    args[2],
                    result,
                )
                if self.cursesScreen.movie:
                    print(output)
                else:
                    self.fail(output)
            return None

        return pref_checker

    def print_parser_state(self):
        caller = inspect.stack()[1]
        callerText = u"in %s:%s:%s(): " % (
            os.path.split(caller[1])[1],
            caller[2],
            caller[3],
        )

        def redo_chain(display, cmdIndex):
            print("Parser state", callerText)
            tb = self.prg.programWindow.focusedWindow.textBuffer
            tb.parser.debug_log(print, tb.parser.data)
            return None

        return redo_chain

    def print_redo_state(self):
        caller = inspect.stack()[1]
        callerText = u"in %s:%s:%s(): " % (
            os.path.split(caller[1])[1],
            caller[2],
            caller[3],
        )

        def redo_state(display, cmdIndex):
            print("Redo state", callerText)
            tb = self.prg.programWindow.focusedWindow.textBuffer
            tb.print_redo_state(print)
            return None

        return redo_state

    def resize_screen(self, rows, cols):
        assert isinstance(rows, int)
        assert isinstance(cols, int)

        def set_screen_size(display, cmdIndex):
            self.cursesScreen.fakeDisplay.set_screen_size(rows, cols)
            return curses.KEY_RESIZE

        return set_screen_size

    def set_clipboard(self, text):
        assert isinstance(text, str)
        caller = inspect.stack()[1]
        callerText = u"in %s:%s:%s(): " % (
            os.path.split(caller[1])[1],
            caller[2],
            caller[3],
        )

        def copy_to_clipboard(display, cmdIndex):
            self.assertTrue(self.prg.clipboard.copy, callerText)
            self.prg.clipboard.copy(text)
            return None

        return copy_to_clipboard

    def set_movie_mode(self, enabled):
        self.cursesScreen.movie = enabled
        self.cursesScreen.fakeInput.isVerbose = enabled

    def write_text(self, text):
        assert isinstance(text, unicode), type(text)
        caller = inspect.stack()[1]
        callerText = u"in %s:%s:%s(): " % (
            os.path.split(caller[1])[1],
            caller[2],
            caller[3],
        )

        def copy_to_clipboard(display, cmdIndex):
            self.assertTrue(self.prg.clipboard.copy, callerText)
            self.prg.clipboard.copy(text)
            return curses_util.CTRL_V

        return copy_to_clipboard

    def check_not_reached(self, depth=1):
        """Check that this step doesn't occur. E.g. verify the app exited.

        Args:
          depth (int): how many stack frames up to report as the error location.
        """
        caller = inspect.stack()[depth]
        callerText = u"\n  %s:%s:%s(): " % (
            os.path.split(caller[1])[1],
            caller[2],
            caller[3],
        )

        def check_end_of_inputs(display, cmdIndex):
            self.fail(
                callerText + "\n  Unexpectedly ran out of fake inputs. Consider adding"
                " CTRL_Q (and 'n' if necessary)."
            )
            return None

        return check_end_of_inputs

    def run_with_fake_inputs(self, fakeInputs, argv=None):
        assert hasattr(fakeInputs, "__getitem__") or hasattr(
            fakeInputs, "__iter__")
        if argv is None:
            argv = ["no_argv"]
        sys.argv = argv
        self.cursesScreen.set_fake_inputs(
            fakeInputs
            + [
                self.check_not_reached(2),
            ]
        )
        self.assertTrue(self.prg)
        self.assertFalse(self.prg.exiting)
        self.prg.run()
        # curses.print_fake_display()
        if ci_program.userConsoleMessage:
            message = ci_program.userConsoleMessage
            ci_program.userConsoleMessage = None
            self.fail(message)
        # Check that the application is closed down (don't leave it running
        # across tests).
        self.assertTrue(self.prg.exiting)
        self.assertEqual(
            self.cursesScreen.fakeInput.inputsIndex, len(fakeInputs) - 1)
        # Handy for debugging.
        if 0:
            caller = inspect.stack()[1]
            callerText = u"  %s:%s:%s(): " % (
                os.path.split(caller[1])[1],
                caller[2],
                caller[3],
            )
            print(u"\n-------- finished", callerText)

    def run_with_test_file(self, kTestFile, fakeInputs):
        if os.path.isfile(kTestFile):
            os.unlink(kTestFile)
        self.assertFalse(os.path.isfile(kTestFile))
        self.run_with_fake_inputs(fakeInputs, ["ci_test_program", kTestFile])

    def selection_document_check(
        self,
        expectedPenRow,
        expectedPenCol,
        expectedMarkerRow,
        expectedMarkerCol,
        expectedMode,
    ):
        caller = inspect.stack()[1]
        callerText = u"in %s:%s:%s(): " % (
            os.path.split(caller[1])[1],
            caller[2],
            caller[3],
        )

        def checker(display, cmdIndex):
            selection = self.prg.get_document_selection()
            self.assertEqual(
                (
                    expectedPenRow,
                    expectedPenCol,
                    expectedMarkerRow,
                    expectedMarkerCol,
                    expectedMode,
                ),
                selection,
                callerText,
            )

        return checker

    def selection_check(
        self,
        expectedPenRow,
        expectedPenCol,
        expectedMarkerRow,
        expectedMarkerCol,
        expectedMode,
    ):
        caller = inspect.stack()[1]
        callerText = u"in %s:%s:%s(): " % (
            os.path.split(caller[1])[1],
            caller[2],
            caller[3],
        )

        def checker(display, cmdIndex):
            selection = self.prg.get_selection()
            self.assertEqual(
                (
                    expectedPenRow,
                    expectedPenCol,
                    expectedMarkerRow,
                    expectedMarkerCol,
                    expectedMode,
                ),
                selection,
                callerText,
            )

        return checker

    def tear_down(self):
        # Disable mouse tracking in xterm.
        sys.stdout.write(u"\033[?1002l")
        # Disable Bracketed Paste Mode.
        sys.stdout.write(u"\033[?2004l")
