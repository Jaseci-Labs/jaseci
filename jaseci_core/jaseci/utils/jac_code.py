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
