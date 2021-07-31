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

from . import config
from . import cu_editor
from . import log
from . import text_buffer
from . import window


class PredictionList(window.Window):
    """This <tbd>."""

    def __init__(self, program, host):
        if config.strict_debug:
            assert host
            assert self is not host
        window.Window.__init__(self, program, host)
        self.host = host
        self.isFocusable = False
        self.controller = cu_editor.PredictionList(self)
        self.set_text_buffer(text_buffer.TextBuffer(self.program))
        # Set up table headers.
        color = host.program.color.get(u"top_info")
        self.optionsRow = window.OptionsSelectionWindow(self.program, self)
        self.optionsRow.set_parent(self)
        self.typeColumn = window.SortableHeaderWindow(
            self.program,
            self.optionsRow,
            u"Type",
            u"editor",
            u"predictionSortAscendingByType",
            8,
        )
        label = window.LabelWindow(self.program, self.optionsRow, u"|")
        label.set_parent(self.optionsRow)
        label.color = color
        self.nameColumn = window.SortableHeaderWindow(
            self.program,
            self.optionsRow,
            u"Name",
            u"editor",
            u"predictionSortAscendingByName",
            -61,
        )
        label = window.LabelWindow(self.program, self.optionsRow, u"|")
        label.set_parent(self.optionsRow)
        label.color = color
        self.statusColumn = window.SortableHeaderWindow(
            self.program,
            self.optionsRow,
            u"Status ",
            u"editor",
            u"predictionSortAscendingByStatus",
            -7,
        )
        label = window.LabelWindow(self.program, self.optionsRow, u"|")
        label.set_parent(self.optionsRow)
        label.color = color

    def highlight_line(self, row):
        self.textBuffer.penRow = min(
            row, self.textBuffer.parser.row_count() - 1)
        self.textBuffer.penCol = 0
        log.info(self.textBuffer.penRow)

    def mouse_click(self, paneRow, paneCol, shift, ctrl, alt):
        self.highlight_line(self.scrollRow + paneRow)
        row = self.scrollRow + paneRow
        if row >= self.textBuffer.parser.row_count():
            return
        self.controller.open_file_or_dir(row)

    def mouse_double_click(self, paneRow, paneCol, shift, ctrl, alt):
        log.info()
        assert False

    # def mouse_moved(self, paneRow, paneCol, shift, ctrl, alt):
    #  log.info()

    # def mouse_release(self, paneRow, paneCol, shift, ctrl, alt):
    #  log.info()

    # def mouse_triple_click(self, paneRow, paneCol, shift, ctrl, alt):
    #  log.info()

    def mouse_wheel_down(self, shift, ctrl, alt):
        self.textBuffer.mouse_wheel_down(shift, ctrl, alt)

    def mouse_wheel_up(self, shift, ctrl, alt):
        self.textBuffer.mouse_wheel_up(shift, ctrl, alt)

    def update(self, items):
        # Filter the list. (The filter function is not used so as to edit the
        # list in place).
        appPrefs = self.program.prefs
        showOpen = appPrefs.editor[u"predictionShowOpenFiles"]
        showAlternate = appPrefs.editor[u"predictionShowAlternateFiles"]
        showRecent = appPrefs.editor[u"predictionShowRecentFiles"]
        if not (showOpen and showAlternate and showRecent):
            i = 0
            while i < len(items):
                if not showOpen and items[i][3] == u"open":
                    items.pop(i)
                elif not showAlternate and items[i][3] == u"alt":
                    items.pop(i)
                elif not showRecent and items[i][3] == u"recent":
                    items.pop(i)
                else:
                    i += 1
        # Sort the list
        sortByPrediction = appPrefs.editor[u"predictionSortAscendingByPrediction"]
        sortByType = appPrefs.editor[u"predictionSortAscendingByType"]
        sortByName = appPrefs.editor[u"predictionSortAscendingByName"]
        sortByStatus = appPrefs.editor[u"predictionSortAscendingByStatus"]
        if sortByPrediction is not None:
            items.sort(reverse=not sortByPrediction, key=lambda x: x[4])
        elif sortByType is not None:
            items.sort(reverse=not sortByType, key=lambda x: x[3])
        elif sortByStatus is not None:
            items.sort(reverse=not sortByStatus, key=lambda x: x[2])
        elif sortByName is not None:
            items.sort(reverse=not sortByName, key=lambda x: x[1])
        # Write the lines to the text buffer.

        def fit_path_to_width(path, width):
            if len(path) < width:
                return path
            return path[-width:]

        if len(items) == 0:
            self.textBuffer.replace_lines((u"",))
        else:
            self.textBuffer.replace_lines(
                tuple(
                    [
                        u"%*s %*s %.*s"
                        % (
                            self.typeColumn.cols,
                            i[3],
                            -self.nameColumn.cols,
                            fit_path_to_width(i[1], self.nameColumn.cols),
                            self.statusColumn.cols,
                            i[2],
                        )
                        for i in items
                    ]
                )
            )
        self.textBuffer.parse_screen_maybe()  # TODO(dschuyler): Add test.
        self.textBuffer.cursor_move_to_begin()

    def on_pref_changed(self, category, name):
        self.controller.option_changed(category, name)
        window.Window.on_pref_changed(self, category, name)

    def reshape(self, top, left, rows, cols):
        """Change self and sub-windows to fit within the given rectangle."""
        log.detail(u"reshape", top, left, rows, cols)
        self.optionsRow.reshape(top, left, 1, cols)
        top += 1
        rows -= 1
        window.Window.reshape(self, top, left, rows, cols)

    def set_text_buffer(self, textBuffer):
        if config.strict_debug:
            assert textBuffer is not self.host.textBuffer
        textBuffer.lineLimitIndicator = 0
        textBuffer.highlightCursorLine = True
        textBuffer.highlightTrailingWhitespace = False
        window.Window.set_text_buffer(self, textBuffer)
        self.controller.set_text_buffer(textBuffer)


class PredictionInputWindow(window.Window):
    def __init__(self, program, host):
        if config.strict_debug:
            assert host
            assert issubclass(host.__class__, window.ActiveWindow), host
        window.Window.__init__(self, program, host)
        self.host = host
        self.controller = cu_editor.PredictionInputController(self)
        self.set_text_buffer(text_buffer.TextBuffer(self.program))

    def get_path(self):
        return self.textBuffer.parser.row_text(0)

    def set_path(self, path):
        self.textBuffer.replace_lines((path,))

    def set_text_buffer(self, textBuffer):
        textBuffer.lineLimitIndicator = 0
        textBuffer.highlightTrailingWhitespace = False
        window.Window.set_text_buffer(self, textBuffer)
        self.controller.set_text_buffer(textBuffer)


class PredictionWindow(window.Window):
    def __init__(self, program, host):
        window.Window.__init__(self, program, host)

        self.showTips = False
        self.controller = cu_editor.PredictionController(self)
        self.set_text_buffer(text_buffer.TextBuffer(self.program))

        self.titleRow = window.OptionsRow(self.program, self)
        self.titleRow.add_label(u" ci   ")
        self.titleRow.set_parent(self)

        self.predictionInputWindow = PredictionInputWindow(self.program, self)
        self.predictionInputWindow.set_parent(self)

        self.predictionList = PredictionList(self.program, self)
        self.predictionList.set_parent(self)

        if 1:
            self.optionsRow = window.RowWindow(self.program, self, 2)
            self.optionsRow.set_parent(self)
            colorPrefs = host.program.color
            self.optionsRow.color = colorPrefs.get(u"top_info")
            label = window.LabelWindow(
                self.program, self.optionsRow, u"Show:")
            label.color = colorPrefs.get(u"top_info")
            label.set_parent(self.optionsRow)
            toggle = window.OptionsToggle(
                self.program,
                self.optionsRow,
                u"open",
                u"editor",
                u"predictionShowOpenFiles",
            )
            toggle.color = colorPrefs.get(u"top_info")
            toggle = window.OptionsToggle(
                self.program,
                self.optionsRow,
                u"alternates",
                u"editor",
                u"predictionShowAlternateFiles",
            )
            toggle.color = colorPrefs.get(u"top_info")
            toggle = window.OptionsToggle(
                self.program,
                self.optionsRow,
                u"recent",
                u"editor",
                u"predictionShowRecentFiles",
            )
            toggle.color = colorPrefs.get(u"top_info")

        self.messageLine = window.LabelWindow(self.program, self, u"")
        self.messageLine.set_parent(self)

    def bring_child_to_front(self, child):
        # The PredictionWindow window doesn't reorder children.
        pass

    def focus(self):
        self.reattach()
        self.parent.layout()
        window.Window.focus(self)
        self.change_focus_to(self.predictionInputWindow)

    def get_path(self):
        return self.predictionInputWindow.get_path()

    def on_pref_changed(self, category, name):
        self.predictionList.controller.option_changed(category, name)
        window.Window.on_pref_changed(self, category, name)

    def reshape(self, top, left, rows, cols):
        """Change self and sub-windows to fit within the given rectangle."""
        window.Window.reshape(self, top, left, rows, cols)
        self.titleRow.reshape(top, left, 1, cols)
        top += 1
        rows -= 1
        self.predictionInputWindow.reshape(top, left, 1, cols)
        top += 1
        rows -= 1
        self.messageLine.reshape(top + rows - 1, left, 1, cols)
        rows -= 1
        self.optionsRow.reshape(top + rows - 1, left, 1, cols)
        rows -= 1
        self.predictionList.reshape(top, left, rows, cols)

    def set_path(self, path):
        self.predictionInputWindow.set_path(path)

    def unfocus(self):
        window.Window.unfocus(self)
        self.detach()
