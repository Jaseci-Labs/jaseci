from django.contrib.auth import get_user_model

from core.utils.utils import TestCaseHelper
from django.test import TestCase

from base.models import JaseciObject
from core.graph import node
from core.graph.graph import graph
from core.actor.sentinel import sentinel
from core.utils import graph_gen
from core.utils.mem_hook import mem_hook
from base.redis_hook import redis_hook
from jaseci.settings import REDIS_HOST
import core.tests.jac_test_code as jtc

import redis


# Alias for create user
create_user = get_user_model().objects.create_user
get_user = get_user_model().objects.get


class jaseci_engine_tests_private(TestCaseHelper, TestCase):
    """Test Jaseci Engine when authenticated"""

    def setUp(self):
        super().setUp()
        self.user = create_user(
            email='JSCadft@jaseci.com',
            password='testpass',
            name='some dude',
        )
        self._h = mem_hook()

    def tearDown(self):
        super().tearDown()

    def test_jsci_db_to_engine_hook_on_authenticate_saving(self):
        """Test that db hooks are set up correctly for saving"""
        user = self.user
        self.assertIsNotNone(user._h)
        tnode = node.node(h=user._h)
        tnode.name = "GOBBY"
        tnode.save()  # Jaseci object save
        user._h.commit()

        load_test = JaseciObject.objects.get(jid=tnode.id)
        self.assertEqual(load_test.name, tnode.name)

    def test_jsci_db_to_engine_hook_on_authenticate_loading(self):
        """Test that db hooks are set up correctly for loading"""
        user = self.user
        self.assertIsNotNone(user._h)
        temp_id = node.node(h=user._h).id

        user._h.commit()
        del user._h.mem[temp_id]
        user._h.red.delete(temp_id.urn)

        load_test = JaseciObject.objects.filter(jid=temp_id).first()

        load_test.kind = "Fasho!"
        load_test.save()  # Jaseci model save
        self.assertIsInstance(load_test, JaseciObject)

        otnode = user._h.get_obj(load_test.jid)
        self.assertEqual(load_test.kind, otnode.kind)

    def test_jsci_db_to_engine_hook_on_authenticated_transacting(self):
        """
        Test that db hooks are set up correctly for loading then saving back
        then deleting, also tests that '_id' and '_ids' conventions handle
        uuid types loading from db
        """
        user = self.user
        self.assertIsNotNone(user._h)
        temp_id = node.node(h=user._h).id

        user._h.commit()
        del user._h.mem[temp_id]
        user._h.red.delete(temp_id.urn)

        load_test = JaseciObject.objects.filter(jid=temp_id).first()

        load_test.kind = "Fasheezzy!"
        load_test.save()  # Jaseci model save

        otnode = user._h.get_obj(load_test.jid)
        self.assertEqual(load_test.kind, otnode.kind)

        otnode.name = "Rizzoou"
        oedge = otnode.attach_outbound(node.node(h=otnode._h))
        otnode.save()  # Jaseci object save
        user._h.commit()
        oload_test = JaseciObject.objects.get(jid=otnode.id)
        self.assertEqual(oload_test.name, otnode.name)
        # Below tests loading hex uuid strings and converting to uuid type
        newobj = otnode._h.get_obj_from_store(oload_test.jid)
        self.assertIn(oedge, newobj.edge_ids.obj_list())

        otnode.destroy()
        self.assertFalse(
            JaseciObject.objects.filter(jid=oload_test.jid).exists(), False
        )

    def test_jsci_node_class_methods_writes_edges_through(self):
        """
        Test that db hooks are set up correctly for loading then saving back
        then deleting
        """
        graph_gen.randomized_graph(h=self._h)
        self.assertEqual(len(self._h.mem), 31)

    def test_jsci_walker_writes_through_graph_updates(self):
        """
        Test that db hooks handle walkers ok
        """
        user = self.user
        gph = graph(h=user._h)
        sent = sentinel(h=gph._h)
        sent.register_code(jtc.prog1)
        test_node = sent.arch_ids.get_obj_by_name('node.life').run()
        test_walker = \
            sent.walker_ids.get_obj_by_name('get_gen_day')
        test_walker.prime(test_node)
        test_walker.context['date'] = '2010-08-03T03:00:00.000000'
        self.assertEqual(len(test_node.outbound_nodes()), 0)
        next = test_walker.step()
        self.assertEqual(test_node.outbound_nodes()[0], next)

    def test_owner_ids_stored_and_loaded_as_uuid(self):
        """
        Test that UUIDs function correctly for store adn loads
        """
        user = self.user
        node1 = node.node(h=user._h)
        node2 = node.node(h=user._h, owner_id=node1.id)
        user._h.commit()
        new_node = JaseciObject.objects.filter(j_owner=node1.id).first()
        new_jsci_node = user._h.get_obj_from_store(new_node.jid)
        self.assertEqual(node2.id, new_node.jid)
        self.assertEqual(node1.id, new_jsci_node.owner_id)

    def test_redis_connection(self):
        """Test redis connection"""
        r = redis.Redis(host=REDIS_HOST, decode_responses=True)
        r.set('test', 'this is a test')
        value = str(r.get('test'))
        self.assertEqual(value, 'this is a test')

    def test_redis_saving(self):
        """Test that redis hooks are set up correctly for saving"""
        tnode = node.node(h=redis_hook())
        tnode.name = "GOBBY"
        tnode.save()  # Jaseci object save

        load_test = tnode._h.get_obj_from_store(tnode.id)
        self.assertEqual(load_test.name, tnode.name)

    def test_redis_loading(self):
        """
        Test that redis hooks are set up correctly for loading single server
        """
        temp_id = node.node(h=redis_hook()).id

        load_test = redis_hook().get_obj(temp_id)

        load_test.kind = "Fasho!"
        load_test.save()  # Jaseci model save

        otnode = redis_hook().get_obj(load_test.id)
        self.assertEqual(load_test.kind, otnode.kind)

    def test_redis_transacting(self):
        """
        Test that db hooks are set up correctly for loading then saving back
        then deleting, also tests that '_id' and '_ids' conventions handle
        uuid types loading from db
        """
        temp_id = node.node(h=redis_hook()).id

        load_test = redis_hook().get_obj(temp_id)

        load_test.kind = "Fasheezzy!"
        load_test.save()  # Jaseci model save

        otnode = redis_hook().get_obj(load_test.id)
        self.assertEqual(load_test.kind, otnode.kind)

        otnode.name = "Rizzoou"
        oedge = otnode.attach_outbound(node.node(h=redis_hook()))
        otnode.save()  # Jaseci object save
        oload_test = redis_hook().get_obj(otnode.id)
        self.assertEqual(oload_test.name, otnode.name)
        # Below tests loading hex uuid strings and converting to uuid type
        newobj = otnode._h.get_obj_from_store(oload_test.id)
        self.assertIn(oedge, newobj.edge_ids.obj_list())

        otnode.destroy()
        self.assertIsNone(
            redis_hook().get_obj(oload_test.id)
        )
