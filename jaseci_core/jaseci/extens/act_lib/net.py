"""
Action library for graph network operations

This library of actions cover the standard operations that can be
run on graph elements (nodes and edges). A number of these actions
accept lists that are exclusively composed of instances of defined
architype node and/or edges. Keep in mind that a \\lstinline{jac_set}
is simply a list that only contains such elements.
"""
from jaseci.jsorc.live_actions import jaseci_action
from jaseci.utils.utils import master_from_meta
from jaseci.jac.jac_set import JacSet
from jaseci.prim.node import Node
from jaseci.prim.edge import Edge
import uuid


@jaseci_action()
def max(item_set: JacSet):
    """
    Max based on anchor value

    This action will return the maximum element in a list of nodes
    and/or edges based on an anchor has variable. Since each node or edge can only
    specify a single anchor this action enables a handy short hand for utilizing the
    anchor variable as the representative field for performing the  comparison in
    ranking. This action does not support arhcitypes lacking an anchor.
    \\par
    For example, if you have a node called \\lstinline{movie_review} with a
    field \\lstinline{has anchor score = .5;} that changes based on sentiment
    analysis, using this action will return the node with the highest score from the
    input list of nodes.

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
def min(item_set: JacSet):
    """
    Min based on anchor value

    This action will return the minimum element in a list of nodes
    and/or edges. This action exclusively utilizes the anchor variable
    of the node/edge arhcitype as the representative field for
    performing the comparison in ranking. This action does not support
    arhcitypes lacking an anchor. (see action max for an example)

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
def pack(item_set: JacSet, destroy: bool = False):
    """
    Convert a subgraph to a generalized dictionary format

    This action takes a subgraph as a collection of nodes in a list and
    creates a generic dictionary representation of the subgraph inclusive of
    all edges between nodes inside the collection. Note that any edges that are
    connecting nodes outside of the list of nodes are omitted from the packed
    subgraph representation. The complete context of all nodes and connecting edges
    are retained in the packed dictionary format. The unpack action can then be used
    to instantiate the identical subgraph back into a graph. Packed graphs are
    highly portable and can be used for many use cases such as exporting graphs and
    subgraphs to be imported using the unpack action.

    :param item_set: A list of nodes comprising the subgraph to be packed. Edges can be
    included in this list but is ultimately ignored. All edges from the actual nodes
    in the context of the source graph will be automatically included in the packed
    dictionary if it contects two nodes within this input list.
    :param destroy: A flag indicating whether the original graph nodes covered by pack
    operation should be destroyed.
    :returns: A generic and portable dictionary representation of the subgraph
    """
    graph_dict = {"nodes": [], "edges": []}
    idx_map = {}
    edge_set = JacSet()
    for i in item_set.obj_list():
        if isinstance(i, Node):
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
    if destroy:
        for i in item_set.obj_list():
            if isinstance(i, Node) and i.name != "root":
                i.destroy()
    return graph_dict


@jaseci_action()
def unpack(graph_dict: dict, meta):
    """
    Convert a packed dictionary to Jac graph elements

    This action takes a dictionary in the format produced by the packed action
    to instantiate a set of nodes and edges corresponding to the subgraph represented
    by the pack action. The original contexts that were pack will also be created.
    Important Note: When using this unpack action, the unpacked collections of elements
    returned must be connected to a source graph to avoid memory leaks.

    :param graph_dict: A dictionary in the format produced by the pack action.
    :returns: A list of the nodes and edges that were created corresponding to the
    input packed format. Note: Must be then connected to a source graph to avoid memory
    leak.
    """
    mast = master_from_meta(meta)
    item_set = JacSet()
    node_list = []
    for i in graph_dict["nodes"]:
        node_list.append(
            Node(
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
        this_edge = Edge(
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
        return mast._h.get_obj(mast._m_id, mast.active_gph_id)
    return None
