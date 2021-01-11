from core.element import mem_hook
from core.graph import node

import random as rand


def randomized_graph(num_nodes=10, num_edges=20,  h=mem_hook()):
    """Create a random graph with random connnections"""
    nodes = []
    edges = []
    for i in range(num_nodes):
        nodes.append(node.node(h=h))

    while(len(edges) < num_edges):
        node1 = nodes[rand.randrange(num_nodes)]
        node2 = nodes[rand.randrange(num_nodes)]
        if(node1.is_attached_out(node2)):
            continue
        else:
            edges.append(node1.attach_outbound(node2))

    hd_node = node.node(h=h, dimension=1)
    for i in nodes:
        hd_node.make_owner_of(i)
