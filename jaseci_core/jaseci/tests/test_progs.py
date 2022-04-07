from jaseci.utils.mem_hook import mem_hook
from jaseci.actor.sentinel import sentinel
from jaseci.graph.graph import graph


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
        self.logger_on()
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtp.bug_check1)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        ret = test_walker.run()
        self.log(ret)
        report = test_walker.report
        self.assertEqual(len(report), 3)
