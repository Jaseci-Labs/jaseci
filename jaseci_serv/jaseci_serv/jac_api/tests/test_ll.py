from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from jaseci.utils.utils import TestCaseHelper
import jaseci.actions.live_actions as lact
from django.test import TestCase
import uuid
import base64
import datetime
import random
import os


class TestLL(TestCaseHelper, TestCase):
    """Test the authorized user node API"""

    def setUp(self):
        super().setUp()
        lact.load_local_actions(os.path.dirname(__file__) + "/infer.py")
        self.user = get_user_model().objects.create_user(
            "JSCITfdfdEST_test@jaseci.com", "password"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        ll_loc = os.path.dirname(__file__) + "/ll.jac"
        ll_file = base64.b64encode(open(ll_loc).read().encode()).decode()
        payload = {
            "op": "sentinel_register",
            "name": "Something",
            "code": ll_file,
            "encoded": True,
        }
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        payload = {"op": "global_sentinel_set"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.user = get_user_model().objects.create_user(
            "J2SCITfdfdEST_test@jaseci.com", "password"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.master = self.user.get_master()
        payload = {"op": "sentinel_active_global"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "graph_create"}
        self.snt = self.master._h.get_obj(
            self.master.jid, uuid.UUID(res.data["sentinel"]["jid"])
        )
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.gph = self.master._h.get_obj(self.master.jid, uuid.UUID(res.data["jid"]))

    def tearDown(self):
        super().tearDown()

    def run_walker(self, w_name, ctx, prime=None):
        """Helper to make calls to execute walkers"""
        if not prime:
            payload = {
                "snt": self.snt.id.urn,
                "name": w_name,
                "nd": self.gph.id.urn,
                "ctx": ctx,
            }
        else:
            payload = {"snt": self.snt.id.urn, "name": w_name, "nd": prime, "ctx": ctx}
        res = self.client.post(reverse("jac_api:walker_run"), payload, format="json")
        return res.data

    def graph_node_set(self, nd_id, ctx):
        """Helper to set node context"""
        payload = {"snt": self.snt.id.urn, "nd": nd_id, "ctx": ctx}
        self.client.post(reverse("jac_api:graph_node_set"), payload, format="json")

    def test_ll_today_new(self):
        """Test LifeLogify Jac Implementation"""
        data = self.run_walker("get_gen_day", {})["report"]
        self.assertEqual(data[0][1]["name"], "day")
        jid = data[0][1]["jid"]
        data = self.run_walker("get_gen_day", {})["report"]
        self.assertEqual(data[0][1]["jid"], jid)

    def test_ll_create_get_workette(self):
        """Test LifeLogify Jac Implementation"""
        data = self.run_walker("get_gen_day", {})["report"]
        self.assertEqual(data[0][1]["name"], "day")
        jid = data[0][1]["jid"]
        data = self.run_walker("create_workette", {}, prime=jid)["report"]
        self.assertEqual(data[0]["name"], "workette")
        data = self.run_walker("create_workette", {}, prime=jid)["report"]
        self.assertEqual(data[0]["name"], "workette")
        data = self.run_walker("get_workettes", {}, prime=jid)["report"]
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["name"], "workette")
        self.assertEqual(data[1]["name"], "workette")
        wjid = data[0]["jid"]
        data = self.run_walker("create_workette", {}, prime=wjid)["report"]
        data = self.run_walker("create_workette", {}, prime=wjid)["report"]
        data = self.run_walker("create_workette", {}, prime=wjid)["report"]
        data = self.run_walker("get_workettes", {}, prime=wjid)["report"]
        self.assertEqual(len(data), 3)
        data = self.run_walker("get_workettes", {}, prime=jid)["report"]
        self.assertEqual(len(data), 2)
        data = self.run_walker("get_workettes_deep", {}, prime=jid)["report"]
        self.assertEqual(len(data), 5)

    def test_ll_get_date(self):
        """Test LifeLogify Jac Implementation"""
        data = self.run_walker("get_gen_day", {})
        data = self.run_walker("gen_rand_life", {})
        data = self.run_walker("get_latest_day", {"show_report": 1})["report"]
        wjid = data[0][1]["jid"]
        data = self.run_walker("get_workettes", {}, prime=wjid)["report"]
        self.assertEqual(len(data), 0)
        data = self.run_walker(
            "get_latest_day", {"before_date": "2020-03-01", "show_report": 1}
        )["report"]
        wjid = data[0][1]["jid"]
        data = self.run_walker("get_workettes", {}, prime=wjid)["report"]
        self.assertGreater(len(data), 1)

    def test_ll_carry_forward_simple(self):
        """Test LifeLogify Jac Implementation"""
        data = self.run_walker("gen_rand_life", {})
        data = self.run_walker("get_gen_day", {})
        wjid = data["report"][0][1]["jid"]
        data = self.run_walker("get_workettes", {}, prime=wjid)
        self.assertGreater(len(data["report"]), 1)

    def test_ll_delete_workette(self):
        """Test LifeLogify Jac Implementation"""
        data = self.run_walker("get_gen_day", {})["report"]
        self.assertEqual(data[0][1]["name"], "day")
        jid = data[0][1]["jid"]
        data = self.run_walker("create_workette", {}, prime=jid)["report"]
        self.assertEqual(data[0]["name"], "workette")
        data = self.run_walker("create_workette", {}, prime=jid)["report"]
        self.assertEqual(data[0]["name"], "workette")
        data = self.run_walker("get_workettes", {}, prime=jid)["report"]
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["name"], "workette")
        self.assertEqual(data[1]["name"], "workette")
        wjid = data[0]["jid"]
        data = self.run_walker("create_workette", {}, prime=wjid)
        data = self.run_walker("create_workette", {}, prime=wjid)
        data = self.run_walker("create_workette", {}, prime=wjid)
        data = self.run_walker("get_workettes", {}, prime=wjid)["report"]
        self.assertEqual(len(data), 3)
        data = self.run_walker("delete_workette", {}, prime=wjid)
        data = self.run_walker("get_workettes", {}, prime=jid)["report"]
        self.assertEqual(len(data), 1)
        data = self.run_walker("get_workettes_deep", {}, prime=jid)["report"]
        self.assertEqual(len(data), 1)

    def test_ll_delete_workette_no_leaks(self):
        """Test LifeLogify Jac Implementation"""
        data = self.run_walker("get_gen_day", {})["report"]
        self.assertEqual(data[0][1]["name"], "day")
        jid = data[0][1]["jid"]
        data = self.run_walker("create_workette", {}, prime=jid)["report"]
        self.assertEqual(data[0]["name"], "workette")
        len_before = self.master._h.get_object_distribution()
        data = self.run_walker("create_workette", {}, prime=jid)["report"]
        self.assertEqual(data[0]["name"], "workette")
        data = self.run_walker("get_workettes", {}, prime=jid)["report"]
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["name"], "workette")
        self.assertEqual(data[1]["name"], "workette")
        wjid = data[1]["jid"]
        data = self.run_walker("create_workette", {}, prime=wjid)["report"]
        exjid = data[0]["jid"]
        data = self.run_walker("create_workette", {}, prime=wjid)
        data = self.run_walker("create_workette", {}, prime=wjid)
        data = self.run_walker("get_workettes", {}, prime=wjid)["report"]
        self.assertEqual(len(data), 3)
        data = self.run_walker("delete_workette", {}, prime=wjid)["report"]
        self.assertNotIn(uuid.UUID(exjid).urn, self.master._h.mem.keys())
        self.assertIn(uuid.UUID(jid).urn, self.master._h.mem.keys())
        data = self.run_walker("get_workettes", {}, prime=jid)["report"]
        self.assertEqual(len(data), 1)
        data = self.run_walker("get_workettes_deep", {}, prime=jid)["report"]
        self.assertEqual(len(data), 1)
        len_after = self.master._h.get_object_distribution()
        self.assertEqual(len_before, len_after)

    def test_due_soon(self):
        """Test generating a list of suggested focus items for a given day"""
        self.run_walker("gen_rand_life", {})
        self.run_walker("get_gen_day", {})
        data = self.run_walker("get_latest_day", {"show_report": 1})
        w_id = data["report"][0][1]["jid"]

        today_date = datetime.datetime.today()
        due_item = False
        for wkt in data["report"]:
            if wkt[1]["name"] == "workette":
                if random.choice([0, 1]) or not due_item:
                    due_item = True
                    due = random.randint(-3, 3)
                    due_date = today_date + datetime.timedelta(days=due)
                    due_date = due_date.replace(
                        hour=0, minute=0, second=0, microsecond=0
                    )
                    wkt[1]["context"]["date"] = due_date.isoformat()
                    self.graph_node_set(wkt[1]["jid"], wkt[1]["context"])

        data = self.run_walker(
            "get_due_soon", {"soon": 4, "show_report": 1}, prime=w_id
        )
        self.assertTrue(len(data["report"]) > 0)

    def test_days_in_backlog(self):
        """Test getting the number of days an item has been in the backlog"""
        self.run_walker("gen_rand_life", {})
        self.run_walker("get_gen_day", {})
        data = self.run_walker("get_latest_day", {"show_report": 1})
        w_id = data["report"][0][1]["jid"]
        workettes = self.run_walker("get_workettes", {}, prime=w_id)["report"]
        for wkt in workettes:
            res = self.run_walker(
                "days_in_backlog", {"show_report": 1}, prime=wkt["jid"]
            )
            self.assertIs(type(res["report"][0]), int)

    def test_get_long_active_items(self):
        """Test getting items been in backlog for long"""
        self.run_walker("gen_rand_life", {})
        self.run_walker("get_gen_day", {})
        data = self.run_walker("get_latest_day", {"show_report": 1})
        w_id = data["report"][0][1]["jid"]
        result = self.run_walker(
            "get_long_active_items", {"show_report": 1, "long_days": 1}, prime=w_id
        )
        self.assertTrue(len(result) > 0)

    def test_get_suggested_focus(self):
        self.run_walker("gen_rand_life", {})
        self.run_walker("get_gen_day", {})
        data = self.run_walker("get_latest_day", {"show_report": 1})
        w_id = data["report"][0][1]["jid"]
        result = self.run_walker(
            "get_suggested_focus", {"max_items": 5, "long_days": 1}, prime=w_id
        )
        self.assertTrue(len(result) > 0)
