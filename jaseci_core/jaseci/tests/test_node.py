from jaseci.utils.utils import TestCaseHelper
from unittest import TestCase
from jaseci.graph.node import node
from jaseci.attr import action
from jaseci.graph.edge import edge
from jaseci.element import element
from jaseci.utils.mem_hook import mem_hook
from jaseci.actor.architype import architype


class node_tests(TestCaseHelper, TestCase):
    """Tests for the funcationality of Jaseci node class"""

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_node_connections(self):
        """Test connecting and disconnecting etc of nodes"""
        node1 = node(m_id="anon", h=mem_hook())
        node2 = node(m_id="anon", h=node1._h)
        node3 = node(m_id="anon", h=node1._h)
        node4 = node(m_id="anon", h=node1._h)
        node1.attach_outbound(node2)
        node3.attach_outbound(node2)
        node1.attach_inbound(node2)
        node3.attach_inbound(node2)
        self.assertEqual(len(node2.inbound_nodes()), 2)
        self.assertEqual(node2.inbound_nodes()[0], node1)
        self.assertTrue(node2.is_attached_out(node3))
        self.assertTrue(node2.is_attached_in(node1))
        self.assertFalse(node4.is_equivalent(node2))

        node2.detach_inbound(node1)
        node2.detach_inbound(node3)
        node2.detach_outbound(node1)
        node2.detach_outbound(node3)

        self.assertTrue(node4.is_equivalent(node2))
        self.assertTrue(node3.is_equivalent(node1))
        self.assertTrue(node3.is_equivalent(node2))
        self.assertEqual(len(node1.inbound_nodes()), 0)
        self.assertEqual(len(node2.inbound_nodes()), 0)
        self.assertEqual(len(node3.inbound_nodes()), 0)
        self.assertEqual(len(node4.inbound_nodes()), 0)

    def test_add_context_to_node_and_destroy(self):
        """Test adding and removing contexts nodes"""
        node1 = node(m_id="anon", h=mem_hook())
        node1.context["yeah dude"] = "SUP"
        self.assertEqual(node1.context["yeah dude"], "SUP")
        self.assertEqual(len(node1.context.keys()), 1)
        self.assertTrue("yeah dude" in node1.context.keys())
        self.assertFalse("yeah  dude" in node1.context.keys())

    def test_add_entry_action_to_node_and_destroy(self):
        """Test connecting and disconnecting etc of nodes"""
        node1 = architype(m_id="anon", h=mem_hook())
        act = action.action(m_id="anon", h=node1._h, name="yeah dude", value="SUP")
        node1.entry_action_ids.add_obj(act)
        self.assertEqual(
            node1.entry_action_ids.get_obj_by_name("yeah dude").value, "SUP"
        )
        self.assertEqual(len(node1.entry_action_ids), 1)
        self.assertTrue(node1.entry_action_ids.has_obj_by_name("yeah dude"))
        self.assertFalse(node1.entry_action_ids.has_obj_by_name("yeah  dude"))

        node1.entry_action_ids.destroy_obj_by_name(name="yeah dude")
        self.assertEqual(len(node1.entry_action_ids), 0)
        self.assertFalse(node1.entry_action_ids.has_obj_by_name("yeah dude"))

    def test_adding_and_removing_from_hdnodes(self):
        """Test adding nodes and removing them from HDGDs"""
        node1 = node(m_id="anon", h=mem_hook())
        hdgd1 = node(m_id="anon", h=node1._h, name="yeah dude", dimension=1)
        node1.make_member_of(hdgd1)
        self.assertEqual(node1.parent_node_ids.obj_list()[0], hdgd1)
        self.assertEqual(hdgd1.member_node_ids.obj_list()[0], node1)

        hdgd2 = node(m_id="anon", h=node1._h, dimension=2)
        node1.make_member_of(hdgd2)
        self.assertNotIn(hdgd2.id, node1.parent_node_ids)

        node1.leave_memebership_of(hdgd1)
        self.assertEqual(len(hdgd1.member_node_ids), 0)

    def test_dimensions_must_match_to_connect_nodes(self):
        """Test dimension matching requirement for node connection"""
        node1 = node(m_id="anon", h=mem_hook())
        hdgd1 = node(m_id="anon", h=node1._h, name="yeah dude", dimension=1)
        node1.attach_outbound(hdgd1)
        self.assertFalse(node1.is_attached_out(hdgd1))

    def test_inherit_from_element_edge(self):
        """Test that inheriting params with kwargs works"""
        hook = element.mem_hook()
        a = edge(
            name="my edge",
            m_id="anon",
            h=hook,
            to_node=node(m_id="anon", h=hook),
            from_node=node(m_id="anon", h=hook),
        )
        self.assertEqual(a.name, "my edge")
