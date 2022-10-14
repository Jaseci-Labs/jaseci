from jaseci.jac.ir.passes import IrPass
from jaseci.jac.jsci_vm.op_codes import JsOp, JsAttr
from base64 import b64encode


def byte_length(val):
    if type(val) == str:
        return len(val)
    else:
        return (val.bit_length() + 7) // 8


def to_bytes(val):
    if type(val) == str:
        return bytes(val, "utf-8")
    else:
        return val.to_bytes(byte_length(val), "little")


class CodeGenPass(IrPass):
    def __init__(self, debug_info=True, **kwargs):
        super().__init__(**kwargs)
        self.bytecode = bytearray()
        self.debug_info = debug_info
        self.cur_loc = None

    def emit(self, *items):
        for i in items:
            if type(i) is bytes:
                self.bytecode += bytearray(i)
            elif type(i) is str:
                self.bytecode += bytearray(i, "utf-8")
            else:
                self.bytecode.append(i)

    def emit_debug_info(self, node):
        node_loc = [node.loc[0], node.loc[2]]
        if not self.debug_info or self.cur_loc == node_loc:
            return
        self.emit(
            JsOp.DEBUG_INFO,
            byte_length(node_loc[0]),
            to_bytes(node_loc[0]),
        )
        if not self.cur_loc or self.cur_loc[1] != node_loc[1]:
            self.emit(byte_length(node_loc[1]), to_bytes(node_loc[1]))
        else:
            self.emit(0)
        self.cur_loc = node_loc

    def enter_node(self, node):
        # print("entering", node)
        if hasattr(self, f"enter_{node.name}"):
            self.emit_debug_info(node)
            getattr(self, f"enter_{node.name}")(node)

    def exit_node(self, node):
        # print("exiting", node)
        if hasattr(self, f"exit_{node.name}"):
            self.emit_debug_info(node)
            getattr(self, f"exit_{node.name}")(node)

    def exit_any_type(self, node):
        node.bytecode = b64encode(self.bytecode).decode()

    # def enter_walker_block(self, node):
    #     self.emit(JsOp.PUSH_SCOPE)

    # def exit_walker_block(self, node):
    #     self.emit(JsOp.POP_SCOPE)

    # def exit_arithmetic(self, node):
    #     self.emit(JsOp.ADD if node.kid[1].name == "PLUS" else JsOp.SUB)

    # def exit_report_action(self, node):
    #     self.emit(JsOp.REPORT)

    def exit_TYP_STRING(self, node):  # noqa
        self.emit(JsOp.LOAD_CONST, JsAttr.TYPE, JsAttr.STRING)

    def exit_TYP_INT(self, node):  # noqa
        self.emit(JsOp.LOAD_CONST, JsAttr.TYPE, JsAttr.INT)

    def exit_TYP_FLOAT(self, node):  # noqa
        self.emit(JsOp.LOAD_CONST, JsAttr.TYPE, JsAttr.FLOAT)

    def exit_TYP_LIST(self, node):  # noqa
        self.emit(JsOp.LOAD_CONST, JsAttr.TYPE, JsAttr.LIST)

    def exit_TYP_DICT(self, node):  # noqa
        self.emit(JsOp.LOAD_CONST, JsAttr.TYPE, JsAttr.DICT)

    def exit_TYP_BOOL(self, node):  # noqa
        self.emit(JsOp.LOAD_CONST, JsAttr.TYPE, JsAttr.BOOL)

    def exit_KW_NODE(self, node):  # noqa
        self.emit(JsOp.LOAD_CONST, JsAttr.TYPE, JsAttr.NODE)

    def exit_KW_EDGE(self, node):  # noqa
        self.emit(JsOp.LOAD_CONST, JsAttr.TYPE, JsAttr.EDGE)

    def exit_KW_TYPE(self, node):  # noqa
        self.emit(JsOp.LOAD_CONST, JsAttr.TYPE, JsAttr.TYPE)

    # def exit_INT(self, node):  # noqa
    #     val = int(node.token_text())
    #     self.emit(
    #         JsOp.LOAD_CONST,
    #         JsAttr.INT,
    #         byte_length(val),
    #         to_bytes(val),
    #     )
