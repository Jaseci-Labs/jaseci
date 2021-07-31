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
"""Manager for key bindings."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import curses
import curses.ascii

from . import config, log, window
from . import curses_util
from . import log
from . import selectable

# from . import window


class Controller:
    """A Controller is a keyboard mapping from keyboard/mouse events to editor
    commands."""

    def __init__(self, view, name):
        if config.strict_debug:
            assert issubclass(self.__class__, Controller)
            assert issubclass(view.__class__, window.Window)
        self.view = view
        self.commandDefault = None
        self.commandSet = None
        self.textBuffer = None
        self.name = name

    def parent_controller(self):
        view = self.view.parent
        while view is not None:
            if view.controller is not None:
                return view.controller
            view = view.parent

    def change_to_confirm_close(self):
        self.find_and_change_to("confirmClose")

    def change_to_confirm_overwrite(self):
        self.find_and_change_to("confirmOverwrite")

    def change_to_file_manager_window(self, *args):
        self.find_and_change_to("fileManagerWindow")

    def change_to_confirm_quit(self):
        self.find_and_change_to("interactiveQuit")

    def change_to_host_window(self, *args):
        host = self.get_named_window("inputWindow")
        if config.strict_debug:
            assert issubclass(self.view.__class__,
                              window.Window), self.view
            assert issubclass(host.__class__, window.Window), host
        self.view.change_focus_to(host)

    def change_to_input_window(self, *args):
        self.find_and_change_to("inputWindow")

    def change_to_find(self):
        self.find_and_change_to("interactiveFind")

    def change_to_find_prior(self):
        curses.ungetch(self.savedCh)
        self.find_and_change_to("interactiveFind")

    def change_to_goto(self):
        self.find_and_change_to("interactiveGoto")

    def change_to_palette_window(self):
        self.find_and_change_to("paletteWindow")

    def change_to_popup(self):
        self.find_and_change_to("popupWindow")

    def change_to_prediction(self):
        self.find_and_change_to("predictionWindow")
        # self.find_and_change_to('interactivePrediction')

    def change_to_prompt(self):
        self.find_and_change_to("interactivePrompt")

    def change_to_quit(self):
        self.find_and_change_to("interactiveQuit")

    def change_to_save_as(self):
        view = self.get_named_window("fileManagerWindow")
        view.set_mode("saveAs")
        view.bring_to_front()
        view.change_focus_to(view)

    def create_new_text_buffer(self):
        bufferManager = self.view.program.bufferManager
        self.view.set_text_buffer(bufferManager.new_text_buffer())

    def do_command(self, ch, meta):
        # Check the commandSet for the input with both its string and integer
        # representation.
        self.savedCh = ch

        cmd = self.commandSet.get(ch) or self.commandSet.get(
            curses_util.curses_key_name(ch)
        )

        if cmd:
            cmd()
        else:
            self.commandDefault(ch, meta)
        self.textBuffer.compound_change_push()

    def get_named_window(self, windowName):
        view = self.view
        while view is not None:
            if hasattr(view, windowName):
                return getattr(view, windowName)
            view = view.parent
        log.fatal(windowName + " not found")
        return None

    def current_input_window(self):
        return self.get_named_window("inputWindow")

    def find_and_change_to(self, windowName):
        window = self.get_named_window(windowName)
        window.bring_to_front()
        self.view.change_focus_to(window)
        return window

    def change_to(self, window):
        window.bring_to_front()
        self.view.change_focus_to(window)

    def focus(self):
        pass

    def confirmation_prompt_finish(self, *args):
        window = self.get_named_window("inputWindow")
        window.userIntent = "edit"
        window.bring_to_front()
        self.view.change_focus_to(window)

    def __close_host_file(self, host):
        """Close the current file and switch to another or create an empty
        file."""
        bufferManager = host.program.bufferManager
        bufferManager.close_text_buffer(host.textBuffer)
        host.userIntent = "edit"
        tb = bufferManager.get_unsaved_buffer()
        if not tb:
            tb = bufferManager.next_buffer()
            if not tb:
                tb = bufferManager.new_text_buffer()
        host.set_text_buffer(tb)

    def close_file(self):
        log.info()
        host = self.get_named_window("inputWindow")
        self.__close_host_file(host)
        self.confirmation_prompt_finish()

    def close_or_confirm_close(self):
        """If the file is clean, close it. If it is dirty, prompt the user
        about whether to lose unsaved changes."""
        host = self.get_named_window("inputWindow")
        tb = host.textBuffer
        if not tb.is_dirty():
            self.__close_host_file(host)
            return
        if host.userIntent == "edit":
            host.userIntent = "close"
        self.change_to_confirm_close()

    def initiate_close(self):
        """Called from input window controller."""
        self.view.userIntent = "close"
        tb = self.view.textBuffer
        if not tb.is_dirty():
            self.__close_host_file(self.view)
            return
        self.view.change_focus_to(self.view.confirmClose)

    def initiate_quit(self):
        """Called from input window controller."""
        self.view.userIntent = "quit"
        tb = self.view.textBuffer
        if tb.is_dirty():
            self.view.change_focus_to(self.view.interactiveQuit)
            return
        bufferManager = self.view.program.bufferManager
        tb = bufferManager.get_unsaved_buffer()
        if tb:
            self.view.set_text_buffer(tb)
            self.view.change_focus_to(self.view.interactiveQuit)
            return
        bufferManager.debug_log()
        self.view.quit_now()

    def initiate_save(self):
        """Called from input window controller."""
        self.view.userIntent = "edit"
        tb = self.view.textBuffer
        if tb.fullPath:
            if not tb.is_safe_to_write():
                self.view.change_focus_to(self.view.confirmOverwrite)
                return
            tb.file_write()
            return
        self.change_to_save_as()

    def overwrite_host_file(self):
        """Close the current file and switch to another or create an empty
        file.
        """
        host = self.get_named_window("inputWindow")
        host.textBuffer.file_write()
        if host.userIntent == "quit":
            self.quit_or_switch_to_confirm_quit()
            return
        if host.userIntent == "close":
            self.__close_host_file(host)
        self.change_to_host_window()

    def next_focusable_window(self):
        window = self.view.next_focusable_window(self.view)
        if window is not None:
            self.view.change_focus_to(window)
        return window is not None

    def prior_focusable_window(self):
        window = self.view.prior_focusable_window(self.view)
        if window is not None:
            self.view.change_focus_to(window)
        return window is not None

    def write_or_confirm_overwrite(self):
        """Ask whether the file should be overwritten."""
        log.debug()
        host = self.get_named_window("inputWindow")
        tb = host.textBuffer
        if not tb.is_safe_to_write():
            self.change_to_confirm_overwrite()
            return
        tb.file_write()
        # TODO(dschuyler): Is there a deeper issue here that necessitates saving
        # the message? Does this only need to wrap the change_to_host_window()?
        # Store the save message so it is not overwritten.
        saveMessage = tb.message
        if host.userIntent == "quit":
            self.quit_or_switch_to_confirm_quit()
            return
        if host.userIntent == "close":
            self.__close_host_file(host)
        self.change_to_host_window()
        tb.message = saveMessage  # Restore the save message.

    def quit_or_switch_to_confirm_quit(self):
        log.debug(self, self.view)
        host = self.get_named_window("inputWindow")
        tb = host.textBuffer
        host.userIntent = "quit"
        if tb.is_dirty():
            self.change_to_confirm_quit()
            return
        bufferManager = self.view.program.bufferManager
        tb = bufferManager.get_unsaved_buffer()
        if tb:
            host.set_text_buffer(tb)
            self.change_to_confirm_quit()
            return
        bufferManager.debug_log()
        host.quit_now()

    def save_or_change_to_save_as(self):
        log.debug()
        host = self.get_named_window("inputWindow")
        if config.strict_debug:
            assert issubclass(self.__class__, Controller), self
            assert issubclass(self.view.__class__, window.Window), self
            assert issubclass(host.__class__, window.Window), self
            assert self.view.textBuffer is self.textBuffer
            assert self.view.textBuffer is not host.textBuffer
        if host.textBuffer.fullPath:
            self.write_or_confirm_overwrite()
            return
        self.change_to_save_as()

    def on_change(self):
        pass

    def save_event_change_to_host_window(self, *args):
        curses.ungetch(self.savedCh)
        host = self.get_named_window("inputWindow")
        host.bring_to_front()
        self.view.change_focus_to(host)

    def set_text_buffer(self, textBuffer):
        if config.strict_debug:
            assert issubclass(
                textBuffer.__class__, text_buffer.TextBuffer
            ), textBuffer
            assert self.view.textBuffer is textBuffer
        self.textBuffer = textBuffer

    def unfocus(self):
        pass


class MainController:
    """The different keyboard mappings are different controllers. This class
    manages a collection of keyboard mappings and allows the user to switch
    between them."""

    def __init__(self, view):
        if config.strict_debug:
            assert issubclass(view.__class__, window.Window)
        self.view = view
        self.commandDefault = None
        self.commandSet = None
        self.controllers = {}
        self.controller = None

    def add(self, controller):
        self.controllers[controller.name] = controller
        self.controller = controller

    def current_input_window(self):
        return self.controller.current_input_window()

    def do_command(self, ch, meta):
        self.controller.do_command(ch, meta)

    def focus(self):
        log.info("MainController.focus")
        self.controller.focus()
        if 0:
            self.commandDefault = self.controller.commandDefault
            commandSet = self.controller.commandSet.copy()
            commandSet.update(
                {
                    curses_util.KEY_F2: self.next_controller,
                }
            )
            self.controller.commandSet = commandSet

    def on_change(self):
        tb = self.view.textBuffer
        if tb.message is None and tb.selectionMode != selectable.kSelectionNone:
            charCount, lineCount = tb.count_selected()
            tb.set_message(
                u"%d characters (%d lines) selected" % (charCount, lineCount)
            )
        self.controller.on_change()

    def next_controller(self):
        log.info("next_controller")
        if 0:
            if self.controller is self.controllers["cuaPlus"]:
                log.info("MainController.next_controller cua")
                self.controller = self.controllers["cua"]
            elif self.controller is self.controllers["cua"]:
                log.info("MainController.next_controller emacs")
                self.controller = self.controllers["emacs"]
            elif self.controller is self.controllers["emacs"]:
                log.info("MainController.next_controller vi")
                self.controller = self.controllers["vi"]
            else:
                log.info("MainController.next_controller cua")
                self.controller = self.controllers["cua"]
            self.controller.set_text_buffer(self.textBuffer)
            self.focus()

    def set_text_buffer(self, textBuffer):
        log.info("MainController.set_text_buffer", self.controller)
        if config.strict_debug:
            assert issubclass(textBuffer.__class__, text_buffer.TextBuffer)
        self.textBuffer = textBuffer
        self.controller.set_text_buffer(textBuffer)

    def unfocus(self):
        self.controller.unfocus()
