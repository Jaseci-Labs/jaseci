from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'ui'

urlpatterns = [
    path('', views.UIHome.as_view(), name='ui'),
    path('test', views.Test.as_view(), name='test'),
    path('login', auth_views.LoginView.as_view(template_name='login.html'),
         name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('create_user', views.CreateUser.as_view(), name='create_user'),
]
