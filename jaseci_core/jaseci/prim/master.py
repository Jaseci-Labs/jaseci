"""
Main master handler for each user of Jaseci, serves as main interface between
between user and Jaseci
"""

from jaseci.prim.element import Element
from jaseci.extens.api.alias_api import AliasAPI
from jaseci.extens.api.object_api import ObjectApi
from jaseci.extens.api.graph_api import GraphApi
from jaseci.extens.api.sentinel_api import SentinelApi
from jaseci.extens.api.walker_api import WalkerApi
from jaseci.extens.api.architype_api import ArchitypeApi
from jaseci.extens.api.config_api import ConfigApi
from jaseci.extens.api.interface import Interface
from jaseci.extens.api.master_api import MasterApi
from jaseci.extens.api.jac_api import JacApi
from jaseci.extens.api.user_api import UserApi
from jaseci.extens.api.queue_api import QueueApi
from jaseci.extens.api.webhook_api import WebhookApi
from jaseci.jsorc.jsorc import JsOrc


@JsOrc.context(name="master")
class Master(
    Element,
    Interface,
    MasterApi,
    AliasAPI,
    GraphApi,
    ObjectApi,
    SentinelApi,
    WalkerApi,
    ArchitypeApi,
    JacApi,
    UserApi,
    QueueApi,
    WebhookApi,
):
    """Main class for master functions for user"""

    def __init__(self, head_master=None, *args, **kwargs):
        kwargs["m_id"] = None

        Element.__init__(self, kind="Jaseci Master", *args, **kwargs)
        MasterApi.__init__(self, head_master)
        AliasAPI.__init__(self)
        ConfigApi.__init__(self)
        ObjectApi.__init__(self)
        GraphApi.__init__(self)
        WalkerApi.__init__(self)
        SentinelApi.__init__(self)
        Interface.__init__(self)

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        GraphApi.destroy(self)
        SentinelApi.destroy(self)
        MasterApi.destroy(self)
        WalkerApi.destroy(self)
        super().destroy()
