from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
import jaseci.actions.live_actions as lact
from jaseci.utils.utils import TestCaseHelper
from django.test import TestCase
import uuid
import base64
import os


class test_zsb(TestCaseHelper, TestCase):
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
        zsb_loc = os.path.dirname(__file__) + '/zsb.jac'
        ll_file = base64.b64encode(
            open(zsb_loc).read().encode()).decode()
        payload = {'op': 'sentinel_register',
                   'name': 'Something', 'code': ll_file, 'encoded': True}
        res = self.client.post(reverse(f'jac_api:{payload["op"]}'), payload)
        self.snt = self.master._h.get_obj(
            self.master.jid, uuid.UUID(res.data[0]['jid']))
        self.gph = self.master._h.get_obj(
            self.master.jid, uuid.UUID(res.data[1]['jid']))

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

    def test_zsb_create_answer(self):
        """Test ZSB Create Answer call USE api"""
        if (not lact.load_remote_actions('http://js-use-qa')):
            self.skipTest("external resource not available")
        data = self.run_walker('add_bot', {'name': "Bot"})
        self.assertEqual(data['report'][0]['name'], 'bot')
        bot_jid = data['report'][0]['jid']
        data = self.run_walker('create_answer', {'text': "Yep"}, prime=bot_jid)
        self.assertEqual(data['report'][0]['name'], 'answer')

    def test_zsb_ask_question(self):
        """Test ZSB Create Answer call USE api"""
        if (not lact.load_remote_actions('http://js-use-qa')):
            self.skipTest("external resource not available")
        data = self.run_walker('add_bot', {'name': "Bot"})
        self.assertEqual(data['report'][0]['name'], 'bot')
        bot_jid = data['report'][0]['jid']
        data = self.run_walker('create_answer', {'text': "Yep"}, prime=bot_jid)
        data = self.run_walker(
            'create_answer', {'text': "Nope"}, prime=bot_jid)
        data = self.run_walker(
            'create_answer', {'text': "Maybe"}, prime=bot_jid)
        data = self.run_walker(
            'ask_question', {'text': "Who says yep?"}, prime=bot_jid)
        data = self.run_walker(
            'get_log', {}, prime=bot_jid)
        self.assertEqual(data['report'][0][0][1], 'Who says yep?')

    def test_zsb_ask_question_multi(self):
        """Test ZSB Create Answer call USE api"""
        if (not lact.load_remote_actions('http://js-use-qa')):
            self.skipTest("external resource not available")
        data = self.run_walker('add_bot', {'name': "Bot"})
        self.assertEqual(data['report'][0]['name'], 'bot')
        bot_jid = data['report'][0]['jid']
        data = self.run_walker('create_answer', {'text': "Yep"}, prime=bot_jid)
        data = self.run_walker(
            'create_answer', {'text': "Nope"}, prime=bot_jid)
        data = self.run_walker(
            'create_answer', {'text': "Maybe"}, prime=bot_jid)
        data = self.run_walker(
            'ask_question', {'text': "Who says yep?"}, prime=bot_jid)
        data = self.run_walker(
            'ask_question', {'text': "Who says yep?"}, prime=bot_jid)
        data = self.run_walker(
            'ask_question', {'text': "Who says yep?"}, prime=bot_jid)
        data = self.run_walker(
            'get_log', {}, prime=bot_jid)
        self.assertEqual(data['report'][0][0][1], 'Who says yep?')
