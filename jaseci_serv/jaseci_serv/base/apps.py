from django.apps import AppConfig


class CoreApiConfig(AppConfig):
    name = "jaseci_serv.base"

    def ready(self):
        print("CoreApiConfig ready")
