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

try:
    unicode
except NameError:
    unicode = str
    unichr = chr

import os
import unittest

try:
    import unittest.mock
except ImportError:
    print("\nWarning: import unittest.mock failed. Some tests will be skipped.")
    pass

from . import buffer_file as test_buffer_file


class pathRowColumnTestCases(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_path_row_column(self):
        if not hasattr(unittest, "mock"):
            return
        # Shortcuts.
        originalIsFile = test_buffer_file.os.path.isfile
        decode = test_buffer_file.path_row_column
        Mock = unittest.mock.MagicMock

        mock = Mock(side_effect=[False, True])
        self.assertEqual(False, mock("a"))
        self.assertEqual(True, mock("a"))
        with self.assertRaises(StopIteration):
            self.assertEqual(True, mock("a"))

        os.path.isfile = Mock(side_effect=[False, True])
        self.assertEqual(False, os.path.isfile("a"))
        self.assertEqual(True, os.path.isfile("a"))
        with self.assertRaises(StopIteration):
            self.assertEqual(True, os.path.isfile("a"))

        os.path.isfile = Mock(side_effect=[False, True])
        self.assertEqual(decode(u"", u""), (u"", None, None))
        self.assertEqual(decode(u"/", u""), (u"/", None, None))

        os.path.isfile = Mock(side_effect=[False, False])
        self.assertEqual(decode(u"//apple", u"/stuff"),
                         (u"/stuff/apple", None, None))

        os.path.isfile = Mock(side_effect=[False, False])
        self.assertEqual(decode(u"//apple", None), (u"//apple", None, None))

        os.path.isfile = Mock(side_effect=[False, False, False])
        self.assertEqual(decode(u":5", u""), (u"", 4, None))

        os.path.isfile = Mock(side_effect=[False, False, False])
        self.assertEqual(decode(u"/:5", u""), (u"/", 4, None))

        os.path.isfile = Mock(side_effect=[False, False, False])
        self.assertEqual(decode(u"//apple:5", u"/stuff"),
                         (u"/stuff/apple", 4, None))

        os.path.isfile = Mock(side_effect=[False, False, False])
        self.assertEqual(decode(u"//apple:5", None), (u"//apple", 4, None))

        os.path.isfile = Mock(side_effect=[False, True])
        self.assertEqual(decode(u"//apple", u"/stuff"),
                         (u"/stuff/apple", None, None))

        os.path.isfile = Mock(side_effect=[False, True])
        self.assertEqual(decode(u"//apple", None), (u"apple", None, None))

        os.path.isfile = Mock(side_effect=[False, True])
        self.assertEqual(decode(u":5", u""), (u"", 4, None))

        os.path.isfile = Mock(side_effect=[False, True])
        self.assertEqual(decode(u"/:5", u""), (u"/", 4, None))

        os.path.isfile = Mock(side_effect=[False, True])
        self.assertEqual(decode(u"//apple:5", u"/stuff"),
                         (u"/stuff/apple", 4, None))

        os.path.isfile = Mock(side_effect=[False, True, True])
        self.assertEqual(decode(u"//apple:5", None), (u"apple", 4, None))

        os.path.isfile = Mock(side_effect=[False, True, True])
        self.assertEqual(decode(u"//apple:5:", None), (u"apple", 4, None))

        os.path.isfile = Mock(side_effect=[False, True, True])
        self.assertEqual(decode(u"//apple:5:9", None), (u"apple", 4, 8))

        os.path.isfile = Mock(side_effect=[False, True, True])
        self.assertEqual(decode(u"//apple:5:9:", None), (u"apple", 4, 8))

        os.path.isfile = Mock(side_effect=[False, True, True])
        self.assertEqual(decode(u"apple:banana", None),
                         (u"apple:banana", None, None))

        os.path.isfile = Mock(side_effect=[False, True, True])
        self.assertEqual(
            decode(u"//apple:banana:cat:",
                   None), (u"apple:banana:cat:", None, None)
        )

        os.path.isfile = originalIsFile
