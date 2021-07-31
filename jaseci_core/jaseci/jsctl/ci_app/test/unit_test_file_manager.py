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

import curses
import sys

from ..curses_util import *
from .. import fake_curses_testing


class FileManagerTestCases(fake_curses_testing.FakeCursesTestCase):
    def setUp(self):
        self.longMessage = True
        fake_curses_testing.FakeCursesTestCase.set_up(self)

    def test_save_as(self):
        # self.set_movie_mode(True)
        self.run_with_fake_inputs(
            [
                self.display_check(0, 0, [u" ci     "]),
                self.display_check(2, 7, [u"     "]),
                CTRL_S,
                self.display_check(0, 0, [u" ci    Save File As"]),
                CTRL_Q,
                CTRL_Q,
            ]
        )  # TODO(dschuyler): fix need for extra CTRL_Q.

    def test_save_as_to_quit(self):
        # self.set_movie_mode(True)
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

    def test_dir_and_path_with_cr(self):
        # self.set_movie_mode(True)
        self.run_with_fake_inputs(
            [
                self.display_check(0, 0, [u" ci     "]),
                self.display_check(2, 7, [u"     "]),
                CTRL_O,
                self.display_check(0, 0, [u" ci    Open File  "]),
                CTRL_A,
                self.write_text(self.path_to_sample(u"")),
                self.display_check(3, 0, [u"./     ", u"../     "]),
                self.display_check(5, 0, [u"._ A name with cr\\r/"]),
                self.mouse_event(0, 5, 0, curses.BUTTON1_PRESSED),
                self.display_check(5, 0, [u"example"]),
                self.display_find_check(u"/._ A name with ", u"cr\\r/"),
                KEY_ESCAPE,
                curses.ERR,
                self.display_check(0, 0, [u" ci     "]),
                self.display_check(2, 7, [u"     "]),
                CTRL_O,
                self.display_check(0, 0, [u" ci    Open File  "]),
                CTRL_A,
                self.write_text(self.path_to_sample(u"._ A name")),
                CTRL_I,
                self.display_check(5, 0, [u"example"]),
                self.display_find_check(u"/._ A name with ", u"cr\\r/"),
                CTRL_Q,
                CTRL_Q,
            ]
        )

    def test_mouse_scroll(self):
        # self.set_movie_mode(True)
        dirList = [
            u"./     ",
            u"../     ",
            u"._ A name with cr\\r/",
        ]
        self.run_with_fake_inputs(
            [
                self.display_check(0, 0, [u" ci     "]),
                self.display_check(2, 7, [u"     "]),
                CTRL_O,
                self.display_check(0, 0, [u" ci    Open File  "]),
                CTRL_A,
                self.write_text(self.path_to_sample(u"")),
                self.display_check(3, 0, dirList[0:3]),
                self.mouse_event(0, 5, 0, curses.REPORT_MOUSE_POSITION),
                self.display_check(3, 0, dirList[0:3]),
                self.mouse_event(1, 5, 0, curses.REPORT_MOUSE_POSITION),
                self.display_check(3, 0, dirList[1:3]),
                self.mouse_event(2, 5, 0, curses.REPORT_MOUSE_POSITION),
                self.display_check(3, 0, dirList[2:3]),
                self.mouse_event(0, 5, 0, curses.BUTTON4_PRESSED),
                self.display_check(3, 0, dirList[1:3]),
                self.mouse_event(1, 5, 0, curses.BUTTON4_PRESSED),
                self.display_check(3, 0, dirList[0:3]),
                self.mouse_event(2, 5, 0, curses.BUTTON4_PRESSED),
                self.display_check(3, 0, dirList[0:3]),
                CTRL_Q,
                CTRL_Q,
            ]
        )

    def test_open(self):
        # self.set_movie_mode(True)
        self.run_with_fake_inputs(
            [
                self.display_check(0, 0, [u" ci     "]),
                self.display_check(2, 7, [u"     "]),
                CTRL_O,
                self.display_check(0, 0, [u" ci    Open File  "]),
                CTRL_Q,
                CTRL_Q,
            ]
        )  # TODO(dschuyler): fix need for extra CTRL_Q.

    def test_open_binary_file(self):
        # self.set_movie_mode(True)
        self.run_with_fake_inputs(
            [
                self.display_check(0, 0, [u" ci     "]),
                self.display_check(2, 7, [u"     "]),
                CTRL_O,
                self.display_check(0, 0, [u" ci    Open File  "]),
                CTRL_A,
                self.write_text(self.path_to_sample(u"binary_test_file")),
                CTRL_J,
                self.display_check(
                    2, 7, [u"006401006c1a005a0800640000640100"]),
                CTRL_Q,
            ]
        )

    def test_open_valid_unicode_file(self):
        # self.set_movie_mode(True)
        self.run_with_fake_inputs(
            [
                self.display_check(0, 0, [u" ci     "]),
                self.display_check(2, 7, [u"     "]),
                CTRL_O,
                self.display_check(0, 0, [u" ci    Open File  "]),
                CTRL_A,
                self.write_text(self.path_to_sample(u"valid_unicode")),
                CTRL_J,
                self.display_check(4, 7, [u"Здравствуйте"]),
                CTRL_Q,
            ]
        )

    def test_empty_path_input(self):
        """Avoid crash when pressing return when the path input is empty."""
        # self.set_movie_mode(True)
        self.run_with_fake_inputs(
            [
                self.display_check(0, 0, [u" ci     "]),
                self.display_check(2, 7, [u"     "]),
                CTRL_O,
                self.display_check(0, 0, [u" ci    Open File  "]),
                CTRL_A,
                KEY_BACKSPACE1,
                self.display_check(2, 7, [u"     "]),
                CTRL_J,
                self.display_check(0, 0, [u" ci    Open File  "]),
                KEY_ESCAPE,
                curses.ERR,
                self.display_check(0, 0, [u" ci     "]),
                CTRL_Q,
            ]
        )

    def test_show_hide_columns(self):
        # self.set_movie_mode(True)
        self.run_with_fake_inputs(
            [
                self.pref_check(u"editor", u"filesShowSizes", True),
                self.display_check(0, 0, [u" ci     "]),
                CTRL_O,
                self.display_check(0, 0, [u" ci    Open"]),
                self.find_text_and_click(
                    1000, u"[x]sizes", curses.BUTTON1_PRESSED),
                CTRL_Q,
            ]
        )

    def test_click_scroll(self):
        # self.set_movie_mode(True)
        self.run_with_fake_inputs(
            [
                self.display_check(0, 0, [u" ci     "]),
                CTRL_O,
                self.display_check(0, 0, [u" ci    Open"]),
                KEY_PAGE_DOWN,
                self.display_find_check(u"AUTHORS", u""),
                CTRL_Q,
                # TODO(dschuyler): Quitting from the file manager uses two frame
                # updates. When that is fixed, this second CTRL_Q should be removed.
                CTRL_Q,
            ]
        )
