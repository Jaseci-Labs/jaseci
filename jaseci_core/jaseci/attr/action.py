"""
Action class for Jaseci

Each action has an id, name, timestamp and it's set of edges.
"""
from .item import item
import importlib

ACTION_PACKAGE = 'jaseci.actions.'


class action(item):
    """
    Action class for Jaseci

    preset_in_out holds a set of parameters in the form of lists of context
    objects that are to be used from whereever those contexts are attached
    e.g., (nodes, edges, walkers, etc). This is used by Jac's runtime
    engine to support preset actions in nodes
    """

    def __init__(self, preset_in_out=None, is_lib=True, *args, **kwargs):
        self.preset_in_out = preset_in_out  # Not using _ids convention
        self.is_lib = is_lib
        super().__init__(*args, **kwargs)

    def trigger(self, param_list):
        """
        param_list should be passed as list of values to lib functions
        Also note that Jac stores preset_in_out as input/output list of hex
        ids since preset_in_out doesn't use _ids convention
        """
        result = getattr(
            importlib.import_module(
                ACTION_PACKAGE+self.value[0].split('.')[-1]),
            self.value[1]
        )(param_list, meta={'m_id': self._m_id, 'h': self._h})
        return result
