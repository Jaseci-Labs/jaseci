# Copyright 2016 Google Inc.
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
import io
import json
import os
import re
import sys

from . import default_prefs
from . import log
from . import regex


class Prefs:
    def __init__(self):
        self.prefsDirectory = "~/.ci_edit/prefs/"
        prefs = default_prefs.prefs
        self.color8 = default_prefs.color8
        self.color16 = default_prefs.color16
        self.color256 = default_prefs.color256
        self.color = self.color256
        self.dictionaries = prefs.get("dictionaries", [])
        self.editor = prefs.get("editor", {})
        self.devTest = prefs.get("devTest", {})
        self.palette = prefs.get("palette", {})
        self.startup = {}
        self.status = prefs.get(u"status", {})
        self.userData = prefs.get(u"userData", {})
        self.__set_up_grammars(prefs.get(u"grammar", {}))
        self.__set_up_file_types(prefs.get(u"fileType", {}))
        self.init()

    def load_prefs(self, fileName, category):
        # Check the user home directory for preferences.
        prefsPath = os.path.expanduser(
            os.path.expandvars(
                os.path.join(self.prefsDirectory, "%s.json" % (fileName,))
            )
        )
        if os.path.isfile(prefsPath) and os.access(prefsPath, os.R_OK):
            with io.open(prefsPath, "r") as f:
                try:
                    additionalPrefs = json.loads(f.read())
                    log.startup(additionalPrefs)
                    category.update(additionalPrefs)
                    log.startup("Updated editor prefs from", prefsPath)
                    log.startup("as", category)
                except Exception as e:
                    log.startup("failed to parse", prefsPath)
                    log.startup("error", e)
        return category

    def init(self):
        self.editor = self.load_prefs("editor", self.editor)
        self.status = self.load_prefs("status", self.status)

        self.colorSchemeName = self.editor["colorScheme"]
        if self.colorSchemeName == "custom":
            # Check the user home directory for a color scheme preference. If
            # found load it to replace the default color scheme.
            self.color = self.load_prefs("color_scheme", self.color)

        defaultColor = self.color["default"]
        defaultKeywordsColor = self.color["keyword"]
        defaultSpecialsColor = self.color["special"]
        for k, v in self.grammars.items():
            # Colors.
            v["colorIndex"] = self.color.get(k, defaultColor)
            if 0:
                v["keywordsColor"] = curses.color_pair(
                    self.color.get(k + "_keyword_color", defaultKeywordsColor)
                )
                v["specialsColor"] = curses.color_pair(
                    self.color.get(k + "_special_color", defaultSpecialsColor)
                )
        log.info("prefs init")

    def category(self, name):
        return {
            "color": self.color,
            "editor": self.editor,
            "startup": self.startup,
        }[name]

    def get_file_type(self, filePath):
        if filePath is None:
            return self.grammars.get("text")
        name = os.path.split(filePath)[1]
        fileType = self.nameToType.get(name)
        if fileType is None:
            fileExtension = os.path.splitext(name)[1]
            fileType = self.extensions.get(fileExtension, "text")
        return fileType

    def tabs_to_spaces(self, fileType):
        prefs = default_prefs.prefs.get(u"fileType", {})
        if fileType is None or prefs is None:
            return False
        file_prefs = prefs.get(fileType)
        return file_prefs and file_prefs.get(u"tabToSpaces")

    def get_grammar(self, fileType):
        return self.grammars.get(fileType)

    def save(self, category, label, value):
        log.info(category, label, value)
        prefCategory = self.category(category)
        prefCategory[label] = value
        prefsPath = os.path.expanduser(
            os.path.expandvars(
                os.path.join(self.prefsDirectory, "%s.json" % (category,))
            )
        )
        with io.open(prefsPath, "w", encoding=u"utf-8") as f:
            try:
                f.write(json.dumps(prefs[category]))
            except Exception as e:
                log.error("error writing prefs")
                log.exception(e)

    def _raise_grammar_not_found(self):
        log.startup("Available grammars:")
        for k, v in self.grammars.items():
            log.startup("  ", k, ":", len(v))
        raise Exception('missing grammar for "' +
                        grammarName + '" in prefs.py')

    def __set_up_grammars(self, defaultGrammars):
        self.grammars = {}
        # Arrange all the grammars by name.
        for k, v in defaultGrammars.items():
            v["name"] = k
            self.grammars[k] = v

        # Compile regexes for each grammar.
        for k, v in defaultGrammars.items():
            if 0:
                # keywords re.
                v["keywordsRe"] = re.compile(
                    regex.join_re_word_list(
                        v.get("keywords", []) + v.get("types", [])
                    )
                )
                v["errorsRe"] = re.compile(
                    regex.join_re_list(v.get("errors", [])))
                v["specialsRe"] = re.compile(
                    regex.join_re_list(v.get("special", []))
                )
            # contains and end re.
            matchGrammars = []
            markers = []
            # Index [0]
            if v.get("escaped"):
                markers.append(v["escaped"])
                matchGrammars.append(v)
            else:
                # Add a non-matchable placeholder.
                markers.append(regex.kNonMatchingRegex)
                matchGrammars.append(None)
            # Index [1]
            if v.get("end"):
                markers.append(v["end"])
                matchGrammars.append(v)
            else:
                # Add a non-matchable placeholder.
                markers.append(regex.kNonMatchingRegex)
                matchGrammars.append(None)
            # |Contains| markers start at index 2.
            for grammarName in v.get("contains", []):
                g = self.grammars.get(grammarName, None)
                if g is None:
                    self._raise_grammar_not_found()
                markers.append(g.get("begin", g.get("matches", u"")))
                matchGrammars.append(g)
            # |Next| markers start after |contains|.
            for grammarName in v.get("next", []):
                g = self.grammars.get(grammarName, None)
                if g is None:
                    self._raise_grammar_not_found()
                markers.append(g["begin"])
                matchGrammars.append(g)
            # |Errors| markers start after |next| markers.
            markers += v.get("errors", [])
            # |Keywords| markers start after |errors| markers.
            for keyword in v.get("keywords", []):
                markers.append(r"\b" + keyword + r"\b")
            # |Types| markers start after |keywords| markers.
            for types in v.get("types", []):
                markers.append(r"\b" + types + r"\b")
            # |Special| markers start after |types| markers.
            markers += v.get("special", [])
            # Variable width characters are at index [-3] in markers.
            markers.append(r"\t+")
            # Potentially double wide characters are at index [-2] in markers.
            markers.append(u"[\U00001100-\U000fffff]+")
            # Carriage return characters are at index [-1] in markers.
            markers.append(r"\n")
            # log.startup('markers', v['name'], markers)
            v["matchRe"] = re.compile(regex.join_re_list(markers))
            v["markers"] = markers
            v["matchGrammars"] = matchGrammars
            containsGrammarIndexLimit = 2 + len(v.get("contains", []))
            nextGrammarIndexLimit = containsGrammarIndexLimit + \
                len(v.get("next", []))
            errorIndexLimit = nextGrammarIndexLimit + len(v.get("errors", []))
            keywordIndexLimit = errorIndexLimit + len(v.get("keywords", []))
            typeIndexLimit = keywordIndexLimit + len(v.get("types", []))
            specialIndexLimit = typeIndexLimit + len(v.get("special", []))
            v["indexLimits"] = (
                containsGrammarIndexLimit,
                nextGrammarIndexLimit,
                errorIndexLimit,
                keywordIndexLimit,
                typeIndexLimit,
                specialIndexLimit,
            )

        # Reset the re.cache for user regexes.
        re.purge()

    def __set_up_file_types(self, defaultFileTypes):
        self.nameToType = {}
        self.extensions = {}
        fileTypes = {}
        for k, v in defaultFileTypes.items():
            for name in v.get("name", []):
                self.nameToType[name] = v.get("grammar")
            for ext in v["ext"]:
                self.extensions[ext] = v.get("grammar")
            fileTypes[k] = v
        if 0:
            log.info("extensions")
            for k, v in extensions.items():
                log.info("  ", k, ":", v)
            log.info("fileTypes")
            for k, v in fileTypes.items():
                log.info("  ", k, ":", v)
