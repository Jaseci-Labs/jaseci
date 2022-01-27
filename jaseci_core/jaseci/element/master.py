"""
Main master handler for each user of Jaseci, serves as main interface between
between user and Jaseci
"""

from jaseci.element.element import element
from jaseci.api.alias_api import alias_api
from jaseci.api.object_api import object_api
from jaseci.api.graph_api import graph_api
from jaseci.api.sentinel_api import sentinel_api
from jaseci.api.walker_api import walker_api
from jaseci.api.architype_api import architype_api
from jaseci.api.config_api import config_api
from jaseci.api.interface import interface
from jaseci.api.master_api import master_api
from jaseci.api.jac_api import jac_api


class master(element, interface, master_api, alias_api,
             graph_api, object_api, sentinel_api, walker_api,
             architype_api, jac_api):
    """Main class for master functions for user"""

    def __init__(self, head_master=None, *args, **kwargs):
        kwargs['m_id'] = None

        element.__init__(self, kind="Jaseci Master", *args, **kwargs)
        master_api.__init__(self, head_master)
        alias_api.__init__(self)
        config_api.__init__(self)
        graph_api.__init__(self)
        walker_api.__init__(self)
        sentinel_api.__init__(self)
        interface.__init__(self)

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        graph_api.destroy(self)
        sentinel_api.destroy(self)
        master_api.destroy(self)
        walker_api.destroy(self)
        super().destroy()
