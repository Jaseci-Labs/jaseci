from jaseci.svcs.common_svc import common_svc
from jaseci.svcs.redis.redis_svc import redis_svc
from jaseci.svcs.task.task_svc import task_svc
from jaseci.svcs.mail.mail_svc import mail_svc
from jaseci.svcs.service_state import ServiceState as SS


class meta_svc(common_svc):
    def __init__(self, hook=None):
        super().__init__(meta_svc)

        if self.is_ready():
            self.state = SS.RUNNING
            self.app = {
                "hook": self.build_hook,
                "master": self.build_master,
                "super_master": self.build_super_master,
            }

    def hook(self):
        h = self.app["hook"]()
        h.redis = redis_svc(h)
        h.task = task_svc(h)
        h.mail = mail_svc(h)
        return h

    def __common(self, t, *args, **kwargs):

        if not kwargs.get("h", None):
            kwargs["h"] = self.hook()

        return self.app[t](*args, **kwargs)

    def master(self, *args, **kwargs):
        return self.__common("master", *args, **kwargs)

    def super_master(self, *args, **kwargs):
        return self.__common("super_master", *args, **kwargs)

    def build_hook(self):
        from jaseci.utils.redis_hook import redis_hook

        return redis_hook()

    def build_master(self, *args, **kwargs):
        from jaseci.element.master import master

        return master(*args, **kwargs)

    def build_super_master(self, *args, **kwargs):
        from jaseci.element.super_master import super_master

        return super_master(*args, **kwargs)
