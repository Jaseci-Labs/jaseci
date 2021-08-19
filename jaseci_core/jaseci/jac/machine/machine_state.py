"""
Interpreter for jac code in AST form

This interpreter should be inhereted from the class that manages state
referenced through self.
"""
from jaseci.utils.utils import logger
from jaseci.actions.utils.find_action import find_action
from jaseci.element import element

from jaseci.jac.jac_set import jac_set
from jaseci.jac.machine.jac_scope import jac_scope


class machine_state():
    """Shared interpreter class across both sentinels and walkers"""

    def __init__(self, owner_override=None):
        self.report = []
        self.runtime_errors = []
        self._owner_override = owner_override
        self._scope_stack = [None]
        self._jac_scope = None
        self._loop_ctrl = None
        self._stopped = None
        self._loop_limit = 10000

    def owner(self):
        if(self._owner_override):
            return self._owner_override
        else:
            return element.owner(self)

    def reset(self):
        self.report = []
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

    # Helper Functions ##################

    def parse_str_token(self, s):
        return str(bytes(s, "utf-8").
                   decode("unicode_escape")[1:-1])

    def obj_set_to_jac_set(self, obj_set):
        """
        Returns nodes jac_set from edge jac_set from current node
        """
        ret = jac_set(self)
        for i in obj_set:
            ret.add_obj(i)
        return ret

    def edge_to_node_jac_set(self, edge_set):
        """
        Returns nodes jac_set from edge jac_set from current node
        """
        ret = jac_set(edge_set.owner_obj)
        for i in edge_set.obj_list():
            ret.add_obj(i.opposing_node(self.current_node))
        return ret

    def get_builtin_action(self, func_name, jac_ast=None):
        """
        Takes reference to action attr, finds the built in function
        and returns new name used as hook by action class
        """
        ret = find_action(func_name)
        if(not ret):
            self.rt_error(f"Builtin action not found - {func_name}", jac_ast)
        return ret

    def rt_log_str(self, msg, jac_ast=None):
        """Generates string for screen output"""
        name = self.name if hasattr(self, 'name') else 'blank'
        if(jac_ast):
            msg = f'{name} - line {jac_ast.line}, ' + \
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
