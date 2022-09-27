from jaseci.utils.test_core import CoreTest


class FileLibTest(CoreTest):

    fixture_src = __file__

    def test_json_dump(self):
        self.logger_on()
        ret = self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("file_stuff.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "pack_it"}])
        self.assertEqual(ret["report"][0], {"hello": 5})
