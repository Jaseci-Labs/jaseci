"""Test for jaseci plugin (default)"""

import io, sys
from jaclang.utils.test import TestCase
from jaclang.cli import cli


class TestJaseciPlugin(TestCase):
    """Test jaseci plugin"""

    def setUp(self) -> None:
        super().setUp()
        self.capturedOutput = io.StringIO()
        sys.stdout = self.capturedOutput

    def tearDown(self) -> None:
        super().tearDown()
        sys.stdout = sys.__stdout__

    def test_simple_persistent(self) -> None:
        """Test simple persistent object"""
        cli.run()
