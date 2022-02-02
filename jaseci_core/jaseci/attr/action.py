"""
Action class for Jaseci

Each action has an id, name, timestamp and it's set of edges.
"""
from .item import item
from jaseci.actions.live_actions import live_actions
# ACTION_PACKAGE = 'jaseci.actions.'


class action(item):
    """
    Action class for Jaseci

    preset_in_out holds a set of parameters in the form of lists of context
    objects that are to be used from whereever those contexts are attached
    e.g., (nodes, edges, walkers, etc). This is used by Jac's runtime
    engine to support preset actions in nodes
    access_list is used by walker to decide what to trigger
    """

    def __init__(self, preset_in_out=None, access_list=None,
                 *args, **kwargs):
        self.preset_in_out = preset_in_out  # Not using _ids convention
        self.access_list = access_list
        super().__init__(*args, **kwargs)

    def trigger(self, param_list, scope):
        """
        param_list should be passed as list of values to lib functions
        Also note that Jac stores preset_in_out as input/output list of hex
        ids since preset_in_out doesn't use _ids convention
        """
        # result = getattr(
        #     importlib.import_module(
        #         ACTION_PACKAGE+self.value[0].split('.')[-1]),
        #     self.value[1]
        # )(param_list, meta={'m_id': scope.parent._m_id,
        #                     'h': scope.parent._h, 'scope': scope})
        result = live_actions[
            self.value](*param_list,
                        meta={'m_id': scope.parent._m_id,
                              'h': scope.parent._h, 'scope': scope})
        return result
