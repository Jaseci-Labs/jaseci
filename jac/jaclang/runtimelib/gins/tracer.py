import types
from typing import Optional, Callable
import threading
import sys
import copy
import os
from collections import deque


class CfgDeque:
    def __init__(self, max_size: int = 10):
        self.__max_size = max_size
        self.__deque = deque()

    def add_cfg(self, cfg_repr: str):
        self.__deque.append(cfg_repr)
        if len(self.__deque) > self.__max_size:
            self.__deque.popleft()

    def display_cfgs(self):
        print("CFG change over updates\n")
        for cfg in self.__deque:
            print("\n")
            print(cfg)


class CFGTracker:
    def __init__(self):
        self.executed_insts = {}
        self.inst_lock = threading.Lock()

        self.curr_variables_lock = threading.Lock()
        self.curr_variables = {}

    def start_tracking(self):
        """Start tracking branch coverage"""
        frame = sys._getframe()
        frame.f_trace_opcodes = True
        sys.settrace(self.trace_callback)

    def stop_tracking(self):
        """Stop tracking branch coverage"""
        sys.settrace(None)

    def get_exec_inst(self):
        self.inst_lock.acquire()
        cpy = copy.deepcopy(self.executed_insts)
        self.executed_insts = {}
        self.inst_lock.release()

        return cpy

    def get_variable_values(self):
        self.curr_variables_lock.acquire()
        cpy = copy.deepcopy(self.curr_variables)
        print(cpy)
        self.curr_variables_lock.release()

        return cpy

    def trace_callback(
        self, frame: types.FrameType, event: str, arg: any
    ) -> Optional[Callable]:
        if event == "call":
            frame.f_trace_opcodes = True

        """Trace function to track executed branches"""
        code = frame.f_code
        if ".jac" not in code.co_filename:
            return self.trace_callback

        if event == "opcode":
            # edge case to handle executing code not within a function
            filename = os.path.basename(code.co_filename)
            module = (
                code.co_name
                if code.co_name != "<module>"
                else os.path.splitext(filename)[0]
            )

            self.inst_lock.acquire()
            if module not in self.executed_insts:
                self.executed_insts[module] = []
            self.executed_insts[module].append(frame.f_lasti)
            self.inst_lock.release()
            variable_dict = {}
            if "__annotations__" in frame.f_locals:
                self.curr_variables_lock.acquire()
                for var_name in frame.f_locals["__annotations__"]:
                    variable_dict[var_name] = frame.f_locals[var_name]
                self.curr_variables[module] = (frame.f_lasti, variable_dict)
                self.curr_variables_lock.release()

        return self.trace_callback
