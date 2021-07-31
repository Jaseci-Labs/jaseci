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
"""Formatters."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


def format_python(text):
    try:
        import black
    except ImportError:
        raise RuntimeError(u"install black formatter to format: pip install black")

    return black.format_str(text, mode=black.FileMode())
