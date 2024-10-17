"""JacLang Jaseci Unit Test."""

from .test_util import JacCloudTest
from ..jaseci.datasources import Collection


class SimpleGraphTest(JacCloudTest):
    """JacLang Jaseci Feature Tests."""

    def setUp(self) -> None:
        """Override setUp."""
        self.run_server(
            "jac_cloud/tests/situational_flows.jac",
            port=8002,
            envs={
                "DATABASE_HOST": "mongodb://localhost/?retryWrites=true&w=majority",
                "SHOW_ENDPOINT_RETURNS": "true",
            },
        )

        Collection.__client__ = None
        Collection.__database__ = None
        self.client = Collection.get_client()

    def tearDown(self) -> None:
        """Override tearDown."""
        self.client.drop_database(self.database)
        self.stop_server()

    def trigger_spawn_test(self) -> None:
        """Test spawn call behavior of walker."""
        res = self.post_api("WalkerTestSpawn", json={})
        self.assertEqual(200, res["status"])

        reports = res["reports"]
        self.assertEqual("Walker entry: Root()", reports[0])
        self.assertEqual("Node entry: Root()", reports[1])
        for i in range(5):
            self.assertEqual(f"Node exit: NodeTest(value={i})", reports[i + 2])
        self.assertEqual("Walker exit: NodeTest(value=4)", reports[7])
        visitor_report = res["reports"][-1]

        visited_nodes = visitor_report["context"]["visited_nodes"]
        entry_count = visitor_report["context"]["entry_count"]
        exit_count = visitor_report["context"]["exit_count"]

        self.assertEqual(visited_nodes, [{"value": i} for i in range(5)])
        self.assertEqual(entry_count, 1)
        self.assertEqual(exit_count, 1)

    def test_situational_features(self) -> None:
        """Test Full Features."""
        self.trigger_create_user_test(has_name=False)

        self.trigger_spawn_test()
