from jaseci.svcs.meta_svc import meta_svc as ms
from jaseci_serv.svcs.redis.redis_svc import redis_svc
from jaseci_serv.svcs.task.task_svc import task_svc
from jaseci_serv.svcs.mail.mail_svc import mail_svc
from jaseci_serv.jaseci_serv.settings import RUN_SVCS


class meta_svc(ms):
    def hook(self):
        h = self.app["hook"]()
        if RUN_SVCS:
            h.redis = redis_svc(h)
            h.task = task_svc(h)
            h.mail = mail_svc(h)
        return h

    def build_hook(self):
        from jaseci_serv.base.models import GlobalVars, JaseciObject
        from jaseci_serv.base.orm_hook import orm_hook

        return orm_hook(objects=JaseciObject.objects, globs=GlobalVars.objects)

    def build_master(self, *args, **kwargs):
        from jaseci_serv.base.models import master

        return master(*args, **kwargs)

    def build_super_master(self, *args, **kwargs):
        from jaseci_serv.base.models import super_master

        return super_master(*args, **kwargs)
