# -*- coding: utf-8 -*-

# Copyright 2019 Google Inc.
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
import os
import sys

from ..curses_util import *
from .. import ci_program
from .. import curses_util
from . import fake_curses_testing

kTestFile = u"#application_test_file_with_unlikely_file_name~"


class CopyPasteTestCases(fake_curses_testing.FakeCursesTestCase):
    def setUp(self):
        self.longMessage = True
        fake_curses_testing.FakeCursesTestCase.set_up(self)
        fake_curses_testing.TestCaseHelper.setUp(self)

    def test_bracketed_paste(self):
        self.assertEqual(curses_util.char_width(u"ế", 0), 1)
        self.run_with_fake_inputs(
            [
                self.display_check(2, 7, [u"      "]),
                curses.ascii.ESC,
                curses_util.BRACKETED_PASTE_BEGIN,
                u"t",
                u"e",
                225,
                186,
                191,  # Send an "" in utf-8.
                u"t",
                curses.ascii.ESC,
                curses_util.BRACKETED_PASTE_END,
                self.display_check(2, 7, [u"te\u1ebft "]),
                CTRL_Q,
                u"n",
            ]
        )

    def test_cut_paste_undo_redo(self):
        # self.set_movie_mode(True)
        self.run_with_fake_inputs(
            [
                self.display_check(2, 7, [u"      "]),
                self.write_text(u"apple\nbanana\ncarrot\ndate\neggplant\nfig"),
                self.display_check(
                    2,
                    7,
                    [
                        u"apple   ",
                        u"banana   ",
                        u"carrot   ",
                        u"date   ",
                        u"eggplant   ",
                        u"fig   ",
                        u"         ",
                    ],
                ),
                self.selection_check(5, 3, 0, 0, 0),
                KEY_UP,
                KEY_UP,
                KEY_SHIFT_UP,
                KEY_SHIFT_UP,
                KEY_SHIFT_LEFT,
                self.selection_check(1, 2, 3, 3, 3),
                CTRL_X,
                self.display_check(
                    2,
                    7,
                    [
                        u"apple   ",
                        u"bae   ",
                        u"eggplant   ",
                        u"fig   ",
                        u"         ",
                    ],
                ),
                self.selection_check(1, 2, 1, 2, 0),
                CTRL_V,
                self.display_check(
                    2,
                    7,
                    [
                        u"apple   ",
                        u"banana   ",
                        u"carrot   ",
                        u"date   ",
                        u"eggplant   ",
                        u"fig   ",
                        u"         ",
                    ],
                ),
                self.selection_check(3, 3, 1, 2, 0),
                CTRL_V,
                self.display_check(
                    2,
                    7,
                    [
                        u"apple   ",
                        u"banana   ",
                        u"carrot   ",
                        u"datnana   ",
                        u"carrot   ",
                        u"date   ",
                        u"eggplant   ",
                        u"fig   ",
                        u"         ",
                    ],
                ),
                self.selection_check(5, 3, 1, 2, 0),
                CTRL_Z,
                self.display_check(
                    2,
                    7,
                    [
                        u"apple   ",
                        u"banana   ",
                        u"carrot   ",
                        u"date   ",
                        u"eggplant   ",
                        u"fig   ",
                        u"         ",
                    ],
                ),
                self.selection_check(3, 3, 1, 2, 0),
                CTRL_Z,
                self.display_check(
                    2,
                    7,
                    [
                        u"apple   ",
                        u"bae   ",
                        u"eggplant   ",
                        u"fig   ",
                        u"         ",
                    ],
                ),
                self.selection_check(1, 2, 1, 2, 0),
                CTRL_Y,
                CTRL_Y,
                self.display_check(
                    2,
                    7,
                    [
                        u"apple   ",
                        u"banana   ",
                        u"carrot   ",
                        u"datnana   ",
                        u"carrot   ",
                        u"date   ",
                        u"eggplant   ",
                        u"fig   ",
                        u"         ",
                    ],
                ),
                self.selection_check(5, 3, 1, 2, 0),
                CTRL_Q,
                u"n",
            ]
        )

    def test_write_text(self):
        self.run_with_fake_inputs([self.write_text(u"test\n"), CTRL_Q, u"n"])
