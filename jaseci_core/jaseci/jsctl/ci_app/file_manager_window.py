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

import os

from . import config
from . import cu_editor
from . import log
from . import string
from . import text_buffer
from . import window


# todo remove or use this.
class PathRow(window.ViewWindow):
    def __init__(self, program, host):
        if config.strict_debug:
            assert host
        window.ViewWindow.__init__(self, program, host)
        self.host = host
        self.path = u""

    def mouse_click(self, paneRow, paneCol, shift, ctrl, alt):
        col = self.scrollCol + paneCol
        line = self.path
        col = self.scrollCol + paneCol
        self.host.controller.shownDirectory = None
        if col >= len(line):
            return
        slash = line[col:].find(u"/")
        self.path = line[: col + slash + 1]

    def render(self):
        color = self.program.color.get(u"message_line")
        self.writeLineRow = 0
        self.write_line(self.path, color)


class DirectoryList(window.Window):
    """This <tbd>."""

    def __init__(self, program, host, inputWindow):
        if config.strict_debug:
            assert host
            assert self is not host
        window.Window.__init__(self, program, host)
        self.host = host
        self.inputWindow = inputWindow
        self.controller = cu_editor.DirectoryList(self)
        self.set_text_buffer(text_buffer.TextBuffer(self.program))

    def color_pref(self, colorType, delta=0):
        if colorType == u"current_line":
            return self.program.color.get("selected", delta)
        return self.program.color.get(colorType, delta)

    def mouse_click(self, paneRow, paneCol, shift, ctrl, alt):
        row = self.scrollRow + paneRow
        if row >= self.textBuffer.parser.row_count():
            return
        self.controller.open_file_or_dir(row)

    def mouse_double_click(self, paneRow, paneCol, shift, ctrl, alt):
        self.change_focus_to(self.host)

    def mouse_moved(self, paneRow, paneCol, shift, ctrl, alt):
        self.change_focus_to(self.host)

    def mouse_release(self, paneRow, paneCol, shift, ctrl, alt):
        self.change_focus_to(self.host)

    def mouse_triple_click(self, paneRow, paneCol, shift, ctrl, alt):
        self.change_focus_to(self.host)

    def mouse_wheel_down(self, shift, ctrl, alt):
        self.textBuffer.mouse_wheel_down(shift, ctrl, alt)
        self.change_focus_to(self.host)

    def mouse_wheel_up(self, shift, ctrl, alt):
        self.textBuffer.mouse_wheel_up(shift, ctrl, alt)
        self.change_focus_to(self.host)

    def on_pref_changed(self, category, name):
        self.controller.option_changed(category, name)
        window.Window.on_pref_changed(self, category, name)

    def set_text_buffer(self, textBuffer):
        if config.strict_debug:
            assert textBuffer is not self.host.textBuffer
        textBuffer.lineLimitIndicator = 0
        textBuffer.highlightCursorLine = True
        textBuffer.highlightTrailingWhitespace = False
        window.Window.set_text_buffer(self, textBuffer)
        textBuffer.view.showCursor = False
        self.controller.set_text_buffer(textBuffer)


class PathWindow(window.Window):
    """The path window is the editable text line where the user may freely type
    in a path.
    """

    def __init__(self, program, host):
        if config.strict_debug:
            assert host
            assert issubclass(host.__class__, window.ActiveWindow), host
        window.Window.__init__(self, program, host)
        self.host = host
        self.controller = cu_editor.FilePathInput(self)
        self.set_text_buffer(text_buffer.TextBuffer(self.program))

    def mouse_click(self, paneRow, paneCol, shift, ctrl, alt):
        col = self.scrollCol + paneCol
        line = self.controller.decoded_path()
        col = self.scrollCol + paneCol
        self.parent.directoryList.controller.shownDirectory = None
        if col >= len(line):
            return
        slash = line[col:].find(u"/")
        self.controller.set_encoded_path(line[: col + slash + 1])

    def set_text_buffer(self, textBuffer):
        textBuffer.lineLimitIndicator = 0
        textBuffer.highlightTrailingWhitespace = False
        window.Window.set_text_buffer(self, textBuffer)
        self.controller.set_text_buffer(textBuffer)


class FileManagerWindow(window.Window):
    def __init__(self, program, host, inputWindow):
        window.Window.__init__(self, program, host)
        self.inputWindow = inputWindow
        self.inputWindow.fileManagerWindow = self

        self.mode = u"open"
        self.showTips = False
        self.controller = cu_editor.FileOpener(self)
        self.set_text_buffer(text_buffer.TextBuffer(self.program))

        self.titleRow = window.OptionsRow(self.program, self)
        self.titleRow.add_label(u" ci   ")
        self.modeTitle = self.titleRow.add_label(u"x")
        self.set_mode(u"open")
        self.titleRow.set_parent(self)

        self.pathWindow = PathWindow(self.program, self)
        self.pathWindow.set_parent(self)

        # Set up table headers.
        color = self.program.color.get(u"top_info")
        self.tableHeaders = window.OptionsSelectionWindow(
            self.program, self)
        self.tableHeaders.set_parent(self)
        window.SortableHeaderWindow(
            self.program,
            self.tableHeaders,
            u"Name",
            u"editor",
            u"filesSortAscendingByName",
            -41,
        )
        label = window.LabelWindow(self.program, self.tableHeaders, u"|")
        label.set_parent(self.tableHeaders)
        label.color = color
        window.SortableHeaderWindow(
            self.program,
            self.tableHeaders,
            u"Size ",
            u"editor",
            u"filesSortAscendingBySize",
            16,
        )
        label = window.LabelWindow(self.program, self.tableHeaders, u"|")
        label.set_parent(self.tableHeaders)
        label.color = color
        window.SortableHeaderWindow(
            self.program,
            self.tableHeaders,
            u"Modified ",
            u"editor",
            u"filesSortAscendingByModifiedDate",
            25,
        )
        label = window.LabelWindow(self.program, self.tableHeaders, u"|")
        label.set_parent(self.tableHeaders)
        label.color = color

        self.directoryList = DirectoryList(self.program, self, inputWindow)
        self.directoryList.set_parent(self)

        if 1:
            self.optionsRow = window.RowWindow(self.program, self, 2)
            self.optionsRow.set_parent(self)
            colorPrefs = self.program.color
            self.optionsRow.color = colorPrefs.get(u"top_info")
            label = window.LabelWindow(
                self.program, self.optionsRow, u"Show:")
            label.color = colorPrefs.get(u"top_info")
            label.set_parent(self.optionsRow)
            toggle = window.OptionsToggle(
                self.program,
                self.optionsRow,
                u"dotFiles",
                u"editor",
                u"filesShowDotFiles",
            )
            toggle.color = colorPrefs.get(u"top_info")
            toggle = window.OptionsToggle(
                self.program, self.optionsRow, u"sizes", u"editor", u"filesShowSizes"
            )
            toggle.color = colorPrefs.get(u"top_info")
            toggle = window.OptionsToggle(
                self.program,
                self.optionsRow,
                u"modified",
                u"editor",
                u"filesShowModifiedDates",
            )
            toggle.color = colorPrefs.get(u"top_info")

        self.messageLine = window.LabelWindow(self.program, self, u"")
        self.messageLine.set_parent(self)

    def bring_child_to_front(self, child):
        # The FileManagerWindow window doesn't reorder children.
        pass

    def focus(self):
        self.reattach()
        self.parent.layout()
        self.controller.focus()
        # Set the initial path each time the window is focused.
        if not self.pathWindow.controller.decoded_path():
            inputWindow = self.parent.inputWindow
            if len(inputWindow.textBuffer.fullPath) == 0:
                path = os.getcwd()
            else:
                path = os.path.dirname(inputWindow.textBuffer.fullPath)
            if len(path) != 0:
                path += os.path.sep
            self.pathWindow.controller.set_encoded_path(unicode(path))
        self.change_focus_to(self.pathWindow)

    def on_pref_changed(self, category, name):
        self.directoryList.controller.option_changed(category, name)
        window.Window.on_pref_changed(self, category, name)

    def next_focusable_window(self, start, reverse=False):
        # Keep the tab focus in the children. This is a top-level window, don't
        # tab out of it.
        return self._child_focusable_window(reverse)

    def reshape(self, top, left, rows, cols):
        """Change self and sub-windows to fit within the given rectangle."""
        log.detail(u"reshape", top, left, rows, cols)
        window.Window.reshape(self, top, left, rows, cols)
        self.titleRow.reshape(top, left, 1, cols)
        top += 1
        rows -= 1
        self.pathWindow.reshape(top, left, 1, cols)
        top += 1
        rows -= 1
        self.tableHeaders.reshape(top, left, 1, cols)
        top += 1
        rows -= 1
        self.messageLine.reshape(top + rows - 1, left, 1, cols)
        rows -= 1
        self.optionsRow.reshape(top + rows - 1, left, 1, cols)
        rows -= 1
        self.directoryList.reshape(top, left, rows, cols)

    def set_mode(self, mode):
        self.mode = mode
        modeTitles = {
            u"open": u"Open File",
            u"saveAs": u"Save File As",
            u"selectDir": u"Select a Directory",
        }
        self.modeTitle[u"name"] = modeTitles[mode]

    def unfocus(self):
        # Clear the path.
        self.pathWindow.controller.set_encoded_path(u"")
        window.Window.unfocus(self)
        self.detach()
