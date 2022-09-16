from django.apps import AppConfig
from .jsorc.jsorc import jsorc_start


class CoreApiConfig(AppConfig):
    name = "jaseci_serv.base"

    def ready(self):
        jsorc_start()
