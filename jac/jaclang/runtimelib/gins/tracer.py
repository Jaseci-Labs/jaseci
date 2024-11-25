import types
from typing import Optional, Union, Callable
import threading
import sys
import copy
import os

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
        self.curr_variables_lock.release()
        
        return cpy
    
    
    def trace_callback(self, frame: types.FrameType, event: str, arg: any) -> Optional[Callable]:
        if event == "call":
            frame.f_trace_opcodes = True
        # frame.f_trace_lines = False
    #     def tracefunc(frame, event, arg):
    #         if event == 'call':
    #             frame.f_trace_opcodes = True
    #         elif event == 'opcode':
    #             if frame.f_code.co_code[frame.f_lasti] == dis.opmap['MAKE_FUNCTION']:
    #                 makefunctiontracefunc(frame)
    # return tracefunc
                
        """Trace function to track executed branches"""        
        code = frame.f_code
        if ".jac" not in code.co_filename:
            return self.trace_callback
        


        # if event != 'line':
        #     return self.trace_callback
        
        if event == 'opcode':
            # print(frame.f_lasti)
        
        # print(frame.f_lineno, frame.f_lasti)
        
        #edge case to handle executing code not within a function
            filename = os.path.basename(code.co_filename)
            module = code.co_name if code.co_name != "<module>" else os.path.splitext(filename)[0]
    
            self.inst_lock.acquire()
            if module not in self.executed_insts:
                self.executed_insts[module] = []
            self.executed_insts[module].append(frame.f_lasti)
            self.inst_lock.release()
            variable_dict = {}
            if '__annotations__' in frame.f_locals:
                self.curr_variables_lock.acquire()
                for var_name in frame.f_locals['__annotations__']:
                    variable_dict[var_name] = frame.f_locals[var_name]
                self.curr_variables[module] = (frame.f_lasti, variable_dict)
                self.curr_variables_lock.release()

        # self.variable_values[code.co_name][frame.f_lineno] = {}

                
        # print(f"{frame.f_lineno}")
        # print(f"Function Name: {code.co_name}") 
        # print(f"Filename: {code.co_filename}") 
        # print(f"First Line Number: {code.co_firstlineno}") 
        # print(f"Argument Count: {code.co_argcount}") 
        # print(f"Constants: {code.co_consts}") 
        # print(f"Local Variables: {code.co_varnames}")

        # if event != 'line':
        #     return self.trace_callback

        # code = frame.f_code
        # if code not in self.cfg_cache:
        #     self.build_cfg(code)

        # # Find current basic block
        # blocks = self.cfg_cache[code]
        # current_offset = frame.f_lasti

        # # Find the block containing this offset
        # current_block = None
        # for block in blocks.values():
        #     if block.offset <= current_offset <= block.offset + sum(inst.size for inst in block.instructions):
        #         current_block = block
        #         break

        # if current_block:
        #     current_block.hits += 1
        #     # Record taken branches
        #     for next_block in current_block.next:
        #         self.coverage_data[code].add(
        #             (current_block.offset, next_block.offset))

        return self.trace_callback