from django.urls import path
from jaseci_serv.studio.views import *


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
