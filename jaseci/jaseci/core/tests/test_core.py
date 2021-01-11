from core.utils.utils import TestCaseHelper

from core.graph.node import node
from core.master import master
from core.element import element
from core.graph.graph import graph
from core.actor.sentinel import sentinel
from core.utils.mem_hook import mem_hook
from core.utils.utils import get_all_subclasses
import core.tests.jac_test_code as jtc


class architype_tests(TestCaseHelper):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_object_creation_basic_no_side_creation(self):
        """

        """
        mast = master(h=mem_hook())
        num_objs = len(mast._h.mem.keys())
        node1 = node(h=mast._h)
        node2 = node(h=mast._h, owner_id=node1.id)
        num_new = len(mast._h.mem.keys())
        self.assertEqual(num_new, num_objs+2)

        new_graph = graph(h=mast._h)
        mast.graph_ids.add_obj(new_graph)
        num_new = len(mast._h.mem.keys())
        self.assertEqual(num_new, num_objs+3)

        new_graph.attach_outbound(node1)
        new_graph.attach_outbound(node2)
        num_new = len(mast._h.mem.keys())
        self.assertEqual(num_new, num_objs+5)

    def test_edge_removal_updates_nodes_edgelist(self):
        """

        """
        mast = master(h=mem_hook())
        node1 = node(h=mast._h)
        node2 = node(h=mast._h)
        edge = node1.attach_outbound(node2)
        self.assertEqual(len(node1.edge_ids), 1)
        self.assertEqual(len(node2.edge_ids), 1)
        edge.destroy()
        self.assertEqual(len(node1.edge_ids), 0)
        self.assertEqual(len(node2.edge_ids), 0)

    def test_object_creation_by_sentinel_no_leaks(self):
        """
        Test that the destroy of sentinels clears owned objects
        """
        mast = master(h=mem_hook())
        num_objs = len(mast._h.mem.keys())
        self.assertEqual(num_objs, 1)
        new_graph = graph(h=mast._h)
        sent = sentinel(h=mast._h)
        sent.code = jtc.prog1
        mast.sentinel_ids.add_obj(sent)
        mast.graph_ids.add_obj(new_graph)
        num_new = len(mast._h.mem.keys())
        self.assertEqual(num_new, num_objs+2)

        sent.register_code()
        num_objs = len(mast._h.mem.keys())
        sent.register_code()
        new_num = len(mast._h.mem.keys())
        self.assertEqual(num_objs, new_num)

    def test_json_blob_of_objects(self):
        for i in get_all_subclasses(element):
            orig = i(h=mem_hook())
            blob1 = orig.json()
            new = i(h=mem_hook())
            self.assertNotEqual(orig.id, new.id)
            new.json_load(blob1)
            self.assertEqual(orig.id, new.id)
            self.assertTrue(orig.is_equivalent(new))
