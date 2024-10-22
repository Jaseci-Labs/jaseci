"""JacLang Jaseci Unit Test."""

from os import path
from shelve import open as shelf

from jaclang import jac_import
from jaclang.runtimelib.context import ExecutionContext

from .test_util import JacCloudTest


class SimpleGraphTest(JacCloudTest):
    """JacLang Jaseci Feature Tests."""

    def __init__(self, methodName: str = "runTest") -> None:  # noqa: N803
        """Overide Init."""
        super().__init__(methodName)

        (base, ignored) = path.split(__file__)
        base = base if base else "./"

        jac_import(
            target="simple_graph_mini",
            base_path=base,
            cachable=True,
            override_name="__main__",
        )

    def setUp(self) -> None:
        """Override setUp."""
        self.run_server(
            "jac_cloud/tests/simple_graph_mini.jac",
            port=8001,
            envs={
                "SHOW_ENDPOINT_RETURNS": "true",
            },
            mini=True,
        )

    def tearDown(self) -> None:
        """Override tearDown."""
        self.clear_db()
        self.stop_server()

    def clear_db(self) -> None:
        """Clean DB."""
        with shelf(self.database) as sh:
            sh.clear()
            sh.sync()

    def nested_count_should_be(self, node: int, edge: int) -> None:
        """Test nested node count."""
        jctx = ExecutionContext.create(session=self.database)

        node_count = 0
        edge_count = 0

        for val in jctx.mem.__shelf__.values():
            if val.architype.__class__.__name__ == "Nested":
                node_count += 1
            elif (
                (source := getattr(val, "source", None))
                and (target := getattr(val, "target", None))
                and (
                    source.architype.__class__.__name__ == "Nested"
                    or target.architype.__class__.__name__ == "Nested"
                )
            ):
                edge_count += 1

        self.assertEqual(node, node_count)
        self.assertEqual(edge, edge_count)

        jctx.close()

    def test_all_features(self) -> None:
        """Test Full Features."""
        self.trigger_openapi_specs_test("jac_cloud/tests/openapi_specs_mini.yaml")

        self.trigger_create_graph_test()
        self.trigger_traverse_graph_test()
        self.trigger_detach_node_test()
        self.trigger_update_graph_test()

        ###################################################
        #                   VIA DETACH                    #
        ###################################################

        self.clear_db()

        self.nested_count_should_be(node=0, edge=0)

        self.trigger_create_nested_node_test()
        self.nested_count_should_be(node=1, edge=1)

        self.trigger_update_nested_node_test()
        self.trigger_detach_nested_node_test()
        self.nested_count_should_be(node=0, edge=0)

        ###################################################
        #                   VIA DESTROY                   #
        ###################################################

        self.trigger_create_nested_node_test()
        self.nested_count_should_be(node=1, edge=1)

        self.trigger_delete_nested_node_test()
        self.nested_count_should_be(node=0, edge=0)

        self.trigger_create_nested_node_test()
        self.nested_count_should_be(node=1, edge=1)

        self.trigger_delete_nested_edge_test()
        self.nested_count_should_be(node=0, edge=0)

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
