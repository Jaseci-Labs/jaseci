"""
Interpreter for jac code in AST form

This interpreter should be inhereted from the class that manages state
referenced through self.
"""
from jaseci.utils.utils import logger
from jaseci.actions.live_actions import live_actions, load_preconfig_actions
# from jaseci.actions.find_action import find_action
from jaseci.element.element import element

from jaseci.jac.jac_set import jac_set
from jaseci.jac.machine.jac_scope import jac_scope


class machine_state():
    """Shared interpreter class across both sentinels and walkers"""

    def __init__(self, parent_override=None, caller=None):
        self.report = []
        self.report_status = None
        self.runtime_errors = []
        self._parent_override = parent_override
        if(not isinstance(self, element) and caller):
            self._m_id = caller._m_id
            self._h = caller._h
        self._scope_stack = [None]
        self._jac_scope = None
        self._loop_ctrl = None
        self._stopped = None
        self._assign_mode = False
        self._loop_limit = 10000
        self._cur_jac_ast = None

    def parent(self):
        if(self._parent_override):
            return self._parent_override
        else:
            return element.parent(self)

    def reset(self):
        self.report = []
        self.report_status = None
        self.runtime_errors = []
        self._scope_stack = [None]
        self._jac_scope = None
        self._loop_ctrl = None
        self._stopped = None

    def push_scope(self, scope: jac_scope):
        self._scope_stack.append(scope)
        self._jac_scope = scope

    def pop_scope(self):
        self._scope_stack.pop()
        self._jac_scope = self._scope_stack[-1]

    def set_cur_ast(self, jac_ast):
        self._cur_jac_ast = jac_ast
        return jac_ast.kid

    # Helper Functions ##################

    def get_arch_for(self, obj):
        """Returns the architype that matches object"""
        return self.parent().arch_ids.get_obj_by_name(
            name=obj.name, kind=obj.kind)

    def obj_set_to_jac_set(self, obj_set):
        """
        Returns nodes jac_set from edge jac_set from current node
        """
        ret = jac_set()
        for i in obj_set:
            ret.add_obj(i)
        return ret

    def edge_to_node_jac_set(self, edge_set):
        """
        Returns nodes jac_set from edge jac_set from current node
        """
        ret = jac_set()
        for i in edge_set.obj_list():
            ret.add_obj(i.opposing_node(self.current_node))
        return ret

    def get_builtin_action(self, func_name, jac_ast=None):
        """
        Takes reference to action attr, finds the built in function
        and returns new name used as hook by action class
        """
        if(func_name not in live_actions.keys()):
            load_preconfig_actions(self._h)
        if(func_name not in live_actions.keys()):
            self.rt_error(f"Builtin action not found - {func_name}", jac_ast)
        return func_name

    def jac_exception(self, e: Exception, jac_ast):
        return {'type': type(e).__name__,
                'mod': jac_ast.mod_name,
                'msg': str(e),
                'args': e.args,
                'line': jac_ast.line,
                'col': jac_ast.column}

    def rt_log_str(self, msg, jac_ast=None):
        """Generates string for screen output"""
        name = self.name if hasattr(self, 'name') else 'blank'
        if(jac_ast):
            msg = f'{jac_ast.mod_name}:{name} - line {jac_ast.line}, ' + \
                f'col {jac_ast.column} - rule {jac_ast.name} - {msg}'
        else:
            msg = f'{msg}'
        return msg

    def rt_warn(self, error, jac_ast=None):
        """Prints runtime error to screen"""
        error = self.rt_log_str(error, jac_ast)
        logger.warning(
            str(error)
        )
        self.runtime_errors.append(error)

    def rt_error(self, error, jac_ast=None):
        """Prints runtime error to screen"""
        error = self.rt_log_str(error, jac_ast)
        logger.error(
            str(error)
        )
        self.runtime_errors.append(error)

    def rt_info(self, msg, jac_ast=None):
        """Prints runtime info to screen"""
        logger.info(
            str(self.rt_log_str(msg, jac_ast))
        )

    def rt_check_type(self, obj, typ, jac_ast=None):
        """Prints error if type mismatach"""
        if(not isinstance(typ, list)):
            typ = [typ]
        for i in typ:
            if (isinstance(obj, i)):
                return True
        self.rt_error(f'Incompatible type for object '
                      f'{obj} - {type(obj).__name__}, '
                      f'expecting {typ}', jac_ast)
        return False
