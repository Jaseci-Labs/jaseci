from jaseci.attr.action import action
from jaseci.actions.find_action import find_action
from jaseci.actions.find_action import get_action_set
import uuid

action_list = get_action_set('std') + get_action_set('net') + \
    get_action_set('rand') + get_action_set('vector') + \
    get_action_set('request')


def get_global_actions(hook):
    """
    Loads all global action hooks for use by Jac programs
    Attaches globals to mem_hook
    """
    global_action_list = []
    for i in action_list:
        global_action_list.append(
            action(
                m_id=uuid.UUID(int=0).urn,
                h=hook,
                mode='public',
                name=i,
                value=find_action(i),
                persist=False
            ).jid
        )
    return global_action_list
