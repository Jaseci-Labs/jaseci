import base64
import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from jaseci_serv.utils.test_utils import skip_without_redis

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
            "throwawayJSCITfdfdEST_test@jaseci.com", "password"
        )
        self.user = get_user_model().objects.create_user(
            "JSCITfdfdEST_test@jaseci.com", "password"
        )
        self.auth_client = APIClient()
        self.auth_client.force_authenticate(self.user)
        self.suser = get_user_model().objects.create_superuser(
            "JSCITfdfdEST_test2@jaseci.com", "password"
        )
        self.sauth_client = APIClient()
        self.sauth_client.force_authenticate(self.suser)

    def tearDown(self):
        super().tearDown()

    def test_login_required_jac_api(self):
        """Test that login required for retrieving nodes"""
        res = self.client.get(reverse("jac_api:graph_list"))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_public_jac_apis_walker_summon_auth(self):
        """Test public API for summoning walker"""
        zsb_file = open(os.path.dirname(__file__) + "/zsb.jac").read()
        payload = {"op": "sentinel_register", "name": "zsb", "code": zsb_file}
        res = self.auth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "walker_spawn_create", "name": "pubinit"}
        res = self.auth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        wjid = res.data["jid"]
        payload = {"op": "walker_get", "mode": "keys", "wlk": wjid}
        res = self.auth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        key = res.data["anyone"]
        payload = {"op": "alias_list"}
        res = self.auth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        nd = res.data["active:graph"]
        payload = {"op": "walker_summon", "key": key, "wlk": wjid, "nd": nd}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(len(res.data["report"]), 0)
        key = "aaaaaaa"
        payload = {"op": "walker_summon", "key": key, "wlk": wjid, "nd": nd}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertFalse(res.data["success"])

    def test_serverside_sentinel_global_public_access_summon(self):
        """Test master delete operation"""
        zsb_file = open(os.path.dirname(__file__) + "/zsb.jac").read()
        payload = {"op": "sentinel_register", "name": "zsb", "code": zsb_file}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(len(res.data), 2)
        payload = {"op": "global_sentinel_set"}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "sentinel_active_global"}
        res = self.auth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertTrue(res.data["success"])
        payload = {"op": "graph_create"}
        res = self.auth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "walker_spawn_create", "name": "pubinit"}
        res = self.auth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "walker_get", "mode": "keys", "wlk": "spawned:walker:pubinit"}
        res = self.auth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        key = res.data["anyone"]
        payload = {"op": "alias_list"}
        res = self.auth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        walk = res.data["spawned:walker:pubinit"]
        nd = res.data["active:graph"]
        payload = {"op": "walker_summon", "key": key, "wlk": walk, "nd": nd}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(len(res.data["report"]), 0)

    def test_serverside_sentinel_global_public_access_callback(self):
        """Test public API for walker callback"""
        zsb_file = open(os.path.dirname(__file__) + "/public.jac").read()
        payload = {"op": "sentinel_register", "name": "public", "code": zsb_file}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(len(res.data), 2)
        payload = {"op": "global_sentinel_set"}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "sentinel_active_global"}
        res = self.auth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertTrue(res.data["success"])
        payload = {"op": "graph_create"}
        res = self.auth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "walker_spawn_create", "name": "callback"}
        res = self.auth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "walker_get", "mode": "keys", "wlk": "spawned:walker:callback"}
        res = self.auth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        key = res.data["anyone"]
        payload = {"op": "alias_list"}
        res = self.auth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        walk = res.data["spawned:walker:callback"].split(":")[2]
        nd = res.data["active:graph"].split(":")[2]
        payload = {"op": "walker_callback", "key": key, "wlk": walk, "nd": nd}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}', args=[payload["nd"], payload["wlk"]])
            + "?keys="
            + key,
            payload,
            format="json",
        )
        self.assertEqual(res.data["updated"], False)
        self.assertEqual(res.status_code, 200)
        zsb_file = open(os.path.dirname(__file__) + "/public_updated.jac").read()
        payload = {"op": "sentinel_register", "name": "public", "code": zsb_file}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(len(res.data), 1)
        payload = {"op": "walker_callback", "key": key, "wlk": walk, "nd": nd}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}', args=[payload["nd"], payload["wlk"]])
            + "?keys="
            + key,
            payload,
            format="json",
        )
        self.assertEqual(res.data["updated"], True)
        self.assertEqual(res.status_code, 201)

    @skip_without_redis
    def test_serverside_sentinel_global_public_access_callback_async(self):
        """Test public API for walker callback"""
        zsb_file = open(os.path.dirname(__file__) + "/public.jac").read()
        payload = {"op": "sentinel_register", "name": "public", "code": zsb_file}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(len(res.data), 2)
        payload = {"op": "global_sentinel_set"}
        res = self.sauth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "sentinel_active_global"}
        res = self.auth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertTrue(res.data["success"])
        payload = {"op": "graph_create"}
        res = self.auth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "walker_spawn_create", "name": "callback"}
        res = self.auth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "walker_get", "mode": "keys", "wlk": "spawned:walker:callback"}
        res = self.auth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        key = res.data["anyone"]
        payload = {"op": "alias_list"}
        res = self.auth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        walk = res.data["spawned:walker:callback"].split(":")[2]
        nd = res.data["active:graph"].split(":")[2]
        payload = {
            "is_async": True,
            "op": "walker_callback",
            "key": key,
            "wlk": walk,
            "nd": nd,
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}', args=[payload["nd"], payload["wlk"]])
            + "?keys="
            + key,
            payload,
            format="json",
        )

        self.assertFalse("updated" in res.data)
        self.assertTrue(res.data["is_queued"])

        task_id = res.data["result"]

        res = self.auth_client.get(
            reverse("jac_api:walker_queue_check") + f"?task_id={task_id}"
        )

        self.assertEqual("SUCCESS", res.data["status"])
        self.assertIsNone(res.data["result"]["anchor"])
        self.assertTrue(res.data["result"]["response"]["success"])


class PrivateJacApiTests(TestCaseHelper, TestCase):
    """Test the authorized user node API"""

    def setUp(self):
        super().setUp()
        get_user_model().objects.create_user(
            "throwawayJSCITfdfdEST_test@jaseci.com", "password"
        )
        self.user = get_user_model().objects.create_user(
            "JSCITfdfdEST_test@jaseci.com", "password"
        )
        self.suser = get_user_model().objects.create_superuser(
            "JSCITfdfdEST_test2@jaseci.com", "password"
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
        payload = {"op": "graph_create"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        gph = self.master._h.get_obj(self.master.j_master, res.data["jid"])
        self.assertEqual(gph.name, "root")

    def test_jac_api_create_sentinel(self):
        """Test API for creating a sentinel"""
        payload = {"op": "graph_create"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.master._h.get_obj(self.master.j_master, res.data["jid"])
        payload = {"op": "sentinel_register", "name": "Untitled Sentinel"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        sent = self.master._h.get_obj(self.master.j_master, res.data[0]["jid"])
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(sent.name, "Untitled Sentinel")

    def test_jac_api_list_graphs_sents(self):
        """Test API for creating a sentinel"""
        payload = {"op": "graph_create"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        payload = {"op": "graph_list"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        glist = res.data
        payload = {"op": "sentinel_register", "name": "SomeSent"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        payload = {"op": "sentinel_register", "name": "SomeSent2"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        payload = {"op": "sentinel_list"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        slist = res.data
        self.assertEqual(len(glist), 1)
        self.assertEqual(len(slist), 2)
        self.assertEqual(slist[1]["name"], "SomeSent2")
        self.assertEqual(glist[0]["name"], "root")

    def test_jac_api_delete_graph(self):
        """Test API for deleteing a graph"""
        payload = {"op": "graph_create"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        gph = self.master._h.get_obj(self.master.j_master, res.data["jid"])
        payload = {"op": "sentinel_register", "name": "Something"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.assertIn(gph.jid, gph._h.mem.keys())
        payload = {"op": "graph_delete", "gph": gph.jid}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.assertNotIn(gph.jid, gph._h.mem.keys())

    def test_jac_api_get_graph_dot(self):
        """Test API for getting graph in dot str"""
        payload = {"op": "graph_create"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)

        gph = self.master._h.get_obj(self.master.j_master, res.data["jid"])
        payload = {"op": "graph_get", "mode": "dot", "nd": gph.jid, "dot": True}

        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.assertTrue("graph root" in res.json())

    def test_jac_api_delete_sentinel(self):
        """Test API for deleting a sentinel"""
        payload = {"op": "graph_create"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        gph = self.master._h.get_obj(self.master.j_master, res.data["jid"])
        payload = {"op": "sentinel_register", "name": "Something"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        sent = self.master._h.get_obj(self.master.j_master, res.data[0]["jid"])
        self.assertIn(gph.jid, gph._h.mem.keys())
        self.assertIn(sent.jid, gph._h.mem.keys())
        payload = {"op": "sentinel_delete", "snt": sent.jid}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.assertIn(gph.jid, gph._h.mem.keys())
        self.assertNotIn(sent.jid, gph._h.mem.keys())

    def test_jac_api_get_jac_code(self):
        """Test API for deleting a sentinel"""
        payload = {"op": "graph_create"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.master._h.get_obj(self.master.j_master, res.data["jid"])
        payload = {
            "op": "sentinel_register",
            "name": "Something",
            "code": 'walker testwalker{ std.log("hello"); }',
        }
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        sent = self.master._h.get_obj(self.master.j_master, res.data[0]["jid"])
        payload = {"op": "sentinel_get", "mode": "code", "snt": sent.jid}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.assertIn("walker test", res.data)

    def test_jac_api_sentinel_set(self):
        """Test API for deleting a sentinel"""
        payload = {"op": "graph_create"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.master._h.get_obj(self.master.j_master, res.data["jid"])
        payload = {"op": "sentinel_register", "name": "Something"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        sent = self.master._h.get_obj(self.master.j_master, res.data[0]["jid"])
        payload = {
            "op": "sentinel_set",
            "snt": sent.jid,
            "code": "node awesome;",
            "encoded": False,
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertIn('{"name": "start"', sent.code_ir)

    def test_jac_api_sentinel_set_encoded(self):
        """Test API for deleting a sentinel"""
        payload = {"op": "graph_create"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.master._h.get_obj(self.master.j_master, res.data["jid"])
        payload = {"op": "sentinel_register", "name": "Something"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        sent = self.master._h.get_obj(self.master.j_master, res.data[0]["jid"])
        enc_str = base64.b64encode(b"node awesome;").decode()
        payload = {
            "op": "sentinel_set",
            "snt": sent.jid,
            "code": enc_str,
            "encoded": True,
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertIn('{"name": "start"', sent.code_ir)

    def test_jac_api_compile(self):
        """Test API for compiling a sentinel"""
        payload = {"op": "graph_create"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.master._h.get_obj(self.master.j_master, res.data["jid"])
        payload = {"op": "sentinel_register", "name": "Something"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        sent = self.master._h.get_obj(self.master.j_master, res.data[0]["jid"])
        payload = {
            "op": "sentinel_set",
            "snt": sent.jid,
            "code": 'walker testwalker{ std.log("hello"); }',
            "encoded": False,
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertTrue(sent.is_active)
        self.assertEqual(sent.arch_ids.obj_list()[3].name, "testwalker")

    def test_jac_api_load_application(self):
        """Test API for loading an application"""
        enc_str = base64.b64encode(b'walker testwalker{ std.log("hello"); }').decode()
        payload = {
            "op": "sentinel_register",
            "name": "test_app",
            "code": enc_str,
            "encoded": True,
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        snt = self.master._h.get_obj(self.master.j_master, res.data[0]["jid"])
        gph = self.master._h.get_obj(self.master.j_master, res.data[1]["jid"])
        self.assertEqual(snt.name, "test_app")
        self.assertEqual(gph.name, "root")
        self.assertTrue(snt.is_active)

    def test_jac_api_load_application_no_leak(self):
        """Test API for loading an application"""
        enc_str = base64.b64encode(
            b"node sample { has apple;} "
            + b"walker testwalker{ new = spawn here ++> node::sample; "
            + b"report new; }"
        ).decode()
        payload = {
            "op": "sentinel_register",
            "name": "test_app",
            "code": enc_str,
            "encoded": True,
        }
        num_objs_a = len(self.master._h.mem.keys())
        self.client.post(reverse(f'jac_api:{payload["op"]}'), payload, format="json")
        num_objs_b = len(self.master._h.mem.keys())
        self.client.post(reverse(f'jac_api:{payload["op"]}'), payload, format="json")
        self.client.post(reverse(f'jac_api:{payload["op"]}'), payload, format="json")
        self.client.post(reverse(f'jac_api:{payload["op"]}'), payload, format="json")
        self.client.post(reverse(f'jac_api:{payload["op"]}'), payload, format="json")
        self.client.post(reverse(f'jac_api:{payload["op"]}'), payload, format="json")
        num_objs_c = len(self.master._h.mem.keys())
        self.assertLess(num_objs_a, num_objs_b)
        self.assertEqual(num_objs_b, num_objs_c)

    def test_jac_api_spawn(self):
        """Test API for spawning a walker"""
        payload = {"op": "graph_create"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.master._h.get_obj(self.master.j_master, res.data["jid"])
        payload = {"op": "sentinel_register", "name": "Something"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        sent = self.master._h.get_obj(self.master.j_master, res.data[0]["jid"])
        payload = {
            "op": "sentinel_set",
            "snt": sent.jid,
            "code": 'walker testwalker{ std.log("hello"); }',
            "encoded": False,
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {
            "op": "walker_spawn_create",
            "snt": sent.jid,
            "name": "testwalker",
        }
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        walk = self.master._h.get_obj(self.master.j_master, res.data["jid"])
        self.assertNotEqual(walk.id, sent.arch_ids.obj_list()[3].id)
        self.assertEqual(walk.name, sent.arch_ids.obj_list()[3].name)

    def test_jac_api_prime(self):
        """Test API for priming a walker"""
        payload = {"op": "graph_create"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        gph = self.master._h.get_obj(self.master.j_master, res.data["jid"])
        payload = {"op": "sentinel_register", "name": "Something"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        sent = self.master._h.get_obj(self.master.j_master, res.data[0]["jid"])
        payload = {
            "op": "sentinel_set",
            "snt": sent.jid,
            "code": 'walker testwalker{ std.log("hello"); }',
            "encoded": False,
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {
            "op": "walker_spawn_create",
            "snt": sent.jid,
            "name": "testwalker",
        }
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        walk = self.master._h.get_obj(self.master.j_master, res.data["jid"])
        payload = {
            "op": "walker_prime",
            "wlk": walk.jid,
            "nd": gph.jid,
            "ctx": {},
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        self.assertIn(gph, walk.next_node_ids.obj_list())

    def test_jac_api_run(self):
        """Test API for running a walker"""
        payload = {"op": "graph_create"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        gph = self.master._h.get_obj(self.master.j_master, res.data["jid"])
        payload = {"op": "sentinel_register", "name": "Something"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        sent = self.master._h.get_obj(self.master.j_master, res.data[0]["jid"])
        payload = {
            "op": "sentinel_set",
            "snt": sent.jid,
            "code": 'walker testwalker{ std.log("hello"); }',
            "encoded": False,
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {
            "op": "walker_spawn_create",
            "snt": sent.jid,
            "name": "testwalker",
        }
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        walk = self.master._h.get_obj(self.master.j_master, res.data["jid"])
        payload = {
            "op": "walker_prime",
            "wlk": walk.jid,
            "nd": gph.jid,
            "ctx": {},
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "walker_execute", "wlk": walk.jid}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.assertGreater(walk.current_step, 0)

    def test_jac_api_graph_node_set(self):
        """Test API for setting context variables of node"""
        payload = {"op": "graph_create"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        gph = self.master._h.get_obj(self.master.j_master, res.data["jid"])
        payload = {"op": "sentinel_register", "name": "Something"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        sent = self.master._h.get_obj(self.master.j_master, res.data[0]["jid"])
        payload = {
            "op": "sentinel_set",
            "snt": sent.jid,
            "code": "node sample { has apple;} "
            + "walker testwalker{ new = spawn here ++> node::sample; "
            + "report new; }",
            "encoded": False,
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {
            "op": "walker_spawn_create",
            "snt": sent.jid,
            "name": "testwalker",
        }
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        walk = self.master._h.get_obj(self.master.j_master, res.data["jid"])
        payload = {
            "op": "walker_prime",
            "wlk": walk.jid,
            "nd": gph.jid,
            "ctx": {},
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "walker_execute", "wlk": walk.jid}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        nid = res.data["report"][0]["jid"]
        payload = {
            "op": "graph_node_set",
            "snt": sent.jid,
            "nd": nid,
            "ctx": {"apple": "TEST"},
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertGreater(walk.current_step, 0)
        self.assertEqual(res.data["context"]["apple"], "TEST")

    def test_deep_serialize_report(self):
        """Test API for running a walker"""
        payload = {"op": "graph_create"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        gph = self.master._h.get_obj(self.master.j_master, res.data["jid"])
        payload = {"op": "sentinel_register", "name": "Something"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        sent = self.master._h.get_obj(self.master.j_master, res.data[0]["jid"])
        payload = {
            "op": "sentinel_set",
            "snt": sent.jid,
            "code": "walker testwalker{ report " "[[[[[here, here], here], here]]]; }",
            "encoded": False,
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {
            "op": "walker_spawn_create",
            "snt": sent.jid,
            "name": "testwalker",
        }
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        walk = self.master._h.get_obj(self.master.j_master, res.data["jid"])
        payload = {
            "op": "walker_prime",
            "wlk": walk.jid,
            "nd": gph.jid,
            "ctx": {},
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "walker_execute", "wlk": walk.jid}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.assertGreater(walk.current_step, 0)

    def test_create_new_fields_auto_on_old_data(self):
        """Test API for running a walker"""
        payload = {"op": "graph_create"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        gph = self.master._h.get_obj(self.master.j_master, res.data["jid"])
        payload = {"op": "sentinel_register", "name": "Something"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        sent = self.master._h.get_obj(self.master.j_master, res.data[0]["jid"])
        payload = {
            "op": "sentinel_set",
            "snt": sent.jid,
            "code": "node a { has b; } walker testwalker"
            + "{ r = spawn here ++> node::a; r.b = 6; }",
            "encoded": False,
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {
            "op": "walker_spawn_create",
            "snt": sent.jid,
            "name": "testwalker",
        }
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        walk = self.master._h.get_obj(self.master.j_master, res.data["jid"])
        payload = {
            "op": "walker_prime",
            "wlk": walk.jid,
            "nd": gph.jid,
            "ctx": {},
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "walker_execute", "wlk": walk.jid}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.assertGreater(walk.current_step, 0)

        payload = {
            "op": "sentinel_set",
            "snt": sent.jid,
            "code": "node a { has b, c; } walker testwalker"
            + "{ with entry {take -->;} "
            + "a { here.c=7; std.log(here.c); }}",
            "encoded": False,
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {
            "op": "walker_spawn_create",
            "snt": sent.jid,
            "name": "testwalker",
        }
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        walk = self.master._h.get_obj(self.master.j_master, res.data["jid"])
        payload = {
            "op": "walker_prime",
            "wlk": walk.jid,
            "nd": gph.jid,
            "ctx": {},
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "walker_execute", "wlk": walk.jid}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.assertEqual(gph.outbound_nodes()[0].context["c"], 7)

    def test_master_create_linked_to_django_users(self):
        """Test master create operation"""
        payload = {
            "op": "master_create",
            "name": "yo@gmail.com",
            "other_fields": {
                "password": "yoyoyoyoyoyo",
                "name": "",
                "is_activated": True,
            },
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertIn("j_type", res.data["user"])
        self.assertEqual(res.data["user"]["j_type"], "master")

    def test_master_create_linked_error_out(self):
        """Test master create operation"""
        payload = {
            "op": "master_create",
            "name": "yo@gmail.com",
            "other_fields": {
                "password": "yoyoyoyoyoyo",
                "name": "",
                "is_activated": True,
            },
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {
            "op": "master_create",
            "name": "yo@gmail.com",
            "other_fields": {"password": "yoyo", "name": "", "is_activated": True},
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertFalse(res.data["success"])
        self.assertIn("already exists", res.data["response"])

    def test_master_create_linked_cant_override(self):
        """Test master create operation"""
        payload = {
            "op": "master_create",
            "name": "yo2@gmail.com",
            "other_fields": {
                "password": "yoyoyoyoyo",
                "name": "",
                "is_activated": True,
                "is_admin": True,
                "is_staff": True,
                "is_superuser": True,
            },
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(res.data["user"]["j_type"], "master")

    def test_master_create_linked_super_limited(self):
        """Test master create operation"""
        payload = {
            "op": "master_createsuper",
            "name": "yo3@gmail.com",
            "other_fields": {
                "password": "yoyoyoyoyo",
                "name": "",
                "is_activated": True,
                "is_admin": True,
                "is_staff": True,
                "is_superuser": True,
            },
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(res.status_code, 403)

    def test_master_create_linked_super_master_create(self):
        """Test master create operation"""
        payload = {
            "op": "master_createsuper",
            "name": "yo3@gmail.com",
            "other_fields": {
                "password": "yoyoyoyoyo",
                "name": "",
                "is_activated": True,
                "is_admin": True,
                "is_staff": True,
                "is_superuser": True,
            },
        }
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertIn("j_type", res.data["user"])
        self.assertEqual(res.data["user"]["j_type"], "super_master")

    def test_master_create_linked_to_django_users_login(self):
        """Test master create operation"""
        payload = {
            "op": "master_create",
            "name": "yo@gmail.com",
            "other_fields": {
                "password": "yoyoyoyoyoyo",
                "name": "",
                "is_activated": True,
            },
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        login_client = APIClient()
        payload = {"email": "yo@gmail.com", "password": "yoyoyoyoyoyo"}
        res = login_client.post(reverse("user_api:token"), payload)
        self.assertIn("token", res.data)

    def test_master_create_linked_survives_orm(self):
        """Test master create operation"""
        self.user.get_master()._h.clear_cache()
        payload = {
            "op": "master_create",
            "name": "yo@gmail.com",
            "other_fields": {
                "password": "yoyoyoyoyoyo",
                "name": "",
                "is_activated": True,
            },
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        login_client = APIClient()
        payload = {"email": "yo@gmail.com", "password": "yoyoyoyoyoyo"}
        res = login_client.post(reverse("user_api:token"), payload)
        self.assertIn("token", res.data)

    def test_master_create_super_inherets_from_django(self):
        """Test master create operation"""
        payload = {
            "op": "master_create",
            "name": "yo@gmail.com",
            "other_fields": {
                "password": "yoyoyoyoyoyo",
                "name": "",
                "is_activated": True,
            },
        }
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        login_client = APIClient()
        payload = {"email": "yo@gmail.com", "password": "yoyoyoyoyoyo"}
        res = login_client.post(reverse("user_api:token"), payload)
        self.assertIn("token", res.data)

    def test_master_delete_linked_to_django(self):
        """Test master delete operation"""
        payload = {
            "op": "master_create",
            "name": "yo@gmail.com",
            "other_fields": {
                "password": "yoyoyoyoyoyo",
                "name": "",
                "is_activated": True,
            },
        }
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        login_client = APIClient()
        payload = {"email": "yo@gmail.com", "password": "yoyoyoyoyoyo"}
        res = login_client.post(reverse("user_api:token"), payload)
        self.assertIn("token", res.data)
        payload = {"op": "master_delete", "name": "yo@gmail.com"}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        login_client = APIClient()
        payload = {"email": "yo@gmail.com", "password": "yoyoyoyoyoyo"}
        res = login_client.post(reverse("user_api:token"), payload)
        self.assertNotIn("token", res.data)

    def test_serverside_sentinel_register_global(self):
        """Test master delete operation"""
        zsb_file = open(os.path.dirname(__file__) + "/zsb.jac").read()
        payload = {"op": "sentinel_register", "name": "zsb", "code": zsb_file}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(len(res.data), 2)
        payload = {"op": "global_sentinel_set"}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "sentinel_active_global"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertTrue(res.data["success"])
        payload = {"op": "sentinel_active_get"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertIn("jid", res.data)
        payload = {"op": "graph_list"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(len(res.data), 0)
        payload = {"op": "graph_create"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "graph_get"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(len(res.data), 1)
        payload = {"op": "walker_run", "name": "init"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "graph_get"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(len(res.data), 3)

    def test_sentinel_active_global_with_auto_run(self):
        zsb_file = open(os.path.dirname(__file__) + "/zsb.jac").read()
        payload = {"op": "sentinel_register", "name": "zsb", "code": zsb_file}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(len(res.data), 2)
        payload = {"op": "global_sentinel_set"}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "graph_create", "set_active": True}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "sentinel_active_get"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertFalse(res.data["success"])
        payload = {"op": "sentinel_active_global", "auto_run": "init"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertTrue(res.data["success"])
        self.assertIn("auto_run_result", res.data)
        payload = {"op": "graph_get"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(len(res.data), 3)

    def test_public_user_create_global_init(self):
        public_client = APIClient()
        zsb_file = open(os.path.dirname(__file__) + "/zsb.jac").read()
        payload = {"op": "sentinel_register", "name": "zsb", "code": zsb_file}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(len(res.data), 2)
        payload = {"op": "global_sentinel_set"}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {
            "op": "user_create",
            "name": "yo@gmail.com",
            "global_init": "init",
            "other_fields": {
                "password": "yoyoyoyoyoyo",
                "name": "",
                "is_activated": True,
            },
        }
        res = public_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(res.data["success"], True)
        self.assertEqual(res.data["global_init"]["auto_run_result"]["success"], True)

    def test_public_user_create_save_through(self):
        public_client = APIClient()
        zsb_file = open(os.path.dirname(__file__) + "/zsb.jac").read()
        payload = {"op": "sentinel_register", "name": "zsb", "code": zsb_file}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(len(res.data), 2)
        payload = {"op": "global_sentinel_set"}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {
            "op": "user_create",
            "name": "yo2@gmail.com",
            "global_init": "init",
            "other_fields": {
                "password": "yoyoyoyoyoyo",
                "name": "",
                "is_activated": True,
            },
        }
        res = public_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        usr = get_user_model().objects.get(email="yo2@gmail.com")
        self.assertIsNotNone(usr.get_master().active_gph_id)

    def test_master_create_global_init(self):
        zsb_file = open(os.path.dirname(__file__) + "/zsb.jac").read()
        payload = {"op": "sentinel_register", "name": "zsb", "code": zsb_file}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(len(res.data), 2)
        payload = {"op": "global_sentinel_set"}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {
            "op": "master_create",
            "name": "yo@gmail.com",
            "global_init": "init",
            "other_fields": {
                "password": "yoyoyoyoyoyo",
                "name": "",
                "is_activated": True,
            },
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(res.data["success"], True)
        self.assertEqual(res.data["global_init"]["auto_run_result"]["success"], True)
        payload = {"op": "master_active_set", "name": "yo@gmail.com"}
        self.client.post(reverse(f'jac_api:{payload["op"]}'), payload, format="json")
        payload = {"op": "graph_get"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(len(res.data), 3)

    def test_serverside_sentinel_unregister_global(self):
        """Test master delete operation"""
        zsb_file = open(os.path.dirname(__file__) + "/zsb.jac").read()
        payload = {"op": "sentinel_register", "name": "zsb", "code": zsb_file}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(len(res.data), 2)
        payload = {"op": "global_sentinel_set"}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "sentinel_active_global"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertTrue(res.data["success"])
        payload = {"op": "graph_create"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "walker_run", "name": "init"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "graph_get"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(len(res.data), 3)
        payload = {"op": "graph_create"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "graph_get"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(len(res.data), 1)
        payload = {"op": "global_sentinel_unset"}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.user._h.clear_cache()
        payload = {"op": "walker_run", "name": "init"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "graph_get"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(len(res.data), 1)

    def test_serverside_sentinel_register_pull(self):
        """Test master delete operation"""
        zsb_file = open(os.path.dirname(__file__) + "/zsb.jac").read()
        payload = {"op": "sentinel_register", "name": "zsb", "code": zsb_file}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(len(res.data), 2)
        payload = {"op": "global_sentinel_set"}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "sentinel_pull"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertTrue(res.data["success"])
        payload = {"op": "sentinel_active_get"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertIn("jid", res.data)
        payload = {"op": "graph_list"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(len(res.data), 0)
        payload = {"op": "graph_create"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "graph_get"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(len(res.data), 1)
        payload = {"op": "walker_run", "name": "init"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "graph_get"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(len(res.data), 3)

    def test_check_json_global_dict(self):
        """Test set get global objects (as json)"""
        from jaseci.tests.jac_test_code import set_get_global_dict

        payload = {
            "op": "sentinel_register",
            "name": "zsb",
            "code": set_get_global_dict,
        }
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "walker_run", "name": "setter"}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "walker_run", "name": "getter"}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(res.data["report"][0]["max_bot_count"], 10)

    def test_check_sentinel_set(self):
        """Test that sentinel set works serverside"""
        import jaseci.tests.jac_test_code as jtc

        payload = {
            "op": "sentinel_register",
            "name": "zsb",
            "auto_run": "",
            "code": jtc.version_label,
        }
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "sentinel_set", "code": jtc.set_get_global_dict}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "walker_run", "name": "setter"}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "walker_run", "name": "getter"}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(res.data["report"][0]["max_bot_count"], 10)

    def test_jac_walker_level_api_run(self):
        """Test API for running a walker"""
        payload = {"op": "graph_create"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        payload = {
            "op": "sentinel_register",
            "name": "Something",
            "code": 'walker testwalker{ std.log("hello"); }',
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        payload = {}
        res = self.client.post(reverse("jac_api:walker_list"), payload)
        self.assertEqual(len(res.data), 1)
        res = self.client.post(reverse("jac_api:wapi", args=["testwalker"]), payload)
        self.assertTrue(res.data["success"])

    def test_jac_report_status_pluck(self):
        """Test API for running a walker"""
        payload = {"op": "graph_create"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        payload = {
            "op": "sentinel_register",
            "name": "Something",
            "code": "walker ss {report:status = 302; report 4;}",
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        payload = {}
        res = self.client.post(reverse("jac_api:walker_list"), payload)
        self.assertEqual(len(res.data), 1)
        res = self.client.post(reverse("jac_api:wapi", args=["ss"]), payload)
        self.assertEqual(res.status_code, 302)
        self.assertTrue(res.data["success"])

    def test_jac_admin_master_allusers(self):
        """Test API for creating a graph"""
        payload = {}
        res = self.sclient.post(
            reverse("jac_api:master_allusers"), payload, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_jac_admin_master_allusers_search(self):
        """Test API for searching users"""
        public_client = APIClient()
        payload = {
            "op": "user_create",
            "name": "john.doe@gmail.com",
            "global_init": "init",
            "other_fields": {
                "password": "yoyoyoyoyoyo",
                "name": "John Doe",
                "is_activated": True,
            },
        }

        public_client.post(reverse(f'jac_api:{payload["op"]}'), payload, format="json")

        res = self.sclient.post(reverse("jac_api:master_allusers"), {}, format="json")
        res_obj = json.loads(res.content)

        search_res = self.sclient.post(
            reverse("jac_api:master_allusers"), {"search": "john.doe"}, format="json"
        )
        search_res_obj = json.loads(search_res.content)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(search_res.status_code, status.HTTP_200_OK)
        self.assertEqual(res_obj["total"], 4)
        self.assertEqual(search_res_obj["total"], 1)
        self.assertEqual(search_res_obj["data"][0]["user"], payload["name"])

    def test_asim_bug_check(self):
        """Test public API for summoning walker"""
        zsb_file = open(os.path.dirname(__file__) + "/zsb.jac").read()
        payload = {"op": "sentinel_register", "name": "zsb", "code": zsb_file}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "walker_run", "name": "asim_bug_check1"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        ret1 = res.data
        self.user.get_master()._h.clear_cache()
        payload = {"op": "walker_run", "name": "asim_bug_check2"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        ret2 = res.data
        self.assertEqual(ret1, ret2)

    def test_asim_bug_check2(self):
        """Test public API for summoning walker"""
        zsb_file = open(os.path.dirname(__file__) + "/zsb.jac").read()
        payload = {"op": "sentinel_register", "name": "zsb", "code": zsb_file}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "walker_run", "name": "asim_bug_check3"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        ret1 = res.data
        self.user.get_master()._h.clear_cache()
        payload = {"op": "walker_run", "name": "asim_bug_check2"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        ret2 = res.data
        self.assertEqual(ret1, ret2)

    def test_asim_bug_check3(self):
        """Test public API for summoning walker"""
        zsb_file = open(os.path.dirname(__file__) + "/zsb.jac").read()
        payload = {"op": "sentinel_register", "name": "zsb", "code": zsb_file}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "walker_run", "name": "asim_bug_check4"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        ret1 = res.data
        self.user.get_master()._h.clear_cache()
        payload = {"op": "walker_run", "name": "asim_bug_check2"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        ret2 = res.data
        self.assertEqual(ret1, ret2)

    def test_serverside_superuser_become(self):
        payload = {"op": "master_active_get"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        user_id = res.data["jid"]
        payload = {"op": "graph_create"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        user_gph_id = res.data["jid"]
        payload = {"op": "master_active_get"}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        super_id = res.data["jid"]
        self.assertNotEqual(user_id, super_id)
        payload = {"op": "graph_list"}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(len(res.data), 0)
        payload = {"op": "master_become", "mast": user_id}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "master_active_get"}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(user_id, res.data["jid"])
        payload = {"op": "graph_list"}
        res = self.sclient.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(user_gph_id, res.data[0]["jid"])

    def test_jac_report_custom(self):
        """Test API for running a walker"""
        payload = {"op": "graph_create"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        payload = {
            "op": "sentinel_register",
            "name": "Something",
            "code": "walker testwalker{ report:status = 302; "
            "report:custom = {'a': 'b'}; }",
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        payload = {}
        res = self.client.post(reverse("jac_api:walker_list"), payload)
        self.assertEqual(len(res.data), 1)
        res = self.client.post(reverse("jac_api:wapi", args=["testwalker"]), payload)
        self.assertEqual(res.data, {"a": "b"})
        self.assertEqual(res.status_code, status.HTTP_302_FOUND)

    def test_jac_create_user_in_jac_django(self):
        """Test API for running a walker"""
        payload = {"op": "graph_create"}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        payload = {
            "op": "sentinel_register",
            "name": "Something",
            "code": "walker testwalker{ report jaseci.master_create('a@b.com', '' ,'',  {},"
            "{'password': 'yoyoyoyoyoyo', 'name': '', 'is_activated': true}); }",
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        payload = {}
        res = self.client.post(reverse("jac_api:walker_list"), payload)
        self.assertEqual(len(res.data), 1)
        res = self.client.post(reverse("jac_api:wapi", args=["testwalker"]), payload)
        self.assertIn("jid", res.data["report"][0]["user"].keys())
        self.assertEqual(res.data["report"][0]["user"]["name"], "a@b.com")

    def test_global_ref(self):
        """Test global action triggers"""
        zsb_file = open(os.path.dirname(__file__) + "/zsb.jac").read()
        payload = {"op": "sentinel_register", "name": "zsb", "code": zsb_file}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "walker_run", "name": "global_actions"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        ).data

        self.assertFalse(res["success"])
        self.assertEqual(payload, res["report"][4]["body"])

    def test_multipart_json_file(self):
        """Test multipart using json file as ctx parameter"""
        zsb_file = open(os.path.dirname(__file__) + "/zsb.jac").read()
        payload = {"op": "sentinel_register", "name": "zsb", "code": zsb_file}
        self.client.post(reverse(f'jac_api:{payload["op"]}'), payload, format="json")
        with open(os.path.dirname(__file__) + "/test.json", "rb") as ctx:
            form = {
                "name": "simple",
                "ctx": ctx,
                "nd": "active:graph",
                "snt": "active:sentinel",
            }
            res = self.client.post(reverse(f'jac_api:{"walker_run"}'), data=form).data

        self.assertTrue(res["success"])
        self.assertEqual({"sample": "sample"}, res["report"][0]["ctx"])

    @skip_without_redis
    def test_multipart_json_file_async(self):
        """Test multipart using json file as ctx parameter"""
        zsb_file = open(os.path.dirname(__file__) + "/zsb.jac").read()
        payload = {"op": "sentinel_register", "name": "zsb", "code": zsb_file}
        self.client.post(reverse(f'jac_api:{payload["op"]}'), payload, format="json")
        with open(os.path.dirname(__file__) + "/test.json", "rb") as ctx:
            form = {
                "name": "simple",
                "ctx": ctx,
                "nd": "active:graph",
                "snt": "active:sentinel",
            }
            res = self.client.post(
                reverse(f'jac_api:{"walker_run"}') + "?is_async=true", data=form
            ).data

        self.assertTrue(res["is_queued"])
        task_id = res["result"]

        res = self.client.get(
            reverse("jac_api:walker_queue_wait") + f"?task_id={task_id}"
        ).data

        self.assertEqual("SUCCESS", res["status"])
        self.assertEqual("test", res["result"]["anchor"])
        self.assertEqual(
            {"sample": "sample"}, res["result"]["response"]["report"][0]["ctx"]
        )

        res = self.client.get(
            reverse("jac_api:walker_queue_check") + f"?task_id={task_id}"
        ).data

        self.assertEqual("SUCCESS", res["status"])
        self.assertEqual("test", res["result"]["anchor"])
        self.assertEqual(
            {"sample": "sample"}, res["result"]["response"]["report"][0]["ctx"]
        )

    @skip_without_redis
    def test_multipart_json_file_async_via_syntax(self):
        """Test multipart using json file as ctx parameter"""
        zsb_file = open(os.path.dirname(__file__) + "/zsb.jac").read()
        payload = {"op": "sentinel_register", "name": "zsb", "code": zsb_file}
        self.client.post(reverse(f'jac_api:{payload["op"]}'), payload, format="json")
        with open(os.path.dirname(__file__) + "/test.json", "rb") as ctx:
            form = {
                "name": "simple_async",
                "ctx": ctx,
                "nd": "active:graph",
                "snt": "active:sentinel",
            }
            res = self.client.post(reverse(f'jac_api:{"walker_run"}'), data=form).data

        self.assertTrue(res["is_queued"])
        task_id = res["result"]

        res = self.client.get(
            reverse(f"jac_api:walker_queue_check") + f"?task_id={task_id}"
        ).data

        self.assertEqual("SUCCESS", res["status"])
        self.assertEqual("test", res["result"]["anchor"])
        self.assertEqual(1, res["result"]["response"]["report"][0])
        self.assertEqual(2, res["result"]["response"]["report"][1])
        self.assertEqual(
            {"sample": "sample"}, res["result"]["response"]["report"][2]["ctx"]
        )
        self.assertEqual(1, res["result"]["response"]["report"][3])
        self.assertEqual(
            {"sample": "sample"}, res["result"]["response"]["report"][4]["ctx"]
        )
        self.assertTrue(res["result"]["response"]["report"][5]["is_queued"])

        res = self.client.get(
            reverse(f"jac_api:walker_queue_check")
            + f'?task_id={res["result"]["response"]["report"][5]["result"]}'
        ).data

        self.assertEqual(1, res["result"]["anchor"])
        self.assertEqual(1, res["result"]["response"]["report"][0])
        self.assertEqual(2, res["result"]["response"]["report"][1])
        self.assertEqual(
            {"sample": "sample"}, res["result"]["response"]["report"][2]["ctx"]
        )

    def test_multipart_json_string(self):
        """Test multipart using json string as ctx parameter"""
        zsb_file = open(os.path.dirname(__file__) + "/zsb.jac").read()
        payload = {"op": "sentinel_register", "name": "zsb", "code": zsb_file}
        self.client.post(reverse(f'jac_api:{payload["op"]}'), payload, format="json")

        form = {
            "name": "simple",
            "ctx": '{"sample":"sample"}',
            "nd": "active:graph",
            "snt": "active:sentinel",
        }

        res = self.client.post(reverse(f'jac_api:{"walker_run"}'), data=form).data

        self.assertTrue(res["success"])
        self.assertEqual({"sample": "sample"}, res["report"][0]["ctx"])

    def test_multipart_with_additional_file(self):
        """Test multipart with additional file"""
        zsb_file = open(os.path.dirname(__file__) + "/zsb.jac").read()
        payload = {"op": "sentinel_register", "name": "zsb", "code": zsb_file}
        self.client.post(reverse(f'jac_api:{payload["op"]}'), payload, format="json")
        with open(os.path.dirname(__file__) + "/test.json", "rb") as ctx, open(
            os.path.dirname(__file__) + "/test.json", "rb"
        ) as ctx2:
            form = {
                "name": "simple_with_file",
                "ctx": ctx,
                "nd": "active:graph",
                "snt": "active:sentinel",
                "fileTypeField": ctx2,
            }
            res = self.client.post(reverse(f'jac_api:{"walker_run"}'), data=form).data

        default_file = [
            {
                "name": "test.json",
                "base64": "eyJzYW1wbGUiOiJzYW1wbGUifQ==",
                "content-type": "application/json",
            }
        ]

        self.assertTrue(res["success"])
        self.assertEqual(default_file, res["report"][0])
        self.assertEqual(default_file, res["report"][1])

    def test_multipart_custom_payload_with_additional_file(self):
        """Test multipart custom payload (non ctx format) with additional file"""
        zsb_file = open(os.path.dirname(__file__) + "/zsb.jac").read()
        payload = {"op": "sentinel_register", "name": "zsb", "code": zsb_file}
        self.client.post(reverse(f'jac_api:{payload["op"]}'), payload, format="json")
        with open(os.path.dirname(__file__) + "/test.json", "rb") as ctx:
            form = {
                "name": "simple_custom_payload_with_file",
                "ctx": "",
                "nd": "active:graph",
                "snt": "active:sentinel",
                "fileTypeField": ctx,
            }
            res = self.client.post(reverse(f'jac_api:{"walker_run"}'), data=form).data

        default_file = [
            {
                "name": "test.json",
                "base64": "eyJzYW1wbGUiOiJzYW1wbGUifQ==",
                "content-type": "application/json",
            }
        ]

        self.assertTrue(res["success"])
        self.assertEqual(default_file, res["report"][2])

    def test_try_catch(self):
        """Test try catch triggers"""
        zsb_file = open(os.path.dirname(__file__) + "/try-syntax.jac").read()
        payload = {"op": "sentinel_register", "name": "zsb", "code": zsb_file}
        self.client.post(reverse(f'jac_api:{payload["op"]}'), payload, format="json")

        payload = {"op": "walker_run", "name": "walker_exception_no_try_else"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        ).data

        self.assertIn("in jac_try_exception", " ".join(res["stack_trace"]))
        self.assertIn(
            "raise TryException(self.jac_exception(e, jac_ast))",
            " ".join(res["stack_trace"]),
        )
        self.assertIn(
            "jaseci.jac.machine.machine_state.TryException: ",
            " ".join(res["stack_trace"]),
        )
        self.assertIn(
            "zsb:walker_exception_no_try_else - line 6, col 20",
            res["errors"][0],
        )

        payload = {"op": "walker_run", "name": "walker_exception_with_try_else"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        ).data

        self.assertFalse("stack_trace" in res)
        self.assertEqual("walker_exception_with_try_else", res["report"][0]["name"])
        self.assertEqual(14, res["report"][0]["line"])
        self.assertEqual(23, res["report"][0]["col"])
        self.assertIn(
            "zsb:walker_exception_with_try_else -"
            " line 14, col 23 - rule atom_trailer - ",
            res["errors"][0],
        )

        payload = {
            "op": "walker_run",
            "name": "walker_exception_with_try_else_multiple_line",
        }

        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        ).data

        self.assertFalse("stack_trace" in res)
        self.assertEqual(
            "walker_exception_with_try_else_multiple_line", res["report"][0]["name"]
        )
        self.assertEqual(32, res["report"][0]["line"])
        self.assertEqual(23, res["report"][0]["col"])
        self.assertIn(
            "zsb:walker_exception_with_try_else_multiple_line "
            "- line 32, col 23 - rule atom_trailer - ",
            res["errors"][0],
        )

    def quick_call(self, bywho, ops):
        return bywho.post(reverse(f'jac_api:{ops["op"]}'), ops, format="json")

    def test_walker_smart_yield(self):
        testfile = open(os.path.dirname(__file__) + "/various.jac").read()
        self.quick_call(
            self.client, {"op": "sentinel_register", "name": "test", "code": testfile}
        )
        ret = self.quick_call(self.client, {"op": "walker_run", "name": "smart_yield"})
        ret = self.quick_call(self.client, {"op": "walker_run", "name": "smart_yield"})
        ret = self.quick_call(self.client, {"op": "walker_run", "name": "smart_yield"})
        ret = self.quick_call(self.client, {"op": "walker_run", "name": "smart_yield"})
        self.assertEqual(ret.data["report"], [{"id": 2}])

    def test_walker_smart_yield_no_future(self):
        testfile = open(os.path.dirname(__file__) + "/various.jac").read()
        self.quick_call(
            self.client, {"op": "sentinel_register", "name": "test", "code": testfile}
        )
        ret = self.quick_call(
            self.client, {"op": "walker_run", "name": "smart_yield_no_future"}
        )
        ret = self.quick_call(
            self.client, {"op": "walker_run", "name": "smart_yield_no_future"}
        )
        ret = self.quick_call(
            self.client, {"op": "walker_run", "name": "smart_yield_no_future"}
        )
        ret = self.quick_call(
            self.client, {"op": "walker_run", "name": "smart_yield_no_future"}
        )
        self.assertEqual(ret.data["report"], [{}])
