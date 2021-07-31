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
"""Interactive prompt to run advanced commands and sub-processes."""

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
import subprocess

from . import controller
from . import formatter
from . import config, log


def function_test_eq(a, b):
    assert a == b, u"%r != %r" % (a, b)


if 1:
    # Break up a command line, separate by |.
    kRePipeChain = re.compile(
        # r'''\|\|?|&&|((?:"(?:\\"|[^"])*"|'(?:\\'|[^'])*'|[^\s|&]+)+)''')
        r"""((?:"(?:\\"|[^"])*"|'(?:\\'|[^'])*'|\|\||[^|]+)+)"""
    )
    function_test_eq(
        kRePipeChain.findall(""" date "a b" 'c d ' | sort """),
        [""" date "a b" 'c d ' """, " sort "],
    )
    function_test_eq(kRePipeChain.findall("date"), ["date"])
    function_test_eq(kRePipeChain.findall("d-a.te"), ["d-a.te"])
    function_test_eq(kRePipeChain.findall("date | wc"), ["date ", " wc"])
    function_test_eq(kRePipeChain.findall("date|wc"), ["date", "wc"])
    function_test_eq(kRePipeChain.findall("date && sort"), ["date && sort"])
    function_test_eq(kRePipeChain.findall("date || sort"), ["date || sort"])
    function_test_eq(
        kRePipeChain.findall("""date "a b" 'c d ' || sort"""),
        ["""date "a b" 'c d ' || sort"""],
    )

# Break up a command line, separate by &&.
kReLogicChain = re.compile(
    r"""\s*(\|\|?|&&|"(?:\\"|[^"])*"|'(?:\\'|[^'])*'|[^\s|&]+)"""
)
function_test_eq(kReLogicChain.findall("date"), ["date"])
function_test_eq(kReLogicChain.findall("d-a.te"), ["d-a.te"])
function_test_eq(kReLogicChain.findall("date | wc"), ["date", "|", "wc"])
function_test_eq(kReLogicChain.findall("date|wc"), ["date", "|", "wc"])
function_test_eq(kReLogicChain.findall("date && sort"), ["date", "&&", "sort"])
function_test_eq(kReLogicChain.findall("date || sort"), ["date", "||", "sort"])
function_test_eq(
    kReLogicChain.findall(""" date "a\\" b" 'c d ' || sort """),
    ["date", '"a\\" b"', "'c d '", "||", "sort"],
)

# Break up a command line, separate by \\s.
kReArgChain = re.compile(r"""\s*("(?:\\"|[^"])*"|'(?:\\'|[^'])*'|[^\s]+)""")
function_test_eq(kReArgChain.findall("date"), ["date"])
function_test_eq(kReArgChain.findall("d-a.te"), ["d-a.te"])
function_test_eq(
    kReArgChain.findall(""" date "a b" 'c d ' "a\\" b" 'c\\' d ' """),
    ["date", '"a b"', "'c d '", '"a\\" b"', "'c\\' d '"],
)
function_test_eq(kReArgChain.findall("""bm +"""), ["bm", "+"])

# Break up a command line, separate by \w (non-word chars will be separated).
kReSplitCmdLine = re.compile(
    r"""\s*("(?:\\"|[^"])*"|'(?:\\'|[^'])*'|\w+|[^\s]+)\s*""")
function_test_eq(kReSplitCmdLine.findall("""bm ab"""), ["bm", "ab"])
function_test_eq(kReSplitCmdLine.findall("""bm+"""), ["bm", "+"])
function_test_eq(kReSplitCmdLine.findall(
    '''bm "one two"'''), ["bm", '"one two"'])
function_test_eq(kReSplitCmdLine.findall(
    '''bm "o\\"ne two"'''), ["bm", '"o\\"ne two"'])

# Unquote text.
kReUnquote = re.compile(r"""(["'])([^\1]*)\1""")
function_test_eq(kReUnquote.sub("\\2", "date"), "date")
function_test_eq(kReUnquote.sub("\\2", '"date"'), "date")
function_test_eq(kReUnquote.sub("\\2", "'date'"), "date")
function_test_eq(kReUnquote.sub("\\2", "'da\\'te'"), "da\\'te")
function_test_eq(kReUnquote.sub("\\2", '"da\\"te"'), 'da\\"te')


class InteractivePrompt(controller.Controller):
    """Extended commands prompt."""

    def __init__(self, view):
        controller.Controller.__init__(self, view, u"prompt")

    def set_text_buffer(self, textBuffer):
        controller.Controller.set_text_buffer(self, textBuffer)
        self.textBuffer = textBuffer
        self.commands = {
            u"bm": self.bookmark_command,
            u"build": self.build_command,
            u"cua": self.change_to_cua_mode,
            u"emacs": self.change_to_emacs_mode,
            u"make": self.make_command,
            u"open": self.open_command,
            # u'split': self.split_command,  # Experimental wip.
            u"vim": self.change_to_vim_normal_mode,
        }
        self.filters = {
            u"format": self.format_command,
            u"lower": self.lower_selected_lines,
            u"numEnum": self.assign_index_to_selected_lines,
            u"s": self.substitute_text,
            u"sort": self.sort_selected_lines,
            u"sub": self.substitute_text,
            u"upper": self.upper_selected_lines,
            u"wrap": self.wrap_selected_lines,
        }
        self.subExecute = {
            u"!": self.shell_execute,
            u"|": self.pipe_execute,
        }

    def bookmark_command(self, cmdLine, view):
        args = kReSplitCmdLine.findall(cmdLine)
        if len(args) > 1 and args[1][0] == u"-":
            if self.view.host.textBuffer.bookmark_remove():
                return {}, u"Removed bookmark"
            else:
                return {}, u"No bookmarks to remove"
        else:
            self.view.host.textBuffer.bookmark_add()
            return {}, u"Added bookmark"

    def build_command(self, cmdLine, view):
        return {}, u"building things"

    def change_to_cua_mode(self, cmdLine, view):
        return {}, u"CUA mode"

    def change_to_emacs_mode(self, cmdLine, view):
        return {}, u"Emacs mode"

    def change_to_vim_normal_mode(self, cmdLine, view):
        return {}, u"Vim normal mode"

    def focus(self):
        log.info(u"InteractivePrompt.focus")
        self.textBuffer.selection_all()

    def format_command(self, cmdLine, lines):
        formatters = {
            # ".js": format_javascript.format
            # ".html": format_html.format,
            ".py": formatter.format_python
        }

        fileName, ext = os.path.splitext(self.view.host.textBuffer.fullPath)

        log.info(fileName, ext)
        formatter = formatters.get(ext)

        if not formatter:
            return lines, u"No formatter for extension {}".format(ext)

        try:
            formattedText = formatter(self.view.host.textBuffer.parser.data)
        except RuntimeError as err:
            return lines, str(err)

        lines = formattedText.split(u"\n")
        return lines, u"Changed %d lines" % (len(lines),)

    def make_command(self, cmdLine, view):
        return {}, u"making stuff"

    def open_command(self, cmdLine, view):
        """
        Opens the file under cursor.
        """
        args = kReArgChain.findall(cmdLine)
        log.info(args)
        if len(args) == 1:
            # If no args are provided, look for a path at the cursor position.
            view.textBuffer.open_file_at_cursor()
            return {}, view.textBuffer.message[0]
        # Try the raw path.
        path = args[1]
        if os.access(path, os.R_OK):
            return self.open_file(path, view)
        # Look in the same directory as the current file.
        path = os.path.join(os.path.dirname(view.textBuffer.fullPath), args[1])
        if os.access(path, os.R_OK):
            return self.open_file(path, view)
        return {}, u"Unable to open " + args[1]

    def open_file(self, path, view):
        textBuffer = view.program.bufferManager.load_text_buffer(path)
        inputWindow = self.current_input_window()
        inputWindow.set_text_buffer(textBuffer)
        self.change_to(inputWindow)
        inputWindow.set_message("Opened file {}".format(path))

    def split_command(self, cmdLine, view):
        view.split_window()
        return {}, u"Split window"

    def execute(self):
        try:
            cmdLine = self.textBuffer.parser.data
            if not len(cmdLine):
                self.change_to_host_window()
                return
            tb = self.view.host.textBuffer
            lines = list(tb.get_selected_text())
            if cmdLine[0] in self.subExecute:
                data = "\n".join(lines).encode("utf-8")
                output, message = self.subExecute.get(
                    cmdLine[0])(cmdLine[1:], data)
                if config.strict_debug:
                    assert isinstance(output, bytes)
                    assert isinstance(message, unicode)
                tb.edit_paste_lines(tuple(output.decode("utf-8").split(u"\n")))
                tb.set_message(message)
            else:
                cmd = re.split(u"\\W", cmdLine)[0]
                dataFilter = self.filters.get(cmd)
                if dataFilter:
                    if not len(lines):
                        tb.set_message(
                            u"The %s filter needs a selection." % (cmd,))
                    else:
                        lines, message = dataFilter(cmdLine, lines)
                        tb.set_message(message)
                        if not len(lines):
                            lines.append(u"")
                        tb.edit_paste_lines(tuple(lines))
                else:
                    command = self.commands.get(cmd, self.unknown_command)
                    message = command(cmdLine, self.view.host)[1]
                    tb.set_message(message)
        except Exception as e:
            log.exception(e)
            tb.set_message(u"Execution threw an error.")
        self.change_to_host_window()

    def shell_execute(self, commands, cmdInput):
        """
        cmdInput is in bytes (not unicode).
        return tuple: output as bytes (not unicode), message as unicode.
        """
        if config.strict_debug:
            assert isinstance(commands, unicode), type(commands)
            assert isinstance(cmdInput, bytes), type(cmdInput)
        try:
            process = subprocess.Popen(
                commands,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True,
            )
            return process.communicate(cmdInput)[0], u""
        except Exception as e:
            return u"", u"Error running shell command\n" + e

    def pipe_execute(self, commands, cmdInput):
        """
        cmdInput is in bytes (not unicode).
        return tuple: output as bytes (not unicode), message as unicode.
        """
        if config.strict_debug:
            assert isinstance(commands, unicode), type(commands)
            assert isinstance(cmdInput, bytes), type(cmdInput)
        chain = kRePipeChain.findall(commands)
        try:
            process = subprocess.Popen(
                kReArgChain.findall(chain[-1]),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            if len(chain) == 1:
                return process.communicate(cmdInput)[0], u""
            else:
                chain.reverse()
                prior = process
                for i in chain[1:]:
                    prior = subprocess.Popen(
                        kReArgChain.findall(i),
                        stdin=subprocess.PIPE,
                        stdout=prior.stdin,
                        stderr=subprocess.STDOUT,
                    )
                prior.communicate(cmdInput)
                return process.communicate()[0], u""
        except Exception as e:
            log.exception(e)
            return b"", u"Error running shell command\n" + unicode(e)

    def info(self):
        log.info(u"InteractivePrompt command set")

    def lower_selected_lines(self, cmdLine, lines):
        lines = [line.lower() for line in lines]
        return lines, u"Changed %d lines" % (len(lines),)

    def assign_index_to_selected_lines(self, cmdLine, lines):
        output = []
        for i, line in enumerate(lines):
            output.append(u"%s = %d" % (line, i))
        return output, u"Changed %d lines" % (len(output),)

    def sort_selected_lines(self, cmdLine, lines):
        lines.sort()
        return lines, u"Changed %d lines" % (len(lines),)

    def substitute_text(self, cmdLine, lines):
        if len(cmdLine) < 2:
            return (
                lines,
                u"""tip: %s/foo/bar/ to replace 'foo' with 'bar'.""" % (
                    cmdLine,),
            )
        if not lines:
            return lines, u"No text was selected."
        sre = re.match("\w+(\W)", cmdLine)
        if not sre:
            return (
                lines,
                u"""Separator punctuation missing, example:"""
                u""" %s/foo/bar/""" % (cmdLine,),
            )
        separator = sre.groups()[0]
        try:
            _, find, replace, flags = cmdLine.split(separator, 3)
        except ValueError:
            return (
                lines,
                u"""Separator punctuation missing, there should be"""
                u""" three '%s'.""" % (separator,),
            )
        data = self.view.host.textBuffer.parser.data
        output = self.view.host.textBuffer.find_replace_text(
            find, replace, flags, data)
        lines = output.split(u"\n")
        return lines, u"Changed %d lines" % (len(lines),)

    def upper_selected_lines(self, cmdLine, lines):
        lines = [line.upper() for line in lines]
        return lines, u"Changed %d lines" % (len(lines),)

    def unknown_command(self, cmdLine, view):
        self.view.host.textBuffer.set_message(u"Unknown command")
        return {}, u"Unknown command %s" % (cmdLine,)

    def wrap_selected_lines(self, cmdLine, lines):
        tokens = cmdLine.split()
        log.info("tokens", tokens)
        width = 80 if len(tokens) == 1 else int(tokens[1])
        indent = len(lines[0]) - len(lines[0].lstrip())
        width -= indent
        lines = curses_util.wrap_lines(lines, u" " * indent, width)
        return lines, u"Changed %d lines" % (len(lines),)
