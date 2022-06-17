from django.urls import include, path

from . import views

app_name = "user_api"

urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create"),
    path("create_super/", views.CreateSuperUserView.as_view(), name="create_super"),
    path("token/", views.CreateTokenView.as_view(), name="token"),
    path("manage/", views.ManageUserView.as_view(), name="manage"),
    path(
        "logout_everyone/", views.LogoutAllUsersView.as_view(), name="logout_everyone"
    ),
    path("activate/<str:code>", views.ActivateUserView.as_view(), name="activate"),
    path(
        "password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
    path(
        "sso/",
        include(
            [
                path("google/", views.GoogleSSOView.as_view(), name="google_login"),
                path(
                    "facebook/", views.FacebookSSOView.as_view(), name="facebook_login"
                ),
            ]
        ),
    ),
    # path(
    #     "sso/scripts",include(
    #         [
    #             path("google/", views.GoogleSSOScriptView.as_view()),
    #             # path("facebook/", views.FacebookSSOScriptView.as_view()),
    #         ]
    #     ),
    # ),
]
