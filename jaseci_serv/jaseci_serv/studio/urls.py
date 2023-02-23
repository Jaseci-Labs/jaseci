from django.urls import path, re_path
from django.conf.urls import url
from jaseci_serv.studio.views import *
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve
from django.conf import settings


urlpatterns = [
    path(
        "",
        studio_index,
        name="studio_index",
    ),
    path(
        "dashboard/",
        studio_dashboard,
        name="studio_dashboard",
    ),
    path(
        "graph-viewer/",
        studio_graph_viewer,
        name="studio_graph_viewer",
    ),
    path(
        "logs/",
        studio_logs_viewer,
        name="studio_logs_viewer",
    ),
    path(
        "architype/",
        studio_architype,
        name="studio_architype",
    ),
    path(
        "actions/",
        studio_actions,
        name="studio_actions",
    ),
]
