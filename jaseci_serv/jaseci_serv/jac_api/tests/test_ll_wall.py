from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from jaseci.utils.utils import TestCaseHelper
import jaseci.actions.live_actions as lact
from django.test import TestCase
import uuid
import base64
import os


class TestLLWall(TestCaseHelper, TestCase):
    """Test the authorized user node API"""

    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_user(
            "JSCITfdfdEST_test@jaseci.com", "password"
        )
        self.master = self.user.get_master()
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        ll_loc = os.path.dirname(__file__) + "/ll_wall.jac"
        ll_file = base64.b64encode(open(ll_loc).read().encode()).decode()
        payload = {
            "op": "sentinel_register",
            "name": "Something",
            "code": ll_file,
            "encoded": True,
        }
        lact.load_local_actions(os.path.dirname(__file__) + "/infer.py")
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.snt = self.master._h.get_obj(
            self.master.jid, uuid.UUID(res.data[0]["jid"])
        )
        self.gph = self.master._h.get_obj(
            self.master.jid, uuid.UUID(res.data[1]["jid"])
        )

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
        res = self.client.post(
            reverse("jac_api:graph_node_set"), payload, format="json"
        )
        return res.data

    def test_ll_wall_get_gen_day(self):
        """Test get_gen_day walker response time after cerify day"""
        num_workettes = 3
        # generate random day workettes
        self.run_walker(
            "gen_day_workettes", {"date": "2021-07-12", "num_workettes": num_workettes}
        )
        data = self.run_walker("get_latest_day", {"show_report": 1})["report"]

        day_id = data[0][1]["jid"]
        day_date = data[0][1]["context"]["day"]
        day_note = data[0][1]["context"]["note"]

        data = self.run_walker("get_workettes_deep", {"show_report": 1}, prime=day_id)[
            "report"
        ]
        self.assertEqual(len(data[0]), num_workettes)

        # certify day, should return day highlights
        data = self.run_walker(
            "set_day_highlight",
            {
                "highlight_items": [
                    {
                        "id": data[0][0],
                        "type": "Most proud accomplishment",
                        "color": "#464ff6",
                        "icon": "0x1F3C6",
                    },
                    {
                        "id": data[0][1],
                        "type": "Made You Happiest",
                        "color": "#6e30dd",
                        "icon": "0x1F604",
                    },
                    {
                        "id": data[0][2],
                        "type": "Required the Most Work",
                        "color": "#b926df",
                        "icon": "0x1F4AA",
                    },
                ]
            },
            prime=day_id,
        )["report"]
        self.assertEqual(data[0][0][0][0][0]["jid"], day_id)
        self.assertEqual(data[0][0][0][0][1], day_date)
        self.assertEqual(data[0][0][0][1], day_note)

        # data[0][0][0][2] is the highlight items
        self.assertEqual(len(data[0][0][0][2]), 3)
