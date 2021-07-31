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

import re


def join_re_list(reList):
    return r"(" + r")|(".join(reList) + r")"


def join_re_word_list(reList):
    return r"(\b" + r"\b)|(\b".join(reList) + r"\b)"


kNonMatchingRegex = r"^\b$"
kReNonMatching = re.compile(kNonMatchingRegex)

# Beware, to include a ] in a set, it should be the first character in the set.
# So, the first ] does not close the set and the second [ does not open a set.
# The set of characters is ]{}()[.
kBracketsRegex = u"[]{}()[]"
kReBrackets = re.compile(kBracketsRegex)

kReComments = re.compile("(?:#|//).*$|/\*.*?\*/|<!--.*?-->")

kEndSpacesRegex = r"\s+$"
kReEndSpaces = re.compile(kEndSpacesRegex)

kReStrings = re.compile(
    r"(\"\"\".*?(?<!\\)\"\"\")|('''.*?(?<!\\)''')|(\".*?(?<!\\)\")" r"|('.*?(?<!\\)')"
)

# The first group is a hack to allow upper case pluralized, e.g. URLs.
kReSubwords = re.compile(
    r"(?:[A-Z]{2,}s\b)|(?:[A-Z][a-z]+)|(?:[A-Z]+(?![a-z]))|(?:[a-z]+)"
)

kReSubwordBoundaryFwd = re.compile(
    "(?:[_-]?[A-Z][a-z-]+)|(?:[_-]?[A-Z]+(?![a-z]))|(?:[_-]?[a-z]+)|(?:\W+)"
)

kReSubwordBoundaryRvr = re.compile(
    "(?:[A-Z][a-z-]+[_-]?)|(?:[A-Z]+(?![a-z])[_-]?)|(?:[a-z]+[_-]?)|(?:\W+)"
)

kReWordBoundary = re.compile("(?:\w+)|(?:\W+)")

kNumbersRegex = (
    # Don't include the [-+]? at the start of a number because it mismatches
    # an equation like 0x33-0x44.
    r"(?:"
    r"0[xX][A-Fa-f0-9]+"
    r"|\d+(?:(?:[uUlL][lL]?[lL]?)|\.?(?:\d+)?(?:e[-+]\d+)?[fFdD]?)?"
    r"|\.\d+[fFdD]?"
    r")"
    # r'0[xX][^A-Fa-f0-9]+(?:[uUlL][lL]?[lL]?)?(?!\w)',
    # r'[-+]?[0-9]*\.[0-9]+(?:[eE][+-][0-9]+)?[fF]?(?!\w)',
    # r'[-+]?[0-9]+(?:\.[0-9]*(?:[eE][+-][0-9]+)?)?[fF]?(?!\w)',
    # r'[-+]?[0-9]+(?:[uUlL][lL]?[lL]?)?(?!\w)',
)
kReNumbers = re.compile(kNumbersRegex)

# Trivia: all English contractions except 'sup, 'tis and 'twas will
# match this regex (with re.I):  [adegIlnotuwy]'[acdmlsrtv]
# The prefix part of that is used in the expression below to identify
# English contractions.
kEnglishContractionRegex = r"(\"(\\\"|[^\"])*?\")|(?<![adegIlnotuwy])('(\\\'|[^'])*?')"
