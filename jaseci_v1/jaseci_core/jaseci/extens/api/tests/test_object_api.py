from jaseci.utils.test_core import CoreTest


class ObjectApiTest(CoreTest):
    """Unit tests for Jac Walker APIs"""

    fixture_src = __file__

    def test_object_set(self):
        ret = self.call(
            self.mast,
            [
                "object_set",
                {"obj": self.mast.jid, "ctx": {"name": "MYNEWNAME", "jid": "MYNEWJID"}},
            ],
        )
        self.assertEqual(ret["name"], "MYNEWNAME")
        self.assertNotEqual(ret["jid"], "MYNEWJID")
        self.assertEqual(self.mast.name, "MYNEWNAME")
        self.assertNotEqual(self.mast.jid, "MYNEWJID")
