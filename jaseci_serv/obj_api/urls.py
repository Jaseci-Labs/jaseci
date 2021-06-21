from django.urls import path, include
from rest_framework.routers import DefaultRouter

from obj_api import views

router = DefaultRouter()
router.register('obj', views.ObjectViewSet)
router.register('config', views.ConfigViewSet)

app_name = 'obj_api'

urlpatterns = [
    path('', include(router.urls))
]
