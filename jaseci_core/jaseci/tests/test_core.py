import uuid
from unittest import TestCase

import jaseci.tests.jac_test_code as jtc
from jaseci.actor.sentinel import Sentinel
from jaseci.element.element import Element
from jaseci.graph.graph import Graph
from jaseci.graph.node import Node
from jaseci.svc import MetaService
from jaseci.utils.utils import TestCaseHelper, get_all_subclasses


class ArchitypeTests(TestCaseHelper, TestCase):
    def setUp(self):
        super().setUp()
        self.meta = MetaService()

    def tearDown(self):
        super().tearDown()

    def test_object_creation_basic_no_side_creation(self):
        """ """
        mast = self.meta.master()
        num_objs = len(mast._h.mem.keys())
        node1 = Node(m_id=mast._m_id, h=mast._h)
        node2 = Node(m_id=mast._m_id, h=mast._h, parent=node1)
        num_new = len(mast._h.mem.keys())
        self.assertEqual(num_new, num_objs + 2)

        new_graph = Graph(m_id=mast._m_id, h=mast._h)
        mast.graph_ids.add_obj(new_graph)
        num_new = len(mast._h.mem.keys())
        self.assertEqual(num_new, num_objs + 3)

        new_graph.attach_outbound(node1)
        new_graph.attach_outbound(node2)
        num_new = len(mast._h.mem.keys())
        self.assertEqual(num_new, num_objs + 5)

    def test_edge_removal_updates_nodes_edgelist(self):
        """ """
        mast = self.meta.master()
        node1 = Node(m_id=mast._m_id, h=mast._h)
        node2 = Node(m_id=mast._m_id, h=mast._h)
        edge = node1.attach_outbound(node2)
        self.assertEqual(len(node1.edge_ids), 1)
        self.assertEqual(len(node2.edge_ids), 1)
        self.assertEqual(len(edge), 1)
        edge[0].destroy()
        self.assertEqual(len(node1.edge_ids), 0)
        self.assertEqual(len(node2.edge_ids), 0)

    def test_object_creation_by_sentinel_no_leaks(self):
        """
        Test that the destroy of sentinels clears owned objects
        """
        mast = self.meta.master()
        num_objs = len(mast._h.mem.keys()) - len(mast._h.global_action_list)
        self.assertEqual(num_objs, 2)
        new_graph = Graph(m_id=mast._m_id, h=mast._h)
        sent = Sentinel(m_id=mast._m_id, h=mast._h)
        code = jtc.prog1
        mast.sentinel_ids.add_obj(sent)
        mast.graph_ids.add_obj(new_graph)
        num_new = len(mast._h.mem.keys()) - len(mast._h.global_action_list)
        self.assertEqual(num_new, num_objs + 2 + 3)

        sent.register_code(code)
        num_objs = len(mast._h.mem.keys()) - len(mast._h.global_action_list)
        sent.register_code(code)
        new_num = len(mast._h.mem.keys()) - len(mast._h.global_action_list)
        self.assertEqual(num_objs, new_num)

    def test_json_blob_of_objects(self):
        """
        Test saving object to json and back to python dict
        """
        for i in get_all_subclasses(Element):
            kwargs = {"m_id": "anon", "h": self.meta.hook()}
            orig = i(**kwargs)
            blob1 = orig.json(detailed=True)
            new = i(**kwargs)
            self.assertNotEqual(orig.id, new.id)
            new.json_load(blob1)
            self.assertEqual(orig.id, new.id)
            self.assertTrue(orig.is_equivalent(new))

    def test_supermaster_can_touch_all_data(self):
        mh = self.meta.hook()
        mast = self.meta.master(h=mh)
        mast2 = self.meta.master(h=mh)
        node12 = Node(m_id=mast2._m_id, h=mast2._h)
        supmast = self.meta.super_master(h=mh)
        bad = mh.get_obj(mast._m_id, uuid.UUID(node12.jid))
        good = mh.get_obj(supmast._m_id, uuid.UUID(node12.jid))
        self.assertEqual(good, node12)
        self.assertNotEqual(bad, node12)
        self.assertIsNone(bad)
