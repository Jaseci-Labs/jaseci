from django.contrib.auth import get_user_model

from jaseci.utils.utils import TestCaseHelper
from jaseci.utils.id_list import IdList
from django.test import TestCase

from jaseci.jsorc.jsorc import JsOrc
from jaseci_serv.base.models import JaseciObject
from jaseci.prim import node
from jaseci.prim import edge
from jaseci.prim.graph import Graph
from jaseci.prim.sentinel import Sentinel
import jaseci.tests.jac_test_code as jtc
from jaseci.utils.test_core import skip_without_redis
import uuid

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
        tnode = node.Node(m_id=0, h=user._h)
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

        otnode = user._h.get_obj(load_test.j_master.urn, load_test.jid.urn)
        self.assertEqual(load_test.kind, otnode.kind)

    def test_jsci_db_to_engine_hook_on_authenticated_transacting(self):
        """
        Test that db hooks are set up correctly for loading then saving back
        then deleting, also tests that '_id' and '_ids' conventions handle
        uuid types loading from db
        """
        user = self.user
        self.assertIsNotNone(user._h)
        temp_id = node.Node(m_id=0, h=user._h).id

        h = user._h
        h.commit()
        del h.mem[temp_id.urn]
        if h.redis.is_running():
            h.redis.delete(temp_id.urn)

        load_test = JaseciObject.objects.filter(jid=temp_id).first()

        load_test.kind = "Fasheezzy!"
        load_test.save()  # Jaseci model save

        otnode = user._h.get_obj(load_test.j_master.urn, load_test.jid.urn)
        self.assertEqual(load_test.kind, otnode.kind)

        otnode.name = "Rizzoou"
        oedge = otnode.attach_outbound(node.Node(m_id=otnode._m_id, h=otnode._h))
        otnode.save()  # Jaseci object save
        user._h.commit()
        oload_test = JaseciObject.objects.get(jid=otnode.id)
        self.assertEqual(oload_test.name, otnode.name)
        # Below tests loading hex uuid strings and converting to uuid type
        newobj = otnode._h.get_obj_from_store(oload_test.jid.urn)
        self.assertIn(oedge[0], newobj.smart_edges)

        otnode.destroy()
        self.assertFalse(
            JaseciObject.objects.filter(jid=oload_test.jid.urn).exists(), False
        )

    def test_jsci_walker_writes_through_graph_updates(self):
        """
        Test that db hooks handle walkers ok
        """
        user = self.user
        gph = Graph(m_id=0, h=user._h)
        sent = Sentinel(m_id=0, h=gph._h)
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
        node1 = node.Node(m_id=0, h=user._h)
        node2 = node.Node(m_id=0, h=user._h, parent=node1)
        user._h.commit()
        new_node = JaseciObject.objects.filter(j_parent=node1.id).first()
        new_jsci_node = user._h.get_obj_from_store(new_node.jid.urn)
        self.assertEqual(node2.id, new_node.jid)
        self.assertEqual(node1.id, new_jsci_node.parent().id)

    @skip_without_redis
    def test_redis_connection(self):
        """Test redis connection"""

        redis = JsOrc.svc("redis")
        self.assertTrue(redis.is_running())

        redis = JsOrc.hook().redis
        self.assertTrue(redis.is_running())

        redis.set("test", "this is a test")
        self.assertEqual(redis.get("test"), "this is a test")

    def test_redis_saving(self):
        """Test that redis hooks are set up correctly for saving"""
        tnode = node.Node(m_id=0, h=self.user._h)
        tnode.name = "GOBBY"
        tnode.save()  # Jaseci object save
        tnode._h.commit()
        load_test = tnode._h.get_obj_from_store(tnode.id.urn)
        self.assertEqual(load_test.name, tnode.name)

    def test_redis_loading(self):
        """
        Test that redis hooks are set up correctly for loading single server
        """
        nd = node.Node(m_id=0, h=self.user._h)
        temp_id = nd.id
        nd._h.commit()
        load_test = nd._h.get_obj(uuid.UUID(int=0).urn, temp_id.urn)

        load_test.kind = "Fasho!"
        load_test.save()
        load_test._h.commit()
        otnode = load_test._h.get_obj(load_test._m_id, load_test.id.urn)
        self.assertEqual(load_test.kind, otnode.kind)

    def test_redis_transacting(self):
        """
        Test that db hooks are set up correctly for loading then saving back
        then deleting, also tests that '_id' and '_ids' conventions handle
        uuid types loading from db
        """
        nd = node.Node(m_id=0, h=self.user._h)
        temp_id = nd.id
        nd._h.commit()

        load_test = nd._h.get_obj(uuid.UUID(int=0).urn, temp_id.urn)

        load_test.kind = "Fasheezzy!"
        load_test.save()  # Jaseci model save
        load_test._h.commit()

        otnode = nd._h.get_obj(load_test._m_id, load_test.id.urn)
        self.assertEqual(load_test.kind, otnode.kind)

        otnode.name = "Rizzoou"
        oedge = otnode.attach_outbound(node.Node(m_id=0, h=self.user._h))
        otnode.save()  # Jaseci object save
        otnode._h.commit()
        oload_test = otnode._h.get_obj(uuid.UUID(int=0).urn, otnode.id.urn)
        self.assertEqual(oload_test.name, otnode.name)
        # Below tests loading hex uuid strings and converting to uuid type
        newobj = otnode._h.get_obj_from_store(oload_test.id.urn)
        self.assertIn(oedge[0], newobj.smart_edges)

        otnode.destroy()
        self.assertIsNone(newobj._h.get_obj(oload_test._m_id, oload_test.id.urn))

    def test_fast_edges(self):
        user = self.user
        gph = Graph(m_id=0, h=user._h)
        sent = Sentinel(m_id=0, h=gph._h)
        sent.register_code(jtc.prog1)
        test_node = sent.arch_ids.get_obj_by_name("life", kind="node").run()
        test_walker = sent.run_architype("get_gen_day")
        test_walker.prime(test_node)
        test_walker.context["date"] = "2010-08-03T03:00:00.000000"
        user._h.commit()
        before = JaseciObject.objects.filter(kind="edge").count()
        test_walker.run()
        user._h.commit()
        after = JaseciObject.objects.filter(kind="edge").count()
        self.assertEqual(before, 1)
        self.assertEqual(after, 1)
        test_walker.run()
        user._h.commit()
        after = JaseciObject.objects.filter(kind="edge").count()
        self.assertEqual(after, 1)

    def test_fast_edges_reloads(self):
        user = self.user
        gph = Graph(m_id=0, h=user._h)
        sent = Sentinel(m_id=0, h=gph._h)
        sent.register_code(jtc.prog1)
        test_node = sent.arch_ids.get_obj_by_name("life", kind="node").run()
        test_walker = sent.run_architype("get_gen_day")
        test_walker.prime(test_node)
        test_walker.context["date"] = "2010-08-03T03:00:00.000000"
        user._h.commit()
        user._h.clear_cache()
        before = JaseciObject.objects.filter(kind="edge").count()
        test_walker.run()
        user._h.commit()
        user._h.clear_cache()
        after = JaseciObject.objects.filter(kind="edge").count()
        self.assertEqual(before, 1)
        self.assertEqual(after, 1)
        test_walker.run()
        user._h.commit()
        user._h.clear_cache()
        after = JaseciObject.objects.filter(kind="edge").count()
        self.assertEqual(after, 1)

    def test_fast_edges_detach(self):
        user = self.user
        snode = node.Node(m_id=0, h=user._h)
        tnode = node.Node(m_id=0, h=user._h)
        cedge = edge.Edge(m_id=0, h=user._h)
        cedge.connect(snode, tnode)
        user._h.commit()
        user._h.clear_cache()
        snode = user._h.get_obj(0, snode.jid)
        tnode = user._h.get_obj(0, tnode.jid)
        self.assertEqual(len(snode.outbound_edges()), 1)
        self.assertEqual(len(tnode.inbound_edges()), 1)
        snode.detach(tnode)
        self.assertEqual(len(snode.outbound_edges()), 0)
        self.assertEqual(len(tnode.inbound_edges()), 0)
        self.assertEqual(len(snode.smart_edges), 0)
        self.assertEqual(len(tnode.smart_edges), 0)

    def test_fast_edges_node_edge_no_dupe(self):
        user = self.user
        e_chk = lambda x: self.assertEqual(
            user._h.get_object_distribution()[edge.Edge], x
        )
        snode = node.Node(m_id=0, h=user._h)
        tnode = node.Node(m_id=0, h=user._h)
        cedge = edge.Edge(m_id=0, h=user._h)
        e_chk(1)
        cedge.connect(snode, tnode)
        e_chk(1)
        user._h.commit()
        user._h.clear_cache()
        snode = user._h.get_obj(0, snode.jid)
        tnode = user._h.get_obj(0, tnode.jid)
        self.assertEqual(len(snode.outbound_edges()), 1)
        e_chk(1)
        self.assertEqual(len(tnode.inbound_edges()), 1)
        e_chk(1)
        snode.destroy()
        self.assertFalse(edge.Edge in user._h.get_object_distribution())

    def test_fast_edges_node_edge_match(self):
        user = self.user
        snode = node.Node(m_id=0, h=user._h)
        tnode = node.Node(m_id=0, h=user._h)
        cedge = edge.Edge(m_id=0, h=user._h)
        cedge.connect(snode, tnode)
        before_jid = cedge.jid
        user._h.commit()
        user._h.clear_cache()
        snode = user._h.get_obj(0, snode.jid)
        tnode = user._h.get_obj(0, tnode.jid)
        self.assertEqual(snode.outbound_edges()[0].jid, tnode.inbound_edges()[0].jid)
        self.assertEqual(snode.outbound_edges()[0].jid, before_jid)

    def test_fast_edges_with_context(self):
        user = self.user
        snode = node.Node(m_id=0, h=user._h)
        tnode = node.Node(m_id=0, h=user._h)
        cedge = edge.Edge(m_id=0, h=user._h)
        cedge.context["a"] = "b"
        cedge.connect(snode, tnode)
        user._h.commit()
        user._h.clear_cache()
        snode = user._h.get_obj(0, snode.jid)
        tnode = user._h.get_obj(0, tnode.jid)
        cedge = snode.outbound_edges()[0]
        self.assertIn("a", cedge.context.keys())
        self.assertEqual(cedge.context["a"], "b")

    def test_node_saves_on_traversing_graphs(self):
        user = self.user
        hook = user._h = JsOrc.hook()
        gph = Graph(m_id=0, h=hook)
        sent = Sentinel(m_id=0, h=gph._h)
        sent.register_code(jtc.simple_graph)
        test_walker = sent.run_architype("sample")
        test_walker.prime(gph)
        test_walker.run()

        self.assertSetEqual(
            set(
                [
                    "basic::sentinel",
                    "root::graph",
                    "a1::node",
                    "a2::node",
                    "a3::node",
                    "b1::node",
                    "b2::node",
                    "root::architype",
                    "a1::architype",
                    "a2::architype",
                    "a3::architype",
                    "b1::architype",
                    "b2::architype",
                    "e1::architype",
                    "e2::architype",
                    "e3::architype",
                    "generic::architype",
                    "sample::architype",
                    "sample2::architype",
                    "sample3::architype",
                    "generic::architype",
                ]
            ),
            set([item.name + "::" + item.j_type for item in hook.save_obj_list]),
        )

        hook.commit()
        hook.clear_cache()

        test_walker = sent.run_architype("sample")
        test_walker.prime(gph)
        test_walker.run()

        self.assertFalse(hook.save_obj_list)

        test_walker = sent.run_architype("sample2")
        test_walker.prime(gph)
        test_walker.run()

        self.assertSetEqual(
            set(["b2::node", "a3::node"]),
            set([item.name + "::" + item.j_type for item in hook.save_obj_list]),
        )

        hook.commit()
        hook.clear_cache()

        test_walker = sent.run_architype("sample3")
        test_walker.prime(gph)
        test_walker.run()

        self.assertSetEqual(
            set(["a1::node", "a2::node", "a3::node"]),
            set([item.name + "::" + item.j_type for item in hook.save_obj_list]),
        )

        hook.commit()
        hook.clear_cache()

        test_walker = sent.run_architype("sample3")
        test_walker.prime(gph)
        test_walker.run()

        # no a3::node since it was already disconnected
        self.assertSetEqual(
            set(["a1::node", "a2::node"]),
            set([item.name + "::" + item.j_type for item in hook.save_obj_list]),
        )

    def test_node_saves_on_fast_edges(self):
        user = self.user
        hook = user._h = JsOrc.hook()
        gph = Graph(m_id=0, h=hook)
        sent = Sentinel(m_id=0, h=gph._h)
        sent.register_code(jtc.simple_graph2)
        test_walker = sent.run_architype("sample")
        test_walker.prime(gph)
        a1 = test_walker.run()["report"][0]["jid"]

        # initial trigger
        self.assertSetEqual(
            set(
                [
                    "basic::sentinel",
                    "root::graph",
                    "a1::node",
                    "root::architype",
                    "a1::architype",
                    "e1::architype",
                    "generic::architype",
                    "sample::architype",
                    "sample2::architype",
                    "sample3::architype",
                    "sample4::architype",
                    "sample5::architype",
                    "sample6::architype",
                    "generic::architype",
                ]
            ),
            set([item.name + "::" + item.j_type for item in hook.save_obj_list]),
        )

        hook.commit()
        hook.clear_cache()

        # trigger change value from node::a1
        a1 = hook.get_obj(0, a1)
        test_walker = sent.run_architype("sample2")
        test_walker.prime(a1)
        reps = test_walker.run()["report"]

        self.assertEqual([4, 4], reps)
        self.assertSetEqual(
            set(["a1::node", "root::graph"]),
            set([item.name + "::" + item.j_type for item in hook.save_obj_list]),
        )

        hook.commit()
        hook.clear_cache()

        # trigger report value from graph::root
        test_walker = sent.run_architype("sample3")
        test_walker.prime(gph)
        reps = test_walker.run()["report"]

        self.assertEqual([4, 4], reps)
        self.assertFalse(hook.save_obj_list)

        # trigger change value from graph::root
        test_walker = sent.run_architype("sample4")
        test_walker.prime(gph)
        reps = test_walker.run()["report"]

        self.assertEqual([6, 6], reps)
        self.assertSetEqual(
            set(["a1::node", "root::graph"]),
            set([item.name + "::" + item.j_type for item in hook.save_obj_list]),
        )

        hook.commit()
        hook.clear_cache()

        # trigger report value from node::a1
        test_walker = sent.run_architype("sample5")
        test_walker.prime(a1)
        reps = test_walker.run()["report"]

        self.assertEqual([6, 6], reps)
        self.assertFalse(hook.save_obj_list)

        # trigger change value from graph::root without accessing node::a1
        test_walker = sent.run_architype("sample6")
        test_walker.prime(gph)
        test_walker.run()

        self.assertSetEqual(
            set(["a1::node", "root::graph"]),
            set([item.name + "::" + item.j_type for item in hook.save_obj_list]),
        )

        hook.commit()
        hook.clear_cache()

        # read node::a1 without accessing graph::root
        test_walker = sent.run_architype("sample6")
        test_walker.prime(a1)
        reps = test_walker.run()["report"]

        self.assertEqual([8], reps)
        self.assertFalse(hook.save_obj_list)
