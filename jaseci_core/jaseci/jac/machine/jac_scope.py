"""
Variable scope manager for Jac

Utility for all runtime interaction with variables in different scopes
"""
from jaseci.utils.id_list import id_list
from jaseci.jac.machine.jac_value import jac_value
from jaseci.jac.machine.jac_value import jac_elem_wrap


class jac_scope():
    def __init__(self, parent, has_obj, action_sets):
        self.parent = parent
        self.local_scope = {}
        self.has_obj = has_obj if has_obj else self
        self.context = {}
        self.action_sets = action_sets + \
            [id_list(parent, in_list=parent._h.global_action_list)]
        self.setup_actions()

    def setup_actions(self):
        allactions = []
        for i in self.action_sets:
            allactions += i.obj_list()
        self.action_sets = {}
        for i in allactions:
            self.add_action(i)

    def add_action(self, act):
        group = act.name.split('.')[0]
        if '.' in act.name:
            if(group not in self.action_sets.keys()):
                self.action_sets[group] = {}
            action = act.name.split('.')[1]
            self.action_sets[group][action] = act
        else:
            self.action_sets[group] = act

    def set_agent_refs(self, cur_node, cur_walker):
        self.local_scope['here'] = jac_elem_wrap(cur_node)
        self.local_scope['visitor'] = jac_elem_wrap(cur_walker)

    def inherit_agent_refs(self, src_scope):
        self.local_scope['here'] = src_scope.local_scope['here']
        self.local_scope['visitor'] = src_scope.local_scope['visitor']

    def get_aganet_refs(self):
        return {
            'here': self.local_scope['here'],
            'visitor': self.local_scope['visitor']
        }

    def find_live_attr(self, name, allow_read_only=True):
        """Finds binding for variable if not in standard scope"""
        # check if var is in walker's context
        if(name in self.has_obj.context.keys()):
            return jac_value(self.parent,
                             ctx=self.has_obj,
                             name=name)
        elif(name in self.action_sets.keys()):
            return jac_value(self.parent,
                             ctx=self.action_sets,
                             name=name)
        return None

    def get_live_var(self, name, create_mode=False):
        """Returns live variable"""
        found = None
        # Lock for variable in various locations
        if (name in self.local_scope.keys()):
            found = jac_value(self.parent,
                              ctx=self.local_scope, name=name)
        else:
            found = self.find_live_attr(name)
        if (found is None and create_mode):
            self.local_scope[name] = None
            return jac_value(self.parent, ctx=self.local_scope, name=name)
        if(found):
            found.unwrap()
            return found
        return None
