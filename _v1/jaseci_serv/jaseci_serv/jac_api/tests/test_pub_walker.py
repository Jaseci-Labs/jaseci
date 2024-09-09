from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient

from jaseci.utils.utils import TestCaseHelper
from django.test import TestCase

import os


class PublicWalkerApiTests(TestCaseHelper, TestCase):
    """Test the authorized user node API"""

    def setUp(self):
        super().setUp()
        get_user_model().objects.create_user(
            "throwawayJSCITfdfdEST_test@jaseci.com", "password"
        )
        self.user = get_user_model().objects.create_user(
            "JSCITfdfdEST_test@jaseci.com", "password"
        )
        self.user2 = get_user_model().objects.create_user(
            "JSCITfdfdEST_test1@jaseci.com", "password"
        )
        self.admin = get_user_model().objects.create_superuser(
            "JSCITfdfdEST_test2@jaseci.com", "password"
        )
        self.no_user_client = APIClient()
        self.user_client = APIClient()
        self.user2_client = APIClient()
        self.admin_client = APIClient()
        self.user_client.force_authenticate(self.user)
        self.user2_client.force_authenticate(self.user2)
        self.admin_client.force_authenticate(self.admin)

        self.master = self.user.get_master()

        zsb_file = open(os.path.dirname(__file__) + "/public.jac").read()

        payload = {"op": "sentinel_register", "name": "public", "code": zsb_file}
        self.admin_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        payload = {"op": "global_sentinel_set"}
        self.admin_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        payload = {"op": "sentinel_active_global"}
        self.admin_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        payload = {"op": "sentinel_register", "name": "public", "code": zsb_file}
        self.user_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        payload = {"op": "sentinel_register", "name": "public", "code": zsb_file}
        self.user2_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        payload = {"op": "walker_run", "name": "manual_init"}
        res = self.user_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        ).data
        self.user_node = res["report"][0]["jid"]

        payload = {"op": "walker_run", "name": "manual_init"}
        res = self.user2_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        ).data
        self.user2_node = res["report"][0]["jid"]

        payload = {"op": "walker_run", "name": "manual_init"}
        res = self.admin_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        ).data
        self.admin_node = res["report"][0]["jid"]

        payload = {"op": "walker_spawn_create", "name": "show_a_details"}
        res = self.user_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        ).data
        self.user_walker = res["jid"].split(":")[2]

        payload = {"op": "walker_spawn_create", "name": "show_a_details"}
        res = self.user2_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        ).data
        self.user2_walker = res["jid"].split(":")[2]

        payload = {"op": "walker_spawn_create", "name": "show_a_details"}
        res = self.admin_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        ).data
        self.admin_walker = res["jid"].split(":")[2]

        payload = {
            "op": "walker_get",
            "mode": "keys",
            "wlk": "spawned:walker:show_a_details",
        }
        res = self.user_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        ).data

        self.user_key = res["requestor"]

        payload = {
            "op": "walker_get",
            "mode": "keys",
            "wlk": "spawned:walker:show_a_details",
        }
        res = self.user2_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        ).data

        self.user2_key = res["requestor"]

        payload = {
            "op": "walker_get",
            "mode": "keys",
            "wlk": "spawned:walker:show_a_details",
        }
        res = self.admin_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        ).data

        self.admin_key = res["requestor"]

    def tearDown(self):
        super().tearDown()

    def walker_callback_trigger(self, payload):
        payload["op"] = "walker_callback"
        return self.no_user_client.post(
            reverse(f'jac_api:{payload["op"]}', args=[payload["nd"], payload["wlk"]])
            + "?keys="
            + payload["key"],
            payload,
            format="json",
        ).data

    def test_user_public_walker_to_user_node(self):
        """Test public API for walker callback"""

        res = self.walker_callback_trigger(
            {"key": self.user_key, "wlk": self.user_walker, "nd": self.user_node}
        )

        self.assertEqual(res["report"][0]["context"]["value"], "user")
        self.assertEqual(res["report"][1]["context"]["value"], "changed")

    def test_user_public_walker_to_admin_node(self):
        """Test public API for walker callback"""

        res = self.walker_callback_trigger(
            {"key": self.user_key, "wlk": self.user_walker, "nd": self.admin_node}
        )

        self.assertFalse(res["success"])

    def test_user_public_walker_to_other_user_node(self):
        """Test public API for walker callback"""

        res = self.walker_callback_trigger(
            {"key": self.user_key, "wlk": self.user_walker, "nd": self.user2_node}
        )

        self.assertFalse(res["success"])

        res = self.walker_callback_trigger(
            {"key": self.user2_key, "wlk": self.user2_walker, "nd": self.user_node}
        )

        self.assertFalse(res["success"])

    def test_admin_public_walker_to_user_node(self):
        """Test public API for walker callback"""

        res = self.walker_callback_trigger(
            {"key": self.admin_key, "wlk": self.admin_walker, "nd": self.user_node}
        )

        self.assertEqual(res["report"][0]["context"]["value"], "user")
        self.assertEqual(res["report"][1]["context"]["value"], "changed")

        res = self.walker_callback_trigger(
            {"key": self.admin_key, "wlk": self.admin_walker, "nd": self.user2_node}
        )

        self.assertEqual(res["report"][0]["context"]["value"], "user")
        self.assertEqual(res["report"][1]["context"]["value"], "changed")
