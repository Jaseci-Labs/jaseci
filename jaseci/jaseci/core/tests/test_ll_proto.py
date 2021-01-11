
from core.utils.mem_hook import mem_hook
from core.actor.sentinel import sentinel
from core.graph.graph import graph

from core.utils.utils import TestCaseHelper
import core.tests.jac_test_code as jtc
import uuid


class jac_tests(TestCaseHelper):
    """Unit tests for Jac language"""

    def setUp(self):
        super().setUp()
        self.gph = graph(h=mem_hook())
        self.sent = sentinel(h=self.gph._h)

    def tearDown(self):
        super().tearDown()

    def test_ll_proto_load(self):
        """Test loading/parsing ll prototype"""
        rand_id = uuid.uuid4()
        init_ctx = {'owner': rand_id.urn}
        self.sent.register_code(jtc.ll_proto, init_ctx)
        self.assertTrue(self.sent.is_active)

    def test_rand_generation(self):
        """Test loading/parsing ll prototype"""
        self.sent.register_code(jtc.ll_proto)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        gen_walker = self.sent.walker_ids.get_obj_by_name('gen_rand_life')
        gen_walker.prime(self.gph.outbound_nodes()[0])
        gen_walker.run()
        self.assertGreater(len(self.gph._h.mem.keys()), 70)

    def test_objects_created(self):
        """Test loading/parsing ll prototype"""
        self.sent.register_code(jtc.ll_proto)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        gen_walker = self.sent.walker_ids.get_obj_by_name('gen_rand_life')
        gen_walker.prime(self.gph.outbound_nodes()[0])
        gen_walker.run()
        for i in self.gph._h.mem.keys():
            self.gph._h.mem[i].json()

    def test_get_latest_day(self):
        """Test loading/parsing ll prototype"""
        self.sent.register_code(jtc.ll_proto)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        gen_walker = self.sent.walker_ids.get_obj_by_name('gen_rand_life')
        gen_walker.prime(self.gph.outbound_nodes()[0])
        gen_walker.run()
        lday_walk = self.sent.walker_ids.get_obj_by_name(
            'get_latest_day')
        lday_walk.prime(self.gph.outbound_nodes()[0])
        lday_walk.run()
        ret = lday_walk.context['latest_day']
        self.assertEqual(self.gph._h.get_obj(uuid.UUID(ret)).kind, 'day')

    def test_carry_forward(self):
        """Test loading/parsing ll prototype"""
        self.sent.register_code(jtc.ll_proto)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        gen_walker = self.sent.walker_ids.get_obj_by_name('gen_rand_life')
        gen_walker.prime(self.gph)
        gen_walker.run()
        lday_walk = self.sent.walker_ids.get_obj_by_name(
            'get_gen_day')
        lday_walk.prime(self.gph)
        lday_walk.run()
        day = self.gph._h.get_obj(
            uuid.UUID(lday_walk.context['day_node']))
        self.assertGreater(len(day.edge_ids), 3)
