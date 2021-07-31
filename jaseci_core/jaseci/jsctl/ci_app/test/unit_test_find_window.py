# -*- coding: latin-1 -*-

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

import curses
import sys

from ..curses_util import *
from .. import fake_curses_testing


class FindWindowTestCases(fake_curses_testing.FakeCursesTestCase):
    def setUp(self):
        self.longMessage = True
        fake_curses_testing.FakeCursesTestCase.set_up(self)

    def test_find(self):
        self.run_with_fake_inputs(
            [
                self.display_check(-1, 0, [u"      "]),
                CTRL_F,
                self.display_check(-3, 0, [u"Find: "]),
                CTRL_J,
                self.display_check(-1, 0, [u"      "]),
                CTRL_F,
                self.display_check(-3, 0, [u"Find: "]),
                CTRL_I,
                self.display_check(-3, 0, [u"Find: ", u"Replace: ", u"["]),
                # KEY_BTAB, KEY_BTAB, self.display_check(-1, 0, [u"Find: "]),
                CTRL_Q,
            ]
        )

    def test_find_forward_and_reverse(self):
        self.run_with_fake_inputs(
            [
                self.write_text(
                    u"ten one two three\nfour one one five\n" u" six seven one\none\n"
                ),
                self.display_check(2, 7, [u"ten one two three  "]),
                self.display_check(-1, 0, [u"      "]),
                CTRL_F,
                self.display_check(-3, 0, [u"Find: "]),
                self.write_text(u"one"),
                self.selection_document_check(0, 4, 0, 7, 3),
                CTRL_F,
                self.selection_document_check(1, 5, 1, 8, 3),
                CTRL_F,
                self.selection_document_check(1, 9, 1, 12, 3),
                CTRL_R,
                self.selection_document_check(1, 5, 1, 8, 3),
                CTRL_R,
                self.selection_document_check(0, 4, 0, 7, 3),
                CTRL_R,
                self.selection_document_check(3, 0, 3, 3, 3),
                CTRL_R,
                self.selection_document_check(2, 11, 2, 14, 3),
                CTRL_R,
                self.selection_document_check(1, 9, 1, 12, 3),
                CTRL_R,
                self.selection_document_check(1, 5, 1, 8, 3),
                CTRL_F,
                self.selection_document_check(1, 9, 1, 12, 3),
                CTRL_F,
                self.selection_document_check(2, 11, 2, 14, 3),
                CTRL_F,
                self.selection_document_check(3, 0, 3, 3, 3),
                CTRL_F,
                self.selection_document_check(0, 4, 0, 7, 3),
                CTRL_F,
                self.selection_document_check(1, 5, 1, 8, 3),
                CTRL_Q,
                u"n",
            ]
        )

    def test_replace(self):
        # self.set_movie_mode(True)
        self.run_with_fake_inputs(
            [
                self.write_text(u"aDog\n"),
                self.display_check(2, 7, [u"aDog  "]),
                CTRL_F,
                self.write_text(u"a(.*)"),
                self.display_check(-3, 0, [u"Find: a(.*)  "]),
                CTRL_I,
                self.write_text(u"x\\1\\1"),
                self.display_check(-2, 0, [u"Replace: x\\1\\1  "]),
                CTRL_G,
                self.display_check(2, 7, [u"xDogDog  "]),
                CTRL_Q,
                u"n",
            ]
        )

    def test_invalid_replace(self):
        # self.set_movie_mode(True)
        self.run_with_fake_inputs(
            [
                self.write_text(u"aDog aDog\n"),
                self.display_check(2, 7, [u"aDog aDog  "]),
                CTRL_F,
                self.write_text(u"a"),
                self.display_check(-3, 0, [u"Find: a  "]),
                self.selection_document_check(0, 0, 0, 1, 3),
                CTRL_I,
                self.write_text(u"x\\1\\1"),
                self.display_check(-2, 0, [u"Replace: x\\1\\1  "]),
                CTRL_G,
                # The replacement will have failed (there is no \1 group). The
                # display should not have changed.
                self.display_check(2, 7, [u"aDog aDog  "]),
                # Since the replacement has an error, the selection should not move.
                # self.selection_document_check(0, 0, 0, 1, 3),
                # Doing a find doesn't involve the error in the replacement string,
                # so the selection should move.
                # CTRL_F, self.selection_document_check(0, 5, 0, 6, 3),
                CTRL_Q,
                u"n",
            ]
        )

    def test_find_replace_groups(self):
        # self.set_movie_mode(True)
        self.run_with_fake_inputs(
            [
                self.write_text(u"a\nb\na\nb\na\nb\n"),
                self.display_check(
                    2, 7, [u"a ", u"b ", u"a ", u"b ", u"a ", u"b "]),
                # Enter Find and make two document replacements.
                CTRL_F,
                self.write_text(u"(a)"),
                self.display_check(-3, 0, [u"Find: (a)  "]),
                CTRL_I,
                self.write_text(u"\\1!\\1"),
                self.display_check(-2, 0, [u"Replace: \\1!\\1  "]),
                CTRL_G,
                self.display_check(
                    2, 7, [u"a!a ", u"b ", u"a ", u"b ", u"a ", u"b "]),
                CTRL_G,
                self.display_check(
                    2, 7, [u"a!a ", u"b ", u"a!a ", u"b ", u"a ", u"b "]
                ),
                # Leave Find and Undo the document changes.
                KEY_ESCAPE,
                curses.ERR,
                CTRL_Z,
                self.display_check(
                    2, 7, [u"a ", u"b ", u"a ", u"b ", u"a ", u"b "]),
                # Go to bottom of document.
                CTRL_G,
                u"b",
                KEY_ESCAPE,
                curses.ERR,
                # Enter Find and make a reverse search replacement.
                CTRL_F,
                CTRL_R,
                CTRL_I,
                CTRL_R,
                self.display_check(
                    2, 7, [u"a ", u"b ", u"a ", u"b ", u"a!a ", u"b "]),
                # TODO(dschuyler): CTRL_R,
                # TODO(dschuyler): self.display_check(2, 7, [u"a ", u"b ", u"a!a ",
                # u"b ", u"a!a ", u"b "]),
                # Quit without saving.
                CTRL_Q,
                u"n",
            ]
        )

    def test_find_esc_from_find(self):
        self.run_with_fake_inputs(
            [
                # Check initial state.
                self.display_check(-1, 0, [u"      "]),
                self.display_check_style(
                    -2, 0, 1, 10, self.prg.color.get(u"status_line", 0)
                ),
                # Basic open and close.
                CTRL_F,
                self.display_check(-3, 0, [u"Find: "]),
                KEY_ESCAPE,
                curses.ERR,
                self.display_check(-3, 0, [u"   ", u"   ", u"   "]),
                self.display_check_style(
                    -2, 0, 1, 10, self.prg.color.get(u"status_line", 0)
                ),
                # Open, expand, and close.
                CTRL_F,
                self.display_check(-3, 0, [u"Find: "]),
                CTRL_I,
                self.display_check(-3, 0, [u"Find: ", u"Replace: ", u"["]),
                KEY_ESCAPE,
                curses.ERR,
                self.display_check(-3, 0, [u"   ", u"   ", u"   "]),
                self.display_check_style(
                    -2, 0, 1, 10, self.prg.color.get(u"status_line", 0)
                ),
                # Regression test one for
                # https://github.com/google/ci_edit/issues/170.
                CTRL_F,
                self.display_check(-3, 0, [u"Find: ", u"Replace: ", u"["]),
                CTRL_I,
                CTRL_I,
                self.display_check(-3, 0, [u"Find: ", u"Replace: ", u"["]),
                KEY_ESCAPE,
                curses.ERR,
                self.display_check(-3, 0, [u"   ", u"   ", u"   "]),
                self.display_check_style(
                    -2, 0, 1, 10, self.prg.color.get(u"status_line", 0)
                ),
                # Regression test two for
                # https://github.com/google/ci_edit/issues/170.
                CTRL_F,
                self.display_check(-3, 0, [u"Find: ", u"Replace: ", u"["]),
                self.mouse_event(0, 2, 10, curses.BUTTON1_PRESSED),
                # self.display_check(-3, 0, ["   ", "   ", "   "]),
                self.display_check_style(
                    -2, 0, 1, 10, self.prg.color.get(u"status_line", 0)
                ),
                CTRL_Q,
            ]
        )

    def test_replace_style_parse(self):
        self.run_with_fake_inputs(
            [
                # self.display_check(2, 7, [u"      "]),
                # self.display_check_style(2, 7, 1, 10,
                #    self.prg.color.get(u'text', 0)),
                self.write_text(u"focusedWindow\n"),
                CTRL_F,
                # self.display_check(-1, 0, [u"Find:         "]),
                self.write_text(u"focused"),
                CTRL_I,
                # self.display_check(
                #    -3, 0, [u"Find: focused", "Replace:          ", u"["]),
                self.write_text(u"  focused"),
                # self.display_check(
                #    -3, 0, [u"Find: focused", "Replace:   focused", u"["]),
                CTRL_G,
                # Regression, replace causes 'Windo' to show as a misspelling.
                self.display_check_style(
                    2, 17, 1, 10, self.prg.color.get(u"text", 0)),
                CTRL_Q,
                ord("n"),
            ]
        )
