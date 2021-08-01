"""
Mix in for jac code object in Jaseci
"""
import pickle


class jac_code():
    """Obj mixin to code pickling"""

    def __init__(self, code=None):
        self.code = pickle.dumps(code, 0).decode()
        self._jac_ast = pickle.loads(
            self.code.encode()) if code else None
        if(self._jac_ast):
            kid = self._jac_ast.kid
            self.kind = f"{kid[0].token_text()}"
            self.name = f"{kid[1].token_text()}"
        self.save()
