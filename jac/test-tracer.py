import sys
import dis
import traceback
import types
from typing import Optional, Callable
import inspect
import ast
import ctypes
import warnings

program_input = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]

def foo(x):
    PROGRAM_INPUT = program_input
    x = x + x
    for i in PROGRAM_INPUT:
        SPECIAL_VARIABLE = i
        print("foo: SPECIAL_VARIABLE = ", i)
    y = 2 * x
    x += y
    print("foo: x = ", x)
    print("foo: y = ", y)
    return x

def trace(frame: types.FrameType, event: str, arg: any) -> Optional[Callable]:
    if event == 'call':
        # TODO: this example itself doesn't need opcode events
        frame.f_trace_opcodes = True
        # keep using this function as the local tracer for this function
        frame.f_trace = trace
        return trace
    elif event == 'opcode':
        #print(dis.opname[frame.f_code.co_code[frame.f_lasti]])
        #print((frame.f_code.co_code[frame.f_lasti]))
        return trace
    elif event == 'line':
        #skip_line: Bool = getattr(trace, 'skip_line', False)
        #if skip_line:
        #    #print(f"Skipped {frame.f_lineno}")
        #    return trace
        ###
        # this is really circumlocutious, but is also how
        # [watchpoints](https://github.com/gaogaotiantian/watchpoints/tree/master)
        # works
        ###
        s = inspect.getsource(frame.f_code)
        #print(s)
        o = frame.f_lineno - frame.f_code.co_firstlineno
        l = s.split('\n')[o].lstrip()
        try:
            a = ast.parse(l)
        except SyntaxError:
            return trace
        #print(ast.dump(a))
        assert len(a.body) == 1 # we only parsed one line
        line_ast = a.body[0]
        if isinstance(line_ast, ast.Assign) or isinstance(line_ast, ast.AugAssign):
            # yes, I know this isn't strictly necessary in python
            lhs_ast = None
            rhs_ast = None
            if isinstance(line_ast, ast.Assign):
                assert len(line_ast.targets) == 1, "Only handling single targets right now"
                lhs_ast = line_ast.targets[0]
            elif isinstance(line_ast, ast.AugAssign):
                lhs_ast = line_ast.target
            lhs_var = lhs_ast.id
            rhs_ast = line_ast.value
            # NOTE: for some reason, eval(ast.Expression(rhs_ast)) doesn't work
            rhs_value = eval(ast.unparse(rhs_ast), frame.f_globals, frame.f_locals)
            #frame.f_locals[lhs_var] = rhs_value
            #ctypes.pythonapi.PyFrame_LocalsToFast(ctypes.py_object(frame), ctypes.c_int(0))
            #if lhs_var in frame.f_locals:
            #    frame.f_locals[lhs_var] = rhs_value
            #elif lhs_var in frame.f_globals:
            #    frame.f_globals[lhs_var] = rhs_value
            #else:
            #    assert False, "I'm pretty sure this doesn't handle closures correctly, but we don't need that for this hack anyways"
            # evaluating rhs again (after trace returns) would duplicate any
            # side effects, so let's "skip" this line in the user program
            #print("uhoh ", frame.f_lineno)
            #trace.skip_line = True
            #frame.f_lineno += 1
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
        return trace
    elif event == 'return':
        return None
    else:
        assert False

print("Starting")
# TODO use sys.monitoring instead?
# needs to be set before settrace due to python 3.12 bug
# https://github.com/python/cpython/issues/114480#issuecomment-1906518084
inspect.currentframe().f_trace_opcodes = True
sys.settrace(trace)
foo(1)
foo(2)
print("Finished")
