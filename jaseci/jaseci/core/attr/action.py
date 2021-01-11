"""
Action class for Jaseci

Each action has an id, name, timestamp and it's set of edges.
"""
from .item import item
import importlib


class action(item):
    """
    Action class for Jaseci

    preset_in_out holds a set of parameters in the form of lists of context
    objects that are to be used from whereever those contexts are attached
    e.g., (nodes, edges, walkers, etc). This is used by Jac's runtime
    engine to support preset actions in nodes
    """

    def __init__(self, preset_in_out=None, *args, **kwargs):
        self.preset_in_out = preset_in_out  # Not using _ids convention
        super().__init__(*args, **kwargs)

    def trigger(self, param_list=None):
        """
        If using a preset param list, must unwind list of contexts otherwise
        param_list should be passed as list of values
        Also note that Jac stores preset_in_out as input/output list of hex
        ids since preset_in_out doesn't use _ids convention
        """
        use_params = []
        if(isinstance(param_list, list)):
            use_params = self.normalize_params(param_list)
        elif(self.preset_in_out):
            use_params = []
            for i in self.preset_in_out['input']:
                use_params.append(i.obj.context[i.name])
        result = getattr(
            importlib.import_module(self.value[0]),
            self.value[1]
        )(use_params)
        if(not param_list and self.preset_in_out and
           self.preset_in_out['output']):
            # uses tuple for the output variable name and owning obj id
            obj = self.preset_in_out['output'].obj
            obj.context[self.preset_in_out['output'].name] = result
        return result

    def normalize_params(self, param_list):
        """Normalize param list to include only values (no contexts)"""
        ret = []
        for i in param_list:
            ret.append(i)
        return ret
