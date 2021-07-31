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


class Frame:
    def __init__(self):
        # Track the total number of commands processed to create this frame.
        # This is used to match a point in the command stream to a frame.
        self.cmdCount = None
        self.cursor = None
        self.drawList = []

    def add_str(self, row, col, text, style):
        self.drawList.append((row, col, text, style))

    def set_cmd_count(self, count):
        self.cmdCount = count

    def set_cursor(self, cursor):
        self.cursor = cursor

    def grab_frame(self):
        r = self.drawList, self.cursor, self.cmdCount
        self.drawList = []
        self.cursor = None
        self.cmdCount = None
        return r
