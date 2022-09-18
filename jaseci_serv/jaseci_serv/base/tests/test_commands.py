from jaseci.utils.utils import TestCaseHelper
from django.test import TestCase
from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError


class TestCmds(TestCaseHelper, TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_wait_for_db_when_ready(self):
        """Test waiting for db when it's available"""
        with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
            gi.return_value = True
            call_command("wait_for_db")
            self.assertEqual(gi.call_count, 1)

    def test_wait_for_db_when_lagging(self):
        """Test waiting for db"""
        with patch("time.sleep") as ts:
            ts.return_value = True
            with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
                gi.side_effect = [OperationalError] * 5 + [True]
                call_command("wait_for_db")
                self.assertEqual(gi.call_count, 6)
