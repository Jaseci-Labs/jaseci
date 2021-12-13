"""
Variable manager for Jac

Representations for all jac runtime variables
"""
from jaseci.element.element import element
from jaseci.graph.node import node
from jaseci.graph.edge import edge
from jaseci.utils.utils import logger
import uuid


class JAC_TYPE:
    NULL = 'null'
    TRUE = 'true'
    FALSE = 'false'
    STR = 'JAC_TYPE.STR'
    INT = 'JAC_TYPE.INT'
    FLOAT = 'JAC_TYPE.FLOAT'
    LIST = 'JAC_TYPE.LIST'
    DICT = 'JAC_TYPE.DICT'
    BOOL = 'JAC_TYPE.BOOL'
    NODE = 'JAC_TYPE.NODE'
    EDGE = 'JAC_TYPE.EDGE'
    TYPE = 'JAC_TYPE.TYPE'


def jac_type_wrap(val):
    if(val == str):
        val = JAC_TYPE.STR
    elif(val == int):
        val = JAC_TYPE.INT
    elif(val == float):
        val = JAC_TYPE.FLOAT
    elif(val == list):
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
        self.name = name
        self.end = end
        self.value = value if value is not None else ctx[name:end] \
            if ctx is not None and name is not None and end is not None \
            else ctx[name] if ctx is not None and name is not None and \
            (type(name) == int or name in ctx.keys()) else None

    def write(self):
        if(self.ctx is None or self.name is None):
            logger.critical(
                f"No valid live variable! ctx: {self.ctx} name: {self.name}")
        if(self.end is not None):
            self.ctx[self.name:self.end] = self.wrap()
        else:
            self.ctx[self.name] = self.wrap()

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
