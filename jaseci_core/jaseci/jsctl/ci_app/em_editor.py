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
"""Key bindings for the emacs-like editor."""

# For Python 2to3 support.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import curses
import curses.ascii
import os
import re

from .curses_util import *
from . import controller
from . import log
from . import text_buffer


def parse_int(str):
    i = 0
    k = 0
    if len(str) > i and str[i] in ("+", "-"):
        i += 1
    k = i
    while len(str) > k and str[k].isdigit():
        k += 1
    if k > i:
        return int(str[:k])
    return 0


def test_parse_int():
    assert parse_int("0") == 0
    assert parse_int("0e") == 0
    assert parse_int("qwee") == 0
    assert parse_int("10") == 10
    assert parse_int("+10") == 10
    assert parse_int("-10") == -10
    assert parse_int("--10") == 0
    assert parse_int("--10") == 0


class EditText(controller.Controller):
    """An EditText is a base class for one-line controllers."""

    def __init__(self, view):
        controller.Controller.__init__(self, view, "EditText")
        self.document = None

    def set_text_buffer(self, textBuffer):
        textBuffer.lines = [u""]
        self.commandSet = {
            KEY_F1: self.info,
            CTRL_A: textBuffer.selection_all,
            CTRL_C: textBuffer.edit_copy,
            CTRL_H: textBuffer.backspace,
            KEY_BACKSPACE1: textBuffer.backspace,
            KEY_BACKSPACE2: textBuffer.backspace,
            KEY_BACKSPACE3: textBuffer.backspace,
            CTRL_Q: self.prg.quit,
            CTRL_S: self.save_document,
            CTRL_V: textBuffer.edit_paste,
            CTRL_X: textBuffer.edit_cut,
            CTRL_Y: textBuffer.redo,
            CTRL_Z: textBuffer.undo,
            # KEY_DOWN: textBuffer.cursor_down,
            KEY_LEFT: textBuffer.cursor_left,
            KEY_RIGHT: textBuffer.cursor_right,
            # KEY_UP: textBuffer.cursor_up,
        }

    def focus(self):
        log.info("EditText.focus", repr(self))
        self.commandDefault = self.textBuffer.insert_printable
        self.commandSet = self.commandSet

    def info(self):
        log.info("EditText command set")

    def save_document(self):
        log.info("save_document", self.document)
        if self.document and self.document.textBuffer:
            self.document.textBuffer.file_write()

    def unfocus(self):
        pass


class InteractiveOpener(EditText):
    """Open a file to edit."""

    def __init__(self, prg, view, textBuffer):
        EditText.__init__(self, prg, view, textBuffer)
        self.document = view.host
        log.info("xxxxx", self.document)
        commandSet = self.commandSet.copy()
        commandSet.update(
            {
                KEY_ESCAPE: self.change_to_input_window,
                KEY_F1: self.info,
                CTRL_I: self.tab_complete_extend,
                CTRL_J: self.create_or_open,
                CTRL_N: self.create_or_open,
                CTRL_O: self.create_or_open,
                CTRL_Q: self.prg.quit,
            }
        )
        self.commandSet = commandSet

    def focus(self):
        log.info("InteractiveOpener.focus")
        EditText.focus(self)
        # Create a new text buffer to display dir listing.
        self.view.host.set_text_buffer(text_buffer.TextBuffer(self.prg))

    def info(self):
        log.info("InteractiveOpener command set")

    def create_or_open(self):
        log.info("create_or_open")
        expandedPath = os.path.abspath(
            os.path.expanduser(self.textBuffer.lines[0]))
        if not os.path.isdir(expandedPath):
            self.view.host.set_text_buffer(
                self.prg.bufferManager.load_text_buffer(
                    expandedPath), self.view.host
            )
        self.change_to_input_window()

    def maybe_slash(self, expandedPath):
        if (
            self.textBuffer.lines[0]
            and self.textBuffer.lines[0][-1] != "/"
            and os.path.isdir(expandedPath)
        ):
            self.textBuffer.insert("/")

    def tab_complete_first(self):
        """Find the first file that starts with the pattern."""
        dirPath, fileName = os.path.split(self.lines[0])
        foundOnce = ""
        for i in os.listdir(os.path.expandvars(os.path.expanduser(dirPath)) or "."):
            if i.startswith(fileName):
                if foundOnce:
                    # Found more than one match.
                    return
                fileName = os.path.join(dirPath, i)
                if os.path.isdir(fileName):
                    fileName += "/"
                self.lines[0] = fileName
                self.on_change()
                return

    def tab_complete_extend(self):
        """Extend the selection to match characters in common."""
        dirPath, fileName = os.path.split(self.textBuffer.lines[0])
        expandedDir = os.path.expandvars(os.path.expanduser(dirPath)) or "."
        matches = []
        if not os.path.isdir(expandedDir):
            return
        for i in os.listdir(expandedDir):
            if i.startswith(fileName):
                matches.append(i)
            else:
                log.info("not", i)
        if len(matches) <= 0:
            self.maybe_slash(expandedDir)
            self.on_change()
            return
        if len(matches) == 1:
            self.textBuffer.insert(matches[0][len(fileName):])
            self.maybe_slash(os.path.join(expandedDir, matches[0]))
            self.on_change()
            return

        def find_common_prefix_length(prefixLen):
            count = 0
            ch = None
            for match in matches:
                if len(match) <= prefixLen:
                    return prefixLen
                if not ch:
                    ch = match[prefixLen]
                if match[prefixLen] == ch:
                    count += 1
            if count and count == len(matches):
                return find_common_prefix_length(prefixLen + 1)
            return prefixLen

        prefixLen = find_common_prefix_length(len(fileName))
        self.textBuffer.insert(matches[0][len(fileName): prefixLen])
        self.on_change()

    def set_file_name(self, path):
        self.textBuffer.lines = [path]
        self.textBuffer.penCol = len(path)
        self.textBuffer.goalCol = self.textBuffer.penCol

    def on_change(self):
        path = os.path.expanduser(os.path.expandvars(self.textBuffer.lines[0]))
        dirPath, fileName = os.path.split(path)
        dirPath = dirPath or "."
        log.info("O.on_change", dirPath, fileName)
        if os.path.isdir(dirPath):
            lines = []
            for i in os.listdir(dirPath):
                if i.startswith(fileName):
                    lines.append(i)
            if len(lines) == 1 and os.path.isfile(os.path.join(dirPath, fileName)):
                self.view.host.set_text_buffer(
                    self.view.program.bufferManager.load_text_buffer(
                        os.path.join(dirPath, fileName), self.view.host
                    )
                )
            else:
                self.view.host.textBuffer.lines = [
                    os.path.abspath(os.path.expanduser(dirPath)) + ":"
                ] + lines
        else:
            self.view.host.textBuffer.lines = [
                os.path.abspath(os.path.expanduser(dirPath)) + ": not found"
            ]


class InteractiveFind(EditText):
    """Find text within the current document."""

    def __init__(self, prg, view, textBuffer):
        EditText.__init__(self, prg, view, textBuffer)
        self.document = view.host
        self.commandSet.update(
            {
                KEY_ESCAPE: self.change_to_input_window,
                KEY_F1: self.info,
                CTRL_F: self.find_next,
                CTRL_J: self.change_to_input_window,
                CTRL_R: self.find_prior,
                # CTRL_S: self.replacement_text_edit,
                KEY_DOWN: self.find_next,
                KEY_MOUSE: self.save_event_change_to_host_window,
                KEY_UP: self.find_prior,
            }
        )
        self.height = 1

    def find_next(self):
        self.findCmd = self.document.textBuffer.find_next

    def find_prior(self):
        self.findCmd = self.document.textBuffer.find_prior

    def focus(self):
        # self.document.statusLine.hide()
        # self.document.resize_by(-self.height, 0)
        # self.view.host.move_by(-self.height, 0)
        # self.view.host.resize_by(self.height-1, 0)
        EditText.focus(self)
        self.findCmd = self.document.textBuffer.find
        selection = self.document.textBuffer.get_selected_text()
        if selection:
            self.textBuffer.selection_all()
            self.textBuffer.insert_lines(selection)
        self.textBuffer.selection_all()
        log.info("find tb", self.textBuffer.penCol)

    def info(self):
        log.info("InteractiveFind command set")

    def on_change(self):
        log.info("InteractiveFind.on_change")
        searchFor = self.textBuffer.lines[0]
        try:
            self.findCmd(searchFor)
        except re.error as e:
            self.error = e.message
        self.findCmd = self.document.textBuffer.find

    # def replacement_text_edit(self):
    #  pass

    def unfocus(self):
        log.info("unfocus Find")
        # self.hide()


class InteractiveGoto(EditText):
    """Jump to a particular line number."""

    def __init__(self, prg, view, textBuffer):
        EditText.__init__(self, prg, view, textBuffer)
        self.document = view.host
        commandSet = self.commandSet.copy()
        commandSet.update(
            {
                KEY_ESCAPE: self.change_to_input_window,
                KEY_F1: self.info,
                CTRL_J: self.change_to_input_window,
                KEY_MOUSE: self.save_event_change_to_host_window,
                ord("b"): self.goto_bottom,
                ord("h"): self.goto_halfway,
                ord("t"): self.goto_top,
            }
        )
        self.commandSet = commandSet

    def focus(self):
        log.info("InteractiveGoto.focus")
        self.textBuffer.selection_all()
        self.textBuffer.insert(str(self.document.textBuffer.penRow + 1))
        self.textBuffer.selection_all()
        EditText.focus(self)

    def info(self):
        log.info("InteractiveGoto command set")

    def goto_bottom(self):
        self.cursor_move_to(len(self.document.textBuffer.lines), 0)
        self.change_to_input_window()

    def goto_halfway(self):
        self.cursor_move_to(len(self.document.textBuffer.lines) // 2 + 1, 0)
        self.change_to_input_window()

    def goto_top(self):
        self.cursor_move_to(1, 0)
        self.change_to_input_window()

    def cursor_move_to(self, row, col):
        textBuffer = self.document.textBuffer
        penRow = min(max(row - 1, 0), len(textBuffer.lines) - 1)
        log.info("cursor_move_to row", row, penRow)
        textBuffer.cursor_move(
            penRow - textBuffer.penRow,
            col - textBuffer.penCol,
            col - textBuffer.goalCol,
        )

    def on_change(self):
        gotoLine = 0
        line = self.textBuffer.parser.row_text(0)
        gotoLine, gotoCol = (line.split(",") + ["0", "0"])[:2]
        self.cursor_move_to(parse_int(gotoLine), parse_int(gotoCol))

    # def unfocus(self):
    #  self.hide()


class CiEdit(controller.Controller):
    """Keyboard mappings for ci."""

    def __init__(self, prg, textBuffer):
        controller.Controller.__init__(self, prg, None, "CiEdit")
        log.info("CiEdit.__init__")
        self.textBuffer = textBuffer
        self.commandSet_Main = {
            CTRL_SPACE: self.switch_to_command_set_cmd,
            CTRL_A: textBuffer.cursor_start_of_line,
            CTRL_B: textBuffer.cursor_left,
            KEY_LEFT: self.cursor_left,
            CTRL_C: self.edit_copy,
            CTRL_D: self.delete,
            CTRL_E: self.cursor_end_of_line,
            CTRL_F: self.cursor_right,
            KEY_RIGHT: self.cursor_right,
            CTRL_H: self.backspace,
            KEY_BACKSPACE1: self.backspace,
            KEY_BACKSPACE2: self.backspace,
            KEY_BACKSPACE3: self.backspace,
            CTRL_J: self.carriage_return,
            CTRL_K: self.delete_to_end_of_line,
            CTRL_L: self.win.refresh,
            CTRL_N: self.cursor_down,
            KEY_DOWN: self.cursor_down,
            CTRL_O: self.split_line,
            CTRL_P: self.cursor_up,
            KEY_UP: self.cursor_up,
            CTRL_V: self.edit_paste,
            CTRL_X: self.edit_cut,
            CTRL_Y: self.redo,
            CTRL_Z: self.undo,
            CTRL_BACKSLASH: self.changeToCmdMode,
            # ord('/'): self.switch_to_command_set_cmd,
        }

        self.commandSet_Cmd = {
            ord("a"): self.switch_to_command_set_application,
            ord("f"): self.switch_to_command_set_file,
            ord("s"): self.switch_to_command_set_select,
            ord(";"): self.switch_to_command_set_main,
            ord("'"): self.marker_place,
        }

        self.commandSet_Application = {
            ord("q"): self.prg.quit,
            ord("t"): self.test,
            ord("w"): self.file_write,
            ord(";"): self.switch_to_command_set_main,
        }

        self.commandSet_File = {
            ord("o"): self.switch_to_command_set_file_open,
            ord("w"): self.file_write,
            ord(";"): self.switch_to_command_set_main,
        }

        self.commandSet_FileOpen = {
            ord(";"): self.switch_to_command_set_main,
        }

        self.commandSet_Select = {
            ord("a"): self.selection_all,
            ord("b"): self.selection_block,
            ord("c"): self.selection_character,
            ord("l"): self.selection_line,
            ord("x"): self.selection_none,
            ord(";"): self.switch_to_command_set_main,
        }

        self.commandDefault = self.insert_printable
        self.commandSet = self.commandSet_Main

    def switch_to_command_set_main(self, ignored=1):
        self.log("ci main", repr(self.prg))
        self.commandDefault = self.insert_printable
        self.commandSet = self.commandSet_Main

    def switch_to_command_set_cmd(self):
        self.log("ci cmd")
        self.commandDefault = self.textBuffer.no_op
        self.commandSet = self.commandSet_Cmd

    def switch_to_command_set_application(self):
        self.log("ci application")
        self.commandDefault = self.textBuffer.no_op
        self.commandSet = self.commandSet_Application

    def switch_to_command_set_file(self):
        self.commandDefault = self.textBuffer.no_op
        self.commandSet = self.commandSet_File

    def switch_to_command_set_file_open(self):
        self.log("switch_to_command_set_file_open")
        self.commandDefault = self.pathInsertPrintable
        self.commandSet = self.commandSet_FileOpen

    def switch_to_main_and_do_command(self, ch):
        self.log("switch_to_main_and_do_command")
        self.switch_to_command_set_main()
        self.do_command(ch)

    def switch_to_command_set_select(self):
        self.log("ci select")
        self.commandDefault = self.SwitchToMainAndDoCommand
        self.commandSet = self.commandSet_Select
        self.selection_character()


class EmacsEdit(controller.Controller):
    """Emacs is a common Unix based text editor. This keyboard mapping is
    similar to basic Emacs commands."""

    def __init__(self, view):
        controller.Controller.__init__(self, view, "EditText")

    def focus(self):
        log.info("EmacsEdit.focus")
        self.commandDefault = self.textBuffer.insert_printable
        self.commandSet = self.commandSet_Main

    def on_change(self):
        pass

    def set_text_buffer(self, textBuffer):
        log.info("EmacsEdit.set_text_buffer")
        self.textBuffer = textBuffer
        self.commandSet_Main = {
            KEY_F1: self.info,
            CTRL_A: textBuffer.cursor_start_of_line,
            CTRL_B: textBuffer.cursor_left,
            KEY_LEFT: textBuffer.cursor_left,
            CTRL_D: textBuffer.delete,
            CTRL_E: textBuffer.cursor_end_of_line,
            CTRL_F: textBuffer.cursor_right,
            KEY_RIGHT: textBuffer.cursor_right,
            # CTRL_H: textBuffer.backspace,
            KEY_BACKSPACE1: textBuffer.backspace,
            KEY_BACKSPACE2: textBuffer.backspace,
            KEY_BACKSPACE3: textBuffer.backspace,
            CTRL_J: textBuffer.carriage_return,
            CTRL_K: textBuffer.delete_to_end_of_line,
            CTRL_L: self.view.host.refresh,
            CTRL_N: textBuffer.cursor_down,
            KEY_DOWN: textBuffer.cursor_down,
            CTRL_O: textBuffer.split_line,
            CTRL_P: textBuffer.cursor_up,
            KEY_UP: textBuffer.cursor_up,
            CTRL_X: self.switch_to_command_set_x,
            CTRL_Y: textBuffer.redo,
            CTRL_Z: textBuffer.undo,
        }
        self.commandSet = self.commandSet_Main

        self.commandSet_X = {
            CTRL_C: self.prg.quit,
        }

    def info(self):
        log.info("EmacsEdit Command set main")
        log.info(repr(self))

    def switch_to_command_set_x(self):
        self.log("emacs x")
        self.commandSet = self.commandSet_X
