# -*- coding: utf-8 -*-
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
from . import window
from . import spelling
from . import render
from . import program_window
from . import prefs
from . import log
from . import history
from . import help
from . import curses_util
from . import color
from . import clipboard
from . import buffer_manager
from . import buffer_file
from . import background
from . import config
import traceback
import time
import sys
import struct
import os
import io
import locale
import curses
import pstats
import cProfile


unicode = str
unichr = chr

argv = []


def set_args(args: list):
    global argv
    argv = args


def get_args():
    global argv
    ret = argv
    argv = []
    return ret


def bytes_to_unicode(values):
    return bytes(values).decode("utf-8")


assert bytes_to_unicode((226, 143, 176)) == u"⏰"

userConsoleMessage = None


def user_message(*args):
    global userConsoleMessage
    if not userConsoleMessage:
        userConsoleMessage = ""
    args = [str(i) for i in args]
    userConsoleMessage += u" ".join(args) + u"\n"


class CiProgram:
    """This is the main editor program. It holds top level information and runs
    the main loop. The CiProgram is intended as a singleton.
    The program interacts with a single top-level ProgramWindow."""

    def __init__(self):
        log.startup(u"Python version ", sys.version)
        self.prefs = prefs.Prefs()
        self.color = color.Colors(self.prefs.color)
        self.dictionary = spelling.Dictionary(
            self.prefs.dictionaries[u"base"], self.prefs.dictionaries[u"path_match"]
        )
        self.clipboard = clipboard.Clipboard()
        # There is a background frame that is being build up/created. Once it's
        # completed it becomes the new front frame that will be drawn on the
        # screen. This frees up the background frame to begin drawing the next
        # frame (similar to, but not exactly like double buffering video).
        self.backgroundFrame = render.Frame()
        self.frontFrame = None
        self.history = history.History(
            self.prefs.userData.get("historyPath"))
        self.bufferManager = buffer_manager.BufferManager(self, self.prefs)
        self.cursesScreen = None
        self.debugMouseEvent = (0, 0, 0, 0, 0)
        self.exiting = False
        self.ch = 0
        self.bg = None

    def set_up_curses(self, cursesScreen):
        self.cursesScreen = cursesScreen
        curses.mousemask(-1)
        curses.mouseinterval(0)
        # Enable mouse tracking in xterm.
        sys.stdout.write("\033[?1002;h")
        # sys.stdout.write('\033[?1005;h')
        curses.meta(1)
        # Access ^c before shell does.
        curses.raw()
        # Enable Bracketed Paste Mode.
        sys.stdout.write("\033[?2004;h")
        # Push the escape codes out to the terminal. (Whether this is needed
        # seems to vary by platform).
        sys.stdout.flush()
        try:
            curses.start_color()
            if not curses.has_colors():
                user_message("This terminal does not support color.")
                self.quit_now()
            else:
                curses.use_default_colors()
        except curses.error as e:
            log.error(e)
        log.startup(u"curses.COLORS", curses.COLORS)
        if 0:
            assert curses.COLORS == 256
            assert curses.can_change_color() == 1
            assert curses.has_colors() == 1
            log.detail("color_content:")
            for i in range(0, curses.COLORS):
                log.detail("color", i, ": ", curses.color_content(i))
            for i in range(16, curses.COLORS):
                curses.init_color(i, 500, 500, i * 787 % 1000)
            log.detail("color_content, after:")
            for i in range(0, curses.COLORS):
                log.detail("color", i, ": ", curses.color_content(i))
        if 1:
            # rows, cols = self.cursesScreen.getmaxyx()
            cursesWindow = self.cursesScreen
            cursesWindow.leaveok(1)  # Don't update cursor position.
            cursesWindow.scrollok(0)
            cursesWindow.timeout(10)
            cursesWindow.keypad(1)
            window.mainCursesWindow = cursesWindow

    def command_loop(self):
        # Cache the thread setting.
        useBgThread = self.prefs.editor["useBgThread"]
        cmdCount = 0
        # Track the time needed to handle commands and render the UI.
        # (A performance measurement).
        self.mainLoopTime = 0
        self.mainLoopTimePeak = 0
        self.cursesWindowGetCh = window.mainCursesWindow.getch
        if self.prefs.startup["timeStartup"]:
            # When running a timing of the application startup, push a CTRL_Q
            # onto the curses event messages to simulate a full startup with a
            # GUI render.
            curses.ungetch(17)
        start = time.time()
        # The first render, to get something on the screen.
        if useBgThread:
            self.bg.put(u"cmdList", [])
        else:
            self.programWindow.short_time_slice()
            self.programWindow.render()
            self.backgroundFrame.set_cmd_count(0)
        # This is the 'main loop'. Execution doesn't leave this loop until the
        # application is closing down.
        while not self.exiting:
            if 0:
                profile = cProfile.Profile()
                profile.enable()
                self.refresh(drawList, cursor, cmdCount)
                profile.disable()
                output = io.StringIO.StringIO()
                stats = pstats.Stats(
                    profile, stream=output).sort_stats("cumulative")
                stats.print_stats()
                log.info(output.getvalue())
            self.mainLoopTime = time.time() - start
            if self.mainLoopTime > self.mainLoopTimePeak:
                self.mainLoopTimePeak = self.mainLoopTime
            # Gather several commands into a batch before doing a redraw.
            # (A performance optimization).
            cmdList = []
            while not len(cmdList):
                if not useBgThread:
                    (
                        drawList,
                        cursor,
                        frameCmdCount,
                    ) = self.backgroundFrame.grab_frame()
                    if frameCmdCount is not None:
                        self.frontFrame = (drawList, cursor, frameCmdCount)
                if self.frontFrame is not None:
                    drawList, cursor, frameCmdCount = self.frontFrame
                    self.refresh(drawList, cursor, frameCmdCount)
                    self.frontFrame = None
                for _ in range(5):
                    eventInfo = None
                    if self.exiting:
                        return
                    ch = self.get_ch()
                    # assert isinstance(ch, int), type(ch)
                    if ch == curses.ascii.ESC:
                        # Some keys are sent from the terminal as a sequence of
                        # bytes beginning with an Escape character. To help
                        # reason about these events (and apply event handler
                        # callback functions) the sequence is converted into
                        # tuple.
                        keySequence = []
                        n = self.get_ch()
                        while n != curses.ERR:
                            keySequence.append(n)
                            n = self.get_ch()
                        # log.info('sequence\n', keySequence)
                        # Check for Bracketed Paste Mode begin.
                        paste_begin = curses_util.BRACKETED_PASTE_BEGIN
                        if tuple(keySequence[: len(paste_begin)]) == paste_begin:
                            ch = curses_util.BRACKETED_PASTE
                            keySequence = keySequence[len(paste_begin):]
                            paste_end = (
                                curses.ascii.ESC,
                            ) + curses_util.BRACKETED_PASTE_END
                            while tuple(keySequence[-len(paste_end):]) != paste_end:
                                # log.info('waiting in paste mode')
                                n = self.get_ch()
                                if n != curses.ERR:
                                    keySequence.append(n)
                            keySequence = keySequence[: -(len(paste_end))]
                            eventInfo = struct.pack(
                                "B" * len(keySequence), *keySequence
                            ).decode(u"utf-8")
                        else:
                            ch = tuple(keySequence)
                        if not ch:
                            # The sequence was empty, so it looks like this
                            # Escape wasn't really the start of a sequence and
                            # is instead a stand-alone Escape. Just forward the
                            # esc.
                            ch = curses.ascii.ESC
                    elif type(ch) is int and 160 <= ch < 257:
                        # Start of utf-8 character.
                        u = None
                        if (ch & 0xE0) == 0xC0:
                            # Two byte utf-8.
                            b = self.get_ch()
                            u = bytes_to_unicode((ch, b))
                        elif (ch & 0xF0) == 0xE0:
                            # Three byte utf-8.
                            b = self.get_ch()
                            c = self.get_ch()
                            u = bytes_to_unicode((ch, b, c))
                        elif (ch & 0xF8) == 0xF0:
                            # Four byte utf-8.
                            b = self.get_ch()
                            c = self.get_ch()
                            d = self.get_ch()
                            u = bytes_to_unicode((ch, b, c, d))
                        assert u is not None
                        eventInfo = u
                        ch = curses_util.UNICODE_INPUT
                    if ch != curses.ERR:
                        self.ch = ch
                        if ch == curses.KEY_MOUSE:
                            # On Ubuntu, Gnome terminal, curses.getmouse() may
                            # only be called once for each KEY_MOUSE. Subsequent
                            # calls will throw an exception. So getmouse is
                            # (only) called here and other parts of the code use
                            # the eventInfo list instead of calling getmouse.
                            self.debugMouseEvent = curses.getmouse()
                            eventInfo = (self.debugMouseEvent, time.time())
                        cmdList.append((ch, eventInfo))
            start = time.time()
            if len(cmdList):
                if useBgThread:
                    self.bg.put(u"cmdList", cmdList)
                else:
                    self.programWindow.execute_command_list(cmdList)
                    self.programWindow.short_time_slice()
                    self.programWindow.render()
                    cmdCount += len(cmdList)
                    self.backgroundFrame.set_cmd_count(cmdCount)

    def process_background_messages(self):
        while self.bg.has_message():
            instruction, message = self.bg.get()
            if instruction == u"exception":
                for line in message:
                    user_message(line[:-1])
                self.quit_now()
                return
            elif instruction == u"render":
                # It's unlikely that more than one frame would be present in the
                # queue. If/when it happens, only the las/most recent frame
                # matters.
                self.frontFrame = message
            else:
                assert False

    def get_ch(self):
        """Get an input character (or event) from curses."""
        if self.exiting:
            return -1
        ch = self.cursesWindowGetCh()
        # The background thread can send a notice at any getch call.
        while ch == 0:
            if self.bg is not None:
                # Hmm, will ch ever equal 0 when self.bg is None?
                self.process_background_messages()
            if self.exiting:
                return -1
            ch = self.cursesWindowGetCh()
        return ch

    def startup(self):
        """A second init-like function. Called after command line arguments are
        parsed."""
        if config.strict_debug:
            assert issubclass(self.__class__, ci_program.CiProgram), self
        self.programWindow = program_window.ProgramWindow(self)
        top, left = window.mainCursesWindow.getyx()
        rows, cols = window.mainCursesWindow.getmaxyx()
        self.programWindow.reshape(top, left, rows, cols)
        self.programWindow.inputWindow.startup()
        self.programWindow.focus()

    def parse_args(self):
        """Interpret the command line arguments."""
        log.startup("isatty", sys.stdin.isatty())
        debugRedo = False
        showLogWindow = False
        cliFiles = []
        openToLine = None
        profile = False
        read_stdin = not sys.stdin.isatty()
        takeAll = False  # Take all args as file paths.
        timeStartup = False
        numColors = min(curses.COLORS, 256)
        if os.getenv(u"CI_EDIT_SINGLE_THREAD"):
            self.prefs.editor["useBgThread"] = False
        for i in get_args():
            if not takeAll and i[:1] == "+":
                openToLine = int(i[1:])
                continue
            if not takeAll and i[:2] == "--":
                if i == "--debugRedo":
                    debugRedo = True
                elif i == "--profile":
                    profile = True
                elif i == "--log":
                    showLogWindow = True
                elif i == "--d":
                    log.channel_enable("debug", True)
                elif i == "--m":
                    log.channel_enable("mouse", True)
                elif i == "--p":
                    log.channel_enable("info", True)
                    log.channel_enable("debug", True)
                    log.channel_enable("detail", True)
                    log.channel_enable("error", True)
                elif i == "--parser":
                    log.channel_enable("parser", True)
                elif i == "--singleThread":
                    self.prefs.editor["useBgThread"] = False
                elif i == "--startup":
                    log.channel_enable("startup", True)
                elif i == "--timeStartup":
                    timeStartup = True
                elif i == "--":
                    # All remaining args are file paths.
                    takeAll = True
                elif i == "--help":
                    user_message(help.docs["command line"])
                    self.quit_now()
                elif i == "--keys":
                    user_message(help.docs["key bindings"])
                    self.quit_now()
                elif i == "--clearHistory":
                    self.history.clear_user_history()
                    self.quit_now()
                elif i == "--eightColors":
                    numColors = 8
                elif i == "--version":
                    user_message(help.docs["version"])
                    self.quit_now()
                elif i.startswith("--"):
                    user_message("unknown command line argument", i)
                    self.quit_now()
                continue
            if i == "-":
                read_stdin = True
            else:

                cliFiles.append({"path": unicode(i)})

        # If there's no line specified, try to reinterpret the paths.
        if openToLine is None:
            decodedPaths = []
            for file in cliFiles:
                path, openToRow, openToColumn = buffer_file.path_row_column(
                    file[u"path"], self.prefs.editor[u"baseDirEnv"]
                )
                decodedPaths.append(
                    {"path": path, "row": openToRow, "col": openToColumn}
                )
            cliFiles = decodedPaths
        self.prefs.startup = {
            "debugRedo": debugRedo,
            "showLogWindow": showLogWindow,
            "cliFiles": cliFiles,
            "openToLine": openToLine,
            "profile": profile,
            "read_stdin": read_stdin,
            "timeStartup": timeStartup,
            "numColors": numColors,
        }
        self.showLogWindow = showLogWindow

    def quit_now(self):
        """Set the intent to exit the program. The actual exit will occur a bit
        later."""
        log.info()
        self.exiting = True

    def refresh(self, drawList, cursor, cmdCount):
        """Paint the drawList to the screen in the main thread."""
        cursesWindow = window.mainCursesWindow
        # Ask curses to hold the back buffer until curses refresh().
        cursesWindow.noutrefresh()
        curses.curs_set(0)  # Hide cursor.
        for i in drawList:
            try:
                cursesWindow.addstr(*i)
            except curses.error:
                log.error("failed to draw", repr(i))
                pass
        if cursor is not None:
            curses.curs_set(1)  # Show cursor.
            try:
                cursesWindow.leaveok(0)  # Do update cursor position.
                cursesWindow.move(cursor[0], cursor[1])  # Move cursor.
                # Calling refresh will draw the cursor.
                cursesWindow.refresh()
                cursesWindow.leaveok(1)  # Don't update cursor position.
            except curses.error:
                log.error("failed to move cursor", repr(i))
                pass
        # This is a workaround to allow background processing (and parser screen
        # redraw) to interact well with the test harness. The intent is to tell
        # the test that the screen includes all commands executed up to N.
        if hasattr(cursesWindow, "test_rendered_command_count"):
            cursesWindow.test_rendered_command_count(cmdCount)

    def make_home_dirs(self, homePath):
        try:
            if not os.path.isdir(homePath):
                os.makedirs(homePath)
            self.dirBackups = os.path.join(homePath, "backups")
            if not os.path.isdir(self.dirBackups):
                os.makedirs(self.dirBackups)
            self.dirPrefs = os.path.join(homePath, "prefs")
            if not os.path.isdir(self.dirPrefs):
                os.makedirs(self.dirPrefs)
            userDictionaries = os.path.join(homePath, "dictionaries")
            if not os.path.isdir(userDictionaries):
                os.makedirs(userDictionaries)
        except Exception as e:
            log.exception(e)

    def run(self):
        self.parse_args()
        self.set_up_palette()
        homePath = self.prefs.userData.get("homePath")
        self.make_home_dirs(homePath)
        self.history.load_user_history()
        curses_util.hack_curses_fixes()
        self.startup()
        if self.prefs.editor["useBgThread"]:
            self.bg = background.startup_background(self.programWindow)
        if self.prefs.startup.get("profile"):
            profile = cProfile.Profile()
            profile.enable()
            self.command_loop()
            profile.disable()
            output = io.StringIO.StringIO()
            stats = pstats.Stats(
                profile, stream=output).sort_stats("cumulative")
            stats.print_stats()
            log.info(output.getvalue())
        else:
            self.command_loop()
        if self.prefs.editor["useBgThread"]:
            self.bg.put(u"quit", None)
            self.bg.join()

    def set_up_palette(self):
        def apply_palette(name):
            palette = self.prefs.palette[name]
            foreground = palette["foregroundIndexes"]
            background = palette["backgroundIndexes"]
            for i in range(1, self.prefs.startup["numColors"]):
                curses.init_pair(i, foreground[i], background[i])

        def two_tries(primary, fallback):
            try:
                apply_palette(primary)
                log.startup(u"Primary color scheme applied")
            except curses.error:
                try:
                    apply_palette(fallback)
                    log.startup(u"Fallback color scheme applied")
                except curses.error:
                    log.startup(u"No color scheme applied")

        self.color.colors = self.prefs.startup["numColors"]
        if self.prefs.startup["numColors"] == 0:
            log.startup("using no colors")
        elif self.prefs.startup["numColors"] == 8:
            self.prefs.color = self.prefs.color8
            log.startup("using 8 colors")
            two_tries(self.prefs.editor["palette8"], "default8")
        elif self.prefs.startup["numColors"] == 16:
            self.prefs.color = self.prefs.color16
            log.startup("using 16 colors")
            two_tries(self.prefs.editor["palette16"], "default16")
        elif self.prefs.startup["numColors"] == 256:
            self.prefs.color = self.prefs.color256
            log.startup("using 256 colors")
            two_tries(self.prefs.editor["palette"], "default")
        else:
            raise Exception(
                "unknown palette color count " +
                repr(self.prefs.startup["numColors"])
            )

    if 1:  # For unit tests/debugging.

        def get_document_selection(self):
            """This is primarily for testing."""
            tb = self.programWindow.inputWindow.textBuffer
            return (tb.penRow, tb.penCol, tb.markerRow, tb.markerCol, tb.selectionMode)

        def get_selection(self):
            """This is primarily for testing."""
            tb = self.programWindow.focusedWindow.textBuffer
            return (tb.penRow, tb.penCol, tb.markerRow, tb.markerCol, tb.selectionMode)


def wrapped_ci(cursesScreen):
    try:
        prg = CiProgram()
        prg.set_up_curses(cursesScreen)
        prg.run()
    except Exception:
        user_message("---------------------------------------")
        user_message("Super sorry, something went very wrong.")
        user_message("Please create a New Issue and paste this info there.\n")
        errorType, value, tracebackInfo = sys.exc_info()
        out = traceback.format_exception(errorType, value, tracebackInfo)
        for i in out:
            user_message(i[:-1])
            # log.error(i[:-1])


def run_ci():
    locale.setlocale(locale.LC_ALL, "")
    try:
        # Reduce the delay waiting for escape sequences.
        os.environ.setdefault("ESCDELAY", "1")
        curses.wrapper(wrapped_ci)
    finally:
        log.flush()
        log.write_to_file("~/.ci_edit/recentLog")
        # Disable Bracketed Paste Mode.
        sys.stdout.write("\033[?2004l")
        # Disable mouse tracking in xterm.
        sys.stdout.write("\033[?1002;l")
        sys.stdout.flush()
    if userConsoleMessage:
        fullPath = buffer_file.expand_full_path(
            "~/.ci_edit/userConsoleMessage")
        with io.open(fullPath, "w+") as f:
            f.write(userConsoleMessage)
        sys.stdout.write(userConsoleMessage + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    run_ci()
