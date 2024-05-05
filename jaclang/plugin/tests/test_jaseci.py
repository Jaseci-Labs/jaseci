"""Test for jaseci plugin (default)"""

import io, sys, os
from jaclang.utils.test import TestCase
from jaclang.cli import cli


class TestJaseciPlugin(TestCase):
    """Test jaseci plugin"""

    def setUp(self) -> None:
        super().setUp()
        self.capturedOutput = io.StringIO()
        sys.stdout = self.capturedOutput
        self.session = "jaclang.test.session"

    def tearDown(self) -> None:
        super().tearDown()
        sys.stdout = sys.__stdout__
        self._del_session()

    def _del_session(self) -> None:
        if os.path.exists(self.session):
            os.remove(self.session)

    def test_simple_persistent(self) -> None:
        """Test simple persistent object"""
        cli.run(
            filename=self.fixture_abs_path("simple_persistent.jac"),
            session=self.session,
            walker="create",
        )
        cli.run(
            filename=self.fixture_abs_path("simple_persistent.jac"),
            session=self.session,
            walker="traverse",
        )
        output = self.capturedOutput.getvalue().strip()
        self.assertEqual(output, "node a\nnode b")
