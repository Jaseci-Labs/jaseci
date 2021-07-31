# -*- coding: utf-8 -*-

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

from . import curses
import sys

from ..curses_util import *
from . import fake_curses_testing


class BraceMatchingTestCases(fake_curses_testing.FakeCursesTestCase):
    def setUp(self):
        self.longMessage = True
        fake_curses_testing.FakeCursesTestCase.set_up(self)
        fake_curses_testing.TestCaseHelper.setUp(self)

    def test_parenthesis(self):
        # self.set_movie_mode(True)
        sys.argv = []
        write = self.write_text
        check_style = self.display_check_style
        bracketColor = self.prg.color.get(u"bracket", 0)
        defaultColor = self.prg.color.get(u"default", 0)
        matchingBracketColor = self.prg.color.get(u"matching_bracket", 0)
        self.run_with_fake_inputs(
            [
                self.display_check(2, 7, [u"     "]),
                # Regression test for open ([{ without closing.
                write(u"("),
                self.display_check(2, 7, [u"(    "]),
                KEY_LEFT,
                CTRL_A,
                write(u"["),
                self.display_check(2, 7, [u"[    "]),
                KEY_LEFT,
                CTRL_A,
                write(u"{"),
                self.display_check(2, 7, [u"{    "]),
                KEY_LEFT,
                CTRL_A,
                # Test for closing )]} without opening.
                write(u")"),
                self.display_check(2, 7, [u")    "]),
                KEY_LEFT,
                CTRL_A,
                write(u"]"),
                self.display_check(2, 7, [u"]    "]),
                KEY_LEFT,
                CTRL_A,
                write(u"}"),
                self.display_check(2, 7, [u"}    "]),
                KEY_LEFT,
                CTRL_A,
                # Test adjacent matching.
                write(u"()"),
                self.display_check(2, 7, [u"()    "]),
                check_style(2, 7, 1, 2, bracketColor),
                KEY_LEFT,
                check_style(2, 7, 1, 2, matchingBracketColor),
                CTRL_A,
                write(u"[]"),
                self.display_check(2, 7, [u"[]    "]),
                check_style(2, 7, 1, 2, bracketColor),
                KEY_LEFT,
                check_style(2, 7, 1, 2, matchingBracketColor),
                CTRL_A,
                write(u"{}"),
                self.display_check(2, 7, [u"{}    "]),
                check_style(2, 7, 1, 2, bracketColor),
                KEY_LEFT,
                check_style(2, 7, 1, 2, matchingBracketColor),
                CTRL_A,
                # Test same line matching.
                write(u"(test)"),
                self.display_check(2, 7, [u"(test)    "]),
                check_style(2, 7, 1, 1, bracketColor),
                check_style(2, 8, 1, 4, defaultColor),
                check_style(2, 12, 1, 1, bracketColor),
                KEY_LEFT,
                check_style(2, 7, 1, 1, matchingBracketColor),
                check_style(2, 8, 1, 4, defaultColor),
                check_style(2, 12, 1, 1, matchingBracketColor),
                CTRL_A,
                write(u"[test]"),
                self.display_check(2, 7, [u"[test]    "]),
                check_style(2, 7, 1, 1, bracketColor),
                check_style(2, 8, 1, 4, defaultColor),
                check_style(2, 12, 1, 1, bracketColor),
                KEY_LEFT,
                check_style(2, 7, 1, 1, matchingBracketColor),
                check_style(2, 8, 1, 4, defaultColor),
                check_style(2, 12, 1, 1, matchingBracketColor),
                CTRL_A,
                write(u"{test}"),
                self.display_check(2, 7, [u"{test}    "]),
                check_style(2, 7, 1, 1, bracketColor),
                check_style(2, 8, 1, 4, defaultColor),
                check_style(2, 12, 1, 1, bracketColor),
                KEY_LEFT,
                check_style(2, 7, 1, 1, matchingBracketColor),
                check_style(2, 8, 1, 4, defaultColor),
                check_style(2, 12, 1, 1, matchingBracketColor),
                CTRL_A,
                CTRL_Q,
                u"n",
            ]
        )

    def test_parenthesis_double_wide_chars(self):
        # self.set_movie_mode(True)
        sys.argv = []
        write = self.write_text
        check_style = self.display_check_style
        bracketColor = self.prg.color.get(u"bracket", 0)
        defaultColor = self.prg.color.get(u"default", 0)
        matchingBracketColor = self.prg.color.get(u"matching_bracket", 0)
        self.run_with_fake_inputs(
            [
                self.display_check(2, 7, [u"     "]),
                # Test for open ([{ without closing.
                write(u"😃("),
                self.display_check(2, 7, [u"😃(    "]),
                KEY_LEFT,
                CTRL_A,
                write(u"😃["),
                self.display_check(2, 7, [u"😃[    "]),
                KEY_LEFT,
                CTRL_A,
                write(u"😃{"),
                self.display_check(2, 7, [u"😃{    "]),
                KEY_LEFT,
                CTRL_A,
                # Test for closing )]} without opening.
                write(u"😃)"),
                self.display_check(2, 7, [u"😃)    "]),
                KEY_LEFT,
                CTRL_A,
                write(u"😃]"),
                self.display_check(2, 7, [u"😃]    "]),
                KEY_LEFT,
                CTRL_A,
                write(u"😃}"),
                self.display_check(2, 7, [u"😃}    "]),
                KEY_LEFT,
                CTRL_A,
                # Test with wide character.
                write(u"(😃)"),
                self.display_check(2, 7, [u"(😃)    "]),
                # check_style(2, 7, 1, 2, bracketColor),
                KEY_LEFT,
                # check_style(2, 7, 1, 2, matchingBracketColor),
                CTRL_A,
                write(u"[😃]"),
                self.display_check(2, 7, [u"[😃]    "]),
                # check_style(2, 7, 1, 2, bracketColor),
                KEY_LEFT,
                # check_style(2, 7, 1, 2, matchingBracketColor),
                CTRL_A,
                write(u"{😃}"),
                self.display_check(2, 7, [u"{😃}    "]),
                # check_style(2, 7, 1, 2, bracketColor),
                KEY_LEFT,
                # check_style(2, 7, 1, 2, matchingBracketColor),
                CTRL_A,
                # Test same line matching.
                write(u"(test😃😃)"),
                self.display_check(2, 7, [u"(test😃😃)    "]),
                # check_style(2, 7, 1, 1, bracketColor),
                # check_style(2, 8, 1, 4, defaultColor),
                # check_style(2, 12, 1, 1, bracketColor),
                KEY_LEFT,
                # check_style(2, 7, 1, 1, matchingBracketColor),
                # heckStyle(2, 8, 1, 4, defaultColor),
                # check_style(2, 12, 1, 1, matchingBracketColor),
                CTRL_A,
                write(u"[😃😃test]"),
                self.display_check(2, 7, [u"[😃😃test]    "]),
                # check_style(2, 7, 1, 1, bracketColor),
                # check_style(2, 8, 1, 4, defaultColor),
                # check_style(2, 12, 1, 1, bracketColor),
                KEY_LEFT,
                # check_style(2, 7, 1, 1, matchingBracketColor),
                # check_style(2, 8, 1, 4, defaultColor),
                # check_style(2, 12, 1, 1, matchingBracketColor),
                CTRL_A,
                write(u"😃😃{test}"),
                self.display_check(2, 7, [u"😃😃{test}    "]),
                # check_style(2, 7, 1, 1, bracketColor),
                # check_style(2, 8, 1, 4, defaultColor),
                # check_style(2, 12, 1, 1, bracketColor),
                KEY_LEFT,
                # check_style(2, 7, 1, 1, matchingBracketColor),
                # check_style(2, 8, 1, 4, defaultColor),
                # check_style(2, 12, 1, 1, matchingBracketColor),
                CTRL_A,
                CTRL_Q,
                u"n",
            ]
        )
