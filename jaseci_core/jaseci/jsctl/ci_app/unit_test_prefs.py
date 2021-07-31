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

import unittest

from .curses_util import *
from . import fake_curses_testing
from . import prefs


class PrefsTestCases(fake_curses_testing.FakeCursesTestCase):
    def setUp(self):
        self.longMessage = True
        fake_curses_testing.FakeCursesTestCase.set_up(self)
        self.prefs = prefs.Prefs()

    def test_default_prefs(self):
        self.run_with_fake_inputs(
            [
                self.pref_check(u"editor", u"saveUndo", True),
                CTRL_Q,
            ]
        )

    def test_get_file_type(self):
        get_file_type = self.prefs.get_file_type
        self.assertEqual(get_file_type(""), "words")
        self.assertEqual(get_file_type("a.py"), "py")
        self.assertEqual(get_file_type("a.cc"), "cpp")
        self.assertEqual(get_file_type("a.c"), "c")
        self.assertEqual(get_file_type("a.h"), "cpp")
        self.assertEqual(get_file_type("Makefile"), "make")
        self.assertEqual(get_file_type("BUILD"), "bazel")
        self.assertEqual(get_file_type("build"), "words")
        self.assertEqual(get_file_type("BUILD.gn"), "gn")
        self.assertEqual(get_file_type("a.md"), "md")

    def test_tabs_to_spaces(self):
        tabs_to_spaces = self.prefs.tabs_to_spaces
        self.assertEqual(tabs_to_spaces("words"), True)
        self.assertEqual(tabs_to_spaces("make"), False)
        self.assertEqual(tabs_to_spaces("cpp"), True)
        self.assertEqual(tabs_to_spaces(None), False)
        self.assertEqual(tabs_to_spaces("foo"), None)
