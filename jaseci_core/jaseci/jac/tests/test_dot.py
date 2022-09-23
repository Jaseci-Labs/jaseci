import io
import sys
from unittest import TestCase

import jaseci.jac.tests.dot_code as dtc
from jaseci.actor.sentinel import Sentinel
from jaseci.graph.graph import Graph
from jaseci.svc import MetaService
from jaseci.utils.utils import TestCaseHelper


class TestDot(TestCaseHelper, TestCase):
    """Unit test for DOT support"""

    def setUp(self):
        super().setUp()
        self.sent = Sentinel(m_id="anon", h=MetaService().hook())
        self.gph = Graph(m_id="anon", h=self.sent._h)

        self.old_stdout = sys.stdout
        self.new_stdout = io.StringIO()
        sys.stdout = self.new_stdout

    def tearDown(self):
        sys.stdout = self.old_stdout
        super().tearDown()

    def to_screen(self):
        sys.stdout = self.old_stdout
        print("output: ", self.new_stdout.getvalue())
        sys.stdout = self.new_stdout

    def test_dot_node(self):
        """Test node in dot"""
        self.sent.register_code(dtc.dot_node)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(), "graph_root_node_name\n")

    def test_dot_node_no_dot_id(self):
        """Test node in dot with no do graph name"""
        self.sent.register_code(dtc.dot_node_no_dot_id)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(), "graph_root_node_name\n")

    def test_spawn_graph_node(self):
        """Test node in using spawn graphs instead of dot"""
        self.sent.register_code(dtc.spawn_graph_node)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(), "graph_root_node_name\n")

    def test_dot_node_multi_stmts(self):
        """Test node in dot, defined with multiple statements."""
        self.sent.register_code(dtc.dot_node_multi_stmts)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(), "real_test_node\n" "2021\n")

    def test_dot_edge(self):
        """Test edge in dot."""
        self.sent.register_code(dtc.dot_edge)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(), "root\n" "node_1\n" "node_2\n")

    def test_dot_edge_with_attrs(self):
        """Test edge in dot with attrs"""
        self.sent.register_code(dtc.dot_edge_with_attrs)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(), "root\n" "node_1\n")

    def test_dot_edge_with_attrs_vars(self):
        """Test edge in dot with attrs and variables"""
        self.sent.register_code(dtc.dot_edge_with_attrs_vars)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(), "edge_1\n" "node_1\n")

    def test_dot_graph_parses(self):
        self.sent.register_code(dtc.dot_graph)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()

    def test_dot_str(self):
        self.sent.register_code(dtc.dot_graph)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        dot_str = self.gph.graph_dot_str()
        self.assertTrue("strict digraph root" in dot_str)

    def test_dot_quoted_string(self):
        self.sent.register_code(dtc.dot_quoted_string)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        report = gen_walker.report
        self.assertEqual(report, ["root", "this has space", "another space"])
