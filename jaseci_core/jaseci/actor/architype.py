"""
Architype class for Jaseci

Each architype is a registered templatized version of instances of any Jaseci
abstractions or collections of instances (e.g., subgraphs, etc)
"""
from jaseci.element import element
from jaseci.jac.architype_machine import architype_machine
from jaseci.utils.jac_code import jac_code


class architype(element, jac_code, architype_machine):
    """Architype class for Jaseci"""

    def __init__(self, code=None, *args, **kwargs):
        jac_code.__init__(self, code)
        element.__init__(self, *args, **kwargs)
        architype_machine.__init__(self)

    def run(self):
        """
        Create set of new object instances from architype if needed
        """
        return self.run_architype(jac_ast=self._jac_ast)

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        super().destroy()
