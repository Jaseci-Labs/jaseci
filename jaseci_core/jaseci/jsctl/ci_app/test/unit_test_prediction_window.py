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


class PredictionWindowTestCases(fake_curses_testing.FakeCursesTestCase):
    def setUp(self):
        self.longMessage = True
        fake_curses_testing.FakeCursesTestCase.set_up(self)

    def test_prediction(self):
        # self.set_movie_mode(True)
        sys.argv = []
        self.run_with_fake_inputs(
            [
                self.display_check(0, 0, [u" ci     "]),
                self.display_check(2, 7, [u"     "]),
                CTRL_P,
                self.display_check(0, 0, [u" ci               "]),
                self.display_check(2, 2, [u"- Type|Name "]),
                # self.display_check_not(3, 0, [u"    open <new file> "]),
                self.find_text_and_click(
                    1000, u"[x]open", curses.BUTTON1_PRESSED),
                self.display_check_not(3, 0, [u"    open <new file> "]),
                self.display_check(2, 2, [u"- Type|Name "]),
                self.find_text_and_click(
                    2000, u"[ ]open", curses.BUTTON1_PRESSED),
                # TODO(dschuyler): Look into why this fails:
                # self.display_check(3, 0, ["    open <new file> "]),
                CTRL_Q,
            ]
        )

    def test_save_as_to_quit(self):
        # self.set_movie_mode(True)
        sys.argv = []
        self.run_with_fake_inputs(
            [
                self.display_check(0, 0, [u" ci     "]),
                self.display_check(2, 7, [u"     "]),
                ord("a"),
                self.display_check(2, 7, [u"a    "]),
                CTRL_S,
                self.display_check(0, 0, [u" ci    Save File As"]),
                CTRL_Q,
                self.display_check(0, 0, [u" ci     "]),
                self.display_check(-2, 0, [u"      "]),
                CTRL_Q,
                ord("n"),
            ]
        )
