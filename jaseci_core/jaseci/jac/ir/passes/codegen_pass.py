from jaseci.jac.ir.passes import IrPass
from jaseci.jac.jsci_vm.op_codes import JsCmp, JsOp, JsType
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
            if not i.is_terminal() and not self.has_bytecode(i) and i.name != "cmp_op":
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

    def exit_logical(self, node):
        if self.is_bytecode_complete(node):
            for i in reversed(node.kid):
                if self.has_bytecode(i):
                    self.emit(node, i.bytecode)
            for i in node.kid:
                if i.name == "KW_AND":
                    self.emit(node, JsOp.AND)
                elif i.name == "KW_OR":
                    self.emit(node, JsOp.OR)

    def exit_compare(self, node):
        if self.is_bytecode_complete(node):
            for i in reversed(node.kid):
                if self.has_bytecode(i):
                    self.emit(node, i.bytecode)
            for i in node.kid:
                if i.name == "NOT":
                    self.emit(node, JsOp.COMPARE, JsCmp.NOT)
                elif i.name == "cmp_op" and i.kid[0].name == "EE":
                    self.emit(node, JsOp.COMPARE, JsCmp.EE)
                elif i.name == "cmp_op" and i.kid[0].name == "LT":
                    self.emit(node, JsOp.COMPARE, JsCmp.LT)
                elif i.name == "cmp_op" and i.kid[0].name == "GT":
                    self.emit(node, JsOp.COMPARE, JsCmp.GT)
                elif i.name == "cmp_op" and i.kid[0].name == "LTE":
                    self.emit(node, JsOp.COMPARE, JsCmp.LTE)
                elif i.name == "cmp_op" and i.kid[0].name == "GTE":
                    self.emit(node, JsOp.COMPARE, JsCmp.GTE)
                elif i.name == "cmp_op" and i.kid[0].name == "NE":
                    self.emit(node, JsOp.COMPARE, JsCmp.NE)
                elif i.name == "cmp_op" and i.kid[0].name == "KW_IN":
                    self.emit(node, JsOp.COMPARE, JsCmp.IN)
                elif i.name == "cmp_op" and i.kid[0].name == "nin":
                    self.emit(node, JsOp.COMPARE, JsCmp.NIN)

    def exit_arithmetic(self, node):
        if self.is_bytecode_complete(node):
            for i in reversed(node.kid):
                if self.has_bytecode(i):
                    self.emit(node, i.bytecode)
            for i in node.kid:
                if i.name == "PLUS":
                    self.emit(node, JsOp.ADD)
                elif i.name == "MINUS":
                    self.emit(node, JsOp.SUBTRACT)

    def exit_term(self, node):
        if self.is_bytecode_complete(node):
            for i in reversed(node.kid):
                if self.has_bytecode(i):
                    self.emit(node, i.bytecode)
            for i in node.kid:
                if i.name == "STAR_MUL":
                    self.emit(node, JsOp.MULTIPLY)
                elif i.name == "DIV":
                    self.emit(node, JsOp.DIVIDE)
                elif i.name == "MOD":
                    self.emit(node, JsOp.MODULO)

    def exit_factor(self, node):
        if self.is_bytecode_complete(node):
            self.emit(node, node.kid[-1].bytecode)
            if node.kid[0].name == "MINUS":
                self.emit(node, JsOp.NEGATE)

    def exit_power(self, node):
        if self.is_bytecode_complete(node):
            for i in reversed(node.kid):
                if self.has_bytecode(i):
                    self.emit(node, i.bytecode)
            for i in node.kid:
                if i.name == "POW":
                    self.emit(node, JsOp.POWER)

    def exit_atom(self, node):  # TODO: Incomplete
        kid = node.kid
        if kid[0].name == "INT":
            val = int(kid[0].token_text())
            self.emit(
                node, JsOp.LOAD_CONST, JsType.INT, byte_length(val), to_bytes(val)
            )
        elif kid[0].name == "FLOAT":
            val = float(kid[0].token_text())
            self.emit(node, JsOp.LOAD_CONST, JsType.FLOAT, to_bytes(val))
        elif kid[0].name == "STRING":
            val = parse_str_token(kid[0].token_text())
            self.emit(node, JsOp.LOAD_CONST, JsType.STRING, byte_length(val))
            if byte_length(val) > 0:
                self.emit(node, to_bytes(val))
        elif kid[0].name == "BOOL":
            val = int(kid[0].token_text() == "true")
            self.emit(node, JsOp.LOAD_CONST, JsType.BOOL, val)
        elif kid[0].name == "NULL":
            self.emit(node, JsOp.LOAD_CONST, JsType.TYPE, JsType.NULL)
        elif kid[0].name == "NAME":
            name = kid[0].token_text()
            self.emit(node, JsOp.LOAD_VAR, byte_length(name), to_bytes(name))

    def exit_any_type(self, node):
        kid = node.kid
        if kid[0].name == "TYP_STRING":
            self.emit(node, JsOp.LOAD_CONST, JsType.TYPE, JsType.STRING)
        elif kid[0].name == "TYP_INT":
            self.emit(node, JsOp.LOAD_CONST, JsType.TYPE, JsType.INT)
        elif kid[0].name == "TYP_FLOAT":
            self.emit(node, JsOp.LOAD_CONST, JsType.TYPE, JsType.FLOAT)
        elif kid[0].name == "TYP_LIST":
            self.emit(node, JsOp.LOAD_CONST, JsType.TYPE, JsType.LIST)
        elif kid[0].name == "TYP_DICT":
            self.emit(node, JsOp.LOAD_CONST, JsType.TYPE, JsType.DICT)
        elif kid[0].name == "TYP_BOOL":
            self.emit(node, JsOp.LOAD_CONST, JsType.TYPE, JsType.BOOL)
        elif kid[0].name == "KW_NODE":
            self.emit(node, JsOp.LOAD_CONST, JsType.TYPE, JsType.NODE)
        elif kid[0].name == "KW_EDGE":
            self.emit(node, JsOp.LOAD_CONST, JsType.TYPE, JsType.EDGE)
        elif kid[0].name == "KW_TYPE":
            self.emit(node, JsOp.LOAD_CONST, JsType.TYPE, JsType.TYPE)
