import base64

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from jaseci.utils.utils import TestCaseHelper
from django.test import TestCase

import uuid


class PublicJacApiTests(TestCaseHelper, TestCase):
    """Test the publicly available node API"""

    def setUp(self):
        super().setUp()
        self.client = APIClient()

    def tearDown(self):
        super().tearDown()

    def test_login_required_jac_api(self):
        """Test that login required for retrieving nodes"""
        res = self.client.get(reverse('jac_api:graph_list'))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateJacApiTests(TestCaseHelper, TestCase):
    """Test the authorized user node API"""

    def setUp(self):
        super().setUp()
        get_user_model().objects.create_user(
            'throwawayJSCITfdfdEST_test@jaseci.com',
            'password'
        )
        self.user = get_user_model().objects.create_user(
            'JSCITfdfdEST_test@jaseci.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.master = self.user.get_master()

    def tearDown(self):
        super().tearDown()

    def test_jac_api_create_graph(self):
        """Test API for creating a graph"""
        payload = {'op': 'graph_create'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        gph = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        self.assertEqual(gph.name, "root")

    def test_jac_api_create_sentinel(self):
        """Test API for creating a sentinel"""
        payload = {'op': 'graph_create'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.master._h.get_obj(self.master.j_master,
                               uuid.UUID(res.data['jid']))
        payload = {'op': 'sentinel_register', 'name': 'Untitled Sentinel'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        sent = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(sent.name, "Untitled Sentinel")

    def test_jac_api_list_graphs_sents(self):
        """Test API for creating a sentinel"""
        payload = {'op': 'graph_create'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        payload = {'op': 'graph_list'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        glist = res.data
        payload = {'op': 'sentinel_register', 'name': 'SomeSent'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        payload = {'op': 'sentinel_register', 'name': 'SomeSent2'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        payload = {'op': 'sentinel_list'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        slist = res.data
        self.assertEqual(len(glist), 1)
        self.assertEqual(len(slist), 2)
        self.assertEqual(slist[1]['name'], 'SomeSent2')
        self.assertEqual(glist[0]['name'], 'root')

    def test_jac_api_delete_graph(self):
        """Test API for deleteing a graph"""
        payload = {'op': 'graph_create'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        gph = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        payload = {'op': 'sentinel_register', 'name': 'Something'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.assertIn(gph.id, gph._h.mem.keys())
        payload = {'op': 'graph_delete', 'gph': gph.id.urn}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.assertNotIn(gph.id, gph._h.mem.keys())

    def test_jac_api_get_graph_dot(self):
        """Test API for getting graph in dot str"""
        payload = {'op': 'graph_create'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        gph = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        payload = {'op': 'graph_get', 'mode': 'dot',
                   'gph': gph.id.urn, 'dot': True}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.assertTrue('graph root' in res.json())

    def test_jac_api_delete_sentinel(self):
        """Test API for deleting a sentinel"""
        payload = {'op': 'graph_create'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        gph = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        payload = {'op': 'sentinel_register', 'name': 'Something'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        sent = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        self.assertIn(gph.id, gph._h.mem.keys())
        self.assertIn(sent.id, gph._h.mem.keys())
        payload = {'op': 'sentinel_delete', 'snt': sent.id.urn}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.assertIn(gph.id, gph._h.mem.keys())
        self.assertNotIn(sent.id, gph._h.mem.keys())

    def test_jac_api_get_jac_code(self):
        """Test API for deleting a sentinel"""
        payload = {'op': 'graph_create'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.master._h.get_obj(self.master.j_master,
                               uuid.UUID(res.data['jid']))
        payload = {'op': 'sentinel_register', 'name': 'Something',
                   'code': 'walker test { std.log("hello"); }', }
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        sent = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        payload = {'op': 'sentinel_get', 'mode': 'code', 'snt': sent.id.urn}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.assertIn('walker test', res.data)

    def test_jac_api_sentinel_set(self):
        """Test API for deleting a sentinel"""
        payload = {'op': 'graph_create'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.master._h.get_obj(self.master.j_master,
                               uuid.UUID(res.data['jid']))
        payload = {'op': 'sentinel_register', 'name': 'Something'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        sent = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        payload = {'op': 'sentinel_set', 'snt': sent.id.urn,
                   'code': '# Something awesome!!', 'encoded': False}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertEqual(sent.code, '# Something awesome!!')

    def test_jac_api_sentinel_set_encoded(self):
        """Test API for deleting a sentinel"""
        payload = {'op': 'graph_create'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.master._h.get_obj(self.master.j_master,
                               uuid.UUID(res.data['jid']))
        payload = {'op': 'sentinel_register', 'name': 'Something'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        sent = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        enc_str = base64.b64encode(b'# Something awesome!!').decode()
        payload = {'op': 'sentinel_set', 'snt': sent.id.urn,
                   'code': enc_str, 'encoded': True}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertEqual(sent.code, '# Something awesome!!')

    def test_jac_api_compile(self):
        """Test API for compiling a sentinel"""
        payload = {'op': 'graph_create'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.master._h.get_obj(self.master.j_master,
                               uuid.UUID(res.data['jid']))
        payload = {'op': 'sentinel_register', 'name': 'Something'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        sent = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        payload = {'op': 'sentinel_set', 'snt': sent.id.urn,
                   'code': 'walker test { std.log("hello"); }',
                   'encoded': False}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertTrue(sent.is_active)
        self.assertEqual(sent.walker_ids.obj_list()[0].name, 'test')

    def test_jac_api_load_application(self):
        """Test API for loading an application"""
        enc_str = base64.b64encode(
            b'walker test { std.log("hello"); }').decode()
        payload = {'op': 'sentinel_register', 'name': 'test_app',
                   'code': enc_str, 'encoded': True}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        snt = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['sentinel']))
        gph = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['graph']))
        self.assertEqual(snt.name, "test_app")
        self.assertEqual(gph.name, "root")
        self.assertTrue(snt.is_active)

    def test_jac_api_load_application_no_leak(self):
        """Test API for loading an application"""
        enc_str = base64.b64encode(
            b'node sample { has apple;} ' +
            b'walker test { new = spawn here --> node::sample; ' +
            b'report new; }').decode()
        payload = {'op': 'sentinel_register', 'name': 'test_app',
                   'code': enc_str, 'encoded': True}
        num_objs_a = len(self.master._h.mem.keys())
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        num_objs_b = len(self.master._h.mem.keys())
        # snt = self.master._h.get_obj(
        #     self.master.j_master, uuid.UUID(res.data['sentinel']))
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        num_objs_c = len(self.master._h.mem.keys())
        self.assertLess(num_objs_a, num_objs_b)
        self.assertEqual(num_objs_b, num_objs_c)

    def test_jac_api_spawn(self):
        """Test API for spawning a walker"""
        payload = {'op': 'graph_create'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.master._h.get_obj(self.master.j_master,
                               uuid.UUID(res.data['jid']))
        payload = {'op': 'sentinel_register', 'name': 'Something'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        sent = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        payload = {'op': 'sentinel_set', 'snt': sent.id.urn,
                   'code': 'walker test { std.log("hello"); }',
                   'encoded': False}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'walker_spawn', 'snt': sent.id.urn,
                   'name': 'test'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        walk = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        self.assertNotEqual(walk.id, sent.walker_ids.obj_list()[0].id)
        self.assertEqual(walk.name, sent.walker_ids.obj_list()[0].name)

    def test_jac_api_prime(self):
        """Test API for priming a walker"""
        payload = {'op': 'graph_create'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        gph = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        payload = {'op': 'sentinel_register', 'name': 'Something'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        sent = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        payload = {'op': 'sentinel_set', 'snt': sent.id.urn,
                   'code': 'walker test { std.log("hello"); }',
                   'encoded': False}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'walker_spawn', 'snt': sent.id.urn,
                   'name': 'test'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        walk = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        payload = {'op': 'walker_prime', 'wlk': walk.id.urn,
                   'nd': gph.id.urn, 'ctx': {}}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')

        self.assertIn(gph, walk.next_node_ids.obj_list())

    def test_jac_api_run(self):
        """Test API for running a walker"""
        payload = {'op': 'graph_create'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        gph = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        payload = {'op': 'sentinel_register', 'name': 'Something'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        sent = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        payload = {'op': 'sentinel_set', 'snt': sent.id.urn,
                   'code': 'walker test { std.log("hello"); }',
                   'encoded': False}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'walker_spawn', 'snt': sent.id.urn,
                   'name': 'test'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        walk = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        payload = {'op': 'walker_prime', 'wlk': walk.id.urn,
                   'nd': gph.id.urn, 'ctx': {}}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'walker_execute', 'wlk': walk.id.urn}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.assertGreater(walk.current_step, 0)

    def test_jac_api_set_node_context(self):
        """Test API for setting context variables of node"""
        payload = {'op': 'graph_create'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        gph = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        payload = {'op': 'sentinel_register', 'name': 'Something'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        sent = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        payload = {'op': 'sentinel_set', 'snt': sent.id.urn,
                   'code': 'node sample { has apple;} ' +
                   'walker test { new = spawn here --> node::sample; ' +
                   'report new; }',
                   'encoded': False}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'walker_spawn', 'snt': sent.id.urn,
                   'name': 'test'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        walk = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        payload = {'op': 'walker_prime', 'wlk': walk.id.urn,
                   'nd': gph.id.urn, 'ctx': {}}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'walker_execute', 'wlk': walk.id.urn}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        nid = res.data[0]['jid']
        payload = {'op': 'set_node_context', 'snt': sent.id.urn, 'nd': nid,
                   'ctx': {'apple': 'TEST'}}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertGreater(walk.current_step, 0)
        self.assertEqual(res.data['context']['apple'], 'TEST')

    def test_deep_serialize_report(self):
        """Test API for running a walker"""
        payload = {'op': 'graph_create'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        gph = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        payload = {'op': 'sentinel_register', 'name': 'Something'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        sent = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        payload = {
            'op': 'sentinel_set', 'snt': sent.id.urn,
            'code': 'walker test { report [[[[[here, here], here], here]]]; }',
            'encoded': False
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'walker_spawn', 'snt': sent.id.urn,
                   'name': 'test'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        walk = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        payload = {'op': 'walker_prime', 'wlk': walk.id.urn,
                   'nd': gph.id.urn, 'ctx': {}}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'walker_execute', 'wlk': walk.id.urn}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.assertGreater(walk.current_step, 0)

    def test_create_new_fields_auto_on_old_data(self):
        """Test API for running a walker"""
        payload = {'op': 'graph_create'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        gph = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        payload = {'op': 'sentinel_register', 'name': 'Something'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        sent = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        payload = {'op': 'sentinel_set', 'snt': sent.id.urn,
                   'code':
                   'node a { has b; } walker test ' +
                   '{ r = spawn here --> node::a; r.b = 6; }',
                   'encoded': False}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'walker_spawn', 'snt': sent.id.urn,
                   'name': 'test'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        walk = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        payload = {'op': 'walker_prime', 'wlk': walk.id.urn,
                   'nd': gph.id.urn, 'ctx': {}}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'walker_execute', 'wlk': walk.id.urn}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.assertGreater(walk.current_step, 0)

        payload = {'op': 'sentinel_set', 'snt': sent.id.urn,
                   'code':
                   'node a { has b, c; } walker test ' +
                   '{ with entry {take -->;} ' +
                   'a { here.c=7; std.log(here.c); }}',
                   'encoded': False}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'walker_spawn', 'snt': sent.id.urn,
                   'name': 'test'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        walk = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        payload = {'op': 'walker_prime', 'wlk': walk.id.urn,
                   'nd': gph.id.urn, 'ctx': {}}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'walker_execute', 'wlk': walk.id.urn}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.assertEqual(gph.outbound_nodes()[0].context['c'], 7)
