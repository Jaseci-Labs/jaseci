"""
Variable manager for Jac

Representations for all jac runtime variables
"""
from jaseci.prim.element import Element
from jaseci.prim.obj_mixins import Anchored
from jaseci.prim.node import Node
from jaseci.prim.edge import Edge
from jaseci.prim.graph import Graph
from jaseci.jac.jac_set import JacSet
import uuid

NoneType = type(None)


class JacType:
    STR = "JAC_TYPE.STR"
    INT = "JAC_TYPE.INT"
    FLOAT = "JAC_TYPE.FLOAT"
    LIST = "JAC_TYPE.LIST"
    DICT = "JAC_TYPE.DICT"
    BOOL = "JAC_TYPE.BOOL"
    NODE = "JAC_TYPE.NODE"
    EDGE = "JAC_TYPE.EDGE"
    TYPE = "JAC_TYPE.TYPE"
    NULL = "JAC_TYPE.NULL"


def jac_type_wrap(val):
    if isinstance(val, type):
        if val == str:
            val = JacType.STR
        elif val == int:
            val = JacType.INT
        elif val == float:
            val = JacType.FLOAT
        elif val == list:
            val = JacType.LIST
        elif val == JacSet:
            val = JacType.LIST
        elif val == dict:
            val = JacType.DICT
        elif val == bool:
            val = JacType.BOOL
        elif val in [Node, Graph]:
            val = JacType.NODE
        elif val == Edge:
            val = JacType.EDGE
        elif val == type:
            val = JacType.TYPE
        elif val == NoneType:
            val = JacType.NULL
    return val


def jac_type_unwrap(val):
    if type(val) == str and val.startswith("JAC_TYPE."):
        if val == JacType.STR:
            val = str
        elif val == JacType.INT:
            val = int
        elif val == JacType.FLOAT:
            val = float
        elif val == JacType.LIST:
            val = list
        elif val == JacType.DICT:
            val = dict
        elif val == JacType.BOOL:
            val = bool
        elif val == JacType.NODE:
            val = Node
        elif val == JacType.EDGE:
            val = Edge
        elif val == JacType.TYPE:
            val = type
        elif val == JacType.NULL:
            val = NoneType
    return val


def is_jac_elem(val):
    """Test if value is jac element"""
    return type(val) == str and val.startswith("jac:uuid:")


def jac_elem_wrap(val, serialize_mode=False):
    if serialize_mode:
        if isinstance(val, Anchored):
            val.context = jac_wrap_value(val.context)
        val = val.serialize()
    else:
        val = val.jid.replace("urn", "jac")
    return val


def jac_elem_unwrap(val, parent):
    val = parent._h.get_obj(parent._m_id, val.replace("jac", "urn"))
    return val


def jac_wrap_value(val, serialize_mode=False):
    """converts all elements to uuids in lists etc"""
    val = jac_type_wrap(val)
    if isinstance(val, Element):
        val = jac_elem_wrap(val, serialize_mode=serialize_mode)
    elif isinstance(val, JacSet):
        val = jac_wrap_value(list(val), serialize_mode)
    elif isinstance(val, list):
        for i in range(len(val)):
            val[i] = jac_wrap_value(val[i], serialize_mode)
    elif isinstance(val, dict):
        for i in val.keys():
            val[i] = jac_wrap_value(val[i], serialize_mode)
    return val


def jac_unwrap_value(val, parent):
    """Reference to variables value"""
    if is_jac_elem(val):
        val = jac_elem_unwrap(val, parent=parent)
    elif isinstance(val, list):
        for i in range(len(val)):
            val[i] = jac_unwrap_value(val[i], parent=parent)
    elif isinstance(val, dict):
        for i in val.keys():
            val[i] = jac_unwrap_value(val[i], parent=parent)
    return jac_type_unwrap(val)


class JacValue:
    """
    A reference to a variable in context dict that is common for elements
    """

    def __init__(
        self, parent, value=None, ctx=None, name=None, end=None, create_mode=False
    ):
        """
        Abstraction of all Jac types, ctx and name serve as obj[key/idx]
        end is for idx ranges for list slices
        """
        self.parent = parent
        self.ctx = ctx
        self.is_element = False
        self.name = name
        self.end = end
        self.value = self.setup_value(value, create_mode=create_mode)

    def setup_value(self, value, create_mode):
        if isinstance(self.ctx, Element):
            self.is_element = self.ctx
            if self.parent._assign_mode:
                self.is_element.save()
            self.ctx = self.ctx.context
        if value is not None:
            return value
        elif self.ctx is not None and self.name is not None:
            if self.end is not None:
                return self.ctx[self.name : self.end]
            elif type(self.name) == int or self.name in self.ctx.keys():
                return self.ctx[self.name]
            elif (
                not self.parent._assign_mode
                and not create_mode
                and (
                    not self.is_element
                    or self.name not in self.is_element.get_architype().has_vars
                )
            ):
                self.parent.rt_error(
                    f"Key {self.name} not found in object/dict.",
                    self.parent._cur_jac_ast,
                )
        else:
            return None

    def write(self, jac_ast, force=False):
        if (
            not force
            and self.is_element
            and self.name not in self.ctx.keys()
            and self.name not in self.is_element.get_architype().has_vars
        ):
            self.parent.rt_error(
                f"Creating variable {self.name} in graph "
                f"element {type(self.is_element)} is not allowed, "
                "please define",
                jac_ast,
            )
        elif self.ctx is None or self.name is None:
            self.parent.rt_error(
                f"No valid live variable! ctx: {self.ctx} name: {self.name}", jac_ast
            )
        elif self.end is not None:
            self.ctx[self.name : self.end] = self.value
        else:
            self.ctx[self.name] = self.value

    def check_assignable(self, jac_ast=None):
        if self.ctx is None:
            self.parent.rt_error("Cannot assign to this value", jac_ast)
            return False
        return True

    def self_destruct(self, jac_ast):
        if self.is_element and self.name in self.ctx.keys():
            self.ctx[self.name] = None  # assumes interp has destroyed element
        elif self.ctx is not None:
            try:
                del self.ctx[self.name]
            except Exception as e:
                self.parent.rt_error(f"{e}", jac_ast)
        else:
            self.parent.rt_error(
                f"{self.value} is not destroyable, try setting to null", jac_ast
            )

    def jac_type(self):
        """Return Jac type of value"""
        return jac_type_wrap(type(self.value))

    def __str__(self):
        return (
            "JacValue:" + str(self.ctx) + ":" + str(self.name) + ":" + str(self.value)
        )
