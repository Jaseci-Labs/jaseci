from django.contrib.auth import get_user_model

from jaseci.utils.utils import TestCaseHelper
from django.test import TestCase

from jaseci_serv.base.models import JaseciObject
from jaseci.graph import node
from jaseci.graph.graph import Graph
from jaseci.actor.sentinel import Sentinel
import jaseci.tests.jac_test_code as jtc
from jaseci_serv.utils.test_utils import skip_without_redis


# Alias for create user
create_user = get_user_model().objects.create_user
get_user = get_user_model().objects.get


class OrmPrivateTests(TestCaseHelper, TestCase):
    """Test Jaseci Engine when authenticated"""

    def setUp(self):
        super().setUp()
        self.user = create_user(
            email="JSCadft@jaseci.com",
            password="testpass",
            name="some dude",
        )

    def tearDown(self):
        super().tearDown()

    def test_jsci_db_to_engine_hook_on_authenticate_saving(self):
        """Test that db hooks are set up correctly for saving"""
        user = self.user
        self.assertIsNotNone(user._h)
        tnode = node.Node(m_id="anon", h=user._h)
        tnode.name = "GOBBY"
        tnode.save()  # Jaseci object save
        user._h.commit()

        load_test = JaseciObject.objects.get(jid=tnode.id)
        self.assertEqual(load_test.name, tnode.name)

    def test_jsci_db_to_engine_hook_on_authenticate_loading(self):
        """Test that db hooks are set up correctly for loading"""
        user = self.user
        self.assertIsNotNone(user._h)
        temp_id = node.Node(m_id=user.master.urn, h=user._h).id
        h = user._h
        h.commit()
        del h.mem[temp_id.urn]
        if h.redis.is_running():
            h.redis.delete(temp_id.urn)

        load_test = JaseciObject.objects.filter(jid=temp_id).first()

        load_test.kind = "Fasho!"
        load_test.save()  # Jaseci model save
        self.assertIsInstance(load_test, JaseciObject)

        otnode = user._h.get_obj(load_test.j_master.urn, load_test.jid)
        self.assertEqual(load_test.kind, otnode.kind)

    def test_jsci_db_to_engine_hook_on_authenticated_transacting(self):
        """
        Test that db hooks are set up correctly for loading then saving back
        then deleting, also tests that '_id' and '_ids' conventions handle
        uuid types loading from db
        """
        user = self.user
        self.assertIsNotNone(user._h)
        temp_id = node.Node(m_id="anon", h=user._h).id

        h = user._h
        h.commit()
        del h.mem[temp_id.urn]
        if h.redis.is_running():
            h.redis.delete(temp_id.urn)

        load_test = JaseciObject.objects.filter(jid=temp_id).first()

        load_test.kind = "Fasheezzy!"
        load_test.save()  # Jaseci model save

        otnode = user._h.get_obj(load_test.j_master.urn, load_test.jid)
        self.assertEqual(load_test.kind, otnode.kind)

        otnode.name = "Rizzoou"
        oedge = otnode.attach_outbound(node.Node(m_id=otnode._m_id, h=otnode._h))
        otnode.save()  # Jaseci object save
        user._h.commit()
        oload_test = JaseciObject.objects.get(jid=otnode.id)
        self.assertEqual(oload_test.name, otnode.name)
        # Below tests loading hex uuid strings and converting to uuid type
        newobj = otnode._h.get_obj_from_store(oload_test.jid)
        self.assertIn(oedge[0], newobj.edge_ids.obj_list())

        otnode.destroy()
        self.assertFalse(
            JaseciObject.objects.filter(jid=oload_test.jid).exists(), False
        )

    def test_jsci_walker_writes_through_graph_updates(self):
        """
        Test that db hooks handle walkers ok
        """
        user = self.user
        gph = Graph(m_id="anon", h=user._h)
        sent = Sentinel(m_id="anon", h=gph._h)
        sent.register_code(jtc.prog1)
        test_node = sent.arch_ids.get_obj_by_name("life", kind="node").run()
        test_walker = sent.run_architype("get_gen_day")
        test_walker.prime(test_node)
        test_walker.context["date"] = "2010-08-03T03:00:00.000000"
        self.assertEqual(len(test_node.outbound_nodes()), 0)
        next = test_walker.step()
        self.assertEqual(test_node.outbound_nodes()[0], next)

    def test_parent_ids_stored_and_loaded_as_uuid(self):
        """
        Test that UUIDs function correctly for store adn loads
        """
        user = self.user
        node1 = node.Node(m_id="anon", h=user._h)
        node2 = node.Node(m_id="anon", h=user._h, parent=node1)
        user._h.commit()
        new_node = JaseciObject.objects.filter(j_parent=node1.id).first()
        new_jsci_node = user._h.get_obj_from_store(new_node.jid)
        self.assertEqual(node2.id, new_node.jid)
        self.assertEqual(node1.id, new_jsci_node.parent().id)

    @skip_without_redis
    def test_redis_connection(self):
        """Test redis connection"""

        redis = self.user._h.redis

        self.assertTrue(redis.is_running())

        redis.set("test", "this is a test")
        self.assertEqual(redis.get("test"), "this is a test")

    def test_redis_saving(self):
        """Test that redis hooks are set up correctly for saving"""
        tnode = node.Node(m_id="anon", h=self.user._h)
        tnode.name = "GOBBY"
        tnode.save()  # Jaseci object save
        tnode._h.commit()
        load_test = tnode._h.get_obj_from_store(tnode.id)
        self.assertEqual(load_test.name, tnode.name)

    def test_redis_loading(self):
        """
        Test that redis hooks are set up correctly for loading single server
        """
        nd = node.Node(m_id="anon", h=self.user._h)
        temp_id = nd.id
        nd._h.commit()
        load_test = nd._h.get_obj("anon", temp_id)

        load_test.kind = "Fasho!"
        load_test.save()
        load_test._h.commit()
        otnode = load_test._h.get_obj(load_test._m_id, load_test.id)
        self.assertEqual(load_test.kind, otnode.kind)

    def test_redis_transacting(self):
        """
        Test that db hooks are set up correctly for loading then saving back
        then deleting, also tests that '_id' and '_ids' conventions handle
        uuid types loading from db
        """
        nd = node.Node(m_id="anon", h=self.user._h)
        temp_id = nd.id
        nd._h.commit()

        load_test = nd._h.get_obj("anon", temp_id)

        load_test.kind = "Fasheezzy!"
        load_test.save()  # Jaseci model save
        load_test._h.commit()

        otnode = nd._h.get_obj(load_test._m_id, load_test.id)
        self.assertEqual(load_test.kind, otnode.kind)

        otnode.name = "Rizzoou"
        oedge = otnode.attach_outbound(node.Node(m_id="anon", h=self.user._h))
        otnode.save()  # Jaseci object save
        otnode._h.commit()
        oload_test = otnode._h.get_obj("anon", otnode.id)
        self.assertEqual(oload_test.name, otnode.name)
        # Below tests loading hex uuid strings and converting to uuid type
        newobj = otnode._h.get_obj_from_store(oload_test.id)
        self.assertIn(oedge[0], newobj.edge_ids.obj_list())

        otnode.destroy()
        self.assertIsNone(newobj._h.get_obj(oload_test._m_id, oload_test.id))
