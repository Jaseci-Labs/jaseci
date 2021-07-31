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
import re
import time
import warnings

from . import buffer_file
from . import config, log
from . import controller
from . import string


class PredictionListController(controller.Controller):
    """Gather and prepare file directory information."""

    def __init__(self, view):
        assert self is not view
        controller.Controller.__init__(
            self, view, "PredictionListController")
        self.filter = None
        # |items| is a tuple of: buffer, path, flags, type.
        self.items = None
        self.shownList = None

    def _build_file_list(self, currentFile):
        if config.strict_debug:
            assert isinstance(currentFile, unicode), repr(currentFile)

        added = set()
        items = self.items = []
        if 1:
            # Add open buffers.
            def add_buffer(items, buffer, prediction):
                dirty = "*" if buffer.is_dirty() else "."
                if buffer.fullPath:
                    items.append((buffer, buffer.fullPath,
                                 dirty, "open", prediction))
                    added.add(buffer.fullPath)
                else:
                    items.append(
                        (
                            buffer,
                            "<new file> %s" % (buffer.parser.row_text(0)[:20]),
                            dirty,
                            "open",
                            prediction,
                        )
                    )

            bufferManager = self.view.program.bufferManager
            # Add the most resent buffer to allow flipping back and forth
            # between two files.
            if len(bufferManager.buffers) >= 2:
                add_buffer(items, bufferManager.buffers[-2], 30000)
            order = 39999
            for i in bufferManager.buffers[:-2]:
                add_buffer(items, i, order)
                order -= 1
            # This is the current buffer. It's unlikely to be the goal.
            if len(bufferManager.buffers) >= 1:
                add_buffer(items, bufferManager.buffers[-1], 90000)
        if 1:
            # Add recent files.
            for recentFile in self.view.program.history.get_recent_files():
                if recentFile not in added:
                    items.append((None, recentFile, "=", "recent", 50000))
                    added.add(recentFile)
        if 1:
            # Add alternate files.
            dirPath, fileName = os.path.split(currentFile)
            fileName, ext = os.path.splitext(fileName)
            # TODO(dschuyler): rework this ignore list.
            ignoreExt = set(
                (".pyc", ".pyo", ".o", ".obj", ".tgz", ".zip", ".tar"))
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
                    fullPath = os.path.join(dirPath, i)
                    if fullPath not in added:
                        items.append((None, fullPath, "=", "alt", 20000))
                        added.add(fullPath)
            if 1:
                # Chromium specific hack.
                if currentFile.endswith("-extracted.js"):
                    chromiumPath = currentFile[: -
                                               len("-extracted.js")] + ".html"
                    if os.path.isfile(chromiumPath) and chromiumPath not in added:
                        items.append((None, chromiumPath, "=", "alt", 20000))
                        added.add(chromiumPath)
                elif currentFile.endswith(".html"):
                    chromiumPath = currentFile[: -
                                               len(".html")] + "-extracted.js"
                    if os.path.isfile(chromiumPath) and chromiumPath not in added:
                        items.append((None, chromiumPath, "=", "alt", 20000))
                        added.add(chromiumPath)
        if self.filter is not None:
            try:
                with warnings.catch_warnings():
                    # Ignore future warning with '[[' regex.
                    warnings.simplefilter("ignore")
                    regex = re.compile(self.filter)
                i = 0
                while i < len(items):
                    if not regex.search(items[i][1]):
                        # Filter the list in-place.
                        items.pop(i)
                    else:
                        i += 1
            except re.error:
                self.view.textBuffer.set_message(u"invalid regex")

    def focus(self):
        # log.info('PredictionListController')
        self.on_change()
        controller.Controller.focus(self)

    def info(self):
        log.info("PredictionListController command set")

    def on_change(self):
        controller = self.view.parent.predictionInputWindow.controller
        self.filter = controller.decoded_path()
        if self.shownList == self.filter:
            return
        self.shownList = self.filter

        inputWindow = self.current_input_window()
        self._build_file_list(inputWindow.textBuffer.fullPath)
        if self.items is not None:
            self.view.update(self.items)
        self.filter = None

    def open_alt_file(self):
        for row, item in enumerate(self.items):
            if item[3] == "alt":
                self.open_file_or_dir(row)

    def open_file_or_dir(self, row):
        if config.strict_debug:
            assert isinstance(row, int)
        if self.items is None or len(self.items) == 0:
            return
        bufferManager = self.view.program.bufferManager
        textBuffer, fullPath = self.items[row][:2]
        self.items = None
        self.shownList = None
        if textBuffer is not None:
            textBuffer = bufferManager.get_valid_text_buffer(textBuffer)
        else:
            expandedPath = os.path.abspath(os.path.expanduser(fullPath))
            textBuffer = bufferManager.load_text_buffer(expandedPath)
        inputWindow = self.current_input_window()
        inputWindow.set_text_buffer(textBuffer)
        self.change_to(inputWindow)

    def option_changed(self, name, value):
        if config.strict_debug:
            assert isinstance(name, unicode)
            assert isinstance(value, unicode)
        self.shownList = None
        self.on_change()

    def set_filter(self, listFilter):
        if config.strict_debug:
            assert isinstance(listFilter, unicode)
        self.filter = listFilter
        self.shownList = None  # Cause a refresh.

    def unfocus(self):
        self.items = None
        self.shownList = None


class PredictionController(controller.Controller):
    """Create or open files."""

    def __init__(self, view):
        controller.Controller.__init__(self, view, "PredictionController")

    def perform_primary_action(self):
        self.view.pathWindow.controller.perform_primary_action()

    def info(self):
        log.info("PredictionController command set")

    def on_change(self):
        # log.info('PredictionController')
        self.view.predictionList.controller.on_change()
        controller.Controller.on_change(self)

    def option_changed(self, name, value):
        self.view.predictionList.controller.shownList = None

    def pass_event_to_prediction_list(self):
        self.view.predictionList.controller.do_command(self.savedCh, None)


class PredictionInputController(controller.Controller):
    """Manipulate query string."""

    def __init__(self, view):
        controller.Controller.__init__(
            self, view, "PredictionInputController")

    def decoded_path(self):
        if config.strict_debug:
            assert self.view.textBuffer is self.textBuffer
        return string.path_decode(self.textBuffer.parser.row_text(0))

    def set_encoded_path(self, path):
        if config.strict_debug:
            assert isinstance(path, unicode)
            assert self.view.textBuffer is self.textBuffer
        return self.textBuffer.replace_lines((string.path_encode(path),))

    def focus(self):
        # log.info('PredictionInputController')
        self.set_encoded_path(u"")
        # self.get_named_window('predictionList').controller.set_filter(u"py")
        self.get_named_window("predictionList").focus()
        controller.Controller.focus(self)

    def info(self):
        log.info("PredictionInputController command set")

    def on_change(self):
        # log.info('PredictionInputController', self.view.parent.get_path())
        self.get_named_window("predictionList").controller.on_change()
        controller.Controller.on_change(self)

    def option_changed(self, name, value):
        if config.strict_debug:
            assert isinstance(name, unicode)
            assert isinstance(value, unicode)
        self.get_named_window("predictionList").controller.shownList = None

    def pass_event_to_prediction_list(self):
        self.get_named_window("predictionList").controller.do_command(
            self.savedCh, None
        )

    def open_alternate_file(self):
        log.info("PredictionInputController")
        predictionList = self.get_named_window("predictionList")
        predictionList.controller.open_alt_file()

    def perform_primary_action(self):
        log.info("PredictionInputController")
        predictionList = self.get_named_window("predictionList")
        row = predictionList.textBuffer.penRow
        predictionList.controller.open_file_or_dir(row)

    def prediction_list_next(self):
        predictionList = self.get_named_window("predictionList")
        if (
            predictionList.textBuffer.penRow
            == predictionList.textBuffer.parser.row_count() - 1
        ):
            predictionList.textBuffer.cursor_move_to(0, 0)
        else:
            predictionList.textBuffer.cursor_down()

    def prediction_list_prior(self):
        predictionList = self.get_named_window("predictionList")
        if predictionList.textBuffer.penRow == 0:
            predictionList.textBuffer.cursor_move_to(
                predictionList.textBuffer.parser.row_count(), 0
            )
        else:
            predictionList.textBuffer.cursor_up()

    def unfocus(self):
        self.get_named_window("predictionList").unfocus()
        controller.Controller.unfocus(self)
