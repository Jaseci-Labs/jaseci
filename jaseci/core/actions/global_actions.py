from core.utils.id_list import id_list
from core.attr.action import action
from core.actions.find_action import find_action
from core.actions.find_action import get_action_set
from core.utils.mem_hook import mem_hook
from core.element import element

global_scope = element(mem_hook())
global_action_ids = id_list(global_scope)


def setup_global_actions():
    """Registers and loads all global action hooks for use by Jac programs"""
    action_list = []
    action_list += get_action_set('std')
    action_list += get_action_set('net')
    action_list += get_action_set('rand')
    action_list += get_action_set('vector')

    for i in action_list:
        global_action_ids.add_obj(
            action(
                h=global_scope._h,
                name=i,
                value=find_action(i)
            )
        )


setup_global_actions()
