"""
Variable scope manager for Jac

Utility for all runtime interaction with variables in different scopes
"""
from jaseci.utils.id_list import IdList
from jaseci.jac.machine.jac_value import JacValue
from jaseci.actions.live_actions import get_global_actions

global_action_sets = None


class JacScope:
    def __init__(self, parent, has_obj, action_sets):
        self.parent = parent
        self.local_scope = {}
        self.has_obj = has_obj if has_obj else self
        self.context = {}
        self.action_sets = action_sets
        self.setup_actions()

    def setup_actions(self):
        global global_action_sets
        if global_action_sets is None:
            global_action_sets = self.group_actions(get_global_actions())
        allactions = []
        for i in self.action_sets:
            allactions += i.obj_list()
        self.action_sets = global_action_sets
        for i in allactions:
            self.add_action(i)

    def add_action(self, act):
        group = act.name.split(".")[0]
        if "." in act.name:
            if group not in self.action_sets.keys():
                self.action_sets[group] = {}
            action = act.name.split(".")[1]
            self.action_sets[group][action] = act
        else:
            self.action_sets[group] = act

    def group_actions(self, act_list):
        action_sets = {}
        for act in act_list:
            group = act.name.split(".")[0]
            if "." in act.name:
                if group not in action_sets.keys():
                    action_sets[group] = {}
                action = act.name.split(".")[1]
                action_sets[group][action] = act
            else:
                action_sets[group] = act
        return action_sets

    def set_agent_refs(self, cur_node, cur_walker):
        self.local_scope["here"] = cur_node
        self.local_scope["visitor"] = cur_walker

    def inherit_agent_refs(self, src_scope, src_node):  # used for calls of abilities
        self.local_scope["here"] = src_node
        self.local_scope["visitor"] = src_scope.local_scope["visitor"]

    def get_aganet_refs(self):
        return {
            "here": self.local_scope["here"],
            "visitor": self.local_scope["visitor"],
        }

    def find_live_attr(self, name, allow_read_only=True):
        """Finds binding for variable if not in standard scope"""
        # check if var is in walker's context
        if "context" in self.has_obj.__dict__ and name in self.has_obj.context.keys():
            return JacValue(self.parent, ctx=self.has_obj, name=name)
        elif name in self.action_sets.keys():
            return JacValue(self.parent, ctx=self.action_sets, name=name)
        return None

    def get_live_var(self, name, create_mode=False):
        """Returns live variable"""
        found = None
        # Lock for variable in various locations
        if name in self.local_scope.keys():
            found = JacValue(self.parent, ctx=self.local_scope, name=name)
        else:
            found = self.find_live_attr(name)
        if found is None and create_mode:
            self.local_scope[name] = None
            return JacValue(self.parent, ctx=self.local_scope, name=name)
        if found:
            return found
        return None
