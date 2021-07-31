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


class Bookmark(object):
    """
    This bookmark object is used as a marker for different places in a
    text document. Note that because text buffer lines index at 0, all
    references to rows also assume that 0 is the first line.
    """

    def __init__(self, beginRow, endRow, data):
        """
        Creates a bookmark located at the specified rows. This will
        automatically cast the passed in rows into integers.
        Args:
          beginRow (int-like): The line that the bookmark starts on (inclusive).
          endRow (int-like): The line that the bookmark ends on (inclusive).
          data (other): This is used to store any information that you would
                        like to to associate with this bookmark. It is an empty
                        dictionary by default.
        """
        self.__begin = int(beginRow)
        self.__end = int(endRow)
        self.data = data

    @property
    def range(self):
        return (self.begin, self.end)

    @range.setter
    def range(self, value):
        self.__begin, self.__end = sorted(int(x) for x in value)

    @property
    def begin(self):
        return self.__begin

    @begin.setter
    def begin(self, value):
        self.__begin, self.__end = sorted(int(x) for x in (value, self.__end))

    @property
    def end(self):
        return self.__end

    @end.setter
    def end(self, value):
        self.__begin, self.__end = sorted(int(x)
                                          for x in (self.__begin, value))

    def overlaps(self, bookmark):
        """
        Takes in another bookmark object and returns True if this bookmark
        shares any rows with the passed in bookmark.
        """
        begin1, end1 = self.range
        begin2, end2 = bookmark.range
        return begin1 <= end2 and end1 >= begin2

    def __contains__(self, row):
        """
        Args:
          row (int): the row that you want to check.

        Returns:
          True if the passed in row is inside the bookmark's range.
        """
        return self.begin <= row <= self.end

    def __lt__(self, other):
        assert isinstance(other, Bookmark)
        return self.range < other.range

    def __gt__(self, other):
        assert isinstance(other, Bookmark)
        return self.range > other.range

    def __eq__(self, other):
        assert isinstance(other, Bookmark)
        return self.range == other.range

    def __ne__(self, other):
        assert isinstance(other, Bookmark)
        return self.range != other.range

    def __le__(self, other):
        assert isinstance(other, Bookmark)
        return self.range <= other.range

    def __ge__(self, other):
        assert isinstance(other, Bookmark)
        return self.range >= other.range

    def __hash__(self):
        # NOTE: Any two bookmarks with the same range WILL have the same hash
        # value. self.range can also change, so be careful when using this in a
        # hash table.
        return hash(self.range)

    def __repr__(self):
        return repr(self.range)
