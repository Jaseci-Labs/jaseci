from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from jaseci.utils.utils import TestCaseHelper
from django.test import TestCase
import uuid
import base64
import os


class test_ll_wall(TestCaseHelper, TestCase):
    """Test the authorized user node API"""

    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_user(
            'JSCITfdfdEST_test@jaseci.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        ll_loc = os.path.dirname(__file__) + '/ll_wall.jac'
        ll_file = base64.b64encode(
            open(ll_loc).read().encode()).decode()
        payload = {'op': 'sentinel_register',
                   'name': 'Something', 'code': ll_file, 'encoded': True}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        payload = {'op': 'global_sentinel_set'}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        self.user = get_user_model().objects.create_user(
            'J2SCITfdfdEST_test@jaseci.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.master = self.user.get_master()
        payload = {'op': 'sentinel_active_global'}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'graph_create'}
        self.snt = self.master._h.get_obj(
            self.master.jid, uuid.UUID(res.data['sentinel']['jid']))
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.gph = self.master._h.get_obj(
            self.master.jid, uuid.UUID(res.data['jid']))

    def tearDown(self):
        super().tearDown()

    def run_walker(self, w_name, ctx, prime=None):
        """Helper to make calls to execute walkers"""
        if(not prime):
            payload = {'snt': self.snt.id.urn, 'name': w_name,
                       'nd': self.gph.id.urn, 'ctx': ctx}
        else:
            payload = {'snt': self.snt.id.urn, 'name': w_name,
                       'nd': prime, 'ctx': ctx}
        res = self.client.post(
            reverse('jac_api:walker_run'), payload, format='json')
        return res.data

    def graph_node_set(self, nd_id, ctx):
        """Helper to set node context"""
        payload = {'snt': self.snt.id.urn, 'nd': nd_id, 'ctx': ctx}
        res = self.client.post(
            reverse('jac_api:graph_node_set'), payload, format='json')
        return res.data

    def test_ll_wall_get_gen_day(self):
        """Test get_gen_day walker response time after cerify day"""
        num_workettes = 112

        # generate random day workettes
        self.run_walker('gen_day_workettes', {
                        "date": "2021-07-12", "num_workettes": num_workettes})

        data = self.run_walker('get_latest_day', {'show_report': 1})

        day_id = data[0][1]['jid']
        day_date = data[0][1]['context']['day']
        day_note = data[0][1]['context']['note']

        data = self.run_walker('get_workettes_deep', {
                               'show_report': 1}, prime=day_id)
        self.assertEqual(len(data[0]), num_workettes)

        # certify day, should return day highlights
        data = self.run_walker('set_day_highlight', {"highlight_items": [
            {"id": data[0][0], "type": "Most proud accomplishment",
                "color": "#464ff6", "icon": "0x1F3C6"},
            {"id": data[0][1], "type": "Made You Happiest",
             "color": "#6e30dd", "icon": "0x1F604"},
            {"id": data[0][2], "type": "Required the Most Work",
             "color": "#b926df", "icon": "0x1F4AA"}
        ]}, prime=day_id)
        self.assertEqual(data[0][0][0][0][0]['jid'], day_id)
        self.assertEqual(data[0][0][0][0][1], day_date)
        self.assertEqual(data[0][0][0][1], day_note)

        # data[0][0][0][2] is the highlight items
        self.assertEqual(len(data[0][0][0][2]), 3)

        data = self.run_walker('get_gen_day', {"date": "2021-07-13"})

    def test_ll_highlevel_groups(self):
        """Test highlevel_groups walker when certifying a day"""

        self.run_walker('get_gen_day', {"date": "2021-07-15"})

        data = self.run_walker('get_latest_day', {'show_report': 1})

        day_id = data[0][1]['jid']

        g1 = self.run_walker('create_workette', {
                             "title": "group 1", "wtype": "workset"}, prime=day_id)
        self.assertEqual(g1[0]['context']['name'], 'group 1')
        self.assertEqual(g1[0]['context']['wtype'], 'workset')

        g2 = self.run_walker('create_workette', {
                             "title": "group 2", "wtype": "workset"}, prime=day_id)
        self.assertEqual(g2[0]['context']['name'], 'group 2')
        self.assertEqual(g2[0]['context']['wtype'], 'workset')

        # child of group 1
        g1_item1 = self.run_walker('create_workette', {
                                   "title": "item 1", "wtype": "workette"}, prime=g1[0]['jid'])
        self.assertEqual(g1_item1[0]['context']['name'], 'item 1')

        self.graph_node_set(g1_item1[0]['jid'], {"status": "done"})

        # child of item 1
        g1_item2 = self.run_walker('create_workette', {
                                   "title": "item 2", "wtype": "workette"}, prime=g1_item1[0]['jid'])
        self.assertEqual(g1_item2[0]['context']['name'], 'item 2')

        data = self.graph_node_set(g1_item2[0]['jid'], {"status": "done"})
        print("child of item 1", data)

        # child of item 2
        g1_item3 = self.run_walker('create_workette', {
                                   "title": "item 3", "wtype": "workette"}, prime=g1_item2[0]['jid'])
        self.assertEqual(g1_item3[0]['context']['name'], 'item 3')

        data = self.graph_node_set(g1_item3[0]['jid'], {"status": "done"})
        print("child of item 1", data)
        # child of item 2 - but not done
        g1_item4 = self.run_walker('create_workette', {
                                   "title": "item 4 - not done", "wtype": "workette"}, prime=g1_item2[0]['jid'])
        self.assertEqual(g1_item4[0]['context']['name'], 'item 4 - not done')

        #data = self.run_walker('set_day_highlevel_groups', {}, prime=day_id)
        # print(data)

        # certify day, should return day highlights
        data = self.run_walker('set_day_highlight', {
                               "highlight_items": []}, prime=day_id)

        dayNode = self.run_walker('get_workette', {}, day_id)

        highlevel_groups = dayNode[0]["context"]["highlevel_groups"]

        self.assertEqual(len(highlevel_groups), 2)
        self.assertEqual(highlevel_groups[0]["name"], "group 1")
        self.assertEqual(highlevel_groups[0]["completed_items"], 3)

        self.assertEqual(highlevel_groups[1]["name"], "group 2")
        self.assertEqual(highlevel_groups[1]["completed_items"], 0)
