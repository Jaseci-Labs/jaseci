from jaseci.svc import MetaService as Ms
from jaseci_serv.jaseci_serv.settings import RUN_SVCS
from jaseci_serv.svc import MailService, RedisService, TaskService


class MetaService(Ms):
    def hook(self):
        h = self.app["hook"]()
        if RUN_SVCS:
            h.redis = RedisService(h)
            h.task = TaskService(h)
            h.mail = MailService(h)
        return h

    def build_hook(self):
        from jaseci_serv.base.models import GlobalVars, JaseciObject
        from jaseci_serv.hook.orm import OrmHook

        return OrmHook(objects=JaseciObject.objects, globs=GlobalVars.objects)

    def build_master(self, *args, **kwargs):
        from jaseci_serv.base.models import Master

        return Master(*args, **kwargs)

    def build_super_master(self, *args, **kwargs):
        from jaseci_serv.base.models import SuperMaster

        return SuperMaster(*args, **kwargs)
