"""
Sentinel class for Jaseci

Each sentinel has an id, name, timestamp and it's set of walkers.
"""
from core.element import element
from core.utils.utils import logger
from core.utils.id_list import id_list
from core.jac.ast import ast
from core.jac.sentinel_machine import sentinel_machine


class sentinel(element, sentinel_machine):
    """
    Sentinel class for Jaseci

    is_active is used to signify whether sentinel is ready to run walkers, i.e,
    register_code succeeded
    """

    def __init__(self, code='', *args, **kwargs):
        self.code = code
        self.is_active = False
        self.arch_ids = id_list(self)
        self.walker_ids = id_list(self)
        self.live_walker_ids = id_list(self)
        element.__init__(self, *args, **kwargs)
        sentinel_machine.__init__(self)

    def reset(self):
        """Resets state of sentinel and unregister's code"""
        self.is_active = False
        self.arch_ids.destroy_all()
        self.walker_ids.destroy_all()
        sentinel_machine.reset(self)

    def register_code(self, text=None, init_ctx=None):
        """Registers a program written in Jac"""
        logger.info(str(f'{self.name}: Registering Jac code...'))
        self.reset()
        self.code = text if text else self.code
        tree = ast(jac_text=self.code)

        if(tree.parse_errors):
            logger.error(str(f'{self.name}: Invalid syntax in Jac code!'))
            for i in tree.parse_errors:
                logger.error(i)
            return self.is_active  # is False due to .reset()

        self.run_start(tree)

        if(self.runtime_errors):
            logger.error(
                str(f'{self.name}: Runtime problem registering code!')
            )
        elif(not self.walker_ids and not self.arch_ids):
            logger.error(
                str(f'{self.name}: No walkers nor architypes created!')
            )
        else:
            self.is_active = True

        if(self.is_active):
            logger.info(str(f'{self.name}: Successfully registered code'))
        else:
            logger.info(str(f'{self.name}: Code not registered'))

        return self.is_active

    def spawn(self, name):
        """Spawns a new walker from registered walkers"""
        src_walk = self.walker_ids.get_obj_by_name(name)
        if (not src_walk):
            logger.error(
                str(f'{self.name}: Unable to spawn walker {name}!')
            )
            self.is_active = False
            self.save()
            return None
        new_walk = src_walk.duplicate(persist_dup=False)
        new_walk._jac_ast = src_walk._jac_ast
        self.live_walker_ids.add_obj(new_walk)
        return new_walk

    def unspawn(self, obj):
        """Destroys spawned walker based on ID"""
        self.live_walker_ids.destroy_obj(obj)

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        for i in self.arch_ids.obj_list() + \
                self.walker_ids.obj_list() + self.live_walker_ids.obj_list():
            self._h.get_obj(i).destroy()
        super().destroy()
