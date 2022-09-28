from jaseci.svc import MetaService as Ms
from jaseci_serv.svc import MailService, RedisService, TaskService


class MetaService(Ms):

    ###################################################
    #                   OVERRIDEN                     #
    ###################################################

    def build_classes(self):
        from jaseci_serv.hook.orm import OrmHook
        from jaseci_serv.base.models import (
            Master,
            SuperMaster,
            GlobalVars,
            JaseciObject,
        )

        self.hook = OrmHook
        self.hook_param = {
            "args": [],
            "kwargs": {"objects": JaseciObject.objects, "globs": GlobalVars.objects},
        }
        self.master = Master
        self.super_master = SuperMaster

    def build_services(self):
        self.add_service_builder("redis", RedisService)
        self.add_service_builder("task", TaskService)
        self.add_service_builder("mail", MailService)
