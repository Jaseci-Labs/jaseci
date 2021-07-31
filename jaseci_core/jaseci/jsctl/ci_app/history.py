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
"""
  Track user history to provide features such as resuming editing at the same
  cursor position after reloading a file; or a recent file list.
"""

# For Python 2to3 support.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = OSError

try:
    import cPickle as pickle
except ImportError:
    import pickle
import hashlib
import os
import time

from . import log


def calculate_checksum(filePath, data=None):
    """
    Calculates the hash value of the specified file.
    The second argument can be passed in if a file's data has
    already been read so that you do not have to read the file again.

    Args:
      filePath (str): The absolute path to the file.
      data (str): Defaults to None. This is the data
        returned by calling read() on a file object.

    Returns:
      The hash value of the file's data.
    """
    log.info("Calculate checksum of the current file")
    hasher = hashlib.sha512()
    try:
        if data is not None:
            if len(data) == 0:
                return None
            hasher.update(data.encode(u"utf-8"))
        else:
            with open(filePath, "rb") as dataFile:
                data = dataFile.read()
                if len(data) == 0:
                    return None
                hasher.update(data)
        return hasher.hexdigest()
    except FileNotFoundError as e:
        pass
    except Exception as e:
        log.exception(e)
    return None


def calculate_file_size(filePath):
    """
    Calculates the size of the specified value.

    Args:
      filePath (str): The absolute path to the file.

    Returns:
      The size of the file in bytes.
    """
    try:
        return os.stat(filePath).st_size
    except FileNotFoundError:
        pass
    except Exception as e:
        log.exception(e)
    return 0


def get_file_info(filePath, data=None):
    """
    Returns the hash value and size of the specified file.
    The second argument can be passed in if a file's data has
    already been read so that you do not have to read the file again.

    Args:
      filePath (str): The absolute path to the file.
      data (str): Defaults to None. This is the data
        returned by calling read() on a file object.

    Returns:
      A tuple containing the checksum and size of the file.
    """
    checksum = calculate_checksum(filePath, data)
    fileSize = calculate_file_size(filePath)
    return (checksum, fileSize)


class History:
    def __init__(self, pathToHistory):
        self.userHistory = {}
        self.pathToHistory = pathToHistory

    def load_user_history(self):
        """
        Retrieves the user's complete edit history for all files.

        Returns:
          None.
        """
        if os.path.isfile(self.pathToHistory):
            with open(self.pathToHistory, "rb") as historyFile:
                try:
                    self.userHistory = pickle.load(historyFile)
                except ValueError as e:
                    log.info(unicode(e))

    def save_user_history(self, fileInfo, fileHistory):
        """
        Saves the user's file history by writing to a pickle file.

        Args:
          fileInfo (tuple): Contains (filePath, lastChecksum, lastFileSize).
          fileHistory (dict): The history of the file that the user wants to
                              save.

        Returns:
          None.
        """
        filePath, lastChecksum, lastFileSize = fileInfo
        try:
            if self.pathToHistory is not None:
                self.userHistory.pop((lastChecksum, lastFileSize), None)
                newChecksum, newFileSize = get_file_info(filePath)
                if newChecksum is None:
                    log.info(u"Failed to checksum", repr(filePath))
                    return
                self.userHistory[(newChecksum, newFileSize)] = fileHistory
                with open(self.pathToHistory, "wb") as historyFile:
                    pickle.dump(self.userHistory, historyFile)
                log.info("wrote pickle")
        except Exception as e:
            log.exception(e)

    def get_file_history(self, filePath, data=None):
        """
        Takes in an file path and an optimal data
        argument and checks for the current file's history.
        It stores the current time in the file history and
        returns the file history. The second argument can be
        passed in if a file's data has already been read
        so that you do not have to read the file again.

        Args:
          filePath (str): The absolute path to the file.
          data (str): Defaults to None. This is the data
            returned by calling read() on a file object.

        Returns:
          The file history (dict) of the desired file if it exists.
        """
        checksum, fileSize = get_file_info(filePath, data)
        if checksum is None:
            fileHistory = {}
        else:
            fileHistory = self.userHistory.get((checksum, fileSize), {})
        fileHistory["adate"] = time.time()
        return fileHistory

    def get_recent_files(self):
        """
        Returns:
          A list of file paths to recently accessed files.
        """
        files = []
        for entry in self.userHistory.values():
            path = entry.get("path")
            if path is not None:
                files.append(path)
        return files

    def clear_user_history(self):
        """
        Clears user history for all files.

        Args:
          None.

        Returns:
          None.
        """
        self.userHistory = {}
        try:
            os.remove(self.pathToHistory)
            log.info("user history cleared")
        except Exception as e:
            log.error("clear_user_history exception", e)
