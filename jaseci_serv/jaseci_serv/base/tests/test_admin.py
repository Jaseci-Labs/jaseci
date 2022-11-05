from jaseci.utils.utils import TestCaseHelper
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminTests(TestCaseHelper, TestCase):
    def setUp(self):
        """Creates test client, admin user and user for this test case"""
        super().setUp()
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="JSCITEST_admin@jaseci.com", password="password"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="JSCITEST_test@jaseci.com", password="password"
        )

    def tearDown(self):
        """Deletes test users out of databases"""
        self.admin_user.delete()
        self.user.delete()
        super().tearDown()

    def test_users_listed(self):
        """Tests that users show up on admin page"""
        url = reverse("admin:base_user_changelist")
        res = self.client.get(url)

        self.assertTrue(self.user.name in str(res.content))
        self.assertTrue(self.user.email in str(res.content))
        self.assertEqual(res.status_code, 200)

    def test_user_add_edit_page(self):
        """Test that the user add and edit pages work"""
        url = reverse("admin:base_user_change", args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

        url = reverse("admin:base_user_add")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_base_has_global_config(self):
        """Tests that global config show up on admin page"""
        url = reverse("admin:base_globalvars_changelist")
        res = self.client.get(url)

        self.assertTrue("Global vars" in str(res.content))
        self.assertEqual(res.status_code, 200)

    def test_base_has_jaseci_objs(self):
        """Tests that jaseci objects show up on admin page"""
        url = reverse("admin:base_jaseciobject_changelist")
        res = self.client.get(url)

        self.assertTrue("Jaseci objects" in str(res.content))
        self.assertEqual(res.status_code, 200)
