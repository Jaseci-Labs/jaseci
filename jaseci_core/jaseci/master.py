"""
Main master handler for each user of Jaseci, serves as main interface between
between user and Jaseci
"""

from jaseci.element import element
from jaseci.api.alias import alias_api
from jaseci.api.object import object_api
from jaseci.api.logger import logger_api
from jaseci.api.graph import graph_api
from jaseci.api.sentinel import sentinel_api
from jaseci.api.walker import walker_api
from jaseci.api.architype import architype_api
from jaseci.api.config import config_api
from jaseci.api.glob import global_api
from jaseci.api.general_interface import interface
from jaseci.api.master import master_api


class master(element, interface, master_api, alias_api, graph_api, object_api,
             sentinel_api, walker_api, architype_api):
    """Main class for master functions for user"""

    def __init__(self, *args, **kwargs):
        kwargs['m_id'] = None

        element.__init__(self, kind="Jaseci Master", *args, **kwargs)
        master_api.__init__(self)
        alias_api.__init__(self)
        config_api.__init__(self)
        graph_api.__init__(self)
        sentinel_api.__init__(self)

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        graph_api.destroy(self)
        sentinel_api.destroy(self)
        master_api.destroy(self)
        super().destroy()


class master_admin(master, logger_api, config_api, global_api):
    """Master with admin APIs"""
