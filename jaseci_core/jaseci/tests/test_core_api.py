from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper
from jaseci.element.super_master import super_master
from jaseci.element.master import master
from jaseci.utils.mem_hook import mem_hook
import jaseci.tests.jac_test_code as jtc


class core_api_test(TestCaseHelper, TestCase):
    """Unit tests for Jac Core APIs"""

    def setUp(self):
        super().setUp()
        self.mast = super_master(h=mem_hook())
        self.mast2 = super_master(h=self.mast._h)
        self.mast.sentinel_register(name='test', code=jtc.basic)

        self.lms = master(h=mem_hook())
        self.lms2 = master(h=self.lms._h)
        self.lms.sentinel_register(name='test', code=jtc.basic)

    def tearDown(self):
        super().tearDown()

    def call(self, mast, pl):
        ret = mast.general_interface_to_api(
            api_name=pl[0], params=pl[1])
        return ret

    def test_sent_global_active(self):
        """Test setting global sentinel"""
        api = ['global_sentinel_set', {'snt': None}]
        self.call(self.mast, api)
        api = ['sentinel_active_global', {}]
        self.call(self.mast2, api)
        api = ['sentinel_list', {'detailed': False}]
        r = self.call(self.mast2, api)
        self.assertEqual(len(r), 0)
        api = ['sentinel_active_get', {'detailed': False}]
        r = self.call(self.mast2, api)
        self.assertIn('jid', r.keys())
        self.assertEqual(r['name'], 'test')
        api = ['sentinel_list', {'detailed': False}]
        r = self.call(self.mast2, api)
        self.assertEqual(len(r), 0)

    def test_sent_global_pull(self):
        """Test setting global sentinel"""
        api = ['global_sentinel_set', {'snt': None}]
        self.call(self.mast, api)
        api = ['sentinel_list', {'detailed': False}]
        r = self.call(self.mast2, api)
        self.assertEqual(len(r), 0)
        api = ['sentinel_pull', {}]
        self.call(self.mast2, api)
        api = ['sentinel_list', {'detailed': False}]
        r = self.call(self.mast2, api)
        self.assertEqual(len(r), 1)
        api = ['sentinel_active_get', {'detailed': False}]
        r = self.call(self.mast2, api)
        self.assertIn('jid', r.keys())
        self.assertEqual(r['name'], 'test')

    def test_global_set_get_delete(self):
        """Test setting global sentinel"""
        api = ['global_get', {'name': 'apple'}]
        r = self.call(self.mast, api)
        self.assertIsNone(r['value'])
        api = ['global_set', {'name': 'apple', 'value': '56'}]
        r = self.call(self.mast, api)
        api = ['global_get', {'name': 'apple'}]
        r = self.call(self.mast2, api)
        self.assertEqual(r['value'], '56')
        api = ['global_delete', {'name': 'apple'}]
        r = self.call(self.mast2, api)
        api = ['global_get', {'name': 'apple'}]
        r = self.call(self.mast, api)
        self.assertIsNone(r['value'])

    def test_master_create(self):
        """Test master create operation"""
        api = ['master_create', {'name': 'yo@gmail.com'}]
        r = self.call(self.lms, api)
        self.assertIn('j_type', r)
        self.assertEqual(r['j_type'], 'master')

    def test_master_create_error_out(self):
        """Test master create operation"""
        api = ['master_create', {'name': 'yo@gmail.com'}]
        r = self.call(self.lms, api)
        api = ['master_create', {'name': 'yo@gmail.com'}]
        r = self.call(self.lms, api)
        self.assertIn('response', r)
        self.assertIn('already exists', r['response'])

    def test_master_create_super_limited(self):
        """Test master create operation"""
        api = ['master_createsuper', {'name': 'yo3@gmail.com'}]
        r = self.call(self.lms, api)
        self.assertIn('response', r)
        self.assertIn('not a valid', r['response'])

    def test_master_create_linked_super_master_create(self):
        """Test master create operation"""
        api = ['master_createsuper', {'name': 'yo3@gmail.com'}]
        r = self.call(self.mast, api)
        self.assertIn('j_type', r)
        self.assertEqual(r['j_type'], 'super_master')

    def test_global_sentinel_set_unset(self):
        api = ['global_sentinel_set', {}]
        r = self.call(self.mast, api)
        self.assertIn('response', r)
        self.assertNotIn('error', r)
        api = ['global_sentinel_unset', {}]
        r = self.call(self.mast, api)
        self.assertIn('response', r)
        self.assertNotIn('error', r)

    def test_global_sentinel_double_unset(self):
        api = ['global_sentinel_set', {}]
        r = self.call(self.mast, api)
        self.assertIn('response', r)
        self.assertNotIn('error', r)
        api = ['global_sentinel_unset', {}]
        r = self.call(self.mast, api)
        self.assertIn('response', r)
        self.assertNotIn('error', r)
        api = ['global_sentinel_unset', {}]
        r = self.call(self.mast, api)
        self.assertIn('response', r)
        self.assertNotIn('error', r)
