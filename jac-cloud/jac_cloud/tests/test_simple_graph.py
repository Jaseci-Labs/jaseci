"""JacLang Jaseci Unit Test."""

from httpx import get, post

from yaml import safe_load

from .test_utils import JacCloudTest
from ..jaseci.datasources import Collection


class SimpleGraphTest(JacCloudTest):
    """JacLang Jaseci Feature Tests."""

    def setUp(self) -> None:
        """Override setUp."""
        self.run_server("jac_cloud/tests/simple_graph.jac")

        Collection.__client__ = None
        Collection.__database__ = None
        self.client = Collection.get_client()
        self.q_node = Collection.get_collection("node")
        self.q_edge = Collection.get_collection("edge")

    def tearDown(self) -> None:
        """Override tearDown."""
        self.client.drop_database(self.database)
        self.stop_server()

    def trigger_openapi_specs_test(self) -> None:
        """Test OpenAPI Specs."""
        res = get(f"{self.host}/openapi.yaml", timeout=1)
        res.raise_for_status()

        with open("jac_cloud/tests/openapi_specs.yaml") as file:
            self.assertEqual(safe_load(file), safe_load(res.text))

    def trigger_create_user_test(self, suffix: str = "") -> None:
        """Test User Creation."""
        email = f"user{suffix}@example.com"

        res = post(
            f"{self.host}/user/register",
            json={
                "password": "string",
                "email": email,
                "name": "string",
            },
        )
        res.raise_for_status()
        self.assertEqual({"message": "Successfully Registered!"}, res.json())

        res = post(
            f"{self.host}/user/login",
            json={"email": email, "password": "string"},
        )
        res.raise_for_status()
        body: dict = res.json()

        token = body.get("token")
        self.assertIsNotNone(token)

        user: dict = body.get("user", {})
        self.assertEqual(email, user["email"])
        self.assertEqual("string", user["name"])

        self.users.append(
            {"user": user, "headers": {"Authorization": f"Bearer {token}"}}
        )

    def trigger_create_graph_test(self) -> None:
        """Test Graph Creation."""
        res = self.post_api("create_graph")

        self.assertEqual(200, res["status"])
        self.assertEqual([None], res["returns"])

        root_node = res["reports"].pop(0)
        self.assertTrue(root_node["id"].startswith("n::"))
        self.assertEqual({}, root_node["context"])

        for idx, report in enumerate(res["reports"]):
            self.assertEqual({"val": idx}, report["context"])

    def trigger_traverse_graph_test(self) -> None:
        """Test Graph Traversion."""
        res = self.post_api("traverse_graph")

        self.assertEqual(200, res["status"])
        self.assertEqual([None, None, None, None], res["returns"])

        root_node = res["reports"].pop(0)
        self.assertTrue(root_node["id"].startswith("n::"))
        self.assertEqual({}, root_node["context"])

        for idx, report in enumerate(res["reports"]):
            self.assertEqual({"val": idx}, report["context"])

            res = self.post_api(f"traverse_graph/{report["id"]}")
            self.assertEqual(200, res["status"])
            self.assertEqual([None for i in range(idx, 3)], res["returns"])
            for _idx, report in enumerate(res["reports"]):
                self.assertEqual({"val": idx + _idx}, report["context"])

    def trigger_detach_node_test(self) -> None:
        """Test detach node."""
        res = self.post_api("detach_node")

        self.assertEqual(200, res["status"])
        self.assertEqual([None, None, True], res["returns"])
        self.assertTrue("reports" not in res)

        res = self.post_api("traverse_graph")
        self.assertEqual(200, res["status"])
        self.assertEqual([None, None, None], res["returns"])

        root_node = res["reports"].pop(0)
        self.assertTrue(root_node["id"].startswith("n::"))
        self.assertEqual({}, root_node["context"])

        for idx, report in enumerate(res["reports"]):
            self.assertEqual({"val": idx}, report["context"])

            res = self.post_api(f"traverse_graph/{report["id"]}")
            self.assertEqual(200, res["status"])
            self.assertEqual([None for i in range(idx, 2)], res["returns"])
            for _idx, report in enumerate(res["reports"]):
                self.assertEqual({"val": idx + _idx}, report["context"])

    def trigger_update_graph_test(self) -> None:
        """Test update graph."""
        res = self.post_api("update_graph")

        self.assertEqual(200, res["status"])
        self.assertEqual([None, None, None], res["returns"])

        root_node = res["reports"].pop(0)
        self.assertTrue(root_node["id"].startswith("n::"))
        self.assertEqual({}, root_node["context"])

        for idx, report in enumerate(res["reports"]):
            self.assertEqual({"val": idx + 1}, report["context"])

        res = self.post_api("traverse_graph")

        self.assertEqual(200, res["status"])
        self.assertEqual([None, None, None], res["returns"])

        root_node = res["reports"].pop(0)
        self.assertTrue(root_node["id"].startswith("n::"))
        self.assertEqual({}, root_node["context"])

        for idx, report in enumerate(res["reports"]):
            self.assertEqual({"val": idx + 1}, report["context"])

            res = self.post_api(f"traverse_graph/{report["id"]}")
            self.assertEqual(200, res["status"])
            self.assertEqual([None for i in range(idx, 2)], res["returns"])
            for _idx, report in enumerate(res["reports"]):
                self.assertEqual({"val": idx + _idx + 1}, report["context"])

    def trigger_create_nested_node_test(self, manual: bool = False) -> None:
        """Test create nested node."""
        res = self.post_api(f"{'manual_' if manual else ""}create_nested_node", user=1)

        self.assertEqual(200, res["status"])
        self.assertEqual(
            {
                "val": 0,
                "arr": [],
                "json": {},
                "parent": {
                    "val": 1,
                    "arr": [1],
                    "json": {"a": 1},
                    "child": {
                        "val": 2,
                        "arr": [1, 2],
                        "json": {"a": 1, "b": 2},
                        "enum_field": "C",
                    },
                    "enum_field": "B",
                },
                "enum_field": "A",
            },
            res["returns"][0]["context"],
        )

    def trigger_update_nested_node_test(
        self, manual: bool = False, user: int = 1
    ) -> None:
        """Test update nested node."""
        for walker in [
            f"{'manual_' if manual else ""}update_nested_node",
            "visit_nested_node",
        ]:
            res = self.post_api(walker, user=user)
            self.assertEqual(200, res["status"])
            self.assertEqual(
                {
                    "val": 1,
                    "arr": [1],
                    "json": {"a": 1},
                    "parent": {
                        "val": 2,
                        "arr": [1, 2],
                        "json": {"a": 1, "b": 2},
                        "child": {
                            "val": 3,
                            "arr": [1, 2, 3],
                            "json": {"a": 1, "b": 2, "c": 3},
                            "enum_field": "A",
                        },
                        "enum_field": "C",
                    },
                    "enum_field": "B",
                },
                res["returns"][0]["context"],
            )

    def trigger_detach_nested_node_test(self, manual: bool = False) -> None:
        """Test detach nested node."""
        res = self.post_api(f"{'manual_' if manual else ""}detach_nested_node", user=1)
        self.assertEqual(200, res["status"])
        self.assertEqual([True], res["returns"])

        res = self.post_api("visit_nested_node", user=1)
        self.assertEqual(200, res["status"])
        self.assertEqual([[]], res["returns"])

    def trigger_delete_nested_node_test(self, manual: bool = False) -> None:
        """Test create nested node."""
        res = self.post_api(f"{'manual_' if manual else ""}delete_nested_node", user=1)
        self.assertEqual(200, res["status"])
        self.assertEqual([[]], res["reports"])

        res = self.post_api("visit_nested_node", user=1)
        self.assertEqual(200, res["status"])
        self.assertEqual([[]], res["returns"])

    def trigger_delete_nested_edge_test(self, manual: bool = False) -> None:
        """Test create nested node."""
        res = self.post_api(f"{'manual_' if manual else ""}delete_nested_edge", user=1)
        self.assertEqual(200, res["status"])
        self.assertEqual([[]], res["reports"])

        res = self.post_api("visit_nested_node", user=1)
        self.assertEqual(200, res["status"])
        self.assertEqual([[]], res["returns"])

    def trigger_access_validation_test(
        self, give_access_to_full_graph: bool, via_all: bool = False
    ) -> None:
        """Test giving access to node or full graph."""
        res = self.post_api("create_nested_node", user=1)

        nested_node = res["returns"][0]

        allow_walker_suffix = (
            "" if give_access_to_full_graph else f'/{nested_node["id"]}'
        )

        self.assertEqual(200, res["status"])
        self.assertEqual(
            {
                "val": 0,
                "arr": [],
                "json": {},
                "parent": {
                    "val": 1,
                    "arr": [1],
                    "json": {"a": 1},
                    "child": {
                        "val": 2,
                        "arr": [1, 2],
                        "json": {"a": 1, "b": 2},
                        "enum_field": "C",
                    },
                    "enum_field": "B",
                },
                "enum_field": "A",
            },
            nested_node["context"],
        )

        ###################################################
        #                    NO ACCESS                    #
        ###################################################

        self.assertEqual(
            403,
            self.post_api(f"visit_nested_node/{nested_node['id']}", expect_error=True),
        )

        ###################################################
        #          WITH ALLOWED ROOT READ ACCESS          #
        ###################################################

        res = self.post_api(
            f"allow_other_root_access{allow_walker_suffix}",
            json={
                "root_id": f'n::{self.users[0]["user"]["root_id"]}',
                "via_all": via_all,
            },
            user=1,
        )
        self.assertEqual(200, res["status"])

        res = self.post_api(f"update_nested_node/{nested_node['id']}")
        self.assertEqual(200, res["status"])
        self.assertEqual(
            {
                "val": 1,
                "arr": [1],
                "json": {"a": 1},
                "parent": {
                    "val": 2,
                    "arr": [1, 2],
                    "json": {"a": 1, "b": 2},
                    "child": {
                        "val": 3,
                        "arr": [1, 2, 3],
                        "json": {"a": 1, "b": 2, "c": 3},
                        "enum_field": "A",
                    },
                    "enum_field": "C",
                },
                "enum_field": "B",
            },
            res["returns"][0]["context"],
        )

        # ----------- NO UPDATE SHOULD HAPPEN ----------- #

        res = self.post_api(f"visit_nested_node/{nested_node['id']}")
        self.assertEqual(200, res["status"])
        self.assertEqual(
            {
                "val": 0,
                "arr": [],
                "json": {},
                "parent": {
                    "val": 1,
                    "arr": [1],
                    "json": {"a": 1},
                    "child": {
                        "val": 2,
                        "arr": [1, 2],
                        "json": {"a": 1, "b": 2},
                        "enum_field": "C",
                    },
                    "enum_field": "B",
                },
                "enum_field": "A",
            },
            res["returns"][0]["context"],
        )

        ###################################################
        #          WITH ALLOWED ROOT WRITE ACCESS         #
        ###################################################

        res = self.post_api(
            f"allow_other_root_access{allow_walker_suffix}",
            json={
                "root_id": f'n::{self.users[0]["user"]["root_id"]}',
                "level": "WRITE",
                "via_all": via_all,
            },
            user=1,
        )
        self.assertEqual(200, res["status"])

        res = self.post_api(f"update_nested_node/{nested_node['id']}")
        self.assertEqual(200, res["status"])
        self.assertEqual(
            {
                "val": 1,
                "arr": [1],
                "json": {"a": 1},
                "parent": {
                    "val": 2,
                    "arr": [1, 2],
                    "json": {"a": 1, "b": 2},
                    "child": {
                        "val": 3,
                        "arr": [1, 2, 3],
                        "json": {"a": 1, "b": 2, "c": 3},
                        "enum_field": "A",
                    },
                    "enum_field": "C",
                },
                "enum_field": "B",
            },
            res["returns"][0]["context"],
        )

        # ------------ UPDATE SHOULD REFLECT ------------ #

        res = self.post_api(f"visit_nested_node/{nested_node['id']}")
        self.assertEqual(200, res["status"])
        self.assertEqual(
            {
                "val": 1,
                "arr": [1],
                "json": {"a": 1},
                "parent": {
                    "val": 2,
                    "arr": [1, 2],
                    "json": {"a": 1, "b": 2},
                    "child": {
                        "val": 3,
                        "arr": [1, 2, 3],
                        "json": {"a": 1, "b": 2, "c": 3},
                        "enum_field": "A",
                    },
                    "enum_field": "C",
                },
                "enum_field": "B",
            },
            res["returns"][0]["context"],
        )

        ###################################################
        #                REMOVE ROOT ACCESS               #
        ###################################################

        res = self.post_api(
            f"disallow_other_root_access{allow_walker_suffix}",
            json={
                "root_id": f'n::{self.users[0]["user"]["root_id"]}',
                "via_all": via_all,
            },
            user=1,
        )
        self.assertEqual(200, res["status"])

        self.assertEqual(
            403,
            self.post_api(f"visit_nested_node/{nested_node['id']}", expect_error=True),
        )

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

    def trigger_custom_status_code(self) -> None:
        """Test custom status code."""
        for acceptable_code in [200, 201, 202, 203, 205, 206, 207, 208, 226]:
            res = self.post_api("custom_status_code", {"status": acceptable_code})
            self.assertEqual(acceptable_code, res["status"])
            self.assertEqual([None], res["returns"])

        for error_code in [
            400,
            401,
            402,
            403,
            404,
            405,
            406,
            407,
            408,
            409,
            410,
            411,
            412,
            413,
            414,
            415,
            416,
            417,
            418,
            421,
            422,
            423,
            424,
            425,
            426,
            428,
            429,
            431,
            451,
            500,
            501,
            502,
            503,
            504,
            505,
            506,
            507,
            508,
            510,
            511,
        ]:
            self.assertEqual(
                error_code,
                self.post_api(
                    "custom_status_code", {"status": error_code}, expect_error=True
                ),
            )

        for invalid_code in [
            100,
            101,
            102,
            103,
            204,
            300,
            301,
            302,
            303,
            304,
            305,
            306,
            307,
            308,
        ]:
            self.assertRaises(
                Exception, self.post_api, "custom_status_code", {"status": invalid_code}
            )

    def trigger_custom_report(self) -> None:
        """Test custom status code."""
        res = self.post_api("custom_report")
        self.assertEqual({"testing": 1}, res)

    def trigger_upload_file(self) -> None:
        """Test upload file."""
        with open("jac_cloud/tests/simple_graph.jac", mode="br") as s:
            files = [
                ("single", ("simple_graph.jac", s)),
                ("multiple", ("simple_graph.jac", s)),
                ("multiple", ("simple_graph.jac", s)),
            ]
            res = post(
                f"{self.host}/walker/post_with_file",
                files=files,
                headers=self.users[0]["headers"],
            )
            res.raise_for_status()
            data: dict = res.json()

            self.assertEqual(200, data["status"])
            self.assertEqual([None], data["returns"])
            self.assertEqual(
                [
                    {
                        "single": {
                            "single": {
                                "name": "simple_graph.jac",
                                "content_type": "application/octet-stream",
                                "size": 17658,
                            }
                        },
                        "multiple": [
                            {
                                "name": "simple_graph.jac",
                                "content_type": "application/octet-stream",
                                "size": 17658,
                            },
                            {
                                "name": "simple_graph.jac",
                                "content_type": "application/octet-stream",
                                "size": 17658,
                            },
                        ],
                        "singleOptional": None,
                    }
                ],
                data["reports"],
            )

    def trigger_reset_graph(self) -> None:
        """Test custom status code."""
        res = self.post_api("populate_graph", user=2)
        self.assertEqual(200, res["status"])
        self.assertEqual([None] * 31, res["returns"])

        res = self.post_api("traverse_populated_graph", user=2)
        self.assertEqual(200, res["status"])
        self.assertEqual([None] * 63, res["returns"])
        reports = res["reports"]

        root = reports.pop(0)
        self.assertTrue(root["id"].startswith("n::"))
        self.assertEqual({}, root["context"])

        cur = 0
        max = 2
        for node in ["D", "E", "F", "G", "H"]:
            for idx in range(cur, cur + max):
                self.assertTrue(reports[idx]["id"].startswith(f"n:{node}:"))
                self.assertEqual({"id": idx % 2}, reports[idx]["context"])
                cur += 1
            max = max * 2

        res = self.post_api("check_populated_graph", user=2)
        self.assertEqual(200, res["status"])
        self.assertEqual([None], res["returns"])
        self.assertEqual([125], res["reports"])

        res = self.post_api("purge_populated_graph", user=2)
        self.assertEqual(200, res["status"])
        self.assertEqual([None], res["returns"])
        self.assertEqual([124], res["reports"])

        res = self.post_api("check_populated_graph", user=2)
        self.assertEqual(200, res["status"])
        self.assertEqual([None], res["returns"])
        self.assertEqual([1], res["reports"])

    def trigger_memory_sync(self) -> None:
        """Test memory sync."""
        res = self.post_api("traverse_graph")

        self.assertEqual(200, res["status"])
        self.assertEqual([None, None, None], res["returns"])

        a_node = res["reports"].pop(1)
        self.assertTrue(a_node["id"].startswith("n:A:"))
        self.assertEqual({"val": 1}, a_node["context"])

        res = self.post_api(
            "check_memory_sync", json={"other_node_id": a_node["id"]}, user=1
        )
        self.assertEqual(200, res["status"])

    def trigger_create_custom_object_test(self) -> str:
        """Test create custom object."""
        res = self.post_api("create_custom_object", user=1)
        obj = res["reports"][0]

        self.assertEqual(200, res["status"])
        self.assertTrue(obj["id"].startswith("o:SavableObject:"))
        self.assertEqual(
            {
                "val": 0,
                "arr": [],
                "json": {},
                "parent": {
                    "val": 1,
                    "arr": [1],
                    "json": {"a": 1},
                    "child": {
                        "val": 2,
                        "arr": [1, 2],
                        "json": {"a": 1, "b": 2},
                        "enum_field": "C",
                    },
                    "enum_field": "B",
                },
                "enum_field": "A",
            },
            obj["context"],
        )

        res = self.post_api("get_custom_object", json={"object_id": obj["id"]}, user=1)
        obj = res["reports"][0]

        self.assertEqual(200, res["status"])
        self.assertTrue(obj["id"].startswith("o:SavableObject:"))
        self.assertEqual(
            {
                "val": 0,
                "arr": [],
                "json": {},
                "parent": {
                    "val": 1,
                    "arr": [1],
                    "json": {"a": 1},
                    "child": {
                        "val": 2,
                        "arr": [1, 2],
                        "json": {"a": 1, "b": 2},
                        "enum_field": "C",
                    },
                    "enum_field": "B",
                },
                "enum_field": "A",
            },
            obj["context"],
        )

        return obj["id"]

    def trigger_update_custom_object_test(self, obj_id: str) -> None:
        """Test update custom object."""
        res = self.post_api("update_custom_object", json={"object_id": obj_id}, user=1)
        obj = res["reports"][0]

        self.assertEqual(200, res["status"])
        self.assertTrue(obj["id"].startswith("o:SavableObject:"))
        self.assertEqual(
            {
                "val": 1,
                "arr": [1],
                "json": {"a": 1},
                "parent": {
                    "val": 2,
                    "arr": [1, 2],
                    "json": {"a": 1, "b": 2},
                    "child": {
                        "val": 3,
                        "arr": [1, 2, 3],
                        "json": {"a": 1, "b": 2, "c": 3},
                        "enum_field": "A",
                    },
                    "enum_field": "C",
                },
                "enum_field": "B",
            },
            obj["context"],
        )

        res = self.post_api("get_custom_object", json={"object_id": obj_id}, user=1)
        obj = res["reports"][0]

        self.assertEqual(200, res["status"])
        self.assertTrue(obj["id"].startswith("o:SavableObject:"))
        self.assertEqual(
            {
                "val": 1,
                "arr": [1],
                "json": {"a": 1},
                "parent": {
                    "val": 2,
                    "arr": [1, 2],
                    "json": {"a": 1, "b": 2},
                    "child": {
                        "val": 3,
                        "arr": [1, 2, 3],
                        "json": {"a": 1, "b": 2, "c": 3},
                        "enum_field": "A",
                    },
                    "enum_field": "C",
                },
                "enum_field": "B",
            },
            obj["context"],
        )

    def trigger_delete_custom_object_test(self, obj_id: str) -> None:
        """Test delete custom object."""
        res = self.post_api("delete_custom_object", json={"object_id": obj_id}, user=1)
        self.assertEqual(200, res["status"])

        res = self.post_api("get_custom_object", json={"object_id": obj_id}, user=1)
        obj = res["reports"][0]

        self.assertEqual(200, res["status"])
        self.assertIsNone(obj)

    def test_all_features(self) -> None:
        """Test Full Features."""
        self.trigger_openapi_specs_test()

        self.trigger_create_user_test()
        self.trigger_create_user_test(suffix="2")
        self.trigger_create_user_test(suffix="3")

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
        #                   TEST PURGER                   #
        ###################################################

        self.trigger_reset_graph()

        ###################################################
        #                 TEST MEMORY SYNC                #
        ###################################################

        self.trigger_memory_sync()

        ##################################################
        #                 SAVABLE OBJECT                  #
        ###################################################

        obj_id = self.trigger_create_custom_object_test()
        self.trigger_update_custom_object_test(obj_id)
        self.trigger_delete_custom_object_test(obj_id)
