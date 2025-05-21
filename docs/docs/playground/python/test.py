from jaclang.runtimelib.builtin import dotgen
from jaclang.runtimelib.machinestate import JacMachineState

__jac_mach__ = JacMachineState()

def bar():
    return 'bar called'

def foo():
    print('foo:line1')
    print('foo:line2')
    print('foo:line3')


foo()
print('main:line1')
