from . import api
from django.urls import path, include
from .views import GoogleLogin, FacebookLogin

app_name = "jac_api"

urlpatterns = api.generated_urls

urlpatterns += [

    path('auth/', include('dj_rest_auth.urls')),
    path('auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('registration/', include('dj_rest_auth.registration.urls')),

]