from uuid import uuid4
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from jaseci.utils.utils import TestCaseHelper
from django.test import TestCase

from unittest.mock import MagicMock, Mock

from jaseci_serv.svc import MetaService, MailService
from jaseci_serv.svc.mail import MAIL_CONFIG


# Consts for url
CREATE_USER_URL = reverse("user_api:create")
TOKEN_URL = reverse("user_api:token")
MANAGE_URL = reverse("user_api:manage")
LOGOUT_EVERYONE_URL = reverse("user_api:logout_everyone")
PASSWORD_RESET_URL = reverse("user_api:password_reset:reset-password-request")
# Alias for create user
create_user = get_user_model().objects.create_user
create_superuser = get_user_model().objects.create_superuser
get_user = get_user_model().objects.get


class UserApiPublicTests(TestCaseHelper, TestCase):
    """Tests for user API (public)"""

    def __init__(self, *args, **kwargs):
        MAIL_CONFIG["enabled"] = True
        MailService.connect = MagicMock(return_value=Mock())
        super(UserApiPublicTests, self).__init__(*args, **kwargs)

    def setUp(self):
        super().setUp()
        self.meta = MetaService()
        self.hook = self.meta.build_hook()
        self.meta.get_service("mail").reset(self.hook)
        self.client = APIClient()

    def tearDown(self):
        super().tearDown()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            "email": "jscitest_test2@jaseci.com",
            "password": "testpass",
            "name": "name",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)
        user.delete()

    def test_first_user_is_super(self):
        """Test first user created its superuser"""
        payload = {
            "email": "jscitest_test2@jaseci.com",
            "password": "testpass",
            "name": "name",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.is_admin)
        payload = {
            "email": "jscitest_test4@jaseci.com",
            "password": "testpass",
            "name": "name",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user2 = get_user_model().objects.get(**res.data)
        self.assertFalse(user2.is_admin)
        user.delete()
        user2.delete()

    def test_create_activated_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            "email": "jscitest_test2@jaseci.com",
            "password": "testpass",
            "name": "name",
            "is_activated": True,
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertTrue(user.is_activated)
        self.assertNotIn("password", res.data)
        user.delete()

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {"email": "jscitest_test2@jaseci.com", "password": "testpass"}
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        get_user(email=payload["email"]).delete()

    def test_user_exists_js_api(self):
        """Test creating a user that already exists fails"""
        payload = {"email": "jscitest_test2@jaseci.com", "password": "testpass"}
        create_user(**payload)
        payload2 = {
            "op": "user_create",
            "name": "jscitest_test2@jaseci.com",
            "other_fields": {
                "password": "password",
                "is_activated": True,
            },
        }
        res = self.client.post(
            reverse(f'jac_api:{payload2["op"]}'), payload2, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        get_user(email=payload["email"]).delete()

    def test_password_too_short(self):
        """Test that passwords less than 8 characters fail"""
        payload = {"email": "jscitest_test2@jaseci.com", "password": "pw"}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)

    def test_logout_everyone(self):
        """Test admin level logout everyone"""
        payload = {"email": "jscitest_test@jaseci.com", "password": "testpass"}
        user = create_user(**payload)
        user.is_activated = True
        user.save()
        payload2 = {"email": "super@jaseci.com", "password": "testpass"}
        superuser = create_superuser(**payload2)
        superuser.save()

        res = self.client.post(TOKEN_URL, payload)
        token = res.data["token"]
        res = self.client.post(TOKEN_URL, payload2)
        stoken = res.data["token"]
        res = self.client.get(MANAGE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        res = self.client.get(MANAGE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.get(MANAGE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + stoken)
        self.client.post(LOGOUT_EVERYONE_URL, {})
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        res = self.client.get(MANAGE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        get_user(email=payload["email"]).delete()
        get_user(email=payload2["email"]).delete()

    def test_logout_everyone_requires_admin(self):
        """Test admin level logout everyone"""
        payload2 = {"email": "super@jaseci.com", "password": "testpass"}
        superuser = create_superuser(**payload2)
        superuser.save()
        payload = {"email": "jscitest_test@jaseci.com", "password": "testpass"}
        user = create_user(**payload)
        user.is_activated = True
        user.save()

        res = self.client.post(TOKEN_URL, payload)
        token = res.data["token"]
        res = self.client.post(TOKEN_URL, payload2)
        # stoken = res.data['token']
        res = self.client.get(MANAGE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        res = self.client.get(MANAGE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.get(MANAGE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        res = self.client.post(LOGOUT_EVERYONE_URL, {})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        res = self.client.get(MANAGE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        get_user(email=payload["email"]).delete()
        get_user(email=payload2["email"]).delete()

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {"email": "jscitest_test@jaseci.com", "password": "testpass"}
        user = create_user(**payload)
        user.is_activated = True
        user.save()
        res = self.client.post(TOKEN_URL, payload)

        # self.assertIsNotNone(get_user(email=payload['email']).hook)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        get_user(email=payload["email"]).delete()

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email="jscitest_test@jaseci.com", password="testpass")
        payload = {"email": "jscitest_test@jaseci.com", "password": "wrong"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        get_user(email=payload["email"]).delete()

    def test_create_token_no_user(self):
        """Test that token is not created if user doens't exist"""
        payload = {"email": "jscitest_test@jaseci.com", "password": "testpass"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {"email": "one", "password": ""})
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication required for users"""
        res = self.client.get(MANAGE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_password_reset_endpoint(self):
        """Test that password resent endpoint succeeds for the user"""
        payload = {"email": "jscitest_test@jaseci.com", "password": "testpass"}
        user = create_user(**payload)
        user.is_activated = True
        user.save()

        email_pl = {"email": "jscitest_test@jaseci.com"}

        res = self.client.post(PASSWORD_RESET_URL, email_pl)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        get_user(email=payload["email"]).delete()

    def test_password_reset_endpoint_invalid_email(self):
        """Test that password resent endpoint succeeds for the user"""
        payload = {"email": "jscitest_test@jaseci.com", "password": "testpass"}
        user = create_user(**payload)
        user.is_activated = True
        user.save()

        email_pl = {"email": "jjscitest_test@jaseci.com"}

        res = self.client.post(PASSWORD_RESET_URL, email_pl)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        get_user(email=payload["email"]).delete()


class UserApiPrivateTests(TestCaseHelper, TestCase):
    """Test API requests that are authenticated"""

    def setUp(self):
        super().setUp()
        self.user = create_user(
            email="jscitest_test@jaseci.com",
            password="testpass",
            name="some dude",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        self.user.delete()
        super().tearDown()

    def test_retrieve_user_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(MANAGE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data,
            {
                "id": self.user.id,
                "name": self.user.name,
                "email": self.user.email,
                "is_activated": self.user.is_activated,
                "is_superuser": self.user.is_superuser,
            },
        )

    def test_user_delete_js_api(self):
        """Test creating a user that already exists fails"""
        payload = {"email": "jscitest_test2@jaseci.com", "password": "testpass"}
        create_user(**payload)
        payload2 = {
            "op": "user_delete",
            "name": "jscitest_test2@jaseci.com",
        }
        self.assertTrue(
            get_user_model().objects.filter(email=payload2["name"]).exists()
        )
        res = self.client.post(
            reverse(f'jac_api:{payload2["op"]}'), payload2, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertFalse(
            get_user_model().objects.filter(email=payload2["name"]).exists()
        )
        res = self.client.post(
            reverse(f'jac_api:{payload2["op"]}'), payload2, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_deleteself_js_api(self):
        """Test creating a user that already exists fails"""
        selfname = "jscitest_test@jaseci.com"
        payload2 = {"op": "user_deleteself"}
        self.assertTrue(get_user_model().objects.filter(email=selfname).exists())
        res = self.client.post(
            reverse(f'jac_api:{payload2["op"]}'), payload2, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertFalse(get_user_model().objects.filter(email=selfname).exists())

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed to update user"""
        res = self.client.post(MANAGE_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {"name": "new name", "password": "newpassword123"}

        res = self.client.patch(MANAGE_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_user_profile_via_put(self):
        """Test updating the user profile for authenticated user"""
        payload = {
            "name": "new name",
            "password": "newpassword123",
            "email": "mars.ninja@gmail.com",
            "is_activated": True,
        }

        res = self.client.put(MANAGE_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_manage_user_by_id(self):
        """Test manage user by id"""
        payload = {"email": f"{uuid4()}@jaseci.com", "password": "testpass"}
        user = create_user(**payload)
        user.save()

        self.assertEqual(user.is_activated, False)
        self.assertEqual(user.is_superuser, False)

        payload = {"email": "super@jaseci.com", "password": "testpass"}
        superuser = create_superuser(**payload)
        superuser.save()

        res = self.client.post(TOKEN_URL, payload).data
        self.client.credentials(HTTP_AUTHORIZATION="Token " + res["token"])

        payload = {
            "is_activated": True,
            "is_superuser": True,
        }

        res = self.client.post(f"{MANAGE_URL}{user.id}", payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, "Update Success!")

        res = self.client.post(f"{MANAGE_URL}{user.id}", payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, "No changes found!")

        user = get_user(id=user.id)

        self.assertEqual(user.is_activated, True)
        self.assertEqual(user.is_superuser, True)
