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

from timeit import timeit
import unittest

from . import parser


class PerformanceTestCases(unittest.TestCase):
    def test_array_vs_getter(self):
        setup = """data = ['a'] * 100\n"""
        setup += """def get(n):\n"""
        setup += """  return data[n]\n"""
        setup += """class B:\n"""
        setup += """  def get_via_member(self, n):\n"""
        setup += """    return data[n]\n"""
        setup += """  def __getitem__(self, n):\n"""
        setup += """    return data[n]\n"""
        setup += """b = B()\n"""
        a = timeit("""x = data[5]\n""", setup=setup, number=10000)
        b = timeit("""x = get(5)\n""", setup=setup, number=10000)
        c = timeit("""x = b.get_via_member(5)\n""", setup=setup, number=10000)
        d = timeit("""x = b[5]\n""", setup=setup, number=10000)
        # print("\n%s | %s %s | %s %s | %s %s" % (a, b, a/b, c, a/c, d, a/d))
        # Calling a function or member is significantly slower than direct
        # access.
        self.assertGreater(b, a * 1.5)
        self.assertGreater(c, a * 2)
        self.assertGreater(d, a * 2)

    def test_slice_vs_startswith(self):
        if 0:
            setup = """x = 'a' * 100\n"""
            a = timeit("""x[:2] == "  "\n""", setup=setup, number=100000)
            b = timeit("""x.startswith("  ")\n""", setup=setup, number=100000)
            c = timeit("""x[0] == " " and x[1] == " "\n""",
                       setup=setup, number=100000)
            # print("\na %s, b %s, c %s | %s %s" % (a, b, c, c, a/c))
            # Calling a function or member is significantly slower than direct
            # access.

            # This check is not performing the same in Python3.
            self.assertGreater(b, a * 1.7)  # b is much slower.
            self.assertGreater(b, c * 1.9)  # b is much slower.
            self.assertGreater(a, c * 0.6)  # a and c are similar.
            self.assertGreater(c, a * 0.4)  # a and c are similar.

    def test_default_parameter(self):
        setup = """def with_default(a, b=None):\n"""
        setup += """  if b is not None: return b\n"""
        setup += """  return a*a\n"""
        setup += """def without_default(a, b):\n"""
        setup += """  if b is -1: return b\n"""
        setup += """  return a*b\n"""
        a = timeit("""with_default(5);""" * 100, setup=setup, number=10000)
        b = timeit("""without_default(5, 0);""" *
                   100, setup=setup, number=10000)
        # Assert that neither too much faster than the other
        # Note: empirically, this is affected (on a MacBook Air) by whether the
        # machine is running from battery or plugged in.
        # It also appears to vary between Python 2 and Python 3.
        self.assertGreater(a, b * 0.6)
        self.assertGreater(b, a * 0.6)

    def test_char_vs_ord(self):
        setup = """a="apple"\n"""
        a = timeit("""a[0] > "z";""" * 100, setup=setup, number=10000)
        b = timeit("""ord(a[0]) > 100;""" * 100, setup=setup, number=10000)
        self.assertGreater(b, a)

    def test_insert1(self):
        # Disabled due to running time.
        if 0:
            # This tests a performance assumption. If this test fails, the
            # program should still work fine, but it may not run as fast as it
            # could by using different assumptions.
            #
            # Insert into an array of strings is expected to be faster than
            # insert into a contiguous buffer of similar size.
            #
            # This is why ci_edit uses both a self.data buffer and a
            # self.lines[] array. Though splitting the data into lines is also
            # expensive, see tests below.
            #
            # At 1,000 bytes the performance is similar.
            a = timeit(
                'data1 = data1[:500] + "x" + data1[500:]',
                setup='data1 = "a" * 1000',
                number=10000,
            )
            b = timeit(
                'data2[5] = data2[5][:50] + "x" + data2[5][50:]',
                setup='data2 = ["a" * 100] * 10',
                number=10000,
            )
            self.assertGreater(a, b * 0.8)
            self.assertLess(a, b * 4)
            # At 10,000 bytes the array of strings is 1.4 to 3 times faster.
            a = timeit(
                'data1 = data1[:5000] + "x" + data1[5000:]',
                setup='data1 = "a" * 10000',
                number=10000,
            )
            b = timeit(
                'data2[50] = data2[50][:50] + "x" + data2[50][50:]',
                setup='data2 = ["a" * 100] * 100',
                number=10000,
            )
            self.assertGreater(a, b * 1.4)
            self.assertLess(a, b * 4)
            # At 100,000 bytes the array of strings is 12 to 24 times faster.
            a = timeit(
                'data1 = data1[:50000] + "x" + data1[50000:]',
                setup='data1 = "a" * 100000',
                number=10000,
            )
            b = timeit(
                'data2[500] = data2[500][:50] + "x" + data2[500][50:]',
                setup='data2 = ["a" * 100] * 1000',
                number=10000,
            )
            self.assertGreater(a, b * 12)
            self.assertLess(a, b * 24)

    def test_split_insert(self):
        # Disabled due to running time.
        if 0:
            # This tests a performance assumption. If this test fails, the
            # program should still work fine, but it may not run as fast as it
            # could by using different assumptions.
            #
            # With frequent splitting the performance reverses.
            for lineCount in (100, 1000, 5000):
                half = lineCount // 2
                a = timeit(
                    r"""data2 = data1.split('\n'); \
                data2[%s] = data2[%s][:50] + "x" + data2[%s][50:]; \
                """
                    % (half, half, half),
                    setup=r"""data1 = ("a" * 100 + '\n') * %s""" % (lineCount,),
                    number=10000,
                )
                b = timeit(
                    'data1 = data1[:%s] + "x" + data1[%s:]' % (half, half),
                    setup=r"""data1 = ("a" * 100 + '\n') * %s""" % (lineCount,),
                    number=10000,
                )
                print("\n%9s: %s %s" % (lineCount, a, b))
                self.assertGreater(a, b)

    def test_split_insert_balance(self):
        # Disabled due to running time.
        if 0:
            # This tests a performance assumption. If this test fails, the
            # program should still work fine, but it may not run as fast as it
            # could by using different assumptions.
            #
            # With 5 inserts between splits, the performance is nearly the same.
            for lineCount in (100, 1000, 5000):
                half = lineCount // 2
                a = timeit(
                    r"""data2 = data1.split('\n');"""
                    + (
                        r"""data2[%s] = data2[%s][:50] + "x" + data2[%s][50:]; \
                """
                        % (half, half, half)
                    )
                    * 5,
                    setup=r"""data1 = ("a" * 100 + '\n') * %s""" % (lineCount,),
                    number=10000,
                )
                b = timeit(
                    ('data1 = data1[:%s] + "x" + data1[%s:]; ' %
                     (half, half)) * 5,
                    setup=r"""data1 = ("a" * 100 + '\n') * %s""" % (lineCount,),
                    number=10000,
                )
                print("\n%9s: %s %s" % (lineCount, a, b))

    def test_instance_vs_tuple(self):
        # Disabled due to running time.
        if 0:
            # This tests a performance assumption. If this test fails, the
            # program should still work fine, but it may not run as fast as it
            # could by using different assumptions.
            for lineCount in (100, 1000, 5000):
                a = timeit(
                    r"""
a = Node()
a.foo = 5
a.bar = 'hi'
a.blah = 7
foo.append(a)
""",
                    setup=r"""
foo = []
class Node:
  def __init__(self):
    self.foo = None
    self.bar = None
    self.blah = None
""",
                    number=10000,
                )
                b = timeit(
                    r"""
a = (5, 'hi', 7)
foo.append(a)
""",
                    setup=r"""
foo = []
""",
                    number=10000,
                )
                print("\n%9s: %s %s" % (lineCount, a, b))
