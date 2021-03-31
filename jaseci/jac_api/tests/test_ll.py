from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient

from core.utils.utils import TestCaseHelper
import uuid
import base64
import datetime
import random
from pprint import pprint


class test_ll(TestCaseHelper):
    """Test the authorized user node API"""

    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_user(
            'JSCITfdfdEST_test@jaseci.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.master = self.user.get_master()
        payload = {'op': 'create_graph', 'name': 'Something'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.gph = self.master._h.get_obj(uuid.UUID(res.data['jid']))
        payload = {'op': 'create_sentinel', 'name': 'Something'}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.snt = self.master._h.get_obj(uuid.UUID(res.data['jid']))
        ll_file = base64.b64encode(
            open("jac_api/tests/ll.jac").read().encode())
        payload = {'op': 'set_jac_code', 'snt': self.snt.id.urn,
                   'code': ll_file, 'encoded': True}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format='json')
        payload = {'op': 'compile', 'snt': self.snt.id.urn}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload)
        self.run_walker('init', {})

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
            reverse(f'jac_api:prime_run'), payload, format='json')
        return res.data

    def set_node_context(self, nd_id, ctx):
        """Helper to set node context"""
        payload = {'snt': self.snt.id.urn, 'nd': nd_id, 'ctx': ctx}
        self.client.post(reverse('jac_api:set_node_context'), payload, format='json')

    def test_ll_today_new(self):
        """Test LifeLogify Jac Implementation"""
        data = self.run_walker('get_gen_day', {})
        self.assertEqual(data[0][1]['kind'], 'day')
        jid = data[0][1]['jid']
        data = self.run_walker('get_gen_day', {})
        self.assertEqual(data[0][1]['jid'], jid)

    def test_ll_create_get_workette(self):
        """Test LifeLogify Jac Implementation"""
        data = self.run_walker('get_gen_day', {})
        self.assertEqual(data[0][1]['kind'], 'day')
        jid = data[0][1]['jid']
        data = self.run_walker('create_workette', {}, prime=jid)
        self.assertEqual(data[0]['kind'], 'workette')
        data = self.run_walker('create_workette', {}, prime=jid)
        self.assertEqual(data[0]['kind'], 'workette')
        data = self.run_walker('get_workettes', {}, prime=jid)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['kind'], 'workette')
        self.assertEqual(data[1]['kind'], 'workette')
        wjid = data[0]['jid']
        data = self.run_walker('create_workette', {}, prime=wjid)
        data = self.run_walker('create_workette', {}, prime=wjid)
        data = self.run_walker('create_workette', {}, prime=wjid)
        data = self.run_walker('get_workettes', {}, prime=wjid)
        self.assertEqual(len(data), 3)
        data = self.run_walker('get_workettes', {}, prime=jid)
        self.assertEqual(len(data), 2)
        data = self.run_walker('get_workettes_deep', {}, prime=jid)
        self.assertEqual(len(data), 5)

    def test_ll_get_date(self):
        """Test LifeLogify Jac Implementation"""
        data = self.run_walker('get_gen_day', {})
        data = self.run_walker('gen_rand_life', {})
        data = self.run_walker('get_latest_day', {'show_report': 1})
        wjid = data[0][1]['jid']
        data = self.run_walker('get_workettes', {}, prime=wjid)
        self.assertEqual(len(data), 0)
        data = self.run_walker('get_latest_day', {'before_date': '2020-03-01',
                                                  'show_report': 1})
        wjid = data[0][1]['jid']
        data = self.run_walker('get_workettes', {}, prime=wjid)
        self.assertGreater(len(data), 1)

    def test_ll_carry_forward_simple(self):
        """Test LifeLogify Jac Implementation"""
        data = self.run_walker('gen_rand_life', {})
        data = self.run_walker('get_gen_day', {})
        wjid = data[0][1]['jid']
        data = self.run_walker('get_workettes', {}, prime=wjid)
        self.assertGreater(len(data), 1)

    def test_ll_delete_workette(self):
        """Test LifeLogify Jac Implementation"""
        data = self.run_walker('get_gen_day', {})
        self.assertEqual(data[0][1]['kind'], 'day')
        jid = data[0][1]['jid']
        data = self.run_walker('create_workette', {}, prime=jid)
        self.assertEqual(data[0]['kind'], 'workette')
        data = self.run_walker('create_workette', {}, prime=jid)
        self.assertEqual(data[0]['kind'], 'workette')
        data = self.run_walker('get_workettes', {}, prime=jid)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['kind'], 'workette')
        self.assertEqual(data[1]['kind'], 'workette')
        wjid = data[0]['jid']
        data = self.run_walker('create_workette', {}, prime=wjid)
        data = self.run_walker('create_workette', {}, prime=wjid)
        data = self.run_walker('create_workette', {}, prime=wjid)
        data = self.run_walker('get_workettes', {}, prime=wjid)
        self.assertEqual(len(data), 3)
        data = self.run_walker('delete_workette', {}, prime=wjid)
        data = self.run_walker('get_workettes', {}, prime=jid)
        self.assertEqual(len(data), 1)
        data = self.run_walker('get_workettes_deep', {}, prime=jid)
        self.assertEqual(len(data), 1)

    def test_ll_delete_workette_no_leaks(self):
        """Test LifeLogify Jac Implementation"""
        data = self.run_walker('get_gen_day', {})
        self.assertEqual(data[0][1]['kind'], 'day')
        jid = data[0][1]['jid']
        data = self.run_walker('create_workette', {}, prime=jid)
        self.assertEqual(data[0]['kind'], 'workette')
        len_before = len(self.master._h.mem.keys())
        data = self.run_walker('create_workette', {}, prime=jid)
        self.assertEqual(data[0]['kind'], 'workette')
        data = self.run_walker('get_workettes', {}, prime=jid)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['kind'], 'workette')
        self.assertEqual(data[1]['kind'], 'workette')
        wjid = data[1]['jid']
        data = self.run_walker('create_workette', {}, prime=wjid)
        data = self.run_walker('create_workette', {}, prime=wjid)
        data = self.run_walker('create_workette', {}, prime=wjid)
        data = self.run_walker('get_workettes', {}, prime=wjid)
        self.assertEqual(len(data), 3)
        data = self.run_walker('delete_workette', {}, prime=wjid)
        data = self.run_walker('get_workettes', {}, prime=jid)
        self.assertEqual(len(data), 1)
        data = self.run_walker('get_workettes_deep', {}, prime=jid)
        self.assertEqual(len(data), 1)
        len_after = len(self.master._h.mem.keys())
        self.assertEqual(len_before, len_after)

    def test_ll_goal_associations(self):
        """Test setting categories for a workette"""
        CATS = [
            "professional work",
            "chores",
            "hobby",
            "relationship",
            "personal improvement"
        ]
        # Create a new day
        data = self.run_walker('get_gen_day', {})
        jid = data[0][1]['jid']

        # Create a new workette
        new_wkt = self.run_walker(
            'create_workette', {'title': 'work on Q2 roadmap'}, prime=jid)
        wkt_id = new_wkt[0]['jid']

        # Set categories for that workette
        self.run_walker(
            'add_and_associate_goals',
            {'goals': CATS},
            prime=wkt_id)
        updated_wkt = self.run_walker('get_workette', {}, prime=wkt_id)

        # Assert on categories
        self.assertSetEqual(set(updated_wkt[0]['context']['goals']), set(CATS))
        self.assertEqual(
            updated_wkt[0]['context']['sorted_goals'][0][0],
            'professional work')

    def test_parent_suggestion(self):
        """Test generating a suggested parent item for a given item"""
        new_wkt = 'clean up the house'
        self.run_walker('gen_rand_life', {})
        self.run_walker('get_gen_day', {})
        data = self.run_walker('get_latest_day', {'show_report': 1})
        w_id = data[0][1]['jid']
        data = self.run_walker('get_suggested_parent',
                                {'new_wkt_name': new_wkt}, prime=w_id)
        self.assertTrue(len(data) > 0)
        self.assertTrue(0 < data[-1][1] < 1)

    def test_due_soon(self):
        """Test generating a list of suggested focus items for a given day"""
        self.run_walker('gen_rand_life', {})
        self.run_walker('get_gen_day', {})
        data = self.run_walker('get_latest_day', {'show_report': 1})
        w_id = data[0][1]['jid']

        today_date = datetime.datetime.today()
        due_item = False
        for wkt in data:
            if wkt[1]['kind'] == 'workette':
                if random.choice([0, 1]) or not due_item:
                    due_item = True
                    due = random.randint(-3, 3)
                    due_date = today_date + datetime.timedelta(days=due)
                    due_date = due_date.replace(hour=0, minute=0, second=0, microsecond=0)
                    wkt[1]['context']['date'] = due_date.isoformat()
                    self.set_node_context(wkt[1]['jid'], wkt[1]['context'])

        data = self.run_walker('get_due_soon', {'soon': 4, 'show_report': 1}, prime=w_id)
        self.assertTrue(len(data) > 0)

    def test_get_snoozed_until_recent(self):
        """Test getting items that have been snoozed before and is now active"""
        self.run_walker('gen_rand_life', {})
        self.run_walker('get_gen_day', {})
        data = self.run_walker('get_latest_day', {'show_report': 1})
        w_id = data[0][1]['jid']
        today_date = datetime.datetime.today()
        snoozed_item = False
        for wkt in data:
            if wkt[1]['kind'] == 'workette':
                if random.choice([0, 1]) or not snoozed_item:
                    snoozed_item = True
                    delta = random.randint(-3, 0)
                    snoozed_date = today_date + datetime.timedelta(days=delta)
                    snoozed_date = snoozed_date.replace(hour=0, minute=0, second=0, microsecond=0)
                    wkt[1]['context']['snooze_till'] = snoozed_date.isoformat()
                    self.set_node_context(wkt[1]['jid'], wkt[1]['context'])
        result = self.run_walker('get_snoozed_until_recent', {'show_report': 1}, prime=w_id)

    def test_days_in_backlog(self):
        """Test getting the number of days an item has been in the backlog"""
        self.run_walker('gen_rand_life', {})
        self.run_walker('get_gen_day', {})
        data = self.run_walker('get_latest_day', {'show_report': 1})
        w_id = data[0][1]['jid']
        workettes = self.run_walker('get_workettes', {}, prime=w_id)
        for wkt in workettes:
            res = self.run_walker('days_in_backlog', {'show_report': 1}, prime=wkt['jid'])
            self.assertIs(type(res[0]), int)
    
    def test_get_long_active_items(self):
        """Test getting the list of items that have been in the backlog for long"""
        self.run_walker('gen_rand_life', {})
        self.run_walker('get_gen_day', {})
        data = self.run_walker('get_latest_day', {'show_report': 1})
        w_id = data[0][1]['jid']
        result = self.run_walker('get_long_active_items', {'show_report': 1}, prime=w_id)

    def test_get_suggested_focus(self):
        self.run_walker('gen_rand_life', {})
        self.run_walker('get_gen_day', {})
        data = self.run_walker('get_latest_day', {'show_report': 1})
        w_id = data[0][1]['jid']
        result = self.run_walker('get_suggested_focus', {'max_items': 5}, prime=w_id)
