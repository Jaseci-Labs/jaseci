from .test_api_core import core_test


class global_api_test(core_test):
    """Unit tests for Jac Global APIs"""

    def test_sent_global_active(self):
        """Test setting global sentinel"""
        api = ["global_sentinel_set", {"snt": None}]
        self.call(self.mast, api)
        api = ["sentinel_active_global", {}]
        self.call(self.mast2, api)
        api = ["sentinel_list", {"detailed": False}]
        r = self.call(self.mast2, api)
        self.assertEqual(len(r), 0)
        api = ["sentinel_active_get", {"detailed": False}]
        r = self.call(self.mast2, api)
        self.assertIn("jid", r.keys())
        self.assertEqual(r["name"], "test")
        api = ["sentinel_list", {"detailed": False}]
        r = self.call(self.mast2, api)
        self.assertEqual(len(r), 0)

    def test_sent_global_pull(self):
        """Test setting global sentinel"""
        api = ["global_sentinel_set", {"snt": None}]
        self.call(self.mast, api)
        api = ["sentinel_list", {"detailed": False}]
        r = self.call(self.mast2, api)
        self.assertEqual(len(r), 0)
        api = ["sentinel_pull", {}]
        self.call(self.mast2, api)
        api = ["sentinel_list", {"detailed": False}]
        r = self.call(self.mast2, api)
        self.assertEqual(len(r), 1)
        api = ["sentinel_active_get", {"detailed": False}]
        r = self.call(self.mast2, api)
        self.assertIn("jid", r.keys())
        self.assertEqual(r["name"], "test")

    def test_global_set_get_delete(self):
        """Test setting global sentinel"""
        api = ["global_get", {"name": "apple"}]
        r = self.call(self.mast, api)
        self.assertIsNone(r["value"])
        api = ["global_set", {"name": "apple", "value": "56"}]
        r = self.call(self.mast, api)
        api = ["global_get", {"name": "apple"}]
        r = self.call(self.mast2, api)
        self.assertEqual(r["value"], "56")
        api = ["global_delete", {"name": "apple"}]
        r = self.call(self.mast2, api)
        api = ["global_get", {"name": "apple"}]
        r = self.call(self.mast, api)
        self.assertIsNone(r["value"])

    def test_master_create(self):
        """Test master create operation"""
        api = ["master_create", {"name": "yo@gmail.com"}]
        r = self.call(self.lms, api)
        self.assertIn("j_type", r)
        self.assertEqual(r["j_type"], "master")

    def test_master_create_error_out(self):
        """Test master create operation"""
        api = ["master_create", {"name": "yo@gmail.com"}]
        r = self.call(self.lms, api)
        api = ["master_create", {"name": "yo@gmail.com"}]
        r = self.call(self.lms, api)
        self.assertIn("response", r)
        self.assertIn("already exists", r["response"])

    def test_master_create_super_limited(self):
        """Test master create operation"""
        api = ["master_createsuper", {"name": "yo3@gmail.com"}]
        r = self.call(self.lms, api)
        self.assertIn("response", r)
        self.assertIn("not a valid", r["response"])

    def test_master_create_linked_super_master_create(self):
        """Test master create operation"""
        api = ["master_createsuper", {"name": "yo3@gmail.com"}]
        r = self.call(self.mast, api)
        self.assertIn("j_type", r)
        self.assertEqual(r["j_type"], "super_master")

    def test_global_sentinel_set_unset(self):
        api = ["global_sentinel_set", {}]
        r = self.call(self.mast, api)
        self.assertIn("response", r)
        self.assertNotIn("error", r)
        api = ["global_sentinel_unset", {}]
        r = self.call(self.mast, api)
        self.assertIn("response", r)
        self.assertNotIn("error", r)

    def test_global_sentinel_double_unset(self):
        api = ["global_sentinel_set", {}]
        r = self.call(self.mast, api)
        self.assertIn("response", r)
        self.assertNotIn("error", r)
        api = ["global_sentinel_unset", {}]
        r = self.call(self.mast, api)
        self.assertIn("response", r)
        self.assertNotIn("error", r)
        api = ["global_sentinel_unset", {}]
        r = self.call(self.mast, api)
        self.assertIn("response", r)
        self.assertNotIn("error", r)

    def test_graph_node_set_mem_leak_fix(self):
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
