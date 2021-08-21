from jaseci.utils.id_list import id_list
from jaseci.attr.action import action
from jaseci.actions.utils.find_action import find_action
from jaseci.actions.utils.find_action import get_action_set

action_list = []
action_list += get_action_set('std')
action_list += get_action_set('net')
action_list += get_action_set('rand')
action_list += get_action_set('vector')


def get_global_actions(parent_obj):
    """Registers and loads all global action hooks for use by Jac programs"""

    global_action_ids = id_list(parent_obj)
    for i in action_list:
        global_action_ids.add_obj(
            action(
                m_id=parent_obj._m_id,
                h=parent_obj._h,
                mode='public',
                name=i,
                value=find_action(i),
                persist=False
            )
        )
    return global_action_ids
