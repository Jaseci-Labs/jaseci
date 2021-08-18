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
        self.mast.api_sentinel_register(name='test', code=jtc.ll_proto)

    def tearDown(self):
        super().tearDown()

    def call(self, pl):
        ret = self.mast.general_interface_to_api(
            api_name=pl[0], params=pl[1])
        self.log(ret)
        return ret

    def test_global_sent(self):
        """Test setting global sentinel"""
        api = ['admin_api_global_sentinel_set', {'snt': None}]
        self.call(api)
        api = ['api_sentinel_active_global', {}]
        self.call(api)
        api = ['api_sentinel_active_get', {'detailed': False}]
        r = self.call(api)
        self.assertIn('jid', r.keys())
        self.assertEqual(r['name'], 'test')
