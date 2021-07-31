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


class ExecutePromptTestCases(fake_curses_testing.FakeCursesTestCase):
    def setUp(self):
        self.longMessage = True
        fake_curses_testing.FakeCursesTestCase.set_up(self)

    def test_execute(self):
        # self.set_movie_mode(True)
        self.run_with_fake_inputs(
            [
                self.display_check(-1, 0, [u"      "]),
                CTRL_E,
                self.display_check(-1, 0, [u"e: "]),
                CTRL_J,
                self.display_check(-1, 0, [u"      "]),
                CTRL_E,
                self.display_check(-1, 0, [u"e: "]),
                CTRL_J,
                CTRL_Q,
            ]
        )

    def test_pipe_sort(self):
        # self.set_movie_mode(True)
        self.run_with_fake_inputs(
            [
                self.write_text(u"carrot\nbanana\nbanana\napple\n"),
                self.display_check(
                    2,
                    7,
                    [u"carrot  ", u"banana  ", u"banana  ",
                        u"apple  ", u"           "],
                ),
                CTRL_A,
                CTRL_E,
                self.write_text(u"|sort"),
                self.display_check(-1, 0, [u"e: |sort  "]),
                CTRL_J,
                self.display_check(
                    2,
                    7,
                    [u"apple  ", u"banana  ", u"banana  ",
                        u"carrot  ", u"           "],
                ),
                CTRL_Q,
                u"n",
            ]
        )
