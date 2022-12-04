"""
Interpreter for jac code in AST form

This interpreter should be inhereted from the class that manages state
referenced through self.
"""
from copy import copy
from jaseci.utils.utils import logger
from jaseci.actions.live_actions import live_actions, load_preconfig_actions

# from jaseci.actions.find_action import find_action
from jaseci.element.element import Element

from jaseci.jac.jac_set import JacSet
from jaseci.jac.machine.jac_scope import JacScope
from jaseci.utils.id_list import IdList
from jaseci.jac.ir.ast import Ast
from jaseci.graph.edge import Edge
from jaseci.graph.node import Node
from jaseci.jac.machine.jac_value import JacValue
from jaseci.jac.jsci_vm.op_codes import JsCmp


class MachineState:
    """Shared interpreter class across both sentinels and walkers"""

    def __init__(self, parent_override=None, caller=None):
        self.report = []
        self.report_status = None
        self.report_custom = None
        self.request_context = None
        self.runtime_errors = []
        self.yielded_walkers_ids = IdList(self)
        self.ignore_node_ids = IdList(self)
        self._parent_override = parent_override
        if not isinstance(self, Element) and caller:
            self._m_id = caller._m_id
            self._h = caller._h
        self._scope_stack = [None]
        self._jac_scope = None
        self._relevant_edges = []
        self._loop_ctrl = None
        self._stopped = None
        self._assign_mode = False
        self._jac_try_mode = 0  # 0 is false, +=1 for each nested try
        self._loop_limit = 10000
        self._cur_jac_ast = Ast("none")
        self._write_candidate = None
        self.inform_hook()

    def inform_hook(self):
        if hasattr(self, "_h"):
            self._h._machine = self

    def parent(self):  # parent here is always a sentinel
        if self._parent_override:
            return self._parent_override
        else:
            return Element.parent(self)

    def reset(self):
        self.report = []
        self.report_status = None
        self.report_custom = None
        self.runtime_errors = []
        self._scope_stack = [None]
        self._jac_scope = None
        self._loop_ctrl = None
        self._stopped = None

    def push_scope(self, scope: JacScope):
        self._scope_stack.append(scope)
        self._jac_scope = scope

    def pop_scope(self):
        self._scope_stack.pop()
        self._jac_scope = self._scope_stack[-1]

    def set_cur_ast(self, jac_ast):
        self._cur_jac_ast = jac_ast
        return jac_ast.kid

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        for i in self.yielded_walkers_ids.obj_list():
            i.destroy()

    # Core State Management ##################
    def load_variable(self, name, assign_mode=None, jac_ast=None):
        val = self._jac_scope.get_live_var(
            name, create_mode=self._assign_mode if assign_mode is None else assign_mode
        )
        if val is None:
            self.rt_error(f"Variable not defined - {name}", jac_ast)
            self.push(JacValue(self))
        else:
            self.push(val)

    def candidate_writethrough(self):
        if self._write_candidate:
            self._write_candidate.save()
            self._write_candidate = None

    def perform_assignment(self, dest, src, jac_ast=None):
        if dest.check_assignable(jac_ast):
            dest.value = src.value
            dest.write(jac_ast)
        self.push(dest)

    def perform_copy_fields(self, dest, src, jac_ast=None):
        if dest.check_assignable(jac_ast):
            if not self.rt_check_type(dest.value, [Node, Edge], jac_ast):
                self.rt_error("Copy fields only applies to nodes and edges", jac_ast)
                self.push(dest)
            if dest.value.name != src.value.name:
                self.rt_error(
                    f"Node/edge arch {dest.value} don't match {src.value}!", jac_ast
                )
                self.push(dest)
            for i in src.value.context.keys():
                if i in dest.value.context.keys():
                    JacValue(
                        self, ctx=dest.value, name=i, value=src.value.context[i]
                    ).write(jac_ast)
        self.push(dest)

    def perform_increment(self, dest, src, op, jac_ast=None):
        if op == JsCmp.PEQ:
            dest.value = dest.value + src.value
        elif op == JsCmp.MEQ:
            dest.value = dest.value - src.value
        elif op == JsCmp.TEQ:
            dest.value = dest.value * src.value
        elif op == JsCmp.DEQ:
            dest.value = dest.value / src.value
        dest.write(jac_ast)
        self.push(dest)

    # Helper Functions ##################

    def inherit_runtime_state(self, mach):
        """Inherits runtime output state from another machine"""
        self.report += mach.report
        if mach.report_status:
            self.report_status = mach.report_status
        if mach.report_custom:
            self.report_custom = mach.report_custom
        self.runtime_errors += mach.runtime_errors

    def obj_set_to_jac_set(self, obj_set):
        """
        Returns nodes jac_set from edge jac_set from current node
        """
        ret = JacSet()
        for i in obj_set:
            ret.add_obj(i)
        return ret

    def edge_to_node_jac_set(self, edge_set):
        """
        Returns nodes jac_set from edge jac_set from current node
        """
        ret = JacSet()
        for i in edge_set.obj_list():
            ret.add_obj(i.opposing_node(self.current_node))
        return ret

    def edges_filter_on_nodes(self, edge_set, node_set):
        """
        Returns nodes jac_set from edge jac_set from current node
        """
        ret = JacSet()
        for i in edge_set.obj_list():
            for j in node_set.obj_list():
                if i.jid in j.smart_edge_list:
                    ret.add_obj(i)
                    break
        return ret

    def check_builtin_action(self, func_name, jac_ast=None):
        """
        Takes reference to action attr, finds the built in function
        and returns new name used as hook by action class
        """
        if func_name not in live_actions.keys():
            self.rt_warn(f"Attempting auto-load for {func_name}", jac_ast)
            load_preconfig_actions(self._h)
        if func_name not in live_actions.keys():
            self.rt_warn(f"Builtin action unable to be loaded - {func_name}", jac_ast)
            return False
        return True

    def jac_try_exception(self, e: Exception, jac_ast):
        if isinstance(e, TryException):
            raise e
        else:
            raise TryException(self.jac_exception(e, jac_ast))

    def jac_exception(self, e: Exception, jac_ast):
        return {
            "type": type(e).__name__,
            "mod": jac_ast.loc[2],
            "msg": str(e),
            "args": e.args,
            "line": jac_ast.loc[0],
            "col": jac_ast.loc[1],
            "name": self.name if hasattr(self, "name") else "blank",
            "rule": jac_ast.name,
        }

    def rt_log_str(self, msg, jac_ast=None):
        """Generates string for screen output"""
        if jac_ast is None:
            jac_ast = self._cur_jac_ast
        name = self.name if hasattr(self, "name") else "blank"
        if jac_ast:
            msg = (
                f"{jac_ast.loc[2]}:{name} - line {jac_ast.loc[0]}, "
                + f"col {jac_ast.loc[1]} - rule {jac_ast.name} - {msg}"
            )
        else:
            msg = f"{msg}"
        return msg

    def rt_warn(self, error, jac_ast=None):
        """Prints runtime error to screen"""
        error = self.rt_log_str(error, jac_ast)
        logger.warning(str(error))

    def rt_error(self, error, jac_ast=None):
        """Prints runtime error to screen"""
        if self._jac_try_mode:
            raise Exception(error)
        error = self.rt_log_str(error, jac_ast)
        logger.error(str(error))
        self.runtime_errors.append(error)

    def rt_info(self, msg, jac_ast=None):
        """Prints runtime info to screen"""
        logger.info(str(self.rt_log_str(msg, jac_ast)))

    def rt_check_type(self, obj, typ, jac_ast=None):
        """Prints error if type mismatach"""
        if not isinstance(typ, list):
            typ = [typ]
        for i in typ:
            if isinstance(obj, i):
                return True
        self.rt_error(
            f"Incompatible type for object "
            f"{obj} - {type(obj).__name__}, "
            f"expecting {typ}",
            jac_ast,
        )
        return False

    def get_info(self):
        return {
            "report": copy(self.report),
            "report_status": self.report_status,
            "report_custom": self.report_custom,
            "request_context": self.request_context,
            "runtime_errors": self.runtime_errors,
        }


class TryException(Exception):
    def __init__(self, ref: dict):
        super().__init__(ref["msg"])
        self.ref = ref
