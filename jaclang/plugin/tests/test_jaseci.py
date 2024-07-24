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

    def tearDown(self) -> None:
        """Tear down test."""
        super().tearDown()
        sys.stdout = sys.__stdout__

    def _output2buffer(self) -> None:
        """Start capturing output."""
        self.capturedOutput = io.StringIO()
        sys.stdout = self.capturedOutput

    def _output2std(self) -> None:
        """Redirect output back to stdout."""
        sys.stdout = sys.__stdout__

    def _del_session(self, session: str) -> None:
        if os.path.exists(session):
            os.remove(session)

    def test_walker_simple_persistent(self) -> None:
        """Test simple persistent object."""
        session = self.fixture_abs_path("test_walker_simple_persistent.session")
        self._output2buffer()
        cli.run(
            filename=self.fixture_abs_path("simple_persistent.jac"),
            session=session,
            walker="create",
        )
        cli.run(
            filename=self.fixture_abs_path("simple_persistent.jac"),
            session=session,
            walker="traverse",
        )
        output = self.capturedOutput.getvalue().strip()
        self.assertEqual(output, "node a\nnode b")
        self._del_session(session)

    def test_entrypoint_root(self) -> None:
        """Test entrypoint being root."""
        session = self.fixture_abs_path("test_entrypoint_root.session")
        cli.run(
            filename=self.fixture_abs_path("simple_persistent.jac"),
            session=session,
            walker="create",
        )
        obj = cli.get_object(session=session, id="root")
        self._output2buffer()
        cli.run(
            filename=self.fixture_abs_path("simple_persistent.jac"),
            session=session,
            node=str(obj["_jac_"]["id"]),
            walker="traverse",
        )
        output = self.capturedOutput.getvalue().strip()
        self.assertEqual(output, "node a\nnode b")
        self._del_session(session)

    def test_entrypoint_non_root(self) -> None:
        """Test entrypoint being non root node."""
        session = self.fixture_abs_path("test_entrypoint_non_root.session")
        cli.run(
            filename=self.fixture_abs_path("simple_persistent.jac"),
            session=session,
            walker="create",
        )
        obj = cli.get_object(session=session, id="root")
        edge_obj = cli.get_object(session=session, id=str(obj["_jac_"]["edge_ids"][0]))
        a_obj = cli.get_object(session=session, id=str(edge_obj["_jac_"]["target_id"]))
        self._output2buffer()
        cli.run(
            filename=self.fixture_abs_path("simple_persistent.jac"),
            session=session,
            node=str(a_obj["_jac_"]["id"]),
            walker="traverse",
        )
        output = self.capturedOutput.getvalue().strip()
        self.assertEqual(output, "node a\nnode b")
        self._del_session(session)

    def test_get_edge(self) -> None:
        """Test get an edge object."""
        session = self.fixture_abs_path("test_get_edge.session")
        cli.run(
            filename=self.fixture_abs_path("simple_node_connection.jac"),
            session=session,
        )
        obj = cli.get_object(session=session, id="root")
        self.assertEqual(len(obj["_jac_"]["edge_ids"]), 2)
        edge_objs = [
            cli.get_object(session=session, id=str(e_id))
            for e_id in obj["_jac_"]["edge_ids"]
        ]
        node_ids = [obj["_jac_"]["target_id"] for obj in edge_objs]
        node_objs = [cli.get_object(session=session, id=str(n_id)) for n_id in node_ids]
        self.assertEqual(len(node_objs), 2)
        self.assertEqual({obj["tag"] for obj in node_objs}, {"first", "second"})
        self._del_session(session)

    def test_filter_on_edge_get_edge(self) -> None:
        """Test filtering on edge."""
        session = self.fixture_abs_path("test_filter_on_edge_get_edge.session")
        cli.run(
            filename=self.fixture_abs_path("simple_node_connection.jac"),
            session=session,
        )
        self._output2buffer()
        cli.run(
            filename=self.fixture_abs_path("simple_node_connection.jac"),
            session=session,
            walker="filter_on_edge_get_edge",
        )
        self.assertEqual(
            self.capturedOutput.getvalue().strip(), "[simple_edge(index=1)]"
        )
        self._del_session(session)

    def test_filter_on_edge_get_node(self) -> None:
        """Test filtering on edge, then get node."""
        session = self.fixture_abs_path("test_filter_on_edge_get_node.session")
        cli.run(
            filename=self.fixture_abs_path("simple_node_connection.jac"),
            session=session,
        )
        self._output2buffer()
        cli.run(
            filename=self.fixture_abs_path("simple_node_connection.jac"),
            session=session,
            walker="filter_on_edge_get_node",
        )
        self.assertEqual(
            self.capturedOutput.getvalue().strip(), "[simple(tag='second')]"
        )
        self._del_session(session)

    def test_filter_on_node_get_node(self) -> None:
        """Test filtering on node, then get edge."""
        session = self.fixture_abs_path("test_filter_on_node_get_node.session")
        cli.run(
            filename=self.fixture_abs_path("simple_node_connection.jac"),
            session=session,
        )
        self._output2buffer()
        cli.run(
            filename=self.fixture_abs_path("simple_node_connection.jac"),
            session=session,
            walker="filter_on_node_get_node",
        )
        self.assertEqual(
            self.capturedOutput.getvalue().strip(), "[simple(tag='second')]"
        )
        self._del_session(session)

    def test_filter_on_edge_visit(self) -> None:
        """Test filtering on edge, then visit."""
        session = self.fixture_abs_path("test_filter_on_edge_visit.session")
        cli.run(
            filename=self.fixture_abs_path("simple_node_connection.jac"),
            session=session,
        )
        self._output2buffer()
        cli.run(
            filename=self.fixture_abs_path("simple_node_connection.jac"),
            session=session,
            walker="filter_on_edge_visit",
        )
        self.assertEqual(self.capturedOutput.getvalue().strip(), "simple(tag='first')")
        self._del_session(session)

    def test_filter_on_node_visit(self) -> None:
        """Test filtering on node, then visit."""
        session = self.fixture_abs_path("test_filter_on_node_visit.session")
        cli.run(
            filename=self.fixture_abs_path("simple_node_connection.jac"),
            session=session,
        )
        self._output2buffer()
        cli.run(
            filename=self.fixture_abs_path("simple_node_connection.jac"),
            session=session,
            walker="filter_on_node_visit",
        )
        self.assertEqual(self.capturedOutput.getvalue().strip(), "simple(tag='first')")
        self._del_session(session)

    def test_indirect_reference_node(self) -> None:
        """Test reference node indirectly without visiting."""
        session = self.fixture_abs_path("test_indirect_reference_node.session")
        cli.run(
            filename=self.fixture_abs_path("simple_persistent.jac"),
            session=session,
            walker="create",
        )
        self._output2buffer()
        cli.run(
            filename=self.fixture_abs_path("simple_persistent.jac"),
            session=session,
            walker="indirect_ref",
        )
        self.assertEqual(
            self.capturedOutput.getvalue().strip(),
            "[b(name='node b')]\n[GenericEdge]",
        )
        self._del_session(session)
