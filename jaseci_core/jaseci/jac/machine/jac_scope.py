"""
Variable scope manager for Jac

Utility for all runtime interaction with variables in different scopes
"""
from jaseci.jac.machine.jac_value import JacValue
from jaseci.jsorc.live_actions import get_global_actions


class JacScope:
    def __init__(self, parent, name, has_obj=None, here=None, visitor=None):
        self.parent = parent
        self.name = name
        self.local_scope = {}
        self.has_obj = has_obj if has_obj else self
        self.context = {}
        self.action_sets = []
        self._start_time = 0  # For profiling
        self._total_time = 0  # For profiling
        self._cum_start_time = None
        self.set_refs(here, visitor)
        self.setup_actions()

    def setup_actions(self):
        allactions = []
        for i in self.action_sets:
            allactions += i.obj_list()
        self.action_sets = get_global_actions()
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

    def set_refs(self, here, visitor):
        self.local_scope["here"] = here
        self.local_scope["visitor"] = visitor
        self.action_sets = []
        if here:
            self.action_sets += [here.get_architype().get_all_abilities()]
        if visitor:
            self.action_sets += [visitor.get_architype().get_all_abilities()]

    def get_refs(self):
        return {
            "here": self.local_scope["here"],
            "visitor": self.local_scope["visitor"],
        }

    def here(self):
        return self.local_scope["here"]

    def visitor(self):
        return self.local_scope["visitor"]

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
