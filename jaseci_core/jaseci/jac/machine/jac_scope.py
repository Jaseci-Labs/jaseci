"""
Variable scope manager for Jac

Utility for all runtime interaction with variables in different scopes
"""
from jaseci.actions.utils.global_actions import get_global_actions
from jaseci.jac.machine.jac_value import jac_value, is_jac_elem
from jaseci.jac.machine.jac_value import jac_elem_wrap, jac_elem_unwrap
from jaseci.utils.utils import logger


class jac_scope():
    def __init__(self, parent, has_obj, action_sets):
        self.parent = parent
        self.local_scope = {}
        self.has_obj = has_obj if has_obj else self
        self.context = {}
        self.action_sets = [get_global_actions(parent)] + action_sets
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

    def find_live_attr(self, name, allow_read_only=True):
        """Finds binding for variable if not in standard scope"""
        if '.' in name:  # Handles node attr references
            subname = name.split('.')
            found = None
            # check if dotted var in current scope (node, etc)
            if subname[0] in self.local_scope.keys():
                found = self.local_scope[subname[0]]
            # check if dotted var in walkers context (node, etc)
            elif(subname[0] in self.has_obj.context.keys()):
                found = self.has_obj.context[subname[0]]
            if(found is not None):
                # return node if it's a node
                if is_jac_elem(found):
                    head_obj = jac_elem_unwrap(found, self.parent)
                    # head_obj.context['id'] = head_obj.jid
                    if (subname[1] in head_obj.context.keys() or
                            self.try_sync_to_arch(head_obj, subname[1])):
                        return jac_value(self.parent,
                                         ctx=head_obj.context,
                                         name=subname[1])
                else:
                    logger.error(
                        f'Something went wrong with {found} {subname}')
                # other types in scope can go here
            # check if dotted var is builtin action (of walker)
            if (allow_read_only):
                for i in self.action_sets:
                    found = i.get_obj_by_name(
                        name, silent=True)
                    if(found):
                        return jac_value(self.parent, value=found)
        else:
            # check if var is in walker's context
            if(name in self.has_obj.context.keys()):
                return jac_value(self.parent,
                                 ctx=self.has_obj.context,
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

    def try_sync_to_arch(self, obj, varname):
        """Checks if latest Architype has variable"""
        # TODO: Only supports node types
        # from jaseci.utils.utils import logger
        # logger.info(f'{obj}')
        if(not obj.j_type == 'node' and not obj.j_type == 'edge'):
            return False
        if (varname in self.parent.parent().run_architype(
                obj.name, kind='node', caller=obj).context.keys()):
            obj.context[varname] = None
            return True
        return False
