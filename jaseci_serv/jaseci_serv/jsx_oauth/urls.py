from django.urls import path, include
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
                    "examples/",
                    include(
                        [
                            path(
                                "google/",
                                GoogleExampleLiveView.as_view(),
                                name="google_example",
                            ),
                        ]
                    ),
                ),
            ]
        ),
    )
]
