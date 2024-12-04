"""Module to track executed branches and variables
"""

import types
from typing import Optional, Callable
import threading
import sys
import copy
import os
import traceback
import dis
from collections import deque
import inspect
import warnings
import ast


class CfgDeque:
    def __init__(self, max_size: int = 10):
        self.__max_size = max_size
        self.__deque = deque()

    def add_cfg(self, cfg_repr: str):
        self.__deque.append(cfg_repr)
        if len(self.__deque) > self.__max_size:
            self.__deque.popleft()

    def get_cfg_repr(self):
      res = [f"CFG Changes in last {len(self.__deque)} Updates:\n"]
      for idx, cfg in enumerate(self.__deque):
        res.append(f"\nCFG {idx+1} of {len(self.__deque)}\n")
        res.append(cfg)
      
      return "".join(res)


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
        # print(cpy)
        self.curr_variables_lock.release()

        return cpy

    def trace_callback(
        self, frame: types.FrameType, event: str, arg: any
    ) -> Optional[Callable]:
        """Trace function to track executed branches"""
        code = frame.f_code
        if ".jac" not in code.co_filename:
            return self.trace_callback

        if event == "call":
            frame.f_trace_opcodes = True
        elif event == "opcode":
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
        elif event == "line":
            ###
            # this is really circumlocutious, but is also how
            # [watchpoints](https://github.com/gaogaotiantian/watchpoints/tree/master)
            # works
            ###
            try:
                #print(inspect.getsourcefile(frame.f_code))
                #print(frame.f_lineno)
                # TODO: super inefficient but just for now
                # inspect.getsource doesn't seem to work like it does for
                # regular python (see test_tracer.py)
                # NOTE: we're parsing jac lines as python, fingers crossed
                with open(inspect.getsourcefile(frame.f_code)) as file:
                    line_asts = ast.parse(file.readlines()[frame.f_lineno - 1].lstrip().rstrip(';'))
                #print("                       ", frame.f_lineno, ast.unparse(line_ast))
            except (IndexError, SyntaxError):
                return self.trace_callback
            #print(ast.dump(a))
            #print(len(a.body))
            assert len(line_asts.body) == 1 # we only parsed one line
            line_ast = line_asts.body[0]
            if isinstance(line_ast, ast.Assign) or isinstance(line_ast, ast.AugAssign):
                # yes, I know this isn't strictly necessary in python
                lhs_ast = None
                rhs_ast = None
                if isinstance(line_ast, ast.Assign):
                    assert len(line_ast.targets) == 1, "Only handling single targets right now"
                    lhs_ast = line_ast.targets[0]
                elif isinstance(line_ast, ast.AugAssign):
                    lhs_ast = line_ast.target
                lhs_var = ast.unparse(lhs_ast)
                rhs_ast = line_ast.value
                # NOTE: for some reason, eval(ast.Expression(rhs_ast)) doesn't work
                rhs_value = eval(ast.unparse(rhs_ast), frame.f_globals, frame.f_locals)
                if isinstance(line_ast, ast.Assign):
                    exec(f"{lhs_var} = {rhs_value}\n", frame.f_globals, frame.f_locals)
                    print(f"{lhs_var} = {rhs_value}")
                elif isinstance(line_ast, ast.AugAssign):
                    exec(f"{lhs_var} += {rhs_value}\n", frame.f_globals, frame.f_locals)
                    print(f"{lhs_var} (+)= {rhs_value}")
                #print(frame.f_locals)
                if lhs_var == 'PROGRAM_INPUT':
                    if isinstance(line_ast, ast.AugAssign):
                        assert False, "Unimplemented"
                    print("tracer: PROGRAM_INPUT = ", rhs_value)
                # this only silences some of the
                # "RuntimeWarning: assigning None to unbound local" warnings
                with warnings.catch_warnings(action="ignore"):
                    frame.f_lineno += 1
        return self.trace_callback
