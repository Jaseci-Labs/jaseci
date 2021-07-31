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
import unittest

from bookmark import Bookmark
from .curses_util import *
from . import fake_curses_testing
from . import prefs
from . import text_buffer
from . import window

kTestFile = "#bookmarks_test_file_with_unlikely_file_name~"


class BookmarkTestCases(fake_curses_testing.FakeCursesTestCase):
    def setUp(self):
        self.prg = ci_program.CiProgram()
        self.fakeHost = window.ViewWindow(self.prg, None)
        self.textBuffer = text_buffer.TextBuffer(self.prg)
        self.textBuffer.lines = 50
        self.lineNumbers = window.LineNumbers(self.prg, self.fakeHost)
        self.lineNumbers.rows = 30
        self.lineNumbers.parent = self.fakeHost
        self.fakeHost.lineNumberColumn = self.lineNumbers
        self.fakeHost.textBuffer = self.textBuffer
        self.fakeHost.scrollRow = self.fakeHost.cursorRow = 0
        fake_curses_testing.FakeCursesTestCase.set_up(self)

    def tearDown(self):
        fake_curses_testing.FakeCursesTestCase.tear_down(self)

    def test_bookmark_comparisons(self):
        b1 = Bookmark(1, 5, {})
        b2 = Bookmark(1, 3, {})
        self.assertTrue(b1 > b2)
        self.assertTrue(b1 >= b2)
        self.assertFalse(b1 < b2)
        self.assertFalse(b1 <= b2)
        self.assertTrue(b2 < b1)
        self.assertTrue(b2 <= b1)
        self.assertFalse(b2 > b1)
        self.assertFalse(b2 >= b1)
        self.assertTrue(b1 != b2)
        self.assertFalse(b1 == b2)
        self.assertFalse(hash(b1) == hash(b2))

        b1 = Bookmark(2, 5, {})
        # b2 = Bookmark(1, 3, {})
        self.assertTrue(b1 > b2)
        self.assertTrue(b1 >= b2)
        self.assertFalse(b1 < b2)
        self.assertFalse(b1 <= b2)
        self.assertTrue(b2 < b1)
        self.assertTrue(b2 <= b1)
        self.assertFalse(b2 > b1)
        self.assertFalse(b2 >= b1)
        self.assertTrue(b1 != b2)
        self.assertFalse(b1 == b2)
        self.assertFalse(hash(b1) == hash(b2))

        # b1 = Bookmark(2, 5, {})
        b2 = Bookmark(1, 10, {})
        self.assertTrue(b1 > b2)
        self.assertTrue(b1 >= b2)
        self.assertFalse(b1 < b2)
        self.assertFalse(b1 <= b2)
        self.assertTrue(b2 < b1)
        self.assertTrue(b2 <= b1)
        self.assertFalse(b2 > b1)
        self.assertFalse(b2 >= b1)
        self.assertTrue(b1 != b2)
        self.assertFalse(b1 == b2)
        self.assertFalse(hash(b1) == hash(b2))

        b1 = Bookmark(1, 10, {})
        # b2 = Bookmark(1, 10, {})
        self.assertFalse(b1 > b2)
        self.assertTrue(b1 >= b2)
        self.assertFalse(b1 < b2)
        self.assertTrue(b1 <= b2)
        self.assertFalse(b2 < b1)
        self.assertTrue(b2 <= b1)
        self.assertFalse(b2 > b1)
        self.assertTrue(b2 >= b1)
        self.assertFalse(b1 != b2)
        self.assertTrue(b1 == b2)
        self.assertTrue(hash(b1) == hash(b2))

        # b1 - Bookmark(1, 10, {})
        b2 = Bookmark(-10, 10, {})
        self.assertTrue(b1 > b2)
        self.assertTrue(b1 >= b2)
        self.assertFalse(b1 < b2)
        self.assertFalse(b1 <= b2)
        self.assertTrue(b2 < b1)
        self.assertTrue(b2 <= b1)
        self.assertFalse(b2 > b1)
        self.assertFalse(b2 >= b1)
        self.assertTrue(b1 != b2)
        self.assertFalse(b1 == b2)
        self.assertFalse(hash(b1) == hash(b2))

    def test_bookmark_contains(self):
        def check_ranges(bookmark):
            """
            Checks that every integer between the bookmark's interval is 'in'
            the bookmark. It also checks if the two integers outside of the
            bookmark's range on both sides of its interval are NOT 'in' the
            bookmark.
            """
            begin = bookmark.begin
            end = bookmark.end
            for i in range(begin, end + 1):
                self.assertTrue(i in bookmark)
            self.assertFalse(begin - 2 in bookmark)
            self.assertFalse(begin - 1 in bookmark)
            self.assertFalse(end + 1 in bookmark)
            self.assertFalse(end + 2 in bookmark)

        check_ranges(Bookmark(1, 5, {}))
        check_ranges(Bookmark(-3, 3, {}))
        check_ranges(Bookmark(-5000, -4990, {}))

        # Check intervals of length 0.
        check_ranges(Bookmark(0, 0, {}))
        check_ranges(Bookmark(5000, 5000, {}))
        check_ranges(Bookmark(-5000, 5000, {}))

        # Floats get cast to int (rounds towards zero).
        b = Bookmark(-3.99, 3.99, {})
        self.assertFalse(-4 in b)
        self.assertTrue(-3 in b)
        self.assertFalse(4 in b)
        self.assertTrue(3 in b)

    def test_bookmark_overlap(self):
        b1 = Bookmark(1, 5, {})
        b2 = Bookmark(1, 5, {})
        self.assertTrue(b1.overlaps(b2))
        self.assertTrue(b2.overlaps(b1))

        b1 = Bookmark(2, 5, {})
        b2 = Bookmark(1, 5, {})
        self.assertTrue(b1.overlaps(b2))
        self.assertTrue(b2.overlaps(b1))

        b1 = Bookmark(1, 3, {})
        b2 = Bookmark(1, 5, {})
        self.assertTrue(b1.overlaps(b2))
        self.assertTrue(b2.overlaps(b1))

        b1 = Bookmark(3, 4, {})
        b2 = Bookmark(1, 5, {})
        self.assertTrue(b1.overlaps(b2))
        self.assertTrue(b2.overlaps(b1))

        b1 = Bookmark(3, 10, {})
        b2 = Bookmark(1, 5, {})
        self.assertTrue(b1.overlaps(b2))
        self.assertTrue(b2.overlaps(b1))

        b1 = Bookmark(5, 10, {})
        b2 = Bookmark(1, 5, {})
        self.assertTrue(b1.overlaps(b2))
        self.assertTrue(b2.overlaps(b1))

        b1 = Bookmark(-5, 0, {})
        b2 = Bookmark(-5, 5, {})
        self.assertTrue(b1.overlaps(b2))
        self.assertTrue(b2.overlaps(b1))

        b1 = Bookmark(0, 0, {})
        b2 = Bookmark(0, 0, {})
        self.assertTrue(b1.overlaps(b2))
        self.assertTrue(b2.overlaps(b1))

        b1 = Bookmark(0, 0, {})
        b2 = Bookmark(-5, 99, {})
        self.assertTrue(b1.overlaps(b2))
        self.assertTrue(b2.overlaps(b1))

        b1 = Bookmark(0, 0, {})
        b2 = Bookmark(-5, -1, {})
        self.assertFalse(b1.overlaps(b2))
        self.assertFalse(b2.overlaps(b1))

        b1 = Bookmark(5, 5, {})
        b2 = Bookmark(6, 9, {})
        self.assertFalse(b1.overlaps(b2))
        self.assertFalse(b2.overlaps(b1))

        b1 = Bookmark(3, 5, {})
        b2 = Bookmark(5, 8, {})
        self.assertTrue(b1.overlaps(b2))
        self.assertTrue(b2.overlaps(b1))

        b1 = Bookmark(-3.999, 3.999, {})  # Rounds to range (-3, 3).
        b2 = Bookmark(-5, -4, {})
        self.assertFalse(b1.overlaps(b2))
        self.assertFalse(b2.overlaps(b1))

        b1 = Bookmark(-3.001, 3.001, {})  # Rounds to range (-3, 3).
        b2 = Bookmark(3.99, 9.0, {})  # Rounds to range (3, 9).
        self.assertTrue(b1.overlaps(b2))
        self.assertTrue(b2.overlaps(b1))

    def test_bookmark_properties(self):
        b = Bookmark(3, 5, {})
        self.assertTrue(b.begin == 3)
        self.assertTrue(b.end == 5)
        self.assertTrue(b.range == (3, 5))

        b = Bookmark(-5.99, 5.99, {})  # Test constructor
        self.assertTrue(b.begin == -5)
        self.assertTrue(b.end == 5)
        self.assertTrue(b.range == (-5, 5))

        b.range = (10, 20)
        self.assertTrue(b.begin == 10)
        self.assertTrue(b.end == 20)
        self.assertTrue(b.range == (10, 20))

        b.range = (20, 10)
        self.assertTrue(b.begin == 10)
        self.assertTrue(b.end == 20)
        self.assertTrue(b.range == (10, 20))

        b.range = (3, 3)
        self.assertTrue(b.begin == 3)
        self.assertTrue(b.end == 3)
        self.assertTrue(b.range == (3, 3))

        b.begin = -3
        self.assertTrue(b.begin == -3)
        self.assertTrue(b.end == 3)
        self.assertTrue(b.range == (-3, 3))

        b.begin = 10
        self.assertTrue(b.begin == 3)
        self.assertTrue(b.end == 10)
        self.assertTrue(b.range == (3, 10))

        b.end = 15
        self.assertTrue(b.begin == 3)
        self.assertTrue(b.end == 15)
        self.assertTrue(b.range == (3, 15))

        b.end = -5
        self.assertTrue(b.begin == -5)
        self.assertTrue(b.end == 3)
        self.assertTrue(b.range == (-5, 3))

        b.begin = 3.9
        self.assertTrue(b.begin == 3)
        self.assertTrue(b.end == 3)
        self.assertTrue(b.range == (3, 3))

        b.end = 2.99
        self.assertTrue(b.begin == 2)
        self.assertTrue(b.end == 3)
        self.assertTrue(b.range == (2, 3))

        b.range = (-9.99, 9.99)
        self.assertTrue(b.begin == -9)
        self.assertTrue(b.end == 9)
        self.assertTrue(b.range == (-9, 9))

    def test_get_next_bookmark_color(self):
        try:
            import mock
        except ImportError:
            startYellow = "\033[93m"
            disableColor = "\033[0m"
            startBlue = "\033[94m"
            exceptionMessage = (
                startYellow
                + "This test could "
                + "not execute because the 'mock' module could not be found. If "
                + "you would like to run this test, please install the mock "
                + "module for python 2.7. You can visit their website at "
                + startBlue
                + "https://pypi.python.org/pypi/mock "
                + startYellow
                + "or you can "
                + "try running "
                + startBlue
                + "pip install mock."
                + disableColor
            )
            # raise Exception(exceptionMessage)
            print(exceptionMessage)
            return

        def test_with_an_x_colored_terminal(x):
            mock.patch.dict(self.prg.prefs.startup, {
                            "numColors": x}, clear=True)
            colors = set()
            expectedNumberOfColors = 5
            for _ in range(expectedNumberOfColors):
                color = self.textBuffer.get_bookmark_color()
                # Make sure that a color index is returned.
                self.assertEqual(type(color), int)
                colors.add(color)
            # Test that all colors were different.
            self.assertEqual(len(colors), expectedNumberOfColors)
            color = self.textBuffer.get_bookmark_color()
            colors.add(color)
            # Test that the function rotates 5 colors.
            self.assertEqual(len(colors), expectedNumberOfColors)

            # Test for 8-colored mode
            test_with_an_x_colored_terminal(8)

            # Test for 256-colored mode
            test_with_an_x_colored_terminal(256)

    def test_get_visible_bookmarks(self):
        # Set up the fake objects to test the LineNumbers methods.
        self.textBuffer.bookmarks = [
            Bookmark(0, 0, {}),
            Bookmark(10, 10, {}),
            Bookmark(20, 20, {}),
            Bookmark(30, 30, {}),
            Bookmark(40, 40, {}),
        ]
        visibleBookmarks = self.lineNumbers.get_visible_bookmarks(
            self.fakeHost.scrollRow, self.fakeHost.scrollRow + self.lineNumbers.rows
        )
        expectedBookmarks = {
            Bookmark(0, 0, {}),
            Bookmark(10, 10, {}),
            Bookmark(20, 20, {}),
        }

        # Check that visibleBookmarks contains all the correct bookmarks
        self.assertEqual(set(visibleBookmarks), expectedBookmarks)
        # Check that the number of bookmarks is the same, as set removes
        # duplicates.
        self.assertEqual(len(visibleBookmarks), len(expectedBookmarks))

        self.fakeHost.scrollRow = 20
        visibleBookmarks = self.lineNumbers.get_visible_bookmarks(
            self.fakeHost.scrollRow, 20 + self.lineNumbers.rows
        )
        expectedBookmarks = {
            Bookmark(20, 20, {}),
            Bookmark(30, 30, {}),
            Bookmark(40, 40, {}),
        }
        self.assertEqual(set(visibleBookmarks), expectedBookmarks)
        self.assertEqual(len(visibleBookmarks), len(expectedBookmarks))

        self.fakeHost.scrollRow = 21
        visibleBookmarks = self.lineNumbers.get_visible_bookmarks(
            self.fakeHost.scrollRow, self.fakeHost.scrollRow + self.lineNumbers.rows
        )
        expectedBookmarks = {Bookmark(30, 30, {}), Bookmark(40, 40, {})}
        self.assertEqual(set(visibleBookmarks), expectedBookmarks)
        self.assertEqual(len(visibleBookmarks), len(expectedBookmarks))

        self.fakeHost.scrollRow = 21
        self.lineNumbers.rows = 10
        visibleBookmarks = self.lineNumbers.get_visible_bookmarks(
            self.fakeHost.scrollRow, self.fakeHost.scrollRow + self.lineNumbers.rows
        )
        expectedBookmarks = {Bookmark(30, 30, {})}
        self.assertEqual(set(visibleBookmarks), expectedBookmarks)
        self.assertEqual(len(visibleBookmarks), len(expectedBookmarks))

        self.lineNumbers.rows = 9
        visibleBookmarks = self.lineNumbers.get_visible_bookmarks(
            self.fakeHost.scrollRow, self.fakeHost.scrollRow + self.lineNumbers.rows
        )
        expectedBookmarks = {}
        self.assertEqual(visibleBookmarks, [])

        self.fakeHost.scrollRow = 10
        self.textBuffer.bookmarks = [
            Bookmark(0, 10, {}),
            Bookmark(11, 29, {}),
            Bookmark(30, 45, {}),
            Bookmark(46, 49, {}),
        ]
        self.lineNumbers.rows = 15
        visibleBookmarks = self.lineNumbers.get_visible_bookmarks(
            self.fakeHost.scrollRow, self.fakeHost.scrollRow + self.lineNumbers.rows
        )
        expectedBookmarks = {Bookmark(0, 10, {}), Bookmark(11, 29, {})}
        self.assertEqual(set(visibleBookmarks), expectedBookmarks)
        self.assertEqual(len(visibleBookmarks), len(expectedBookmarks))

    def test_bookmarks_jump(self):
        # self.set_movie_mode(True)
        self.run_with_test_file(
            kTestFile,
            [
                self.display_check(
                    0,
                    0,
                    [
                        u" ci    _file_with_unlikely_file_name~ . ",
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
                        u"Creating new file  |    1, 1 |   0%,  0%",
                        u"                                        ",
                    ],
                ),
                self.write_text(u"one"),
                CTRL_E,
                "b",
                "m",
                CTRL_J,
                CTRL_J,  # Create bookmark and go to next line.
                CTRL_E,
                "b",
                "m",
                CTRL_J,  # Create bookmark.
                self.write_text(u"two"),
                CTRL_J,
                self.write_text(u"three"),
                CTRL_E,
                "b",
                "m",
                CTRL_J,
                CTRL_J,  # Create bookmark and go to next line.
                self.write_text(u"four"),
                CTRL_J,
                self.write_text(u"five"),
                CTRL_J,
                self.write_text(u"six"),
                CTRL_J,
                self.write_text(u"seven"),
                CTRL_J,
                self.write_text(u"eight"),
                CTRL_J,
                CTRL_E,
                "b",
                "m",
                CTRL_J,  # Create a new bookmark.
                self.write_text(u"nine"),
                CTRL_J,
                self.write_text(u"ten"),
                CTRL_J,
                self.write_text(u"eleven"),
                CTRL_J,
                self.write_text(u"twelve"),
                CTRL_J,
                self.write_text(u"thirteen"),
                CTRL_J,
                self.write_text(u"fourteen"),
                CTRL_J,
                self.write_text(u"fifteen"),
                CTRL_J,
                self.write_text(u"sixteen"),
                CTRL_J,
                self.write_text(u"seventeen"),
                CTRL_J,
                self.write_text(u"eighteen"),
                CTRL_J,
                self.write_text(u"nineteen"),
                CTRL_J,
                self.write_text(u"twenty"),
                CTRL_J,
                self.write_text(u"twenty-one"),
                CTRL_J,
                self.write_text(u"twenty-two"),
                CTRL_J,
                self.write_text(u"twenty-three"),
                CTRL_E,
                "b",
                "m",
                CTRL_J,  # Create a new bookmark.
                # Bookmarks are at positions (1, 4), (2, 1), (3, 6) (9, 1),
                # (23, 13).
                # Note that rows here start at 1, so 1 is the first row.
                self.display_check(
                    0,
                    0,
                    [
                        u" ci    _file_with_unlikely_file_name~ * ",
                        u"                                        ",
                        u"    13 thirteen                         ",
                        u"    14 fourteen                         ",
                        u"    15 fifteen                          ",
                        u"    16 sixteen                          ",
                        u"    17 seventeen                        ",
                        u"    18 eighteen                         ",
                        u"    19 nineteen                         ",
                        u"    20 twenty                           ",
                        u"    21 twenty-one                       ",
                        u"    22 twenty-two                       ",
                        u"    23 twenty-three                     ",
                        u"Added bookmark     |   23,13 |  95%,100%",
                        u"                                        ",
                    ],
                ),
                KEY_F2,  # Jump to the first bookmark (1, 4).
                self.display_check(
                    0,
                    0,
                    [
                        u" ci    _file_with_unlikely_file_name~ * ",
                        u"                                        ",
                        u"     1 one                              ",
                        u"     2 two                              ",
                        u"     3 three                            ",
                        u"     4 four                             ",
                        u"     5 five                             ",
                        u"     6 six                              ",
                        u"     7 seven                            ",
                        u"     8 eight                            ",
                        u"     9 nine                             ",
                        u"    10 ten                              ",
                        u"    11 eleven                           ",
                        u"                        1, 4 |   0%,100%",
                        u"                                        ",
                    ],
                ),
                KEY_F2,  # Jump to the second bookmark (2, 1).
                # The display doesn't move because the bookmark is already in
                # the optimal position.
                self.display_check(
                    0,
                    0,
                    [
                        u" ci    _file_with_unlikely_file_name~ * ",
                        u"                                        ",
                        u"     1 one                              ",
                        u"     2 two                              ",
                        u"     3 three                            ",
                        u"     4 four                             ",
                        u"     5 five                             ",
                        u"     6 six                              ",
                        u"     7 seven                            ",
                        u"     8 eight                            ",
                        u"     9 nine                             ",
                        u"    10 ten                              ",
                        u"    11 eleven                           ",
                        u"                        2, 1 |   4%,  0%",
                        u"                                        ",
                    ],
                ),
                KEY_F2,  # Jump to the third bookmark (3, 6).
                self.display_check(
                    0,
                    0,
                    [
                        u" ci    _file_with_unlikely_file_name~ * ",
                        u"                                        ",
                        u"     1 one                              ",
                        u"     2 two                              ",
                        u"     3 three                            ",
                        u"     4 four                             ",
                        u"     5 five                             ",
                        u"     6 six                              ",
                        u"     7 seven                            ",
                        u"     8 eight                            ",
                        u"     9 nine                             ",
                        u"    10 ten                              ",
                        u"    11 eleven                           ",
                        u"                        3, 6 |   8%,100%",
                        u"                                        ",
                    ],
                ),
                KEY_F2,  # Jump to the third bookmark (9, 6).
                # This moves the bookmark to the optimal scroll position.
                self.display_check(
                    0,
                    0,
                    [
                        u" ci    _file_with_unlikely_file_name~ * ",
                        u"                                        ",
                        u"     7 seven                            ",
                        u"     8 eight                            ",
                        u"     9 nine                             ",
                        u"    10 ten                              ",
                        u"    11 eleven                           ",
                        u"    12 twelve                           ",
                        u"    13 thirteen                         ",
                        u"    14 fourteen                         ",
                        u"    15 fifteen                          ",
                        u"    16 sixteen                          ",
                        u"    17 seventeen                        ",
                        u"                        9, 1 |  34%,  0%",
                        u"                                        ",
                    ],
                ),
                KEY_F2,  # Jump to the fourth bookmark (23, 13).
                # This moves the bookmark to the optimal scroll position.
                self.display_check(
                    0,
                    0,
                    [
                        u" ci    _file_with_unlikely_file_name~ * ",
                        u"                                        ",
                        u"    21 twenty-one                       ",
                        u"    22 twenty-two                       ",
                        u"    23 twenty-three                     ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                       23,13 |  95%,100%",
                        u"                                        ",
                    ],
                ),
                KEY_F2,  # Jump to the first bookmark (1, 4).
                # This moves the bookmark to the optimal scroll position.
                self.display_check(
                    0,
                    0,
                    [
                        u" ci    _file_with_unlikely_file_name~ * ",
                        u"                                        ",
                        u"     1 one                              ",
                        u"     2 two                              ",
                        u"     3 three                            ",
                        u"     4 four                             ",
                        u"     5 five                             ",
                        u"     6 six                              ",
                        u"     7 seven                            ",
                        u"     8 eight                            ",
                        u"     9 nine                             ",
                        u"    10 ten                              ",
                        u"    11 eleven                           ",
                        u"                        1, 4 |   0%,100%",
                        u"                                        ",
                    ],
                ),
                KEY_SHIFT_F2,  # Go back to the fourth bookmark (23, 13).
                # This moves the bookmark to the optimal scroll position.
                self.display_check(
                    0,
                    0,
                    [
                        u" ci    _file_with_unlikely_file_name~ * ",
                        u"                                        ",
                        u"    21 twenty-one                       ",
                        u"    22 twenty-two                       ",
                        u"    23 twenty-three                     ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                                        ",
                        u"                       23,13 |  95%,100%",
                        u"                                        ",
                    ],
                ),
                KEY_SHIFT_F2,  # Go back to the third bookmark (8, 6).
                # This moves the bookmark to the optimal scroll position.
                self.display_check(
                    0,
                    0,
                    [
                        u" ci    _file_with_unlikely_file_name~ * ",
                        u"                                        ",
                        u"     7 seven                            ",
                        u"     8 eight                            ",
                        u"     9 nine                             ",
                        u"    10 ten                              ",
                        u"    11 eleven                           ",
                        u"    12 twelve                           ",
                        u"    13 thirteen                         ",
                        u"    14 fourteen                         ",
                        u"    15 fifteen                          ",
                        u"    16 sixteen                          ",
                        u"    17 seventeen                        ",
                        u"                        9, 1 |  34%,  0%",
                        u"                                        ",
                    ],
                ),
                KEY_SHIFT_F2,  # Go back to the second bookmark (2, 1).
                # This moves the bookmark to the optimal scroll position.
                self.display_check(
                    0,
                    0,
                    [
                        u" ci    _file_with_unlikely_file_name~ * ",
                        u"                                        ",
                        u"     1 one                              ",
                        u"     2 two                              ",
                        u"     3 three                            ",
                        u"     4 four                             ",
                        u"     5 five                             ",
                        u"     6 six                              ",
                        u"     7 seven                            ",
                        u"     8 eight                            ",
                        u"     9 nine                             ",
                        u"    10 ten                              ",
                        u"    11 eleven                           ",
                        u"                        3, 6 |   8%,100%",
                        u"                                        ",
                    ],
                ),
                KEY_SHIFT_F2,  # Go back to the first bookmark (1, 4).
                # The display doesn't move because the bookmark is already in
                # the optimal position.
                self.display_check(
                    0,
                    0,
                    [
                        u" ci    _file_with_unlikely_file_name~ * ",
                        u"                                        ",
                        u"     1 one                              ",
                        u"     2 two                              ",
                        u"     3 three                            ",
                        u"     4 four                             ",
                        u"     5 five                             ",
                        u"     6 six                              ",
                        u"     7 seven                            ",
                        u"     8 eight                            ",
                        u"     9 nine                             ",
                        u"    10 ten                              ",
                        u"    11 eleven                           ",
                        u"                        2, 1 |   4%,  0%",
                        u"                                        ",
                    ],
                ),
                CTRL_Q,
                "n",
            ],
        )
