"""Test for jaseci plugin (default)"""

import io
import os
import sys

from jaclang.cli import cli
from jaclang.utils.test import TestCase


class TestJaseciPlugin(TestCase):
    """Test jaseci plugin."""

    def setUp(self) -> None:
        """Set up test."""
        super().setUp()
        self.session = "jaclang.test.session"

    def tearDown(self) -> None:
        """Tear down test."""
        super().tearDown()
        sys.stdout = sys.__stdout__
        self._del_session()

    def _output2buffer(self) -> None:
        """Start capturing output."""
        self.capturedOutput = io.StringIO()
        sys.stdout = self.capturedOutput

    def _output2std(self) -> None:
        """Redirect output back to stdout."""
        sys.stdout = sys.__stdout__

    def _del_session(self) -> None:
        if os.path.exists(self.session):
            os.remove(self.session)

    def test_walker_simple_persistent(self) -> None:
        """Test simple persistent object."""
        self._output2buffer()
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

    def test_entrypoint_root(self) -> None:
        """Test entrypoint being root."""
        cli.run(
            filename=self.fixture_abs_path("simple_persistent.jac"),
            session=self.session,
            walker="create",
        )
        obj = cli.get_object(session=self.session, id="root")
        self._output2buffer()
        cli.run(
            filename=self.fixture_abs_path("simple_persistent.jac"),
            session=self.session,
            node=obj["_jac_"]["id"],
            walker="traverse",
        )
        output = self.capturedOutput.getvalue().strip()
        self.assertEqual(output, "node a\nnode b")

    def test_entrypoint_non_root(self) -> None:
        """Test entrypoint being non root node."""
        cli.run(
            filename=self.fixture_abs_path("simple_persistent.jac"),
            session=self.session,
            walker="create",
        )
        obj = cli.get_object(session=self.session, id="root")
        edge_obj = cli.get_object(session=self.session, id=obj["_jac_"]["edge_ids"][0])
        a_obj = cli.get_object(session=self.session, id=edge_obj["_jac_"]["target_id"])
        self._output2buffer()
        cli.run(
            filename=self.fixture_abs_path("simple_persistent.jac"),
            session=self.session,
            node=a_obj["_jac_"]["id"],
            walker="traverse",
        )
        output = self.capturedOutput.getvalue().strip()
        self.assertEqual(output, "node a\nnode b")

    def test_get_edge(self) -> None:
        """Test get an edge object."""
        cli.run(
            filename=self.fixture_abs_path("simple_node_connection.jac"),
            session=self.session,
        )
        obj = cli.get_object(session=self.session, id="root")
        self.assertEqual(len(obj["_jac_"]["edge_ids"]), 2)
        edge_objs = [
            cli.get_object(session=self.session, id=e_id)
            for e_id in obj["_jac_"]["edge_ids"]
        ]
        node_ids = [obj["_jac_"]["target_id"] for obj in edge_objs]
        node_objs = [cli.get_object(session=self.session, id=n_id) for n_id in node_ids]
        self.assertEqual(len(node_objs), 2)
        self.assertEqual({obj["tag"] for obj in node_objs}, {"first", "second"})

    # def test_filtering_on_edge(self) -> None:
    # """test filtering on edge"

    # def test_filtering_on_node(self) -> None:
    # """test filtering on node"

    # def test_traverse_backwards(self) -> None:
    # """test traversing backwards"

    # def test_direct_reference_edge(self)
    # def test_direct_referece_node(self)
    # def test_entrypoint_node(self) -> None:
    #     """Test entrypoint being non root node."""

    # def test_get_object(self) -> None:
    #     """Test get object cli."""

    # def test_persistent_root(self):
    #    """"Test that root and its connecting nodes are persistent"""
