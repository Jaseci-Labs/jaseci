"""
Architype class for Jaseci

Each architype is a registered templatized version of instances of any Jaseci
abstractions or collections of instances (e.g., subgraphs, etc)
"""
from jaseci.element.element import Element
from jaseci.jac.interpreter.architype_interp import ArchitypeInterp
from jaseci.jac.ir.jac_code import JacCode
from jaseci.utils.id_list import IdList


class Architype(Element, JacCode, ArchitypeInterp):
    """Architype class for Jaseci"""

    def __init__(self, code_ir=None, *args, **kwargs):
        self.super_archs = list()
        self.anchor_var = None
        self.private_vars = []
        self.entry_action_ids = IdList(self)
        self.activity_action_ids = IdList(self)
        self.exit_action_ids = IdList(self)
        Element.__init__(self, *args, **kwargs)
        JacCode.__init__(self, code_ir)
        ArchitypeInterp.__init__(self)

    def run(self):
        """
        Create set of new object instances from architype if needed
        """
        return self.run_architype(jac_ast=self.get_jac_ast())

    def get_jac_ast(self):
        if not self._jac_ast:
            self.refresh()
        return self._jac_ast

    def get_all_actions(self):
        actions = IdList(self)
        for i in self.arch_with_supers():
            actions += i.entry_action_ids + i.activity_action_ids + i.exit_action_ids
        return actions

    def arch_with_supers(self):
        archs = [self]
        for i in self.super_archs:
            obj = self.parent().arch_ids.get_obj_by_name(name=i, kind=self.kind)
            archs += obj.arch_with_supers()
        return archs

    def derived_types(self):
        names = []
        for i in self.arch_with_supers():
            names += i.super_archs + [i.name]
        return names

    def is_instance(self, name):
        return name in self.derived_types()

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        des = (
            self.activity_action_ids.obj_list()
            + self.entry_action_ids.obj_list()
            + self.exit_action_ids.obj_list()
        )
        for i in des:
            i.destroy()
        super().destroy()
