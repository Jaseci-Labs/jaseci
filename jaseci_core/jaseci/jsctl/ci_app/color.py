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

import curses


class Colors:
    def __init__(self, colorPrefs):
        self.__colorPrefs = colorPrefs
        self.colors = 256
        self.__cache = {}

    def get(self, colorType, delta=0):
        if type(colorType) == type(0):
            colorIndex = colorType
        else:
            colorIndex = self.__colorPrefs[colorType]
        colorIndex = min(self.colors - 1, colorIndex + delta)
        color = self.__cache.get(colorIndex) or curses.color_pair(colorIndex)
        self.__cache[colorIndex] = color
        if colorType in ("error", "misspelling"):
            color |= curses.A_BOLD | curses.A_REVERSE
        return color
