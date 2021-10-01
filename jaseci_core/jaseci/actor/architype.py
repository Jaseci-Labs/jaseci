"""
Architype class for Jaseci

Each architype is a registered templatized version of instances of any Jaseci
abstractions or collections of instances (e.g., subgraphs, etc)
"""
from jaseci.element.element import element
from jaseci.jac.interpreter.architype_interp import architype_interp
from jaseci.jac.ir.jac_code import jac_code


class architype(element, jac_code, architype_interp):
    """Architype class for Jaseci"""

    def __init__(self, code_ir=None, *args, **kwargs):
        element.__init__(self, *args, **kwargs)
        jac_code.__init__(self, code_ir)
        architype_interp.__init__(self)

    def run(self):
        """
        Create set of new object instances from architype if needed
        """
        if(not self._jac_ast):
            self.refresh()
        return self.run_architype(jac_ast=self._jac_ast)

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        super().destroy()
