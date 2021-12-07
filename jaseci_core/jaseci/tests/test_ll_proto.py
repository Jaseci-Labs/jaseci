
from jaseci.utils.mem_hook import mem_hook
from jaseci.actor.sentinel import sentinel
from jaseci.graph.graph import graph
from jaseci.jac.machine.jac_value import jac_elem_unwrap as jeu

from jaseci.utils.utils import TestCaseHelper
from unittest import TestCase
import jaseci.tests.jac_test_code as jtc


class jac_tests(TestCaseHelper, TestCase):
    """Unit tests for Jac language"""

    def setUp(self):
        super().setUp()
        self.gph = graph(m_id='anon', h=mem_hook())
        self.sent = sentinel(m_id='anon', h=self.gph._h)

    def tearDown(self):
        super().tearDown()

    def test_ll_proto_load(self):
        """Test loading/parsing ll prototype"""
        self.sent.register_code(jtc.ll_proto)
        self.assertTrue(self.sent.is_active)

    def test_rand_generation(self):
        """Test loading/parsing ll prototype"""
        self.sent.register_code(jtc.ll_proto)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        gen_walker = self.sent.walker_ids.get_obj_by_name(
            'gen_rand_life', kind='walker')
        gen_walker.prime(self.gph.outbound_nodes()[0])
        gen_walker.run()
        self.assertGreater(len(self.gph._h.mem.keys()), 70)

    def test_objects_created(self):
        """Test loading/parsing ll prototype"""
        self.sent.register_code(jtc.ll_proto)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        gen_walker = self.sent.walker_ids.get_obj_by_name(
            'gen_rand_life', kind='walker')
        gen_walker.prime(self.gph.outbound_nodes()[0])
        gen_walker.run()
        for i in self.gph._h.mem.keys():
            if(i == 'global'):
                continue
            self.gph._h.mem[i].json()

    def test_get_latest_day(self):
        """Test loading/parsing ll prototype"""
        self.sent.register_code(jtc.ll_proto)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        gen_walker = self.sent.walker_ids.get_obj_by_name(
            'gen_rand_life', kind='walker')
        gen_walker.prime(self.gph.outbound_nodes()[0])
        gen_walker.run()
        lday_walk = self.sent.walker_ids.get_obj_by_name(
            'get_latest_day')
        lday_walk.prime(self.gph.outbound_nodes()[0])
        lday_walk.run()
        ret = lday_walk.context['latest_day']
        self.assertEqual(jeu(ret, self.gph).name, 'day')

    def test_carry_forward(self):
        """Test loading/parsing ll prototype"""
        self.sent.register_code(jtc.ll_proto)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        gen_walker = self.sent.walker_ids.get_obj_by_name(
            'gen_rand_life', kind='walker')
        gen_walker.prime(self.gph)
        gen_walker.run()
        lday_walk = self.sent.walker_ids.get_obj_by_name(
            'get_gen_day')
        lday_walk.prime(self.gph)
        lday_walk.run()
        day = jeu(lday_walk.context['day_node'], self.gph)
        self.assertGreater(len(day.edge_ids), 3)
