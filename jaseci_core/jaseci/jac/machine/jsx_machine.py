"""
The Jaseci Jac virtual machine for jsx bytecode
"""

from jaseci.jac.machine.machine_state import machine_state
from jaseci.jac.machine.jac_scope import jac_scope


class jsx_machine(machine_state):
    """Create 'bit switch' for jsx bytecode"""

    def __init__(self, jsx):
        self.PC = 0
        self.jsx = jsx

    def IDS_CLEAR(self, *args):
        """IDS_CLEAR op code"""
        self.get_ref(args[0]).remove_all()

    def IDS_ADD_OBJ(self, *args):
        """IDS_ADD_OBJ op code"""
        self.get_ref(args[0]).add_obj(self.get_ref(args[1]))

    def IDS_GET_LEN(self, *args):
        """IDS_GET_LEN op code"""
        self.set_ref(args[0], len(self.get_ref(args[1])))

    def PUSH_SCOPE_W(self, *args):
        """PUSH_SCOPE_W op code"""
        self.push_scope(
            jac_scope(
                parent=self,
                has_obj=self,
                action_sets=[self.activity_action_ids,
                             self.current_node.activity_action_ids]))

    def POP_SCOPE(self, *args):
        """POP_SCOPE op code"""
        self.pop_scope()

    def SET_LIVE_VAR(self, *args):
        """SET_LIVE_VAR op code"""
        self._jac_scope.set_live_var(
            name=args[0], value=self.get_ref(args[1]),
            md_index=args[2], jac_ast=None)

    def SET_REF_VAR(self, *args):
        """SET_REF_VAR op code"""
        self.set_ref(args[0], self.get_ref(args[1]))

    def SET_REF_VARI(self, *args):
        """SET_REF_VARI op code"""
        self.set_ref(args[0], args[1])

    def CREATE_CTX_VAR(self, *args):
        """CREATE_CTX_VAR op code"""
        obj = self.get_ref(args[0])
        var_name = args[1]
        var_val = self.get_ref(args[2])
        is_private = args[3]
        if (var_name not in obj.context.keys()):  # Runs has once per walk
            obj.context[var_name] = var_val
        if(is_private):
            if('_private' in obj.context.keys()):
                if(var_name not in obj.context['_private']):
                    obj.context['_private'].append(var_name)
            else:
                obj.context['_private'] = [var_name]

    def SET_ANCHOR(self, *args):
        """SET_ANCHOR op code"""
        obj = args[0]
        var_name = args[1]
        if('anchor' in dir(obj)):
            if(obj.anchor is None):
                obj.anchor = var_name

    def B_NEQ(self, *args):
        """B_NEQ op code"""
        if(self.get_ref(args[0]) != self.get_ref(args[1])):
            self.PC += args[2]

    def B_NEQI(self, *args):
        """B_NEQI op code"""
        if(self.get_ref(args[0]) != args[1]):
            self.PC += args[2]

    def B_NIT(self, *args):
        """B_NIT op code"""
        if(not isinstance(self.get_ref(args[0]), args[1])):
            self.PC += args[2]

    def B_A(self, *args):
        """B_NEQ op code"""
        self.PC += args[0]

    def PLUS(self, *args):
        """B_NEQ op code"""
        self.set_ref(self.get_ref(args[0]), self.get_ref(
            args[1]) + self.get_ref(args[2]))

    def END(self, *args):
        """END op code"""
        self.PC = len(self.jsx)

    def get_ref(self, r):
        """Access ref from instruction"""

    def set_ref(self, r, val):
        """Access ref from instruction"""
