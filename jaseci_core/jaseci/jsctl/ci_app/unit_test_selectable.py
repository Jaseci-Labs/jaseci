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

from . import log
from . import ci_program
from . import selectable


class SelectableTestCases(unittest.TestCase):
    def setUp(self):
        self.selectable = selectable.Selectable(ci_program.CiProgram())
        log.shouldWritePrintLog = True

    def tearDown(self):
        self.selectable = None

    def test_default_values(self):
        selectable = self.selectable
        self.assertEqual(selectable.selection(), (0, 0, 0, 0))

    def test_selection_none(self):
        selectable = self.selectable
        selectable.parser.data = u"oneTwo\n\nfive"
        selectable.parse_document()
        selectable.selectionMode = selectable.kSelectionNone
        self.assertEqual(selectable.extend_selection(), (0, 0, 0, 0, 0))
        selectable.penCol = 3
        self.assertEqual(selectable.extend_selection(), (0, 0, 0, 0, 0))

    def test_selection_all(self):
        selectable = self.selectable
        selectable.parser.data = u"oneTwo\n\nfive"
        selectable.parse_document()
        selectable.selectionMode = selectable.kSelectionAll
        self.assertEqual(selectable.extend_selection(), (2, 4, 0, 0, 0))
        selectable.penCol = 3
        self.assertEqual(selectable.extend_selection(), (2, 1, 0, 0, 0))

    def test_selection_block(self):
        selectable = self.selectable
        selectable.parser.data = u"oneTwo\n\nfive"
        selectable.parse_document()
        selectable.selectionMode = selectable.kSelectionBlock
        self.assertEqual(selectable.extend_selection(), (0, 0, 0, 0, 0))
        selectable.penCol = 3
        self.assertEqual(selectable.extend_selection(), (0, 0, 0, 0, 0))

    def test_selection_character(self):
        selectable = self.selectable
        selectable.parser.data = u"oneTwo\n\nfive"
        selectable.parse_document()
        selectable.selectionMode = selectable.kSelectionCharacter
        self.assertEqual(selectable.extend_selection(), (0, 0, 0, 0, 0))
        selectable.penCol = 3
        self.assertEqual(selectable.extend_selection(), (0, 0, 0, 0, 0))

    def test_selection_line(self):
        selectable = self.selectable
        selectable.parser.data = u"one two\n\nfive"
        selectable.parse_document()
        selectable.penRow = 1
        selectable.selectionMode = selectable.kSelectionLine
        log.debug(u"selectable.extend_selection",
                  selectable.extend_selection())
        self.assertEqual(selectable.extend_selection(), (0, 0, 0, 0, 0))
        selectable.penRow = 3
        selectable.penCol = 3
        selectable.markerRow = 1
        selectable.markerCol = 4
        self.assertEqual(selectable.extend_selection(), (0, -3, 0, -4, 0))

    def test_selection_word(self):
        selectable = self.selectable
        selectable.parser.data = u"one two\nSeveral test words\nfive"
        selectable.parse_document()
        selectable.selectionMode = selectable.kSelectionWord
        selectable.penRow = 1
        selectable.penCol = 2
        self.assertEqual(selectable.extend_selection(), (0, 5, 0, 0, 0))
        selectable.penRow = 1
        selectable.penCol = 9
        selectable.markerCol = 2
        self.assertEqual(selectable.extend_selection(), (0, 3, 0, -2, 0))

    # Deletion tests.

    def test_deletion_none(self):
        selectable = self.selectable
        selectable.parser.data = u"one two\nSeveral test words.\nfive"
        selectable.parse_document()
        selectable.selectionMode = selectable.kSelectionNone
        selectable.penCol = 1
        selectable.do_delete_selection()
        self.assertEqual(selectable.parser.data,
                         u"one two\nSeveral test words.\nfive")

    def test_deletion_all(self):
        selectable = self.selectable

        def apply_selection(args):
            selectable.penRow += args[0]
            selectable.penCol += args[1]
            selectable.markerRow += args[2]
            selectable.markerCol += args[3]
            selectable.selectionMode += args[4]

        self.assertEqual(selectable.selection(), (0, 0, 0, 0))
        selectable.parser.data = u"oneTwo\n\nfive"
        selectable.parse_document()
        self.assertEqual(selectable.selection(), (0, 0, 0, 0))
        selectable.selectionMode = selectable.kSelectionAll
        self.assertEqual(selectable.extend_selection(), (2, 4, 0, 0, 0))
        selectable.penCol = 3
        self.assertEqual(selectable.extend_selection(), (2, 1, 0, 0, 0))

        apply_selection(selectable.extend_selection())
        self.assertEqual(selectable.selection(), (2, 4, 0, 0))
        selectable.do_delete_selection()
        self.assertEqual(selectable.parser.data, u"")

        selectable.insert_lines_at(
            0, 0, (u"wx", u"", u"yz"), selectable.kSelectionAll
        )
        self.assertEqual(selectable.parser.data, u"wx\n\nyz")

    def test_deletion_block(self):
        selectable = self.selectable
        selectable.parser.data = u"oneTwo\n\nfive"
        selectable.parse_document()
        selectable.selectionMode = selectable.kSelectionBlock
        self.assertEqual(selectable.extend_selection(), (0, 0, 0, 0, 0))
        selectable.markerRow = 0
        selectable.markerCol = 1
        selectable.penRow = 2
        selectable.penCol = 3
        self.assertEqual(selectable.extend_selection(), (0, 0, 0, 0, 0))
        self.assertEqual(selectable.parser.data, u"oneTwo\n\nfive")
        selectable.do_delete_selection()
        self.assertEqual(selectable.parser.data, u"oTwo\n\nfe")
        selectable.insert_lines_at(
            0, 1, (u"wx", u"", u"yz"), selectable.kSelectionBlock
        )
        self.assertEqual(selectable.parser.data, u"owxTwo\n\nfyze")

    def test_deletion_character(self):
        selectable = self.selectable
        selectable.parser.data = u"one two\nSeveral test words.\nfive"
        selectable.parse_document()
        selectable.selectionMode = selectable.kSelectionCharacter
        selectable.penCol = 1
        selectable.do_delete_selection()
        self.assertEqual(selectable.parser.data,
                         u"ne two\nSeveral test words.\nfive")
        selectable.markerCol = 3
        selectable.do_delete_selection()
        self.assertEqual(selectable.parser.data,
                         u"ntwo\nSeveral test words.\nfive")
        selectable.penRow = 1
        selectable.penCol = 1
        selectable.do_delete_selection()
        self.assertEqual(selectable.parser.data,
                         u"ntweveral test words.\nfive")

    def test_deletion_line(self):
        selectable = self.selectable
        selectable.parser.data = u"one two\n\nfive"
        selectable.parse_document()
        selectable.penRow = 1
        selectable.selectionMode = selectable.kSelectionLine
        log.debug(u"selectable.extend_selection",
                  selectable.extend_selection())
        self.assertEqual(selectable.extend_selection(), (0, 0, 0, 0, 0))
        selectable.penRow = 3
        selectable.penCol = 3
        selectable.markerRow = 1
        selectable.markerCol = 4
        self.assertEqual(selectable.extend_selection(), (0, -3, 0, -4, 0))

    def test_deletion_word(self):
        selectable = self.selectable
        selectable.parser.data = u"one two\nSeveral test words.\nfive"
        selectable.parse_document()
        selectable.selectionMode = selectable.kSelectionWord
        selectable.penRow = 1
        selectable.penCol = 2
        self.assertEqual(selectable.extend_selection(), (0, 5, 0, 0, 0))
        selectable.penRow = 1
        selectable.penCol = 9
        selectable.markerCol = 2
        self.assertEqual(selectable.extend_selection(), (0, 3, 0, -2, 0))

    def test_unicode(self):
        selectable = self.selectable
        selectable.parser.data = u"one two\n😀Several test words.\nfive"
        selectable.parse_document()
        selectable.selectionMode = selectable.kSelectionCharacter
        selectable.penRow = 1
        selectable.penCol = 0
        self.assertEqual(selectable.markerCol, 0)
        selectable.penCol = 2
        self.assertEqual(selectable.markerCol, 0)


if __name__ == "__main__":
    unittest.main()
