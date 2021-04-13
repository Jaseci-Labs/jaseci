from core.utils.utils import TestCaseHelper
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class ui_test(TestCaseHelper, TestCase):

    def setUp(self):
        """Creates test client, admin user and user for this test case"""
        super().setUp()
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="JSCIT88EST_admin@jaseci.com",
            password="password"
        )

    def tearDown(self):
        """Deletes test users out of databases"""
        super().tearDown()

    def test_main_page_loads_auth(self):
        """Tests that users show up on admin page"""
        self.client.force_login(self.admin_user)
        url = reverse('ui:ui')
        res = self.client.get(url)

        self.assertIsNotNone(self.admin_user._h)
        self.assertTrue('mynetwork' in str(res.content))
        self.assertTrue('Logout' in str(res.content))
        self.assertTrue('Login' not in str(res.content))
        self.assertTrue('Create Account' not in str(res.content))
        self.assertEqual(res.status_code, 200)
        self.client.logout()

    def test_page_loads_noauth(self):
        """Test that the user add and edit pages work"""
        url = reverse('ui:ui')
        res = self.client.get(url)

        self.assertTrue('mynetwork' not in str(res.content))
        self.assertTrue('Logout' not in str(res.content))
        self.assertTrue('Login' in str(res.content))
        self.assertTrue('Create Account' in str(res.content))
        self.assertEqual(res.status_code, 200)

    def test_page_loads_login(self):
        """Test that the user add and edit pages work"""
        url = reverse('ui:login')
        res = self.client.get(url)

        self.assertTrue('mynetwork' not in str(res.content))
        self.assertTrue('Logout' not in str(res.content))
        self.assertTrue('Email' in str(res.content))
        self.assertTrue('Password' in str(res.content))
        self.assertEqual(res.status_code, 200)

    def test_page_loads_create_user(self):
        """Test that the user add and edit pages work"""
        url = reverse('ui:create_user')
        res = self.client.get(url)

        self.assertTrue('mynetwork' not in str(res.content))
        self.assertTrue('Logout' not in str(res.content))
        self.assertTrue('Email Address' in str(res.content))
        self.assertTrue('Password confirmation' in str(res.content))
        self.assertEqual(res.status_code, 200)
