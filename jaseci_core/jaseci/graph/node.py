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

import copy
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

    def attach_outbound(self, node_obj, use_edge=None):
        """
        Creates edge to a node and returns the edge

        If edge already exists, this function logs a warning and returns the
        edge anyway.
        """
        # check if connection already exists
        if(self.is_attached_out(node_obj)):
            logger.warning(
                str("{} node already is connected to {} node".
                    format(self, node_obj))
            )
            return self.outbound_edge(node_obj)
        # create edge
        if(not use_edge):
            use_edge = edge(h=self._h)
        use_edge.set_from_node(self)
        use_edge.set_to_node(node_obj)
        # add edge to nodes
        self.edge_ids.add_obj(use_edge)
        if(self is not node_obj):
            node_obj.edge_ids.add_obj(use_edge)
        # save and return
        self.save()
        node_obj.save()
        return use_edge

    def attach_inbound(self, node_obj, use_edge=None):
        """
        Creates edge from a node and returns the edge

        If edge already exists, this function logs a warning and returns the
        edge anyway.
        """
        # check if connection already exists
        if(self.is_attached_in(node_obj)):
            logger.warning(
                str("{} already has connection from {}".
                    format(self, node_obj))
            )
            return self.inbound_edge(node_obj)
        # create edge (check for matching dims at edge class)
        if(not use_edge):
            use_edge = edge(h=self._h)
        use_edge.set_from_node(node_obj)
        use_edge.set_to_node(self)
        # add edge to nodes
        self.edge_ids.add_obj(use_edge)
        if(self is not node_obj):
            node_obj.edge_ids.add_obj(use_edge)
        # save and return
        self.save()
        node_obj.save()
        return use_edge

    def detach_outbound(self, node_obj):
        """
        Destroy edge to a node

        If edge already exists, this function logs an error.
        """
        # validate connection already exists
        if(not self.is_attached_out(node_obj)):
            logger.error(
                str("{} already is not connected to {}".
                    format(self, node_obj))
            )
            return
        target = self.outbound_edge(node_obj)
        # remove edge from nodes
        self.edge_ids.remove_obj(target)
        if(self is not node_obj):
            node_obj.edge_ids.remove_obj(target)
        # destroy edge
        target.destroy()

    def detach_inbound(self, node_obj):
        """
        Destroy edge from a node

        If edge already exists, this function logs an error.
        """
        # validate connection already exists
        if(not self.is_attached_in(node_obj)):
            logger.warning(
                str("{} already is not connected from {}".
                    format(self, node_obj))
            )
            return
        target = self.inbound_edge(node_obj)
        # remove edge from nodes
        self.edge_ids.remove_obj(target)
        if(self is not node_obj):
            node_obj.edge_ids.remove_obj(target)
        # destroy edge
        target.destroy()

    def destroy_outbound(self, node_obj):
        """
        Destroy edge and node

        If edge already exists, this function logs an error.
        """
        self.detach_outbound(node_obj)
        node_obj.destroy()

    def destroy_inbound(self, node_obj):
        """
        Destroy edge and node

        If edge already exists, this function logs an error.
        """
        self.detach_inbound(node_obj)
        node_obj.destroy()

    def is_attached_out(self, node_obj):
        """Tests whether edge exists to a node"""
        return self.outbound_edge(node_obj, silent=True) is not None

    def is_attached_in(self, node_obj):
        """Tests whether edge exists from a node"""
        return self.inbound_edge(node_obj, silent=True) is not None

    def is_attached(self, node_obj):
        """Tests whether edge exists either to or from a node"""
        return self.is_attached_out(node_obj) or \
            self.is_attached_in(node_obj)

    def get_edge(self, node_obj, silent=False):
        """
        Returns the edge connecting self to or from a node

        silent is used to indicate whther the edge is intened to be used.
        (effectively turns off error checking when false)
        """
        use_edge = self.outbound_edge(node_obj, silent=True)
        if(not use_edge):
            use_edge = self.inbound_edge(node_obj, silent)
        return use_edge

    def outbound_edge(self, node_obj, silent=False):
        """
        Returns the edge connecting self to a node

        silent is used to indicate whther the edge is intened to be used.
        (effectively turns off error checking when false)
        """
        for cur_edge in self.edge_ids.obj_list():
            if(cur_edge.from_node() == self and
               cur_edge.to_node() == node_obj):
                return cur_edge
        if(not silent):
            logger.error(
                str("Edge does not exists from {} to {}!".
                    format(self, node_obj))
            )
        return None

    def inbound_edge(self, node_obj, silent=False):
        """
        Returns the edge connecting self from a node

        silent is used to indicate whther the edge is intened to be used.
        (effectively turns off error checking when false)
        """
        for cur_edge in self.edge_ids.obj_list():
            if(cur_edge.from_node() == node_obj and
               cur_edge.to_node() == self):
                return cur_edge
        if(not silent):
            logger.error(
                str("Edge does not exists from {} to {}!".
                    format(node_obj, self))
            )
        return None

    def outbound_edges(self):
        """Returns list of all edges out of node"""
        ret_list = []
        for cur_edge in self.edge_ids.obj_list():
            if(cur_edge.from_node() == self):
                ret_list.append(cur_edge)
        return ret_list

    def inbound_edges(self):
        """Returns list of all edges in to node"""
        ret_list = []
        for cur_edge in self.edge_ids.obj_list():
            if(cur_edge.to_node() == self):
                ret_list.append(cur_edge)
        return ret_list

    def attached_edges(self):
        """Returns list of all edges connected"""
        return self.outbound_edges() + \
            self.inbound_edges()

    def outbound_nodes(self):
        """Returns list of all nodes connected by edges out"""
        ret_list = []
        for cur_edge in self.edge_ids.obj_list():
            if (cur_edge.from_node() == self):
                # TODO: HACK FOR BUG IN JAC's EDGE DISCONNECT
                if (cur_edge not in cur_edge.to_node().edge_ids.obj_list()):
                    continue
                ret_list.append(cur_edge.to_node())
        return ret_list

    def inbound_nodes(self):
        """Returns list of all nodes connected by edges in"""
        ret_list = []
        for cur_edge in self.edge_ids.obj_list():
            if (cur_edge.to_node() == self):
                # TODO: HACK FOR BUG IN JAC's EDGE DISCONNECT
                if (cur_edge not in cur_edge.from_node().edge_ids.obj_list()):
                    continue
                ret_list.append(cur_edge.from_node())
        return ret_list

    def attached_nodes(self):
        """Returns list of all nodes connected"""
        return self.outbound_nodes() + \
            self.inbound_nodes()

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
        if(not arch):
            arch = self
        for i in ctx.keys():
            if (i not in arch.context.keys()):
                logger.warning(str(f"{i} not a context member of {self}"))
                continue
            else:
                self.context[i] = ctx[i]
        self.save()

    def get_network(self, inward=False, g_list=None):
        """
        Walk network of node and return all reachable nodes

        inward is a flag for whether to return paths pointing into node
        path_list and touched are used internally for recursion
        TODO: Not fully tested, also redundant with get_network_nodes
        """
        if(not isinstance(g_list, list)):
            g_list = []

        # if cycle detected in path
        if(self in g_list):
            return g_list

        g_list.append(self)

        get_edges_func = self.outbound_edges
        if(inward):
            get_edges_func = self.inbound_edges
        child_list = get_edges_func()
        for i in child_list:
            g_list.append(i)

        for i in child_list:
            next_node = i.to_node()
            if(next_node == self):
                next_node = i.from_node()
            next_node.get_network(inward, g_list)

        return g_list

    def get_network_nodes(self, inward=False, node_list=None):
        """
        Walk network of node and return all reachable nodes

        inward is a flag for whether to return paths pointing into node
        path_list and touched are used internally for recursion
        TODO: Not fully tested
        """
        if(not isinstance(node_list, list)):
            node_list = []

        # if cycle detected in path
        if(self in node_list):
            return node_list

        node_list.append(self)

        get_nodes_func = self.outbound_nodes
        if(inward):
            get_nodes_func = self.inbound_nodes
        child_list = get_nodes_func()

        for i in child_list:
            i.get_network_nodes(inward, node_list)

        return node_list

    def get_network_paths(self, inward=False, nodes_only=False, path_list=None,
                          touched=None):
        """
        Detect all paths directed out and pretty print to string

        inward is a flag for whether to return paths pointing into node
        path_list and touched are used internally for recursion
        TODO: Not fully tested
        """
        if(not isinstance(touched, list)):
            touched = []
        if(not isinstance(path_list, list)):
            path_list = []

        # if cycle detected in path
        if(self in touched):
            touched.append(self)
            path_list.append(copy.copy(touched))
            touched.pop()
            if(not nodes_only and len(touched)):
                touched.pop()
            return path_list

        touched.append(self)

        get_nodes_func = self.outbound_nodes
        if(inward):
            get_nodes_func = self.inbound_nodes
        child_list = get_nodes_func()

        for i in child_list:
            if(not nodes_only):
                touched.append(self.get_edge(i))
            i.get_network_paths(inward, nodes_only, path_list, touched)

        if(not len(child_list)):
            path_list.append(copy.copy(touched))

        touched.pop()
        if(not nodes_only and len(touched)):
            touched.pop()

        return path_list

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
