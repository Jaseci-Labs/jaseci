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
        if not hasattr(node, "bytecode"):
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
            if type(i) is bytes:
                node.bytecode += bytearray(i)
            elif type(i) is str:
                node.bytecode += bytearray(i, "utf-8")
            else:
                node.bytecode.append(i)

    def enter_node(self, node):
        # print("entering", node)
        if hasattr(self, f"enter_{node.name}"):
            getattr(self, f"enter_{node.name}")(node)

    def exit_node(self, node):
        # print("exiting", node)
        if hasattr(self, f"exit_{node.name}"):
            getattr(self, f"exit_{node.name}")(node)

    def exit_atom(self, node):
        if len(node.kid) == 1 and hasattr(node.kid[0], "bytecode"):
            node.bytecode = node.kid[0].bytecode

    def exit_any_type(self, node):
        node.bytecode = node.kid[0].bytecode

    def exit_TYP_STRING(self, node):  # noqa
        self.emit(node, JsOp.LOAD_CONST, JsAttr.TYPE, JsAttr.STRING)

    def exit_TYP_INT(self, node):  # noqa
        self.emit(node, JsOp.LOAD_CONST, JsAttr.TYPE, JsAttr.INT)

    def exit_TYP_FLOAT(self, node):  # noqa
        self.emit(node, JsOp.LOAD_CONST, JsAttr.TYPE, JsAttr.FLOAT)

    def exit_TYP_LIST(self, node):  # noqa
        self.emit(node, JsOp.LOAD_CONST, JsAttr.TYPE, JsAttr.LIST)

    def exit_TYP_DICT(self, node):  # noqa
        self.emit(node, JsOp.LOAD_CONST, JsAttr.TYPE, JsAttr.DICT)

    def exit_TYP_BOOL(self, node):  # noqa
        self.emit(node, JsOp.LOAD_CONST, JsAttr.TYPE, JsAttr.BOOL)

    def exit_KW_NODE(self, node):  # noqa
        self.emit(node, JsOp.LOAD_CONST, JsAttr.TYPE, JsAttr.NODE)

    def exit_KW_EDGE(self, node):  # noqa
        self.emit(node, JsOp.LOAD_CONST, JsAttr.TYPE, JsAttr.EDGE)

    def exit_KW_TYPE(self, node):  # noqa
        self.emit(node, JsOp.LOAD_CONST, JsAttr.TYPE, JsAttr.TYPE)

    def exit_INT(self, node):  # noqa
        val = int(node.token_text())
        self.emit(
            node,
            JsOp.LOAD_CONST,
            JsAttr.INT,
            byte_length(val),
            to_bytes(val),
        )

    def exit_FLOAT(self, node):  # noqa
        val = float(node.token_text())
        self.emit(
            node,
            JsOp.LOAD_CONST,
            JsAttr.FLOAT,
            to_bytes(val),
        )

    def exit_STRING(self, node):  # noqa
        val = parse_str_token(node.token_text())
        self.emit(
            node,
            JsOp.LOAD_CONST,
            JsAttr.STRING,
            byte_length(val),
        )
        if byte_length(val) > 0:
            self.emit(node, to_bytes(val))

    def exit_BOOL(self, node):  # noqa
        val = int(node.token_text() == "true")
        self.emit(
            node,
            JsOp.LOAD_CONST,
            JsAttr.BOOL,
            val,
        )

    def exit_NULL(self, node):  # noqa
        self.emit(
            node,
            JsOp.LOAD_CONST,
            JsAttr.TYPE,
            JsAttr.NULL,
        )
