from jaseci.jsorc.jsorc import JsOrc
from jaseci.extens.svc.elastic_svc import ElasticService
from jaseci.utils.test_core import CoreTest


class ElasticTest(CoreTest):
    """Unit tests for Jac Walker APIs"""

    fixture_src = __file__

    def setUp(self):
        super().setUp()

    @JsOrc.inject(services=["elastic"])
    def test_elastic(self, elastic: ElasticService):
        if not elastic.is_running():
            self.skipTest("Elastic is not available!")

        res = self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("elastic.jac")}],
        )

        res = self.call(
            self.mast,
            [
                "walker_run",
                {"name": "test_activity", "ctx": {"a": 1, "b": 2, "c": 3}},
            ],
        )

        # report std.log_activity({"other_field": 1}, action = "CUSTOM_ACTION_NAME");
        self.assertEqual("created", res["report"][0]["result"])

        # report std.log_activity({"other_field": 2}, action = "CUSTOM_ACTION_NAME", suffix="-sample-id");
        self.assertEqual("created", res["report"][1]["result"])

        # report elastic.doc_activity({"testing": "doc_activity"});
        self.assertEqual("created", res["report"][2]["result"])

        # report elastic.search_activity({});
        hits = res["report"][3]["hits"]

        self.assertEqual(2, hits["total"]["value"])
        self.assertEqual({"a": 1, "b": 2, "c": 3}, hits["hits"][0]["_source"]["data"])
        self.assertEqual(1, hits["hits"][0]["_source"].get("other_field"))
        self.assertEqual({"testing": "doc_activity"}, hits["hits"][1]["_source"])

        # report elastic.search_activity({}, suffix="-sample-id");
        hits = res["report"][4]["hits"]

        self.assertEqual(1, hits["total"]["value"])
        self.assertEqual({"a": 1, "b": 2, "c": 3}, hits["hits"][0]["_source"]["data"])
        self.assertEqual(2, hits["hits"][0]["_source"].get("other_field"))

        # report elastic.mapping_activity();
        mapping: dict = res["report"][5]
        for key, value in mapping.items():
            self.assertTrue(key.endswith("-activity"))
            self.assertTrue(key.startswith("jaseci-"))
            self.assertTrue(value["mappings"])

        # report elastic.mapping_activity(suffix="-sample-id");
        mapping: dict = res["report"][6]
        for key, value in mapping.items():
            self.assertTrue(key.endswith("-activity-sample-id"))
            self.assertTrue(key.startswith("jaseci-"))
            self.assertTrue(value["mappings"])

        res = self.call(
            self.mast,
            [
                "walker_run",
                {"name": "test_common", "ctx": {"d": 1, "e": 2, "f": 3}},
            ],
        )

        # report elastic.doc({"testing": "doc"});
        self.assertEqual("created", res["report"][0]["result"])

        # elastic.doc({"testing": "doc-other-index"}, index="other-index");
        self.assertEqual("created", res["report"][1]["result"])

        # elastic.doc({"testing": "doc-other-index"}, index="other-index", suffix="-user-id");
        self.assertEqual("created", res["report"][2]["result"])

        # report elastic.search({});
        hits = res["report"][3]["hits"]

        self.assertEqual(1, hits["total"]["value"])
        self.assertEqual({"testing": "doc"}, hits["hits"][0]["_source"])

        # elastic.search({}, index="other-index");
        hits = res["report"][4]["hits"]

        self.assertEqual(1, hits["total"]["value"])
        self.assertEqual({"testing": "doc-other-index"}, hits["hits"][0]["_source"])

        # elastic.search({}, index="other-index", suffix="-user-id");
        hits = res["report"][5]["hits"]

        self.assertEqual(1, hits["total"]["value"])
        self.assertEqual(
            {"testing": "doc-other-index-suffix"}, hits["hits"][0]["_source"]
        )

        # report elastic.mapping();
        mapping: dict = res["report"][6]
        for key, value in mapping.items():
            self.assertTrue(key.endswith("-common"))
            self.assertTrue(key.startswith("jaseci-"))
            self.assertTrue(value["mappings"])

        # report elastic.mapping(index="other-index");
        mapping: dict = res["report"][7]
        for key, value in mapping.items():
            self.assertEqual(key, "other-index")
            self.assertTrue(value["mappings"])

        # report elastic.mapping(index="other-index", suffix="-user-id");
        mapping: dict = res["report"][8]
        for key, value in mapping.items():
            self.assertEqual(key, "other-index-user-id")
            self.assertTrue(value["mappings"])

        res = self.call(
            self.mast,
            [
                "walker_run",
                {"name": "test_other", "ctx": {}},
            ],
        )

        # report elastic.reindex
        self.assertEqual(1, res["report"][0]["created"])

        # report elastic.aliases();
        aliases: dict = res["report"][1]
        self.assertEqual(6, len(aliases.keys()))
        self.assertTrue(aliases.pop("other-index"))
        self.assertTrue(aliases.pop("other-index-user-id"))
        self.assertTrue(aliases.pop("new-index"))
        for key in list(aliases.keys()):
            if key.startswith("jaseci-"):
                if (
                    key.endswith("-activity")
                    or key.endswith("-common")
                    or key.endswith("-activity-sample-id")
                ):
                    self.assertTrue(aliases.pop(key))
        self.assertFalse(aliases)

        # report elastic.search({}, index="new-index");
        hits = res["report"][2]["hits"]

        self.assertEqual(1, hits["total"]["value"])
        self.assertEqual(
            {"testing": "doc-other-index-suffix"}, hits["hits"][0]["_source"]
        )
