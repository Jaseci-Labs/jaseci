import os
from django.apps import AppConfig

from jaseci.jsorc.jsorc import JsOrc


class CoreApiConfig(AppConfig):
    name = "jaseci_serv.svc"

    def ready(self):
        from .task_svc import TaskService  # noqa
        from .socket_svc import SocketService  # noqa

        if os.environ.get("RUN_MAIN"):
            JsOrc.run()
