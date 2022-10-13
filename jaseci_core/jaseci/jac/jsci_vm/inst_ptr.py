from jaseci.jac.jsci_vm.op_codes import JsOp


def from_bytes(typ, val):
    if typ == str:
        return val.decode("utf-8")
    else:
        return typ.from_bytes(val, "little")


class InstPtr:
    def __init__(self):
        self._ip = 0
        self._bytecode = None

    def offset(self, delta, range=0):
        if range:
            return self._bytecode[self._ip + delta : self._ip + delta + range]
        return self._bytecode[self._ip + delta]

    def cur_op(self):
        return JsOp(self.offset(0)).name
