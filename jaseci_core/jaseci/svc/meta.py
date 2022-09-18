from jaseci.svc import (
    CommonService,
    MailService,
    RedisService,
    ServiceState as Ss,
    TaskService,
)


class MetaService(CommonService):
    def __init__(self, hook=None):
        super().__init__(MetaService)

        if self.is_ready():
            self.state = Ss.RUNNING
            self.app = {
                "hook": self.build_hook,
                "master": self.build_master,
                "super_master": self.build_super_master,
            }

    def hook(self):
        h = self.app["hook"]()
        h.redis = RedisService(h)
        h.task = TaskService(h)
        h.mail = MailService(h)
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
        from jaseci.hook import RedisHook

        return RedisHook()

    def build_master(self, *args, **kwargs):
        from jaseci.element.master import Master

        return Master(*args, **kwargs)

    def build_super_master(self, *args, **kwargs):
        from jaseci.element.super_master import SuperMaster

        return SuperMaster(*args, **kwargs)
