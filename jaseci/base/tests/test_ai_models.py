from core.utils.mem_hook import mem_hook
from core.actor.sentinel import sentinel
from core.graph.graph import graph

from core.utils.utils import TestCaseHelper
from django.test import TestCase
import core.tests.jac_test_code as jtc


class jac_tests(TestCaseHelper, TestCase):
    """Unit tests for Jac language"""

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_basic_USE_calls_from_jac(self):
        """Test the execution of a basic walker building graph"""
        gph = graph(h=mem_hook())
        sent = sentinel(h=gph._h)
        sent.register_code(jtc.prog1)
        test_node = sent.arch_ids.get_obj_by_name('node.life').run()
        test_walker = \
            sent.walker_ids.get_obj_by_name('use_test')
        test_walker.prime(test_node)
        report = test_walker.run()
        test_walker.save()
        test_walker._h.commit()
        self.assertEqual(len(report[0]), 2)
        self.assertEqual(len(report[0][1]), 2)

    def test_basic_USE_single_string_calls_from_jac(self):
        """Test the execution of a basic walker building graph"""
        gph = graph(h=mem_hook())
        sent = sentinel(h=gph._h)
        sent.register_code(jtc.prog1)
        test_node = sent.arch_ids.get_obj_by_name('node.life').run()
        test_walker = \
            sent.walker_ids.get_obj_by_name('use_test_single')
        test_walker.prime(test_node)
        report = test_walker.run()
        test_walker.save()
        test_walker._h.commit()
        self.assertEqual(len(report[0]), 1)
        self.assertEqual(len(report[0][0]), 1)

    def test_USE_qa_with_ctx(self):
        """Test the execution of a basic walker building graph"""
        gph = graph(h=mem_hook())
        sent = sentinel(h=gph._h)
        sent.register_code(jtc.prog1)
        test_node = sent.arch_ids.get_obj_by_name('node.life').run()
        test_walker = \
            sent.walker_ids.get_obj_by_name('use_test_with_ctx')
        test_walker.prime(test_node)
        report = test_walker.run()
        test_walker.save()
        test_walker._h.commit()
        self.assertEqual(len(report[0]), 1)
        self.assertEqual(len(report[0][0]), 1)

    def test_USE_qa_with_ctx_clean(self):
        """Test the execution of a basic walker building graph"""
        gph = graph(h=mem_hook())
        sent = sentinel(h=gph._h)
        sent.register_code(jtc.prog1)
        test_node = sent.arch_ids.get_obj_by_name('node.life').run()
        test_walker = \
            sent.walker_ids.get_obj_by_name('use_test_with_ctx2')
        test_walker.prime(test_node)
        report = test_walker.run()
        test_walker.save()
        test_walker._h.commit()
        self.assertEqual(len(report), 8)
        self.assertEqual(len(report[0]), 1)
        self.assertEqual(len(report[0][0]), 1)
