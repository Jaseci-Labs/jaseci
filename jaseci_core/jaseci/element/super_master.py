"""
Super master handler for each user of Jaseci, serves as main interface between
between user and Jaseci
"""

from jaseci.element.master import Master
from jaseci.api.logger_api import LoggerApi
from jaseci.api.config_api import ConfigApi
from jaseci.api.global_api import GlobalApi
from jaseci.api.super_api import SuperApi
from jaseci.api.actions_api import ActionsApi


class SuperMaster(Master, LoggerApi, ActionsApi, ConfigApi, GlobalApi, SuperApi):
    """Master with admin APIs"""

    def __init__(self, *args, **kwargs):
        Master.__init__(self, *args, **kwargs)
