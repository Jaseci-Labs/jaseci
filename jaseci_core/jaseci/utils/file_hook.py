from .mem_hook import mem_hook
import pickle


class file_hook(mem_hook):
    """
    Uses files for persistence
    """

    def __init__(self, filename):
        mem_hook.__init__(self)
        self.filename = filename
        with open(filename, 'rb') as f:
            self.mem = pickle.load(f)

    def commit(self):
        """Write through all saves to store"""
        with open(self.filename, 'wb') as f:
            pickle.dump(self.mem, f)
