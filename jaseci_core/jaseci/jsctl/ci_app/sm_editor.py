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
"""Key bindings for the slash-menu editor."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import curses
import curses.ascii
from . import editor
import os
import re
import text_buffer

from .curses_util import *
from . import controller


class CiEdit(controller.Controller):
    """Keyboard mappings for ci."""

    def __init__(self, prg, textBuffer):
        controller.Controller.__init__(self, prg, None, "CiEdit")
        self.prg.log("CiEdit.__init__")
        self.textBuffer = textBuffer
        self.commandSet_Main = {
            CTRL_SPACE: self.switch_to_command_set_cmd,
            CTRL_A: textBuffer.cursor_start_of_line,
            CTRL_B: textBuffer.cursor_left,
            KEY_LEFT: self.cursor_left,
            CTRL_C: self.edit_copy,
            CTRL_H: self.backspace,
            KEY_BACKSPACE1: textBuffer.backspace,
            KEY_BACKSPACE2: textBuffer.backspace,
            KEY_BACKSPACE3: textBuffer.backspace,
            CTRL_D: self.delete,
            CTRL_E: self.cursor_end_of_line,
            CTRL_F: self.cursor_right,
            KEY_RIGHT: self.cursor_right,
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
