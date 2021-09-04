"""
Main master handler for each user of Jaseci, serves as main interface between
between user and Jaseci
"""

from jaseci.element import element
from jaseci.api.alias_api import alias_api
from jaseci.api.object_api import object_api
from jaseci.api.logger_api import logger_api
from jaseci.api.graph_api import graph_api
from jaseci.api.sentinel_api import sentinel_api
from jaseci.api.walker_api import walker_api
from jaseci.api.architype_api import architype_api
from jaseci.api.config_api import config_api
from jaseci.api.global_api import global_api
from jaseci.api.interface import interface
from jaseci.api.master_api import master_api
from jaseci.api.super_api import super_api


class master(element, interface, master_api, alias_api, graph_api, object_api,
             sentinel_api, walker_api, architype_api):
    """Main class for master functions for user"""

    def __init__(self, head_master=None, *args, **kwargs):
        kwargs['m_id'] = None

        element.__init__(self, kind="Jaseci Master", *args, **kwargs)
        master_api.__init__(self, head_master)
        alias_api.__init__(self)
        config_api.__init__(self)
        graph_api.__init__(self)
        sentinel_api.__init__(self)

    def spawn_master(self, name: str):
        """Helper to create sub masters"""
        new_m = master(h=self._h, name=name)
        new_m.head_master_id = self.jid
        new_m.give_access(self)
        return new_m

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        graph_api.destroy(self)
        sentinel_api.destroy(self)
        master_api.destroy(self)
        super().destroy()


class super_master(master, logger_api, config_api, global_api, super_api):
    """Master with admin APIs"""

    def spawn_super(self, name: str):
        """Helper to create sub masters"""
        new_m = super_master(h=self._h, name=name)
        new_m.head_master_id = self.jid
        new_m.give_access(self)
        return new_m
