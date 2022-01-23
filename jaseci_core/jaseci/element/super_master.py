"""
Super master handler for each user of Jaseci, serves as main interface between
between user and Jaseci
"""

from jaseci.element.master import master
from jaseci.api.logger_api import logger_api
from jaseci.api.config_api import config_api
from jaseci.api.global_api import global_api
from jaseci.api.super_api import super_api
from jaseci.api.stripe_api import stripe_api
from jaseci.api.actions_api import actions_api


class super_master(master, logger_api, actions_api, config_api, global_api,
                   super_api, stripe_api):
    """Master with admin APIs"""

    def __init__(self, *args, **kwargs):
        master.__init__(self, *args, **kwargs)
        stripe_api.__init__(self)
