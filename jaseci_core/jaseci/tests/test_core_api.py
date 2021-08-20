from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper
from jaseci.master import master
from jaseci.utils.mem_hook import mem_hook
import jaseci.tests.jac_test_code as jtc


class core_api_test(TestCaseHelper, TestCase):
    """Unit tests for Jac Core APIs"""

    def setUp(self):
        super().setUp()
        self.mast = master(h=mem_hook())
        self.mast2 = master(h=self.mast._h)
        self.mast.api_sentinel_register(name='test', code=jtc.ll_proto)

    def tearDown(self):
        super().tearDown()

    def call(self, mast, pl):
        ret = mast.general_interface_to_api(
            api_name=pl[0], params=pl[1])
        self.log(ret)
        return ret

    def test_sent_global_active(self):
        """Test setting global sentinel"""
        api = ['admin_api_global_sentinel_set', {'snt': None}]
        self.call(self.mast, api)
        api = ['api_sentinel_active_global', {}]
        self.call(self.mast2, api)
        api = ['api_sentinel_list', {'detailed': False}]
        r = self.call(self.mast2, api)
        self.assertEqual(len(r), 0)
        api = ['api_sentinel_active_get', {'detailed': False}]
        r = self.call(self.mast2, api)
        self.assertIn('jid', r.keys())
        self.assertEqual(r['name'], 'test')
        api = ['api_sentinel_list', {'detailed': False}]
        r = self.call(self.mast2, api)
        self.assertEqual(len(r), 0)

    def test_sent_global_pull(self):
        """Test setting global sentinel"""
        api = ['admin_api_global_sentinel_set', {'snt': None}]
        self.call(self.mast, api)
        api = ['api_sentinel_list', {'detailed': False}]
        r = self.call(self.mast2, api)
        self.assertEqual(len(r), 0)
        api = ['api_sentinel_pull', {}]
        self.call(self.mast2, api)
        api = ['api_sentinel_list', {'detailed': False}]
        r = self.call(self.mast2, api)
        self.assertEqual(len(r), 1)
        api = ['api_sentinel_active_get', {'detailed': False}]
        r = self.call(self.mast2, api)
        self.assertIn('jid', r.keys())
        self.assertEqual(r['name'], 'test')

    def test_global_set_get_delete(self):
        """Test setting global sentinel"""
        api = ['admin_api_global_get', {'name': 'apple'}]
        r = self.call(self.mast, api)
        self.assertIsNone(r)
        api = ['admin_api_global_set', {'name': 'apple', 'value': '56'}]
        r = self.call(self.mast, api)
        api = ['admin_api_global_get', {'name': 'apple'}]
        r = self.call(self.mast2, api)
        self.assertEqual(r, '56')
        api = ['admin_api_global_delete', {'name': 'apple'}]
        r = self.call(self.mast2, api)
        api = ['admin_api_global_get', {'name': 'apple'}]
        r = self.call(self.mast, api)
        self.assertIsNone(r)
