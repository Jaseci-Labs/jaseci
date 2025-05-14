from __future__ import annotations
from jaclang.runtimelib.builtin import *
from jaclang import JacMachineInterface as _
if _.TYPE_CHECKING:
    from time import sleep, time
else:
    sleep, time = _.py_jac_import('time', __file__, lng='py', items={'sleep': None, 'time': None})

class A(_.Node):
    val: int = 0

    @_.entry
    def do(self, here) -> None:
        print('Started')
        sleep(2)
        print(here)

class B(_.Walker):
    name: str

def add(x: int, y: int) -> int:
    print(x)
    z = x + y
    sleep(2)
    print(x)
    return z
start = time()
t1 = _.thread_run(lambda: _.spawn(A(), B('Thami')))
task1 = _.thread_run(lambda: add(1, 10))
task2 = _.thread_run(lambda: add(2, 11))
print('All are started')
res1 = _.thread_wait(task1)
res2 = _.thread_wait(task2)
print('All are done')
print(res1)
print(res2)
print(time() - start)