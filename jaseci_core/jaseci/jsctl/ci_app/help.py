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

import os
import sys

dirPath = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]

docs = {
    "command line": """\
Command line help
%s [args] [file...]

  -               Read from standard in.
  --              Treat remaining arguments as file names.
  --clearHistory  Cleanup the file (and undo) into in ~/.ci_edit/.
  --log           Display logging and debug info.
  --help          Print this help message then exit.
  --keys          Print key bindings then exit.
  --singleThread  Do not use a background thread for parsing.
  --test          Run unit tests and exit.
  --version       Print version and license information then exit.\
"""
    % (sys.argv[0],),
    "key bindings": """\
Key Bindings

Within the main text window:

  ctrl+a       Select all
  ctrl+c       Copy
  ctrl+e       Execute prompt (e:)
  ctrl+f       Find prompt (find:)
  ctrl+g       Go to line prompt (goto:)
  ctrl+l       Select current line (subsequent select next line)
  ctrl+o       Open file prompt (open:)
  ctrl+p       Prediction prompt (p:)
  ctrl+q       Quit (exit editor)
  ctrl+r       Reverse find
  ctrl+s       Save file
  ctrl+v       Paste
  ctrl+w       Close document
  ctrl+x       Cut
  ctrl+y       Redo
  ctrl+z       Undo

Within the Find prompt:

  Text commands (such as cut and paste)
  operate on the prompt text rather
  than the main window.

  return       Exit Find
  esc          Exit Find
  ctrl+a       Select all*
  ctrl+c       Copy*
  ctrl+f       Find next
  ctrl+g       Find next
  ctrl+l       Select whole line*
  ctrl+o       Switch to Open prompt (open:)
  ctrl+p       Switch to Prediction prompt (p:)
  ctrl+q       Quit (exit editor)
  ctrl+r       Reverse find
  ctrl+s       Save file
  ctrl+v       Paste*
  ctrl+x       Cut*
  ctrl+y       Redo*
  ctrl+z       Undo*

  * Affects find: prompt, not the document.

Within the Goto line prompt:

  Text commands (such as cut and paste)
  operate on the prompt text rather
  than the main window.

  b            Jump to bottom of document
  h            Jump to half-way in the document
  t            Jump to top of document
  return       Exit Goto
  esc          Exit Goto
  ctrl+a       Select all*
  ctrl+c       Copy*
  ctrl+l       Select whole line*
  ctrl+p       Prediction prompt (p:)
  ctrl+q       Quit (exit editor)
  ctrl+s       Save file
  ctrl+v       Paste*
  ctrl+x       Cut*
  ctrl+y       Redo*
  ctrl+z       Undo*

  * Affects goto: prompt, not the document.\
""",
    "tips": [
        """Welcome to ci_edit.""",
        "",
        """Tips: press ctrl+q to quit, ctrl+s (aka ^s) to save, """
        """^a select all,""",
        """      ^z cut, ^x cut, ^c copy, ^v paste, ^f find, """
        """^o open file, ^w close,""",
        """      ^g goto line. ^e and ^p are need more explanation, """
        """see help.md file.""",
        "",
        # """What do you think of the help text above?""",
        # """Please add feedback"""
        # """ to https://github.com/google/ci_edit/issues/107""",
    ],
    "version": """\
  Version (build iteration): v51
  Within Python %s
  See LICENSE for license information
  See readme.md for an introduction
  Both files may be found in "%s"
  Please give the gift of feedback and bug reports at
    https://github.com/google/ci_edit/issues\
"""
    % (
        sys.version,
        dirPath,
    ),
    "welcome": """\
Welcome to the ci_edit text editor.\
""",
}
