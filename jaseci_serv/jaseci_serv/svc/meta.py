from jaseci.svc import MetaService as Ms
from jaseci_serv.svc import (
    MailService,
    RedisService,
    TaskService,
    PromotheusService,
    ElasticService,
)
from .config import RUN_SVCS


class MetaService(Ms):

    ###################################################
    #                   OVERRIDEN                     #
    ###################################################
    def __init__(self):
        super().__init__(run_svcs=RUN_SVCS)

    ###################################################
    #                   OVERRIDEN                     #
    ###################################################

    def populate_context(self):
        from jaseci_serv.hook.orm import OrmHook
        from jaseci_serv.base.models import (
            Master,
            SuperMaster,
            GlobalVars,
            JaseciObject,
        )

        self.add_context(
            "hook", OrmHook, objects=JaseciObject.objects, globs=GlobalVars.objects
        )
        self.add_context("master", Master)
        self.add_context("super_master", SuperMaster)

    def populate_services(self):
        self.add_service_builder("redis", RedisService)
        self.add_service_builder("task", TaskService)
        self.add_service_builder("mail", MailService)
        self.add_service_builder("promon", PromotheusService)
        self.add_service_builder("elastic", ElasticService)
