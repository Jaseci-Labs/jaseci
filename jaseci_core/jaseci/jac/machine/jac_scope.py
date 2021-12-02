"""
Variable scope manager for Jac

Utility for all runtime interaction with variables in different scopes
"""
from jaseci.actions.utils.global_actions import get_global_actions
from jaseci.jac.jac_set import jac_set
from jaseci.element.element import element
from jaseci.utils.utils import is_urn, logger
import uuid


class ctx_value():
    """A reference into the context dict that is common for elements"""

    def __init__(self, value=None, ctx=None, name=None):
        self.ctx = ctx
        self.name = name
        self.value = value if value is not None else ctx[name] \
            if ctx is not None and name is not None and \
            (type(name) == int or name in ctx.keys()) \
            else None

    def write(self):
        if(self.ctx is None or self.name is None):
            logger.error(
                f"No valid live variable! ctx: {self.ctx} name: {self.name}")
        self.ctx[self.name] = self.deep_element_deserialize(self.value)

    def deep_element_deserialize(self, value):
        """converts all elements to uuids in lists etc"""
        if (isinstance(value, element)):
            value = value.id.urn
        elif (isinstance(value, list)):
            for i in range(len(value)):
                value[i] = self.deep_element_deserialize(value[i])
        return value


class jac_scope():
    def __init__(self, parent, has_obj, action_sets):
        self.parent = parent
        self.local_scope = {}
        self.has_obj = has_obj if has_obj else self
        self.context = {}
        self.action_sets = [get_global_actions(parent)] + action_sets

    def add_actions(self, actions):
        self.action_sets.append(actions)

    def set_agent_refs(self, cur_node=None, cur_walker=None):
        from jaseci.graph.node import node
        from jaseci.actor.walker import walker
        if(cur_node):
            if(not isinstance(cur_node, node)):
                logger.error(f"Unable to set here, invalid type: {cur_node}")
            else:
                self.local_scope['here'] = cur_node.jid
        if(cur_walker):
            if(not isinstance(cur_walker, walker)):
                logger.error(
                    f"Unable to set visitor, invalid type: {cur_walker}")
            else:
                self.local_scope['visitor'] = cur_walker.jid

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
                if is_urn(found):
                    head_obj = self.parent._h.get_obj(
                        self.parent._m_id, uuid.UUID(found))
                    # head_obj.context['id'] = head_obj.jid
                    if (subname[1] in head_obj.context.keys() or
                            self.try_sync_to_arch(head_obj, subname[1])):
                        return ctx_value(ctx=head_obj.context, name=subname[1])
                else:
                    logger.error(f'Something went wrong with {found}')
                # other types in scope can go here
            # check if dotted var is builtin action (of walker)
            if (allow_read_only):
                for i in self.action_sets:
                    found = i.get_obj_by_name(
                        name, silent=True)
                    if(found):
                        return ctx_value(value=found)
        else:
            # check if var is in walker's context
            if(name in self.has_obj.context.keys()):
                return ctx_value(ctx=self.has_obj.context, name=name)
        return None

    def get_live_var(self, name, create_mode=False):
        """Returns live variable"""
        found = None
        # First look for variable in various locations
        if (name in self.local_scope.keys()):
            found = ctx_value(ctx=self.local_scope, name=name)
        else:
            found = self.find_live_attr(name)
        if (found is None):
            if(create_mode):
                self.local_scope[name] = None
                return ctx_value(ctx=self.local_scope, name=name)
            logger.error(f"Variable not defined - {name}")
            return None
        found.value = self.reference_to_value(found.value)
        return found

    def reference_to_value(self, val):
        """Reference to variables value"""
        if(is_urn(val)):
            val = self.parent._h.get_obj(self.parent._m_id, uuid.UUID(val))
        return val

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
