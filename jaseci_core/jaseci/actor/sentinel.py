"""
Sentinel class for Jaseci

Each sentinel has an id, name, timestamp and it's set of walkers.
"""
from jaseci.element import element
from jaseci.utils.utils import logger
from jaseci.utils.id_list import id_list
from jaseci.jac.ir.jac_code import jac_code
from jaseci.jac.interpreter.sentinel_interp import sentinel_interp


class sentinel(element, jac_code, sentinel_interp):
    """
    Sentinel class for Jaseci

    is_active is used to signify whether sentinel is ready to run walkers, i.e,
    register_code succeeded
    """

    def __init__(self, *args, **kwargs):
        self.version = None
        self.arch_ids = id_list(self)
        self.walker_ids = id_list(self)
        element.__init__(self, *args, **kwargs)
        jac_code.__init__(self, code_ir=None)
        sentinel_interp.__init__(self)

    def reset(self):
        """Resets state of sentinel and unregister's code"""
        self.arch_ids.destroy_all()
        self.walker_ids.destroy_all()
        jac_code.reset(self)
        sentinel_interp.reset(self)

    def refresh(self):
        super().refresh()
        self.ir_load()

    def register_code(self, text):
        """
        Registers a program (set of walkers and architypes) written in Jac
        """
        self.reset()
        self.register(text)
        if(self.is_active):
            self.ir_load()
        return self.is_active

    def ir_load(self):
        """
        Load walkers and architypes from IR
        """
        self.run_start(self._jac_ast)

        if(self.runtime_errors):
            logger.error(
                str(f'{self.name}: Runtime problem processing sentinel!')
            )
            self.is_active = False
        elif(not self.walker_ids and not self.arch_ids):
            logger.error(
                str(f'{self.name}: No walkers nor architypes created!')
            )
            self.is_active = False
        return self.is_active

    def register_walker(self, code):
        """Adds a walker based on jac code"""
        tree = self.parse_jac(code, start_rule='walker')
        if(not tree):
            return None
        return self.load_walker(tree)

    def register_architype(self, code):
        """Adds a walker based on jac code"""
        tree = self.parse_jac(code, start_rule='architype')
        if(not tree):
            return None
        return self.load_architype(tree)

    def spawn_walker(self, name):
        """
        Spawns a new walker from registered walkers and adds to
        live walkers
        """
        src_walk = self.walker_ids.get_obj_by_name(name)
        if (not src_walk):
            logger.error(
                str(f'{self.name}: Unable to spawn walker {name}!')
            )
            return None
        new_walk = src_walk.duplicate()
        new_walk._jac_ast = src_walk._jac_ast
        return new_walk

    def spawn_architype(self, name, kind=None):
        """
        Spawns a new architype from registered architypes and adds to
        live walkers
        """
        src_arch = self.arch_ids.get_obj_by_name(name, kind=kind)
        if (not src_arch):
            logger.error(
                str(f'{self.name}: Unable to spawn architype {[name, kind]}!')
            )
            return None
        # No need to dup architypes as they are stateless generators
        return src_arch

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        for i in self.arch_ids.obj_list() + \
                self.walker_ids.obj_list():
            i.destroy()
        super().destroy()
