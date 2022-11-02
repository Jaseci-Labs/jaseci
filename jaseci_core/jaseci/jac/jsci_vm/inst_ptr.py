from jaseci.jac.jsci_vm.op_codes import JsOp
from struct import unpack


def from_bytes(typ, val):
    if typ == str:
        if val is None:
            return ""
        return val.decode("unicode_escape")
    if typ == float:
        return unpack("d", val)[0]
    else:
        if val is None:
            return 0
        return typ.from_bytes(val, "little")


class InstPtr:
    def __init__(self):
        self._ip = 0
        self._bytecode = None

    def offset(self, delta, range=None):
        if range == 0:
            return None
        elif range is not None:
            return self._bytecode[self._ip + delta : self._ip + delta + range]
        return self._bytecode[self._ip + delta]

    def cur_op(self):
        return JsOp(self.offset(0)).name
