# -*- coding: utf-8 -*-
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
from jaseci.utils.utils import TestCaseHelper

from .. import log
from .. import ci_program
from .. import selectable


class SelectableTestCases(TestCaseHelper, unittest.TestCase):
    def setUp(self):
        TestCaseHelper.setUp(self)
        self.selectable = selectable.Selectable(ci_program.CiProgram())
        log.shouldWritePrintLog = True

    def tearDown(self):
        self.selectable = None
        TestCaseHelper.tearDown(self)

    def test_default_values(self):
        selectable = self.selectable
        self.assertEqual(selectable.selection(), (0, 0, 0, 0))

    def test_selection_none(self):
        slectable = self.selectable
        slectable.parser.data = u"oneTwo\n\nfive"
        slectable.parse_document()
        slectable.selectionMode = selectable.kSelectionNone
        self.assertEqual(slectable.extend_selection(), (0, 0, 0, 0, 0))
        slectable.penCol = 3
        self.assertEqual(slectable.extend_selection(), (0, 0, 0, 0, 0))

    def test_selection_all(self):
        slectable = self.selectable
        slectable.parser.data = u"oneTwo\n\nfive"
        slectable.parse_document()
        slectable.selectionMode = selectable.kSelectionAll
        self.assertEqual(slectable.extend_selection(), (2, 4, 0, 0, 0))
        slectable.penCol = 3
        self.assertEqual(slectable.extend_selection(), (2, 1, 0, 0, 0))

    def test_selection_block(self):
        slectable = self.selectable
        slectable.parser.data = u"oneTwo\n\nfive"
        slectable.parse_document()
        slectable.selectionMode = selectable.kSelectionBlock
        self.assertEqual(slectable.extend_selection(), (0, 0, 0, 0, 0))
        slectable.penCol = 3
        self.assertEqual(slectable.extend_selection(), (0, 0, 0, 0, 0))

    def test_selection_character(self):
        slectable = self.selectable
        slectable.parser.data = u"oneTwo\n\nfive"
        slectable.parse_document()
        slectable.selectionMode = selectable.kSelectionCharacter
        self.assertEqual(slectable.extend_selection(), (0, 0, 0, 0, 0))
        slectable.penCol = 3
        self.assertEqual(slectable.extend_selection(), (0, 0, 0, 0, 0))

    def test_selection_line(self):
        slectable = self.selectable
        slectable.parser.data = u"one two\n\nfive"
        slectable.parse_document()
        slectable.penRow = 1
        slectable.selectionMode = selectable.kSelectionLine
        log.debug(u"slectable.extend_selection",
                  slectable.extend_selection())
        self.assertEqual(slectable.extend_selection(), (0, 0, 0, 0, 0))
        slectable.penRow = 3
        slectable.penCol = 3
        slectable.markerRow = 1
        slectable.markerCol = 4
        self.assertEqual(slectable.extend_selection(), (0, -3, 0, -4, 0))

    def test_selection_word(self):
        slectable = self.selectable
        slectable.parser.data = u"one two\nSeveral test words\nfive"
        slectable.parse_document()
        slectable.selectionMode = selectable.kSelectionWord
        slectable.penRow = 1
        slectable.penCol = 2
        self.assertEqual(slectable.extend_selection(), (0, 5, 0, 0, 0))
        slectable.penRow = 1
        slectable.penCol = 9
        slectable.markerCol = 2
        self.assertEqual(slectable.extend_selection(), (0, 3, 0, -2, 0))

    # Deletion tests.

    def test_deletion_none(self):
        slectable = self.selectable
        slectable.parser.data = u"one two\nSeveral test words.\nfive"
        slectable.parse_document()
        slectable.selectionMode = selectable.kSelectionNone
        slectable.penCol = 1
        slectable.do_delete_selection()
        self.assertEqual(slectable.parser.data,
                         u"one two\nSeveral test words.\nfive")

    def test_deletion_all(self):
        slectable = self.selectable

        def apply_selection(args):
            slectable.penRow += args[0]
            slectable.penCol += args[1]
            slectable.markerRow += args[2]
            slectable.markerCol += args[3]
            slectable.selectionMode += args[4]

        self.assertEqual(slectable.selection(), (0, 0, 0, 0))
        slectable.parser.data = u"oneTwo\n\nfive"
        slectable.parse_document()
        self.assertEqual(slectable.selection(), (0, 0, 0, 0))
        slectable.selectionMode = selectable.kSelectionAll
        self.assertEqual(slectable.extend_selection(), (2, 4, 0, 0, 0))
        slectable.penCol = 3
        self.assertEqual(slectable.extend_selection(), (2, 1, 0, 0, 0))

        apply_selection(slectable.extend_selection())
        self.assertEqual(slectable.selection(), (2, 4, 0, 0))
        slectable.do_delete_selection()
        self.assertEqual(slectable.parser.data, u"")

        slectable.insert_lines_at(
            0, 0, (u"wx", u"", u"yz"), selectable.kSelectionAll
        )
        self.assertEqual(slectable.parser.data, u"wx\n\nyz")

    def test_deletion_block(self):
        slectable = self.selectable
        slectable.parser.data = u"oneTwo\n\nfive"
        slectable.parse_document()
        slectable.selectionMode = selectable.kSelectionBlock
        self.assertEqual(slectable.extend_selection(), (0, 0, 0, 0, 0))
        slectable.markerRow = 0
        slectable.markerCol = 1
        slectable.penRow = 2
        slectable.penCol = 3
        self.assertEqual(slectable.extend_selection(), (0, 0, 0, 0, 0))
        self.assertEqual(slectable.parser.data, u"oneTwo\n\nfive")
        slectable.do_delete_selection()
        self.assertEqual(slectable.parser.data, u"oTwo\n\nfe")
        slectable.insert_lines_at(
            0, 1, (u"wx", u"", u"yz"), selectable.kSelectionBlock
        )
        self.assertEqual(slectable.parser.data, u"owxTwo\n\nfyze")

    def test_deletion_character(self):
        slectable = self.selectable
        slectable.parser.data = u"one two\nSeveral test words.\nfive"
        slectable.parse_document()
        slectable.selectionMode = selectable.kSelectionCharacter
        slectable.penCol = 1
        slectable.do_delete_selection()
        self.assertEqual(slectable.parser.data,
                         u"ne two\nSeveral test words.\nfive")
        slectable.markerCol = 3
        slectable.do_delete_selection()
        self.assertEqual(slectable.parser.data,
                         u"ntwo\nSeveral test words.\nfive")
        slectable.penRow = 1
        slectable.penCol = 1
        slectable.do_delete_selection()
        self.assertEqual(slectable.parser.data,
                         u"ntweveral test words.\nfive")

    def test_deletion_line(self):
        slectable = self.selectable
        slectable.parser.data = u"one two\n\nfive"
        slectable.parse_document()
        slectable.penRow = 1
        slectable.selectionMode = selectable.kSelectionLine
        log.debug(u"slectable.extend_selection",
                  slectable.extend_selection())
        self.assertEqual(slectable.extend_selection(), (0, 0, 0, 0, 0))
        slectable.penRow = 3
        slectable.penCol = 3
        slectable.markerRow = 1
        slectable.markerCol = 4
        self.assertEqual(slectable.extend_selection(), (0, -3, 0, -4, 0))

    def test_deletion_word(self):
        slectable = self.selectable
        slectable.parser.data = u"one two\nSeveral test words.\nfive"
        slectable.parse_document()
        slectable.selectionMode = selectable.kSelectionWord
        slectable.penRow = 1
        slectable.penCol = 2
        self.assertEqual(slectable.extend_selection(), (0, 5, 0, 0, 0))
        slectable.penRow = 1
        slectable.penCol = 9
        slectable.markerCol = 2
        self.assertEqual(slectable.extend_selection(), (0, 3, 0, -2, 0))

    def test_unicode(self):
        slectable = self.selectable
        slectable.parser.data = u"one two\n😀Several test words.\nfive"
        slectable.parse_document()
        slectable.selectionMode = selectable.kSelectionCharacter
        slectable.penRow = 1
        slectable.penCol = 0
        self.assertEqual(slectable.markerCol, 0)
        slectable.penCol = 2
        self.assertEqual(slectable.markerCol, 0)


if __name__ == "__main__":
    unittest.main()
