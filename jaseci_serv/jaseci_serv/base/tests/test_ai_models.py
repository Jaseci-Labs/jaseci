from jaseci.utils.mem_hook import mem_hook
from jaseci.actor.sentinel import sentinel
from jaseci.graph.graph import graph

from jaseci.utils.utils import TestCaseHelper
from django.test import TestCase
import jaseci.tests.jac_test_code as jtc
import jaseci.actions.live_actions as lact


class jac_tests(TestCaseHelper, TestCase):
    """Unit tests for Jac language"""

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_basic_USE_calls_from_jac(self):
        """Test the execution of a basic walker building graph"""
        if (not lact.load_remote_actions('http://js-use-qa')):
            self.skipTest("external resource not available")
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id=gph._m_id, h=gph._h)
        sent.register_code(jtc.prog1)
        test_node = sent.arch_ids.get_obj_by_name('life', kind='node').run()
        test_walker = \
            sent.walker_ids.get_obj_by_name('use_test')
        test_walker.prime(test_node)
        report = test_walker.run()
        test_walker.save()
        test_walker._h.commit()
        self.assertEqual(len(report['report'][0]), 2)
        self.assertEqual(len(report['report'][0][1]), 2)

    def test_basic_USE_single_string_calls_from_jac(self):
        """Test the execution of a basic walker building graph"""
        if (not lact.load_remote_actions('http://js-use-qa')):
            self.skipTest("external resource not available")
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id=gph._m_id, h=gph._h)
        sent.register_code(jtc.prog1)
        test_node = sent.arch_ids.get_obj_by_name('life', kind='node').run()
        test_walker = \
            sent.walker_ids.get_obj_by_name('use_test_single')
        test_walker.prime(test_node)
        report = test_walker.run()
        test_walker.save()
        test_walker._h.commit()
        self.assertEqual(len(report['report'][0]), 1)
        self.assertEqual(len(report['report'][0][0]), 1)

    def test_USE_qa_with_ctx(self):
        """Test the execution of a basic walker building graph"""
        if (not lact.load_remote_actions('http://js-use-qa')):
            self.skipTest("external resource not available")
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id=gph._m_id, h=gph._h)
        sent.register_code(jtc.prog1)
        test_node = sent.arch_ids.get_obj_by_name('life', kind='node').run()
        test_walker = \
            sent.walker_ids.get_obj_by_name('use_test_with_ctx')
        test_walker.prime(test_node)
        report = test_walker.run()
        test_walker.save()
        test_walker._h.commit()
        self.assertEqual(len(report['report'][0]), 1)
        self.assertEqual(len(report['report'][0][0]), 1)

    def test_USE_qa_with_ctx_clean(self):
        """Test the execution of a basic walker building graph"""
        if (not lact.load_remote_actions('http://js-use-qa')):
            self.skipTest("external resource not available")
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id=gph._m_id, h=gph._h)
        sent.register_code(jtc.prog1)
        test_node = sent.arch_ids.get_obj_by_name('life', kind='node').run()
        test_walker = \
            sent.walker_ids.get_obj_by_name('use_test_with_ctx2')
        test_walker.prime(test_node)
        report = test_walker.run()
        test_walker.save()
        test_walker._h.commit()
        self.assertEqual(len(report['report']), 8)
        self.assertEqual(len(report['report'][0]), 1)
        self.assertEqual(len(report['report'][0][0]), 1)
