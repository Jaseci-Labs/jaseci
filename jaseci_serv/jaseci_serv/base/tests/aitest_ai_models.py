from django.test import TestCase

import jaseci.actions.live_actions as lact
import jaseci.tests.jac_test_code as jtc
from jaseci.actor.sentinel import sentinel
from jaseci.graph.graph import Graph
from jaseci.utils.utils import TestCaseHelper
from jaseci_serv.svc import MetaService


class JacTests(TestCaseHelper, TestCase):
    """Unit tests for Jac language"""

    def setUp(self):
        super().setUp()
        self.meta = MetaService()

    def tearDown(self):
        super().tearDown()

    def test_basic_use_calls_from_jac(self):
        """Test the execution of a basic walker building graph"""
        if not lact.load_remote_actions("http://js-use-qa"):
            self.skipTest("external resource not available")
        gph = Graph(m_id="anon", h=self.meta.build_hook())
        sent = sentinel(m_id=gph._m_id, h=gph._h)
        sent.register_code(jtc.prog1)
        test_node = sent.arch_ids.get_obj_by_name("life", kind="node").run()
        test_walker = sent.run_architype("use_test")
        test_walker.prime(test_node)
        report = test_walker.run()
        test_walker.save()
        test_walker._h.commit()
        self.assertEqual(len(report["report"][0]), 2)
        self.assertEqual(len(report["report"][0][1]), 2)

    def test_basic_use_single_string_calls_from_jac(self):
        """Test the execution of a basic walker building Graph"""
        if not lact.load_remote_actions("http://js-use-qa"):
            self.skipTest("external resource not available")
        gph = Graph(m_id="anon", h=self.meta.build_hook())
        sent = sentinel(m_id=gph._m_id, h=gph._h)
        sent.register_code(jtc.prog1)
        test_node = sent.arch_ids.get_obj_by_name("life", kind="node").run()
        test_walker = sent.run_architype("use_test_single")
        test_walker.prime(test_node)
        report = test_walker.run()
        test_walker.save()
        test_walker._h.commit()
        self.assertEqual(len(report["report"][0]), 1)
        self.assertEqual(len(report["report"][0][0]), 1)

    def test_use_qa_with_ctx(self):
        """Test the execution of a basic walker building Graph"""
        if not lact.load_remote_actions("http://js-use-qa"):
            self.skipTest("external resource not available")
        gph = Graph(m_id="anon", h=self.meta.build_hook())
        sent = sentinel(m_id=gph._m_id, h=gph._h)
        sent.register_code(jtc.prog1)
        test_node = sent.arch_ids.get_obj_by_name("life", kind="node").run()
        test_walker = sent.run_architype("use_test_with_ctx")
        test_walker.prime(test_node)
        report = test_walker.run()
        test_walker.save()
        test_walker._h.commit()
        self.assertEqual(len(report["report"][0]), 1)
        self.assertEqual(len(report["report"][0][0]), 1)

    def test_use_qa_with_ctx_clean(self):
        """Test the execution of a basic walker building Graph"""
        if not lact.load_remote_actions("http://js-use-qa"):
            self.skipTest("external resource not available")
        gph = Graph(m_id="anon", h=self.meta.build_hook())
        sent = sentinel(m_id=gph._m_id, h=gph._h)
        sent.register_code(jtc.prog1)
        test_node = sent.arch_ids.get_obj_by_name("life", kind="node").run()
        test_walker = sent.run_architype("use_test_with_ctx2")
        test_walker.prime(test_node)
        report = test_walker.run()
        test_walker.save()
        test_walker._h.commit()
        self.assertEqual(len(report["report"]), 8)
        self.assertEqual(len(report["report"][0]), 1)
        self.assertEqual(len(report["report"][0][0]), 1)
