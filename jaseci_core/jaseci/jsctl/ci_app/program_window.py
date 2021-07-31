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

import curses
import os
import signal
import sys

from . import curses_util
from . import debug_window
from . import file_manager_window
from . import log
from . import prediction_window
from . import window
from . import config


class ProgramWindow(window.ActiveWindow):
    """The outermost window. This window doesn't draw content itself. It is
    primarily a container the child windows that make up the UI. The program
    window is expected to be a singleton. The program window has no parent (the
    parent is None). Calls that propagate up the window tree stop here or jump
    over to the |program|."""

    def __init__(self, program):
        if config.strict_debug:
            assert issubclass(program.__class__,
                              ci_program.CiProgram), self
        window.ActiveWindow.__init__(self, program, None)
        self.clicks = 0
        self.focusedWindow = None
        self.modalUi = None
        self.program = program
        self.priorClick = 0
        self.savedMouseButton1Down = False
        self.savedMouseWindow = None
        self.savedMouseX = -1
        self.savedMouseY = -1
        self.showLogWindow = self.program.prefs.startup["showLogWindow"]
        self.debugWindow = debug_window.DebugWindow(self.program, self)
        self.debugUndoWindow = debug_window.DebugUndoWindow(
            self.program, self)
        self.logWindow = window.LogWindow(self.program, self)
        self.popupWindow = window.PopupWindow(self.program, self)
        self.paletteWindow = window.PaletteWindow(self.program, self)
        # The input window is the main document window.
        self.inputWindow = window.InputWindow(self.program, self)
        self.inputWindow.parent = self
        # Set up file manager.
        self.fileManagerWindow = file_manager_window.FileManagerWindow(
            self.program, self, self.inputWindow
        )
        self.fileManagerWindow.parent = self
        # Set up prediction.
        self.predictionWindow = prediction_window.PredictionWindow(
            self.program, self
        )
        self.predictionWindow.parent = self
        # Put the input window in front on startup.
        self.inputWindow.reattach()

    def change_focus_to(self, change_to):
        self.focusedWindow.controller.on_change()
        # Unfocus all the windows from the prior focused window to the common
        # root.
        commonRoot = self.find_common_root(self.focusedWindow, change_to)
        current = self.focusedWindow
        while current != commonRoot:
            if current.isFocusable:
                current.unfocus()
            current = current.parent
        self.set_focused_window(change_to)

    def debug_draw(self, win):
        if self.showLogWindow:
            self.debugWindow.debug_draw(self.program, win)
            self.debugUndoWindow.debug_undo_draw(win)

    def execute_command_list(self, cmdList):
        for cmd, eventInfo in cmdList:
            self.do_pre_command()
            if cmd == curses.KEY_RESIZE:
                self.handle_screen_resize(self.focusedWindow)
                continue
            self.focusedWindow.controller.do_command(cmd, eventInfo)
            if cmd == curses.KEY_MOUSE:
                self.handle_mouse(eventInfo)
            self.focusedWindow.controller.on_change()

    def find_common_root(self, first, second):
        """Find the Window that is the parent of both |first| and |second|. If
        |first| is a (grand*)parent of |second|, return |first| (or vice versa).
        """
        # assert self.focusedWindow is not change_to
        if first is second:
            return first
        firstPath = [first]
        while firstPath[-1].parent:
            firstPath.append(firstPath[-1].parent)
            if firstPath[-1] == second:
                return second
        secondPath = [second]
        while secondPath[-1].parent:
            secondPath.append(secondPath[-1].parent)
            if secondPath[-1] == first:
                return first
        # assert firstPath[-1] is secondPath[-1]
        # Assumptions: The first unequal match will never be found at [-1]. A
        # match will always be found before exhausting the lists. It doesn't
        # matter which list is longer.
        for i in range(len(firstPath)):
            if firstPath[-(i + 1)] is not secondPath[-(i + 1)]:
                root = firstPath[-i]
                break
        return root

    def focus(self):
        self.set_focused_window(self.zOrder[-1])

    def set_focused_window(self, window):
        # Depth-first search for focusable window.
        depth = [window]
        while len(depth):
            possibility = depth.pop()
            if possibility.isFocusable:
                if config.strict_debug:
                    assert issubclass(possibility.__class__,
                                      window.ActiveWindow)
                    assert possibility.controller
                self.focusedWindow = possibility
                self.focusedWindow.focus()
                self.focusedWindow.textBuffer.compound_change_push()
                return
            depth += possibility.zOrder
            log.info(depth)
        log.error("focusable window not found")

    def do_pre_command(self):
        # Reset UI elements that adjust when new commands are issued.
        # E.g. set_message()
        win = self.focusedWindow
        while win is not None and win is not self:
            win.do_pre_command()
            win = win.parent

    def long_time_slice(self):
        """returns whether work is finished (no need to call again)."""
        win = self.focusedWindow
        while win is not None and win is not self:
            if not win.long_time_slice():
                return False
            win = win.parent
        return True

    def short_time_slice(self):
        """returns whether work is finished (no need to call again)."""
        win = self.focusedWindow
        while win is not None and win is not self:
            if not win.short_time_slice():
                return False
            # assert win is not win.parent
            win = win.parent
        return True

    def clicked_nearby(self, row, col):
        y, x = self.priorClickRowCol
        return y - 1 <= row <= y + 1 and x - 1 <= col <= x + 1

    def handle_mouse(self, info):
        """Mouse handling is a special case. The getch() curses function will
        signal the existence of a mouse event, but the event must be fetched and
        parsed separately."""
        (_, mouseCol, mouseRow, _, bState) = info[0]
        log.mouse()
        eventTime = info[1]
        rapidClickTimeout = 0.5

        def find_window(parent, mouseRow, mouseCol):
            for window in reversed(parent.zOrder):
                if window.contains(mouseRow, mouseCol):
                    return find_window(window, mouseRow, mouseCol)
            return parent

        window = find_window(self, mouseRow, mouseCol)
        if window == self:
            log.mouse("click landed on screen")
            return
        if self.focusedWindow != window and window.isFocusable:
            log.debug("before change focus")
            window.change_focus_to(window)
            log.debug("after change focus")
        mouseRow -= window.top
        mouseCol -= window.left
        log.mouse(mouseRow, mouseCol)
        log.mouse("\n", window)
        button1WasDown = self.savedMouseButton1Down
        self.savedMouseButton1Down = False
        # log.info('bState', curses_util.mouse_button_name(bState))
        if bState & curses.BUTTON1_RELEASED:
            if button1WasDown:
                log.mouse(bState, curses.BUTTON1_RELEASED)
                if self.priorClick + rapidClickTimeout <= eventTime:
                    window.mouse_release(
                        mouseRow,
                        mouseCol,
                        bState & curses.BUTTON_SHIFT,
                        bState & curses.BUTTON_CTRL,
                        bState & curses.BUTTON_ALT,
                    )
                # else:
                #  signal.setitimer(signal.ITIMER_REAL, rapidClickTimeout)
            else:
                # Some terminals (linux?) send BUTTON1_RELEASED after moving the
                # mouse. Specifically if the terminal doesn't use button 4 for
                # mouse movement. Mouse drag or mouse wheel movement done.
                pass
        elif bState & curses.BUTTON1_PRESSED:
            self.savedMouseButton1Down = True
            if self.priorClick + rapidClickTimeout > eventTime and self.clicked_nearby(
                mouseRow, mouseCol
            ):
                self.clicks += 1
                self.priorClick = eventTime
                if self.clicks == 2:
                    window.mouse_double_click(
                        mouseRow,
                        mouseCol,
                        bState & curses.BUTTON_SHIFT,
                        bState & curses.BUTTON_CTRL,
                        bState & curses.BUTTON_ALT,
                    )
                else:
                    window.mouse_triple_click(
                        mouseRow,
                        mouseCol,
                        bState & curses.BUTTON_SHIFT,
                        bState & curses.BUTTON_CTRL,
                        bState & curses.BUTTON_ALT,
                    )
                    self.clicks = 1
            else:
                self.clicks = 1
                self.priorClick = eventTime
                self.priorClickRowCol = (mouseRow, mouseCol)
                window.mouse_click(
                    mouseRow,
                    mouseCol,
                    bState & curses.BUTTON_SHIFT,
                    bState & curses.BUTTON_CTRL,
                    bState & curses.BUTTON_ALT,
                )
        elif bState & (curses.BUTTON2_PRESSED | 0x200000):
            window.mouse_wheel_up(
                bState & curses.BUTTON_SHIFT,
                bState & curses.BUTTON_CTRL,
                bState & curses.BUTTON_ALT,
            )
        elif bState & (curses.BUTTON4_PRESSED | curses.REPORT_MOUSE_POSITION):
            # Notes from testing:
            # Mac seems to send BUTTON4_PRESSED during mouse move; followed by
            #   BUTTON4_RELEASED.
            # Linux seems to send REPORT_MOUSE_POSITION during mouse move;
            # followed by
            #   BUTTON1_RELEASED.
            if self.savedMouseX == mouseCol and self.savedMouseY == mouseRow:
                if bState & curses.REPORT_MOUSE_POSITION:
                    # This is a hack for dtterm mouse wheel on Mac OS X.
                    window.mouse_wheel_up(
                        bState & curses.BUTTON_SHIFT,
                        bState & curses.BUTTON_CTRL,
                        bState & curses.BUTTON_ALT,
                    )
                else:
                    # This is the normal case:
                    window.mouse_wheel_down(
                        bState & curses.BUTTON_SHIFT,
                        bState & curses.BUTTON_CTRL,
                        bState & curses.BUTTON_ALT,
                    )
            else:
                if self.savedMouseWindow and self.savedMouseWindow is not window:
                    mouseRow += window.top - self.savedMouseWindow.top
                    mouseCol += window.left - self.savedMouseWindow.left
                    window = self.savedMouseWindow
                window.mouse_moved(
                    mouseRow,
                    mouseCol,
                    bState & curses.BUTTON_SHIFT,
                    bState & curses.BUTTON_CTRL,
                    bState & curses.BUTTON_ALT,
                )
        elif bState & curses.BUTTON4_RELEASED:
            # Mouse drag or mouse wheel movement done.
            log.mouse("BUTTON4_RELEASED")
            pass
        else:
            log.mouse(
                "got bState", curses_util.mouse_button_name(
                    bState), hex(bState)
            )
        self.savedMouseWindow = window
        self.savedMouseX = mouseCol
        self.savedMouseY = mouseRow

    def handle_screen_resize(self, window):
        # log.debug('handle_screen_resize -----------------------')
        if sys.platform == "darwin":
            # Some terminals seem to resize the terminal and others leave it
            # to the application to resize the curses terminal.
            rows, cols = curses_util.terminal_size()
            curses.resizeterm(rows, cols)
        self.top = self.left = 0
        self.rows, self.cols = window.mainCursesWindow.getmaxyx()
        self.layout()
        window.controller.on_change()
        self.render()

    def hide(self):
        pass

    def layout(self):
        """Arrange the debug, log, and input windows."""
        rows, cols = self.rows, self.cols
        # log.detail('layout', rows, cols)
        if self.showLogWindow:
            inputWidth = min(88, cols)
            debugWidth = max(cols - inputWidth - 1, 0)
            debugRows = 20
            self.debugWindow.reshape(0, inputWidth + 1, debugRows, debugWidth)
            self.debugUndoWindow.reshape(
                debugRows, inputWidth + 1, rows - debugRows, debugWidth
            )
            self.logWindow.reshape(debugRows, 0, rows - debugRows, inputWidth)
            rows = debugRows
        else:
            inputWidth = cols
        if 1:  # Full screen.
            for window in self.zOrder:
                window.reshape(0, 0, rows, inputWidth)
        else:  # Split horizontally.
            count = len(self.zOrder)
            eachRows = rows // count
            for i, window in enumerate(self.zOrder[:-1]):
                window.reshape(eachRows * i, 0, eachRows, inputWidth)
            self.zOrder[-1].reshape(
                eachRows * (count - 1), 0, rows -
                eachRows * (count - 1), inputWidth
            )

    def next_focusable_window(self, start, reverse=False):
        # Keep the tab focus in the child branch. (The child view will call
        # this, tell the child there is nothing to tab to up here).
        return None

    def normalize(self):
        self.present_modal(None)

    def on_pref_changed(self, category, name):
        pass

    def present_modal(self, change_to, top=0, left=0):
        if self.modalUi is not None:
            # self.modalUi.controller.on_change()
            self.modalUi.hide()
        log.info("\n", change_to)
        self.modalUi = change_to
        if self.modalUi is not None:
            self.modalUi.move_size_to_fit(top, left)
            self.modalUi.bring_to_front()

    def quit_now(self):
        self.program.quit_now()

    def render(self):
        if self.showLogWindow:
            self.logWindow.render()
        window.ActiveWindow.render(self)
        wndow = self.focusedWindow
        self.debug_draw(wndow)
        penRow = wndow.textBuffer.penRow
        penCol = wndow.textBuffer.penCol
        if (
            wndow.showCursor
            and penRow >= wndow.scrollRow
            and penRow < wndow.scrollRow + wndow.rows
        ):
            self.program.backgroundFrame.set_cursor(
                (
                    wndow.top + penRow - wndow.scrollRow,
                    wndow.left + penCol - wndow.scrollCol,
                )
            )
        else:
            self.program.backgroundFrame.set_cursor(None)

    def reshape(self, top, left, rows, cols):
        window.ActiveWindow.reshape(self, top, left, rows, cols)
        self.layout()

    def bring_to_front(self):
        pass

    def unfocus(self):
        pass
