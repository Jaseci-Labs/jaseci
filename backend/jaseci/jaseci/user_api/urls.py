from django.urls import path

from . import views

app_name = 'user_api'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('manage/', views.ManageUserView.as_view(), name='manage'),
]
