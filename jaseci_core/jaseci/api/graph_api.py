"""
Graph api functions as a mixin
"""
from jaseci.api.interface import interface
from jaseci.utils.id_list import id_list
from jaseci.graph.graph import graph
from jaseci.graph.node import node
from jaseci.actor.sentinel import sentinel
import uuid


class graph_api():
    """
    Graph APIs
    """

    def __init__(self):
        self.active_gph_id = None
        self.graph_ids = id_list(self)

    @interface.private_api()
    def graph_create(self, set_active: bool = True):
        """
        Create a graph instance and return root node graph object
        """
        gph = graph(m_id=self._m_id, h=self._h)
        self.graph_ids.add_obj(gph)
        if(set_active):
            self.graph_active_set(gph)
        return gph.serialize()

    @interface.private_api()
    def graph_get(self, gph: graph = None,
                  mode: str = 'default', detailed: bool = False):
        """
        Return the content of the graph with mode
        Valid modes: {default, dot, }
        """
        if(mode == 'dot'):
            return gph.graph_dot_str()
        else:
            items = []
            for i in gph.get_all_nodes():
                items.append(i.serialize(detailed=detailed))
            for i in gph.get_all_edges():
                items.append(i.serialize(detailed=detailed))
            return items

    @interface.private_api()
    def graph_list(self, detailed: bool = False):
        """
        Provide complete list of all graph objects (list of root node objects)
        """
        gphs = []
        for i in self.graph_ids.obj_list():
            gphs.append(i.serialize(detailed=detailed))
        return gphs

    @interface.private_api(cli_args=['gph'])
    def graph_active_set(self, gph: graph):
        """
        Sets the default graph master should use
        """
        self.active_gph_id = gph.jid
        self.alias_register('active:graph', gph.jid)
        return [f'Graph {gph.id} set as default']

    @interface.private_api()
    def graph_active_unset(self):
        """
        Unsets the default sentinel master should use
        """
        self.active_gph_id = None
        self.alias_delete('active:graph')
        return ['Default graph unset']

    @interface.private_api()
    def graph_active_get(self, detailed: bool = False):
        """
        Returns the default graph master is using
        """
        if(self.active_gph_id):
            default = self._h.get_obj(
                self._m_id, uuid.UUID(self.active_gph_id))
            return default.serialize(detailed=detailed)
        else:
            return ['No default graph is selected!']

    @interface.private_api(cli_args=['gph'])
    def graph_delete(self, gph: graph):
        """
        Permanently delete graph with given id
        """
        if(self.active_gph_id == gph.jid):
            self.graph_active_unset()
        self.graph_ids.destroy_obj(gph)
        return [f'Graph {gph.id} successfully deleted']

    @interface.private_api(cli_args=['nd'])
    def graph_node_get(self, nd: node, ctx: list = None):
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

    @interface.private_api(cli_args=['nd'])
    def graph_node_set(self, nd: node, ctx: dict, snt: sentinel = None):
        """
        Assigns values to member variables of a given node using ctx object
        """
        nd.set_context(
            ctx=ctx, arch=snt.run_architype(
                nd.name, kind='node', caller=self))
        return nd.serialize()

    def active_gph(self):
        return self._h.get_obj(
            self._m_id, uuid.UUID(self.active_gph_id))

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        for i in self.graph_ids.obj_list():
            i.destroy()
