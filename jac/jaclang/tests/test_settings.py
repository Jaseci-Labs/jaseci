"""Test Jac settings module."""

import os
from unittest.mock import mock_open, patch

from jaclang.settings import settings
from jaclang.utils.test import TestCase


class JacSettings(TestCase):
    """Test settings module."""

    def test_settings_config(self) -> None:
        """Basic settings for pass."""
        config_content = "[settings]\npass_timer = True"
        with patch("builtins.open", mock_open(read_data=config_content)):
            settings.load_config_file()
            self.assertEqual(settings.pass_timer, True)
        config_content = "[settings]\npass_timer = False"
        with patch("builtins.open", mock_open(read_data=config_content)):
            settings.load_config_file()
            self.assertEqual(settings.pass_timer, False)

    def test_settings_env_vars(self) -> None:
        """Basic settings for pass."""
        os.environ["JACLANG_PASS_TIMER"] = "True"
        settings.load_env_vars()
        self.assertEqual(settings.pass_timer, True)
        os.environ["JACLANG_PASS_TIMER"] = "False"
        settings.load_env_vars()
        self.assertEqual(settings.pass_timer, False)
        os.unsetenv("JACLANG_PASS_TIMER")

    def test_settings_precedence(self) -> None:
        """Basic settings for pass."""
        os.environ["JACLANG_PASS_TIMER"] = "True"
        config_content = "[settings]\npass_timer = False"
        with patch("builtins.open", mock_open(read_data=config_content)):
            settings.load_all()
            self.assertEqual(settings.pass_timer, True)
        config_content = "[settings]\npass_timer = True"
        os.environ["JACLANG_PASS_TIMER"] = "False"
        with patch("builtins.open", mock_open(read_data=config_content)):
            settings.load_all()
            self.assertEqual(settings.pass_timer, False)
        os.unsetenv("JACLANG_PASS_TIMER")
