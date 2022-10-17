from jaseci.jac.ir.passes import IrPass
from jaseci.jac.jsci_vm.op_codes import JsOp, JsAttr
from struct import pack

from jaseci.utils.utils import parse_str_token


def byte_length(val):
    if type(val) == str:
        return len(val)
    else:
        return (val.bit_length() + 7) // 8


def to_bytes(val):
    if type(val) == str:
        return bytes(val, "utf-8")
    elif type(val) == float:
        return pack("d", val)
    elif type(val) == int:
        return val.to_bytes(byte_length(val), "little")


class CodeGenPass(IrPass):
    def __init__(self, debug_info=True, **kwargs):
        super().__init__(**kwargs)
        self.debug_info = debug_info
        self.cur_loc = None

    def emit(self, node, *items):
        if not self.has_bytecode(node):
            node.bytecode = bytearray()
        node_loc = [node.loc[0], node.loc[2]]
        if self.debug_info and self.cur_loc != node_loc:
            debug_inst = [
                JsOp.DEBUG_INFO,
                byte_length(node_loc[0]),
                to_bytes(node_loc[0]),
            ]
            if not self.cur_loc or self.cur_loc[1] != node_loc[1]:
                debug_inst += [byte_length(node_loc[1]), to_bytes(node_loc[1])]
            else:
                debug_inst += [0]
            self.cur_loc = node_loc
            items = debug_inst + list(items)
        for i in items:
            if type(i) in [bytes, bytearray]:
                node.bytecode += bytearray(i)
            elif type(i) is str:
                node.bytecode += bytearray(i, "utf-8")
            else:
                node.bytecode.append(i)

    def is_bytecode_complete(self, node):
        for i in node.kid:
            if not i.is_terminal() and not self.has_bytecode(i):
                return False
        return True

    def has_bytecode(self, node):
        if not hasattr(node, "bytecode"):
            return False
        return True

    def enter_node(self, node):
        # print("entering", node)
        if hasattr(self, f"enter_{node.name}"):
            getattr(self, f"enter_{node.name}")(node)

    def exit_node(self, node):
        # print("exiting", node)
        if hasattr(self, f"exit_{node.name}"):
            getattr(self, f"exit_{node.name}")(node)

    def exit_arithmetic(self, node):
        if self.is_bytecode_complete(node):
            for i in reversed(node.kid):
                if self.has_bytecode(i):
                    self.emit(node, i.bytecode)
            for i in node.kid:
                if i.name == "PLUS":
                    self.emit(node, JsOp.ADD)
                elif i.name == "MINUS":
                    self.emit(node, JsOp.SUB)

    def exit_factor(self, node):
        pass

    def exit_atom(self, node):  # TODO: Incomplete
        kid = node.kid
        if kid[0].name == "INT":
            val = int(kid[0].token_text())
            self.emit(
                node, JsOp.LOAD_CONST, JsAttr.INT, byte_length(val), to_bytes(val)
            )
        elif kid[0].name == "FLOAT":
            val = float(kid[0].token_text())
            self.emit(node, JsOp.LOAD_CONST, JsAttr.FLOAT, to_bytes(val))
        elif kid[0].name == "STRING":
            val = parse_str_token(kid[0].token_text())
            self.emit(node, JsOp.LOAD_CONST, JsAttr.STRING, byte_length(val))
            if byte_length(val) > 0:
                self.emit(node, to_bytes(val))
        elif kid[0].name == "BOOL":
            val = int(kid[0].token_text() == "true")
            self.emit(node, JsOp.LOAD_CONST, JsAttr.BOOL, val)
        elif kid[0].name == "NULL":
            self.emit(node, JsOp.LOAD_CONST, JsAttr.TYPE, JsAttr.NULL)
        elif kid[0].name == "NAME":
            name = kid[0].token_text()
            self.emit(node, JsOp.LOAD_VAR, byte_length(name), to_bytes(name))

    def exit_any_type(self, node):
        kid = node.kid
        if kid[0].name == "TYP_STRING":
            self.emit(node, JsOp.LOAD_CONST, JsAttr.TYPE, JsAttr.STRING)
        elif kid[0].name == "TYP_INT":
            self.emit(node, JsOp.LOAD_CONST, JsAttr.TYPE, JsAttr.INT)
        elif kid[0].name == "TYP_FLOAT":
            self.emit(node, JsOp.LOAD_CONST, JsAttr.TYPE, JsAttr.FLOAT)
        elif kid[0].name == "TYP_LIST":
            self.emit(node, JsOp.LOAD_CONST, JsAttr.TYPE, JsAttr.LIST)
        elif kid[0].name == "TYP_DICT":
            self.emit(node, JsOp.LOAD_CONST, JsAttr.TYPE, JsAttr.DICT)
        elif kid[0].name == "TYP_BOOL":
            self.emit(node, JsOp.LOAD_CONST, JsAttr.TYPE, JsAttr.BOOL)
        elif kid[0].name == "KW_NODE":
            self.emit(node, JsOp.LOAD_CONST, JsAttr.TYPE, JsAttr.NODE)
        elif kid[0].name == "KW_EDGE":
            self.emit(node, JsOp.LOAD_CONST, JsAttr.TYPE, JsAttr.EDGE)
        elif kid[0].name == "KW_TYPE":
            self.emit(node, JsOp.LOAD_CONST, JsAttr.TYPE, JsAttr.TYPE)
