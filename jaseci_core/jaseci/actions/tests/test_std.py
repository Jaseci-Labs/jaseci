from jaseci.utils.mem_hook import mem_hook
from jaseci.actor.sentinel import sentinel
from jaseci.graph.graph import graph

from jaseci.utils.utils import TestCaseHelper
from unittest import TestCase
import jaseci.actions.tests.std_test_code as stc


class jac_tests(TestCaseHelper, TestCase):
    """Unit tests for STD library language"""

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_rand_std(self):
        gph = graph(m_id="anon", h=mem_hook())
        sent = sentinel(m_id="anon", h=gph._h)
        sent.register_code(stc.rand_std)
        test_walker = sent.walker_ids.get_obj_by_name("init")
        test_walker.prime(gph)
        test_walker.run()
        report = test_walker.report
        self.assertEqual(len(report), 4)
        self.assertGreater(len(report[1]), len(report[0]))
        self.assertGreater(len(report[2]), len(report[1]))
        self.assertGreater(len(report[3]), len(report[2]))

    def test_file_io(self):
        gph = graph(m_id="anon", h=mem_hook())
        sent = sentinel(m_id="anon", h=gph._h)
        sent.register_code(stc.file_io)
        test_walker = sent.walker_ids.get_obj_by_name("init")
        test_walker.prime(gph)
        test_walker.run()
        report = test_walker.report
        self.assertEqual(report, ['{"a": 10}{"a": 10}'])

    def test_std_used_in_node_has_var(self):
        gph = graph(m_id="anon", h=mem_hook())
        sent = sentinel(m_id="anon", h=gph._h)
        sent.register_code(stc.std_used_in_node_has_var)
        test_walker = sent.walker_ids.get_obj_by_name("init")
        test_walker.prime(gph)
        test_walker.run()
        report = test_walker.report
        self.assertGreater(len(report[0]), 10)
        self.assertEqual(type(report[0]), str)
