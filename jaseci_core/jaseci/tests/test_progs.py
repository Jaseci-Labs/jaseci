from jaseci.utils.mem_hook import mem_hook
from jaseci.actor.sentinel import sentinel
from jaseci.graph.graph import graph
from jaseci.element.super_master import super_master
from jaseci.element.master import master
from jaseci.utils.utils import TestCaseHelper
from unittest import TestCase
import jaseci.tests.jac_test_progs as jtp


class jac_tests(TestCaseHelper, TestCase):
    """Unit tests for Jac language"""

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_bug_check1(self):
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtp.bug_check1)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        report = test_walker.report
        self.assertEqual(report[0][0], "THIS IS AN INTENT_LABEL")

    def test_action_load_std_lib(self):
        mast = super_master(h=mem_hook())
        mast.sentinel_register(name='test', code=jtp.action_load_std_lib)
        report = mast.general_interface_to_api(
            api_name='walker_run', params={'name': 'aload'})['report']
        self.assertEqual(report[0], True)

    def test_action_load_std_lib_only_super(self):
        mast = master(h=mem_hook())
        mast.sentinel_register(name='test', code=jtp.action_load_std_lib)
        report = mast.general_interface_to_api(
            api_name='walker_run', params={'name': 'aload'})
        report = report['report']
        self.assertEqual(report[0], False)

    def test_globals(self):
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtp.globals)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        report = test_walker.report
        self.assertEqual(report, ["testing", 56])

    def test_net_root_std_lib(self):
        mast = master(h=mem_hook())
        mast.sentinel_register(name='test', code=jtp.net_root_std_lib)
        report = mast.general_interface_to_api(
            api_name='walker_run', params={'name': 'init'})['report']
        self.assertEqual(report[0][0], report[0][1])
        self.assertEqual(report[0][1], report[1][1])
        self.assertNotEqual(report[1][0], report[1][1])

    def test_or_stmt(self):
        mast = master(h=mem_hook())
        mast.sentinel_register(name='test', code=jtp.or_stmt)
        report = mast.general_interface_to_api(
            api_name='walker_run', params={'name': 'init'})['report']
        self.assertEqual(report, [[3.4, "Hello"]])

    def test_nd_equals(self):
        mast = master(h=mem_hook())
        mast.sentinel_register(
            name='test', code=jtp.nd_equals_error_correct_line)
        report = mast.general_interface_to_api(
            api_name='walker_run', params={'name': 'init'})
        self.assertIn("line 3", report['errors'][0])
