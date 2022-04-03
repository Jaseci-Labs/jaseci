import base64

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from jaseci.utils.utils import TestCaseHelper
from django.test import TestCase

import uuid
import os


class PublicJacApiTests(TestCaseHelper, TestCase):
    """Test the publicly available node API"""

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        get_user_model().objects.create_user(
            'throwawayJSCITfdfdEST_test@jaseci.com',
            'password'
        )
        self.user = get_user_model().objects.create_user(
            'JSCITfdfdEST_test@jaseci.com',
            'password'
        )
        self.auth_client = APIClient()
        self.auth_client.force_authenticate(self.user)
        self.suser = get_user_model().objects.create_superuser(
            'JSCITfdfdEST_test2@jaseci.com',
            'password'
        )
        self.sauth_client = APIClient()
        self.sauth_client.force_authenticate(self.suser)

    def tearDown(self):
        super().tearDown()

    def test_login_required_jac_api(self):
        """Test that login required for retrieving nodes"""
        res = self.client.get(reverse('jac_api:graph_list'))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_public_jac_apis_walker_summon_auth(self):
        """Test public API for summoning walker"""
        zsb_file = open(os.path.dirname(__file__) +
                        "/zsb.jac").read()
        payload = {'op': 'sentinel_register', 'name': 'zsb',
                   'code': zsb_file}
        res = self.auth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'walker_get', 'mode': 'keys',
                   'wlk': 'zsb:walker:pubinit'}
        res = self.auth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        key = res.data['anyone']
        payload = {'op': 'alias_list'}
        res = self.auth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        walk = res.data['zsb:walker:pubinit']
        nd = res.data['active:graph']
        payload = {'op': 'walker_summon', 'key': key, 'wlk': walk, 'nd': nd}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertEqual(len(res.data['report']), 0)
        key = 'aaaaaaa'
        payload = {'op': 'walker_summon', 'key': key, 'wlk': walk, 'nd': nd}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertFalse(res.data['success'])

    def test_serverside_sentinel_global_public_access_summon(self):
        """Test master delete operation"""
        zsb_file = open(os.path.dirname(__file__) +
                        "/zsb.jac").read()
        payload = {'op': 'sentinel_register', 'name': 'zsb',
                   'code': zsb_file}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertEqual(len(res.data), 2)
        payload = {'op': 'global_sentinel_set'}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'sentinel_active_global'}
        res = self.auth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertTrue(res.data['success'])
        payload = {'op': 'graph_create'}
        res = self.auth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'walker_spawn_create', 'name': 'pubinit'}
        res = self.auth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'walker_get', 'mode': 'keys',
                   'wlk': 'spawned:walker:pubinit'}
        res = self.auth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        key = res.data['anyone']
        payload = {'op': 'alias_list'}
        res = self.auth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        walk = res.data['spawned:walker:pubinit']
        nd = res.data['active:graph']
        payload = {'op': 'walker_summon', 'key': key, 'wlk': walk, 'nd': nd}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertEqual(len(res.data['report']), 0)


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
        self.suser = get_user_model().objects.create_superuser(
            'JSCITfdfdEST_test2@jaseci.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.sclient = APIClient()
        self.sclient.force_authenticate(self.suser)
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
            self.master.j_master, uuid.UUID(res.data[0]['jid']))
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
            self.master.j_master, uuid.UUID(res.data[0]['jid']))
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
                   'code': 'walker testwalker{ std.log("hello"); }', }
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        sent = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data[0]['jid']))
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
            self.master.j_master, uuid.UUID(res.data[0]['jid']))
        payload = {'op': 'sentinel_set', 'snt': sent.id.urn,
                   'code': 'node awesome;', 'encoded': False}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertTrue(sent.code_ir.startswith('{"name": "start"'))

    def test_jac_api_sentinel_set_encoded(self):
        """Test API for deleting a sentinel"""
        payload = {'op': 'graph_create'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.master._h.get_obj(self.master.j_master,
                               uuid.UUID(res.data['jid']))
        payload = {'op': 'sentinel_register', 'name': 'Something'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        sent = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data[0]['jid']))
        enc_str = base64.b64encode(b'node awesome;').decode()
        payload = {'op': 'sentinel_set', 'snt': sent.id.urn,
                   'code': enc_str, 'encoded': True}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertTrue(sent.code_ir.startswith('{"name": "start"'))

    def test_jac_api_compile(self):
        """Test API for compiling a sentinel"""
        payload = {'op': 'graph_create'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.master._h.get_obj(self.master.j_master,
                               uuid.UUID(res.data['jid']))
        payload = {'op': 'sentinel_register', 'name': 'Something'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        sent = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data[0]['jid']))
        payload = {'op': 'sentinel_set', 'snt': sent.id.urn,
                   'code': 'walker testwalker{ std.log("hello"); }',
                   'encoded': False}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertTrue(sent.is_active)
        self.assertEqual(sent.walker_ids.obj_list()[0].name, 'testwalker')

    def test_jac_api_load_application(self):
        """Test API for loading an application"""
        enc_str = base64.b64encode(
            b'walker testwalker{ std.log("hello"); }').decode()
        payload = {'op': 'sentinel_register', 'name': 'test_app',
                   'code': enc_str, 'encoded': True}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        snt = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data[0]['jid']))
        gph = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data[1]['jid']))
        self.assertEqual(snt.name, "test_app")
        self.assertEqual(gph.name, "root")
        self.assertTrue(snt.is_active)

    def test_jac_api_load_application_no_leak(self):
        """Test API for loading an application"""
        enc_str = base64.b64encode(
            b'node sample { has apple;} ' +
            b'walker testwalker{ new = spawn here --> node::sample; ' +
            b'report new; }').decode()
        payload = {'op': 'sentinel_register', 'name': 'test_app',
                   'code': enc_str, 'encoded': True}
        num_objs_a = len(self.master._h.mem.keys())
        self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        num_objs_b = len(self.master._h.mem.keys())
        self.client.post(
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
            self.master.j_master, uuid.UUID(res.data[0]['jid']))
        payload = {'op': 'sentinel_set', 'snt': sent.id.urn,
                   'code': 'walker testwalker{ std.log("hello"); }',
                   'encoded': False}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'walker_spawn_create', 'snt': sent.id.urn,
                   'name': 'testwalker'}
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
            self.master.j_master, uuid.UUID(res.data[0]['jid']))
        payload = {'op': 'sentinel_set', 'snt': sent.id.urn,
                   'code': 'walker testwalker{ std.log("hello"); }',
                   'encoded': False}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'walker_spawn_create', 'snt': sent.id.urn,
                   'name': 'testwalker'}
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
            self.master.j_master, uuid.UUID(res.data[0]['jid']))
        payload = {'op': 'sentinel_set', 'snt': sent.id.urn,
                   'code': 'walker testwalker{ std.log("hello"); }',
                   'encoded': False}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'walker_spawn_create', 'snt': sent.id.urn,
                   'name': 'testwalker'}
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

    def test_jac_api_graph_node_set(self):
        """Test API for setting context variables of node"""
        payload = {'op': 'graph_create'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        gph = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        payload = {'op': 'sentinel_register', 'name': 'Something'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        sent = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data[0]['jid']))
        payload = {'op': 'sentinel_set', 'snt': sent.id.urn,
                   'code': 'node sample { has apple;} ' +
                   'walker testwalker{ new = spawn here --> node::sample; ' +
                   'report new; }',
                   'encoded': False}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'walker_spawn_create', 'snt': sent.id.urn,
                   'name': 'testwalker'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        walk = self.master._h.get_obj(
            self.master.j_master, uuid.UUID(res.data['jid']))
        payload = {'op': 'walker_prime', 'wlk': walk.id.urn,
                   'nd': gph.id.urn, 'ctx': {}}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'walker_execute', 'wlk': walk.id.urn}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        nid = res.data['report'][0]['jid']
        payload = {'op': 'graph_node_set', 'snt': sent.id.urn, 'nd': nid,
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
            self.master.j_master, uuid.UUID(res.data[0]['jid']))
        payload = {
            'op': 'sentinel_set', 'snt': sent.id.urn,
            'code': 'walker testwalker{ report '
                    '[[[[[here, here], here], here]]]; }',
            'encoded': False
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'walker_spawn_create', 'snt': sent.id.urn,
                   'name': 'testwalker'}
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
            self.master.j_master, uuid.UUID(res.data[0]['jid']))
        payload = {'op': 'sentinel_set', 'snt': sent.id.urn,
                   'code':
                   'node a { has b; } walker testwalker' +
                   '{ r = spawn here --> node::a; r.b = 6; }',
                   'encoded': False}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'walker_spawn_create', 'snt': sent.id.urn,
                   'name': 'testwalker'}
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
                   'node a { has b, c; } walker testwalker' +
                   '{ with entry {take -->;} ' +
                   'a { here.c=7; std.log(here.c); }}',
                   'encoded': False}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'walker_spawn_create', 'snt': sent.id.urn,
                   'name': 'testwalker'}
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

    def test_master_create_linked_to_django_users(self):
        """Test master create operation"""
        payload = {'op': 'master_create', 'name': 'yo@gmail.com',
                   'other_fields': {'password': 'yoyoyoyoyoyo', 'name': '',
                                    'is_activated': True}}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertIn('j_type', res.data)
        self.assertEqual(res.data['j_type'], 'master')

    def test_master_create_linked_error_out(self):
        """Test master create operation"""
        payload = {'op': 'master_create', 'name': 'yo@gmail.com',
                   'other_fields': {'password': 'yoyoyoyoyoyo', 'name': '',
                                    'is_activated': True}}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'master_create', 'name': 'yo@gmail.com',
                   'other_fields': {'password': 'yoyo', 'name': '',
                                    'is_activated': True}}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertIn('errors', res.data)
        self.assertIn('email', res.data['errors'])
        self.assertIn('password', res.data['errors'])

    def test_master_create_linked_cant_override(self):
        """Test master create operation"""
        payload = {'op': 'master_create', 'name': 'yo2@gmail.com',
                   'other_fields': {'password': 'yoyoyoyoyo', 'name': '',
                                    'is_activated': True, 'is_admin': True,
                                    'is_staff': True, 'is_superuser': True}}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertEqual(res.data['j_type'], 'master')

    def test_master_create_linked_super_limited(self):
        """Test master create operation"""
        payload = {'op': 'master_createsuper', 'name': 'yo3@gmail.com',
                   'other_fields': {'password': 'yoyoyoyoyo', 'name': '',
                                    'is_activated': True, 'is_admin': True,
                                    'is_staff': True, 'is_superuser': True}}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertEqual(res.status_code, 403)

    def test_master_create_linked_super_master_create(self):
        """Test master create operation"""
        payload = {'op': 'master_createsuper', 'name': 'yo3@gmail.com',
                   'other_fields': {'password': 'yoyoyoyoyo', 'name': '',
                                    'is_activated': True, 'is_admin': True,
                                    'is_staff': True, 'is_superuser': True}}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertIn('j_type', res.data)
        self.assertEqual(res.data['j_type'], 'super_master')

    def test_master_create_linked_to_django_users_login(self):
        """Test master create operation"""
        payload = {'op': 'master_create', 'name': 'yo@gmail.com',
                   'other_fields': {'password': 'yoyoyoyoyoyo', 'name': '',
                                    'is_activated': True}}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        login_client = APIClient()
        payload = {'email': 'yo@gmail.com', 'password': 'yoyoyoyoyoyo'}
        res = login_client.post(reverse('user_api:token'), payload)
        self.assertIn('token', res.data)

    def test_master_create_linked_survives_ORM(self):
        """Test master create operation"""
        self.user.get_master()._h.clear_mem_cache()
        payload = {'op': 'master_create', 'name': 'yo@gmail.com',
                   'other_fields': {'password': 'yoyoyoyoyoyo', 'name': '',
                                    'is_activated': True}}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        login_client = APIClient()
        payload = {'email': 'yo@gmail.com', 'password': 'yoyoyoyoyoyo'}
        res = login_client.post(reverse('user_api:token'), payload)
        self.assertIn('token', res.data)

    def test_master_create_super_inherets_from_django(self):
        """Test master create operation"""
        payload = {'op': 'master_create', 'name': 'yo@gmail.com',
                   'other_fields': {'password': 'yoyoyoyoyoyo', 'name': '',
                                    'is_activated': True}}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        login_client = APIClient()
        payload = {'email': 'yo@gmail.com', 'password': 'yoyoyoyoyoyo'}
        res = login_client.post(reverse('user_api:token'), payload)
        self.assertIn('token', res.data)

    def test_master_delete_linked_to_django(self):
        """Test master delete operation"""
        payload = {'op': 'master_create', 'name': 'yo@gmail.com',
                   'other_fields': {'password': 'yoyoyoyoyoyo', 'name': '',
                                    'is_activated': True}}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        login_client = APIClient()
        payload = {'email': 'yo@gmail.com', 'password': 'yoyoyoyoyoyo'}
        res = login_client.post(reverse('user_api:token'), payload)
        self.assertIn('token', res.data)
        payload = {'op': 'master_delete', 'name': 'yo@gmail.com'}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        login_client = APIClient()
        payload = {'email': 'yo@gmail.com', 'password': 'yoyoyoyoyoyo'}
        res = login_client.post(reverse('user_api:token'), payload)
        self.assertNotIn('token', res.data)

    def test_serverside_sentinel_register_global(self):
        """Test master delete operation"""
        zsb_file = open(os.path.dirname(__file__) +
                        "/zsb.jac").read()
        payload = {'op': 'sentinel_register', 'name': 'zsb',
                   'code': zsb_file}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertEqual(len(res.data), 2)
        payload = {'op': 'global_sentinel_set'}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'sentinel_active_global'}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertTrue(res.data['success'])
        payload = {'op': 'sentinel_active_get'}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertIn('jid', res.data)
        payload = {'op': 'graph_list'}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertEqual(len(res.data), 0)
        payload = {'op': 'graph_create'}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'graph_get'}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertEqual(len(res.data), 1)
        payload = {'op': 'walker_run', 'name': 'init'}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'graph_get'}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertEqual(len(res.data), 3)

    def test_serverside_sentinel_unregister_global(self):
        """Test master delete operation"""
        zsb_file = open(os.path.dirname(__file__) +
                        "/zsb.jac").read()
        payload = {'op': 'sentinel_register', 'name': 'zsb',
                   'code': zsb_file}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertEqual(len(res.data), 2)
        payload = {'op': 'global_sentinel_set'}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'sentinel_active_global'}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertTrue(res.data['success'])
        payload = {'op': 'graph_create'}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'walker_run', 'name': 'init'}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'graph_get'}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertEqual(len(res.data), 3)
        payload = {'op': 'graph_create'}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'graph_get'}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertEqual(len(res.data), 1)
        payload = {'op': 'global_sentinel_unset'}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.user._h.clear_mem_cache()
        payload = {'op': 'walker_run', 'name': 'init'}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'graph_get'}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertEqual(len(res.data), 1)

    def test_serverside_sentinel_register_pull(self):
        """Test master delete operation"""
        zsb_file = open(os.path.dirname(__file__) +
                        "/zsb.jac").read()
        payload = {'op': 'sentinel_register', 'name': 'zsb',
                   'code': zsb_file}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertEqual(len(res.data), 2)
        payload = {'op': 'global_sentinel_set'}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'sentinel_pull'}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertTrue(res.data['success'])
        payload = {'op': 'sentinel_active_get'}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertIn('jid', res.data)
        payload = {'op': 'graph_list'}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertEqual(len(res.data), 0)
        payload = {'op': 'graph_create'}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'graph_get'}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertEqual(len(res.data), 1)
        payload = {'op': 'walker_run', 'name': 'init'}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'graph_get'}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertEqual(len(res.data), 3)

    def test_check_json_global_dict(self):
        """Test set get global objects (as json)"""
        from jaseci.tests.jac_test_code import set_get_global_dict
        payload = {'op': 'sentinel_register', 'name': 'zsb',
                   'code': set_get_global_dict}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'walker_run', 'name': 'setter'}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'walker_run', 'name': 'getter'}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertEqual(res.data['report'][0]['max_bot_count'], 10)

    def test_check_sentinel_set(self):
        """Test that sentinel set works serverside"""
        import jaseci.tests.jac_test_code as jtc
        payload = {'op': 'sentinel_register', 'name': 'zsb',
                   'auto_run': '', 'code': jtc.version_label}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'sentinel_set', 'code': jtc.set_get_global_dict}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'walker_run', 'name': 'setter'}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'walker_run', 'name': 'getter'}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertEqual(res.data['report'][0]['max_bot_count'], 10)

    def test_action_loads_remote_config_save(self):
        """Test that sentinel set works serverside"""
        import jaseci.actions.live_actions as lact
        import json
        if (not lact.load_remote_actions('http://js-use-enc')):
            self.skipTest("external resource not available")
        payload = {'op': 'config_delete', 'name': 'ACTION_SETS'}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'actions_load_remote', 'url': 'http://js-use-enc'}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertEqual(res.data, {'success': True})
        payload = {'op': 'config_get', 'name': 'ACTION_SETS'}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.assertEqual(
            res.data,
            json.dumps({"local": [], "remote": ["http://js-use-enc"]}))

    def test_jac_walker_level_api_run(self):
        """Test API for running a walker"""
        payload = {'op': 'graph_create'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        payload = {'op': 'sentinel_register', 'name': 'Something',
                   'code': 'walker testwalker{ std.log("hello"); }', }
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload,
                               format='json')

        payload = {}
        res = self.client.post(
            reverse('jac_api:walker_list'), payload)
        self.assertEqual(len(res.data), 1)
        res = self.client.post(
            reverse('jac_api:wapi', args=['testwalker']), payload)
        self.assertTrue(res.data['success'])

    def test_jac_report_status_pluck(self):
        """Test API for running a walker"""
        payload = {'op': 'graph_create'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        payload = {'op': 'sentinel_register', 'name': 'Something',
                   'code': 'walker ss {report.status = 302; report 4;}', }
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload,
                               format='json')

        payload = {}
        res = self.client.post(
            reverse('jac_api:walker_list'), payload)
        self.assertEqual(len(res.data), 1)
        res = self.client.post(
            reverse('jac_api:wapi', args=['ss']), payload)
        self.assertEqual(res.status_code, 302)
        self.assertTrue(res.data['success'])
