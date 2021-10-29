from jaseci.utils.id_list import id_list
from jaseci.attr.action import action
from jaseci.actions.utils.find_action import find_action
from jaseci.actions.utils.find_action import get_action_set

action_list = []
action_list += get_action_set('std')
action_list += get_action_set('net')
action_list += get_action_set('rand')
action_list += get_action_set('vector')

registered_globals = {}


def get_global_actions(parent_obj):
    """Registers and loads all global action hooks for use by Jac programs"""

    # NOTE: Regenerating global_actions based on hooks changing
    if(parent_obj._m_id not in registered_globals.keys() or
       registered_globals[parent_obj._m_id][-1] != parent_obj._h):
        registered_globals[parent_obj._m_id] = [
            [], parent_obj._h]
        for i in action_list:
            registered_globals[parent_obj._m_id][0].append(
                action(
                    m_id=parent_obj._m_id,
                    h=parent_obj._h,
                    mode='public',
                    name=i,
                    value=find_action(i),
                    persist=False
                )
            )
    global_action_ids = id_list(parent_obj)
    for i in registered_globals[parent_obj._m_id][0]:
        global_action_ids.add_obj(i)
    return global_action_ids
