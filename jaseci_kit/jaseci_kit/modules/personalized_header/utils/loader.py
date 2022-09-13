import torch.nn as nn
import collections

# class Builder(object):
#     def __init__(self, *namespaces):
#         self._namespace = collections.ChainMap(*namespaces)

#     def __call__(self, name, *args, **kwargs):
#         try:
#             return self._namespace[name](*args, **kwargs)
#         except Exception as e:
#             raise e.__class__(str(e), name, args, kwargs) from e

#     def add_namespace(self, namespace, index=-1):
#         if index >= 0:
#             namespaces = self._namespace.maps
#             namespaces.insert(index, namespace)
#             self._namespace = collections.ChainMap(*namespaces)
#         else:
#             self._namespace = self._namespace.new_child(namespace)


# def build_network(architecture, builder=Builder(nn.__dict__)):
#     layers = []
#     for block in architecture:
#         assert len(block) == 1
#         name, kwargs = list(block.items())[0]
#         if kwargs is None:
#             kwargs = {}
#         args = kwargs.pop("args", [])
#         layers.append(builder(name, *args, **kwargs))
#     return nn.Sequential(*layers)