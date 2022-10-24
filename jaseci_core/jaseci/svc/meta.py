from jaseci.svc import (
    CommonService,
    ApplicationContext,
    MetaProperties,
    MailService,
    RedisService,
    TaskService,
    KubernetesService,
    PromotheusService,
    JsOrcService,
)


class MetaService(CommonService, MetaProperties):
    def __init__(self, run_svcs=True):
        self.run_svcs = run_svcs
        MetaProperties.__init__(self, __class__)

        self.start()

    ###################################################
    #                     BUILDER                     #
    ###################################################

    def run(self, hook=None):
        self.app = ApplicationContext()
        self.populate_context()
        self.populate_services()

    ###################################################
    #                    SERVICES                     #
    ###################################################

    def add_service_builder(self, name, svc):
        self.app.add_service_builder(name, svc)

    def build_service(self, name, background, *args, **kwargs):
        return self.app.build_service(name, background, *args, **kwargs)

    def get_service(self, name, *args, **kwargs):
        return self.app.get_service(name, *args, **kwargs)

    ###################################################
    #                    CONTEXT                      #
    ###################################################

    def add_context(self, ctx, cls, *args, **kwargs):
        self.app.add_context(ctx, cls, *args, **kwargs)

    def build_context(self, ctx, *args, **kwargs):
        return self.app.build_context(ctx, *args, **kwargs)

    def get_context(self, ctx):
        return self.app.context.get(ctx, {}).get("class")

    ###################################################
    #                     BUILDER                     #
    ###################################################

    def build_hook(self):
        h = self.build_context("hook")
        h.meta = self
        if self.run_svcs:
            h.kube = self.get_service("kube", h)
            h.jsorc = self.get_service("jsorc", h)
            h.promon = self.get_service("promon", h)
            h.redis = self.get_service("redis", h)
            h.task = self.get_service("task", h)
            h.mail = self.get_service("mail", h)

            if not (
                h.kube.start(h)
                and h.kube.is_running()
                and h.jsorc.start(h)
                and h.jsorc.is_running()
            ):
                h.mail.start(h)
                h.redis.start(h)
                h.task.start(h)

        return h

    def build_master(self, *args, **kwargs):
        return self.__common("master", *args, **kwargs)

    def build_super_master(self, *args, **kwargs):
        return self.__common("super_master", *args, **kwargs)

    def __common(self, ctx, *args, **kwargs):
        if not kwargs.get("h", None):
            kwargs["h"] = self.build_hook()

        return self.build_context(ctx, *args, **kwargs)

    ###################################################
    #                   OVERRIDEN                     #
    ###################################################

    def populate_context(self):
        from jaseci.hook import RedisHook
        from jaseci.element.master import Master
        from jaseci.element.super_master import SuperMaster

        self.add_context("hook", RedisHook)
        self.add_context("master", Master)
        self.add_context("super_master", SuperMaster)

    def populate_services(self):
        self.add_service_builder("redis", RedisService)
        self.add_service_builder("task", TaskService)
        self.add_service_builder("mail", MailService)
        self.add_service_builder("kube", KubernetesService)
        self.add_service_builder("promon", PromotheusService)
        self.add_service_builder("jsorc", JsOrcService)
