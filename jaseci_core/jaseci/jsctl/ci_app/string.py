# Copyright 2017 Google Inc.
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

from . import config

ENCODE = {
    u"\\": u"\\\\",
    u"\a": u"\\a",
    u"\b": u"\\b",
    u"\f": u"\\f",
    u"\n": u"\\n",
    u"\r": u"\\r",
    u"\t": u"\\t",
    u"\v": u"\\v",
    u"\x7f": u"\\x7f",
}

DECODE = {
    u"\\": u"\\",
    u"a": u"\a",
    u"b": u"\b",
    u"f": u"\f",
    u"n": u"\n",
    u"r": u"\r",
    u"t": u"\t",
    u"v": u"\v",
}


def path_encode(path):
    if config.strict_debug:
        assert isinstance(path, unicode), repr(path)
    out = u""
    for i in range(len(path)):
        c = path[i]
        ord_c = ord(c)
        t = ENCODE.get(c)
        if t is not None:
            c = t
        elif ord_c < 32:
            c = u"\\x%02x" % (ord_c,)
        out += c
    return out


def path_decode(path):
    if config.strict_debug:
        assert isinstance(path, unicode)
    out = u""
    limit = len(path)
    i = 0
    while i < limit:
        c = path[i]
        i += 1
        if c == u"\\":
            if i >= len(path):
                out += u"\\"
                break
            c = path[i]
            i += 1
            if c == u"x":
                c = unichr(path[i - 1: i + 3])
            elif c == u"u" or c == u"o":
                c = unichr(path[i - 1: i + 5])
            elif c == u"U":
                c = unichr(path[i - 1: i + 9])
            else:
                c = DECODE.get(c, u"\\")
        out += c
    return out
