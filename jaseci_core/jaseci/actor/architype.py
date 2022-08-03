"""
Architype class for Jaseci

Each architype is a registered templatized version of instances of any Jaseci
abstractions or collections of instances (e.g., subgraphs, etc)
"""
from jaseci.element.element import element
from jaseci.jac.interpreter.architype_interp import architype_interp
from jaseci.jac.ir.jac_code import jac_code
from jaseci.utils.id_list import id_list


class architype(element, jac_code, architype_interp):
    """Architype class for Jaseci"""

    def __init__(self, code_ir=None, *args, **kwargs):
        self.super_archs = list()
        self.entry_action_ids = id_list(self)
        self.activity_action_ids = id_list(self)
        self.exit_action_ids = id_list(self)
        element.__init__(self, *args, **kwargs)
        jac_code.__init__(self, code_ir)
        architype_interp.__init__(self)

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
        actions = id_list(self)
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
