from .test_api_core import core_test


class walker_api_test(core_test):
    """Unit tests for Jac Walker APIs"""

    def test_another_thing(self):
        api = ["graph_create", {}]
        r = self.call(self.mast, api)
        before = len(self.mast._h.mem)
        jid = r["jid"]
        api = ["graph_node_set", {"nd": jid, "ctx": {}}]
        r = self.call(self.mast, api)
        api = ["graph_node_set", {"nd": jid, "ctx": {}}]
        r = self.call(self.mast, api)
        api = ["graph_node_set", {"nd": jid, "ctx": {}}]
        r = self.call(self.mast, api)
        api = ["graph_node_set", {"nd": jid, "ctx": {}}]
        r = self.call(self.mast, api)
        api = ["graph_node_set", {"nd": jid, "ctx": {}}]
        r = self.call(self.mast, api)
        api = ["graph_node_set", {"nd": jid, "ctx": {}}]
        r = self.call(self.mast, api)
        after = len(self.mast._h.mem)
        self.assertEqual(before, after)

    def test_current_node_present_in_output(self):
        pass
