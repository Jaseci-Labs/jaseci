from jaseci.utils.id_list import id_list
from jaseci.attr.action import action
from jaseci.actions.utils.find_action import find_action
from jaseci.actions.utils.find_action import get_action_set
from jaseci.utils.mem_hook import mem_hook
from jaseci.element import element

global_scope = element(m_id='anon', h=mem_hook())
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
                m_id='anon',
                h=global_scope._h,
                name=i,
                value=find_action(i)
            )
        )


setup_global_actions()
