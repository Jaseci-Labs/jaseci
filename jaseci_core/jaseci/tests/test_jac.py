from antlr4 import InputStream, CommonTokenStream
from jaseci.jac.jac_parse.jacLexer import jacLexer
from jaseci.jac.jac_parse.jacParser import jacParser
from jaseci.utils.mem_hook import mem_hook
from jaseci.actor.sentinel import sentinel
from jaseci.graph.graph import graph

from jaseci.utils.utils import TestCaseHelper
from unittest import TestCase
import jaseci.tests.jac_test_code as jtc


class jac_tests(TestCaseHelper, TestCase):
    """Unit tests for Jac language"""

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_antlr4_parsing_lifelogify(self):
        """Basic test of jac grammar with lifelogify program"""
        input_stream = InputStream(jtc.prog1)
        lexer = jacLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = jacParser(stream)
        parser.start()
        self.assertEqual(parser.getNumberOfSyntaxErrors(), 0)

    def test_sentinel_loading_jac_code(self):
        """Test the generation of jaseci trees for programs in grammar"""
        gph = graph(h=mem_hook())
        sent = sentinel(h=gph._h)
        sent.register_code(jtc.prog1)
        self.assertIsNotNone(
            sent.walker_ids.get_obj_by_name('get_gen_day'))
        self.assertIsNotNone(
            sent.arch_ids.get_obj_by_name('week', kind='node'))

    def test_sentinel_loading_jac_code_multiple_times(self):
        """Test registering resets correctly for multiple attempts"""
        gph = graph(h=mem_hook())
        sent = sentinel(h=gph._h)
        sent.register_code(jtc.prog0)
        num_walkers = len(sent.walker_ids)
        num_arch = len(sent.arch_ids)
        sent.register_code(jtc.prog0)
        self.assertEqual(len(sent.walker_ids), num_walkers)
        self.assertEqual(len(sent.arch_ids), num_arch)
        sent.register_code(jtc.prog0)
        self.assertEqual(len(sent.walker_ids), num_walkers)
        self.assertEqual(len(sent.arch_ids), num_arch)

    def test_sentinel_register_dep_on_static_errors(self):
        """Test Jac registering is dependant on correct static/dynamic code"""
        gph = graph(h=mem_hook())
        sent = sentinel(h=gph._h)
        correct = "node b { has anchor a; }"
        wrong1 = "adfdsf"
        sent.register_code(correct)
        self.assertTrue(sent.is_active)
        sent.register_code(wrong1)
        self.assertFalse(sent.is_active)
        sent.register_code(correct)
        self.assertTrue(sent.is_active)
        sent.register_code(wrong1)
        self.assertFalse(sent.is_active)
        sent.register_code(correct)
        self.assertTrue(sent.is_active)

    def test_sentinel_loading_arhitype(self):
        """Test the generation of jaseci trees for programs in grammar"""
        gph = graph(h=mem_hook())
        sent = sentinel(h=gph._h)
        sent.register_code(jtc.prog1)
        self.assertGreater(
            len(sent.arch_ids.get_obj_by_name('month', kind='node').code_ir),
            5)

    def test_sentinel_running_basic_walker(self):
        """Test the execution of a basic walker building graph"""
        gph = graph(h=mem_hook())
        sent = sentinel(h=gph._h)
        sent.register_code(jtc.prog1)
        test_node = sent.arch_ids.get_obj_by_name(
            'life', kind='node').run()
        test_walker = \
            sent.walker_ids.get_obj_by_name('get_gen_day')
        test_walker.prime(test_node)
        test_walker.context['date'] = '2010-08-03T03:00:00.000000'
        test_walker.run()
        self.assertEqual(len(test_node.outbound_nodes()), 1)
        self.assertEqual(test_node.outbound_nodes()[0].name, 'year')
        self.assertEqual(test_node.outbound_nodes()[0].
                         outbound_nodes()[0].outbound_nodes()[0].name, 'week')

    def test_sentinel_setp_running_walker(self):
        """Test the execution of a basic walker building graph"""
        gph = graph(h=mem_hook())
        sent = sentinel(h=gph._h)
        sent.register_code(jtc.prog1)
        test_node = sent.arch_ids.get_obj_by_name(
            'life', kind='node').run()
        test_walker = \
            sent.walker_ids.get_obj_by_name('get_gen_day')
        test_walker.prime(test_node)
        test_walker.context['date'] = '2010-08-03T03:00:00.000000'
        self.assertEqual(len(test_node.outbound_nodes()), 0)
        next = test_walker.step()
        self.assertEqual(test_node.outbound_nodes()[0], next)
        next = test_walker.step()
        next = test_walker.step()
        self.assertEqual(next.name, 'week')
        next = test_walker.step()
        next = test_walker.step()
        self.assertEqual(test_walker.current_step, 5)
        self.assertTrue(next)
        next = test_walker.step()
        self.assertFalse(next)

    def test_walker_writes_through_no_data_gain_loss_on_contexts(self):
        """
        Test that  no loss or gain of data on second trak on second trek
        """
        gph = graph(h=mem_hook())
        sent = sentinel(h=gph._h)
        sent.register_code(jtc.prog1)
        test_node = sent.arch_ids.get_obj_by_name(
            'life', kind='node').run()
        test_walker = \
            sent.walker_ids.get_obj_by_name('get_gen_day')
        test_walker.prime(test_node)
        test_walker.context['date'] = '2010-08-03T03:00:00.000000'
        self.assertEqual(test_walker.context['date'],
                         '2010-08-03T03:00:00.000000')
        test_walker.run()
        after_gen = len(gph._h.mem)
        test_walker.prime(test_node)
        test_walker.context['date'] = '2010-08-03T03:00:00.000000'
        test_walker.run()
        after_track = len(gph._h.mem)
        # Tests that more items were created the first time through
        self.assertEqual(after_gen, after_track)

    def test_arch_ids_generate_node_bound_objects_scalably(self):
        """
        Test that arch_ids in sents bind contents to actual nodes
        scalably (node contexts dont get deleted when arch_ids deleted)
        """
        gph = graph(h=mem_hook())
        sent = sentinel(h=gph._h)
        sent.register_code(jtc.prog1)
        test_node = sent.arch_ids.get_obj_by_name('life', kind='node').run()
        test_walker = \
            sent.walker_ids.get_obj_by_name('get_gen_day')
        test_walker.prime(test_node)
        test_walker.context['date'] = '2010-08-03T03:00:00.000000'
        self.assertEqual(test_walker.context['date'],
                         '2010-08-03T03:00:00.000000')
        test_walker.run()

        year_node = test_node.outbound_nodes()[0]
        before_del = year_node.context['year']
        sent.register_code(jtc.prog1)
        after_del = year_node.context['year']
        self.assertEqual(before_del, after_del)

    def test_sent_loads_complex_walker_and_arch(self):
        """Test loading attributes of arch and walkers"""
        gph = graph(h=mem_hook())
        sent = sentinel(h=gph._h)
        sent.register_code(jtc.prog1)
        test_node = sent.arch_ids.get_obj_by_name('test', kind='node').run()
        test_walker = \
            sent.walker_ids.get_obj_by_name('test')
        test_walker.prime(test_node)
        test_walker.run()
        self.assertEqual(test_node.context['c'],
                         '43Yeah \n"fools"!')

    def test_availabilty_of_global_functions(self):
        """Test preset function loading"""
        from jaseci.actions.global_actions import global_action_ids
        self.assertTrue(global_action_ids.has_obj_by_name('std.log'))

    def test_multiple_edged_between_nodes_work(self):
        """Test that multiple edges between the same two nodes are allowed"""
        gph = graph(h=mem_hook())
        sent = sentinel(h=gph._h)
        sent.register_code(jtc.edgey)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        edges = gph.get_all_edges()
        self.assertEqual(len(edges), 3)
        edge_names = [edges[0].name, edges[1].name, edges[2].name]
        self.assertIn('generic', edge_names)
        self.assertIn('apple', edge_names)
        self.assertIn('banana', edge_names)

    def test_multiple_edged_between_nodes_delete_all(self):
        """Test that multiple edges deleted correctly if delete all"""
        gph = graph(h=mem_hook())
        sent = sentinel(h=gph._h)
        sent.register_code(jtc.edgey2)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        edges = gph.get_all_edges()
        self.assertEqual(len(edges), 0)

    def test_multiple_edged_between_nodes_delete_all_specific(self):
        """Test that multiple edges deleted correctly if delete all"""
        gph = graph(h=mem_hook())
        sent = sentinel(h=gph._h)
        sent.register_code(jtc.edgey2b)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        edges = gph.get_all_edges()
        self.assertEqual(len(edges), 1)

    def test_multiple_edged_between_nodes_delete_all_labeled(self):
        """Test that multiple edges deleted correctly if delete all"""
        gph = graph(h=mem_hook())
        sent = sentinel(h=gph._h)
        sent.register_code(jtc.edgey2c)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        edges = gph.get_all_edges()
        self.assertEqual(len(edges), 3)

    def test_multiple_edged_between_nodes_delete_filtered(self):
        """Test that multiple edges deleted correctly if delete filtered"""
        gph = graph(h=mem_hook())
        sent = sentinel(h=gph._h)
        sent.register_code(jtc.edgey3)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        edges = gph.get_all_edges()
        self.assertEqual(len(edges), 5)

    def test_generic_can_be_used_to_specify_generic_edges(self):
        """Test that generic edge tag works"""
        gph = graph(h=mem_hook())
        sent = sentinel(h=gph._h)
        sent.register_code(jtc.edgey4)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        edges = gph.get_all_edges()
        self.assertEqual(len(edges), 2)

    def test_can_disconnect_multi_nodes_simultaneously(self):
        """Test disconnecting mutilpe nodes"""
        gph = graph(h=mem_hook())
        sent = sentinel(h=gph._h)
        sent.register_code(jtc.edgey5)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        edges = gph.get_all_edges()
        self.assertEqual(len(edges), 2)

    def test_can_connect_multi_nodes_simultaneously(self):
        """Test connecting mutilpe nodes"""
        gph = graph(h=mem_hook())
        sent = sentinel(h=gph._h)
        sent.register_code(jtc.edgey6)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        edges = gph.get_all_edges()
        self.assertEqual(len(edges), 4)

    def test_can_disconnect_multi_nodes_advanced(self):
        """Test disconnecting mutilpe nodes advanced"""
        gph = graph(h=mem_hook())
        sent = sentinel(h=gph._h)
        sent.register_code(jtc.edgey7)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        edges = gph.get_all_edges()
        self.assertEqual(len(edges), 3)

    def test_accessing_edges_basic(self):
        """Test accessing Edges"""
        gph = graph(h=mem_hook())
        sent = sentinel(h=gph._h)
        sent.register_code(jtc.edge_access)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        edges = gph.get_all_edges()
        if(edges[0].name == 'apple'):
            self.assertEqual(edges[0].context['v1'], 7)
            self.assertEqual(edges[1].context['x1'], 8)
        else:
            self.assertEqual(edges[1].context['v1'], 7)
            self.assertEqual(edges[0].context['x1'], 8)

    def test_has_assign(self):
        """Test assignment on definition"""
        gph = graph(h=mem_hook())
        sent = sentinel(h=gph._h)
        sent.register_code(jtc.has_assign)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        nodes = gph.get_all_nodes()
        self.assertEqual(len(nodes), 3)
        num = 0
        for i in nodes:
            if(i.name == 'test'):
                self.assertEqual(i.context['a'], 8)
                num += 1
        self.assertEqual(num, 2)
