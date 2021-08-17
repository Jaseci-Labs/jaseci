"""
Walker class for Jaseci

Each walker has an id, name, timestamp and it's owner sentinel.
TODO: Perhaps  I should have walker state (context ids) in mem only with
default hooks to save db read/writes
"""

from jaseci.utils.utils import logger
from jaseci.element import element
from jaseci.utils.obj_mixins import anchored
from jaseci.utils.id_list import id_list
from jaseci.jac.interpreter.walker_interp import walker_interp
from jaseci.utils.jac_code import jac_code
import uuid


class walker(element, jac_code, walker_interp, anchored):
    """Walker class for Jaseci"""

    def __init__(self, code_ir=None, *args, **kwargs):
        self.activity_action_ids = id_list(self)
        self.context = {}
        self.profile = {}
        # Process state
        self.current_node_id = None
        self.next_node_ids = id_list(self)
        self.ignore_node_ids = id_list(self)
        self.destroy_node_ids = id_list(self)
        self.current_step = 0
        self.in_entry_exit = False
        self.step_limit = 10000
        anchored.__init__(self)
        element.__init__(self, *args, **kwargs)
        jac_code.__init__(self, code_ir=code_ir)
        walker_interp.__init__(self)

    @ property
    def current_node(self):
        if(not self.current_node_id):
            return None
        else:
            return self._h.get_obj(uuid.UUID(self.current_node_id))

    @ current_node.setter
    def current_node(self, obj):
        if(obj):
            self.current_node_id = obj.id.urn
        else:
            self.current_node_id = None

    def step(self):
        """
        Take single step through program
        if no ast provided, will be generated from code
        """
        if(not self.next_node_ids):
            logger.debug(str(f'Walker {self.name} is disengaged'))
            return False
        if(self.current_step > self.step_limit):
            logger.error(
                str(f'Walker {self.name} walked too many steps ' +
                    f'- {self.step_limit}')
            )
            return False

        self.current_node = self.next_node_ids.pop_first_obj()
        self.run_walker(jac_ast=self._jac_ast)
        self.log_history('visited', self.current_node.id)
        self.current_step += 1
        self.profile['steps'] = self.current_step
        if (self._stopped == 'skip'):
            self._stopped = None
        if(self.next_node_ids):
            logger.debug(str(f'Step complete, Walker {self.name} next node: ' +
                             f'- {self.next_node_ids.first_obj()}'))
            return self.next_node_ids.first_obj()
        else:
            logger.debug(
                str(f'Final step of walker {self.name} complete' +
                    f'- disengaging from {self.current_node}'))
            for i in self.destroy_node_ids.obj_list():
                i.destroy()
            return True

    def prime(self, start_node, prime_ctx=None):
        """Place walker on node and get ready to step step"""
        self.clear_state()
        self.next_node_ids.add_obj(start_node)
        if (prime_ctx):
            for i in prime_ctx.keys():
                self.context[str(i)] = prime_ctx[i]
        self.profile['steps'] = self.current_step
        logger.debug(str(f'Walker {self.name} primed - {start_node}'))

    def run(self, start_node=None, prime_ctx=None):
        """Executes Walker to completion"""
        if(start_node):
            self.prime(start_node, prime_ctx)

        while self.step():
            pass
        self.save()

        if(not self.report):
            logger.debug(
                str(f'Walker {self.name} did not arrive at report state')
            )
        return self.report

    def log_history(self, name, value):
        """Helper function for logging history of walker's activities"""
        if (isinstance(value, element)):
            value = {'type': value.j_type, 'id': value.id.urn}
        if (isinstance(value, uuid.UUID)):
            value = value.urn
        if name in self.profile.keys():
            self.profile[name].append(value)
        else:
            self.profile[name] = [value]

    def clear_state(self):
        """Clears walker state after report"""
        self.profile = {}
        self.current_step = 0
        self.next_node_ids.remove_all()
        self.ignore_node_ids.remove_all()
        self.destroy_node_ids.remove_all()
        self.current_node = None
        self.activity_action_ids.destroy_all()
        self.context = {}
        self.reset()

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        for i in self.activity_action_ids.obj_list():
            i.destroy()
        super().destroy()
