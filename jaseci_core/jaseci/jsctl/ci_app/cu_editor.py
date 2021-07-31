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
"""Key bindings for the cua-like editor."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import curses

from .curses_util import *
from . import controller, log
from . import editor
from . import file_manager_controller
from . import interactive_prompt
from . import prediction_controller
from . import text_buffer


def init_command_set(controller, textBuffer):
    """The basic command set includes line editing controls."""
    return {
        CTRL_A: textBuffer.selection_all,
        CTRL_C: textBuffer.edit_copy,
        # CTRL_H: textBuffer.backspace,
        CTRL_L: textBuffer.cursor_select_line,
        CTRL_Q: controller.quit_or_switch_to_confirm_quit,
        CTRL_S: controller.save_or_change_to_save_as,
        CTRL_V: textBuffer.edit_paste,
        CTRL_W: controller.close_or_confirm_close,
        CTRL_X: textBuffer.edit_cut,
        CTRL_Y: textBuffer.edit_redo,
        CTRL_Z: textBuffer.edit_undo,
        KEY_BACKSPACE1: textBuffer.backspace,
        KEY_BACKSPACE2: textBuffer.backspace,
        KEY_BACKSPACE3: textBuffer.backspace,
        CTRL_BACKSPACE: textBuffer.backspace_word,
        KEY_DELETE: textBuffer.delete,
        KEY_HOME: textBuffer.cursor_start_of_line,
        KEY_END: textBuffer.cursor_end_of_line,
        KEY_SHOME: textBuffer.cursor_select_to_start_of_line,
        KEY_SEND: textBuffer.cursor_select_to_end_of_line,
        # KEY_DOWN: textBuffer.cursor_down,
        KEY_LEFT: textBuffer.cursor_left,
        KEY_RIGHT: textBuffer.cursor_right,
        # KEY_UP: textBuffer.cursor_up,
        KEY_ALT_LEFT: textBuffer.cursor_move_subword_left,
        KEY_ALT_SHIFT_LEFT: textBuffer.cursor_select_subword_left,
        KEY_ALT_RIGHT: textBuffer.cursor_move_subword_right,
        KEY_ALT_SHIFT_RIGHT: textBuffer.cursor_select_subword_right,
        KEY_CTRL_LEFT: textBuffer.cursor_move_word_left,
        KEY_CTRL_SHIFT_LEFT: textBuffer.cursor_select_word_left,
        KEY_CTRL_RIGHT: textBuffer.cursor_move_word_right,
        KEY_CTRL_SHIFT_RIGHT: textBuffer.cursor_select_word_right,
    }


def main_window_commands(controller, textBuffer):
    """The command set for a window (rather than a single line)."""
    commands = init_command_set(controller, textBuffer).copy()
    commands.update(
        {
            KEY_ESCAPE: textBuffer.normalize,
            KEY_F1: controller.info,
            KEY_BTAB: textBuffer.unindent,
            KEY_PAGE_UP: textBuffer.cursor_select_none_page_up,
            KEY_PAGE_DOWN: textBuffer.cursor_select_none_page_down,
            KEY_SHIFT_PAGE_UP: textBuffer.cursor_select_character_page_up,
            KEY_SHIFT_PAGE_DOWN: textBuffer.cursor_select_character_page_down,
            KEY_ALT_SHIFT_PAGE_UP: textBuffer.cursor_select_block_page_up,
            KEY_ALT_SHIFT_PAGE_DOWN: textBuffer.cursor_select_block_page_down,
            # CTRL_B:
            # textBuffer.jump_to_matching_bracket,
            CTRL_F: controller.change_to_find,
            CTRL_G: controller.change_to_goto,
            CTRL_I: textBuffer.indent,
            CTRL_J: textBuffer.carriage_return,
            CTRL_N: controller.create_new_text_buffer,
            CTRL_O: controller.change_to_file_manager_window,
            CTRL_Q: controller.initiate_quit,
            CTRL_R: controller.change_to_find_prior,
            CTRL_S: controller.initiate_save,
            CTRL_W: controller.initiate_close,
            KEY_DOWN: textBuffer.cursor_down,
            KEY_SHIFT_LEFT: textBuffer.cursor_select_left,
            KEY_SHIFT_RIGHT: textBuffer.cursor_select_right,
            KEY_UP: textBuffer.cursor_up,
            KEY_SHIFT_DOWN: textBuffer.cursor_select_down,
            KEY_SHIFT_UP: textBuffer.cursor_select_up,
            KEY_CTRL_DOWN: textBuffer.cursor_down_scroll,
            KEY_CTRL_SHIFT_DOWN: textBuffer.cursor_select_down_scroll,
            KEY_CTRL_UP: textBuffer.cursor_up_scroll,
            KEY_CTRL_SHIFT_UP: textBuffer.cursor_select_up_scroll,
        }
    )
    return commands


class ConfirmClose(controller.Controller):
    """Ask about closing a file with unsaved changes."""

    def __init__(self, view):
        controller.Controller.__init__(self, view, "confirmClose")

    def set_text_buffer(self, textBuffer):
        controller.Controller.set_text_buffer(self, textBuffer)
        commandSet = init_command_set(self, textBuffer)
        commandSet.update(
            {
                ord("n"): self.close_file,
                ord("N"): self.close_file,
                ord("y"): self.save_or_change_to_save_as,
                ord("Y"): self.save_or_change_to_save_as,
            }
        )
        self.commandSet = commandSet
        self.commandDefault = self.confirmation_prompt_finish


class ConfirmOverwrite(controller.Controller):
    """Ask about writing over an existing file."""

    def __init__(self, view):
        controller.Controller.__init__(self, view, "confirmOverwrite")

    def set_text_buffer(self, textBuffer):
        controller.Controller.set_text_buffer(self, textBuffer)
        commandSet = init_command_set(self, textBuffer)
        commandSet.update(
            {
                ord("y"): self.overwrite_host_file,
                ord("Y"): self.overwrite_host_file,
            }
        )
        self.commandSet = commandSet
        self.commandDefault = self.confirmation_prompt_finish


class InteractiveFind(editor.InteractiveFind):
    def __init__(self, view):
        editor.InteractiveFind.__init__(self, view)

    def set_text_buffer(self, textBuffer):
        pass


class InteractiveFindInput(editor.InteractiveFindInput):
    """Find text within the current document."""

    def __init__(self, view):
        editor.InteractiveFindInput.__init__(self, view)

    def focus(self):
        if self.view.parent.expanded:
            self.view.parent.parent.textBuffer.set_message(
                "Press ctrl+g to find again; ctrl+r find prior."
            )
        else:
            self.view.parent.parent.textBuffer.set_message(
                "Press tab for more options; ctrl+g to find next;" " ctrl+r find prior."
            )

    def set_text_buffer(self, textBuffer):
        editor.InteractiveFindInput.set_text_buffer(self, textBuffer)
        commandSet = init_command_set(self, textBuffer)
        commandSet.update(
            {
                KEY_BTAB: self.prior_focusable_window,
                KEY_ESCAPE: self.change_to_host_window,
                KEY_F1: self.info,
                KEY_F3: self.save_event_change_to_host_window,
                KEY_SHIFT_F3: self.save_event_change_to_host_window,
                # CTRL_E: self.extend_find_window,
                CTRL_F: self.find_next,
                CTRL_G: self.find_next,
                CTRL_I: self.next_focusable_window,
                CTRL_J: self.change_to_host_window,
                CTRL_N: self.save_event_change_to_host_window,
                CTRL_O: self.change_to_file_manager_window,
                CTRL_P: self.change_to_prediction,
                CTRL_R: self.find_prior,
                # KEY_DOWN: self.find_next,
                # KEY_UP: self.find_prior,
            }
        )
        self.commandSet = commandSet
        self.commandDefault = self.textBuffer.insert_printable


class InteractiveReplaceInput(editor.InteractiveFindInput):
    """Find text within the current document."""

    def __init__(self, view):
        editor.InteractiveFindInput.__init__(self, view)

    def focus(self):
        self.view.parent.parent.textBuffer.set_message(
            "Press ctrl+g to replace and find next; ctrl+r to replace and find"
            " prior."
        )

    def set_text_buffer(self, textBuffer):
        editor.InteractiveFindInput.set_text_buffer(self, textBuffer)
        commandSet = init_command_set(self, textBuffer)
        commandSet.update(
            {
                KEY_BTAB: self.prior_focusable_window,
                KEY_ESCAPE: self.change_to_host_window,
                KEY_F1: self.info,
                KEY_F3: self.save_event_change_to_host_window,
                KEY_SHIFT_F3: self.save_event_change_to_host_window,
                CTRL_E: self.extend_find_window,
                CTRL_F: self.find_next,
                CTRL_G: self.replace_and_next,
                CTRL_I: self.next_focusable_window,
                CTRL_J: self.change_to_host_window,
                CTRL_N: self.save_event_change_to_host_window,
                CTRL_O: self.change_to_file_manager_window,
                CTRL_P: self.change_to_prediction,
                CTRL_R: self.replace_and_prior,
                # KEY_DOWN: self.find_next,
                # KEY_UP: self.find_prior,
            }
        )
        self.commandSet = commandSet
        self.commandDefault = self.textBuffer.insert_printable

    def extend_find_window(self):
        self.view.host.toggleExtendedFindWindow()


class InteractiveGoto(editor.InteractiveGoto):
    """Jump to a particular line number."""

    def __init__(self, view):
        editor.InteractiveGoto.__init__(self, view)

    def set_text_buffer(self, textBuffer):
        editor.InteractiveGoto.set_text_buffer(self, textBuffer)
        commandSet = init_command_set(self, textBuffer)
        commandSet.update(
            {
                KEY_ESCAPE: self.change_to_host_window,
                KEY_F1: self.info,
                CTRL_F: self.change_to_find,
                CTRL_J: self.change_to_host_window,
                CTRL_N: self.save_event_change_to_host_window,
                CTRL_P: self.change_to_prediction,
                ord("b"): self.goto_bottom,
                ord("B"): self.goto_bottom,
                ord("h"): self.goto_halfway,
                ord("H"): self.goto_halfway,
                ord("t"): self.goto_top,
                ord("T"): self.goto_top,
            }
        )
        self.commandSet = commandSet
        self.commandDefault = self.textBuffer.insert_printable


class DirectoryList(file_manager_controller.DirectoryListController):
    """Open a file to edit."""

    def __init__(self, view):
        file_manager_controller.DirectoryListController.__init__(
            self, view)

    def set_text_buffer(self, textBuffer):
        assert textBuffer is self.view.textBuffer, textBuffer
        file_manager_controller.DirectoryListController.set_text_buffer(
            self, textBuffer
        )
        commandSet = {
            KEY_BTAB: self.prior_focusable_window,
            CTRL_I: self.next_focusable_window,
            CTRL_J: self.perform_open,
            KEY_ESCAPE: self.change_to_input_window,
            KEY_F1: self.info,
            KEY_PAGE_DOWN: textBuffer.cursor_select_none_page_down,
            KEY_PAGE_UP: textBuffer.cursor_select_none_page_up,
            KEY_DOWN: textBuffer.cursor_down,
            KEY_UP: textBuffer.cursor_up,
        }
        self.commandSet = commandSet
        self.commandDefault = self.pass_default_to_path_input


class FileOpener(file_manager_controller.FileManagerController):
    """Open a file to edit."""

    def __init__(self, view):
        file_manager_controller.FileManagerController.__init__(self, view)

    def set_text_buffer(self, textBuffer):
        file_manager_controller.FileManagerController.set_text_buffer(
            self, textBuffer
        )
        commandSet = init_command_set(self, textBuffer)
        commandSet.update(
            {
                KEY_ESCAPE: self.change_to_input_window,
                KEY_F1: self.info,
                KEY_PAGE_DOWN: self.pass_event_to_directory_list,
                KEY_PAGE_UP: self.pass_event_to_directory_list,
                KEY_DOWN: self.pass_event_to_directory_list,
                KEY_UP: self.pass_event_to_directory_list,
                CTRL_I: self.tab_complete_extend,
                CTRL_J: self.perform_primary_action,
                CTRL_N: self.save_event_change_to_host_window,
                CTRL_O: self.perform_primary_action,
                CTRL_P: self.change_to_prediction,
                CTRL_Q: self.save_event_change_to_host_window,
                CTRL_S: self.save_event_change_to_host_window,
            }
        )
        self.commandSet = commandSet
        self.commandDefault = self.textBuffer.insert_printable


class FilePathInput(file_manager_controller.FilePathInputController):
    """Open a file to edit."""

    def __init__(self, view):
        file_manager_controller.FilePathInputController.__init__(
            self, view)

    def set_text_buffer(self, textBuffer):
        file_manager_controller.FilePathInputController.set_text_buffer(
            self, textBuffer
        )
        commandSet = init_command_set(self, textBuffer)
        commandSet.update(
            {
                KEY_BTAB: self.prior_focusable_window,
                KEY_ESCAPE: self.change_to_input_window,
                KEY_F1: self.info,
                KEY_PAGE_DOWN: self.pass_event_to_directory_list,
                KEY_PAGE_UP: self.pass_event_to_directory_list,
                KEY_DOWN: self.pass_event_to_directory_list,
                KEY_UP: self.pass_event_to_directory_list,
                CTRL_I: self.tab_complete_extend,
                CTRL_J: self.perform_primary_action,
                CTRL_N: self.save_event_change_to_host_window,
                CTRL_O: self.perform_primary_action,
                CTRL_P: self.change_to_prediction,
                CTRL_Q: self.save_event_change_to_host_window,
                CTRL_S: self.save_event_change_to_host_window,
            }
        )
        self.commandSet = commandSet
        self.commandDefault = self.textBuffer.insert_printable


class InteractivePrediction(editor.InteractivePrediction):
    """Make a guess."""

    def __init__(self, view):
        editor.InteractivePrediction.__init__(self, view)

    def set_text_buffer(self, textBuffer):
        editor.InteractivePrediction.set_text_buffer(self, textBuffer)
        commandSet = init_command_set(self, textBuffer)
        commandSet.update(
            {
                KEY_ESCAPE: self.cancel,
                KEY_F1: self.info,
                CTRL_F: self.change_to_find,
                CTRL_G: self.change_to_goto,
                CTRL_J: self.select_item,
                CTRL_N: self.next_item,
                CTRL_O: self.change_to_file_manager_window,
                CTRL_P: self.prior_item,
                CTRL_Q: self.save_event_change_to_host_window,
                KEY_DOWN: self.next_item,
                KEY_UP: self.prior_item,
            }
        )
        self.commandSet = commandSet
        self.commandDefault = self.textBuffer.insert_printable


class InteractivePrompt(interactive_prompt.InteractivePrompt):
    """Extended command prompt."""

    def __init__(self, view):
        interactive_prompt.InteractivePrompt.__init__(self, view)

    def set_text_buffer(self, textBuffer):
        interactive_prompt.InteractivePrompt.set_text_buffer(
            self, textBuffer)
        commandSet = init_command_set(self, textBuffer)
        commandSet.update(
            {
                KEY_ESCAPE: self.change_to_host_window,
                KEY_F1: self.info,
                CTRL_J: self.execute,
                CTRL_N: self.save_event_change_to_host_window,
            }
        )
        self.commandSet = commandSet
        self.commandDefault = self.textBuffer.insert_printable


class InteractiveQuit(controller.Controller):
    """Ask about unsaved changes."""

    def __init__(self, view):
        controller.Controller.__init__(self, view, "interactiveQuit")

    def set_text_buffer(self, textBuffer):
        controller.Controller.set_text_buffer(self, textBuffer)
        self.textBuffer = textBuffer
        commandSet = init_command_set(self, textBuffer)
        commandSet.update(
            {
                # KEY_F1: self.info,
                ord("n"): self.view.quit_now,
                ord("N"): self.view.quit_now,
                ord("y"): self.save_or_change_to_save_as,
                ord("Y"): self.save_or_change_to_save_as,
            }
        )
        self.commandSet = commandSet
        self.commandDefault = self.confirmation_prompt_finish


class CuaEdit(controller.Controller):
    """Keyboard mappings for CUA. CUA is the Cut/Copy/Paste paradigm."""

    def __init__(self, view):
        controller.Controller.__init__(self, view, "CuaEdit")
        # self.view = view

    def set_text_buffer(self, textBuffer):
        controller.Controller.set_text_buffer(self, textBuffer)
        self.commandSet = main_window_commands(self, textBuffer)
        self.commandDefault = self.textBuffer.insert_printable

    def info(self):
        log.info("CuaEdit Command set main")
        log.info(repr(self))

    def on_change(self):
        pass


class CuaPlusEdit(CuaEdit):
    """Keyboard mappings for CUA, plus some extra."""

    def __init__(self, view):
        CuaEdit.__init__(self, view)
        log.info("CuaPlusEdit.__init__")

    def info(self):
        log.info("CuaPlusEdit Command set main")
        log.info(repr(self))

    def set_text_buffer(self, textBuffer):
        CuaEdit.set_text_buffer(self, textBuffer)
        commandSet = self.commandSet.copy()
        commandSet.update(
            {
                CTRL_E: self.change_to_prompt,
                CTRL_P: self.change_to_prediction,
                KEY_F1: textBuffer.toggle_show_tips,
                KEY_F2: textBuffer.bookmark_next,
                KEY_F3: textBuffer.find_again,
                KEY_F4: self.change_to_palette_window,
                KEY_F5: self.change_to_popup,
                KEY_SHIFT_F2: textBuffer.bookmark_prior,
                KEY_SHIFT_F3: textBuffer.find_back,
            }
        )
        self.commandSet = commandSet
        self.commandDefault = self.textBuffer.insert_printable_with_pairing


class PopupController(controller.Controller):
    """
    A controller for pop up boxes to notify the user.
    """

    def __init__(self, view):
        controller.Controller.__init__(self, view, "popup")
        self.callerSemaphore = None

        def no_op(ch, meta):
            log.info("no_op in PopupController")

        self.commandDefault = no_op
        self.commandSet = {
            KEY_ESCAPE: self.change_to_input_window,
        }

    def change_to_input_window(self):
        self.find_and_change_to("inputWindow")
        if self.callerSemaphore:
            self.callerSemaphore.release()
            self.callerSemaphore = None

    def set_options(self, options):
        """
        This function is used to change the options that are displayed in the
        popup window as well as their functions.

        Args:
          options (dict): A dictionary mapping keys (ints) to its
                          corresponding action.

        Returns;
          None.
        """
        self.commandSet = options

    def set_text_buffer(self, textBuffer):
        self.textBuffer = textBuffer


class PaletteDialogController(controller.Controller):
    """."""

    def __init__(self, view):
        controller.Controller.__init__(self, view, "Palette")
        self.view = view
        log.info("PaletteDialogController.__init__")

        def no_op(c, meta):
            log.info("no_op in PaletteDialogController")

        self.commandDefault = no_op
        self.commandSet = {
            KEY_F4: self.change_to_host_window,
            CTRL_J: self.change_to_host_window,
            KEY_ESCAPE: self.change_to_host_window,
        }

    def change_to_host_window(self):
        mainProgram = self.view.prg
        mainProgram.change_focus_to(mainProgram.inputWindow)

    def info(self):
        log.info("PaletteDialogController command set")
        log.info(repr(self))

    def set_text_buffer(self, textBuffer):
        self.textBuffer = textBuffer


class PredictionList(prediction_controller.PredictionListController):
    """Open a file to edit."""

    def __init__(self, view):
        prediction_controller.PredictionListController.__init__(self, view)

    def set_text_buffer(self, textBuffer):
        assert textBuffer is self.view.textBuffer, textBuffer
        prediction_controller.PredictionListController.set_text_buffer(
            self, textBuffer
        )
        commandSet = init_command_set(self, textBuffer)
        commandSet.update(
            {
                KEY_ESCAPE: self.change_to_input_window,
                KEY_F1: self.info,
                KEY_PAGE_DOWN: textBuffer.cursor_select_none_page_down,
                KEY_PAGE_UP: textBuffer.cursor_select_none_page_up,
                KEY_DOWN: textBuffer.cursor_down,
                KEY_UP: textBuffer.cursor_up,
            }
        )
        self.commandSet = commandSet
        self.commandDefault = self.textBuffer.insert_printable


class PredictionController(prediction_controller.PredictionController):
    """Open a file to edit."""

    def __init__(self, view):
        prediction_controller.PredictionController.__init__(self, view)

    def set_text_buffer(self, textBuffer):
        prediction_controller.PredictionController.set_text_buffer(
            self, textBuffer)
        commandSet = init_command_set(self, textBuffer)
        commandSet.update(
            {
                KEY_ESCAPE: self.change_to_input_window,
                KEY_F1: self.info,
                KEY_PAGE_DOWN: self.pass_event_to_directory_list,
                KEY_PAGE_UP: self.pass_event_to_directory_list,
                KEY_DOWN: self.pass_event_to_directory_list,
                KEY_UP: self.pass_event_to_directory_list,
                # CTRL_I: self.tab_complete_extend,
                CTRL_J: self.perform_primary_action,
                CTRL_N: self.save_event_change_to_host_window,
                CTRL_O: self.perform_primary_action,
                CTRL_P: self.change_to_prediction,
                CTRL_Q: self.save_event_change_to_host_window,
                CTRL_S: self.save_event_change_to_host_window,
            }
        )
        self.commandSet = commandSet
        self.commandDefault = self.textBuffer.insert_printable


class PredictionInputController(prediction_controller.PredictionInputController):
    """Open a file to edit."""

    def __init__(self, view):
        prediction_controller.PredictionInputController.__init__(
            self, view)

    def set_text_buffer(self, textBuffer):
        prediction_controller.PredictionInputController.set_text_buffer(
            self, textBuffer
        )
        commandSet = init_command_set(self, textBuffer)
        commandSet.update(
            {
                KEY_BTAB: self.prior_focusable_window,
                KEY_ESCAPE: self.change_to_input_window,
                KEY_F1: self.info,
                KEY_PAGE_DOWN: self.pass_event_to_prediction_list,
                KEY_PAGE_UP: self.pass_event_to_prediction_list,
                KEY_DOWN: self.pass_event_to_prediction_list,
                KEY_UP: self.pass_event_to_prediction_list,
                CTRL_L: self.open_alternate_file,
                CTRL_I: self.next_focusable_window,
                CTRL_J: self.perform_primary_action,
                CTRL_N: self.save_event_change_to_host_window,
                CTRL_O: self.perform_primary_action,
                CTRL_P: self.prediction_list_next,
                CTRL_Q: self.save_event_change_to_host_window,
                CTRL_S: self.save_event_change_to_host_window,
            }
        )
        self.commandSet = commandSet
        self.commandDefault = self.textBuffer.insert_printable


class ToggleController(editor.ToggleController):
    """Find text within the current document."""

    def __init__(self, view):
        editor.ToggleController.__init__(self, view)

    def set_text_buffer(self, textBuffer):
        editor.ToggleController.set_text_buffer(self, textBuffer)
        commandSet = init_command_set(self, textBuffer)
        commandSet.update(
            {
                KEY_BTAB: self.prior_focusable_window,
                KEY_ESCAPE: self.change_to_host_window,
                KEY_F3: self.save_event_change_to_host_window,
                KEY_SHIFT_F3: self.save_event_change_to_host_window,
                # CTRL_E: self.extend_find_window,
                CTRL_F: self.change_to_find,
                CTRL_G: self.change_to_find,
                CTRL_I: self.next_focusable_window,
                CTRL_J: self.toggle_value,
                CTRL_N: self.save_event_change_to_host_window,
                CTRL_O: self.change_to_file_manager_window,
                CTRL_P: self.change_to_prediction,
                CTRL_R: self.change_to_find_prior,
                ord(" "): self.toggle_value,
            }
        )
        self.commandSet = commandSet

        def no_op(ch, meta):
            log.info("no_op in ToggleController")

        self.commandDefault = no_op
