"""
Action library for graph network operations

This library of actions cover the standard operations that can be
run on graph elements (nodes and edges). A number of these actions
accept lists that are exclusively composed of instances of defined
architype node and/or edges. Keep in mind that a \\lstinline{jac_set}
is simply a list that only contains such elements.
"""
from jaseci.actions.live_actions import jaseci_action
from jaseci.utils.utils import master_from_meta
from jaseci.jac.jac_set import jac_set
from jaseci.graph.node import node
from jaseci.graph.edge import edge
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
    graph_dict = {"nodes": [], "edges": []}
    idx_map = {}
    edge_set = jac_set()
    for i in item_set.obj_list():
        if isinstance(i, node):
            node_pack = {"name": i.name, "ctx": i.context}
            idx_map[i.jid] = len(graph_dict["nodes"])
            graph_dict["nodes"].append(node_pack)
            for j in i.attached_edges():
                edge_set.add_obj(j)
    for i in edge_set:
        fnd = i.from_node()
        tnd = i.to_node()
        if fnd.jid in idx_map.keys() and tnd.jid in idx_map.keys():
            edge_pack = {
                "name": i.name,
                "ctx": i.context,
                "connect": [idx_map[fnd.jid], idx_map[tnd.jid]],
                "bi_dir": i.is_bidirected(),
            }
            graph_dict["edges"].append(edge_pack)
    return graph_dict


@jaseci_action()
def unpack(graph_dict: dict, meta):
    """Built in actions for Jaseci"""
    mast = master_from_meta(meta)
    item_set = jac_set()
    node_list = []
    for i in graph_dict["nodes"]:
        node_list.append(
            node(
                m_id=mast._m_id,
                h=mast._h,
                kind="node",
                name=i["name"],
            )
        )
        node_list[-1].context = i["ctx"]
        item_set.add_obj(node_list[-1])
        node_list[-1].save()
    for i in graph_dict["edges"]:
        this_edge = edge(
            m_id=mast._m_id,
            h=mast._h,
            kind="edge",
            name=i["name"],
        )
        this_edge.connect(
            node_list[i["connect"][0]], node_list[i["connect"][1]], i["bi_dir"]
        )
        item_set.add_obj(this_edge)
        this_edge.save()
    return item_set


@jaseci_action()
def root(meta):
    """
    Returns a user's root node

    This action returns the root node for the graph of a given user (master). A call
    to this action is only valid if the user has an active graph set, otherwise it
    return null. This is a handy way for any walker to get to the root node of a
    graph from anywhere.

    :returns: The root node of the active graph for a user. If none set, returns null.
    """
    mast = master_from_meta(meta)
    if mast.active_gph_id:
        return mast._h.get_obj(mast._m_id, uuid.UUID(mast.active_gph_id))
    return None
