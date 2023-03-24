from jaseci.utils.test_core import CoreTest
from jaseci.jsorc.jsorc import JsOrc
import jaseci.tests.jac_test_code as jtc


class GlobalApiTest(CoreTest):
    """Unit tests for Jac Global APIs"""

    fixture_src = __file__

    def setUp(self):
        super().setUp()

        self.smast2 = JsOrc.super_master(h=self.smast._h)
        self.smast.sentinel_register(name="test", code=jtc.basic)

        self.mast2 = JsOrc.master(h=self.mast._h)
        self.mast.sentinel_register(name="test", code=jtc.basic)

    def tearDown(self):
        super().tearDown()

    def test_sent_global_active(self):
        """Test setting global sentinel"""
        api = ["global_sentinel_set", {"snt": None}]
        self.call(self.smast, api)
        api = ["sentinel_active_global", {}]
        self.call(self.smast2, api)
        api = ["sentinel_list", {"detailed": False}]
        r = self.call(self.smast2, api)
        self.assertEqual(len(r), 0)
        api = ["sentinel_active_get", {"detailed": False}]
        r = self.call(self.smast2, api)
        self.assertIn("jid", r.keys())
        self.assertEqual(r["name"], "test")
        api = ["sentinel_list", {"detailed": False}]
        r = self.call(self.smast2, api)
        self.assertEqual(len(r), 0)

    def test_sent_global_pull(self):
        """Test setting global sentinel"""
        api = ["global_sentinel_set", {"snt": None}]
        self.call(self.smast, api)
        api = ["sentinel_list", {"detailed": False}]
        r = self.call(self.smast2, api)
        self.assertEqual(len(r), 0)
        api = ["sentinel_pull", {}]
        self.call(self.smast2, api)
        api = ["sentinel_list", {"detailed": False}]
        r = self.call(self.smast2, api)
        self.assertEqual(len(r), 1)
        api = ["sentinel_active_get", {"detailed": False}]
        r = self.call(self.smast2, api)
        self.assertIn("jid", r.keys())
        self.assertEqual(r["name"], "test")

    def test_global_set_get_delete(self):
        """Test setting global sentinel"""
        api = ["global_get", {"name": "apple"}]
        r = self.call(self.smast, api)
        self.assertIsNone(r["value"])
        api = ["global_set", {"name": "apple", "value": "56"}]
        r = self.call(self.smast, api)
        api = ["global_get", {"name": "apple"}]
        r = self.call(self.smast2, api)
        self.assertEqual(r["value"], "56")
        api = ["global_delete", {"name": "apple"}]
        r = self.call(self.smast2, api)
        api = ["global_get", {"name": "apple"}]
        r = self.call(self.smast, api)
        self.assertIsNone(r["value"])

    def test_user_create(self):
        """Test master create operation"""
        api = ["user_create", {"name": "yo@gmail.com"}]
        r = self.call(self.mast, api)
        self.assertIn("j_type", r["user"])
        self.assertEqual(r["user"]["j_type"], "master")

    def test_master_create(self):
        """Test master create operation"""
        api = ["master_create", {"name": "yo@gmail.com"}]
        r = self.call(self.mast, api)
        self.assertIn("j_type", r["user"])
        self.assertEqual(r["user"]["j_type"], "master")

    def test_master_create_error_out(self):
        """Test master create operation"""
        api = ["master_create", {"name": "yo@gmail.com"}]
        r = self.call(self.mast, api)
        api = ["master_create", {"name": "yo@gmail.com"}]
        r = self.call(self.mast, api)
        self.assertIn("response", r)
        self.assertIn("already exists", r["response"])

    def test_master_create_super_limited(self):
        """Test master create operation"""
        api = ["master_createsuper", {"name": "yo3@gmail.com"}]
        r = self.call(self.mast, api)
        self.assertIn("response", r)
        self.assertIn("not a valid", r["response"])

    def test_master_create_linked_super_master_create(self):
        """Test master create operation"""
        api = ["master_createsuper", {"name": "yo3@gmail.com"}]
        r = self.call(self.smast, api)
        self.assertIn("j_type", r["user"])
        self.assertEqual(r["user"]["j_type"], "super_master")

    def test_global_sentinel_set_unset(self):
        api = ["global_sentinel_set", {}]
        r = self.call(self.smast, api)
        self.assertIn("response", r)
        self.assertNotIn("error", r)
        api = ["global_sentinel_unset", {}]
        r = self.call(self.smast, api)
        self.assertIn("response", r)
        self.assertNotIn("error", r)

    def test_global_sentinel_double_unset(self):
        api = ["global_sentinel_set", {}]
        r = self.call(self.smast, api)
        self.assertIn("response", r)
        self.assertNotIn("error", r)
        api = ["global_sentinel_unset", {}]
        r = self.call(self.smast, api)
        self.assertIn("response", r)
        self.assertNotIn("error", r)
        api = ["global_sentinel_unset", {}]
        r = self.call(self.smast, api)
        self.assertIn("response", r)
        self.assertNotIn("error", r)

    def test_graph_node_set_mem_leak_fix(self):
        api = ["graph_create", {}]
        r = self.call(self.smast, api)
        before = len(self.smast._h.mem)
        jid = r["jid"]
        api = ["graph_node_set", {"nd": jid, "ctx": {}}]
        r = self.call(self.smast, api)
        api = ["graph_node_set", {"nd": jid, "ctx": {}}]
        r = self.call(self.smast, api)
        api = ["graph_node_set", {"nd": jid, "ctx": {}}]
        r = self.call(self.smast, api)
        api = ["graph_node_set", {"nd": jid, "ctx": {}}]
        r = self.call(self.smast, api)
        api = ["graph_node_set", {"nd": jid, "ctx": {}}]
        r = self.call(self.smast, api)
        api = ["graph_node_set", {"nd": jid, "ctx": {}}]
        r = self.call(self.smast, api)
        after = len(self.smast._h.mem)
        self.assertEqual(before, after)

    def test_mem_no_leak_creating_one_node_and_node_set(self):
        mem_state = self.smast._h.mem
        before = len(mem_state)
        self.call(
            self.smast,
            ["sentinel_register", {"code": self.load_jac("hello_world.jac")}],
        )
        self.assertEqual(len(mem_state) - before, 8)
        before = len(mem_state)
        r = self.call(
            self.smast,
            ["walker_run", {"name": "one_node"}],
        )
        jid = r["report"][0]["jid"]
        self.assertEqual(len(mem_state) - before, 2)
        before = len(mem_state)
        self.call(
            self.smast,
            ["graph_node_set", {"nd": jid, "ctx": {"msg": "goodbye world"}}],
        )
        self.assertEqual(len(mem_state) - before, 0)
        r = self.call(
            self.smast,
            ["graph_node_get", {"nd": jid}],
        )
        self.assertEqual(r["msg"], "goodbye world")
