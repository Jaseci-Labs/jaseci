"""
Main master handler for each user of Jaseci, serves as main interface between
between user and Jaseci
"""

from jaseci.element.element import Element
from jaseci.api.alias_api import AliasAPI
from jaseci.api.object_api import ObjectApi
from jaseci.api.graph_api import GraphApi
from jaseci.api.sentinel_api import SentinelApi
from jaseci.api.walker_api import WalkerApi
from jaseci.api.architype_api import ArchitypeApi
from jaseci.api.config_api import ConfigApi
from jaseci.api.interface import Interface
from jaseci.api.master_api import MasterApi
from jaseci.api.jac_api import JacApi
from jaseci.api.user_api import UserApi
from jaseci.api.queue_api import QueueApi


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
