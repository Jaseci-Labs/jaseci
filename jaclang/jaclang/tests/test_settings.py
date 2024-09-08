"""Test Jac settings module."""

import os
from unittest.mock import mock_open, patch

from jaclang.settings import settings
from jaclang.utils.test import TestCase


class JacSettings(TestCase):
    """Test settings module."""

    def test_settings_config(self) -> None:
        """Basic settings for pass."""
        config_content = "[settings]\nfuse_type_info_debug = True"
        with patch("builtins.open", mock_open(read_data=config_content)):
            settings.load_config_file()
            self.assertEqual(settings.fuse_type_info_debug, True)
        config_content = "[settings]\nfuse_type_info_debug = False"
        with patch("builtins.open", mock_open(read_data=config_content)):
            settings.load_config_file()
            self.assertEqual(settings.fuse_type_info_debug, False)

    def test_settings_env_vars(self) -> None:
        """Basic settings for pass."""
        os.environ["JACLANG_FUSE_TYPE_INFO_DEBUG"] = "True"
        settings.load_env_vars()
        self.assertEqual(settings.fuse_type_info_debug, True)
        os.environ["JACLANG_FUSE_TYPE_INFO_DEBUG"] = "False"
        settings.load_env_vars()
        self.assertEqual(settings.fuse_type_info_debug, False)
        os.unsetenv("JACLANG_FUSE_TYPE_INFO_DEBUG")

    def test_settings_precedence(self) -> None:
        """Basic settings for pass."""
        os.environ["JACLANG_FUSE_TYPE_INFO_DEBUG"] = "True"
        config_content = "[settings]\nfuse_type_info_debug = False"
        with patch("builtins.open", mock_open(read_data=config_content)):
            settings.load_all()
            self.assertEqual(settings.fuse_type_info_debug, True)
        config_content = "[settings]\nfuse_type_info_debug = True"
        os.environ["JACLANG_FUSE_TYPE_INFO_DEBUG"] = "False"
        with patch("builtins.open", mock_open(read_data=config_content)):
            settings.load_all()
            self.assertEqual(settings.fuse_type_info_debug, False)
        os.unsetenv("JACLANG_FUSE_TYPE_INFO_DEBUG")
