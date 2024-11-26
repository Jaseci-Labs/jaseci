import sys
import time

def g():
    a = 0
    for _ in range(100000):
        a += 1
    return a

def f():
    for _ in range(10):
        g()

events = 0

def trace(frame, event, arg):
    frame.f_trace_opcodes = True
    if event == 'opcode':
        print(frame.)
    return trace


sys.settrace(trace)
start = time.time()
f()
print(time.time() - start)
sys.settrace(None)
print(events)