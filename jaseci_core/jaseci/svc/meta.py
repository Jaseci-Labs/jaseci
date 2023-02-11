import signal
from jaseci.utils.utils import logger
from jaseci.svc import (
    CommonService,
    JsOrc,
    MailService,
    RedisService,
    TaskService,
    PrometheusService,
    ElasticService,
    ServiceState as Ss,
)


class MetaService(CommonService):
    app = None
    enabled = True
    state = Ss.NOT_STARTED
    quiet = False
    running_interval = 0

    def __init__(self, run_svcs=True):
        self.run_svcs = run_svcs

        self.start()

    ###################################################
    #                     BUILDER                     #
    ###################################################

    def run(self, hook=None):
        MetaService.app = JsOrc(self)
        self.populate_context()
        self.populate_services()

    def post_run(self, hook=None):
        if self.run_svcs:
            MetaService.app.build()
            if self.is_automated():
                logger.info("JsOrc is automated. Pushing interval check alarm...")
                self.push_interval(1)
            else:
                logger.info("JsOrc is not automated.")

    def push_interval(self, interval):
        if MetaService.state == 0:
            MetaService.state += 1
            signal.alarm(interval)
        else:
            logger.info("Reusing current running interval...")

    ###################################################
    #                    SERVICES                     #
    ###################################################

    def add_service_builder(self, name, svc):
        MetaService.app.add_service_builder(name, svc)

    def build_service(self, name, background, *args, **kwargs):
        return MetaService.app.build_service(name, background, *args, **kwargs)

    def get_service(self, name, *args, **kwargs):
        return MetaService.app.get_service(name, *args, **kwargs)

    ###################################################
    #                    CONTEXT                      #
    ###################################################

    def add_context(self, ctx, cls, *args, **kwargs):
        MetaService.app.add_context(ctx, cls, *args, **kwargs)

    def build_context(self, ctx, *args, **kwargs):
        return MetaService.app.build_context(ctx, *args, **kwargs)

    def get_context(self, ctx):
        return MetaService.app.context.get(ctx, {}).get("class")

    ###################################################
    #                     COMMON                      #
    ###################################################

    def is_automated(self):
        return self.is_running() and MetaService.app and MetaService.app.automated

    def in_cluster(self):
        return MetaService.app.in_cluster()

    ###################################################
    #                     BUILDER                     #
    ###################################################

    def build_hook(self):
        h = self.build_context("hook")
        h.meta = self
        if self.run_svcs:
            h.promon = self.get_service("promon", h)
            h.redis = self.get_service("redis", h)
            h.task = self.get_service("task", h)
            h.mail = self.get_service("mail", h)
            h.elastic = self.get_service("elastic", h)

            if not self.is_automated():
                h.mail.start(h)
                h.redis.start(h)
                h.task.start(h)
                h.elastic.start(h)

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

    def reset(self, hook=None, start=True):
        self.terminate_daemon("jsorc")
        MetaService.app = None
        MetaService.state = Ss.NOT_STARTED
        self.__init__()

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
        self.add_service_builder("promon", PrometheusService)
        self.add_service_builder("elastic", ElasticService)


def interval_check(signum, frame):
    meta = MetaService()
    if meta.is_automated():
        meta.app.interval_check()
        logger.info(
            f"Backing off for {meta.app.backoff_interval} seconds before the next interval check..."
        )

        # wait interval_check to be finished before decrement
        meta.running_interval -= 1
        meta.push_interval(meta.app.backoff_interval)
    else:
        meta.running_interval -= 1


signal.signal(signal.SIGALRM, interval_check)
