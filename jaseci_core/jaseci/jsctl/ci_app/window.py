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

import bisect
import os
import sys
import types
import curses

from . import config, bookmark
from . import controller
from . import cu_editor
from . import em_editor
from . import string
from . import text_buffer
from . import vi_editor
from . import log, selectable

# The terminal area that the curses can draw to.
mainCursesWindow = None


class ViewWindow:
    """A view window is a base window that does not get focus or have
    TextBuffer.

    See class ActiveWindow for a window that can get focus. See class Window for
    a window that can get focus and have a TextBuffer.
    """

    def __init__(self, program, parent):
        """
        Args:
          parent is responsible for the order in which this window is updated,
          relative to its siblings.
        """
        if config.strict_debug:
            assert issubclass(self.__class__, ViewWindow), self
            assert issubclass(program.__class__, ci_program.CiProgram), self
            if parent is not None:
                assert issubclass(parent.__class__, ViewWindow), parent
        self.program = program
        self.parent = parent
        self.isFocusable = False
        self.top = 0
        self.left = 0
        self.rows = 1
        self.cols = 1
        self.scrollRow = 0
        self.scrollCol = 0
        self.showCursor = True
        self.writeLineRow = 0
        self.zOrder = []

    def add_str(self, row, col, text, colorPair):
        """Overwrite text at row, column with text.

        The caller is responsible for avoiding overdraw.
        """
        if config.strict_debug:
            log.check_le(row, self.rows)
            log.check_le(col, self.cols)
        self.program.backgroundFrame.add_str(
            self.top + row, self.left + col, text.encode("utf-8"), colorPair
        )

    def reattach(self):
        self.set_parent(self.parent)

    def blank(self, colorPair):
        """Clear the window."""
        for i in range(self.rows):
            self.add_str(i, 0, " " * self.cols, colorPair)

    def bring_child_to_front(self, child):
        """Bring it to the top layer."""
        try:
            self.zOrder.remove(child)
        except ValueError:
            pass
        self.zOrder.append(child)

    def bring_to_front(self):
        """Bring it to the top layer."""
        self.parent.bring_child_to_front(self)

    def change_focus_to(self, change_to):
        if config.strict_debug:
            assert issubclass(self.__class__, ViewWindow), self
            assert issubclass(change_to.__class__, ViewWindow), change_to
        topWindow = self
        while topWindow.parent:
            topWindow = topWindow.parent
        topWindow.change_focus_to(change_to)

    def color_pref(self, colorType, delta=0):
        return self.program.color.get(colorType, delta)

    def contains(self, row, col):
        """Determine whether the position at row, col lay within this window."""
        for i in self.zOrder:
            if i.contains(row, col):
                return i
        return (
            self.top <= row < self.top + self.rows
            and self.left <= col < self.left + self.cols
            and self
        )

    def debug_draw(self):
        programWindow = self
        while programWindow.parent is not None:
            programWindow = programWindow.parent
        programWindow.debug_draw(self)

    def deselect(self):
        pass

    def detach(self):
        """Hide the window by removing self from parents' children, but keep
        same parent to be reattached later."""
        try:
            self.parent.zOrder.remove(self)
        except ValueError:
            pass

    def layout_horizontally(self, children, separation=0):
        left = self.left
        cols = self.cols
        for view in children:
            preferredCols = view.preferred_size(self.rows, max(0, cols))[1]
            view.reshape(self.top, left, self.rows,
                         max(0, min(cols, preferredCols)))
            delta = view.cols + separation
            left += delta
            cols -= delta

    def layout_vertically(self, children, separation=0):
        top = self.top
        rows = self.rows
        for view in children:
            preferredRows = view.preferred_size(max(0, rows), self.cols)[0]
            view.reshape(top, self.left, max(
                0, min(rows, preferredRows)), self.cols)
            delta = view.rows + separation
            top += delta
            rows -= delta

    def mouse_click(self, paneRow, paneCol, shift, ctrl, alt):
        pass

    def mouse_double_click(self, paneRow, paneCol, shift, ctrl, alt):
        pass

    def mouse_moved(self, paneRow, paneCol, shift, ctrl, alt):
        pass

    def mouse_release(self, paneRow, paneCol, shift, ctrl, alt):
        pass

    def mouse_triple_click(self, paneRow, paneCol, shift, ctrl, alt):
        pass

    def mouse_wheel_down(self, shift, ctrl, alt):
        pass

    def mouse_wheel_up(self, shift, ctrl, alt):
        pass

    def move_to(self, top, left):
        self.top = top
        self.left = left

    def move_by(self, top, left):
        self.top += top
        self.left += left

    def _child_focusable_window(self, reverse=False):
        windows = self.zOrder[:]
        if reverse:
            windows.reverse()
        for i in windows:
            if i.isFocusable:
                return i
            else:
                r = i._child_focusable_window(reverse)
                if r is not None:
                    return r

    def next_focusable_window(self, start, reverse=False):
        """Windows without |isFocusable| are skipped. Ignore (skip) |start| when
        searching.

        Args:
          start (window): the child window to start from. If |start| is not
              found, start from the first child window.
          reverse (bool): if True, find the prior focusable window.

        Returns:
          A window that should be focused.

        See also: show_full_window_hierarchy() which can help in debugging.
        """
        windows = self.parent.zOrder[:]
        if reverse:
            windows.reverse()
        try:
            found = windows.index(start)
        except ValueError:
            found = -1
        windows = windows[found + 1:]
        for i in windows:
            if i.isFocusable:
                return i
            else:
                r = i._child_focusable_window(reverse)
                if r is not None:
                    return r
        r = self.parent.next_focusable_window(self.parent, reverse)
        if r is not None:
            return r
        return self._child_focusable_window(reverse)

    def normalize(self):
        self.parent.normalize()

    def on_pref_changed(self, category, name):
        self.parent.on_pref_changed(category, name)

    def paint(self, row, col, count, colorPair):
        """Paint text a row, column with colorPair.

        fyi, I thought this may be faster than using add_str to paint over the
        text with a different colorPair. It looks like there isn't a significant
        performance difference between chgat and addstr.
        """
        mainCursesWindow.chgat(
            self.top + row, self.left + col, count, colorPair)

    def preferred_size(self, rowLimit, colLimit):
        # Derived classes should override this.
        return rowLimit, colLimit

    def present_modal(self, change_to, paneRow, paneCol):
        self.parent.present_modal(change_to, paneRow, paneCol)

    def prior_focusable_window(self, start):
        return self.next_focusable_window(start, True)

    def quit_now(self):
        self.program.quit_now()

    def render(self):
        """Redraw window."""
        for child in self.zOrder:
            child.render()

    def show_window_hierarchy(self, indent="  "):
        """For debugging."""
        focus = u"[f]" if self.isFocusable else u"[ ]"
        extra = u""
        if hasattr(self, "label"):
            extra += u' "' + self.label + u'"'
        log.info("%s%s%s%s" % (indent, focus, self, extra))
        for child in self.zOrder:
            child.show_window_hierarchy(indent + u"  ")

    def show_full_window_hierarchy(self, indent=u"  "):
        """For debugging."""
        f = self
        while f.parent is not None:
            f = f.parent
        assert f
        f.show_window_hierarchy()

    def do_pre_command(self):
        pass

    def long_time_slice(self):
        """returns whether work is finished (no need to call again)."""
        return True

    def short_time_slice(self):
        """returns whether work is finished (no need to call again)."""
        return True

    def reshape(self, top, left, rows, cols):
        self.move_to(top, left)
        self.resize_to(rows, cols)
        # log.debug(self, top, left, rows, cols)

    def resize_bottom_by(self, rows):
        self.rows += rows

    def resize_by(self, rows, cols):
        self.rows += rows
        self.cols += cols

    def resize_to(self, rows, cols):
        # log.detail(rows, cols, self)
        if config.strict_debug:
            assert rows >= 0, rows
            assert cols >= 0, cols
        self.rows = rows
        self.cols = cols

    def resize_top_by(self, rows):
        self.top += rows
        self.rows -= rows

    def set_parent(self, parent, layerIndex=sys.maxsize):
        """Setting the parent will cause the the window to refresh (i.e. if self
        was hidden with detach() it will no longer be hidden)."""
        if config.strict_debug:
            assert issubclass(self.__class__, ViewWindow), self
            assert issubclass(parent.__class__, ViewWindow), parent
        if self.parent:
            try:
                self.parent.zOrder.remove(self)
            except ValueError:
                pass
        self.parent = parent
        if parent:
            self.parent.zOrder.insert(layerIndex, self)

    def write_line(self, text, color):
        """Simple line writer for static windows."""
        if config.strict_debug:
            assert isinstance(text, unicode)
        text = text[: self.cols]
        text = text + u" " * max(0, self.cols - len(text))
        self.program.backgroundFrame.add_str(
            self.top +
            self.writeLineRow, self.left, text.encode(u"utf-8"), color
        )
        self.writeLineRow += 1

    def get_program(self):
        return self.program


class ActiveWindow(ViewWindow):
    """An ActiveWindow may have focus and a controller."""

    def __init__(self, program, parent):
        if config.strict_debug:
            assert issubclass(self.__class__, ActiveWindow), self
            assert issubclass(program.__class__, ci_program.CiProgram), repr(
                program
            )
            if parent is not None:
                assert issubclass(parent.__class__, ViewWindow), parent
        ViewWindow.__init__(self, program, parent)
        self.controller = None
        self.hasFocus = False
        self.isFocusable = True

    def focus(self):
        """
        Note: to focus a view it must have a controller. Focusing a view without
            a controller would make the program appear to freeze since nothing
            would be responding to user input.
        """
        self.hasFocus = True
        self.controller.focus()

    def set_controller(self, controller):
        if config.strict_debug:
            assert issubclass(self.__class__, Window), self
        self.controller = controller(self)

    def unfocus(self):
        self.hasFocus = False
        self.controller.unfocus()


class Window(ActiveWindow):
    """A Window holds a TextBuffer and a controller that operates on the
    TextBuffer."""

    def __init__(self, program, parent):
        if config.strict_debug:
            assert issubclass(self.__class__, Window), self
            assert issubclass(program.__class__, ci_program.CiProgram), self
            assert issubclass(parent.__class__, ViewWindow), parent
        ActiveWindow.__init__(self, program, parent)
        self.hasCaptiveCursor = self.program.prefs.editor["captiveCursor"]
        self.textBuffer = None

    def mouse_click(self, paneRow, paneCol, shift, ctrl, alt):
        if self.textBuffer:
            self.textBuffer.mouse_click(paneRow, paneCol, shift, ctrl, alt)

    def mouse_double_click(self, paneRow, paneCol, shift, ctrl, alt):
        if self.textBuffer:
            self.textBuffer.mouse_double_click(
                paneRow, paneCol, shift, ctrl, alt)

    def mouse_moved(self, paneRow, paneCol, shift, ctrl, alt):
        if self.textBuffer:
            self.textBuffer.mouse_moved(paneRow, paneCol, shift, ctrl, alt)

    def mouse_release(self, paneRow, paneCol, shift, ctrl, alt):
        if self.textBuffer:
            self.textBuffer.mouse_release(paneRow, paneCol, shift, ctrl, alt)

    def mouse_triple_click(self, paneRow, paneCol, shift, ctrl, alt):
        if self.textBuffer:
            self.textBuffer.mouse_triple_click(
                paneRow, paneCol, shift, ctrl, alt)

    def mouse_wheel_down(self, shift, ctrl, alt):
        if self.textBuffer:
            self.textBuffer.mouse_wheel_down(shift, ctrl, alt)

    def mouse_wheel_up(self, shift, ctrl, alt):
        if self.textBuffer:
            self.textBuffer.mouse_wheel_up(shift, ctrl, alt)

    def preferred_size(self, rowLimit, colLimit):
        return min(rowLimit, self.textBuffer.parser.row_count()), colLimit

    def render(self):
        if self.textBuffer:
            self.textBuffer.draw(self)
        ViewWindow.render(self)

    def set_controller(self, controller):
        ActiveWindow.set_controller(self, controller)
        self.controller.set_text_buffer(self.textBuffer)

    def set_text_buffer(self, textBuffer):
        textBuffer.set_view(self)
        self.textBuffer = textBuffer

    def do_pre_command(self):
        if self.textBuffer is not None:
            self.textBuffer.set_message()

    def long_time_slice(self):
        """returns whether work is finished (no need to call again)."""
        finished = True
        tb = self.textBuffer
        if tb is not None and tb.parser.resumeAtRow < tb.parser.row_count():
            tb.parse_document()
            # If a user event came in while parsing, the parsing will be paused
            # (to be resumed after handling the event).
            finished = tb.parser.resumeAtRow >= tb.parser.row_count()
        for child in self.zOrder:
            finished = finished and child.long_time_slice()
        return finished

    def short_time_slice(self):
        """returns whether work is finished (no need to call again)."""
        tb = self.textBuffer
        if tb is not None:
            tb.parse_screen_maybe()
            return tb.parser.resumeAtRow >= tb.parser.row_count()
        return True


class LabelWindow(ViewWindow):
    """A text label.

    The label is inert, it will pass events to its parent.
    """

    def __init__(self, program, parent, label, preferredWidth=None, align=u"left"):
        if config.strict_debug:
            assert issubclass(program.__class__, ci_program.CiProgram), self
            assert issubclass(parent.__class__, ViewWindow), parent
            assert isinstance(label, unicode)
            assert preferredWidth is None or isinstance(preferredWidth, int)
            assert isinstance(align, unicode)
        ViewWindow.__init__(self, program, parent)
        self.label = label
        self.preferredWidth = preferredWidth
        self.align = -1 if align == u"left" else 1
        self.color = self.program.color.get(u"keyword")

    def preferred_size(self, rowLimit, colLimit):
        if config.strict_debug:
            assert self.parent
            assert rowLimit >= 0
            assert colLimit >= 0
        preferredWidth = (
            self.preferredWidth if self.preferredWidth is not None else len(
                self.label)
        )
        return (min(rowLimit, 1), min(colLimit, preferredWidth))

    def render(self):
        if self.rows <= 0:
            return
        line = self.label[: self.cols]
        line = u"%*s" % (self.cols * self.align, line)
        self.add_str(0, 0, line, self.color)
        ViewWindow.render(self)


class LabeledLine(Window):
    """A single line with a label.

    This is akin to a line prompt or gui modal dialog. It's used for things like
    'find' and 'goto line'.
    """

    def __init__(self, program, parent, label):
        if config.strict_debug:
            assert issubclass(self.__class__, LabeledLine), self
            assert issubclass(program.__class__, ci_program.CiProgram), self
            assert issubclass(parent.__class__, ViewWindow), parent
        Window.__init__(self, program, parent)
        self.host = parent
        tb = text_buffer.TextBuffer(self.program)
        tb.rootGrammar = self.program.prefs.grammars[u"none"]
        self.set_text_buffer(tb)
        self.label = label
        self.leftColumn = ViewWindow(self.program, self)
        # TODO(dschuyler) Add self.rightColumn.

    def focus(self):
        self.bring_to_front()
        if not self.controller:
            log.info(self, repr(self.label))
        Window.focus(self)

    def preferred_size(self, rowLimit, colLimit):
        return min(rowLimit, 1), colLimit

    def render(self):
        # log.info('LabeledLine', self.label, self.rows, self.cols)
        if self.rows <= 0:
            return
        self.leftColumn.add_str(
            0, 0, self.label, self.program.color.get(u"keyword"))
        Window.render(self)

    def reshape(self, top, left, rows, cols):
        labelWidth = len(self.label)
        Window.reshape(self, top, left + labelWidth,
                       rows, max(0, cols - labelWidth))
        self.leftColumn.reshape(top, left, rows, labelWidth)

    def set_label(self, label):
        self.label = label
        self.reshape(self.top, self.left, self.rows, self.cols)


class Menu(ViewWindow):
    """Work in progress on a context menu."""

    def __init__(self, program, host):
        if config.strict_debug:
            assert issubclass(self.__class__, Menu), self
            assert issubclass(host.__class__, ActiveWindow)
        ViewWindow.__init__(self, program, host)
        self.host = host
        self.label = u""
        self.lines = []
        self.commands = []

    def add_item(self, label, command):
        self.lines.append(label)
        self.commands.append(command)

    def clear(self):
        self.lines = []
        self.commands = []

    def move_size_to_fit(self, left, top):
        self.clear()
        self.add_item(u"some menu", None)
        # self.add_item('sort', self.host.textBuffer.sortSelection)
        self.add_item(u"cut", self.host.textBuffer.edit_cut)
        self.add_item(u"paste", self.host.textBuffer.edit_paste)
        longest = 0
        for i in self.lines:
            if len(i) > longest:
                longest = len(i)
        self.reshape(left, top, len(self.lines), longest + 2)

    def render(self):
        color = self.program.color.get(u"context_menu")
        self.writeLineRow = 0
        for i in self.lines[: self.rows]:
            self.write_line(" " + i, color)
        ViewWindow.render(self)


class LineNumbers(ViewWindow):
    def __init__(self, program, host):
        ViewWindow.__init__(self, program, host)
        self.host = host

    def draw_line_numbers(self):
        if config.strict_debug:
            assert isinstance(self.rows, int)
            assert isinstance(self.host.scrollRow, int)
            assert self.rows >= 1
            assert self.host.textBuffer.parser.row_count() >= 1
            assert self.host.scrollRow >= 0
        limit = min(
            self.rows, self.host.textBuffer.parser.row_count() - self.host.scrollRow
        )
        cursorBookmarkColorIndex = None
        visibleBookmarks = self.get_visible_bookmarks(
            self.host.scrollRow, self.host.scrollRow + limit
        )
        currentBookmarkIndex = 0
        colorPrefs = self.program.color
        for i in range(limit):
            color = colorPrefs.get(u"line_number")
            currentRow = self.host.scrollRow + i
            if currentBookmarkIndex < len(visibleBookmarks):
                currentBookmark = visibleBookmarks[currentBookmarkIndex]
            else:
                currentBookmark = None
            # Use a different color if the row is associated with a bookmark.
            if currentBookmark:
                if (
                    currentRow >= currentBookmark.begin
                    and currentRow <= currentBookmark.end
                ):
                    color = colorPrefs.get(
                        currentBookmark.data.get(u"colorIndex"))
                    if self.host.textBuffer.penRow == currentRow:
                        cursorBookmarkColorIndex = currentBookmark.data.get(
                            u"colorIndex"
                        )
                if currentRow + 1 > currentBookmark.end:
                    currentBookmarkIndex += 1
            self.add_str(i, 0, u" %5d " % (currentRow + 1), color)
        # Draw indicators for text off of the left edge.
        if self.host.scrollCol > 0:
            color = colorPrefs.get(u"line_overflow")
            for i in range(limit):
                if self.host.textBuffer.parser.row_width(self.host.scrollRow + i) > 0:
                    self.add_str(i, 6, u" ", color)
        # Draw blank line number rows past the end of the document.
        color = colorPrefs.get(u"outside_document")
        for i in range(limit, self.rows):
            self.add_str(i, 0, u"       ", color)
        # Highlight the line numbers for the current cursor line.
        cursorAt = self.host.textBuffer.penRow - self.host.scrollRow
        if 0 <= cursorAt < limit:
            if cursorBookmarkColorIndex:
                if self.program.prefs.startup[u"numColors"] == 8:
                    color = colorPrefs.get(cursorBookmarkColorIndex)
                else:
                    color = colorPrefs.get(cursorBookmarkColorIndex % 32 + 128)
            else:
                color = colorPrefs.get(u"line_number_current")
            self.add_str(cursorAt, 1, u"%5d" %
                         (self.host.textBuffer.penRow + 1), color)

    def get_visible_bookmarks(self, beginRow, endRow):
        """
        Args:
          beginRow (int): the index of the line number that you want the list of
                          bookmarks to start from.
          endRow (int): the index of the line number that you want the list of
                        bookmarks to end at (exclusive).

        Returns:
          A list containing the bookmarks that are displayed on the screen. If
          there are no bookmarks, returns an empty list.
        """
        bookmarkList = self.host.textBuffer.bookmarks
        beginIndex = endIndex = 0
        if len(bookmarkList):
            needle = bookmark.Bookmark(beginRow, beginRow, {})
            beginIndex = bisect.bisect_left(bookmarkList, needle)
            if beginIndex > 0 and bookmarkList[beginIndex - 1].end >= beginRow:
                beginIndex -= 1
            needle.range = (endRow, endRow)
            endIndex = bisect.bisect_left(bookmarkList, needle)
        return bookmarkList[beginIndex:endIndex]

    def mouse_click(self, paneRow, paneCol, shift, ctrl, alt):
        if ctrl:
            log.info(u"click at", paneRow, paneCol)
            return
        self.host.change_focus_to(self.host)
        tb = self.host.textBuffer
        if self.host.scrollRow + paneRow >= tb.parser.row_count():
            tb.selection_none()
            return
        if shift:
            if tb.selectionMode == selectable.kSelectionNone:
                tb.selection_line()
            self.mouse_release(paneRow, paneCol, shift, ctrl, alt)
        else:
            tb.cursor_move_and_mark(
                self.host.scrollRow + paneRow - tb.penRow,
                0,
                self.host.scrollRow + paneRow - tb.markerRow,
                0,
                selectable.kSelectionNone - tb.selectionMode,
            )
            self.mouse_release(paneRow, paneCol, shift, ctrl, alt)

    def mouse_double_click(self, paneRow, paneCol, shift, ctrl, alt):
        self.host.textBuffer.selection_all()

    def mouse_moved(self, paneRow, paneCol, shift, ctrl, alt):
        log.info(paneRow, paneCol, shift)
        self.host.textBuffer.mouse_moved(
            paneRow, paneCol - self.cols, True, ctrl, alt)

    def mouse_release(self, paneRow, paneCol, shift, ctrl, alt):
        log.info(paneRow, paneCol, shift)
        tb = self.host.textBuffer
        tb.select_line_at(self.host.scrollRow + paneRow)

    def mouse_triple_click(self, paneRow, paneCol, shift, ctrl, alt):
        pass

    def mouse_wheel_down(self, shift, ctrl, alt):
        self.host.mouse_wheel_down(shift, ctrl, alt)

    def mouse_wheel_up(self, shift, ctrl, alt):
        self.host.mouse_wheel_up(shift, ctrl, alt)

    def render(self):
        self.draw_line_numbers()


class LogWindow(ViewWindow):
    def __init__(self, program, parent):
        ViewWindow.__init__(self, program, parent)
        self.lines = log.get_lines()
        self.renderCounter = 0

    def render(self):
        self.renderCounter += 1
        log.meta(u" " * 10, self.renderCounter, u"- screen render -")
        self.writeLineRow = 0
        colorPrefs = self.program.color
        colorA = colorPrefs.get(u"default")
        colorB = colorPrefs.get(u"highlight")
        for i in self.lines[-self.rows:]:
            color = colorA
            if len(i) and i[-1] == u"-":
                color = colorB
            self.write_line(i, color)
        ViewWindow.render(self)


class InteractiveFind(Window):
    def __init__(self, program, host):
        Window.__init__(self, program, host)
        self.host = host
        self.expanded = False
        self.set_controller(cu_editor.InteractiveFind)
        indent = u"  "

        self.findLine = LabeledLine(self.program, self, u"Find: ")
        self.findLine.set_controller(cu_editor.InteractiveFindInput)
        self.findLine.set_parent(self)

        self.replaceLine = LabeledLine(self.program, self, u"Replace: ")
        self.replaceLine.set_controller(cu_editor.InteractiveReplaceInput)
        self.replaceLine.set_parent(self)

        self.matchOptionsRow = RowWindow(self.program, self, 2)
        self.matchOptionsRow.set_parent(self)

        # If findUseRegex is false, re.escape the search.
        OptionsToggle(
            self.program, self.matchOptionsRow, u"regex", u"editor", u"findUseRegex"
        )
        # If findWholeWord, wrap with \b.
        OptionsToggle(
            self.program,
            self.matchOptionsRow,
            u"wholeWord",
            u"editor",
            u"findWholeWord",
        )
        # If findIgnoreCase, pass ignore case flag to regex.
        OptionsToggle(
            self.program,
            self.matchOptionsRow,
            u"ignoreCase",
            u"editor",
            u"findIgnoreCase",
        )
        if 0:
            # Use locale.
            OptionsToggle(
                self.program, self.matchOptionsRow, u"locale", u"editor", u"findLocale"
            )
            # Span lines.
            OptionsToggle(
                self.program,
                self.matchOptionsRow,
                u"multiline",
                u"editor",
                u"findMultiline",
            )
            # Dot matches anything (even \n).
            OptionsToggle(
                self.program, self.matchOptionsRow, u"dotAll", u"editor", u"findDotAll"
            )
            # Unicode match.
            OptionsToggle(
                self.program,
                self.matchOptionsRow,
                u"unicode",
                u"editor",
                u"findUnicode",
            )
            # Replace uppercase with upper and lowercase with lower.
            OptionsToggle(
                self.program,
                self.matchOptionsRow,
                u"smartCaps",
                u"editor",
                u"findReplaceSmartCaps",
            )

        if 0:
            self.scopeOptions, self.scopeRow = self.add_select_options_row(
                indent + u"scope     ",
                [u"file", u"directory", u"openFiles", u"project"],
            )
            (self.changeCaseOptions, self.changeCaseRow) = self.add_select_options_row(
                indent + u"changeCase", [u"none", u"smart", u"upper", u"lower"]
            )
            (self.withinOptions, self.withinOptionsRow) = self.add_select_options_row(
                indent + u"within    ",
                [
                    u"any",
                    u"code",
                    u"comment",
                    u"error",
                    u"markup",
                    u"misspelled",  # Find in misspelled words.
                    u"quoted",  # Find in strings.
                ],
            )
            (
                self.searchSelectionOption,
                self.searchSelectionRow,
            ) = self.add_select_options_row(
                indent + u"selection ", [u"any", u"yes", u"no"]
            )
            (
                self.searchChangedOption,
                self.searchChangedRow,
            ) = self.add_select_options_row(
                indent + u"changed   ", [u"any", u"yes", u"no"]
            )
            self.pathsLine = LabeledLine(self.program, self, u"Paths: ")
            self.pathsLine.set_controller(cu_editor.InteractiveFindInput)
            self.pathsLine.set_parent(self)

    def reattach(self):
        Window.reattach(self)
        # TODO(dschuyler): consider removing expanded control.
        # See https://github.com/google/ci_edit/issues/170
        self.expanded = True
        self.parent.layout()

    def detach(self):
        Window.detach(self)
        self.parent.layout()

    def add_select_options_row(self, label, optionsList):
        """Such as a radio group."""
        optionsRow = OptionsRow(self.program, self)
        optionsRow.color = self.program.color.get(u"keyword")
        optionsRow.add_label(label)
        optionsDict = {}
        optionsRow.begin_group()
        for key in optionsList:
            optionsDict[key] = False
            optionsRow.add_selection(key, optionsDict)
        optionsRow.end_group()
        optionsDict[optionsList[0]] = True
        optionsRow.set_parent(self)
        return optionsDict, optionsRow

    def bring_child_to_front(self, child):
        # The find window doesn't reorder children.
        pass

    def focus(self):
        self.reattach()
        if config.strict_debug:
            assert self.parent
            assert self.findLine.parent
            assert self.rows > 0, self.rows
            assert self.findLine.rows > 0, self.findLine.rows
        self.controller.focus()
        self.change_focus_to(self.findLine)

    def preferred_size(self, rowLimit, colLimit):
        if config.strict_debug:
            assert self.parent
            assert rowLimit >= 0
            assert colLimit >= 0
        if self.parent and self in self.parent.zOrder and self.expanded:
            return (min(rowLimit, len(self.zOrder)), colLimit)
        return (1, -1)

    def expand_find_window(self, expanded):
        self.expanded = expanded
        self.parent.layout()

    def reshape(self, top, left, rows, cols):
        Window.reshape(self, top, left, rows, cols)
        self.layout_vertically(self.zOrder)

    def unfocus(self):
        self.detach()
        Window.unfocus(self)


class MessageLine(ViewWindow):
    """The message line appears at the bottom of the screen."""

    def __init__(self, program, host):
        ViewWindow.__init__(self, program, host)
        self.host = host
        self.message = None
        self.renderedMessage = None

    def render(self):
        colorPrefs = self.program.color
        if self.message:
            if self.message != self.renderedMessage:
                self.writeLineRow = 0
                self.write_line(self.message, colorPrefs.get(u"message_line"))
        else:
            self.blank(colorPrefs.get(u"message_line"))


class StatusLine(ViewWindow):
    """The status line appears at the bottom of the screen.

    It shows the current line and column the cursor is on.
    """

    def __init__(self, program, host):
        ViewWindow.__init__(self, program, host)
        self.host = host

    def render(self):
        tb = self.host.textBuffer
        colorPrefs = self.program.color
        color = colorPrefs.get(u"status_line")
        if self.host.showTips:
            tipRows = help.docs[u"tips"]
            if len(tipRows) + 1 < self.rows:
                for i in range(self.rows):
                    self.add_str(i, 0, u" " * self.cols, color)
                for i, k in enumerate(tipRows):
                    self.add_str(i + 1, 4, k, color)
                self.add_str(
                    1, 40, u"(Press F1 to show/hide tips)", color | curses.A_REVERSE
                )

        statusLine = u""
        if tb.message:
            statusLine = tb.message[0]
            color = (
                tb.message[1]
                if tb.message[1] is not None
                else colorPrefs.get(u"status_line")
            )
        if 0:
            if tb.is_dirty():
                statusLine += u" * "
            else:
                statusLine += u" . "
        # Percentages.
        rowPercentage = 0
        colPercentage = 0
        lineCount = tb.parser.row_count()
        if lineCount:
            rowPercentage = self.host.textBuffer.penRow * 100 // lineCount
            charCount = tb.parser.row_width(self.host.textBuffer.penRow)
            if charCount and self.host.textBuffer.penCol != 0:
                colPercentage = self.host.textBuffer.penCol * 100 // charCount
        # Format.
        rightSide = u""
        if len(statusLine):
            rightSide += u" |"
        if self.program.prefs.startup.get("showLogWindow"):
            rightSide += u" %s | %s |" % (
                tb.cursor_grammar_name(),
                tb.selection_mode_name(),
            )
        rightSide += u" %4d,%2d | %3d%%,%3d%%" % (
            self.host.textBuffer.penRow + 1,
            self.host.textBuffer.penCol + 1,
            rowPercentage,
            colPercentage,
        )
        statusLine += u" " * (self.cols - len(statusLine) -
                              len(rightSide)) + rightSide
        self.add_str(self.rows - 1, 0, statusLine[: self.cols], color)


class TopInfo(ViewWindow):
    def __init__(self, program, host):
        ViewWindow.__init__(self, program, host)
        self.host = host
        self.borrowedRows = 0
        self.lines = []
        self.mode = 2

    def on_change(self):
        if self.mode == 0:
            return
        tb = self.host.textBuffer
        lines = []
        # TODO: Make dynamic topInfo work properly
        if tb.parser.row_count():
            lineCursor = self.host.scrollRow
            line = ""
            # Check for extremely small window.
            if tb.parser.row_count() > lineCursor:
                while len(line) == 0 and lineCursor > 0:
                    line = tb.parser.row_text(lineCursor)
                    lineCursor -= 1
            if len(line):
                indent = len(line) - len(line.lstrip(u" "))
                lineCursor += 1
                while lineCursor < tb.parser.row_count():
                    line = tb.parser.row_text(lineCursor)
                    if not len(line):
                        continue
                    z = len(line) - len(line.lstrip(u" "))
                    if z > indent:
                        indent = z
                        lineCursor += 1
                    else:
                        break
                while indent and lineCursor > 0:
                    line = tb.parser.row_text(lineCursor)
                    if len(line):
                        z = len(line) - len(line.lstrip(u" "))
                        if z < indent:
                            indent = z
                            lines.append(line)
                    lineCursor -= 1
        pathLine = string.path_encode(self.host.textBuffer.fullPath)
        if 1:
            if tb.isReadOnly:
                pathLine += u" [RO]"
        if 1:
            if tb.is_dirty():
                pathLine += u" * "
            else:
                pathLine += u" . "
        lines.append(pathLine[-self.cols:])
        self.lines = lines
        infoRows = len(self.lines)
        if self.mode > 0:
            infoRows = self.mode
        if self.borrowedRows != infoRows:
            self.host.topRows = infoRows
            self.host.layout()
            self.borrowedRows = infoRows

    def render(self):
        """Render the context information at the top of the window."""
        lines = self.lines[-self.mode:]
        lines.reverse()
        color = self.program.color.get("top_info")
        for i, line in enumerate(lines):
            self.add_str(
                i, 0, (line + u" " * (self.cols - len(line))
                       )[: self.cols], color
            )
        for i in range(len(lines), self.rows):
            self.add_str(i, 0, u" " * self.cols, color)

    def reshape(self, top, left, rows, cols):
        self.borrowedRows = 0
        ViewWindow.reshape(self, top, left, rows, cols)


class InputWindow(Window):
    """This is the main content window.

    Often the largest pane displayed.
    """

    def __init__(self, program, host):
        if config.strict_debug:
            assert host
        Window.__init__(self, program, host)
        self.host = host
        self.showFooter = True
        self.savedScrollPositions = {}
        self.showLineNumbers = self.program.prefs.editor.get(
            "showLineNumbers", True)
        self.showMessageLine = True
        self.showRightColumn = True
        self.showTopInfo = True
        self.statusLineCount = 0 if self.program.prefs.status.get(
            "seenTips") else 8

        self.topRows = 2  # Number of lines in default TopInfo status.
        self.controller = controller.MainController(self)
        self.controller.add(em_editor.EmacsEdit(self))
        self.controller.add(vi_editor.ViEdit(self))
        self.controller.add(cu_editor.CuaPlusEdit(self))
        # What does the user appear to want: edit, quit, or something else?
        self.userIntent = "edit"
        if 1:
            self.confirmClose = LabeledLine(
                self.program, self, "Save changes? (yes, no, or cancel): "
            )
            self.confirmClose.set_controller(cu_editor.ConfirmClose)
        if 1:
            self.confirmOverwrite = LabeledLine(
                self.program, self, "Overwrite exiting file? (yes or no): "
            )
            self.confirmOverwrite.set_controller(cu_editor.ConfirmOverwrite)
        self.contextMenu = Menu(self.program, self)
        if 1:  # wip on multi-line interactive find.
            self.interactiveFind = InteractiveFind(self.program, self)
            self.interactiveFind.set_parent(self, 0)
        else:
            self.interactiveFind = LabeledLine(self.program, self, u"find: ")
            self.interactiveFind.set_controller(cu_editor.InteractiveFind)
        if 1:
            self.interactiveGoto = LabeledLine(self.program, self, u"goto: ")
            self.interactiveGoto.set_controller(cu_editor.InteractiveGoto)
        if 1:
            self.interactivePrediction = LabeledLine(
                self.program, self, u"p: ")
            self.interactivePrediction.set_controller(
                cu_editor.InteractivePrediction
            )
        if 1:
            self.interactivePrompt = LabeledLine(self.program, self, u"e: ")
            self.interactivePrompt.set_controller(cu_editor.InteractivePrompt)
        if 1:
            self.interactiveQuit = LabeledLine(
                self.program, self, u"Save changes? (yes, no, or cancel): "
            )
            self.interactiveQuit.set_controller(cu_editor.InteractiveQuit)
        if 1:
            self.topInfo = TopInfo(self.program, self)
            self.topInfo.set_parent(self, 0)
            if not self.showTopInfo:
                self.topInfo.detach()
        if 1:
            self.statusLine = StatusLine(self.program, self)
            self.statusLine.set_parent(self, 0)
            if not self.showFooter:
                self.statusLine.detach()
        if 1:
            self.lineNumberColumn = LineNumbers(self.program, self)
            self.lineNumberColumn.set_parent(self, 0)
            if not self.showLineNumbers:
                self.lineNumberColumn.detach()
        if 1:
            self.logoCorner = ViewWindow(self.program, self)
            self.logoCorner.name = u"Logo"
            self.logoCorner.set_parent(self, 0)
        if 1:
            self.rightColumn = ViewWindow(self.program, self)
            self.rightColumn.name = u"Right"
            self.rightColumn.set_parent(self, 0)
            if not self.showRightColumn:
                self.rightColumn.detach()
        if 1:
            self.popupWindow = PopupWindow(self.program, self)
        if self.showMessageLine:
            self.messageLine = MessageLine(self.program, self)
            self.messageLine.set_parent(self, 0)
        self.showTips = self.program.prefs.status.get(u"showTips")
        self.statusLineCount = 8 if self.showTips else 1

    if 0:

        def split_window(self):
            """Experimental."""
            log.info()
            other = InputWindow(self.prg, self)
            other.set_text_buffer(self.textBuffer)
            log.info()
            self.prg.zOrder.append(other)
            self.prg.layout()
            log.info()

    def layout(self):
        """Change self and sub-windows to fit within the given rectangle."""
        top, left, rows, cols = self.outerShape
        lineNumbersCols = 7
        topRows = self.topRows
        bottomRows = max(1, self.interactiveFind.preferred_size(rows, cols)[0])

        # The top, left of the main window is the rows, cols of the logo corner.
        self.logoCorner.reshape(top, left, 2, lineNumbersCols)

        if self.showTopInfo and rows > topRows and cols > lineNumbersCols:
            self.topInfo.reshape(
                top, left + lineNumbersCols, topRows, cols - lineNumbersCols
            )
            top += topRows
            rows -= topRows
        rows -= bottomRows
        bottomFirstRow = top + rows

        self.confirmClose.reshape(bottomFirstRow, left, bottomRows, cols)
        self.confirmOverwrite.reshape(bottomFirstRow, left, bottomRows, cols)
        self.interactivePrediction.reshape(
            bottomFirstRow, left, bottomRows, cols)
        self.interactivePrompt.reshape(bottomFirstRow, left, bottomRows, cols)
        self.interactiveQuit.reshape(bottomFirstRow, left, bottomRows, cols)
        if self.showMessageLine:
            self.messageLine.reshape(bottomFirstRow, left, bottomRows, cols)
        self.interactiveFind.reshape(bottomFirstRow, left, bottomRows, cols)
        if 1:
            self.interactiveGoto.reshape(
                bottomFirstRow, left, bottomRows, cols)
        if self.showFooter and rows > 0:
            self.statusLine.reshape(
                bottomFirstRow - self.statusLineCount, left, self.statusLineCount, cols
            )
            rows -= self.statusLineCount
        if self.showLineNumbers and cols > lineNumbersCols:
            self.lineNumberColumn.reshape(top, left, rows, lineNumbersCols)
            cols -= lineNumbersCols
            left += lineNumbersCols
        if self.showRightColumn and cols > 0:
            self.rightColumn.reshape(top, left + cols - 1, rows, 1)
            cols -= 1
        Window.reshape(self, top, left, rows, cols)

    def draw_logo_corner(self):
        """."""
        logo = self.logoCorner
        if logo.rows <= 0 or logo.cols <= 0:
            return
        color = self.program.color.get("logo")
        for i in range(logo.rows):
            logo.add_str(i, 0, u" " * logo.cols, color)
        logo.add_str(0, 1, u"ci"[: self.cols], color)
        logo.render()

    def draw_right_edge(self):
        """Draw makers to indicate text extending past the right edge of the
        window."""
        maxRow, maxCol = self.rows, self.cols
        limit = min(maxRow, self.textBuffer.parser.row_count() - self.scrollRow)
        colorPrefs = self.program.color
        for i in range(limit):
            color = colorPrefs.get("right_column")
            if (
                self.textBuffer.parser.row_width(
                    i + self.scrollRow) - self.scrollCol
                > maxCol
            ):
                color = colorPrefs.get("line_overflow")
            self.rightColumn.add_str(i, 0, u" ", color)
        color = colorPrefs.get("outside_document")
        for i in range(limit, maxRow):
            self.rightColumn.add_str(i, 0, u" ", color)

    def focus(self):
        self.layout()
        if self.showMessageLine:
            self.messageLine.bring_to_front()
        Window.focus(self)

    def next_focusable_window(self, start, reverse=False):
        # Keep the tab focus in the child branch. (The child view will call
        # this, tell the child there is nothing to tab to up here).
        return None

    def render(self):
        self.topInfo.on_change()
        self.draw_logo_corner()
        self.draw_right_edge()
        Window.render(self)

    def reshape(self, top, left, rows, cols):
        """Change self and sub-windows to fit within the given rectangle."""
        log.detail(top, left, rows, cols)
        Window.reshape(self, top, left, rows, cols)
        self.outerShape = (top, left, rows, cols)
        self.layout()

    def set_text_buffer(self, textBuffer):
        if config.strict_debug:
            assert issubclass(textBuffer.__class__, text_buffer.TextBuffer), repr(
                textBuffer
            )
        log.info("set_text_buffer")
        if self.textBuffer is not None:
            self.savedScrollPositions[self.textBuffer.fullPath] = (
                self.scrollRow,
                self.scrollCol,
            )
        # self.normalize()
        textBuffer.lineLimitIndicator = self.program.prefs.editor["lineLimitIndicator"]
        textBuffer.debugRedo = self.program.prefs.startup.get("debugRedo")
        Window.set_text_buffer(self, textBuffer)
        self.controller.set_text_buffer(textBuffer)
        savedScroll = self.savedScrollPositions.get(self.textBuffer.fullPath)
        if savedScroll is not None:
            self.scrollRow, self.scrollCol = savedScroll
        else:
            historyScroll = self.textBuffer.fileHistory.get("scroll")
            if historyScroll is not None:
                self.scrollRow, self.scrollCol = historyScroll
            else:
                self.textBuffer.scroll_to_optimal_scroll_position()

    def startup(self):
        bufferManager = self.program.bufferManager
        for f in self.program.prefs.startup.get("cliFiles", []):
            tb = bufferManager.load_text_buffer(f["path"])
            if tb is None:
                # log.info('failed to load', repr(f["path"]))
                continue
            tb.parse_document()
            if f["row"] is not None:
                if f["col"] is not None:
                    tb.select_text(f["row"], f["col"], 0,
                                   selectable.kSelectionNone)
                else:
                    tb.select_text(f["row"], 0, 0, selectable.kSelectionNone)
        if self.program.prefs.startup.get("read_stdin"):
            bufferManager.read_stdin()
        bufferManager.buffers.reverse()
        tb = bufferManager.top_buffer()
        if not tb:
            tb = bufferManager.new_text_buffer()
        self.set_text_buffer(tb)
        # Should parsing the document be a standard part of set_text_buffer? TBD.
        self.textBuffer.parse_document()
        openToLine = self.program.prefs.startup.get("openToLine")
        if openToLine is not None:
            self.textBuffer.select_text(
                openToLine - 1, 0, 0, selectable.kSelectionNone
            )

    def toggle_show_tips(self):
        self.showTips = not self.showTips
        self.statusLineCount = 8 if self.showTips else 1
        self.layout()
        self.program.prefs.save("status", "showTips", self.showTips)

    def unfocus(self):
        if self.showMessageLine:
            self.messageLine.detach()
        Window.unfocus(self)


class OptionsSelectionWindow(ViewWindow):
    """Mutex window."""

    def __init__(self, program, parent):
        if config.strict_debug:
            assert parent is not None
        ViewWindow.__init__(self, program, parent)
        self.color = self.program.color.get("top_info")

    def reshape(self, top, left, rows, cols):
        ViewWindow.reshape(self, top, left, rows, cols)
        self.layout_horizontally(self.zOrder)

    def child_selected(self, selectedChild):
        log.info(self.zOrder)
        for child in self.zOrder:
            if child is not selectedChild:
                child.deselect()

    def render(self):
        self.blank(self.color)
        ViewWindow.render(self)


class OptionsTrinaryStateWindow(Window):
    def __init__(self, program, parent, label, prefCategory, prefName):
        if config.strict_debug:
            assert isinstance(label, unicode)
            assert isinstance(prefCategory, unicode)
            assert isinstance(prefName, unicode)
        Window.__init__(self, program, parent)
        # TODO(dschuyler): Creating a text buffer is rather heavy for a toggle
        # control. This should get some optimization.
        self.set_text_buffer(text_buffer.TextBuffer(self.program))
        self.set_controller(cu_editor.ToggleController)
        self.set_parent(parent)
        self.name = label
        self.prefCategory = prefCategory
        self.prefName = prefName
        colorPrefs = self.program.color
        self.color = colorPrefs.get("keyword")
        self.focusColor = colorPrefs.get("selected")
        self.textBuffer.view.showCursor = False

    def focus(self):
        Window.focus(self)

    def set_up(self, toggleOn, toggleOff, toggleUndefined, width=None):
        if config.strict_debug:
            assert isinstance(toggleOn, unicode)
            assert isinstance(toggleOff, unicode)
            assert isinstance(toggleUndefined, unicode)
            assert width is None or isinstance(width, int)
        self.toggleOn = toggleOn
        self.toggleOff = toggleOff
        self.toggleUndefined = toggleUndefined
        longest = max(len(toggleOn), len(toggleOff), len(toggleUndefined))
        self.width = width if width is not None else longest
        self.update_label()

    def mouse_click(self, paneRow, paneCol, shift, ctrl, alt):
        self.controller.toggle_value()

    def on_pref_changed(self, category, name):
        Window.on_pref_changed(self, category, name)
        if category != self.prefCategory or name != self.prefName:
            return
        self.update_label()

    def update_label(self):
        pref = self.program.prefs.category(self.prefCategory)[self.prefName]
        if pref is None:
            label = self.toggleUndefined
        else:
            label = self.toggleOn if pref else self.toggleOff
        self.label = u"%*s" % (self.width, label)

    def preferred_size(self, rowLimit, colLimit):
        return min(rowLimit, 1), min(colLimit, abs(self.width))

    def render(self):
        Window.render(self)
        if self.rows <= 0:
            return
        self.writeLineRow = 0
        color = self.focusColor if self.hasFocus else self.color
        self.write_line(self.label[: self.cols], color)


class OptionsToggle(OptionsTrinaryStateWindow):
    def __init__(self, program, parent, label, prefCategory, prefName, width=None):
        if config.strict_debug:
            assert isinstance(label, unicode)
            assert isinstance(prefCategory, unicode)
            assert isinstance(prefName, unicode)
        OptionsTrinaryStateWindow.__init__(
            self, program, parent, label, prefCategory, prefName
        )
        # I considered these unicode characters, but [x] looks clearer to me.
        # toggleOn = unichr(0x2612) + ' ' + control['name']
        # toggleOff = unichr(0x2610) + ' ' + control['name']
        OptionsTrinaryStateWindow.set_up(
            self, u"[x]" + label, u"[ ]" + label, u"[-]" + label, width
        )


class RowWindow(ViewWindow):
    def __init__(self, program, host, separator):
        if config.strict_debug:
            assert host
        ViewWindow.__init__(self, program, host)
        self.color = self.program.color.get("keyword")
        self.separator = separator

    def preferred_size(self, rowLimit, colLimit):
        return min(rowLimit, 1), colLimit

    def render(self):
        self.blank(self.color)
        ViewWindow.render(self)

    def reshape(self, top, left, rows, cols):
        ViewWindow.reshape(self, top, left, rows, cols)
        # log.info(top, left, rows, cols, self)
        self.layout_horizontally(self.zOrder, self.separator)


class OptionsRow(ViewWindow):
    class ControlElement:
        def __init__(self, elementType, name, reference, width=None, sep=" "):
            self.type = elementType
            self.name = name
            self.reference = reference
            self.width = width if width is not None else len(name)
            self.sep = sep

    def __init__(self, program, host):
        if config.strict_debug:
            assert host
        ViewWindow.__init__(self, program, host)
        self.host = host
        self.color = self.program.color.get("top_info")
        self.controlList = []
        self.group = None

    def add_element(self, draw, kind, name, reference, width, sep, extraWidth=0):
        if config.strict_debug:
            assert isinstance(name, unicode)
            assert isinstance(sep, unicode)
            assert width is None or isinstance(width, int)
            assert isinstance(extraWidth, int)
            if reference is not None:
                assert isinstance(reference, dict)
                assert name in reference
        if self.group is not None:
            self.group.append(len(self.controlList))
        element = {
            "dict": reference,
            "draw": draw,
            "name": name,
            "sep": sep,
            "type": kind,
            "width": width if width is not None else len(name) + extraWidth,
        }
        self.controlList.append(element)
        return element

    def add_label(self, name, width=None, sep=u" "):
        def draw(control):
            return control[u"name"]

        return self.add_element(draw, u"label", name, None, width, sep)

    def add_sort_header(self, name, reference, width=None, sep=u" |"):
        def draw(control):
            decoration = u"v" if control[u"dict"][control[u"name"]] else u"^"
            if control[u"dict"][control[u"name"]] is None:
                decoration = u"-"
            if control[u"width"] < 0:
                return u"%s %s" % (control[u"name"], decoration)
            return u"%s %s" % (decoration, control[u"name"])

        self.add_element(draw, u"sort", name, reference,
                         width, sep, len(u" v"))

    def add_selection(self, name, reference, width=None, sep=u"  "):
        if config.strict_debug:
            assert isinstance(name, unicode)
        if 1:
            toggleOn = u"(*)" + name
            toggleOff = u"( )" + name

        def draw(control):
            return toggleOn if control[u"dict"][control[u"name"]] else toggleOff

        width = max(width, min(len(toggleOn), len(toggleOff)))
        self.add_element(draw, u"selection", name,
                         reference, width, sep, len(u"(*)"))

    def remove_this_add_toggle(self, name, reference, width=None, sep=u"  "):
        if config.strict_debug:
            assert isinstance(name, unicode)
        if 1:
            toggleOn = u"[x]" + name
            toggleOff = u"[ ]" + name
        if 0:
            toggleOn = unichr(0x2612) + " " + control["name"]
            toggleOff = unichr(0x2610) + " " + control["name"]
        if 0:
            toggleOn = "[+" + control["name"] + "]"
            toggleOff = "[-" + control["name"] + "]"

        def draw(control):
            return toggleOn if control["dict"][control["name"]] else toggleOff

        width = max(width, min(len(toggleOn), len(toggleOff)))
        self.add_element(draw, u"toggle", name, reference,
                         width, sep, len("[-]"))

    def begin_group(self):
        """Like a radio group, or column sort headers."""
        self.group = []

    def end_group(self):
        """Like a radio group, or column sort headers."""
        pass

    def mouse_click(self, paneRow, paneCol, shift, ctrl, alt):
        # row = self.scrollRow + paneRow
        col = self.scrollCol + paneCol
        offset = 0
        for index, control in enumerate(self.controlList):
            width = abs(control["width"])
            if offset <= col < offset + width:
                if control["type"] == "selection":
                    name = control["name"]
                    for element in self.group:
                        elementName = self.controlList[element]["name"]
                        self.controlList[element]["dict"][elementName] = False
                    control["dict"][name] = True
                    self.host.controller.option_changed(
                        name, control["dict"][name])
                    break
                if control["type"] == "sort":
                    name = control["name"]
                    newValue = not control["dict"][name]
                    if index in self.group:
                        for element in self.group:
                            elementName = self.controlList[element]["name"]
                            self.controlList[element]["dict"][elementName] = None
                    control["dict"][name] = newValue
                    self.host.controller.option_changed(
                        name, control["dict"][name])
                    break
                if control["type"] == "toggle":
                    name = control["name"]
                    control["dict"][name] = not control["dict"][name]
                    self.host.controller.option_changed(
                        name, control["dict"][name])
                    break
            offset += width + len(control["sep"])

    def preferred_size(self, rowLimit, colLimit):
        return min(rowLimit, 1), colLimit

    def render(self):
        if self.rows <= 0:
            return
        line = u""
        for control in self.controlList:
            label = control["draw"](control)
            line += u"%*s%s" % (control["width"], label, control["sep"])
            if len(line) >= self.cols:
                break
        self.writeLineRow = 0
        self.write_line(line[: self.cols], self.color)


class PopupWindow(Window):
    def __init__(self, program, host):
        if config.strict_debug:
            assert host
        Window.__init__(self, program, host)
        self.host = host
        self.controller = cu_editor.PopupController(self)
        self.set_text_buffer(text_buffer.TextBuffer(self.program))
        self.longestLineLength = 0
        self.__message = []
        self.showOptions = True
        # This will be displayed and should contain the keys that respond to
        # user input. This should be updated if you change the controller's
        # command set.
        self.options = []

    def render(self):
        """Display a box of text in the center of the window."""
        maxRows, maxCols = self.host.rows, self.host.cols
        cols = min(self.longestLineLength + 6, maxCols)
        rows = min(len(self.__message) + 4, maxRows)
        self.resize_to(rows, cols)
        self.move_to(maxRows // 2 - rows // 2, maxCols // 2 - cols // 2)
        color = self.program.color.get("popup_window")
        for row in range(rows):
            if row == rows - 2 and self.showOptions:
                message = "/".join(self.options)
            elif row == 0 or row >= rows - 3:
                self.add_str(row, 0, " " * cols, color)
                continue
            else:
                message = self.__message[row - 1]
            lineLength = len(message)
            spacing1 = (cols - lineLength) // 2
            spacing2 = cols - lineLength - spacing1
            self.add_str(row, 0, " " * spacing1 +
                         message + " " * spacing2, color)

    def set_message(self, message):
        """Sets the Popup window's message to the given message.

        message (str): A string that you want to display.

        Returns:
          None.
        """
        self.__message = message.split("\n")
        self.longestLineLength = max([len(line) for line in self.__message])

    def set_options_to_display(self, options):
        """
        This function is used to change the options that are displayed in the
        popup window. They will be separated by a '/' character when displayed.

        Args:
          options (list): A list of possible keys which the user can press and
                          should be responded to by the controller.
        """
        self.options = options

    def set_text_buffer(self, textBuffer):
        Window.set_text_buffer(self, textBuffer)
        self.controller.set_text_buffer(textBuffer)

    def unfocus(self):
        self.detach()
        Window.unfocus(self)


class PaletteWindow(Window):
    """A window with example foreground and background text colors."""

    def __init__(self, prg, host):
        Window.__init__(self, prg, host)
        self.prg = prg
        self.resize_to(16, 16 * 5)
        self.move_to(8, 8)
        self.controller = cu_editor.PaletteDialogController(self)
        self.set_text_buffer(text_buffer.TextBuffer(self.program))

    def render(self):
        width = 16
        rows = 16
        colorPrefs = self.program.color
        for i in range(width):
            for k in range(rows):
                self.add_str(
                    k, i * 5, " %3d " % (i + k * width,
                                         ), colorPrefs.get(i + k * width)
                )

    def set_text_buffer(self, textBuffer):
        Window.set_text_buffer(self, textBuffer)
        self.controller.set_text_buffer(textBuffer)

    def unfocus(self):
        self.detach()
        Window.unfocus(self)


class SortableHeaderWindow(OptionsTrinaryStateWindow):
    def __init__(self, program, parent, label, prefCategory, prefName, width=None):
        if config.strict_debug:
            assert issubclass(program.__class__, ci_program.CiProgram), program
            assert isinstance(label, unicode)
            assert isinstance(prefCategory, unicode)
            assert isinstance(prefName, unicode)
        OptionsTrinaryStateWindow.__init__(
            self, program, parent, label, prefCategory, prefName
        )
        self.color = self.program.color.get(u"top_info")

        def draw(label, decoration, width):
            if width < 0:
                x = u"%s %s" % (label, decoration)
            else:
                x = u"%s %s" % (decoration, label)
            return u"%*s" % (width, x)

        OptionsTrinaryStateWindow.set_up(
            self,
            draw(label, u"v", width),
            draw(label, u"^", width),
            draw(label, u"-", width),
        )

    def deselect(self):
        self.controller.clear_value()

    def mouse_click(self, paneRow, paneCol, shift, ctrl, alt):
        self.parent.child_selected(self)
        self.controller.toggle_value()
