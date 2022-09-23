"""
Action class for Jaseci

Each action has an id, name, timestamp and it's set of edges.
"""
from .item import Item
from jaseci.actions.live_actions import live_actions
from jaseci.jac.jac_set import JacSet
import inspect

# ACTION_PACKAGE = 'jaseci.actions.'


class Action(Item):
    """
    Action class for Jaseci

    preset_in_out holds a set of parameters in the form of lists of context
    objects that are to be used from whereever those contexts are attached
    e.g., (nodes, edges, walkers, etc). This is used by Jac's runtime
    engine to support preset actions in nodes
    access_list is used by walker to decide what to trigger
    """

    def __init__(self, preset_in_out=None, access_list=None, **kwargs):
        self.preset_in_out = preset_in_out  # Not using _ids convention
        self.access_list = access_list
        Item.__init__(self, **kwargs)

    def do_auto_conversions(self, args, func, params):
        """
        Automatically make conversions for jac to internal, e.g., list to jac_set
        """

        for i in args.annotations.keys():
            if args.annotations[i] == JacSet:
                idx = args.args.index(i)
                params[idx] = JacSet(in_list=params[idx])

    def trigger(self, param_list, scope, interp):
        """
        param_list should be passed as list of values to lib functions
        Also note that Jac stores preset_in_out as input/output list of hex
        ids since preset_in_out doesn't use _ids convention
        """
        func = live_actions[self.value]
        args = inspect.getfullargspec(func)
        self.do_auto_conversions(args, func, param_list)
        args = args[0] + args[4]
        if "meta" in args:
            result = func(
                *param_list,
                meta={
                    "m_id": scope.parent._m_id,
                    "h": scope.parent._h,
                    "scope": scope,
                    "interp": interp,
                }
            )
        else:
            result = func(*param_list)
        return result
