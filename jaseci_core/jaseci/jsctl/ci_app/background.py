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

# For Python 2to3 support.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    unicode
except NameError:
    unicode = str
    unichr = chr

import os

try:
    import Queue as queue
except ImportError:
    import queue
import signal
import sys
import threading
import time
import traceback

from . import config, log
from . import profile
from . import render


class InstructionQueue(queue.Queue):
    def __init__(self, *args, **keywords):
        queue.Queue.__init__(self, *args, **keywords)

    def get(self, *args, **keywords):
        result = queue.Queue.get(self, *args, **keywords)
        if config.strict_debug:
            assert isinstance(result, tuple), repr(result)
            assert isinstance(result[0], unicode), repr(result[0])
        return result[0], result[1]

    def empty(self, *args, **keywords):
        # This thread yield (time.sleep(0)) dramatically improves Python3
        # performance. Without this line empty() will be called far too often.
        time.sleep(0)
        return queue.Queue.empty(self, *args, **keywords)

    def put(self, instruction, message):
        if config.strict_debug:
            assert isinstance(instruction, unicode), repr(instruction)
        queue.Queue.put(self, (instruction, message))


class BackgroundThread(threading.Thread):
    def __init__(self, programWindow, toBackground, fromBackground, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self._programWindow = programWindow
        self._toBackground = toBackground
        self._fromBackground = fromBackground

    def get(self):
        return self._fromBackground.get()

    def has_message(self):
        return not self._fromBackground.empty()

    def has_user_event(self):
        return not self._toBackground.empty()

    def put(self, instruction, message):
        self._toBackground.put(instruction, message)

    def run(self):
        cmdCount = 0
        block = True
        pid = os.getpid()
        signalNumber = signal.SIGUSR1
        programWindow = self._programWindow
        while True:
            try:
                try:
                    instruction, message = self._toBackground.get(block)
                    # profile = profile.begin_python_profile()
                    if instruction == u"quit":
                        log.info("bg received quit message")
                        return
                    elif instruction == u"cmdList":
                        log.info(programWindow, message)
                        programWindow.execute_command_list(message)
                    else:
                        assert False, instruction
                    block = programWindow.short_time_slice()
                    programWindow.render()
                    # debugging only: programWindow.show_window_hierarchy()
                    cmdCount += len(message)
                    programWindow.program.backgroundFrame.set_cmd_count(
                        cmdCount)
                    self._fromBackground.put(
                        u"render", programWindow.program.backgroundFrame.grab_frame()
                    )
                    os.kill(pid, signalNumber)
                    # profile.end_python_profile(profile)
                    time.sleep(0)  # See note in has_message().
                    if block or not self._toBackground.empty():
                        continue
                except queue.Empty:
                    pass
                block = programWindow.long_time_slice()
                if block:
                    programWindow.render()
                    programWindow.program.backgroundFrame.set_cmd_count(
                        cmdCount)
                    self._fromBackground.put(
                        u"render", programWindow.program.backgroundFrame.grab_frame()
                    )
                    os.kill(pid, signalNumber)
            except Exception as e:
                log.exception(e)
                log.error("bg thread exception", e)
                errorType, value, tracebackInfo = sys.exc_info()
                out = traceback.format_exception(
                    errorType, value, tracebackInfo)
                self._fromBackground.put(u"exception", out)
                os.kill(pid, signalNumber)
                while True:
                    instruction, message = self._toBackground.get()
                    if instruction == u"quit":
                        log.info("bg received quit message")
                        return


def startup_background(programWindow):
    toBackground = InstructionQueue()
    fromBackground = InstructionQueue()
    bg = BackgroundThread(programWindow, toBackground, fromBackground)
    bg.setName("ci_edit_bg")
    bg.setDaemon(True)
    bg.start()
    return bg
