from django.apps import AppConfig
from .jsorc.jsorc import jsorc_start
import sys


class JacApiConfig(AppConfig):
    name = "jaseci_serv.jac_api"

    def ready(self):
        if "runserver" in sys.argv:
            jsorc_start()
