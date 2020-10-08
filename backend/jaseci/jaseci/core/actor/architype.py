"""
Architype class for Jaseci

Each architype is a registered templatized version of instances of any Jaseci
abstractions or collections of instances (e.g., subgraphs, etc)
"""
from core.element import element
from core.jac.architype_machine import architype_machine
from core.jac.ast import ast


class architype(element, architype_machine):
    """Architype class for Jaseci"""

    def __init__(self, code=None, *args, **kwargs):
        self.code = code
        element.__init__(self, *args, **kwargs)
        architype_machine.__init__(self)

    def register(self, obj):
        """
        Registers element in architype by creating copy

        TODO: Known bug, copying objects with linked objects needs handling
        """
        new = obj.duplicate()
        new.owner_id = self.owner_id
        self.element_ids.add_obj(new)

    def run(self):
        """
        Create set of new object instances from architype
        """
        jac_ast = ast(jac_text=self.code,
                      parse_rule='architype')
        return self.run_architype(jac_ast=jac_ast)

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        super().destroy()
