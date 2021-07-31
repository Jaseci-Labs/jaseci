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
"""Interactive UIs for the ciEditor."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    unicode
except NameError:
    unicode = str
    unichr = chr

import os
import re

from . import config, log, window
from . import controller
from . import text_buffer


def parse_int(inStr):
    if config.strict_debug:
        assert isinstance(inStr, unicode), type(inStr)
    i = 0
    k = 0
    if len(inStr) > i and inStr[i] in ("+", "-"):
        i += 1
    k = i
    while len(inStr) > k and inStr[k].isdigit():
        k += 1
    if k > i:
        return int(inStr[:k])
    return 0


def test_parse_int():
    assert parse_int("0") == 0
    assert parse_int("0e") == 0
    assert parse_int("text") == 0
    assert parse_int("10") == 10
    assert parse_int("+10") == 10
    assert parse_int("-10") == -10
    assert parse_int("--10") == 0
    assert parse_int("--10") == 0


class InteractivePrediction(controller.Controller):
    """Make a guess about what the user desires."""

    def __init__(self, view):
        if config.strict_debug:
            assert issubclass(self.__class__, InteractivePrediction), self
            assert issubclass(view.__class__, window.ViewWindow), view
        controller.Controller.__init__(self, view, u"prediction")

    def cancel(self):
        self.items = [
            (self.priorTextBuffer, self.priorTextBuffer.fullPath, "")]
        self.index = 0
        self.change_to_host_window()

    def cursor_move_to(self, row, col):
        if config.strict_debug:
            assert isinstance(row, int)
            assert isinstance(col, int)
        textBuffer = self.view.host.textBuffer
        textBuffer.cursor_move_to(row, col)
        textBuffer.cursor_scroll_to_middle()
        textBuffer.redo()

    def focus(self):
        log.info("InteractivePrediction.focus")
        controller.Controller.focus(self)
        self.priorTextBuffer = self.view.host.textBuffer
        self.index = self.build_file_list(self.view.host.textBuffer.fullPath)
        self.view.host.set_text_buffer(text_buffer.TextBuffer())
        self.commandDefault = self.view.textBuffer.insert_printable
        self.view.host.textBuffer.lineLimitIndicator = 0
        self.view.host.textBuffer.rootGrammar = self.view.program.prefs.get_grammar(
            "_pre"
        )

    def info(self):
        log.info("InteractivePrediction command set")

    def build_file_list(self, currentFile):
        if config.strict_debug:
            assert isinstance(currentFile, str)
        self.items = []
        bufferManager = self.view.program.bufferManager
        for i in bufferManager.buffers:
            dirty = "*" if i.is_dirty() else "."
            if i.fullPath:
                self.items.append((i, i.fullPath, dirty))
            else:
                self.items.append(
                    (i, "<new file> %s" % (i.parser.row_text(0)[:20]), dirty)
                )
        dirPath, fileName = os.path.split(currentFile)
        fileName, ext = os.path.splitext(fileName)
        # TODO(dschuyler): rework this ignore list.
        ignoreExt = set(
            (
                ".pyc",
                ".pyo",
                ".o",
                ".obj",
                ".tgz",
                ".zip",
                ".tar",
            )
        )
        try:
            contents = os.listdir(
                os.path.expandvars(os.path.expanduser(dirPath)) or "."
            )
        except OSError:
            contents = []
        contents.sort()
        for i in contents:
            f, e = os.path.splitext(i)
            if fileName == f and ext != e and e not in ignoreExt:
                self.items.append((None, os.path.join(dirPath, i), "="))
        if 1:
            log.info()
            # Chromium specific hack.
            if currentFile.endswith("-extracted.js"):
                chromiumPath = currentFile[: -len("-extracted.js")] + ".html"
                log.info(chromiumPath)
                if os.path.isfile(chromiumPath):
                    log.info()
                    self.items.append((None, chromiumPath, "="))
            elif currentFile.endswith(".html"):
                log.info()
                chromiumPath = currentFile[: -len(".html")] + "-extracted.js"
                if os.path.isfile(chromiumPath):
                    log.info()
                    self.items.append((None, chromiumPath, "="))
        # Suggest item.
        return (len(bufferManager.buffers) - 2) % len(self.items)

    def on_change(self):
        assert False
        clip = []
        limit = max(5, self.view.host.cols - 10)
        for i, item in enumerate(self.items):
            prefix = "-->" if i == self.index else "   "
            suffix = " <--" if i == self.index else ""
            clip.append("%s %s %s%s" %
                        (prefix, item[1][-limit:], item[2], suffix))
        self.view.host.textBuffer.selection_all()
        self.view.host.textBuffer.edit_paste_lines(tuple(clip))
        self.cursor_move_to(self.index, 0)

    def next_item(self):
        self.index = (self.index + 1) % len(self.items)

    def prior_item(self):
        self.index = (self.index - 1) % len(self.items)

    def select_item(self):
        self.change_to_host_window()

    def unfocus(self):
        controller.Controller.unfocus(self)
        if self.items is None:
            return
        bufferManager = self.view.program.bufferManager
        textBuffer, fullPath = self.items[self.index][:2]
        if textBuffer is not None:
            self.view.host.set_text_buffer(
                bufferManager.get_valid_text_buffer(textBuffer)
            )
        else:
            expandedPath = os.path.abspath(os.path.expanduser(fullPath))
            textBuffer = bufferManager.load_text_buffer(expandedPath)
            self.view.host.set_text_buffer(textBuffer)
        self.items = None


class InteractiveFind(controller.Controller):
    """Find text within the current document."""

    def __init__(self, view):
        if config.strict_debug:
            assert issubclass(self.__class__, InteractiveFind), self
            assert issubclass(view.__class__, window.ViewWindow), view
        controller.Controller.__init__(self, view, "find")

    def find_next(self):
        self.findCmd = self.view.host.textBuffer.find_next

    def find_prior(self):
        self.findCmd = self.view.host.textBuffer.find_prior

    def focus(self):
        self.findCmd = self.view.host.textBuffer.find
        selection = self.view.host.textBuffer.get_selected_text()
        if selection:
            self.view.findLine.textBuffer.selection_all()
            # Make a single regex line.
            selection = "\\n".join(selection)
            log.info(selection)
            self.view.findLine.textBuffer.insert(re.escape(selection))
        self.view.findLine.textBuffer.selection_all()

    def on_change(self):
        self.view.findLine.textBuffer.parse_screen_maybe()
        searchFor = self.view.findLine.textBuffer.parser.row_text(0)
        try:
            self.findCmd(searchFor)
        except re.error as e:
            if hasattr(e, "msg"):
                self.error = e.msg
            elif hasattr(e, "message"):
                self.error = e.message
            else:
                self.error = u"invalid regex"
        self.findCmd = self.view.host.textBuffer.find

    def replace_and_next(self):
        replaceWith = self.view.replaceLine.textBuffer.parser.row_text(0)
        self.view.host.textBuffer.replace_found(replaceWith)
        self.findCmd = self.view.host.textBuffer.find_next

    def replace_and_prior(self):
        replaceWith = self.view.replaceLine.textBuffer.parser.row_text(0)
        self.view.host.textBuffer.replace_found(replaceWith)
        self.findCmd = self.view.host.textBuffer.find_prior


class InteractiveFindInput(controller.Controller):
    """Find text within the current document."""

    def __init__(self, view):
        if config.strict_debug:
            assert issubclass(self.__class__, InteractiveFindInput), self
            assert issubclass(view.__class__, window.ViewWindow), view
        controller.Controller.__init__(self, view, "find")

    def next_focusable_window(self):
        self.view.parent.expand_find_window(True)
        controller.Controller.next_focusable_window(self)

    # def prior_focusable_window(self):
    #  if not controller.Controller.prior_focusable_window(self):
    #    self.view.host.expand_find_window(False)

    def find_next(self):
        self.parent_controller().find_next()

    def find_prior(self):
        self.parent_controller().find_prior()

    def info(self):
        log.info("InteractiveFind command set")

    def on_change(self):
        self.parent_controller().on_change()

    def replace_and_next(self):
        self.parent_controller().replace_and_next()

    def replace_and_prior(self):
        self.parent_controller().replace_and_prior()


class InteractiveGoto(controller.Controller):
    """Jump to a particular line number."""

    def __init__(self, view):
        if config.strict_debug:
            assert issubclass(self.__class__, InteractiveGoto), self
            assert issubclass(view.__class__, window.ViewWindow), view
        controller.Controller.__init__(self, view, "goto")

    def focus(self):
        log.info("InteractiveGoto.focus")
        self.textBuffer.selection_all()
        self.textBuffer.insert(unicode(self.view.host.textBuffer.penRow + 1))
        self.textBuffer.selection_all()

    def info(self):
        log.info(u"InteractiveGoto command set")

    def goto_bottom(self):
        log.info()
        self.textBuffer.selection_all()
        self.textBuffer.insert(
            unicode(self.view.host.textBuffer.parser.row_count()))
        self.change_to_host_window()

    def goto_halfway(self):
        self.textBuffer.selection_all()
        self.textBuffer.insert(
            unicode(self.view.host.textBuffer.parser.row_count() // 2 + 1)
        )
        self.change_to_host_window()

    def goto_top(self):
        self.textBuffer.selection_all()
        self.textBuffer.insert(u"0")
        self.change_to_host_window()

    def cursor_move_to(self, row, col):
        if config.strict_debug:
            assert isinstance(row, int)
            assert isinstance(col, int)
        textBuffer = self.view.host.textBuffer
        textBuffer.cursor_move_to(row, col)
        textBuffer.cursor_scroll_to_middle()
        textBuffer.redo()

    def on_change(self):
        log.info()
        self.textBuffer.parse_document()
        line = self.textBuffer.parser.row_text(0)
        gotoLine, gotoCol = (line.split(u",") + [u"0", u"0"])[:2]
        self.cursor_move_to(parse_int(gotoLine) - 1, parse_int(gotoCol))


class ToggleController(controller.Controller):
    def __init__(self, view):
        if config.strict_debug:
            assert issubclass(self.__class__, ToggleController), self
            assert issubclass(view.__class__, window.ViewWindow), view
        controller.Controller.__init__(self, view, u"toggle")

    def clear_value(self):
        category = self.view.prefCategory
        name = self.view.prefName
        prefs = self.view.program.prefs
        prefs.save(category, name, None)
        self.view.on_pref_changed(category, name)

    def toggle_value(self):
        category = self.view.prefCategory
        name = self.view.prefName
        prefs = self.view.program.prefs
        prefs.save(category, name, not prefs.category(category)[name])
        self.view.on_pref_changed(category, name)
