"""Test for jaseci plugin."""

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

    def test_filter_on_edge_get_edge(self) -> None:
        """Test filtering on edge."""
        cli.run(
            filename=self.fixture_abs_path("simple_node_connection.jac"),
            session=self.session,
        )
        self._output2buffer()
        cli.run(
            filename=self.fixture_abs_path("simple_node_connection.jac"),
            session=self.session,
            walker="filter_on_edge_get_edge",
        )
        self.assertEqual(
            self.capturedOutput.getvalue().strip(), "[simple_edge(index=1)]"
        )

    def test_filter_on_edge_get_node(self) -> None:
        """Test filtering on edge, then get node."""
        cli.run(
            filename=self.fixture_abs_path("simple_node_connection.jac"),
            session=self.session,
        )
        self._output2buffer()
        cli.run(
            filename=self.fixture_abs_path("simple_node_connection.jac"),
            session=self.session,
            walker="filter_on_edge_get_node",
        )
        self.assertEqual(
            self.capturedOutput.getvalue().strip(), "[simple(tag='second')]"
        )

    def test_filter_on_node_get_edge(self) -> None:
        """Test filtering on node, then get edge."""
        self.skipTest("Not sure if this is supported by the language")
        cli.run(
            filename=self.fixture_abs_path("simple_node_connection.jac"),
            session=self.session,
        )
        self._output2buffer()
        cli.run(
            filename=self.fixture_abs_path("simple_node_connection.jac"),
            session=self.session,
            walker="filter_on_node_get_edge",
        )
        self.assertEqual(
            self.capturedOutput.getvalue().strip(), "[simple_edge(index=1)]"
        )

    def test_filter_on_node_get_node(self) -> None:
        """Test filtering on node, then get edge."""
        cli.run(
            filename=self.fixture_abs_path("simple_node_connection.jac"),
            session=self.session,
        )
        self._output2buffer()
        cli.run(
            filename=self.fixture_abs_path("simple_node_connection.jac"),
            session=self.session,
            walker="filter_on_node_get_node",
        )
        self.assertEqual(
            self.capturedOutput.getvalue().strip(), "[simple(tag='second')]"
        )

    def test_filter_on_edge_visit(self) -> None:
        """Test filtering on edge, then visit."""
        cli.run(
            filename=self.fixture_abs_path("simple_node_connection.jac"),
            session=self.session,
        )
        self._output2buffer()
        cli.run(
            filename=self.fixture_abs_path("simple_node_connection.jac"),
            session=self.session,
            walker="filter_on_edge_visit",
        )
        self.assertEqual(self.capturedOutput.getvalue().strip(), "simple(tag='first')")

    def test_filter_on_node_visit(self) -> None:
        """Test filtering on node, then visit."""
        cli.run(
            filename=self.fixture_abs_path("simple_node_connection.jac"),
            session=self.session,
        )
        self._output2buffer()
        cli.run(
            filename=self.fixture_abs_path("simple_node_connection.jac"),
            session=self.session,
            walker="filter_on_node_visit",
        )
        self.assertEqual(self.capturedOutput.getvalue().strip(), "simple(tag='first')")

    def test_indirect_reference_node(self) -> None:
        """Test reference node indirectly without visiting."""
        cli.run(
            filename=self.fixture_abs_path("simple_persistent.jac"),
            session=self.session,
            walker="create",
        )
        self._output2buffer()
        cli.run(
            filename=self.fixture_abs_path("simple_persistent.jac"),
            session=self.session,
            walker="indirect_ref",
        )
        self.assertEqual(
            self.capturedOutput.getvalue().strip(),
            "[b(name='node b')]\n[GenericEdge]",
        )
