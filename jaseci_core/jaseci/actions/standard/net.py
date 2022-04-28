"""Built in actions for Jaseci"""
from jaseci.actions.live_actions import jaseci_action
from jaseci.utils.utils import master_from_meta
from jaseci.jac.jac_set import jac_set
import uuid


@jaseci_action()
def max(item_set: jac_set):
    ret = None
    if not len(item_set):
        return None
    items = item_set.obj_list()
    max_val = items[0].anchor_value()
    ret = items[0]
    for i in items:
        if i.anchor_value() > max_val:
            ret = i
            max_val = i.anchor_value()
    return ret


@jaseci_action()
def min(item_set: jac_set):
    ret = None
    if not len(item_set):
        return None
    items = item_set.obj_list()
    min_val = items[0].anchor_value()
    ret = items[0]
    for i in items:
        if i.anchor_value() < min_val:
            ret = i
            min_val = i.anchor_value()
    return ret


@jaseci_action()
def root(meta):
    mast = master_from_meta(meta)
    if mast.active_gph_id:
        return mast._h.get_obj(mast._m_id, uuid.UUID(mast.active_gph_id))
    return None
