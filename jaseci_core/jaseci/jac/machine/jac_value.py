"""
Variable manager for Jac

Representations for all jac runtime variables
"""
from jaseci.element.element import element
from jaseci.graph.node import node
from jaseci.graph.edge import edge
from jaseci.jac.jac_set import jac_set
import uuid

NoneType = type(None)


class JAC_TYPE:
    STR = 'JAC_TYPE.STR'
    INT = 'JAC_TYPE.INT'
    FLOAT = 'JAC_TYPE.FLOAT'
    LIST = 'JAC_TYPE.LIST'
    DICT = 'JAC_TYPE.DICT'
    BOOL = 'JAC_TYPE.BOOL'
    NODE = 'JAC_TYPE.NODE'
    EDGE = 'JAC_TYPE.EDGE'
    TYPE = 'JAC_TYPE.TYPE'
    NULL = 'JAC_TYPE.NULL'


def jac_type_wrap(val):
    if(isinstance(val, type)):
        if(val == str):
            val = JAC_TYPE.STR
        elif(val == int):
            val = JAC_TYPE.INT
        elif(val == float):
            val = JAC_TYPE.FLOAT
        elif(val == list):
            val = JAC_TYPE.LIST
        elif(val == jac_set):
            val = JAC_TYPE.LIST
        elif(val == dict):
            val = JAC_TYPE.DICT
        elif(val == bool):
            val = JAC_TYPE.BOOL
        elif(val == node):
            val = JAC_TYPE.NODE
        elif(val == edge):
            val = JAC_TYPE.EDGE
        elif(val == type):
            val = JAC_TYPE.TYPE
        elif(val == NoneType):
            val = JAC_TYPE.NULL
    return val


def jac_type_unwrap(val):
    if(type(val) == str and val.startswith('JAC_TYPE.')):
        if(val == JAC_TYPE.STR):
            val = str
        elif(val == JAC_TYPE.INT):
            val = int
        elif(val == JAC_TYPE.FLOAT):
            val = float
        elif(val == JAC_TYPE.LIST):
            val = list
        elif(val == JAC_TYPE.DICT):
            val = dict
        elif(val == JAC_TYPE.BOOL):
            val = bool
        elif(val == JAC_TYPE.NODE):
            val = node
        elif(val == JAC_TYPE.EDGE):
            val = edge
        elif(val == JAC_TYPE.TYPE):
            val = type
        elif(val == JAC_TYPE.NULL):
            val = NoneType
    return val


def is_jac_elem(val):
    """Test if value is jac element"""
    return type(val) == str and val.startswith("jac:uuid:")


def jac_elem_wrap(val, serialize_mode=False):
    if(serialize_mode):
        val = val.serialize()
    else:
        val = val.id.urn.replace('urn', 'jac')
    return val


def jac_elem_unwrap(val, parent):
    val = parent._h.get_obj(
        parent._m_id, uuid.UUID(val.replace('jac', 'urn')))
    return val


def jac_wrap_value(val, serialize_mode=False):
    """converts all elements to uuids in lists etc"""
    val = jac_type_wrap(val)
    if (isinstance(val, element)):
        val = jac_elem_wrap(val, serialize_mode=serialize_mode)
    elif(isinstance(val, jac_set)):
        val = jac_wrap_value(list(val), serialize_mode)
    elif (isinstance(val, list)):
        for i in range(len(val)):
            val[i] = jac_wrap_value(val[i], serialize_mode)
    elif (isinstance(val, dict)):
        for i in val.keys():
            val[i] = jac_wrap_value(val[i], serialize_mode)
    return val


def jac_unwrap_value(val, parent):
    """Reference to variables value"""
    if(is_jac_elem(val)):
        val = jac_elem_unwrap(val, parent=parent)
    elif (isinstance(val, list)):
        for i in range(len(val)):
            val[i] = jac_unwrap_value(val[i], parent=parent)
    elif (isinstance(val, dict)):
        for i in val.keys():
            val[i] = jac_unwrap_value(val[i], parent=parent)
    return jac_type_unwrap(val)


class jac_value():
    """
    A reference to a variable in context dict that is common for elements
    """

    def __init__(self, parent, value=None, ctx=None, name=None, end=None):
        """
        Abstraction of all Jac types, ctx and name serve as obj[key/idx]
        end is for idx ranges for list slices
        """
        self.parent = parent
        self.ctx = ctx
        self.is_element = False
        self.name = name
        self.end = end
        self.value = self.setup_value(value)

    def setup_value(self, value):
        if (isinstance(self.ctx, element)):
            self.is_element = self.ctx
            self.ctx = self.ctx.context
        if value is not None:
            return value
        elif(self.ctx is not None and self.name is not None):
            if(self.end is not None):
                return self.ctx[self.name:self.end]
            elif(type(self.name) == int or self.name in self.ctx.keys()):
                return self.ctx[self.name]
        else:
            return None

    def write(self, jac_ast, force=False):
        if(not force and self.is_element and self.name not in self.ctx.keys()
           and not self.parent.parent().
           check_in_arch_context(self.name, self.is_element)):
            self.parent.rt_error(
                f"Creating variable {self.name} in graph "
                f"element {type(self.is_element)} is not allowed, "
                "please define",
                jac_ast)
        elif(self.ctx is None or self.name is None):
            self.parent.rt_error(
                f"No valid live variable! ctx: {self.ctx} name: {self.name}",
                jac_ast)
        elif(self.end is not None):
            self.ctx[self.name:self.end] = self.wrap()
        else:
            self.ctx[self.name] = self.wrap()

    def self_destruct(self, jac_ast):
        if(self.is_element and self.name in self.ctx.keys()):
            self.parent.rt_error(
                f"Deleting {self.name} in graph element "
                f"{type(self.is_element)} is not allowed, try setting to null",
                jac_ast)
            return
        if(self.ctx is not None):
            try:
                del self.ctx[self.name]
            except Exception as e:
                self.parent.rt_error(f'{e}', jac_ast)
        else:
            self.parent.rt_error(
                f'{self.value} is not destroyable',
                jac_ast)

    def wrap(self, serialize_mode=False):
        "Caller for recursive wrap"
        self.value = jac_wrap_value(self.value, serialize_mode)
        return self.value

    def unwrap(self):
        "Caller for recursive unwrap"
        self.value = jac_unwrap_value(self.value, self.parent)
        return self.value

    def jac_type(self):
        """Return Jac type of value"""
        return jac_type_wrap(type(self.value))
