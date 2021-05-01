from django.urls import path, include

from . import views

app_name = 'user_api'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('manage/', views.ManageUserView.as_view(), name='manage'),
    path('activate/<str:code>', views.ActivateUserView.as_view(),
         name='activate'),
    path('password_reset/',
         include('django_rest_passwordreset.urls',
                 namespace='password_reset')),
]
