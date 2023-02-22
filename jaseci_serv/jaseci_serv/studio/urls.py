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
        TemplateView.as_view(template_name="studio/index.html"),
        name="studio_index",
    ),
    path(
        "dashboard/",
        TemplateView.as_view(template_name="studio/dashboard.html"),
        name="studio_dashboard",
    ),
    path(
        "graph-viewer/",
        TemplateView.as_view(template_name="studio/graph-viewer.html"),
        name="studio_graph_viewer",
    ),
    path(
        "logs/",
        TemplateView.as_view(template_name="studio/logs.html"),
        name="studio_logs_viewer",
    ),
    path(
        "architype/",
        TemplateView.as_view(template_name="studio/architype.html"),
        name="studio_architypes",
    ),
    path(
        "actions/",
        TemplateView.as_view(template_name="studio/actions.html"),
        name="studio_actions",
    ),
]
