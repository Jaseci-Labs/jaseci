"""
Variable scope manager for Jac

Utility for all runtime interaction with variables in different scopes
"""
from jaseci.actions.utils.global_actions import get_global_actions
from jaseci.element.element import element
from jaseci.utils.utils import is_urn, logger
import uuid


class JAC_TYPE:
    NULL = 'null'
    TRUE = 'true'
    FALSE = 'false'


class ctx_value():
    """A reference into the context dict that is common for elements"""

    def __init__(self, parent, value=None, ctx=None, name=None):
        self.parent = parent
        self.ctx = ctx
        self.name = name
        self.value = value if value is not None else ctx[name] \
            if ctx is not None and name is not None and \
            (type(name) == int or name in ctx.keys()) \
            else None

    def write(self):
        if(self.ctx is None or self.name is None):
            logger.critical(
                f"No valid live variable! ctx: {self.ctx} name: {self.name}")
        self.ctx[self.name] = self.wrap()

    def wrap(self, serialize_mode=False):
        "Caller for recursive wrap"
        return self.wrap_value(self.value, serialize_mode)

    def unwrap(self):
        "Caller for recursive unwrap"
        return self.unwrap_value(self.value)

    def wrap_value(self, val, serialize_mode):
        """converts all elements to uuids in lists etc"""
        val = self.jac_type_wrap(val)
        if (isinstance(val, element)):
            if(serialize_mode):
                val = val.serialize()
            else:
                val = val.id.urn
        elif (isinstance(val, list)):
            for i in range(len(val)):
                val[i] = self.wrap_value(val[i], serialize_mode)
        elif (isinstance(val, dict)):
            for i in val.keys():
                val[i] = self.wrap_value(val[i], serialize_mode)
        return val

    def unwrap_value(self, val):
        """Reference to variables value"""
        val = self.jac_type_unwrap(val)
        if(is_urn(val)):
            val = self.parent._h.get_obj(self.parent._m_id, uuid.UUID(val))
        elif (isinstance(val, list)):
            for i in range(len(val)):
                val[i] = self.unwrap_value(val[i])
        elif (isinstance(val, dict)):
            for i in val.keys():
                val[i] = self.unwrap_value(val[i])
        return val

    def jac_type_wrap(self, val):
        if (type(val) == bool):
            if (val):
                val = JAC_TYPE.TRUE
            else:
                val = JAC_TYPE.FALSE
        elif(val is None):
            val = JAC_TYPE.NULL
        return val

    def jac_type_unwrap(self, val):
        if (val == JAC_TYPE.TRUE):
            val = True
        elif(val == JAC_TYPE.FALSE):
            val = False
        elif(val == JAC_TYPE.NULL):
            val = None
        return val


class jac_scope():
    def __init__(self, parent, has_obj, action_sets):
        self.parent = parent
        self.local_scope = {}
        self.has_obj = has_obj if has_obj else self
        self.context = {}
        self.action_sets = [get_global_actions(parent)] + action_sets

    def add_actions(self, actions):
        self.action_sets.append(actions)

    def set_agent_refs(self, cur_node, cur_walker):
        self.local_scope['here'] = cur_node.jid
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
                        return ctx_value(parent=self.parent, ctx=head_obj.context, name=subname[1])
                else:
                    logger.error(f'Something went wrong with {found}')
                # other types in scope can go here
            # check if dotted var is builtin action (of walker)
            if (allow_read_only):
                for i in self.action_sets:
                    found = i.get_obj_by_name(
                        name, silent=True)
                    if(found):
                        return ctx_value(parent=self.parent, value=found)
        else:
            # check if var is in walker's context
            if(name in self.has_obj.context.keys()):
                return ctx_value(parent=self.parent, ctx=self.has_obj.context, name=name)
        return None

    def get_live_var(self, name, create_mode=False):
        """Returns live variable"""
        found = None
        # Lock for variable in various locations
        if (name in self.local_scope.keys()):
            found = ctx_value(parent=self.parent,
                              ctx=self.local_scope, name=name)
        else:
            found = self.find_live_attr(name)
        if (found is None and create_mode):
            self.local_scope[name] = None
            return ctx_value(parent=self.parent, ctx=self.local_scope, name=name)
        if(found):
            found.value = found.unwrap()
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
