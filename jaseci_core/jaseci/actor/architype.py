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
        return id_list(
            self,
            in_list=self.entry_action_ids
            + self.activity_action_ids
            + self.exit_action_ids,
        )

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
