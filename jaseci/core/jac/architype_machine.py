"""
Sentinel machine for jac code in AST form

This machine should be inhereted from the class that manages state referenced
through self.
"""
from core.graph.node import node
from core.graph.edge import edge
from core.jac.machine import machine


class architype_machine(machine):
    """Jac machine mixin for objects that will execute Jac code"""

    def run_architype(self, jac_ast):
        """
        architype:
            KW_NODE NAME (COLON INT)? attr_block
            | KW_EDGE NAME attr_block
            | KW_GRAPH NAME graph_block;
        """
        kid = jac_ast.kid
        if(kid[0].name == 'KW_NODE'):
            item = node(h=self._h, kind=kid[1].token_text())
            if(kid[2].name == 'COLON'):
                item.dimension = int(kid[3].token_text())
            self.run_attr_block(kid[-1], item)
        elif(kid[0].name == 'KW_EDGE'):
            item = edge(h=self._h, kind=kid[1].token_text())
            self.run_attr_block(kid[-1], item)
        elif (kid[0].name == 'KW_GRAPH'):
            item = self.run_graph_block(kid[-1])
        item.owner_id = self.owner().id
        return item

    def run_attr_block(self, jac_ast, obj):
        """
        attr_block:
            LBRACE (attr_stmt)* RBRACE
            | COLON (attr_stmt)* SEMI
            | SEMI;
        """
        kid = jac_ast.kid
        for i in kid:
            if(i.name == 'attr_stmt'):
                self.run_attr_stmt(i, obj)

    def run_graph_block(self, jac_ast):
        """
        graph_block:
            LBRACE has_root dot_graph RBRACE
            | COLON has_root dot_graph SEMI;
        """
        kid = jac_ast.kid
        graph_state = {'root_name': self.run_has_root(kid[1]),
                       'root_node': None,
                       'strict': False,
                       'digraph': True,
                       'node': [],
                       'edge': [],
                       'subgraph': []}
        self.run_dot_graph(kid[2], graph_state)
        gph = graph_state['root_node']
        if (not gph):
            self.rt_error(f"Graph didn't produce root node!",
                          kid[0])
        return gph

    def run_has_root(self, jac_ast):
        """
        has_root: KW_HAS KW_ANCHOR NAME SEMI;
        """
        kid = jac_ast.kid
        return kid[2].token_text()

    def run_dot_graph(self, jac_ast, graph_state):
        """
        dot_graph:
            KW_STRICT? (KW_GRAPH | KW_DIGRAPH) dot_id? '{' dot_stmt_list '}';
        """
        kid = jac_ast.kid
        if (kid[0].name == 'KW_STRICT'):
            graph_state['strict'] = True
            kid = kid[1:]
        if (kid[0].name == 'KW_GRAPH'):
            graph_state['digraph'] = False
            kid = kid[1:]
        if (kid[0].name == 'dot_id'):
            kid = kid[1:]
        self.run_dot_stmt_list(kid[1], graph_state)

    def run_dot_stmt_list(self, jac_ast, graph_state):
        """
        dot_stmt_list: (dot_stmt ';'?)*
        """
        kid = jac_ast.kid
        for i in kid:
            if(i.name == 'dot_stmt'):
                self.run_dot_stmt(i, graph_state)

    def run_dot_stmt(self, jac_ast, graph_state):
        """
        dot_stmt:
            dot_node_stmt
            | dot_edge_stmt
            | dot_attr_stmt
            | dot_id '=' dot_id
            | dot_subgraph
        """
        kid = jac_ast.kid
        if (kid[0] == 'dot_id'):
            pass
        else:
            getattr(self, f'run_{kid[0].name}')(kid[0], graph_state)

    def run_dot_attr_stmt(self, jac_ast, graph_state):
        """
        dot_attr_stmt: (KW_GRAPH | KW_NODE | KW_EDGE) dot_attr_list
        """
        kid = jac_ast.kid

    def run_dot_attr_list(self, jac_ast):
        """
        dot_attr_list: ('[' dot_a_list? ']')+
        """
        kid = jac_ast.kid

    def run_dot_a_list(self, jac_ast, graph_state):
        """
        dot_a_list: (dot_id('=' dot_id)? ','?)+
        """
        kid = jac_ast.kid

    def run_dot_edge_stmt(self, jac_ast, graph_state):
        """
        dot_edge_stmt: (dot_node_id | dot_subgraph) dot_edgeRHS dot_attr_list?
        """
        kid = jac_ast.kid
        if (kid[0] == 'dot_subgraph'):
            self.rt_error('Subgraphs not supported!', kid[0])
            return
        lhs_name = str(self.run_dot_node_id(kid[0]))
        attrs = {}
        if(kid[-1].name == 'dot_attr_list'):
            attrs = self.run_dot_attr_list(kid[-1])
        edges = self.run_dot_edgeRHS(kid[1], graph_state, lhs_name)
        for edge in edges:
            edge['attrs'] = attrs
        graph_state['edge'] += edges

    def run_dot_edgeRHS(self, jac_ast, graph_state, lhs):
        """
        dot_edgeRHS: (dot_edgeop(dot_node_id | dot_subgraph))+
        """
        kid = jac_ast.kid
        cur_lhs = lhs
        edges = []
        while (len(kid) > 0):
            is_directional = self.run_dot_edgeop(kid[0])
            if (kid[1] == 'dot_subgraph'):
                self.rt_error('Subgraphs not supported!', kid[1])
                return
            rhs_name = str(self.run_dot_node_id(kid[1]))
            edges.append({
                'lhs': cur_lhs,
                'rhs': rhs_name,
                'is_directional': is_directional
            })
            cur_lhs = rhs_name
            kid = kid[2:0]
        return edges

    def run_dot_edgeop(self, jac_ast):
        """
        dot_edgeop: '->' | '--'
        """
        kid = jac_ast.kid
        if (kid[0].token_text == '->'):
            return True
        else:
            return False

    def run_dot_node_stmt(self, jac_ast, graph_state):
        """
        dot_node_stmt: dot_node_id dot_attr_list?
        """
        kid = jac_ast.kid

    def run_dot_node_id(self, jac_ast):
        """
        dot_node_id: dot_id dot_port?
        """
        kid = jac_ast.kid
        if (kid[-1].name == 'dot_port'):
            self.rt_warn('Node ports not supported')
        return self.run_dot_id(kid[0])

    def run_dot_port(self, jac_ast, graph_state):
        """
        dot_port: ':' dot_id(':' dot_id)?
        """
        kid = jac_ast.kid

    def run_dot_subgraph(self, jac_ast, graph_state):
        """
        dot_subgraph: (KW_SUBGRAPH dot_id?)? '{' dot_stmt_list '}'
        """
        kid = jac_ast.kid

    def run_dot_id(self, jac_ast):
        """
        dot_id: NAME | STRING | INT | FLOAT
        """
        kid = jac_ast.kid
        if(kid[0].name == 'INT'):
            return int(kid[0].token_text())
        if (kid[0].name == 'FLOAT'):
            return float(kid[0].token_text())
        return kid[0].token_text()
