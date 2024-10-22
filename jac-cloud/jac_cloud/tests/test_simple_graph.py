"""JacLang Jaseci Unit Test."""

from .test_util import JacCloudTest
from ..jaseci.datasources import Collection


class SimpleGraphTest(JacCloudTest):
    """JacLang Jaseci Feature Tests."""

    def setUp(self) -> None:
        """Override setUp."""
        self.run_server(
            "jac_cloud/tests/simple_graph.jac",
            envs={
                "DATABASE_HOST": "mongodb://localhost/?retryWrites=true&w=majority",
                "SHOW_ENDPOINT_RETURNS": "true",
            },
        )

        Collection.__client__ = None
        Collection.__database__ = None
        self.client = Collection.get_client()
        self.q_node = Collection.get_collection("node")
        self.q_edge = Collection.get_collection("edge")

    def tearDown(self) -> None:
        """Override tearDown."""
        self.client.drop_database(self.database)
        self.stop_server()

    def nested_count_should_be(self, node: int, edge: int) -> None:
        """Test nested node count."""
        self.assertEqual(node, self.q_node.count_documents({"name": "Nested"}))
        self.assertEqual(
            edge,
            self.q_edge.count_documents(
                {
                    "$or": [
                        {"source": {"$regex": "^n:Nested:"}},
                        {"target": {"$regex": "^n:Nested:"}},
                    ]
                }
            ),
        )

    def test_all_features(self) -> None:
        """Test Full Features."""
        self.trigger_openapi_specs_test("jac_cloud/tests/openapi_specs.yaml")

        self.trigger_create_user_test()
        self.trigger_create_user_test(suffix="2")

        self.trigger_create_graph_test()
        self.trigger_traverse_graph_test()
        self.trigger_detach_node_test()
        self.trigger_update_graph_test()

        ###################################################
        #                   VIA DETACH                    #
        ###################################################

        self.nested_count_should_be(node=0, edge=0)

        self.trigger_create_nested_node_test()
        self.nested_count_should_be(node=1, edge=1)

        self.trigger_update_nested_node_test()
        self.trigger_detach_nested_node_test()
        self.nested_count_should_be(node=0, edge=0)

        self.trigger_create_nested_node_test(manual=True)
        self.nested_count_should_be(node=1, edge=1)

        self.trigger_update_nested_node_test(manual=True)
        self.trigger_detach_nested_node_test(manual=True)
        self.nested_count_should_be(node=0, edge=0)

        ###################################################
        #                   VIA DESTROY                   #
        ###################################################

        self.trigger_create_nested_node_test()
        self.nested_count_should_be(node=1, edge=1)

        self.trigger_delete_nested_node_test()
        self.nested_count_should_be(node=0, edge=0)

        self.trigger_create_nested_node_test(manual=True)
        self.nested_count_should_be(node=1, edge=1)

        self.trigger_delete_nested_node_test(manual=True)
        self.nested_count_should_be(node=0, edge=0)

        self.trigger_create_nested_node_test()
        self.nested_count_should_be(node=1, edge=1)

        self.trigger_delete_nested_edge_test()
        self.nested_count_should_be(node=0, edge=0)

        self.trigger_create_nested_node_test(manual=True)
        self.nested_count_should_be(node=1, edge=1)

        # only automatic cleanup remove nodes that doesn't have edges
        # manual save still needs to trigger the destroy for that node
        self.trigger_delete_nested_edge_test(manual=True)
        self.nested_count_should_be(node=1, edge=0)

        self.trigger_access_validation_test(give_access_to_full_graph=False)
        self.trigger_access_validation_test(give_access_to_full_graph=True)

        self.trigger_access_validation_test(
            give_access_to_full_graph=False, via_all=True
        )
        self.trigger_access_validation_test(
            give_access_to_full_graph=True, via_all=True
        )

        ###################################################
        #                  CUSTOM STATUS                  #
        ###################################################

        self.trigger_custom_status_code()

        ###################################################
        #                  CUSTOM REPORT                  #
        ###################################################

        self.trigger_custom_report()

        ###################################################
        #                   FILE UPLOAD                   #
        ###################################################

        self.trigger_upload_file()

        ###################################################
        #                  VISIT SEQUENCE                 #
        ###################################################

        self.trigger_visit_sequence()
