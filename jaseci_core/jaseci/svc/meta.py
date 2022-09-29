from jaseci.svc import (
    CommonService,
    MetaProperties,
    MailService,
    RedisService,
    ServiceState as Ss,
    TaskService,
    KubernetesService,
    PromotheusService,
)

from jaseci.utils.utils import logger


class MetaService(CommonService, MetaProperties):
    def __init__(self, run_svcs=True):
        self.run_svcs = run_svcs
        MetaProperties.__init__(self, __class__)
        CommonService.__init__(self, __class__)

    ###################################################
    #                     BUILDER                     #
    ###################################################

    def build(self, hook=None):
        self.build_classes()
        self.build_services()
        self.state = Ss.RUNNING

    ###################################################
    #                    SERVICES                     #
    ###################################################

    # args & kwargs will be used as *args & **kwargs on initialization
    def add_service_builder(self, name, svc, custom=False, args=[], kwargs={}):
        if self.services.get(name):
            raise Exception(f"{name} already exists!")

        if not custom and not issubclass(svc, CommonService):
            raise Exception(
                f"{svc.__class__.__name__} is not instance of CommonService!"
            )

        self.services[name] = {"cls": svc, "args": args, "kwargs": kwargs}

    def run_service(self, name, background=False, *args, **kwargs):

        svc = self.services.get(name, False)

        if not svc:
            logger.error(f"Service {name} is not yet set!")
            return None

        kwargs.update(svc["kwargs"])

        svc = svc["cls"](*args, *svc["args"], **kwargs)

        if background:
            self.background[name] = svc

        return svc

    def get_service(self, name, *args, **kwargs):
        svc = self.background.get(name, False)

        if not svc:
            return self.run_service(name, True, *args, **kwargs)

        return svc

    ###################################################
    #                     BUILDER                     #
    ###################################################

    def build_hook(self):
        params = self.hook_param
        h = self.hook(*params.get("args", []), **params.get("kwargs", {}))
        if self.run_svcs:
            h.redis = self.get_service("redis", h)
            h.task = self.get_service("task", h)
            h.mail = self.get_service("mail", h)
            h.kube = self.get_service("kube", h)
            h.promon = self.get_service("promon", h)
            h.meta = self

        return h

    def build_master(self, *args, **kwargs):
        return self.__common(self.master, *args, **kwargs)

    def build_super_master(self, *args, **kwargs):
        return self.__common(self.super_master, *args, **kwargs)

    def __common(self, cls, *args, **kwargs):

        if not kwargs.get("h", None):
            kwargs["h"] = self.build_hook()

        return cls(*args, **kwargs)

    ###################################################
    #                   OVERRIDEN                     #
    ###################################################

    def build_classes(self):
        from jaseci.hook import RedisHook
        from jaseci.element.master import Master
        from jaseci.element.super_master import SuperMaster

        self.hook = RedisHook
        self.hook_param = {
            "args": [],  # override to add arg
            "kwargs": {},  # override to add field
        }
        self.master = Master
        self.super_master = SuperMaster

    def build_services(self):
        self.add_service_builder("redis", RedisService)
        self.add_service_builder("task", TaskService)
        self.add_service_builder("mail", MailService)
        self.add_service_builder("kube", KubernetesService)
        self.add_service_builder("promon", PromotheusService)
