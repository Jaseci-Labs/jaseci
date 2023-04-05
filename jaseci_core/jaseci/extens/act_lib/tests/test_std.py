from unittest import TestCase

import jaseci.extens.act_lib.tests.std_test_code as stc
from jaseci.prim.sentinel import Sentinel
from jaseci.prim.graph import Graph
from jaseci.jsorc.jsorc import JsOrc
from jaseci.utils.utils import TestCaseHelper


class JacTests(TestCaseHelper, TestCase):
    """Unit tests for STD library language"""

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_rand_std(self):
        sent = Sentinel(m_id=0, h=JsOrc.hook())
        gph = Graph(m_id=0, h=sent._h)
        sent.register_code(stc.rand_std)
        test_walker = sent.run_architype("init")
        test_walker.prime(gph)
        test_walker.run()
        report = test_walker.report
        self.assertEqual(len(report), 4)
        self.assertGreater(len(report[1]), len(report[0]))
        self.assertGreater(len(report[2]), len(report[1]))
        self.assertGreater(len(report[3]), len(report[2]))

    def test_file_io(self):
        sent = Sentinel(m_id=0, h=JsOrc.hook())
        gph = Graph(m_id=0, h=sent._h)
        sent.register_code(stc.file_io)
        test_walker = sent.run_architype("init")
        test_walker.prime(gph)
        test_walker.run()
        report = test_walker.report
        self.assertEqual(report, ['{"a": 10}{"a": 10}'])

    def test_std_used_in_node_has_var(self):
        sent = Sentinel(m_id=0, h=JsOrc.hook())
        gph = Graph(m_id=0, h=sent._h)
        sent.register_code(stc.std_used_in_node_has_var)
        test_walker = sent.run_architype("init")
        test_walker.prime(gph)
        test_walker.run()
        report = test_walker.report
        self.assertGreater(len(report[0]), 10)
        self.assertEqual(type(report[0]), str)
