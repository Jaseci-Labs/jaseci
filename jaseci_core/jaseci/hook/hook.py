from jaseci.svc import (
    MetaService,
    RedisService,
    PrometheusService,
    TaskService,
    MailService,
    ProxyService,
)


class Hook:
    def __init__(self, meta: MetaService):
        self._redis = None
        self._promon = None
        self._task = None
        self._mail = None
        self.meta = meta

    @property
    def redis(self) -> RedisService:
        if not self._redis:
            self._redis = ProxyService()
            self._redis = self.meta.get_service("redis", hook=self)
        return self._redis

    @property
    def promon(self) -> PrometheusService:
        if not self._promo:
            self._promo = self.meta.get_service("promon", hook=self)
        return self._promon

    @property
    def task(self) -> TaskService:
        if not self._task:
            self._task = self.meta.get_service("task", hook=self)
        return self._task

    @property
    def mail(self) -> MailService:
        if not self._mail:
            self._mail = self.meta.get_service("mail", hook=self)
        return self._mail

    def __getstate__(self):
        state = self.__dict__.copy()
        state["_redis"] = None
        state["_promon"] = None
        state["_task"] = None
        state["_mail"] = None
        return state
