from antlr4 import InputStream, CommonTokenStream
from jaseci.jac.jac_parse.jacLexer import jacLexer
from jaseci.jac.jac_parse.jacParser import jacParser
from jaseci.utils.mem_hook import mem_hook
from jaseci.actor.sentinel import sentinel
from jaseci.graph.graph import graph
from jaseci.element.super_master import super_master
from jaseci.element.master import master

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
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.prog1)
        self.assertIsNotNone(
            sent.walker_ids.get_obj_by_name('get_gen_day'))
        self.assertIsNotNone(
            sent.arch_ids.get_obj_by_name('week', kind='node'))

    def test_sentinel_loading_jac_code_multiple_times(self):
        """Test registering resets correctly for multiple attempts"""
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
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
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
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
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.prog1)
        self.assertGreater(
            len(sent.arch_ids.get_obj_by_name('month', kind='node').code_ir),
            5)

    def test_sentinel_running_basic_walker(self):
        """Test the execution of a basic walker building graph"""
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
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
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
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
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
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
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
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
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.prog1)
        test_node = sent.arch_ids.get_obj_by_name(
            'testnode', kind='node').run()
        test_walker = \
            sent.walker_ids.get_obj_by_name('testwalk')
        test_walker.prime(test_node)
        test_walker.run()
        self.assertEqual(test_node.context['c'],
                         '43Yeah \n"fools"!')

    def test_availabilty_of_global_functions(self):
        """Test preset function loading"""
        self.assertGreater(len(mem_hook().global_action_list), 10)

    def test_multiple_edged_between_nodes_work(self):
        """Test that multiple edges between the same two nodes are allowed"""
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
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
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.edgey2)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        edges = gph.get_all_edges()
        self.assertEqual(len(edges), 0)

    def test_multiple_edged_between_nodes_delete_all_specific(self):
        """Test that multiple edges deleted correctly if delete all"""
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.edgey2b)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        edges = gph.get_all_edges()
        self.assertEqual(len(edges), 1)

    def test_multiple_edged_between_nodes_delete_all_labeled(self):
        """Test that multiple edges deleted correctly if delete all"""
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.edgey2c)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        edges = gph.get_all_edges()
        self.assertEqual(len(edges), 3)

    def test_multiple_edged_between_nodes_delete_filtered(self):
        """Test that multiple edges deleted correctly if delete filtered"""
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.edgey3)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        edges = gph.get_all_edges()
        self.assertEqual(len(edges), 5)

    def test_generic_can_be_used_to_specify_generic_edges(self):
        """Test that generic edge tag works"""
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.edgey4)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        edges = gph.get_all_edges()
        self.assertEqual(len(edges), 2)

    def test_can_disconnect_multi_nodes_simultaneously(self):
        """Test disconnecting mutilpe nodes"""
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.edgey5)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        edges = gph.get_all_edges()
        self.assertEqual(len(edges), 2)

    def test_can_connect_multi_nodes_simultaneously(self):
        """Test connecting mutilpe nodes"""
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.edgey6)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        edges = gph.get_all_edges()
        self.assertEqual(len(edges), 4)

    def test_can_disconnect_multi_nodes_advanced(self):
        """Test disconnecting mutilpe nodes advanced"""
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.edgey7)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        edges = gph.get_all_edges()
        self.assertEqual(len(edges), 3)

    def test_accessing_edges_basic(self):
        """Test accessing Edges"""
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
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
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.has_assign)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        nodes = gph.get_all_nodes()
        self.assertEqual(len(nodes), 3)
        num = 0
        for i in nodes:
            if(i.name == 'testnode'):
                self.assertEqual(i.context['a'], 8)
                num += 1
        self.assertEqual(num, 2)

    def test_global_get_set(self):
        """Test assignment on definition"""
        mast = super_master(h=mem_hook())
        gph = graph(m_id=mast.jid, h=mast._h)
        sent = sentinel(m_id=mast.jid, h=gph._h)
        sent.register_code(jtc.set_get_global)
        test_walker = \
            sent.walker_ids.get_obj_by_name('setter')
        test_walker.prime(gph)
        test_walker.run()
        test_walker2 = \
            sent.walker_ids.get_obj_by_name('getter')
        test_walker2.prime(gph)
        test_walker2.run()
        self.assertEqual(test_walker2.context['a'], 59)

    def test_global_set_requires_admin(self):
        """Test assignment on definition"""
        mast = master(h=mem_hook())
        gph = graph(m_id=mast.jid, h=mast._h)
        sent = sentinel(m_id=mast.jid, h=gph._h)
        sent.register_code(jtc.set_get_global)
        test_walker = \
            sent.walker_ids.get_obj_by_name('setter')
        test_walker.prime(gph)
        test_walker.run()
        test_walker2 = \
            sent.walker_ids.get_obj_by_name('getter')
        test_walker2.prime(gph)
        test_walker2.run()
        self.assertEqual(test_walker2.context['a'], None)

    def test_sentinel_version_label(self):
        """Test sentinel version labeling"""
        mast = master(h=mem_hook())
        gph = graph(m_id=mast.jid, h=mast._h)
        sent = sentinel(m_id=mast.jid, h=gph._h)
        sent.register_code(jtc.version_label)
        self.assertEqual(sent.version, 'alpha-1.0')

    def test_visibility_builtins(self):
        """Test builtins to see into nodes and edges"""
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.visibility_builtins)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        self.assertEqual(2, len(test_walker.report[0][0].keys()))
        self.assertGreaterEqual(len(test_walker.report[0][1].keys()), 7)
        self.assertLess(len(test_walker.report[0][1].keys()), 14)
        self.assertGreaterEqual(len(test_walker.report[0][2].keys()), 14)

    def test_spawn_ctx_for_edges_nodes(self):
        """Test builtins to see into nodes and edges"""
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.spawn_ctx_edge_node)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        self.assertEqual(test_walker.report[0]['age'], 32)
        self.assertEqual(test_walker.report[1]['meeting_place'], 'college')
        self.assertEqual(test_walker.report[2]['name'], 'Jane')
        self.assertEqual(test_walker.report[3]['kind'], 'sister')

    def test_filter_ctx_for_edges_nodes(self):
        """Test builtins to see into nodes and edges"""
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.filter_ctx_edge_node)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        self.assertEqual(test_walker.report[0]['age'], 30)
        self.assertEqual(len(test_walker.report[1]), 0)

    def test_null_handling(self):
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.null_handleing)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        self.assertEqual(test_walker.report[0], True)
        self.assertEqual(test_walker.report[1], False)
        self.assertEqual(test_walker.report[2], True)
        self.assertEqual(test_walker.report[3], False)

    def test_bool_type_convert(self):
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.bool_type_convert)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        self.assertEqual(test_walker.report[0], True)
        self.assertEqual(True, test_walker.report[1]['name'])

    def test_typecasts(self):
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.typecasts)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        self.assertEqual(test_walker.report[0], 7.6)
        self.assertEqual(test_walker.report[1], 7)
        self.assertEqual(test_walker.report[2], "7.6")
        self.assertEqual(test_walker.report[3], True)
        self.assertEqual(test_walker.report[4], 7.0)
        self.assertEqual(test_walker.report[5], "Types comes back correct")

    def test_typecast_error(self):
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.typecasts_error)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        self.assertIn('Cannot get edges from 7.6',
                      test_walker.runtime_errors[0])
        self.assertIn('Invalid cast of JAC_TYPE.STR to JAC_TYPE.INT',
                      test_walker.runtime_errors[1])

    def test_filter_on_context(self):
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.filter_on_context)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        self.assertEqual({'yo': 'Yeah i said'},
                         test_walker.report[0][0])
        self.assertNotIn("name",
                         test_walker.report[0][1].keys())
        self.assertIn("name",
                      test_walker.report[0][2].keys())

    def test_string_manipulation(self):
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.string_manipulation)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        rep = test_walker.report
        self.assertEqual(rep[0], 't')
        self.assertEqual(rep[1], 'tin')
        self.assertEqual(rep[2], 'sting me ')
        self.assertEqual(rep[3], ' TESTING ME  ')
        self.assertEqual(rep[4], ' testing me  ')
        self.assertEqual(rep[5], ' Testing Me  ')
        self.assertEqual(rep[6], ' testing me  ')
        self.assertEqual(rep[7], ' TeSTING ME  ')
        self.assertEqual(rep[8], False)
        self.assertEqual(rep[9], False)
        self.assertEqual(rep[10], False)
        self.assertEqual(rep[11], False)
        self.assertEqual(rep[12], False)
        self.assertEqual(rep[13], False)
        self.assertEqual(rep[14], False)
        self.assertEqual(rep[15], {'a': 5})
        self.assertEqual(rep[16], 2)
        self.assertEqual(rep[17], 5)
        self.assertEqual(rep[18], ['tEsting', 'me'])
        self.assertEqual(rep[19], [' t', 'sting me  '])
        self.assertEqual(rep[20], False)
        self.assertEqual(rep[21], False)
        self.assertEqual(rep[22], ' tEsting you  ')
        self.assertEqual(rep[23], 'tEsting me')
        self.assertEqual(rep[24], 'Esting me')
        self.assertEqual(rep[25], 'tEsting me  ')
        self.assertEqual(rep[26], 'sting me  ')
        self.assertEqual(rep[27], ' tEsting me')
        self.assertEqual(rep[28], ' tEsting m')
        self.assertEqual(rep[29], True)

    def test_list_manipulation(self):
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.list_manipulation)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        rep = test_walker.report
        self.assertEqual(rep[0], [4])
        self.assertEqual(rep[1], [5])
        self.assertEqual(rep[2], [4, 5, 5])
        self.assertEqual(rep[3], [5, 5, 4])
        self.assertEqual(rep[4], [4, 5, 5])
        self.assertEqual(rep[5], 2)
        self.assertEqual(rep[6], [5, 5, 4, 2])
        self.assertEqual(rep[7], [5, 'apple', 4, 2])
        self.assertEqual(rep[8], 1)
        self.assertEqual(rep[9], [5, 'apple', 4])
        self.assertEqual(rep[10], [])

    def test_dict_manipulation(self):
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.dict_manipulation)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        rep = test_walker.report
        self.assertEqual(rep[0], {'four': 4, 'five': 5})
        self.assertEqual(rep[1], {'four': 5, 'five': 5})
        self.assertEqual(rep[2], [['four', 4], ['five', 5]])
        self.assertEqual(rep[3], ['four', 'five'])
        self.assertEqual(rep[4], {'four': 4})
        self.assertEqual(rep[5], [4])
        self.assertEqual(rep[6], {'four': 7})
        self.assertEqual(rep[7], {})

    def test_string_join(self):
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.string_join)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        rep = test_walker.report
        self.assertEqual(rep[0], 'test_me_now')

    def test_sub_list(self):
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.sub_list)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        rep = test_walker.report
        self.assertEqual(rep[0][0], 5)
        self.assertEqual(rep[0][1], 6)
        self.assertEqual(rep[0][2], 7)

    def test_destroy_and_misc(self):
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.destroy_and_misc)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        rep = test_walker.report
        self.assertEqual(rep[0], 'Josh')
        self.assertEqual(
            rep[1],  {'name': 'Josh', 'age': 32,
                      'birthday': None, 'profession': None})
        self.assertEqual(
            rep[2], {'age': 32, 'birthday': None,
                     'name': 'pete', 'profession': None})
        self.assertEqual(rep[3], [1, 3])
        self.assertEqual(rep[4], {'a': 'b'})
        self.assertEqual(rep[5], [1, 2, 5, 6, 7, 8, 9])
        self.assertEqual(rep[6], [1, 2, 45, 33, 7, 8, 9])
        self.assertEqual(rep[7], None)
        self.assertEqual(rep[8], {'age': 32,
                                  'birthday': None,
                                  'name': 'pete',
                                  'profession': None})
        self.assertEqual(rep[9], True)

    def test_arbitrary_assign_on_element(self):
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.arbitrary_assign_on_element)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        rep = test_walker.report
        self.assertEqual(rep[0],  {'name': None,
                                   'age': None,
                                   'birthday': None,
                                   'profession': None})

    def test_try_else_stmts(self):
        self.logger_on()
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.try_else_stmts)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        rep = test_walker.report
        self.assertEqual(rep[0], {'args': ('division by zero',),
                                  'col': 8,
                                  'line': 5,
                                  'mod': 'basic',
                                  'msg': 'division by zero',
                                  'type': 'ZeroDivisionError'})
        self.assertEqual(rep[1], 'dont need err')
        self.assertEqual(rep[2], None)
        self.assertEqual(rep[3], 2)

    def test_node_edge_same_name(self):
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.node_edge_same_name)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        rep = test_walker.report
        self.assertEqual(rep[0], {'meeting_place': 'college'})
        self.assertEqual(
            rep[1], {'age': 32, 'birthday': None,
                     'name': 'Josh', 'profession': None})

    def test_testcases(self):
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.testcases)
        sent.run_tests(silent=True)
        self.assertEqual(len(sent.testcases), 4)
        for i in sent.testcases:
            self.assertEqual(i['passed'], True)

    def test_testcase_asserts(self):
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.testcase_asserts)
        sent.run_tests(silent=True)
        self.assertEqual(len(sent.testcases), 3)
        self.assertEqual(sent.testcases[0]['passed'], True)
        self.assertEqual(sent.testcases[1]['passed'], False)
        self.assertEqual(sent.testcases[2]['passed'], False)

    def test_report_not_to_jacset(self):
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.report_not_to_jacset)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        rep = test_walker.report
        self.assertIn('context', rep[0][0].keys())
        self.assertIn('j_type', rep[0][0].keys())

    def test_walker_spawn_unwrap_check(self):
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.walker_spawn_unwrap_check)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        rep = test_walker.report
        self.assertTrue(rep[0].startswith('urn:uuid'))

    def test_std_get_report(self):
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.std_get_report)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        rep = test_walker.report
        self.assertEqual(rep, [3, 5, 6, 7, [3, 5, 6, 7], 8])

    def test_func_with_array_index(self):
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.func_with_array_index)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        rep = test_walker.report
        self.assertEqual(rep, [3, 5, 3])

    def test_rt_error_test1(self):
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.rt_error_test1)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        self.assertIn("List index out of range",
                      test_walker.runtime_errors[0])
        self.assertIn(" line ",
                      test_walker.runtime_errors[0])
        self.assertIn(" col ",
                      test_walker.runtime_errors[0])

    def test_root_type_nodes(self):
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.root_type_nodes)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        report = test_walker.report
        self.assertEqual(report, ["root", "root"])

    def test_invalid_key_error(self):
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.invalid_key_error)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        errors = test_walker.runtime_errors
        self.assertGreater(len(errors), 0)

    def test_file_io(self):
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.file_io)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        report = test_walker.report
        self.assertEqual(report, ['{"a": 10}{"a": 10}'])

    def test_auto_cast(self):
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.auto_cast)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        report = test_walker.report
        self.assertEqual(report, [True, True])

    def test_no_error_on_dict_key_assign(self):
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.no_error_on_dict_key_assign)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        report = test_walker.report
        self.assertEqual(report, [{'b': 4}])
        self.assertEqual(len(test_walker.runtime_errors), 0)

    def test_report_status(self):
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtc.report_status)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        report = test_walker.report
        self.assertEqual(report, ['hello'])
        self.assertEqual(test_walker.report_status, 302)
