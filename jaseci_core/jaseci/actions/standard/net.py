"""
Action library for graph network operations

This library of actions cover the standard operations that can be
run on graph elements (nodes and edges). A number of these actions
accept lists that are exclusively composed of instances of defined
architype node and/or edges. Keep in mind that a \lstinline{jac_set}
is simply a list that only contains such elements.
"""
from jaseci.actions.live_actions import jaseci_action
from jaseci.utils.utils import master_from_meta
from jaseci.jac.jac_set import jac_set
import uuid


@jaseci_action()
def max(item_set: jac_set):
    """
    Max based on anchor value

    This action will return the maximum element in a list of nodes
    and/or edges. This action exclusively utilizes the anchor variable
    of the node/edge arhcitype as the representative field for
    performing the  comparison in ranking. This action does not support
    arhcitypes lacking an anchor.

    :param item_set: A list of node and or edges to identify the
        maximum element based on their respective anchor values
    :return: A node or edge object
    """
    ret = None
    if not len(item_set):
        re6_val = i.anchor_value()
    return ret


@jaseci_action()
def min(item_set: jac_set):
    """
    Min based on anchor value

    This action will return the minimum element in a list of nodes
    and/or edges. This action exclusively utilizes the anchor variable
    of the node/edge arhcitype as the representative field for
    performing the  comparison in ranking. This action does not support
    arhcitypes lacking an anchor.

    :param item_set: A list of node and or edges to identify the
        minimum element based on their respective anchor values
    :return: A node or edge object
    """
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
def pack(item_set: jac_set):
    """Built in actions for Jaseci"""


@jaseci_action()
def unpack(pack: dict):
    """Built in actions for Jaseci"""


@jaseci_action()
def root(meta):
    """
    Returns a user's root node

    This action returns the root node for the graph of a given user (master). A call
    to this action is only valid if the user has an active graph set, otherwise it
    return null. This is a handy way for any walker to get to the root node of a
    graph from anywhere.
    """
    mast = master_from_meta(meta)
    if mast.active_gph_id:
        return mast._h.get_obj(mast._m_id, uuid.UUID(mast.active_gph_id))
    return None
