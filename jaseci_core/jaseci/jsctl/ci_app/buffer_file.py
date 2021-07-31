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

from . import config


def path_row_column(path, projectDir):
    """Guess whether unrecognized file path refers to another file or has line
    and column information.

    Try to convert an unrecognized path to an exiting file.
    E.g.
    In `git diff` an 'a/' or 'b/' may be prepended to the path. Or in a compiler
    error ':<line number>' may be appended. If the file doesn't exist as-is, try
    removing those decorations, and if that exists use that path instead.

    Returns: (fullPath, openToRow, openToCol)
    """
    if config.strict_debug:
        assert isinstance(path, unicode)
        assert projectDir is None or isinstance(projectDir, unicode)
    openToRow = None
    openToColumn = None
    if os.path.isfile(path):  # or os.path.isdir(os.path.dirname(path)):
        return path, openToRow, openToColumn
    pieces = path.split(u":")
    if pieces[-1] == u"":
        if len(pieces) == 3:
            try:
                openToRow = int(pieces[1]) - 1
            except ValueError:
                pass
        elif len(pieces) == 4:
            try:
                openToRow = int(pieces[1]) - 1
                openToColumn = int(pieces[2]) - 1
            except ValueError:
                pass
    else:
        if len(pieces) == 2:
            try:
                openToRow = int(pieces[1]) - 1
            except ValueError:
                pass
        elif len(pieces) == 3:
            try:
                openToRow = int(pieces[1]) - 1
                openToColumn = int(pieces[2]) - 1
            except ValueError:
                pass
    if openToRow is not None:
        path = pieces[0]
    if len(path) > 2:  # and not os.path.isdir(path[:2]):
        if projectDir is not None and path.startswith(u"//"):
            path = projectDir + path[1:]
        elif path[1] == u"/":
            if os.path.isfile(path[2:]):
                path = path[2:]
    return path, openToRow, openToColumn


def expand_full_path(path):
    return os.path.abspath(os.path.expanduser(os.path.expandvars(path)))
