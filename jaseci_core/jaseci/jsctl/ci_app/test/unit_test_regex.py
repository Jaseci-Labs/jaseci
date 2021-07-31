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

# import re
import unittest
from jaseci.utils.utils import TestCaseHelper

from .. import regex


class RegexTestCases(TestCaseHelper, unittest.TestCase):
    def setUp(self):
        TestCaseHelper.setUp(self)

    def tearDown(self):
        TestCaseHelper.tearDown(self)

    def test_common_numbers(self):
        def test_number(strInput, reg):
            sre = regex.kReNumbers.search(strInput)
            if sre is None:
                self.assertEqual(sre, reg)
                return
            self.assertEqual(reg, sre.regs[0])

        test_number("quick", None)
        test_number("0342", (0, 4))
        test_number("2342", (0, 4))
        test_number("0x42", (0, 4))
        test_number("0x0", (0, 3))
        test_number(".2342", (0, 5))
        test_number("2.342", (0, 5))
        test_number("23.42", (0, 5))
        test_number("234.2", (0, 5))
        test_number("2342.", (0, 5))
        test_number("23q42.", (0, 2))
        test_number(" 2u ", (1, 3))
        test_number(" 2U ", (1, 3))
        test_number(" 2ull ", (1, 5))
        test_number(" 2ULL ", (1, 5))
        test_number(" 2.f ", (1, 4))
        test_number(" .3f ", (1, 4))
        test_number(" 4.7234e-11 ", (1, 11))
