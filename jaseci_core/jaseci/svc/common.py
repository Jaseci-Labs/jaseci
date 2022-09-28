from .state import ServiceState as Ss


class CommonService:
    def __init__(self, cls):
        self.cls = cls
        if not hasattr(self.cls, "_app"):
            setattr(self.cls, "_app", None)
            setattr(self.cls, "_state", Ss.NOT_STARTED)
            setattr(self.cls, "_quiet", True)

    @property
    def app(self):
        return self.cls._app

    @app.setter
    def app(self, val):
        self.cls._app = val

    @property
    def state(self) -> Ss:
        return self.cls._state

    @state.setter
    def state(self, val: Ss):
        self.cls._state = val

    @property
    def quiet(self) -> bool:
        return self.cls._quiet

    @quiet.setter
    def quiet(self, val: bool):
        self.cls._quiet = val

    ###################################################
    #                     COMMONS                     #
    ###################################################

    def is_ready(self):
        return self.state.is_ready() and self.app is None

    def is_running(self):
        return self.state.is_running() and not (self.app is None)

    def has_failed(self):
        return self.state.has_failed()

    ###################################################
    #                     CLEANER                     #
    ###################################################

    def build(self, hook):
        self.app = None
        self.state = Ss.NOT_STARTED
        self.__init__(hook)


class ProxyService(CommonService):
    def __init__(self):
        super().__init__(ProxyService)


class MetaProperties:
    def __init__(self, prop):
        if not hasattr(prop, "_services"):
            setattr(prop, "_services", {})
            setattr(prop, "_background", {})
            setattr(prop, "_hook", None)
            setattr(prop, "_hook_param", {})
            setattr(prop, "_master", None)
            setattr(prop, "_super_master", None)

    @property
    def services(self) -> dict:
        return self.cls._services

    @services.setter
    def services(self, val: dict):
        self.cls._services = val

    @property
    def background(self) -> dict:
        return self.cls._background

    @background.setter
    def background(self, val: dict):
        self.cls._background = val

    @property
    def hook(self):
        return self.cls._hook

    @hook.setter
    def hook(self, val):
        self.cls._hook = val

    @property
    def hook_param(self) -> dict:
        return self.cls._hook_param

    @hook_param.setter
    def hook_param(self, val: dict):
        self.cls._hook_param = val

    @property
    def master(self):
        return self.cls._master

    @master.setter
    def master(self, val):
        self.cls._master = val

    @property
    def super_master(self):
        return self.cls._super_master

    @super_master.setter
    def super_master(self, val):
        self.cls._super_master = val
