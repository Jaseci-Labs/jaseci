from django.urls import path, include
from rest_framework.routers import DefaultRouter

from jaseci_serv.obj_api import views

router = DefaultRouter()
router.register("obj", views.ObjectViewSet)
router.register("global", views.ConfigViewSet)

app_name = "obj_api"

urlpatterns = [path("", include(router.urls))]
