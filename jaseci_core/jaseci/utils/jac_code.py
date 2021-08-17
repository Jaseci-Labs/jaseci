"""
Mix in for jac code object in Jaseci
"""
import json
from jaseci.jac.code_gen.ast import ast


class jac_json_enc(json.JSONEncoder):
    """Custom Json encoder for Jac ASTs"""

    def default(self, obj):
        if(isinstance(obj, ast)):
            return obj.__dict__
        return super().default(obj)


class jac_json_dec(json.JSONDecoder):
    """Custom hook for decoding Jac ASTs"""

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(
            self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):

        if isinstance(obj, dict):
            if "start_rule" in obj and "kid" in obj:
                ret = ast()
                for i in ret.__dict__.keys():
                    setattr(ret, i, obj[i])
                return ret

        if isinstance(obj, dict):
            for key in list(obj):
                obj[key] = self.object_hook(obj[key])
            return obj

        if isinstance(obj, list):
            for i in range(0, len(obj)):
                obj[i] = self.object_hook(obj[i])
            return obj

        return obj


class jac_code():
    """Obj mixin to code pickling"""

    def __init__(self, code=None):
        self.code = json.dumps(cls=jac_json_enc, obj=code)
        self._jac_ast = json.loads(
            cls=jac_json_dec, s=self.code) if code else None
        if(self._jac_ast):
            kid = self._jac_ast.kid
            self.kind = f"{kid[0].token_text()}"
            self.name = f"{kid[1].token_text()}"
        self.save()
