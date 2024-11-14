
from __future__ import annotations
from jaclang.lib import *



from jaclang.plugin.feature import JacFeature as _Jac
from jaclang.plugin.builtin import *
from dataclasses import dataclass as __jac_dataclass__

"""

class Foo(JacObj):
    a1: int = 1
    a2: int = 2

    def do_something(self):
        print("Doing something")

class MyNode(JacNode):
    pass

class MyWalker(JacWalker):

    @with_entry
    def do_entry(self, here):
        print("here = ", here)

a_walker = MyWalker()
a_node = MyNode()


a_walker.spawn(a_node)
spawn(a_walker, a_node)

# _Jac.spawn_call(w, n)

# @_Jac.make_walker(on_entry=[_Jac.DSFunc('do_entry', MyNode)], on_exit=[])
# @__jac_dataclass__(eq=False)
# class MyWalker(_Jac.Walker):

#     def do_entry(self, _jac_here_: MyNode) -> None:
#         print('here =', _jac_here_)

# print(Foo())
"""



class MyNode(JacNode):
    val: int = 0

class a(JacEdge):
    pass

class b(JacEdge):
    pass

class c(JacEdge):
    pass

Start = MyNode(5)

root = _Jac.get_root()

connect(root, Start, a) # _Jac.connect(left=_Jac.get_root(), right=Start, edge_spec=_Jac.build_edge(is_undirected=False, conn_type=a, conn_assign=None))

i1 = MyNode(10)
connect(Start, i1, b)
connect(i1, MyNode(15), c)

i2 = MyNode(20)
connect(Start, i2, b)
connect(i2, MyNode(25), a)

print(_Jac.edge_ref(_Jac.get_root(), target_obj=None, dir=_Jac.EdgeDir.OUT, filter_func=None, edges_only=False))
print(_Jac.edge_ref(_Jac.get_root(), target_obj=None, dir=_Jac.EdgeDir.IN, filter_func=None, edges_only=False))
print(_Jac.edge_ref(_Jac.get_root(), target_obj=None, dir=_Jac.EdgeDir.OUT, filter_func=lambda x: [i for i in x if isinstance(i, a)], edges_only=False))
print(_Jac.edge_ref(_Jac.edge_ref(_Jac.get_root(), target_obj=None, dir=_Jac.EdgeDir.OUT, filter_func=lambda x: [i for i in x if isinstance(i, a)], edges_only=False), target_obj=None, dir=_Jac.EdgeDir.OUT, filter_func=lambda x: [i for i in x if isinstance(i, b)], edges_only=False))
print(_Jac.edge_ref(_Jac.edge_ref(_Jac.edge_ref(_Jac.get_root(), target_obj=None, dir=_Jac.EdgeDir.OUT, filter_func=lambda x: [i for i in x if isinstance(i, a)], edges_only=False), target_obj=None, dir=_Jac.EdgeDir.OUT, filter_func=lambda x: [i for i in x if isinstance(i, b)], edges_only=False), target_obj=None, dir=_Jac.EdgeDir.OUT, filter_func=lambda x: [i for i in x if isinstance(i, c)], edges_only=False))


# from __future__ import annotations
# from jaclang.plugin.feature import JacFeature as _Jac
# from jaclang.plugin.builtin import *
# from dataclasses import dataclass as __jac_dataclass__
#
#
# class Meta(type):
#
#     def __new__(cls, name, bases, dct):
#         cls = super().__new__(cls, name, bases, dct)
#         cls = __jac_dataclass__(eq=False)(cls)
#         cls = _Jac.make_node(on_entry=[], on_exit=[])(cls)
#         return cls
#
#
# class Base(metaclass=Meta):
#     pass
#
#
# class Foo(Base):
#     pass
#
# print(Foo())

# @_Jac.make_node(on_entry=[], on_exit=[])
# @__jac_dataclass__(eq=False)
# class MyNode(_Jac.Node):
#     pass
#
# # Print all the parent class names of MyNode
# def print_parents(node):
#     print(node.__class__.__name__)
#     if hasattr(node, 'parent'):
#         print_parents(node.parent)
#
# print_parents(MyNode())
