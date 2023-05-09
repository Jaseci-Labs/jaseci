"""
Interpreter for jac code in AST form

This interpreter should be inhereted from the class that manages state
referenced through self.
"""
from copy import copy
from jaseci.utils.utils import logger
from jaseci.jsorc.live_actions import live_actions, load_preconfig_actions

# from jaseci.actions.find_action import find_action
from jaseci.prim.element import Element

from jaseci.jac.jac_set import JacSet
from jaseci.jac.machine.jac_scope import JacScope
from jaseci.utils.id_list import IdList
from jaseci.jac.ir.ast import Ast
from jaseci.prim.edge import Edge
from jaseci.prim.node import Node
from jaseci.jac.machine.jac_value import JacValue
from jaseci.jac.jsci_vm.op_codes import JsCmp
import time


class MachineState:
    """Shared interpreter class across both sentinels and walkers"""

    def __init__(self):
        self.report = []
        self.report_status = None
        self.report_custom = None
        self.request_context = None
        self.runtime_errors = []
        self.yielded_walkers_ids = IdList(self)
        self.ignore_node_ids = IdList(self)
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
        self._mast = self.get_master()

        self.inform_hook()

    def inform_hook(self):
        if hasattr(self, "_h"):
            self._h._machine = self

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
        self.profile_pause()
        self._scope_stack.append(scope)
        self._jac_scope = scope
        self.profile_in()

    def pop_scope(self):
        self.profile_out()
        self._scope_stack.pop()
        self._jac_scope = self._scope_stack[-1]
        self.profile_unpause()

    def profile_in(self):
        if self._mast and self._mast._profiling:
            self._jac_scope._start_time = time.time()
            self._jac_scope._per_call_start = time.time()

    def profile_out(self):
        if self._mast and self._mast._profiling:
            name = f"{self.kind}::{self.name}:{self._jac_scope.name}"
            if name not in self._mast._jac_profile:
                self._mast._jac_profile[name] = {
                    "calls": 1,
                    "time": self._jac_scope._total_time
                    + (time.time() - self._jac_scope._start_time),
                    "per_call": time.time() - self._jac_scope._per_call_start,
                }
            else:
                c = self._mast._jac_profile[name]["calls"]
                t = self._mast._jac_profile[name]["time"]
                p = self._mast._jac_profile[name]["per_call"]
                self._mast._jac_profile[name]["calls"] = c + 1
                self._mast._jac_profile[name]["time"] = (
                    t * c
                    + (
                        self._jac_scope._total_time
                        + (time.time() - self._jac_scope._start_time)
                    )
                ) / (c + 1)
                self._mast._jac_profile[name]["per_call"] = (
                    p * c + time.time() - self._jac_scope._per_call_start
                ) / (c + 1)

    def profile_pause(self):
        if self._mast and self._mast._profiling and self._jac_scope:
            self._jac_scope._total_time += time.time() - self._jac_scope._start_time
            self._jac_scope._start_time = None

    def profile_unpause(self):
        if self._mast and self._mast._profiling and self._jac_scope:
            self._jac_scope._start_time = time.time()

    def here(self):
        return self._scope_stack[-1].here() if self._scope_stack[-1] else None

    def visitor(self):
        return self._scope_stack[-1].visitor() if self._scope_stack[-1] else None

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

    def edge_to_node_jac_set(self, edge_set, location=None):
        """
        Returns nodes jac_set from edge jac_set from current node
        """
        ret = JacSet()
        if not location:
            location = self.here()
        for i in edge_set.obj_list():
            ret.add_obj(i.opposing_node(location))
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
