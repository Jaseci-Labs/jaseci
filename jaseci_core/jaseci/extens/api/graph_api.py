"""
Graph api functions as a mixin
"""
from jaseci.extens.api.interface import Interface
from jaseci.utils.id_list import IdList
from jaseci.prim.graph import Graph
from jaseci.prim.node import Node
import uuid


class GraphApi:
    """
    Graph APIs
    """

    def __init__(self):
        self.active_gph_id = None
        self.graph_ids = IdList(self)

    @Interface.private_api()
    def graph_create(self, set_active: bool = True):
        """
        Create a graph instance and return root node graph object
        """
        gph = Graph(m_id=self._m_id, h=self._h)
        self.graph_ids.add_obj(gph)
        if set_active:
            self.graph_active_set(gph)
        return gph.serialize()

    @Interface.private_api()
    def graph_get(
        self,
        nd: Node = None,
        mode: str = "default",
        detailed: bool = False,
        depth: int = 0,
    ):
        """
        Return the content of the graph with mode
        Valid modes: {default, dot, }
        """
        if mode == "dot":
            return nd.traversing_dot_str(detailed, depth)

        nodes, edges = nd.get_all_architypes(depth)
        items = []
        for i in nodes.values():
            items.append(i.serialize(detailed=detailed))
        for i in edges.values():
            items.append(i.serialize(detailed=detailed))
        return items

    @Interface.private_api()
    def graph_list(self, detailed: bool = False):
        """
        Provide complete list of all graph objects (list of root node objects)
        """
        gphs = []
        for i in self.graph_ids.obj_list():
            gphs.append(i.serialize(detailed=detailed))
        return gphs

    @Interface.private_api(cli_args=["gph"])
    def graph_active_set(self, gph: Graph):
        """
        Sets the default graph master should use
        """
        self.active_gph_id = gph.jid
        self.alias_register("active:graph", gph.jid)
        return [f"Graph {gph.id} set as default"]

    @Interface.private_api()
    def graph_active_unset(self):
        """
        Unsets the default sentinel master should use
        """
        self.active_gph_id = None
        self.alias_delete("active:graph")
        return ["Default graph unset"]

    @Interface.private_api()
    def graph_active_get(self, detailed: bool = False):
        """
        Returns the default graph master is using
        """
        if self.active_gph_id:
            default = self._h.get_obj(self._m_id, self.active_gph_id)
            return default.serialize(detailed=detailed)
        else:
            return {"success": False, "response": "No default graph is selected!"}

    @Interface.private_api(cli_args=["gph"])
    def graph_delete(self, gph: Graph):
        """
        Permanently delete graph with given id
        """
        if self.active_gph_id == gph.jid:
            self.graph_active_unset()
        self.graph_ids.destroy_obj(gph)
        return [f"Graph {gph.id} successfully deleted"]

    @Interface.private_api(cli_args=["nd"])
    def graph_node_get(self, nd: Node, keys: list = []):
        """
        Returns value a given node
        """
        ret = {}
        nd_ctx = nd.serialize(detailed=True)["context"]
        for i in nd_ctx.keys():
            if not len(keys) or i in keys:
                ret[i] = nd_ctx[i]
        return ret

    @Interface.private_api(cli_args=["nd"])
    def graph_node_view(
        self,
        nd: Node = None,
        detailed: bool = False,
        show_edges: bool = False,
        node_type: str = "",
        edge_type: str = "",
    ):
        """
        Returns value a given node
        """
        ret = [nd.serialize(detailed=detailed)]
        for i in nd.attached_nodes():
            if not len(node_type) or i.name == node_type:
                edges = [
                    en
                    for en in nd.attached_edges(i)
                    if not len(edge_type) or en.name == edge_type
                ]
                if len(edges):
                    ret.append(i.serialize(detailed=detailed))
                    if show_edges:
                        for j in edges:
                            ret.append(j.serialize(detailed=detailed))
        return ret

    @Interface.private_api(cli_args=["nd"])
    def graph_node_set(self, nd: Node, ctx: dict):
        """
        Assigns values to member variables of a given node using ctx object
        """
        nd.set_context(ctx=ctx)
        return nd.serialize()

    @Interface.cli_api(cli_args=["file"])
    def graph_walk(self, nd: Node = None):
        cmd = ""
        while cmd not in ["quit", "q", "exit"]:
            print(
                "location - " + ":".join([nd.kind, nd.name, nd.jid.strip("urn:uuid:")])
            )
            cmd = input("graph_walk_mode > ")

    def active_gph(self):
        return self._h.get_obj(self._m_id, self.active_gph_id)

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        for i in self.graph_ids.obj_list():
            i.destroy()
