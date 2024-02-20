'''Helper for the plugin builtin.'''
from __future__ import annotations

from typing import  Callable

from jaclang.core.construct import (
    EdgeArchitype,
    NodeArchitype,
)
__all__ = [
    "NodeArchitype",
    "EdgeArchitype",
]

def helper(node:NodeArchitype,cur_depth:float,connections:list,visited_nodes:list,queue:list,bfs:bool,dfs:Callable,depth:float,node_limit:int,edge_limit:int)-> None:
        '''Helper function for bfs and dfs.'''
        for edge in node._jac_.edges:
            is_self_loop = id( edge._jac_.source) == id(edge._jac_.target)
            is_in_edge =  edge._jac_.target== node 
            if is_self_loop: continue #lets skip self loop for a while      
            else:
                other_nd=edge._jac_.target if not is_in_edge else edge._jac_.source
                new_con=(node, other_nd,edge) if not is_in_edge else (other_nd, node,edge)
                if new_con not in connections:
                    if cur_depth<=depth and  node_limit>len(visited_nodes) and edge_limit>len(connections) :
                        connections.append(new_con)
                        if bfs:
                            queue.append([other_nd,cur_depth+1])
                        else:
                            dfs(other_nd,cur_depth+1)