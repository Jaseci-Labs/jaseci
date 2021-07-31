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

# Python comment
/* Not a comment */
/** Not a comment */
<!-- Not a comment -->
// Not a comment
<script> Still Python (no embedded script) </script>

# TODO(dschuyler): A test comment.

'a\\' # double escape
'a\\\\' # quadruple escape
'a\02112s\0a\01b\012cfd23323sa' # numbers
'\nfiller\w\\aaa\adf\bfsdf\'d\\\'sdff' # special values

"a\\" # double escape
"a\\\\" # quadruple escape
"filler\nsfas\w\\aaa\adf\bfsdf\"d\\\"sadff" # special values

'''asd\nsad'a"fsadf''' # triple single quotes
r'''asd\nsad'a"fsadf''' # triple single quotes

"""asd\nsad'a"fsadf""" # triple double quotes
r"""asd\nsad'a"fsadf""" # triple double quotes

class Foo:
  def __init__(self, data):
    print data

  def blah(self):
    pass

