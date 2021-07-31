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

import curses

from .curses_util import *
from . import fake_curses_testing


class MisspellingsTestCases(fake_curses_testing.FakeCursesTestCase):
    def setUp(self):
        self.longMessage = True
        fake_curses_testing.FakeCursesTestCase.set_up(self)

    def test_highlight_misspellings(self):
        # self.set_movie_mode(True)
        self.run_with_fake_inputs(
            [
                self.display_check(0, 0, [u" ci  "]),
                self.cursor_check(2, 7),
                self.write_text(u"test asdf orange"),
                self.selection_check(0, 16, 0, 0, 0),
                self.display_check_style(
                    2, 7, 1, len(u"test "), self.prg.color.get(u"text", 0)
                ),
                self.display_check_style(
                    2, 12, 1, len(u"asdf"), self.prg.color.get(
                        u"misspelling", 0)
                ),
                self.display_check_style(
                    2, 16, 1, len(u" orange"), self.prg.color.get(u"text", 0)
                ),
                CTRL_Q,
                u"n",
            ]
        )
