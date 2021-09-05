"""
Main master handler for each user of Jaseci, serves as main interface between
between user and Jaseci
"""
from jaseci.element.master import master
from jaseci.api.logger_api import logger_api
from jaseci.api.config_api import config_api
from jaseci.api.global_api import global_api
from jaseci.api.super_api import super_api


class super_master(master, logger_api, config_api, global_api, super_api):
    """Master with admin APIs"""
