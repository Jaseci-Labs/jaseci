"""
Graph api functions as a mixin
"""
from jaseci.utils.id_list import id_list
from jaseci.graph.graph import graph
from jaseci.graph.node import node
from jaseci.actor.sentinel import sentinel


class graph_api():
    """
    Graph APIs
    """

    def __init__(self):
        self.graph_ids = id_list(self)

    def api_graph_create(self, name: str):
        """
        Create a graph instance and return root node graph object
        """
        gph = graph(h=self._h, name=name)
        self.graph_ids.add_obj(gph)
        return gph.serialize()

    def api_graph_list(self, detailed: bool = False):
        """
        Provide complete list of all graph objects (list of root node objects)
        """
        gphs = []
        for i in self.graph_ids.obj_list():
            gphs.append(i.serialize(detailed=detailed))
        return gphs

    def api_graph_delete(self, gph: graph):
        """
        Permanently delete graph with given id
        """
        self.graph_ids.destroy_obj(gph)
        return [f'Graph {gph.id} successfully deleted']

    def api_graph_get(self, gph: graph, detailed: bool = False,
                      dot: bool = False):
        """
        Return the content of the graph
        """
        if(dot):
            return gph.graph_dot_str()
        else:
            nds = []
            for i in gph.get_network_nodes():
                nds.append(i.serialize(detailed=detailed))
            return nds

    def api_graph_node_get(self, nd: node, ctx: list = None):
        """
        Returns value a given node
        """
        ret = {}
        nd_ctx = nd.serialize(detailed=True)['context']
        if(ctx):
            for i in nd_ctx.keys():
                if i in ctx:
                    ret[i] = nd_ctx[i]
        return ret

    def api_graph_node_set(self, snt: sentinel, nd: node, ctx: dict):
        """
        Assigns values to member variables of a given node using ctx object
        """
        nd.set_context(
            ctx=ctx, arch=snt.arch_ids.get_obj_by_name('node.'+nd.kind).run())
        return nd.serialize()

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        for i in self.graph_ids.obj_list():
            i.destroy()
        super().destroy()
