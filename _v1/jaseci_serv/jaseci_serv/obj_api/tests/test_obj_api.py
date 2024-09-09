from django.contrib.auth import get_user_model
from django.urls import reverse

from jaseci.utils.utils import TestCaseHelper
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from jaseci_serv.base.models import JaseciObject, GlobalVars


NODE_URL = reverse("obj_api:jaseciobject-list")
CONFIG_URL = reverse("obj_api:globalvars-list")


class PublicNodeApiTests(TestCaseHelper, TestCase):
    """Test the publicly available node API"""

    def setUp(self):
        super().setUp()
        self.client = APIClient()

    def tearDown(self):
        super().tearDown()

    def test_login_required_obj_api(self):
        """Test that login required for retrieving nodes"""
        res = self.client.get(NODE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateNodeApiTests(TestCaseHelper, TestCase):
    """Test the authorized user node API"""

    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_user(
            "JSCITfdfdEST_test@jaseci.com", "password"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def tearDown(self):
        super().tearDown()

    def test_retrieve_nodes(self):
        """Test retrieving node list"""
        JaseciObject.objects.create(name="Vegan")
        JaseciObject.objects.create(name="Dessert")

        res = self.client.get(NODE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # def test_nodes_limited_to_user(self):
    #     """Test that nodes returned are for authenticated user"""
    #     user2 = get_user_model().objects.create_user(
    #         'JSCITEST_other@jaseci.com',
    #         'testpass'
    #     )
    #     JaseciObject.objects.create(name='Fruity')
    #     node = JaseciObject.objects.create(name='Comfort Food')

    #     res = self.client.get(NODE_URL)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data['results']), 2)
    #     self.assertEqual(res.data['results'][1]['name'], node.name)
    #     user2.delete()

    def test_create_node_successful(self):
        """Test creating a new node"""
        payload = {"name": "Simple", "j_type": "node"}
        self.client.post(NODE_URL, payload)

        exists = JaseciObject.objects.filter(name=payload["name"]).exists()
        self.assertTrue(exists)


class ConfigApiTests(TestCaseHelper, TestCase):
    """Test the authorized user node API"""

    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_superuser(
            "JSCITfdfdEST_test@jaseci.com", "password"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def tearDown(self):
        super().tearDown()

    def test_retrieve_configs(self):
        """Test retrieving config list"""
        GlobalVars.objects.create(name="Vegan", value="46")
        GlobalVars.objects.create(name="Dessert", value="446")

        res = self.client.get(CONFIG_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_config_successful(self):
        """Test creating a new config"""
        payload = {"name": "Simple", "value": "Peezzy"}
        self.client.post(CONFIG_URL, payload)

        exists = GlobalVars.objects.filter(
            name=payload["name"], value=payload["value"]
        ).exists()
        self.assertTrue(exists)

    def test_configs_limited_to_admin_user(self):
        """Test that configs only available to admin user"""
        user2 = get_user_model().objects.create_user(
            "JSCITEST_other@jaseci.com", "testpass"
        )
        client = APIClient()
        client.force_authenticate(user2)

        payload = {"name": "Simple", "value": "Peezzy"}
        res = client.post(CONFIG_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
