# from __future__ import absolute_import, unicode_literals
# from uuid import uuid4
# from django.contrib.auth import get_user_model
# from django.urls import reverse

# from rest_framework.test import APIClient
# from rest_framework import status

# from jaseci.utils.utils import TestCaseHelper
# from django.test import TestCase
# from jaseci_enterprise.jsx_oauth.models import LicenseCheckStatus
# from allauth.socialaccount.models import SocialApp
# from datetime import datetime, timedelta


# from importlib import import_module
# from requests.exceptions import HTTPError

# from django.conf import settings
# from django.contrib.auth.models import User
# from django.core import mail
# from django.test.client import RequestFactory
# from django.test.utils import override_settings
# from django.urls import reverse

# from allauth.account import app_settings as account_settings
# from allauth.account.adapter import get_adapter
# from allauth.account.models import EmailAddress, EmailConfirmation
# from allauth.account.signals import user_signed_up
# from allauth.socialaccount.models import SocialAccount, SocialToken
# from allauth.socialaccount.tests import OAuth2TestsMixin
# from allauth.tests import MockedResponse, TestCase, patch

# # from allauth.socialaccount.providers import GoogleProvider
# from allauth.socialaccount.providers.google.provider import GoogleProvider


# GOOGLE_CLIENT_ID = (
#     "582296225245-3kqi04d89ahlk1kr8j15j1uolci0hrtq.apps.googleusercontent.com"
# )
# GOOGLE_CLIENT_SECRET = "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"
# GET_TEST_URL = reverse("get_test_url")
# SSO_PROVIDER = "GOOGLE"
# TOKEN_URL = reverse("user_api:token")
# MANAGE_URL = reverse("user_api:manage")
# LOGOUT_EVERYONE_URL = reverse("user_api:logout_everyone")
# PASSWORD_RESET_URL = reverse("user_api:password_reset:reset-password-request")
# # Alias for create user
# create_user = get_user_model().objects.create_user
# create_superuser = get_user_model().objects.create_superuser
# get_user = get_user_model().objects.get


# def toggle_license_validation(make_valid=True):
#     if make_valid:
#         lcs = LicenseCheckStatus.objects.create(
#             last_checked=datetime.now() - timedelta(days=3),
#             license_validity=datetime.now() + timedelta(days=30),
#             license_status=True,
#             is_user_active=True,
#         )
#         return lcs
#     else:
#         lcs = LicenseCheckStatus.objects.create(
#             last_checked=datetime.now() - timedelta(days=30),
#             license_validity=datetime.now() - timedelta(days=3),
#             license_status=False,
#             is_user_active=False,
#         )

#         return lcs


# class JSXUserAUthTests(TestCaseHelper, TestCase):
#     def setUp(self):
#         super().setUp()
#         self.user = create_user(
#             email="jscitest_test@jaseci.com",
#             password="testpass",
#             name="some dude",
#         )
#         self.social_app = SocialApp.objects.create(
#             provider="google",
#             name="google",
#             client_id=GOOGLE_CLIENT_ID,
#             secret=GOOGLE_CLIENT_SECRET,
#         )
#         self.client = APIClient()
#         # self.toggle_license_validation
#         # self.client.force_authenticate(user=self.user)

#     def tearDown(self):
#         self.user.delete()
#         super().tearDown()

#     def test_response_on_valid_license1(self):
#         """Test API response When license Expired"""
#         toggle_license_validation(True)
#         payload = {"provider": "GOOGLE"}
#         res = self.client.post(GET_TEST_URL, payload)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)

# # ===========================================================================================================================


# @override_settings(
#     SOCIALACCOUNT_AUTO_SIGNUP=True,
#     ACCOUNT_SIGNUP_FORM_CLASS=None,
#     ACCOUNT_EMAIL_VERIFICATION=account_settings.EmailVerificationMethod.MANDATORY,
# )

# class GoogleTests(OAuth2TestsMixin, TestCase):
#     provider_id = GoogleProvider.id

#     def get_mocked_response(
#         self,
#         family_name="Penners",
#         given_name="Raymond",
#         name="Raymond Penners",
#         email="raymond.penners@example.com",
#         verified_email=True,
#     ):
#         return MockedResponse(
#             200,
#             """
#               {"family_name": "%s", "name": "%s",
#                "picture": "https://lh5.googleusercontent.com/photo.jpg",
#                "locale": "nl", "gender": "male",
#                "email": "%s",
#                "link": "https://plus.google.com/108204268033311374519",
#                "given_name": "%s", "id": "108204268033311374519",
#                "verified_email": %s }
#         """
#             % (
#                 family_name,
#                 name,
#                 email,
#                 given_name,
#                 (repr(verified_email).lower()),
#             ),
#         )

#     # def test_google_compelete_login_401(self):
#     #     from allauth.socialaccount.providers.google.views import (
#     #         GoogleOAuth2Adapter,
#     #     )

#     #     class LessMockedResponse(MockedResponse):
#     #         def raise_for_status(self):
#     #             if self.status_code != 200:
#     #                 raise HTTPError(None)

#     #     request = RequestFactory().get(
#     #         reverse(self.provider.id + "_login"), dict(process="login")
#     #     )

#     #     adapter = GoogleOAuth2Adapter(request)
#     #     app = adapter.get_provider().get_app(request)
#     #     token = SocialToken(token="some_token")
#     #     response_with_401 = LessMockedResponse(
#     #         401,
#     #         """
#     #         {"error": {
#     #           "errors": [{
#     #             "domain": "global",
#     #             "reason": "authError",
#     #             "message": "Invalid Credentials",
#     #             "locationType": "header",
#     #             "location": "Authorization" } ],
#     #           "code": 401,
#     #           "message": "Invalid Credentials" }
#     #         }""",
#     #     )
#     #     with patch(
#     #         "allauth.socialaccount.providers.google.views.requests"
#     #     ) as patched_requests:
#     #         patched_requests.get.return_value = response_with_401
#     #         with self.assertRaises(HTTPError):
#     #             adapter.complete_login(request, app, token)

#     def test_username_based_on_email(self):
#         first_name = "明"
#         last_name = "小"
#         email = "raymond.penners@example.com"
#         self.login(
#             self.get_mocked_response(
#                 name=first_name + " " + last_name,
#                 email=email,
#                 given_name=first_name,
#                 family_name=last_name,
#                 verified_email=True,
#             )
#         )
#         user = User.objects.get(email=email)
#         self.assertEqual(user.username, "raymond.penners")

#     def test_email_verified(self):
#         test_email = "raymond.penners@example.com"
#         self.login(self.get_mocked_response(verified_email=True))
#         email_address = EmailAddress.objects.get(email=test_email, verified=True)
#         self.assertFalse(
#             EmailConfirmation.objects.filter(email_address__email=test_email).exists()
#         )
#         account = email_address.user.socialaccount_set.all()[0]
#         self.assertEqual(account.extra_data["given_name"], "Raymond")

#     def test_user_signed_up_signal(self):
#         sent_signals = []

#         def on_signed_up(sender, request, user, **kwargs):
#             sociallogin = kwargs["sociallogin"]
#             self.assertEqual(sociallogin.account.provider, GoogleProvider.id)
#             self.assertEqual(sociallogin.account.user, user)
#             sent_signals.append(sender)

#         user_signed_up.connect(on_signed_up)
#         self.login(self.get_mocked_response(verified_email=True))
#         self.assertTrue(len(sent_signals) > 0)

#     @override_settings(ACCOUNT_EMAIL_CONFIRMATION_HMAC=False)
#     def test_email_unverified(self):
#         test_email = "raymond.penners@example.com"
#         resp = self.login(self.get_mocked_response(verified_email=False))
#         email_address = EmailAddress.objects.get(email=test_email)
#         self.assertFalse(email_address.verified)
#         self.assertTrue(
#             EmailConfirmation.objects.filter(email_address__email=test_email).exists()
#         )
#         self.assertTemplateUsed(
#             resp, "account/email/email_confirmation_signup_subject.txt"
#         )

#     def test_email_verified_stashed(self):
#         # http://slacy.com/blog/2012/01/how-to-set-session-variables-in-django-unit-tests/
#         engine = import_module(settings.SESSION_ENGINE)
#         store = engine.SessionStore()
#         store.save()
#         self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
#         request = RequestFactory().get("/")
#         request.session = self.client.session
#         adapter = get_adapter(request)
#         test_email = "raymond.penners@example.com"
#         adapter.stash_verified_email(request, test_email)
#         request.session.save()

#         self.login(self.get_mocked_response(verified_email=False))
#         email_address = EmailAddress.objects.get(email=test_email)
#         self.assertTrue(email_address.verified)
#         self.assertFalse(
#             EmailConfirmation.objects.filter(email_address__email=test_email).exists()
#         )

#     def test_account_connect(self):
#         email = "user@example.com"
#         user = User.objects.create(username="user", is_active=True, email=email)
#         user.set_password("test")
#         user.save()
#         EmailAddress.objects.create(user=user, email=email, primary=True, verified=True)
#         self.client.login(username=user.username, password="test")
#         self.login(self.get_mocked_response(verified_email=True), process="connect")
#         # Check if we connected...
#         self.assertTrue(
#             SocialAccount.objects.filter(user=user, provider=GoogleProvider.id).exists()
#         )
#         # For now, we do not pick up any new e-mail addresses on connect
#         self.assertEqual(EmailAddress.objects.filter(user=user).count(), 1)
#         self.assertEqual(EmailAddress.objects.filter(user=user, email=email).count(), 1)

#     @override_settings(
#         ACCOUNT_EMAIL_VERIFICATION=account_settings.EmailVerificationMethod.MANDATORY,
#         SOCIALACCOUNT_EMAIL_VERIFICATION=account_settings.EmailVerificationMethod.NONE,
#     )
#     def test_social_email_verification_skipped(self):
#         test_email = "raymond.penners@example.com"
#         self.login(self.get_mocked_response(verified_email=False))
#         email_address = EmailAddress.objects.get(email=test_email)
#         self.assertFalse(email_address.verified)
#         self.assertFalse(
#             EmailConfirmation.objects.filter(email_address__email=test_email).exists()
#         )

#     @override_settings(
#         ACCOUNT_EMAIL_VERIFICATION=account_settings.EmailVerificationMethod.OPTIONAL,
#         SOCIALACCOUNT_EMAIL_VERIFICATION=account_settings.EmailVerificationMethod.OPTIONAL,
#     )
#     def test_social_email_verification_optional(self):
#         self.login(self.get_mocked_response(verified_email=False))
#         self.assertEqual(len(mail.outbox), 1)
#         self.login(self.get_mocked_response(verified_email=False))
#         self.assertEqual(len(mail.outbox), 1)
