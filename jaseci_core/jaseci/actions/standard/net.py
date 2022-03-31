"""Built in actions for Jaseci"""
from jaseci.actions.live_actions import jaseci_action
from jaseci.jac.jac_set import jac_set


@jaseci_action()
def max(item_set: jac_set):
    ret = None
    if (not len(item_set)):
        return None
    items = item_set.obj_list()
    max_val = items[0].anchor_value()
    ret = items[0]
    for i in items:
        if(i.anchor_value() > max_val):
            ret = i
            max_val = i.anchor_value()
    return ret
