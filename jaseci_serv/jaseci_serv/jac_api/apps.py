from django.apps import AppConfig
from .jsorc.jsorc import jsorc_start


class JacApiConfig(AppConfig):
    name = "jaseci_serv.jac_api"

    def ready(self):
        jsorc_start()
