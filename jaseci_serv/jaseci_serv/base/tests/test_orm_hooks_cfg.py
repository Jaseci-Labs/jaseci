from django.contrib.auth import get_user_model
from django.db.models import Q

from jaseci.utils.utils import TestCaseHelper
from django.test import TestCase

from jaseci_serv.base.models import GlobalVars

# Alias for create user
create_user = get_user_model().objects.create_user
get_user = get_user_model().objects.get


class OrmConfigTestsPrivate(TestCaseHelper, TestCase):
    """Test Jaseci Engine when authenticated"""

    def setUp(self):
        super().setUp()
        self.user = create_user(
            email="JSCadft@jaseci.com",
            password="testpass",
            name="some dude",
        )

    def tearDown(self):
        super().tearDown()

    def test_jsci_db_to_engine_hook_saving(self):
        """Test that db hooks are set up correctly for saving"""
        user = self.user
        self.assertIsNotNone(user._h)
        h = user._h
        h.save_glob("GOOBY", "MOOBY")
        h.commit()

        load_test = GlobalVars.objects.get(name="GOOBY")
        self.assertEqual(load_test.value, "MOOBY")

    def test_jsci_db_to_engine_hook_loading(self):
        """Test that db glob hooks are set up correctly for loading"""
        user = self.user
        self.assertIsNotNone(user._h)
        h = user._h
        h.save_glob("GOOBY1", "MOOBY1")
        h.commit()

        del user._h.mem["global"]["GOOBY1"]
        if h.redis.is_running():
            h.redis.delete("GOOBY1")
        self.assertNotIn("GOOBY1", user._h.mem["global"].keys())

        load_test = GlobalVars.objects.filter(name="GOOBY1").first()
        self.assertIsInstance(load_test, GlobalVars)

        user._h.get_glob("GOOBY1")
        self.assertEqual(user._h.mem["global"]["GOOBY1"], "MOOBY1")

    def test_jsci_db_glob_listing(self):
        """Test that db glob hooks are set up correctly for listing"""
        user = self.user
        self.assertIsNotNone(user._h)
        h = user._h
        h.save_glob("GOOBY1", "MOOBY1")
        h.save_glob("GOOBY2", "MOOBY2")
        h.save_glob("GOOBY3", "MOOBY3")
        h.commit()

        h.clear_cache()
        if h.redis.is_running():
            h.redis.delete("GOOBY1")
        self.assertEqual(len(user._h.mem["global"].keys()), 0)
        self.assertNotIn("GOOBY1", user._h.mem["global"].keys())

        # Removing default configs
        GlobalVars.objects.filter(Q(name__endswith="_CONFIG")).delete()
        GlobalVars.objects.filter(Q(name__endswith="_MANIFEST")).delete()

        li = user._h.list_glob()
        self.assertEqual(len(li), 3)
        self.assertEqual(len(user._h.mem["global"].keys()), 0)
        user._h.get_glob("GOOBY1")
        self.assertEqual(user._h.mem["global"]["GOOBY1"], "MOOBY1")
