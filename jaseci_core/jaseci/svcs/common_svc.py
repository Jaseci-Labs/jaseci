from jaseci.utils.app_state import AppState as AS


class common_svc:
    def __init__(self, cls):
        self.cls = cls
        if not hasattr(self.cls, "_app"):
            setattr(self.cls, "_app", None)
            setattr(self.cls, "_state", AS.NOT_STARTED)
            setattr(self.cls, "_quiet", True)

    @property
    def app(self):
        return self.cls._app

    @app.setter
    def app(self, val):
        self.cls._app = val

    @property
    def state(self) -> AS:
        return self.cls._state

    @state.setter
    def state(self, val: AS):
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
        self.state = AS.NOT_STARTED
        self.__init__(hook)


class proxy_svc(common_svc):
    def __init__(self):
        super().__init__(proxy_svc)


MAIL_ERR_MSG = "Mail service is disabled or not yet configured!"
