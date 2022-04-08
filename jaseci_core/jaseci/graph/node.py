"""
Node class for Jaseci

Each node has an id, name, timestamp and it's set of edges.
First node in list of 'member_node_ids' is designated root node
"""
from jaseci.element.element import element
from jaseci.element.obj_mixins import anchored
from jaseci.graph.edge import edge
from jaseci.utils.id_list import id_list
from jaseci.utils.utils import logger

import uuid


class node(element, anchored):
    """Node class for Jaseci"""

    def __init__(self, dimension=0, *args, **kwargs):
        self.edge_ids = id_list(self)
        self.parent_node_ids = id_list(self)
        self.member_node_ids = id_list(self)
        self.dimension = dimension  # Nodes are always hdgd 0
        self.context = {}

        anchored.__init__(self)
        element.__init__(self, *args, **kwargs)

    def attach(self, node_obj, edge_set=None, as_outbound=True,
               as_bidirected=False):
        """
        Generalized attach function for attaching nodes with edges
        """
        if(edge_set is None):
            edge_set = [edge(m_id=self._m_id, h=self._h,
                             kind='edge', name='generic')]
        link_order = [self, node_obj] if as_outbound else [node_obj, self]
        for e in edge_set:
            if(not e.set_from_node(link_order[0]) or
               not e.set_to_node(link_order[1])):
                # Node not found error logged in set node function
                return []
            e.set_bidirected(as_bidirected)
        # save and return
        self.save()
        node_obj.save()
        return edge_set

    def attach_outbound(self, node_obj, edge_set=None):
        """
        Creates edge to a node and returns the edge
        edge_set is the list of edges to be used to make connections
        new edge is created if edge_set is empty
        """
        return self.attach(node_obj, edge_set, as_outbound=True)

    def attach_inbound(self, node_obj, edge_set=None):
        """
        Creates edge from a node and returns the edge
        edge_set is the list of edges to be used to make connections
        new edge is created if edge_set is empty
        """
        return self.attach(node_obj, edge_set, as_outbound=False)

    def attach_bidirected(self, node_obj, edge_set=None):
        """
        Creates bidirected edge to node returns the edge
        edge_set is the list of edges to be used to make connections
        new edge is created if edge_set is empty
        """
        return self.attach(node_obj, edge_set, as_bidirected=True)

    def detach(self, node_obj, edge_set=None, as_outbound=True,
               as_bidirected=False, ignore_direction=False, silent=True):
        """
        Generalized detach function for detaching nodes with edges
        """
        if(edge_set is None):
            edge_set = self.attached_edges(node_obj)
        link_order = [self, node_obj] if as_outbound else [node_obj, self]
        num_detached = 0
        for e in edge_set:
            # validate edge connection exists
            if(not e.connects(link_order[0], link_order[1],
                              ignore_direction=ignore_direction)):
                if(not silent):
                    logger.warning(
                        str(
                            f"{e} does not connect "
                            f"{link_order[0]} to {link_order[1]}")
                    )
                continue
            if(as_bidirected and not ignore_direction
               and not e.is_bidirected()):
                if(not silent):
                    logger.warning(
                        str(f"{e} is not a bidirected edge "))
                continue
            # destroy edge
            num_detached += 1
            e.destroy()
        return num_detached

    def detach_outbound(self, node_obj, edge_set=None, silent=True):
        """
        Destroy edges to a node
        edge_set is the list of edges to be detached (and distroyed)
        all edges are deteached and destroyed if edge_set empty
        returns number of detachments
        """
        return self.detach(node_obj, edge_set, as_outbound=True)

    def detach_inbound(self, node_obj, edge_set=None, silent=True):
        """
        Destroy edges from a node
        edge_set is the list of edges to be detached (and distroyed)
        all edges are deteached and destroyed if edge_set empty
        returns number of detachments
        """
        return self.detach(node_obj, edge_set, as_outbound=False)

    def detach_bidirected(self, node_obj, edge_set=None, silent=True):
        """
        Destroy bidirected edges between nodes
        edge_set is the list of edges to be detached (and distroyed)
        all edges are deteached and destroyed if edge_set empty
        returns number of detachments
        """
        return self.detach(node_obj, edge_set, as_bidirected=True)

    def detach_edges(self, node_obj, edge_set=None, silent=True):
        """
        Destroy given edges between nodes without checking orientation
        edge_set is the list of edges to be detached (and distroyed)
        all edges are deteached and destroyed if edge_set empty
        returns number of detachments
        """
        return self.detach(node_obj, edge_set, ignore_direction=True)

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
            if(e.is_bidirected() and e.connects(self, node_obj)):
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
            self.parent_node_ids.add_obj(node_obj)

    def make_owner_of(self, node_obj):
        """
        Adds node to lower dimension node and does relevant checks
        """
        node_obj.make_member_of(self)

    def leave_memebership_of(self, node_obj):
        """Remove node from higher dimension node"""
        node_obj.member_node_ids.remove_obj(self)
        self.parent_node_ids.remove_obj(node_obj)

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
        for i in self.edge_ids.obj_list():
            i.destroy()
        super().destroy()

    def dot_str(self, node_map=None):
        """
        DOT representation
        """
        if(node_map is None):
            nid = f'{uuid.UUID(self.jid).hex}'
        else:
            nid = f'{node_map.index(self.jid)}'

        dstr = f'"n{nid}" [ id="{uuid.UUID(self.jid).hex}", '
        dstr += f'label="n{nid}:{self.name}" '

        node_dict = self.context

        if (node_dict):
            for k, v in node_dict.items():
                if(not isinstance(v, str) or v == ""):
                    continue
                dstr += f', {k}="{v[:32]}"'

        dstr += ' ]'

        return dstr+'\n'
