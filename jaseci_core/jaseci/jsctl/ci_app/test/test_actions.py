# Copyright 2016 Google Inc.
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
import unittest
from jaseci.utils.utils import TestCaseHelper

from .. import ci_program, log
from .. import text_buffer, selectable


class FakeCursorWindow:
    def getmaxyx(self):
        return (100, 100)


class FakeView:
    def __init__(self):
        self.cursorWindow = FakeCursorWindow()
        self.top = 0
        self.left = 0
        self.rows = 10
        self.cols = 100
        self.scrollRow = 0
        self.scrollCol = 0


def check_row(test, text_buffer, row, expected):
    text_buffer.parse_document()
    if not (expected == text_buffer.parser.row_text(row)):
        test.fail(
            "\n\nExpected these to match: "
            "row {}: expected {}, parser {}".format(
                row, repr(expected), repr(text_buffer.parser.data)
            )
        )


class ActionsTestCase(TestCaseHelper, unittest.TestCase):
    def current_row_text(self):
        return self.textBuffer.parser.row_text(self.textBuffer.penRow)

    def set_marker_pen_row_col(self, mRow, mCol, row, col):
        self.assertTrue(isinstance(mRow, int))
        self.assertTrue(isinstance(mCol, int))
        self.assertTrue(isinstance(row, int))
        self.assertTrue(isinstance(col, int))
        self.assertTrue(hasattr(self.textBuffer, "markerRow"))
        self.assertTrue(hasattr(self.textBuffer, "markerCol"))
        self.assertTrue(hasattr(self.textBuffer, "penRow"))
        self.assertTrue(hasattr(self.textBuffer, "penCol"))
        self.assertTrue(hasattr(self.textBuffer, "goalCol"))
        self.textBuffer.markerRow = mRow
        self.textBuffer.markerCol = mCol
        self.textBuffer.penRow = row
        self.textBuffer.penCol = col
        self.textBuffer.goalCol = col

    def marker_pen_row_col(self):
        return (
            self.textBuffer.markerRow,
            self.textBuffer.markerCol,
            self.textBuffer.penRow,
            self.textBuffer.penCol,
        )


class MouseTestCases(ActionsTestCase):
    def setUp(self):
        TestCaseHelper.setUp(self)
        log.shouldWritePrintLog = False
        self.prg = ci_program.CiProgram()
        self.textBuffer = text_buffer.TextBuffer(self.prg)
        self.textBuffer.set_view(FakeView())
        test = """/* first comment */
two
// second comment
apple banana carrot
#include "test.h"
void blah();
"""
        self.textBuffer.insert_lines(tuple(test.split("\n")))
        self.textBuffer.parse_document()
        # self.assertEqual(self.textBuffer.scrollRow, 0)
        # self.assertEqual(self.textBuffer.scrollCol, 0)
        self.assertEqual(self.textBuffer.parser.row_text(1), "two")

    def tearDown(self):
        self.textBuffer = None
        TestCaseHelper.tearDown(self)

    def test_mouse_selection(self):
        self.textBuffer.mouse_click(3, 9, False, False, False)
        self.assertEqual(self.textBuffer.penRow, 3)
        self.assertEqual(self.textBuffer.penCol, 9)

        self.textBuffer.mouse_click(3, 8, True, False, False)
        self.assertEqual(self.marker_pen_row_col(), (3, 9, 3, 8))

        self.textBuffer.mouse_click(4, 8, True, False, False)
        self.assertEqual(self.marker_pen_row_col(), (3, 9, 4, 8))

        self.textBuffer.mouse_click(3, 8, True, False, False)
        self.assertEqual(self.marker_pen_row_col(), (3, 9, 3, 8))

        self.textBuffer.mouse_click(4, 8, True, False, False)
        self.textBuffer.mouse_click(4, 9, True, False, False)
        self.assertEqual(self.marker_pen_row_col(), (3, 9, 4, 9))

        self.textBuffer.mouse_click(4, 10, True, False, False)
        self.assertEqual(self.marker_pen_row_col(), (3, 9, 4, 10))

        self.textBuffer.mouse_click(4, 11, True, False, False)
        self.assertEqual(self.marker_pen_row_col(), (3, 9, 4, 11))

    def test_mouse_word_selection(self):
        # self.assertEqual(self.textBuffer.scrollCol, 0)
        self.textBuffer.selection_word()
        # self.assertEqual(self.textBuffer.scrollCol, 0)
        row = 3
        col = 9
        wordBegin = 6
        wordEnd = 12
        self.textBuffer.mouse_click(row, col, False, False, False)
        self.assertEqual(self.textBuffer.penRow, row)
        self.assertEqual(self.textBuffer.penCol, col)

        self.textBuffer.mouse_double_click(row, col - 1, False, False, False)
        self.assertEqual(self.textBuffer.markerRow, row)
        self.assertEqual(self.textBuffer.markerCol, wordBegin)
        self.assertEqual(self.textBuffer.penRow, row)
        self.assertEqual(self.textBuffer.penCol, wordEnd)

        self.textBuffer.mouse_moved(row, wordBegin, False, False, False)
        self.assertEqual(self.textBuffer.markerRow, row)
        self.assertEqual(self.textBuffer.markerCol, wordBegin)
        self.assertEqual(self.textBuffer.penRow, row)
        self.assertEqual(self.textBuffer.penCol, wordEnd)

        self.textBuffer.mouse_moved(row, wordBegin - 1, False, False, False)
        self.assertEqual(self.textBuffer.markerRow, row)
        self.assertEqual(self.textBuffer.penCol, 0)
        self.assertEqual(self.textBuffer.markerCol, wordEnd)
        self.assertEqual(self.textBuffer.penRow, row)
        self.assertEqual(self.textBuffer.penCol, 0)

        self.textBuffer.mouse_moved(row, 1, False, False, False)
        self.assertEqual(self.textBuffer.markerRow, row)
        self.assertEqual(self.textBuffer.markerCol, wordEnd)
        self.assertEqual(self.textBuffer.penRow, row)
        self.assertEqual(self.textBuffer.penCol, 0)

        self.textBuffer.mouse_moved(row + 1, 0, False, False, False)
        self.assertEqual(self.textBuffer.markerRow, row)
        self.assertEqual(self.textBuffer.markerCol, wordBegin)
        self.assertEqual(self.textBuffer.penRow, row + 1)
        self.assertEqual(self.textBuffer.penCol, 1)

        self.textBuffer.mouse_moved(row + 1, 1, False, False, False)
        self.assertEqual(self.textBuffer.markerRow, row)
        self.assertEqual(self.textBuffer.markerCol, wordBegin)
        self.assertEqual(self.textBuffer.penRow, row + 1)
        self.assertEqual(self.textBuffer.penCol, 8)

        self.textBuffer.mouse_moved(row, 1, False, False, False)
        self.assertEqual(self.textBuffer.markerRow, row)
        self.assertEqual(self.textBuffer.markerCol, wordEnd)
        self.assertEqual(self.textBuffer.penRow, row)
        self.assertEqual(self.textBuffer.penCol, 0)


class SelectionTestCases(ActionsTestCase):
    def setUp(self):
        TestCaseHelper.setUp(self)
        log.shouldWritePrintLog = False
        self.prg = ci_program.CiProgram()
        self.textBuffer = text_buffer.TextBuffer(self.prg)
        self.textBuffer.set_view(FakeView())
        test = """/* first comment */
two
// second comment
apple banana carrot
#include "test.h"
void blah();
\ta\t
a\twith tab
\t\t
\twhile
{
"""
        self.textBuffer.set_file_type(u"text")
        self.textBuffer.insert_lines(tuple(test.split("\n")))
        self.textBuffer.parse_document()
        # self.textBuffer.parser.debug_log(print, test)
        # self.assertEqual(self.textBuffer.scrollRow, 0)
        # self.assertEqual(self.textBuffer.scrollCol, 0)
        self.assertEqual(self.textBuffer.parser.row_text(1), "two")
        self.assertEqual(
            self.textBuffer.parser.row_text_and_width(8), ("\t\t", 16))

    def test_cursor_col_delta(self):
        self.set_marker_pen_row_col(0, 0, 0, 2)
        self.assertEqual(self.textBuffer.cursor_col_delta(4), 0)
        self.assertEqual(self.textBuffer.cursor_col_delta(6), -2)
        self.set_marker_pen_row_col(0, 0, 0, 12)
        self.assertEqual(self.textBuffer.cursor_col_delta(4), 0)
        self.assertEqual(self.textBuffer.cursor_col_delta(6), -3)

    def test_cursor_move(self):
        self.set_marker_pen_row_col(0, 0, 2, 5)
        self.assertEqual(self.current_row_text(), u"// second comment")
        self.textBuffer.cursor_move_left()
        self.assertEqual(self.marker_pen_row_col(), (0, 0, 2, 4))
        self.textBuffer.cursor_move_right()
        self.assertEqual(self.marker_pen_row_col(), (0, 0, 2, 5))

        self.set_marker_pen_row_col(0, 0, 8, 16)
        self.assertEqual(self.current_row_text(), u"\t\t")
        self.textBuffer.cursor_move_left()
        self.assertEqual(self.marker_pen_row_col(), (0, 0, 8, 8))
        self.textBuffer.cursor_move_left()
        self.assertEqual(self.marker_pen_row_col(), (0, 0, 8, 0))
        self.textBuffer.cursor_move_left()
        self.assertEqual(self.current_row_text(), u"a\twith tab")
        self.assertEqual(self.marker_pen_row_col(), (0, 0, 7, 16))
        self.textBuffer.cursor_move_right()
        self.assertEqual(self.current_row_text(), u"\t\t")
        self.assertEqual(self.marker_pen_row_col(), (0, 0, 8, 0))
        self.textBuffer.cursor_move_right()
        self.assertEqual(self.marker_pen_row_col(), (0, 0, 8, 8))
        self.textBuffer.cursor_move_right()
        self.assertEqual(self.marker_pen_row_col(), (0, 0, 8, 16))
        self.textBuffer.cursor_move_right()
        self.assertEqual(self.current_row_text(), u"\twhile")
        self.assertEqual(self.marker_pen_row_col(), (0, 0, 9, 0))
        self.textBuffer.cursor_move_right()
        self.assertEqual(self.marker_pen_row_col(), (0, 0, 9, 8))
        self.textBuffer.cursor_move_right()
        self.assertEqual(self.marker_pen_row_col(), (0, 0, 9, 9))
        self.textBuffer.cursor_move_right()
        self.assertEqual(self.marker_pen_row_col(), (0, 0, 9, 10))
        self.textBuffer.cursor_move_up_or_begin()
        self.assertEqual(self.current_row_text(), u"\t\t")
        self.assertEqual(self.marker_pen_row_col(), (0, 0, 8, 8))
        self.textBuffer.cursor_move_up_or_begin()
        self.assertEqual(self.current_row_text(), u"a\twith tab")
        # The column is 10 because of the prior move right which set goalCol.
        self.assertEqual(self.marker_pen_row_col(), (0, 0, 7, 10))
        self.textBuffer.cursor_move_left()
        self.assertEqual(self.marker_pen_row_col(), (0, 0, 7, 9))
        self.textBuffer.cursor_move_left()
        self.assertEqual(self.marker_pen_row_col(), (0, 0, 7, 8))
        self.textBuffer.cursor_move_left()
        self.assertEqual(self.marker_pen_row_col(), (0, 0, 7, 1))
        self.textBuffer.cursor_move_down_or_end()
        self.assertEqual(self.current_row_text(), u"\t\t")
        self.assertEqual(self.marker_pen_row_col(), (0, 0, 8, 0))

    def test_backspace(self):
        self.set_marker_pen_row_col(0, 0, 6, 8)
        self.assertEqual(self.current_row_text(), u"\ta\t")
        self.textBuffer.backspace()
        self.textBuffer.parse_document()
        self.assertEqual(self.marker_pen_row_col(), (0, 0, 6, 0))
        self.assertEqual(self.current_row_text(), u"a\t")
        self.textBuffer.cursor_move_right()
        self.assertEqual(self.marker_pen_row_col(), (0, 0, 6, 1))

    def test_cursor_select_word_left(self):
        tb = self.textBuffer
        self.set_marker_pen_row_col(0, 0, 2, 5)

        self.assertEqual(self.current_row_text(), u"// second comment")
        self.textBuffer.cursor_select_word_left()
        self.assertEqual(self.marker_pen_row_col(), (2, 5, 2, 3))

        self.textBuffer.cursor_select_word_left()
        self.assertEqual(self.marker_pen_row_col(), (2, 5, 2, 0))

        self.textBuffer.cursor_select_word_left()
        self.assertEqual(self.marker_pen_row_col(), (2, 5, 1, 3))

        self.textBuffer.cursor_select_word_left()
        self.assertEqual(self.marker_pen_row_col(), (2, 5, 1, 0))

        self.textBuffer.cursor_select_word_left()
        self.assertEqual(self.marker_pen_row_col(), (2, 5, 0, 19))

        self.textBuffer.cursor_select_word_left()
        self.assertEqual(self.marker_pen_row_col(), (2, 5, 0, 16))

        self.textBuffer.cursor_select_word_left()
        self.assertEqual(self.marker_pen_row_col(), (2, 5, 0, 9))

        self.textBuffer.cursor_select_word_left()
        self.assertEqual(self.marker_pen_row_col(), (2, 5, 0, 8))

        self.textBuffer.cursor_select_word_left()
        self.assertEqual(self.marker_pen_row_col(), (2, 5, 0, 3))

        self.textBuffer.cursor_select_word_left()
        self.assertEqual(self.marker_pen_row_col(), (2, 5, 0, 0))

        # Top of document. This call should have no effect (and not crash).
        self.textBuffer.cursor_select_word_left()
        self.assertEqual(self.marker_pen_row_col(), (2, 5, 0, 0))


class TextIndentTestCases(ActionsTestCase):
    def setUp(self):
        TestCaseHelper.setUp(self)
        log.shouldWritePrintLog = False
        self.prg = ci_program.CiProgram()
        self.textBuffer = text_buffer.TextBuffer(self.prg)
        self.textBuffer.set_view(FakeView())
        # self.assertEqual(self.textBuffer.scrollRow, 0)
        # self.assertEqual(self.textBuffer.scrollCol, 0)

    def tearDown(self):
        self.textBuffer = None
        TestCaseHelper.tearDown(self)

    def test_auto_indent(self):
        self.prg.prefs.editor["autoInsertClosingCharacter"] = False

        def insert(*args):
            self.textBuffer.insert_printable_with_pairing(*args)
            self.textBuffer.parse_document()

        tb = self.textBuffer
        self.assertEqual(tb.parser.row_count(), 1)
        insert(ord("a"), None)
        insert(ord(":"), None)
        self.assertEqual(tb.penRow, 0)
        tb.carriage_return()
        self.assertEqual(tb.penRow, 1)
        check_row(self, tb, 0, "a:")
        check_row(self, tb, 1, "")

        # Replace member function to return a grammar with and indent.
        def grammar_at(row, col):
            return {"indent": "  "}

        tb.parser.grammar_at = grammar_at
        tb.backspace()
        tb.carriage_return()
        check_row(self, tb, 0, "a:")
        check_row(self, tb, 1, "  ")
        insert(ord("b"), None)
        insert(ord(":"), None)
        tb.carriage_return()
        insert(ord("c"), None)
        insert(ord(":"), None)
        tb.carriage_return()
        check_row(self, tb, 0, "a:")
        check_row(self, tb, 1, "  b:")
        check_row(self, tb, 2, "    c:")

    def test_indent_unindent_lines(self):
        def insert(*args):
            self.textBuffer.insert_printable_with_pairing(*args)
            self.textBuffer.parse_document()

        tb = self.textBuffer
        self.assertEqual(tb.parser.row_count(), 1)
        insert(ord("a"), None)
        tb.carriage_return()
        insert(ord("b"), None)
        tb.carriage_return()
        insert(ord("c"), None)
        tb.carriage_return()
        insert(ord("d"), None)
        tb.carriage_return()
        check_row(self, tb, 0, "a")
        check_row(self, tb, 1, "b")
        check_row(self, tb, 2, "c")
        check_row(self, tb, 3, "d")
        tb.penRow = 1
        tb.markerRow = 2
        tb.indent_lines()
        check_row(self, tb, 0, "a")
        check_row(self, tb, 1, "  b")
        check_row(self, tb, 2, "  c")
        check_row(self, tb, 3, "d")
        tb.penRow = 0
        tb.markerRow = 3
        tb.indent_lines()
        check_row(self, tb, 0, "  a")
        check_row(self, tb, 1, "    b")
        check_row(self, tb, 2, "    c")
        check_row(self, tb, 3, "  d")
        tb.unindent_lines()
        check_row(self, tb, 0, "a")
        check_row(self, tb, 1, "  b")
        check_row(self, tb, 2, "  c")
        check_row(self, tb, 3, "d")
        tb.unindent_lines()
        check_row(self, tb, 0, "a")
        check_row(self, tb, 1, "b")
        check_row(self, tb, 2, "c")
        check_row(self, tb, 3, "d")
        tb.penRow = 1
        tb.markerRow = 1
        tb.indent_lines()
        check_row(self, tb, 0, "a")
        check_row(self, tb, 1, "  b")
        check_row(self, tb, 2, "c")
        check_row(self, tb, 3, "d")
        tb.indent_lines()
        check_row(self, tb, 0, "a")
        check_row(self, tb, 1, "    b")
        check_row(self, tb, 2, "c")
        check_row(self, tb, 3, "d")
        tb.unindent_lines()
        check_row(self, tb, 0, "a")
        check_row(self, tb, 1, "  b")
        check_row(self, tb, 2, "c")
        check_row(self, tb, 3, "d")
        tb.penRow = 3
        tb.markerRow = 3
        tb.indent_lines()
        check_row(self, tb, 0, "a")
        check_row(self, tb, 1, "  b")
        check_row(self, tb, 2, "c")
        check_row(self, tb, 3, "  d")
        tb.penRow = 0
        tb.markerRow = 3
        tb.indent_lines()
        check_row(self, tb, 0, "  a")
        check_row(self, tb, 1, "    b")
        check_row(self, tb, 2, "  c")
        check_row(self, tb, 3, "    d")
        tb.penRow = 3
        tb.markerRow = 3
        tb.unindent_lines()
        check_row(self, tb, 0, "  a")
        check_row(self, tb, 1, "    b")
        check_row(self, tb, 2, "  c")
        check_row(self, tb, 3, "  d")
        tb.unindent_lines()
        check_row(self, tb, 0, "  a")
        check_row(self, tb, 1, "    b")
        check_row(self, tb, 2, "  c")
        check_row(self, tb, 3, "d")
        tb.unindent_lines()
        check_row(self, tb, 0, "  a")
        check_row(self, tb, 1, "    b")
        check_row(self, tb, 2, "  c")
        check_row(self, tb, 3, "d")
        tb.penRow = 0
        tb.markerRow = 0
        tb.unindent_lines()
        check_row(self, tb, 0, "a")
        check_row(self, tb, 1, "    b")
        check_row(self, tb, 2, "  c")
        check_row(self, tb, 3, "d")
        tb.unindent_lines()
        check_row(self, tb, 0, "a")
        check_row(self, tb, 1, "    b")
        check_row(self, tb, 2, "  c")
        check_row(self, tb, 3, "d")

    def test_indent_unindent_lines2(self):
        def insert(input):
            for i in input:
                if i == u"\n":
                    self.textBuffer.carriage_return()
                else:
                    self.textBuffer.insert_printable_with_pairing(ord(i), None)
                    self.textBuffer.parse_document()
            self.assertEqual(self.textBuffer.parser.data, input)

        def check_pen_marker(penRow, penCol, markerRow, markerCol):
            self.assertEqual(
                (penRow, penCol, markerRow, markerCol),
                (tb.penRow, tb.penCol, tb.markerRow, tb.markerCol),
            )

        def select_char(penRow, penCol, markerRow, markerCol):
            self.textBuffer.penRow = penRow
            self.textBuffer.penCol = penCol
            self.textBuffer.markerRow = markerRow
            self.textBuffer.markerCol = markerCol
            self.textBuffer.selectionMode = selectable.kSelectionCharacter

        tb = self.textBuffer
        self.assertEqual(tb.parser.row_count(), 1)
        check_pen_marker(0, 0, 0, 0)
        insert(u"apple\nbanana\ncarrot\ndate\neggplant\n")
        check_row(self, tb, 0, "apple")
        check_row(self, tb, 1, "banana")
        check_row(self, tb, 2, "carrot")
        check_row(self, tb, 3, "date")
        check_row(self, tb, 4, "eggplant")
        select_char(0, 3, 2, 2)
        check_pen_marker(0, 3, 2, 2)
        tb.indent()
        check_row(self, tb, 0, "  apple")
        check_row(self, tb, 1, "  banana")
        check_row(self, tb, 2, "  carrot")
        check_row(self, tb, 3, "date")
        check_row(self, tb, 4, "eggplant")
        check_pen_marker(0, 5, 2, 4)
        tb.indent()
        check_row(self, tb, 0, "    apple")
        check_row(self, tb, 1, "    banana")
        check_row(self, tb, 2, "    carrot")
        check_row(self, tb, 3, "date")
        check_row(self, tb, 4, "eggplant")
        check_pen_marker(0, 7, 2, 6)

        select_char(0, 3, 0, 2)
        tb.unindent()
        check_row(self, tb, 0, "  apple")
        check_row(self, tb, 1, "    banana")
        check_row(self, tb, 2, "    carrot")
        check_row(self, tb, 3, "date")
        check_row(self, tb, 4, "eggplant")
        check_pen_marker(0, 1, 0, 0)

        select_char(0, 3, 2, 2)
        tb.indent()
        check_row(self, tb, 0, "    apple")
        check_row(self, tb, 1, "      banana")
        check_row(self, tb, 2, "      carrot")
        check_row(self, tb, 3, "date")
        check_row(self, tb, 4, "eggplant")
        check_pen_marker(0, 5, 2, 4)
        tb.indent()
        check_pen_marker(0, 7, 2, 6)
        tb.indent()
        check_pen_marker(0, 9, 2, 8)


class TextInsertTestCases(ActionsTestCase):
    def setUp(self):
        TestCaseHelper.setUp(self)
        log.shouldWritePrintLog = False
        self.prg = ci_program.CiProgram()
        self.textBuffer = text_buffer.TextBuffer(self.prg)
        self.textBuffer.set_view(FakeView())
        # self.assertEqual(self.textBuffer.scrollRow, 0)
        # self.assertEqual(self.textBuffer.scrollCol, 0)

    def tearDown(self):
        self.textBuffer = None
        TestCaseHelper.tearDown(self)

    def test_auto_insert_pair_disable(self):
        self.prg.prefs.editor["autoInsertClosingCharacter"] = False

        def insert(*args):
            self.textBuffer.insert_printable_with_pairing(*args)
            self.textBuffer.parse_document()

        tb = self.textBuffer
        insert(ord("o"), None)
        insert(ord("("), None)
        check_row(self, tb, 0, "o(")
        insert(ord("a"), None)
        check_row(self, tb, 0, "o(a")
        tb.edit_undo()
        check_row(self, tb, 0, "o(")
        tb.edit_undo()
        check_row(self, tb, 0, "o")
        tb.edit_undo()
        check_row(self, tb, 0, "")
        # Don't insert pair if the next char is not whitespace.
        insert(ord("o"), None)
        check_row(self, tb, 0, "o")
        tb.cursor_left()
        check_row(self, tb, 0, "o")
        insert(ord("("), None)
        check_row(self, tb, 0, "(o")

    def test_auto_insert_pair_enable(self):
        self.prg.prefs.editor["autoInsertClosingCharacter"] = True

        def insert(*args):
            self.textBuffer.insert_printable_with_pairing(*args)
            self.textBuffer.parse_document()

        tb = self.textBuffer
        insert(ord("o"), None)
        insert(ord("("), None)
        check_row(self, tb, 0, "o()")
        insert(ord("a"), None)
        check_row(self, tb, 0, "o(a)")
        tb.edit_undo()
        check_row(self, tb, 0, "o()")
        tb.edit_undo()
        check_row(self, tb, 0, "")
        # Don't insert pair if the next char is not whitespace.
        insert(ord("o"), None)
        check_row(self, tb, 0, "o")
        tb.cursor_left()
        check_row(self, tb, 0, "o")
        insert(ord("("), None)
        check_row(self, tb, 0, "(o")


class GrammarDeterminationTestCases(ActionsTestCase):
    def setUp(self):
        TestCaseHelper.setUp(self)
        log.shouldWritePrintLog = False
        self.prg = ci_program.CiProgram()
        self.textBuffer = text_buffer.TextBuffer(self.prg)
        self.textBuffer.set_view(FakeView())

    def tearDown(self):
        self.textBuffer = None
        TestCaseHelper.tearDown(self)

    def test_message_backspace(self):
        tb = self.textBuffer
        self.assertEqual(
            tb._determine_root_grammar(*os.path.splitext("test.cc")),
            self.prg.prefs.grammars.get(self.prg.prefs.extensions.get(".cc")),
        )
