"""
Sentinel interpreter for jac code in AST form

This interpreter should be inhereted from the class that manages state
referenced through self.
"""
from jaseci.graph.node import node
from jaseci.graph.edge import edge
from jaseci.jac.interpreter.interp import interp
from jaseci.jac.machine.jac_scope import jac_scope
from jaseci.utils.utils import parse_str_token
from jaseci.jac.machine.jac_value import jac_elem_unwrap as jeu


class architype_interp(interp):
    """Jac interpreter mixin for objects that will execute Jac code"""

    def run_architype(self, jac_ast):
        """
        architype:
            KW_NODE NAME (COLON INT)? attr_block
            | KW_EDGE NAME attr_block
            | KW_GRAPH NAME graph_block;
        """
        if(jac_ast is None):  # Using defaults
            if(self.kind == 'node' and self.name in ['root', 'generic']):
                return node(m_id=self._m_id, h=self._h,
                            kind=self.kind, name=self.name)
            elif(self.kind == 'edge' and self.name in ['generic']):
                return edge(m_id=self._m_id, h=self._h,
                            kind=self.kind, name=self.name)
        kid = self.set_cur_ast(jac_ast)
        self.push_scope(
            jac_scope(
                parent=self,
                has_obj=self,
                action_sets=[]))
        if(kid[0].name == 'KW_NODE'):
            item = node(m_id=self._m_id, h=self._h,
                        kind=kid[0].token_text(), name=kid[1].token_text())
            if(kid[2].name == 'COLON'):
                item.dimension = int(kid[3].token_text())
            self.run_attr_block(kid[-1], item)
        elif(kid[0].name == 'KW_EDGE'):
            item = edge(m_id=self._m_id, h=self._h,
                        kind=kid[0].token_text(), name=kid[1].token_text())
            self.run_attr_block(kid[-1], item)
        elif (kid[0].name == 'KW_GRAPH'):
            item = self.run_graph_block(kid[-1])
        elif (jac_ast.name == 'graph_block'):  # used in jac tests
            item = self.run_graph_block(jac_ast)
        item.parent_id = self.parent().id
        self.pop_scope()
        return item

    def run_attr_block(self, jac_ast, obj):
        """
        attr_block:
            LBRACE (attr_stmt)* RBRACE
            | COLON (attr_stmt)* SEMI
            | SEMI;
        """
        kid = self.set_cur_ast(jac_ast)
        for i in kid:
            if(i.name == 'attr_stmt'):
                self.run_attr_stmt(i, obj)
        self._can_compiled_flag = True

    def run_graph_block(self, jac_ast):
        """
        graph_block: graph_block_spawn | graph_block_dot;
        """
        kid = self.set_cur_ast(jac_ast)
        return getattr(self, f'run_{kid[0].name}')(kid[0])

    def run_graph_block_spawn(self, jac_ast):
        """
        graph_block_spawn:
            LBRACE has_root KW_SPAWN code_block RBRACE
            | COLON has_root KW_SPAWN code_block SEMI;
        """
        kid = self.set_cur_ast(jac_ast)
        root_name = self.run_has_root(kid[1])
        m = interp(parent_override=self.parent(), caller=self)
        m.push_scope(jac_scope(parent=self,
                               has_obj=None,
                               action_sets=[]))
        m.run_code_block(kid[3])
        local_state = m._jac_scope.local_scope
        self.report = self.report + m.report
        if(root_name in local_state.keys()):
            obj = jeu(local_state[root_name], parent=self)
            if(not isinstance(obj, node)):
                self.rt_error(f"{root_name} is {type(obj)} not node!",
                              kid[2])
            return obj
        else:
            self.rt_error(f"Graph didn't produce root node!",
                          kid[2])
            return None

    def run_graph_block_dot(self, jac_ast):
        """
        graph_block_dot:
            LBRACE has_root dot_graph RBRACE
            | COLON has_root dot_graph SEMI;
        """
        kid = self.set_cur_ast(jac_ast)
        graph_state = {
            'strict': False,
            'digraph': True,
            'node_ops': [],
            'edge_ops': []
        }
        root_name = self.run_has_root(kid[1])
        self.run_dot_graph(kid[2], graph_state)

        nodes_def = {}
        for op in graph_state['node_ops']:
            node_id = op.pop('id', None)
            # TODO: is op actually needed?
            op.pop('op')
            if (node_id not in nodes_def):
                nodes_def[node_id] = op
            nodes_def[node_id].update(op)

        if (root_name not in nodes_def):
            del nodes_def
            self.rt_error(f"Graph didn't produce root node!",
                          kid[1])
            return None

        # Create node objects
        node_objs = {}
        for node_id, node_def in nodes_def.items():
            node_name = node_def.pop('node', None)
            if(node_name is None):
                self.rt_error('Missing "node" attribute for node.')
                continue
            node_obj = self.parent().run_architype(
                node_name, kind='node', caller=self)
            node_obj.set_context(node_def)

            # Overwrite node name with _n_name_ in the attrs if defined
            node_objs[node_id] = node_obj

        # Create edge objects
        edge_objs = []
        for op in graph_state['edge_ops']:
            edge_kind = op.pop('edge', None)
            if(edge_kind):
                edge_obj = self.parent().run_architype(
                    edge_kind, kind='edge', caller=self)
            else:
                edge_obj = edge(m_id=self._m_id, h=self._h,
                                kind='edge', name='generic')

            lhs_node_id = op.pop('lhs_node_id')
            rhs_node_id = op.pop('rhs_node_id')
            op.pop('op')
            op.pop('is_directional')
            edge_obj.set_context(op)
            lhs_node = node_objs.get(lhs_node_id, None)
            if(lhs_node is None):
                del nodes_def
                del node_objs
                del edge_objs
                self.rt_error('Invalid from node for edge')
                return None
            rhs_node = node_objs.get(rhs_node_id, None)
            if(rhs_node is None):
                del nodes_def
                del node_objs
                del edge_objs
                self.rt_error('Invalid to node for edge')

            lhs_node.attach_outbound(rhs_node, [edge_obj])
            edge_objs.append(edge_obj)

            # TODO: handle non-directional edge once that's supported in jac

        return node_objs[root_name]

    def run_has_root(self, jac_ast):
        """
        has_root: KW_HAS KW_ANCHOR NAME SEMI;
        """
        kid = self.set_cur_ast(jac_ast)
        return kid[2].token_text()

    def run_dot_graph(self, jac_ast, graph_state):
        """
        dot_graph:
            KW_STRICT? (KW_GRAPH | KW_DIGRAPH) dot_id? '{' dot_stmt_list '}';
        """
        # TODO: jac should support multiple edges between the same node but it
        # currently does not. once that's updates, need to update here
        # accordingly. We will only support non strict graph.
        kid = self.set_cur_ast(jac_ast)
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
        kid = self.set_cur_ast(jac_ast)
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
        kid = self.set_cur_ast(jac_ast)
        if (kid[0] == 'dot_id'):
            pass
        else:
            getattr(self, f'run_{kid[0].name}')(kid[0], graph_state)

    def run_dot_attr_stmt(self, jac_ast, graph_state):
        """
        dot_attr_stmt: (KW_GRAPH | KW_NODE | KW_EDGE) dot_attr_list
        """
        pass

    def run_dot_attr_list(self, jac_ast):
        """
        dot_attr_list: ('[' dot_a_list? ']')+
        """
        kid = self.set_cur_ast(jac_ast)
        attrs = {}
        while (len(kid) > 0):
            attrs.update(self.run_dot_a_list(kid[1]))
            kid = kid[3:]
        return attrs

    def run_dot_a_list(self, jac_ast):
        """
        dot_a_list: (dot_id('=' dot_id)? ','?)+
        """
        kid = self.set_cur_ast(jac_ast)
        a_list = {}
        while (len(kid) > 0):
            lhs_id = self.run_dot_id(kid[0])
            kid = kid[1:]
            if (len(kid) == 0 or kid[0].token_text() != '='):
                # If there is no rhs, treat it as a boolean value of True
                # e.g. [is_active, color=red] sets the attributes
                # is_active as True and color as "red"
                rhs_id = True
            else:
                rhs_id = self.run_dot_id(kid[1])
                kid = kid[2:]

            a_list[lhs_id] = rhs_id

            # deal with the optional comma
            if (len(kid) > 0 and kid[0].token_text() == ','):
                kid = kid[1:]

        return a_list

    def run_dot_edge_stmt(self, jac_ast, graph_state):
        """
        dot_edge_stmt: (dot_node_id | dot_subgraph) dot_edgeRHS dot_attr_list?
        """
        kid = self.set_cur_ast(jac_ast)
        if (kid[0] == 'dot_subgraph'):
            self.rt_error('Subgraphs not supported!', kid[0])
            return
        lhs_id = str(self.run_dot_node_id(kid[0]))
        graph_state['node_ops'].append({
            'op': 'create',
            'id': lhs_id
        })
        edge_attrs = {}
        if(kid[-1].name == 'dot_attr_list'):
            edge_attrs = self.run_dot_attr_list(kid[-1])
        self.run_dot_edgeRHS(kid[1], graph_state, lhs_id, edge_attrs)

    def run_dot_edgeRHS(self, jac_ast, graph_state, lhs_id, edge_attrs):
        """
        dot_edgeRHS: (dot_edgeop(dot_node_id | dot_subgraph))+
        """
        kid = self.set_cur_ast(jac_ast)
        cur_lhs_id = lhs_id
        while (len(kid) > 0):
            is_directional = self.run_dot_edgeop(kid[0])
            if (kid[1] == 'dot_subgraph'):
                self.rt_error('Subgraphs not supported!', kid[1])
                return
            rhs_id = str(self.run_dot_node_id(kid[1]))
            # Add create node rhs
            graph_state['node_ops'].append({
                'op': 'create',
                'id': rhs_id
            })
            # Add create edge
            edge_op = {
                'op': 'create',
                'is_directional': is_directional,
                'lhs_node_id': cur_lhs_id,
                'rhs_node_id': rhs_id
            }
            edge_op.update(edge_attrs)
            graph_state['edge_ops'].append(edge_op)
            cur_lhs_id = rhs_id
            kid = kid[2:]

    def run_dot_edgeop(self, jac_ast):
        """
        dot_edgeop: '->' | '--'
        """
        kid = self.set_cur_ast(jac_ast)
        if (kid[0].token_text() == '->'):
            return True
        else:
            return False

    def run_dot_node_stmt(self, jac_ast, graph_state):
        """
        dot_node_stmt: dot_node_id dot_attr_list?
        """
        kid = self.set_cur_ast(jac_ast)
        node_id = self.run_dot_node_id(kid[0])
        node_attrs = {}
        if (kid[-1].name == 'dot_attr_list'):
            node_attrs = self.run_dot_attr_list(kid[-1])
        node_create_op = {
            'op': 'create',
            'id': node_id,
        }
        graph_state['node_ops'].append(node_create_op)

        node_update_op = {
            'op': 'update',
            'id': node_id,
        }
        node_update_op.update(node_attrs)
        graph_state['node_ops'].append(node_update_op)

    def run_dot_node_id(self, jac_ast):
        """
        dot_node_id: dot_id dot_port?
        """
        kid = self.set_cur_ast(jac_ast)
        if (kid[-1].name == 'dot_port'):
            self.rt_warn('Node ports not supported')
        return self.run_dot_id(kid[0])

    def run_dot_port(self, jac_ast, graph_state):
        """
        dot_port: ':' dot_id(':' dot_id)?
        """
        pass

    def run_dot_subgraph(self, jac_ast, graph_state):
        """
        dot_subgraph: (KW_SUBGRAPH dot_id?)? '{' dot_stmt_list '}'
        """
        pass

    def run_dot_id(self, jac_ast):
        """
        dot_id:
            NAME
            | STRING
            | INT
            | FLOAT
            | KW_GRAPH
            | KW_NODE
            | KW_EDGE;
        """
        kid = self.set_cur_ast(jac_ast)
        if(kid[0].name == 'INT'):
            return int(kid[0].token_text())
        elif (kid[0].name == 'FLOAT'):
            return float(kid[0].token_text())
        elif(kid[0].name == 'STRING'):
            return parse_str_token(kid[0].token_text())
        return kid[0].token_text()
