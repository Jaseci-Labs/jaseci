import uuid
from unittest import TestCase

import jaseci.tests.jac_test_code as jtc
from jaseci.prim.sentinel import Sentinel
from jaseci.prim.element import Element
from jaseci.prim.graph import Graph
from jaseci.prim.node import Node
from jaseci.jsorc.jsorc import JsOrc
from jaseci.utils.utils import TestCaseHelper, get_all_subclasses
from jaseci.prim.architype import Architype


class ArchitypeTests(TestCaseHelper, TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_object_creation_basic_no_side_creation(self):
        """ """
        mast = JsOrc.master()
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
        mast = JsOrc.master()
        node1 = Node(m_id=mast._m_id, h=mast._h)
        node2 = Node(m_id=mast._m_id, h=mast._h)
        edge = node1.attach_outbound(node2)
        self.assertEqual(len(node1.smart_edge_list), 1)
        self.assertEqual(len(node2.smart_edge_list), 1)
        self.assertEqual(len(edge), 1)
        edge[0].destroy()
        self.assertEqual(len(node1.smart_edge_list), 0)
        self.assertEqual(len(node2.smart_edge_list), 0)

    def test_object_creation_by_sentinel_no_leaks(self):
        """
        Test that the destroy of sentinels clears owned objects
        """
        mast = JsOrc.master()
        num_objs = len(mast._h.mem.keys())
        self.assertEqual(num_objs, 2)
        new_graph = Graph(m_id=mast._m_id, h=mast._h)
        sent = Sentinel(m_id=mast._m_id, h=mast._h)
        code = jtc.prog1
        mast.sentinel_ids.add_obj(sent)
        mast.graph_ids.add_obj(new_graph)
        num_new = len(mast._h.mem.keys())
        self.assertEqual(num_new, num_objs + 2)

        sent.register_code(code)
        num_objs = len(mast._h.mem.keys())
        sent.register_code(code)
        new_num = len(mast._h.mem.keys())
        self.assertEqual(num_objs, new_num)

    def test_json_blob_of_objects(self):
        """
        Test saving object to json and back to python dict
        """
        for i in get_all_subclasses(Element):
            kwargs = {"m_id": 0, "h": JsOrc.hook()}
            orig = i(**kwargs)
            blob1 = orig.json(detailed=True)
            new = i(**kwargs)
            self.assertNotEqual(orig.id, new.id)
            new.json_load(blob1)
            self.assertEqual(orig.id, new.id)
            self.assertTrue(orig.is_equivalent(new))

    def test_supermaster_can_touch_all_data(self):
        mh = JsOrc.hook()
        mast = JsOrc.master(h=mh)
        mast2 = JsOrc.master(h=mh)
        node12 = Node(m_id=mast2._m_id, h=mast2._h)
        supmast = JsOrc.super_master(h=mh)
        bad = mh.get_obj(mast._m_id, node12.jid)
        good = mh.get_obj(supmast._m_id, node12.jid)
        self.assertEqual(good, node12)
        self.assertNotEqual(bad, node12)
        self.assertIsNone(bad)

    def test_id_list_smart_name_error(self):
        mast = JsOrc.master()
        sent = Sentinel(m_id=mast._m_id, h=mast._h)
        self.assertIn("arch_ids", sent.arch_ids.obj_for_id_not_exist_error(0))

    def test_dont_store_invalid_feilds_in_blob(self):
        mast = JsOrc.master()
        sent = Sentinel(m_id=mast._m_id, h=mast._h)
        sent.fake_data = 5
        stored = sent.jsci_payload()
        sent2 = Sentinel(m_id=mast._m_id, h=mast._h)
        sent2.json_load(stored)
        self.assertNotIn("fake_data", vars(sent2).keys())

    def test_sentinel_default_archs_dont_grow(self):
        mast = JsOrc.master()
        sent = Sentinel(m_id=mast._m_id, h=mast._h)
        sent.register_code(text="node simple; walker init {}")
        before = sent._h.get_object_distribution()[Architype]
        stored = sent.jsci_payload()
        sent2 = Sentinel(m_id=mast._m_id, h=mast._h)
        sent2.json_load(stored)
        sent2 = Sentinel(m_id=mast._m_id, h=mast._h)
        sent2.json_load(stored)
        after = sent2._h.get_object_distribution()[Architype]
        self.assertEqual(before, after)

    def test_sentinel_default_archs_dont_grow_multi_compile(self):
        mast = JsOrc.master()
        sent = Sentinel(m_id=mast._m_id, h=mast._h)
        sent.register_code(text="node simple; walker init {}")
        before = sent._h.get_object_distribution()[Architype]
        stored = sent.jsci_payload()
        sent2 = Sentinel(m_id=mast._m_id, h=mast._h)
        sent2.json_load(stored)
        sent2.register_code(text="node simple; walker init {}")
        before_id = sent2.arch_ids[0]
        sent2.register_code(text="node simple; walker init {}")
        sent2.register_code(text="node simple; walker init {}")
        after_id = sent2.arch_ids[0]
        after = sent2._h.get_object_distribution()[Architype]
        self.assertEqual(before, after)
        self.assertNotEqual(before_id, after_id)

    def test_id_list_heals(self):
        mast = JsOrc.master()
        sent = Sentinel(m_id=mast._m_id, h=mast._h)
        sent.register_code(text="node simple; walker init {}")
        before = len(sent.arch_ids)
        sent._h.get_obj(mast._m_id, sent.arch_ids[1]).destroy()
        sent._h.get_obj(mast._m_id, sent.arch_ids[3]).destroy()
        sent.arch_ids.obj_list()
        after = len(sent.arch_ids)
        self.assertEqual(after, before - 2)
