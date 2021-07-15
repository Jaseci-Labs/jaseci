"""
Node class for Jaseci

Each node has an id, name, timestamp and it's set of edges.
First node in list of 'member_node_ids' is designated root node
"""
from jaseci.element import element
from jaseci.utils.obj_mixins import anchored
from jaseci.graph.edge import edge
from jaseci.utils.id_list import id_list
from jaseci.utils.utils import logger

import uuid


class node(element, anchored):
    """Node class for Jaseci"""

    def __init__(self, dimension=0, *args, **kwargs):
        self.edge_ids = id_list(self)
        self.owner_node_ids = id_list(self)
        self.member_node_ids = id_list(self)
        self.dimension = dimension  # Nodes are always hdgd 0
        self.context = {}
        self.entry_action_ids = id_list(self)
        self.activity_action_ids = id_list(self)
        self.exit_action_ids = id_list(self)
        anchored.__init__(self)
        element.__init__(self, *args, **kwargs)

    def attach_outbound(self, node_obj, edge_set=None):
        """
        Creates edge to a node and returns the edge
        edge_set is the list of edges to be used to make connections
        new edge is created if edge_set is empty
        """
        if(edge_set is None):
            edge_set = [edge(h=self._h)]
        for e in edge_set:
            if(not e.set_from_node(self) or not e.set_to_node(node_obj)):
                return []
            e.set_bidirected(False)
            # add edge to nodes
            self.edge_ids.add_obj(e)
            if(self is not node_obj):
                node_obj.edge_ids.add_obj(e)
        # save and return
        self.save()
        node_obj.save()
        return edge_set

    def attach_inbound(self, node_obj, edge_set=None):
        """
        Creates edge from a node and returns the edge
        edge_set is the list of edges to be used to make connections
        new edge is created if edge_set is empty
        """
        if(edge_set is None):
            edge_set = [edge(h=self._h)]
        for e in edge_set:
            if(not e.set_from_node(node_obj) or not e.set_to_node(self)):
                return []
            e.set_bidirected(False)
            # add edge to nodes
            self.edge_ids.add_obj(e)
            if(self is not node_obj):
                node_obj.edge_ids.add_obj(e)
        # save and return
        self.save()
        node_obj.save()
        return edge_set

    def attach_bidirected(self, node_obj, edge_set=None):
        """
        Creates bidirected edge to node returns the edge
        edge_set is the list of edges to be used to make connections
        new edge is created if edge_set is empty
        """
        if(edge_set is None):
            edge_set = [edge(h=self._h)]
        for e in edge_set:
            if(not e.set_from_node(self) or not e.set_to_node(node_obj)):
                return []
            e.set_bidirected(True)
            # add edge to nodes
            self.edge_ids.add_obj(e)
            if(self is not node_obj):
                node_obj.edge_ids.add_obj(e)
        # save and return
        self.save()
        node_obj.save()
        return edge_set

    def detach_outbound(self, node_obj, edge_set=None):
        """
        Destroy edges to a node
        edge_set is the list of edges to be detached (and distroyed)
        all edges are deteached and destroyed if edge_set empty
        returns number of detachments
        """
        if(edge_set is None):
            edge_set = self.outbound_edges(node_obj)
        num_detached = 0
        for e in edge_set:
            # validate edge connection exists
            if(not e.connects(self, node_obj)):
                logger.error(
                    str(f"{e} does not connect {self} to {node_obj}")
                )
                continue
            # remove edge from nodes
            num_detached += 1
            self.edge_ids.remove_obj(e)
            if(self is not node_obj):
                node_obj.edge_ids.remove_obj(e)
            # destroy edge
            e.destroy()
        return num_detached

    def detach_inbound(self, node_obj, edge_set=None):
        """
        Destroy edges from a node
        edge_set is the list of edges to be detached (and distroyed)
        all edges are deteached and destroyed if edge_set empty
        returns number of detachments
        """
        if(edge_set is None):
            edge_set = self.inbound_edges(node_obj)
        num_detached = 0
        for e in edge_set:
            # validate edge connection exists
            if(not e.connects(node_obj, self)):
                logger.error(
                    str(f"{e} does not connect {node_obj} to {self}")
                )
                continue
            # remove edge from nodes
            num_detached += 1
            self.edge_ids.remove_obj(e)
            if(self is not node_obj):
                node_obj.edge_ids.remove_obj(e)
            # destroy edge
            e.destroy()
        return num_detached

    def detach_bidirected(self, node_obj, edge_set=None):
        """
        Destroy bidirected edges between nodes
        edge_set is the list of edges to be detached (and distroyed)
        all edges are deteached and destroyed if edge_set empty
        returns number of detachments
        """
        if(edge_set is None):
            edge_set = self.bidirected_edges(node_obj)
        num_detached = 0
        for e in edge_set:
            # validate edge connection exists
            if(not e.connects(self, node_obj) and e.is_bidirected()):
                logger.error(
                    str(f"{e} does not connect {self} and {node_obj}")
                )
                continue
            # remove edge from nodes
            num_detached += 1
            self.edge_ids.remove_obj(e)
            if(self is not node_obj):
                node_obj.edge_ids.remove_obj(e)
            # destroy edge
            e.destroy()
        return num_detached

    def destroy_outbound(self, node_obj, edge_set=None):
        """
        Destroys attached node and all relevant edges
        Node and all edges are destroyed if edge_set empty
        """
        if(edge_set is None):
            edge_set = self.outbound_edges(node_obj)
        if(self.detach_outbound(node_obj, edge_set)):
            node_obj.destroy()

    def destroy_inbound(self, node_obj, edge_set=None):
        """
        Destroys attached node and all relevant edges
        Node and all edges are destroyed if edge_set empty
        """
        if(edge_set is None):
            edge_set = self.inbound_edges(node_obj)
        if(self.detach_inbound(node_obj, edge_set)):
            node_obj.destroy()

    def destroy_bidirected(self, node_obj, edge_set=None):
        """
        Destroys attached node and all relevant edges
        Node and all edges are destroyed if edge_set empty
        """
        if(edge_set is None):
            edge_set = self.bidirected_edges(node_obj)
        if(self.detach_bidirected(node_obj, edge_set)):
            node_obj.destroy()

    def is_attached_out(self, node_obj, edge_set=None):
        """
        Tests whether edges attach to a node
        """
        out_set = self.outbound_edges(node_obj)
        if(edge_set is None):
            return len(out_set)
        else:
            for e in edge_set:
                if(e not in out_set):
                    return False
        return True

    def is_attached_in(self, node_obj, edge_set=None):
        """
        Tests whether edges attach from a node
        """
        in_set = self.inbound_edges(node_obj)
        if(edge_set is None):
            return len(in_set)
        else:
            for e in edge_set:
                if(e not in in_set):
                    return False
        return True

    def is_attached_bi(self, node_obj, edge_set=None):
        """
        Tests whether edges attach either to or from a node
        """
        bi_set = self.bidirected_edges(node_obj)
        if(edge_set is None):
            return len(bi_set)
        else:
            for e in edge_set:
                if(e not in bi_set):
                    return False
        return True

    def outbound_edges(self, node_obj=None):
        """Returns list of all edges out of node"""
        edge_set = []
        for e in self.edge_ids.obj_list():
            if(not e.is_bidirected() and e.connects(self, node_obj)):
                edge_set.append(e)
        return edge_set

    def inbound_edges(self, node_obj=None):
        """Returns list of all edges in to node"""
        edge_set = []
        for e in self.edge_ids.obj_list():
            if(not e.is_bidirected() and e.connects(node_obj, self)):
                edge_set.append(e)
        return edge_set

    def bidirected_edges(self, node_obj=None):
        """Returns list of all edges between nodes"""
        edge_set = []
        for e in self.edge_ids.obj_list():
            if(e.is_bidirected() and e.connects(node_obj)):
                edge_set.append(e)
        return edge_set

    def attached_edges(self, node_obj=None, silent=False):
        """
        Returns the edges connecting self to or from a node

        silent is used to indicate whther the edge is intened to be used.
        (effectively turns off error checking when false)
        """
        edge_set = self.outbound_edges(node_obj) + \
            self.inbound_edges(node_obj) + \
            self.bidirected_edges(node_obj)
        if(not silent and edge_set is None):
            logger.error(
                str(f"No edges found between {self} and {node_obj}")
            )
        return edge_set

    def outbound_nodes(self, edge_set=None):
        """Returns list of all nodes connected by edges out"""
        if(edge_set is None):
            edge_set = self.edge_ids.obj_list()
        ret_list = []
        for e in edge_set:
            if (not e.is_bidirected() and e.connects(source=self)):
                ret_list.append(e.to_node())
        return ret_list

    def inbound_nodes(self, edge_set=None):
        """Returns list of all nodes connected by edges in"""
        if(edge_set is None):
            edge_set = self.edge_ids.obj_list()
        ret_list = []
        for e in edge_set:
            if (not e.is_bidirected() and e.connects(target=self)):
                ret_list.append(e.from_node())
        return ret_list

    def bidirected_nodes(self, edge_set=None):
        """Returns list of all nodes connected by edges"""
        if(edge_set is None):
            edge_set = self.edge_ids.obj_list()
        ret_list = []
        for e in edge_set:
            if (e.is_bidirected()):
                ret_list.append(e.opposing_node(self))
        return ret_list

    def attached_nodes(self):
        """Returns list of all nodes connected"""
        edge_set = self.edge_ids.obj_list()
        ret_list = []
        for e in edge_set:
            ret_list.append(e.opposing_node(self))
        return ret_list

    def dimension_matches(self, node_obj, silent=True):
        """Test if dimension matches another node"""
        matches = self.dimension == node_obj.dimension
        if(not matches and not silent):
            logger.error(
                str("'{}' cant connect to '{}' - dim mismatch {}->{}".
                    format(self, node_obj, self.dimension,
                           node_obj.dimension))
            )
        return matches

    def make_member_of(self, node_obj):
        """
        Adds node to higher dimension node and does relevant checks
        """
        # check if valid inclusion
        if(node_obj.dimension != self.dimension+1):
            logger.error(
                str("'{}' cant be member to '{}' - dimension mismatch {}->{}".
                    format(self, node_obj, self.dimension, node_obj.dimension))
            )
        # adds self to hdgd and hdgd to list of owners
        else:
            node_obj.member_node_ids.add_obj(self)
            self.owner_node_ids.add_obj(node_obj)

    def make_owner_of(self, node_obj):
        """
        Adds node to lower dimension node and does relevant checks
        """
        node_obj.make_member_of(self)

    def leave_memebership_of(self, node_obj):
        """Remove node from higher dimension node"""
        node_obj.member_node_ids.remove_obj(self)
        self.owner_node_ids.remove_obj(node_obj)

    def disown(self, node_obj):
        """Remove node from higher dimension node"""
        node_obj.leave_membership_of(self)

    def set_context(self, ctx, arch=None):
        """Assign values to context fields of node, arch is node architype"""
        if(arch is None):
            arch = self
        for i in ctx.keys():
            if (i not in arch.context.keys()):
                logger.warning(str(f"{i} not a context member of {self}"))
                continue
            else:
                self.context[i] = ctx[i]
        self.save()

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        des = self.activity_action_ids.obj_list() + \
            self.edge_ids.obj_list() + self.entry_action_ids.obj_list() + \
            self.exit_action_ids.obj_list()
        for i in des:
            i.destroy()
        super().destroy()

    def dot_str(self):
        """
        DOT representation
        """
        # _n_name is a reserved key for node name. Note that this is
        # different than the name you could set in context
        dstr = uuid.UUID(self.jid).hex+' '

        node_dict = self.context
        if (self.kind != 'generic'):
            node_dict['_kind_'] = self.kind
        if (self.name != 'basic'):
            node_dict['_name_'] = self.name

        if (node_dict):
            dstr += '['
            num_items = 0
            for k, v in node_dict.items():
                if(v is None or v == ""):
                    num_items += 1
                    continue
                if (num_items != 0):
                    dstr += ' '
                dstr += f'{k}={v}'

                num_items += 1
                if (num_items < len(node_dict)):
                    dstr += ','
            dstr += ']'

        return dstr+'\n'
