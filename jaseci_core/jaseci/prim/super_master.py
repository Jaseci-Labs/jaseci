"""
Super master handler for each user of Jaseci, serves as main interface between
between user and Jaseci
"""

from jaseci.extens.api.jsorc_api import JsOrcApi
from jaseci.prim.master import Master
from jaseci.extens.api.logger_api import LoggerApi
from jaseci.extens.api.config_api import ConfigApi
from jaseci.extens.api.global_api import GlobalApi
from jaseci.extens.api.super_api import SuperApi
from jaseci.extens.api.actions_api import ActionsApi
from jaseci.extens.api.prometheus_api import PrometheusApi
from jaseci.jsorc.jsorc import JsOrc


@JsOrc.context(name="super_master")
class SuperMaster(
    Master,
    LoggerApi,
    ActionsApi,
    ConfigApi,
    GlobalApi,
    SuperApi,
    JsOrcApi,
    PrometheusApi,
):
    """Master with admin APIs"""

    def __init__(self, *args, **kwargs):
        Master.__init__(self, *args, **kwargs)
