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

import bisect
import glob
import io
import os
import re

from . import log


class OsDictionary:
    def __init__(self):
        path = "/usr/share/dict/words"
        try:
            self.file = io.open(path, "r")
            self.fileLength = self.file.seek(0, 2)  # Seek to end of file.
            self.pageSize = 1024 * 8  # Arbitrary.
            # Add one to pick up any partial page at the end.
            self.filePages = self.fileLength // self.pageSize + 1
        except IOError:
            self.file = None
        self.cache = {}
        self.knownOffsets = []

    def check(self, word):
        if self.file is None:
            return False
        word = word.lower()
        r = self.cache.get(word)
        if r is not None:
            return r
        high = self.filePages
        low = 0
        leash = 20  # Way more than should be necessary.
        try:
            while True:
                if not leash:
                    # There's likely a bug in this function if we hit this.
                    log.info("spelling leash", word)
                    return False
                leash -= 1
                page = low + (high - low) // 2
                self.file.seek(page * self.pageSize)
                # Add 100 to catch any words that straddle a page.
                size = min(self.pageSize + 100,
                           self.fileLength - page * self.pageSize)
                if not size:
                    self.cache[word] = False
                    return False
                chunk = self.file.read(size)
                chunk = chunk[chunk.find("\n"): chunk.rfind("\n")]
                if not chunk:
                    self.cache[word] = False
                    return False
                words = chunk.split()
                if word < words[0].lower():
                    high = page
                    continue
                if word > words[-1].lower():
                    low = page
                    continue
                lowerWords = [i.lower() for i in words]
                index = bisect.bisect_left(lowerWords, word)
                if lowerWords[index] == word:
                    self.cache[word] = True
                    return True
                self.cache[word] = False
                return False
        except IOError:
            return False


class Dictionary:
    def __init__(self, dictionaryList, pathPrefs):
        self.osDictionary = OsDictionary()
        self.pathPrefs = pathPrefs

        self.grammarWords = {}
        self.load_words(os.path.dirname(__file__))
        self.load_words(os.path.expanduser("~/.ci_edit/dictionaries"))

        words = set()
        for i in dictionaryList:
            words.update(self.grammarWords.get(i, set()))
        self.baseWords = words
        self.pathWords = set()

    def set_up_words_for_path(self, path):
        self.pathWords = set()
        # log.info(repr(self.pathPrefs))
        for k, v in self.pathPrefs.items():
            if k in path:
                for i in v:
                    self.pathWords.update(self.grammarWords.get(i, set()))

    def load_words(self, dirPath):
        dirPath = os.path.join(dirPath, "dictionary.")
        for path in glob.iglob(dirPath + "*.words"):
            if os.path.isfile(path):
                grammarName = path[len(dirPath): -len(".words")]
                with io.open(path, "r") as f:
                    lines = f.readlines()
                    index = 0
                    while not len(lines[index]) or lines[index][0] == "#":
                        index += 1
                    log.startup(len(lines) - index, "words from", path)
                    # TODO(dschuyler): Word contractions are hacked by storing
                    # the components of the contraction. So didn, doesn, and isn
                    # are considered 'words'.
                    self.grammarWords[grammarName] = set(
                        [
                            p
                            for l in lines[index:]
                            for w in l.split()
                            for p in w.split("'")
                        ]
                    )

    def is_correct(self, word, grammarName):
        if len(word) <= 1:
            return True
        words = self.baseWords
        lowerWord = word.lower()
        if word in words or lowerWord in words:
            return True
        if lowerWord in self.grammarWords.get(grammarName, set()):
            return True
        if lowerWord.startswith("sub") and lowerWord[3:] in words:
            return True
        if lowerWord.startswith("un") and lowerWord[2:] in words:
            return True
        if lowerWord in self.pathWords:
            return True
        if 1:
            if len(word) == 2 and word[1] == "s" and word[0].isupper():
                # Upper case, with an 's' for plurality (e.g. PDFs).
                return True
        if 0:
            if len(re.sub("[A-Z]", "", word)) == 0:
                # All upper case.
                return True
        if 0:
            # TODO(dschuyler): This is an experiment. Considering a py specific
            # word list instead.
            if grammarName == "py":
                # Handle run together (undelineated) words.
                if len(re.sub("[a-z]+", "", word)) == 0:
                    for i in range(len(word), 0, -1):
                        if word[:i] in words and word[i:] in words:
                            return True
        if 1:  # Experimental.
            # Fallback to the OS dictionary.
            return self.osDictionary.check(word)
        # log.info(grammarName, word)
        return False
