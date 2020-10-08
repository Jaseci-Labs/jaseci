"""
machine for jac code in AST form

This machine should be inhereted from the class that manages state referenced
through self.
"""
from core.utils.utils import logger
from core.actions.find_action import find_action
from core.graph.node import node
from core.element import ctx_value
from core.attr.action import action


class machine():
    """Shared machine class across both sentinels and walkers"""

    def __init__(self):
        self.runtime_errors = []

    def reset(self):
        self.runtime_errors = []

    def run_attr_stmt(self, jac_ast, obj):
        """
        attr_stmt: has_stmt | can_stmt;
        """
        kid = jac_ast.kid
        if(kid[0].name == 'has_stmt'):
            self.run_has_stmt(kid[0], obj)
        elif(kid[0].name == 'can_stmt'):
            self.run_can_stmt(kid[0], obj)

    def run_has_stmt(self, jac_ast, obj):
        """
        has_stmt: KW_HAS KW_ANCHOR? NAME (COMMA NAME)* SEMI;
        """
        kid = jac_ast.kid
        kid = kid[1:]
        while True:
            if(kid[0].name == 'KW_ANCHOR'):
                kid = kid[1:]
                if('anchor' in dir(obj)):
                    if(obj.anchor is None):
                        obj.anchor = kid[0].token_text()
                else:
                    self.rt_error('anchors not allowed for this type',
                                  kid[0])
            ctx_name = kid[0].token_text()
            if (ctx_name not in obj.context.keys()):
                obj.context[ctx_name] = ""
            kid = kid[1:]
            if(not len(kid) or kid[0].name != 'COMMA'):
                break
            else:
                kid = kid[1:]

    def run_can_stmt(self, jac_ast, obj):
        """
        can_stmt:
            KW_CAN dotted_name preset_in_out? (KW_WITH KW_MOVE)? (
                COMMA dotted_name preset_in_out? (KW_WITH KW_MOVE)?
            )* SEMI;
        """
        kid = jac_ast.kid
        kid = kid[1:]
        while True:
            action_type = 'activity'
            preset_in_out = {'input': [], 'output': None}
            action_name = self.run_dotted_name(kid[0])
            kid = kid[1:]
            if(len(kid) > 0 and kid[0].name == 'preset_in_out'):
                preset_in_out = self.run_preset_in_out(kid[0], obj)
                kid = kid[1:]
            if(len(kid) > 0 and kid[0].name == 'KW_WITH'):
                action_type = kid[1].token_text()
                kid = kid[2:]
            if(not isinstance(obj, node)):  # only nodes have on entry/exit
                action_type = 'activity'
            func_link = \
                self.get_builtin_action(action_name, jac_ast)
            if(func_link):
                getattr(obj, f"{action_type}_action_ids").add_obj(
                    action(
                        h=self._h,
                        name=action_name,
                        value=func_link,
                        preset_in_out=preset_in_out
                    )
                )
            if(not len(kid) or kid[0].name != 'COMMA'):
                break
            else:
                kid = kid[1:]

    def run_preset_in_out(self, jac_ast, obj):
        """
        preset_in_out: DBL_COLON NAME (COMMA NAME)* (COLON_OUT NAME)?;
        """
        kid = jac_ast.kid
        result = {'input': [], 'output': None}
        for i in kid:
            if (i.name == 'NAME'):
                if (i.token_text() not in obj.context.keys()):
                    self.rt_error(f"No context for preset param {i}", i)
                else:
                    prm = ctx_value(obj, i.token_text())
                    result['input'].append(prm)
        if (kid[-2].name == 'COLON_OUT'):
            result['input'].pop()
            result['output'] = ctx_value(obj, kid[-1].token_text())
        return result

    def run_dotted_name(self, jac_ast):
        """
        dotted_name: NAME (DOT NAME)*;
        """
        kid = jac_ast.kid
        ret = ''
        while True:
            ret += kid[0].token_text()
            kid = kid[1:]
            if(not len(kid) or kid[0].name != 'DOT'):
                break
            if(kid[0].name == 'DOT'):
                ret += '.'
                kid = kid[1:]
        return ret

    # Helper Functions ##################

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
        if(jac_ast):
            msg = f'{self.name} - line {jac_ast.line}, ' + \
                f'col {jac_ast.column} - rule {jac_ast.name} - {msg}'
        else:
            msg = f'{msg}'
        return msg

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
        if (not isinstance(obj, typ)):
            self.rt_error(f'Incompatible type {typ.__name__} for object ' +
                          f'{obj}', jac_ast)
            return False
        else:
            return True
