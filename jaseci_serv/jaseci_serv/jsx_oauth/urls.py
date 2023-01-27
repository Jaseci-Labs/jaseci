from django.urls import path, re_path, include
from jaseci_serv.jsx_oauth.views import *


urlpatterns = [
    path(
        "auth/",
        include(
            [
                path("get-test-url/", ExampleUrlView.as_view(), name="get_test_url"),
                path("google/", GoogleLogin.as_view(), name="google_login"),
                path("facebook/", FaceBookLogin.as_view(), name="facebook_login"),
                path("github/", GitHubLogin.as_view(), name="github_login"),
                path("microsoft/", MicrosoftLogin.as_view(), name="microsoft_login"),
                path("okta/", OktaLogin.as_view(), name="okta_login"),
                # path("openid/", OpenIdLogin.as_view(), name="openid_login"), #
                path(
                    "examples/<str:provider>/",
                    ExampleLiveView.as_view(),
                    name="oauth_example",
                ),
            ]
        ),
    ),
    re_path(r"^accounts/", include("allauth.urls"), name="socialaccount_signup"),
]
