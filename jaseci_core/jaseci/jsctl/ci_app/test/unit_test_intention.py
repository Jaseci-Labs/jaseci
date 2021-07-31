# -*- coding: latin-1 -*-

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

import curses
import os
import sys

from ..curses_util import *
from .. import ci_program
from .. import fake_curses_testing

kTestFile = u"#application_test_file_with_unlikely_file_name~"


class IntentionTestCases(fake_curses_testing.FakeCursesTestCase):
    def setUp(self):
        self.longMessage = True
        fake_curses_testing.FakeCursesTestCase.set_up(self)

    def test_open_and_quit(self):
        self.run_with_test_file(kTestFile, [CTRL_Q])

    def test_new_file_quit(self):
        self.run_with_test_file(
            kTestFile, [self.display_check(2, 7, [u"        "]), CTRL_Q]
        )

    def test_quit_cancel(self):
        # self.set_movie_mode(True)
        self.run_with_fake_inputs(
            [
                self.display_check(
                    0,
                    0,
                    [
                        u" ci     .                               ",
                    ],
                ),
                u"x",
                CTRL_Q,
                u"c",
                self.write_text(u" after cancel"),
                self.display_check(
                    2,
                    7,
                    [
                        u"x after cancel ",
                    ],
                ),
                CTRL_Q,
                u"n",
            ]
        )

    def test_quit_save_as(self):
        # self.set_movie_mode(True)
        self.assertFalse(os.path.isfile(kTestFile))
        self.run_with_fake_inputs(
            [
                self.display_check(
                    0,
                    0,
                    [
                        u" ci     .                               ",
                    ],
                ),
                u"x",
                CTRL_Q,
                u"y",
                self.write_text(kTestFile),
                CTRL_J,
                CTRL_Q,
            ]
        )
        self.assertTrue(os.path.isfile(kTestFile))
        os.unlink(kTestFile)
        self.assertFalse(os.path.isfile(kTestFile))
