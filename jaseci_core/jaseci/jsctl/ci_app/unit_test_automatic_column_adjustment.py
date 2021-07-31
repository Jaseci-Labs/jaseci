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

import os
import sys

from .curses_util import *
from . import fake_curses_testing

kTestFile = u"#automatic_column_adjustment_test_file_with_unlikely_file_name~"


class AutomaticColumnAdjustmentCases(fake_curses_testing.FakeCursesTestCase):
    def setUp(self):
        fake_curses_testing.FakeCursesTestCase.set_up(self)

    def tearDown(self):
        fake_curses_testing.FakeCursesTestCase.tear_down(self)

    def test_column_adjustment_on_moving_by_one_line(self):
        # self.set_movie_mode(True)
        self.run_with_fake_inputs(
            [
                self.display_check(
                    0,
                    0,
                    [
                        u" ci     .                               ",
                        u"                                        ",
                        u"     1                                  ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"New buffer         |    1, 1 |   0%,  0%",
                        u"                                        ",
                    ],
                ),
                self.write_text(u"short line"),
                CTRL_J,
                self.write_text(
                    u"super long line that should go past the screen"),
                CTRL_J,
                self.write_text(u"line that slightly goes off screen"),
                self.display_check(
                    0,
                    0,
                    [
                        u" ci     *                               ",
                        u"                                        ",
                        u"     1 rt line                          ",
                        u"     2 er long line that should go past ",
                        u"     3 e that slightly goes off screen  ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                        3,35 |  66%,100%",
                        u"                                        ",
                    ],
                ),
                KEY_UP,
                KEY_END,  # Place cursor at the end of the second line.
                self.display_check(
                    0,
                    0,
                    [
                        u" ci     *                               ",
                        u"                                        ",
                        u"     1                                  ",
                        u"     2  that should go past the screen  ",
                        u"     3 tly goes off screen              ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                        2,47 |  33%,100%",
                        u"                                        ",
                    ],
                ),
                # scrollCol should be set to 0 since line 1 fits on screen.
                KEY_UP,
                self.display_check(
                    0,
                    0,
                    [
                        u" ci     *                               ",
                        u"                                        ",
                        u"     1 short line                       ",
                        u"     2 super long line that should go p ",
                        u"     3 line that slightly goes off scre ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                        1,11 |   0%,100%",
                        u"                                        ",
                    ],
                ),
                # cursor should snap back to the end of the second line.
                KEY_DOWN,
                self.display_check(
                    0,
                    0,
                    [
                        u" ci     *                               ",
                        u"                                        ",
                        u"     1                                  ",
                        u"     2  that should go past the screen  ",
                        u"     3 tly goes off screen              ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                        2,47 |  33%,100%",
                        u"                                        ",
                    ],
                ),
                # scrollCol should not change since line 1 doesn't fit on
                # screen.
                KEY_DOWN,
                self.display_check(
                    0,
                    0,
                    [
                        u" ci     *                               ",
                        u"                                        ",
                        u"     1                                  ",
                        u"     2  that should go past the screen  ",
                        u"     3 tly goes off screen              ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                        3,35 |  66%,100%",
                        u"                                        ",
                    ],
                ),
                KEY_UP,  # cursor moves back to original position.
                self.display_check(
                    0,
                    0,
                    [
                        u" ci     *                               ",
                        u"                                        ",
                        u"     1                                  ",
                        u"     2  that should go past the screen  ",
                        u"     3 tly goes off screen              ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                        2,47 |  33%,100%",
                        u"                                        ",
                    ],
                ),
                # Make line 3 fit on screen. This includes making room for the
                # cursor.
                KEY_DOWN,
                KEY_BACKSPACE1,
                KEY_BACKSPACE1,
                KEY_BACKSPACE1,
                KEY_UP,
                # Since line 3 now fits on screen, this should set scrollCol to
                # 0.
                KEY_DOWN,
                self.display_check(
                    0,
                    0,
                    [
                        u" ci     *                               ",
                        u"                                        ",
                        u"     1 short line                       ",
                        u"     2 super long line that should go p ",
                        u"     3 line that slightly goes off scr  ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                        3,32 |  66%,100%",
                        u"                                        ",
                    ],
                ),
                CTRL_Q,
                u"n",
            ]
        )

    def test_column_adjustment_on_moving_multiple_lines(self):
        """
        A test to check that the cursor column is stored properly and that
        after using a series of up/down arrow keys, when we end up back at the
        same line, the cursor should also be at the same position as when
        it first arrived on that line.
        """
        # self.set_movie_mode(True)
        self.run_with_fake_inputs(
            [
                self.display_check(
                    0,
                    0,
                    [
                        u" ci     .                               ",
                        u"                                        ",
                        u"     1                                  ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"New buffer         |    1, 1 |   0%,  0%",
                        u"                                        ",
                    ],
                ),
                self.write_text(u"short line"),
                CTRL_J,
                self.write_text(
                    u"super long line that should go past the screen"),
                CTRL_J,
                self.write_text(u"line that slightly goes off screen"),
                CTRL_J,
                self.write_text(u"short line"),
                CTRL_J,
                self.write_text(u"medium-short line"),
                CTRL_J,
                self.write_text(u"medium-long line that can fit"),
                self.display_check(
                    0,
                    0,
                    [
                        u" ci     *                               ",
                        u"                                        ",
                        u"     1 short line                       ",
                        u"     2 super long line that should go p ",
                        u"     3 line that slightly goes off scre ",
                        u"     4 short line                       ",
                        u"     5 medium-short line                ",
                        u"     6 medium-long line that can fit    ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                        6,30 |  83%,100%",
                        u"                                        ",
                    ],
                ),
                KEY_UP,  # Goes to end of 5th line.
                self.display_check(
                    0,
                    0,
                    [
                        u" ci     *                               ",
                        u"                                        ",
                        u"     1 short line                       ",
                        u"     2 super long line that should go p ",
                        u"     3 line that slightly goes off scre ",
                        u"     4 short line                       ",
                        u"     5 medium-short line                ",
                        u"     6 medium-long line that can fit    ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                        5,18 |  66%,100%",
                        u"                                        ",
                    ],
                ),
                KEY_UP,  # Goes to end of 4th line.
                self.display_check(
                    0,
                    0,
                    [
                        u" ci     *                               ",
                        u"                                        ",
                        u"     1 short line                       ",
                        u"     2 super long line that should go p ",
                        u"     3 line that slightly goes off scre ",
                        u"     4 short line                       ",
                        u"     5 medium-short line                ",
                        u"     6 medium-long line that can fit    ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                        4,11 |  50%,100%",
                        u"                                        ",
                    ],
                ),
                # Should go to column 30 of line 3 since we started at column
                # 30.
                KEY_UP,
                self.display_check(
                    0,
                    0,
                    [
                        u" ci     *                               ",
                        u"                                        ",
                        u"     1 short line                       ",
                        u"     2 super long line that should go p ",
                        u"     3 line that slightly goes off scre ",
                        u"     4 short line                       ",
                        u"     5 medium-short line                ",
                        u"     6 medium-long line that can fit    ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                        3,30 |  33%, 85%",
                        u"                                        ",
                    ],
                ),
                KEY_UP,  # Goes to column 30 of line 2.
                self.display_check(
                    0,
                    0,
                    [
                        u" ci     *                               ",
                        u"                                        ",
                        u"     1 short line                       ",
                        u"     2 super long line that should go p ",
                        u"     3 line that slightly goes off scre ",
                        u"     4 short line                       ",
                        u"     5 medium-short line                ",
                        u"     6 medium-long line that can fit    ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                        2,30 |  16%, 63%",
                        u"                                        ",
                    ],
                ),
                KEY_UP,  # Goes to end of line 1.
                self.display_check(
                    0,
                    0,
                    [
                        u" ci     *                               ",
                        u"                                        ",
                        u"     1 short line                       ",
                        u"     2 super long line that should go p ",
                        u"     3 line that slightly goes off scre ",
                        u"     4 short line                       ",
                        u"     5 medium-short line                ",
                        u"     6 medium-long line that can fit    ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                        1,11 |   0%,100%",
                        u"                                        ",
                    ],
                ),
                # All subsequent KEY_DOWNs should mirror the previous displays.
                KEY_DOWN,
                self.display_check(
                    0,
                    0,
                    [
                        u" ci     *                               ",
                        u"                                        ",
                        u"     1 short line                       ",
                        u"     2 super long line that should go p ",
                        u"     3 line that slightly goes off scre ",
                        u"     4 short line                       ",
                        u"     5 medium-short line                ",
                        u"     6 medium-long line that can fit    ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                        2,30 |  16%, 63%",
                        u"                                        ",
                    ],
                ),
                KEY_DOWN,
                self.display_check(
                    0,
                    0,
                    [
                        u" ci     *                               ",
                        u"                                        ",
                        u"     1 short line                       ",
                        u"     2 super long line that should go p ",
                        u"     3 line that slightly goes off scre ",
                        u"     4 short line                       ",
                        u"     5 medium-short line                ",
                        u"     6 medium-long line that can fit    ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                        3,30 |  33%, 85%",
                        u"                                        ",
                    ],
                ),
                KEY_DOWN,
                self.display_check(
                    0,
                    0,
                    [
                        u" ci     *                               ",
                        u"                                        ",
                        u"     1 short line                       ",
                        u"     2 super long line that should go p ",
                        u"     3 line that slightly goes off scre ",
                        u"     4 short line                       ",
                        u"     5 medium-short line                ",
                        u"     6 medium-long line that can fit    ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                        4,11 |  50%,100%",
                        u"                                        ",
                    ],
                ),
                KEY_DOWN,
                self.display_check(
                    0,
                    0,
                    [
                        u" ci     *                               ",
                        u"                                        ",
                        u"     1 short line                       ",
                        u"     2 super long line that should go p ",
                        u"     3 line that slightly goes off scre ",
                        u"     4 short line                       ",
                        u"     5 medium-short line                ",
                        u"     6 medium-long line that can fit    ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                        5,18 |  66%,100%",
                        u"                                        ",
                    ],
                ),
                KEY_DOWN,
                self.display_check(
                    0,
                    0,
                    [
                        u" ci     *                               ",
                        u"                                        ",
                        u"     1 short line                       ",
                        u"     2 super long line that should go p ",
                        u"     3 line that slightly goes off scre ",
                        u"     4 short line                       ",
                        u"     5 medium-short line                ",
                        u"     6 medium-long line that can fit    ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                        6,30 |  83%,100%",
                        u"                                        ",
                    ],
                ),
                CTRL_Q,
                u"n",
            ]
        )
