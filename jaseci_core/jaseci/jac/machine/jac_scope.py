"""
Variable scope manager for Jac

Utility for all runtime interaction with variables in different scopes
"""
from jaseci.actions.utils.global_actions import global_action_ids
from jaseci.jac.jac_set import jac_set
from jaseci.element import element
from jaseci.utils.utils import is_urn
import uuid


class ctx_value():
    """A reference into the context dict that is common for elements"""

    def __init__(self, obj, name):
        self.obj = obj
        self.name = name


class jac_scope():
    def __init__(self, parent, has_obj, action_sets):
        self.parent = parent
        self.local_scope = {}
        self.has_obj = has_obj if has_obj else self
        self.context = {}
        self.action_sets = [global_action_ids] + action_sets

    def add_actions(self, actions):
        self.action_sets.append(actions)

    def find_live_attr(self, name, allow_read_only=True):
        """Finds binding for variable if not in standard scope"""
        if '.' in name:  # Handles node attr references
            subname = name.split('.')
            found = None
            # check if dotted var in current scope (node, etc)
            if subname[0] in self.local_scope.keys():
                found = self.local_scope[subname[0]]
            # check if dotted var in walkers context (node, etc)
            else:
                if(subname[0] in self.has_obj.context.keys()):
                    found = self.has_obj.context[subname[0]]
            if(found is not None):
                # return node if it's a node
                if is_urn(found):
                    head_obj = self.parent._h.get_obj(
                        self.parent, uuid.UUID(found))
                    # head_obj.context['id'] = head_obj.jid
                    if (subname[1] in head_obj.context.keys() or
                            self.try_sync_to_arch(head_obj, subname[1])):
                        return ctx_value(head_obj, subname[1])
                # other types in scope can go here
            # check if dotted var is builtin action (of walker)
            if (allow_read_only):
                for i in self.action_sets:
                    found = i.get_obj_by_name(
                        name, silent=True)
                    if(found):
                        return found
        else:
            # check if var is in walker's context
            if(name in self.has_obj.context.keys()):
                return ctx_value(self.has_obj, name)
        return None

    def get_live_var(self, name, jac_ast):
        """Returns live variable, to support builtins in the future"""
        found = None
        # First look for variable in various locations
        if (name in self.local_scope.keys()):
            found = self.local_scope[name]
        else:
            found = self.find_live_attr(name)
        if (found is None):
            self.parent.rt_error(f"Variable not defined - {name}", jac_ast)
            return None
        return self.reference_to_value(found)

    def reference_to_value(self, val):
        """Reference to variables value"""
        while (is_urn(val) or type(val) == ctx_value):
            if(is_urn(val)):
                val = self.parent._h.get_obj(self.parent, uuid.UUID(val))
            if (type(val) == ctx_value):
                val = val.obj.context[val.name]
        return val

    def set_live_var(self, name, value, md_index, jac_ast):
        """Returns live variable, to support builtins in the future"""
        value = self.deep_element_deserialize(value)
        if name not in self.local_scope.keys():
            look = self.find_live_attr(name, allow_read_only=False)
            if (look):
                if(not md_index):
                    look.obj.context[look.name] = value
                else:
                    self.set_array_live_var(look.obj.context[look.name],
                                            value, md_index, jac_ast)
                return
            elif '.' in name:
                self.parent.rt_error(
                    f"Arbitrary dotted names not allowed - {name}", jac_ast)
                return
        if(not md_index):
            self.local_scope[name] = value
        else:
            self.set_array_live_var(self.local_scope[name], value,
                                    md_index, jac_ast)

    def set_array_live_var(self, item, value, md_index, jac_ast):
        """
        Helper for setting array values
        md_index list of [1, 2, 3, 4] corresponds to [1][2][3][4] in jac code
        """
        for i in md_index[:-1]:
            self.check_index_in_bounds(i, item, jac_ast)
            item = item[i]
        self.check_index_in_bounds(md_index[-1], item, jac_ast)
        item[md_index[-1]] = value

    def check_index_in_bounds(self, index, item, jac_ast):
        if (isinstance(index, int) and index >= len(item)):
            self.parent.rt_error(
                f"Array index {index} out of bounds!", jac_ast)
            return False
        elif (isinstance(index, str) and index not in item.keys()):
            from jaseci.utils.utils import logger
            logger.error(f'{item}')
            self.parent.rt_error(f"Object has no member {index}!", jac_ast)
            return False
        return True

    def try_sync_to_arch(self, obj, varname):
        """Checks if latest Architype has variable"""
        # TODO: Only supports node types
        # from jaseci.utils.utils import logger
        # logger.info(f'{obj}')
        if (varname in self.parent.parent().arch_ids.get_obj_by_name(
                obj.name, kind='node').run().context.keys()):
            obj.context[varname] = None
            return True
        return False

    def report_deep_serialize(self, report):
        """Performs JSON serialization for lists of lists of lists etc"""
        if (isinstance(report, element)):
            report = report.serialize()
        elif (isinstance(report, jac_set)):
            blobs = []
            for i in report.obj_list():
                blobs.append(i.serialize())
            report = blobs
        elif (isinstance(report, list)):
            blobs = []
            for i in report:
                blobs.append(self.report_deep_serialize(i))
            report = blobs
        return report

    def deep_element_deserialize(self, value):
        """converts all elements to uuids in lists etc"""
        if (isinstance(value, element)):
            value = value.id.urn
        elif (isinstance(value, list)):
            for i in range(len(value)):
                value[i] = self.deep_element_deserialize(value[i])
        return value
