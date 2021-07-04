from django.contrib.auth import get_user_model

from jaseci.utils.utils import TestCaseHelper
from django.test import TestCase

from base.models import GlobalConfig
from jaseci.utils.mem_hook import mem_hook

# Alias for create user
create_user = get_user_model().objects.create_user
get_user = get_user_model().objects.get


class jaseci_engine_orm_config_tests_private(TestCaseHelper, TestCase):
    """Test Jaseci Engine when authenticated"""

    def setUp(self):
        super().setUp()
        self.user = create_user(
            email='JSCadft@jaseci.com',
            password='testpass',
            name='some dude',
        )
        self._h = mem_hook()

    def tearDown(self):
        super().tearDown()

    def test_jsci_db_to_engine_hook_saving(self):
        """Test that db hooks are set up correctly for saving"""
        user = self.user
        self.assertIsNotNone(user._h)
        h = user._h
        h.save_cfg('GOOBY', 'MOOBY')
        h.commit()

        load_test = GlobalConfig.objects.get(name='GOOBY')
        self.assertEqual(load_test.value, 'MOOBY')

    def test_jsci_db_to_engine_hook_loading(self):
        """Test that db cfg hooks are set up correctly for loading"""
        user = self.user
        self.assertIsNotNone(user._h)
        h = user._h
        h.save_cfg('GOOBY1', 'MOOBY1')
        h.commit()

        del user._h.mem['config']['GOOBY1']
        user._h.red.delete('GOOBY1')
        self.assertNotIn('GOOBY1', user._h.mem['config'].keys())

        load_test = GlobalConfig.objects.filter(name='GOOBY1').first()
        self.assertIsInstance(load_test, GlobalConfig)

        user._h.get_cfg('GOOBY1')
        self.assertEqual(user._h.mem['config']['GOOBY1'], 'MOOBY1')

    def test_jsci_db_cfg_listing(self):
        """Test that db cfg hooks are set up correctly for listing"""
        user = self.user
        self.assertIsNotNone(user._h)
        h = user._h
        h.save_cfg('GOOBY1', 'MOOBY1')
        h.save_cfg('GOOBY2', 'MOOBY2')
        h.save_cfg('GOOBY3', 'MOOBY3')
        h.commit()

        user._h.clear_mem_cache()
        user._h.red.delete('GOOBY1')
        self.assertEqual(len(user._h.mem['config'].keys()), 0)
        self.assertNotIn('GOOBY1', user._h.mem['config'].keys())

        li = user._h.list_cfg()
        self.assertEqual(len(li), 3)
        self.assertEqual(len(user._h.mem['config'].keys()), 0)
        user._h.get_cfg('GOOBY1')
        self.assertEqual(user._h.mem['config']['GOOBY1'], 'MOOBY1')
