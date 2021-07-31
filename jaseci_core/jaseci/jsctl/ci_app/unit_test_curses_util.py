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
import unittest
import unicodedata

from . import curses_util


class CursesUtilTestCases(unittest.TestCase):
    def test_curses_key_name(self):
        # These actually test the fake curses.
        def test1():
            curses.keyname(-3)

        self.assertRaises(ValueError, test1)

        def test2():
            curses.keyname([])

        self.assertRaises(TypeError, test2)

        def test3():
            curses.keyname(9 ** 999)

        self.assertRaises(OverflowError, test3)

    def test_rendered_find_iter(self):
        def test(line, startCol, endCol, matches):
            matches.reverse()
            for s, column, length, index in curses_util.rendered_find_iter(
                line, startCol, endCol, (u"[]{}()",), True, True
            ):
                self.assertEqual(matches.pop(), (s, column, length, index))

        # Float and leading zero.
        line = u"""5.32e+30 a 000808"""
        test(
            line,
            0,
            len(line),
            [
                (u"5.32e+30", 0, 8, 1),
                (u"000808", 11, 6, 1),
            ],
        )

        # Parenthesis and number.
        line = u"""(23432ull a"""
        test(
            line,
            0,
            len(line),
            [
                (u"(", 0, 1, 0),
                (u"23432ull", 1, 8, 1),
            ],
        )

        # Multiple numbers and string of brackets.
        line = u"""23 five )}]](23432ull a"""
        test(
            line,
            0,
            len(line),
            [
                (u"23", 0, 2, 1),
                (u")}]](", 8, 5, 0),
                (u"23432ull", 13, 8, 1),
            ],
        )

        # Constrained columns.
        line = u"""23 five )}]](23432ull a"""
        test(
            line,
            1,
            len(line) - 4,
            [
                (u"3", 1, 1, 1),
                (u")}]](", 8, 5, 0),
                (u"23432u", 13, 6, 1),
            ],
        )

    def test_unicode_data(self):
        self.assertEqual(unicodedata.east_asian_width(u"a"), "Na")
        self.assertEqual(unicodedata.east_asian_width(u" "), "Na")
        self.assertEqual(unicodedata.east_asian_width(u"\b"), "N")
        self.assertEqual(unicodedata.east_asian_width(u"こ"), "W")
        # This is "W" in python3 and "F" in python2.
        self.assertIn(unicodedata.east_asian_width(u"⏰"), ("F", "W"))

    def test_column_to_index(self):
        self.assertEqual(0, curses_util.column_to_index(0, u"test"))
        self.assertEqual(1, curses_util.column_to_index(1, u"test"))
        self.assertEqual(2, curses_util.column_to_index(2, u"test"))
        self.assertEqual(3, curses_util.column_to_index(3, u"test"))
        # Test past the length of the string.
        self.assertIs(None, curses_util.column_to_index(4, u"test"))
        self.assertIs(None, curses_util.column_to_index(8, u"test"))

        self.assertEqual(
            0, curses_util.column_to_index(0, u"\ttest\ttabs"))
        self.assertEqual(
            0, curses_util.column_to_index(1, u"\ttest\ttabs"))
        self.assertEqual(
            0, curses_util.column_to_index(2, u"\ttest\ttabs"))
        self.assertEqual(
            0, curses_util.column_to_index(3, u"\ttest\ttabs"))
        self.assertEqual(
            0, curses_util.column_to_index(4, u"\ttest\ttabs"))
        self.assertEqual(
            0, curses_util.column_to_index(5, u"\ttest\ttabs"))
        self.assertEqual(
            0, curses_util.column_to_index(6, u"\ttest\ttabs"))
        self.assertEqual(
            0, curses_util.column_to_index(7, u"\ttest\ttabs"))
        self.assertEqual(
            1, curses_util.column_to_index(8, u"\ttest\ttabs"))
        self.assertEqual(
            2, curses_util.column_to_index(9, u"\ttest\ttabs"))
        self.assertEqual(
            3, curses_util.column_to_index(10, u"\ttest\ttabs"))
        self.assertEqual(
            4, curses_util.column_to_index(11, u"\ttest\ttabs"))
        self.assertEqual(
            5, curses_util.column_to_index(12, u"\ttest\ttabs"))
        self.assertEqual(
            5, curses_util.column_to_index(13, u"\ttest\ttabs"))
        self.assertEqual(
            5, curses_util.column_to_index(14, u"\ttest\ttabs"))
        self.assertEqual(
            5, curses_util.column_to_index(15, u"\ttest\ttabs"))
        self.assertEqual(
            6, curses_util.column_to_index(16, u"\ttest\ttabs"))
        self.assertEqual(
            7, curses_util.column_to_index(17, u"\ttest\ttabs"))
        self.assertEqual(
            8, curses_util.column_to_index(18, u"\ttest\ttabs"))
        # Test past the length of the string.
        self.assertIs(None, curses_util.column_to_index(
            21, u"\ttest\ttabs"))
        self.assertIs(None, curses_util.column_to_index(
            22, u"\ttest\ttabs"))
        self.assertIs(None, curses_util.column_to_index(
            999, u"\ttest\ttabs"))

        self.assertEqual(0, curses_util.column_to_index(0, u"こんにちは"))
        self.assertEqual(0, curses_util.column_to_index(1, u"こんにちは"))
        self.assertEqual(1, curses_util.column_to_index(2, u"こんにちは"))
        self.assertEqual(1, curses_util.column_to_index(3, u"こんにちは"))
        self.assertEqual(2, curses_util.column_to_index(4, u"こんにちは"))
        self.assertEqual(4, curses_util.column_to_index(8, u"こんにちは"))
        self.assertEqual(4, curses_util.column_to_index(9, u"こんにちは"))
        # Test past the length of the string.
        self.assertIs(None, curses_util.column_to_index(10, u"こんにちは"))
        self.assertIs(None, curses_util.column_to_index(11, u"こんにちは"))
        self.assertIs(None, curses_util.column_to_index(12, u"こんにちは"))

    def test_char_at_column(self):
        cu = curses_util
        self.assertEqual(u"t", cu.char_at_column(0, u"test"))
        self.assertEqual(u"e", cu.char_at_column(1, u"test"))
        self.assertEqual(u"s", cu.char_at_column(2, u"test"))
        self.assertEqual(u"t", cu.char_at_column(3, u"test"))
        # Test past the length of the string.
        self.assertIs(None, cu.char_at_column(4, u"test"))
        self.assertIs(None, cu.char_at_column(8, u"test"))

        self.assertEqual(u"\t", cu.char_at_column(0, u"\ttest\ttabs"))
        self.assertEqual(u"\t", cu.char_at_column(1, u"\ttest\ttabs"))
        self.assertEqual(u"\t", cu.char_at_column(2, u"\ttest\ttabs"))
        self.assertEqual(u"\t", cu.char_at_column(3, u"\ttest\ttabs"))
        self.assertEqual(u"\t", cu.char_at_column(4, u"\ttest\ttabs"))
        self.assertEqual(u"\t", cu.char_at_column(5, u"\ttest\ttabs"))
        self.assertEqual(u"\t", cu.char_at_column(6, u"\ttest\ttabs"))
        self.assertEqual(u"\t", cu.char_at_column(7, u"\ttest\ttabs"))
        self.assertEqual(u"t", cu.char_at_column(8, u"\ttest\ttabs"))
        self.assertEqual(u"e", cu.char_at_column(9, u"\ttest\ttabs"))
        self.assertEqual(u"s", cu.char_at_column(10, u"\ttest\ttabs"))
        self.assertEqual(u"t", cu.char_at_column(11, u"\ttest\ttabs"))
        self.assertEqual(u"\t", cu.char_at_column(12, u"\ttest\ttabs"))
        self.assertEqual(u"\t", cu.char_at_column(13, u"\ttest\ttabs"))
        self.assertEqual(u"\t", cu.char_at_column(14, u"\ttest\ttabs"))
        self.assertEqual(u"\t", cu.char_at_column(15, u"\ttest\ttabs"))
        self.assertEqual(u"t", cu.char_at_column(16, u"\ttest\ttabs"))
        self.assertEqual(u"a", cu.char_at_column(17, u"\ttest\ttabs"))
        self.assertEqual(u"b", cu.char_at_column(18, u"\ttest\ttabs"))
        self.assertEqual(u"s", cu.char_at_column(19, u"\ttest\ttabs"))
        # Test past the length of the string.
        self.assertIs(None, cu.char_at_column(20, u"\ttest\ttabs"))
        self.assertIs(None, cu.char_at_column(21, u"\ttest\ttabs"))
        self.assertIs(None, cu.char_at_column(999, u"\ttest\ttabs"))

        self.assertEqual(u"こ", cu.char_at_column(0, u"こんにちは"))
        self.assertEqual(u"こ", cu.char_at_column(1, u"こんにちは"))
        self.assertEqual(u"ん", cu.char_at_column(2, u"こんにちは"))
        self.assertEqual(u"ん", cu.char_at_column(3, u"こんにちは"))
        self.assertEqual(u"に", cu.char_at_column(4, u"こんにちは"))
        self.assertEqual(u"は", cu.char_at_column(8, u"こんにちは"))
        self.assertEqual(u"は", cu.char_at_column(9, u"こんにちは"))
        # Test past the length of the string.
        self.assertIs(None, cu.char_at_column(10, u"こんにちは"))
        self.assertIs(None, cu.char_at_column(11, u"こんにちは"))
        self.assertIs(None, cu.char_at_column(12, u"こんにちは"))

    def test_fit_to_rendered_width(self):
        fit_to_rendered_width = curses_util.fit_to_rendered_width

        self.assertEqual(0, fit_to_rendered_width(0, 0, u"test"))
        self.assertEqual(1, fit_to_rendered_width(0, 1, u"test"))
        self.assertEqual(2, fit_to_rendered_width(0, 2, u"test"))
        self.assertEqual(3, fit_to_rendered_width(0, 3, u"test"))
        self.assertEqual(4, fit_to_rendered_width(0, 4, u"test"))
        # Test past the length of the string.
        self.assertEqual(4, fit_to_rendered_width(0, 8, u"test"))

        # Test double wide characters (theses characters render as two cells in
        # a fixed width font).
        self.assertEqual(0, fit_to_rendered_width(0, 0, u"こんにちは"))
        self.assertEqual(0, fit_to_rendered_width(0, 1, u"こんにちは"))
        self.assertEqual(1, fit_to_rendered_width(0, 2, u"こんにちは"))
        self.assertEqual(1, fit_to_rendered_width(0, 3, u"こんにちは"))
        self.assertEqual(2, fit_to_rendered_width(0, 4, u"こんにちは"))
        self.assertEqual(4, fit_to_rendered_width(0, 8, u"こんにちは"))
        self.assertEqual(4, fit_to_rendered_width(0, 9, u"こんにちは"))
        self.assertEqual(5, fit_to_rendered_width(0, 10, u"こんにちは"))

        # Test past the length of the string.
        self.assertEqual(5, fit_to_rendered_width(0, 11, u"こんにちは"))
        self.assertEqual(5, fit_to_rendered_width(0, 12, u"こんにちは"))

        # Test tabs.
        self.assertEqual(1, fit_to_rendered_width(0, 8, u"\t"))
        self.assertEqual(0, fit_to_rendered_width(0, 7, u"\t"))

    def test_rendered_sub_str(self):
        self.assertEqual(u"test", curses_util.rendered_sub_str(u"test", 0))
        self.assertEqual(
            u"test", curses_util.rendered_sub_str(u"test", 0, 4))
        self.assertEqual(
            u"est", curses_util.rendered_sub_str(u"test", 1, 4))
        self.assertEqual(
            u"st", curses_util.rendered_sub_str(u"test", 2, 4))
        self.assertEqual(u"t", curses_util.rendered_sub_str(u"test", 3, 4))
        self.assertEqual(u"", curses_util.rendered_sub_str(u"test", 4, 4))
        self.assertEqual(
            u"tes", curses_util.rendered_sub_str(u"test", 0, 3))
        self.assertEqual(
            u"te", curses_util.rendered_sub_str(u"test", 0, 2))
        self.assertEqual(u"t", curses_util.rendered_sub_str(u"test", 0, 1))
        self.assertEqual(u"", curses_util.rendered_sub_str(u"test", 0, 0))
        self.assertEqual(
            u"es", curses_util.rendered_sub_str(u"test", 1, 3))
        self.assertEqual(u"", curses_util.rendered_sub_str(u"test", 2, 2))
        self.assertEqual(
            u"eight", curses_util.rendered_sub_str(u"eight", 0, 5))
        self.assertEqual(
            u"igh", curses_util.rendered_sub_str(u"eight", 1, 4))
        self.assertEqual(
            u"g", curses_util.rendered_sub_str(u"eight", 2, 3))
        self.assertEqual(u"", curses_util.rendered_sub_str(u"eight", 3, 3))
        self.assertEqual(
            u"こんにちは", curses_util.rendered_sub_str(u"こんにちは", 0, 10))
        self.assertEqual(
            u" んにちは", curses_util.rendered_sub_str(u"こんにちは", 1, 10))
        self.assertEqual(
            u"んにちは", curses_util.rendered_sub_str(u"こんにちは", 2, 10))
        self.assertEqual(
            u" にちは", curses_util.rendered_sub_str(u"こんにちは", 3, 10))
        self.assertEqual(
            u"にちは", curses_util.rendered_sub_str(u"こんにちは", 4, 10))
        self.assertEqual(u"は", curses_util.rendered_sub_str(u"こんにちは", 8))
        self.assertEqual(
            u"は", curses_util.rendered_sub_str(u"こんにちは", 8, 10))
        self.assertEqual(
            u" ", curses_util.rendered_sub_str(u"こんにちは", 9, 10))
        self.assertEqual(
            u"", curses_util.rendered_sub_str(u"こんにちは", 10, 10))
        self.assertEqual(
            u"こんにち ", curses_util.rendered_sub_str(u"こんにちは", 0, 9))
        self.assertEqual(
            u"こんにち", curses_util.rendered_sub_str(u"こんにちは", 0, 8))
        self.assertEqual(
            u"こんに ", curses_util.rendered_sub_str(u"こんにちは", 0, 7))
        self.assertEqual(
            u"こんに", curses_util.rendered_sub_str(u"こんにちは", 0, 6))
        self.assertEqual(
            u"こん ", curses_util.rendered_sub_str(u"こんにちは", 0, 5))
        self.assertEqual(
            u"こん", curses_util.rendered_sub_str(u"こんにちは", 0, 4))
        self.assertEqual(
            u"こ ", curses_util.rendered_sub_str(u"こんにちは", 0, 3))
        self.assertEqual(
            u"こ", curses_util.rendered_sub_str(u"こんにちは", 0, 2))
        self.assertEqual(
            u" ", curses_util.rendered_sub_str(u"こんにちは", 0, 1))
        self.assertEqual(u"", curses_util.rendered_sub_str(u"こんにちは", 0, 0))

        # Test past the length of the string.
        self.assertEqual(u"", curses_util.rendered_sub_str(u"", 1, 1))
        self.assertEqual(
            u"test", curses_util.rendered_sub_str(u"test", 0, 8))

        # Test with tabs.
        self.assertEqual(
            u"   ", curses_util.rendered_sub_str(u"\tこんにちは", 0, 3))
        self.assertEqual(
            u"     こ", curses_util.rendered_sub_str(u"\tこんにちは", 3, 10))
        self.assertEqual(
            u"        こん", curses_util.rendered_sub_str(u"\tこんにちは", 0, 12)
        )
        self.assertEqual(
            u"        <tab", curses_util.rendered_sub_str(
                u"\t<tab", 0, None)
        )
        self.assertEqual(
            u"         <tab+space",
            curses_util.rendered_sub_str(u"\t <tab+space", 0, None),
        )
        self.assertEqual(
            u"        <space+tab",
            curses_util.rendered_sub_str(u" \t<space+tab", 0, None),
        )
        self.assertEqual(
            u"a       <", curses_util.rendered_sub_str(u"a\t<", 0, None)
        )
        self.assertEqual(
            u"some text.>     <",
            curses_util.rendered_sub_str(u"some text.>\t<", 0, None),
        )
        self.assertEqual(
            u"                <2tabs",
            curses_util.rendered_sub_str(u"\t\t<2tabs", 0, None),
        )
        self.assertEqual(
            u"line    with    tabs",
            curses_util.rendered_sub_str(u"line\twith\ttabs", 0, None),
        )
        self.assertEqual(
            u"ends with tab>  ",
            curses_util.rendered_sub_str(u"ends with tab>\t", 0, None),
        )

    def test_rendered_width(self):
        self.assertEqual(0, curses_util.column_width(u""))
        self.assertEqual(4, curses_util.column_width(u"test"))
        self.assertEqual(8, curses_util.column_width(u"\t"))
        self.assertEqual(9, curses_util.column_width(u"\ta"))
        self.assertEqual(16, curses_util.column_width(u"\ta\t"))
        self.assertEqual(8, curses_util.column_width(u"i\t"))

        self.assertEqual(2, curses_util.column_width(u"こ"))
        self.assertEqual(4, curses_util.column_width(u"こん"))
        self.assertEqual(6, curses_util.column_width(u"こんに"))
        self.assertEqual(10, curses_util.column_width(u"こんにちは"))

        self.assertEqual(3, curses_util.column_width(u"aこ"))
        self.assertEqual(5, curses_util.column_width(u"aこん"))
        self.assertEqual(3, curses_util.column_width(u"こc"))
        self.assertEqual(4, curses_util.column_width(u"aこc"))
        self.assertEqual(7, curses_util.column_width(u"aこbんc"))

    def test_char_width(self):
        self.assertEqual(0, curses_util.char_width(u"", 0))
        self.assertEqual(8, curses_util.char_width(u"\t", 0))
        self.assertEqual(1, curses_util.char_width(u" ", 0))
        self.assertEqual(7, curses_util.char_width(u"\t", 1))
        self.assertEqual(6, curses_util.char_width(u"\t", 2))
        self.assertEqual(2, curses_util.char_width(u"\t", 6))
        self.assertEqual(1, curses_util.char_width(u"\t", 7))
        self.assertEqual(0, curses_util.char_width(u"", 8))
        self.assertEqual(8, curses_util.char_width(u"\t", 8))
        self.assertEqual(7, curses_util.char_width(u"\t", 9))
        self.assertEqual(2, curses_util.char_width(u"こ", 0))
        self.assertEqual(0, curses_util.char_width(u"\b", 0))
        self.assertEqual(0, curses_util.char_width(u"\n", 0))
        self.assertEqual(2, curses_util.char_width(u"⏰", 0))

    def test_floor_col(self):
        test = u"""\tfive\t"""
        floor_col = curses_util.floor_col
        self.assertEqual(0, floor_col(0, test))
        self.assertEqual(0, floor_col(1, test))
        self.assertEqual(0, floor_col(2, test))
        self.assertEqual(0, floor_col(3, test))
        self.assertEqual(0, floor_col(4, test))
        self.assertEqual(0, floor_col(5, test))
        self.assertEqual(0, floor_col(6, test))
        self.assertEqual(0, floor_col(7, test))
        self.assertEqual(8, floor_col(8, test))
        self.assertEqual(9, floor_col(9, test))
        self.assertEqual(10, floor_col(10, test))
        self.assertEqual(11, floor_col(11, test))
        self.assertEqual(12, floor_col(12, test))
        self.assertEqual(12, floor_col(13, test))
        self.assertEqual(12, floor_col(14, test))
        self.assertEqual(12, floor_col(15, test))
        self.assertEqual(16, floor_col(16, test))
        self.assertEqual(16, floor_col(17, test))
        self.assertEqual(16, floor_col(99, test))

        test2 = u"""more testing"""
        self.assertEqual(0, floor_col(0, test2))
        self.assertEqual(2, floor_col(2, test2))
        self.assertEqual(12, floor_col(99, test2))

    def test_prior_char_col(self):
        test = u"""\tfive\t"""
        prior_char_col = curses_util.prior_char_col
        self.assertEqual(None, prior_char_col(0, test))
        self.assertEqual(0, prior_char_col(1, test))
        self.assertEqual(0, prior_char_col(2, test))
        self.assertEqual(0, prior_char_col(3, test))
        self.assertEqual(0, prior_char_col(4, test))
        self.assertEqual(0, prior_char_col(5, test))
        self.assertEqual(0, prior_char_col(6, test))
        self.assertEqual(0, prior_char_col(7, test))
        self.assertEqual(0, prior_char_col(8, test))
        self.assertEqual(8, prior_char_col(9, test))
        self.assertEqual(9, prior_char_col(10, test))
        self.assertEqual(10, prior_char_col(11, test))
        self.assertEqual(11, prior_char_col(12, test))
        self.assertEqual(12, prior_char_col(13, test))
        self.assertEqual(12, prior_char_col(14, test))
        self.assertEqual(12, prior_char_col(15, test))
        self.assertEqual(12, prior_char_col(16, test))
        self.assertEqual(None, prior_char_col(17, test))

        test2 = u"""more testing"""
        self.assertEqual(None, prior_char_col(0, test2))
        self.assertEqual(1, prior_char_col(2, test2))
        self.assertEqual(11, prior_char_col(12, test2))
        self.assertEqual(None, prior_char_col(13, test2))
