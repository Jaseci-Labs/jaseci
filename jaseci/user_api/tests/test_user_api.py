from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.utils.utils import TestCaseHelper


# Consts for url
CREATE_USER_URL = reverse('user_api:create')
TOKEN_URL = reverse('user_api:token')
MANAGE_URL = reverse('user_api:manage')
# Alias for create user
create_user = get_user_model().objects.create_user
get_user = get_user_model().objects.get


class user_api_tests_public(TestCaseHelper):
    """Tests for user API (public)"""

    def setUp(self):
        super().setUp()
        self.client = APIClient()

    def tearDown(self):
        super().tearDown()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'jscitest_test2@jaseci.com',
            'password': 'testpass',
            'name': 'name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(
            user.check_password(payload['password'])
        )
        self.assertNotIn('password', res.data)
        user.delete()

    def test_create_activated_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'jscitest_test2@jaseci.com',
            'password': 'testpass',
            'name': 'name',
            'is_activated': True
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(
            user.check_password(payload['password'])
        )
        self.assertTrue(user.is_activated)
        self.assertNotIn('password', res.data)
        user.delete()

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {
            'email': 'jscitest_test2@jaseci.com',
            'password': 'testpass'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        get_user(email=payload['email']).delete()

    def test_password_too_short(self):
        """Test that passwords less than 8 characters fail"""
        payload = {
            'email': 'jscitest_test2@jaseci.com',
            'password': 'pw'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {'email': 'jscitest_test@jaseci.com', 'password': 'testpass'}
        user = create_user(**payload)
        user.is_activated = True
        user.save()
        res = self.client.post(TOKEN_URL, payload)

        # self.assertIsNotNone(get_user(email=payload['email']).hook)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        get_user(email=payload['email']).delete()

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='jscitest_test@jaseci.com', password='testpass')
        payload = {'email': 'jscitest_test@jaseci.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        get_user(email=payload['email']).delete()

    def test_create_token_no_user(self):
        """Test that token is not created if user doens't exist"""
        payload = {'email': 'jscitest_test@jaseci.com', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication required for users"""
        res = self.client.get(MANAGE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class user_api_tests_private(TestCaseHelper):
    """Test API requests that are authenticated"""

    def setUp(self):
        super().setUp()
        self.user = create_user(
            email='jscitest_test@jaseci.com',
            password='testpass',
            name='some dude',
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
        self.assertEqual(res.data, {
            'id': self.user.id,
            'name': self.user.name,
            'email': self.user.email,
            'is_activated': self.user.is_activated,
        })

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed to update user"""
        res = self.client.post(MANAGE_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {'name': 'new name', 'password': 'newpassword123'}

        res = self.client.patch(MANAGE_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
