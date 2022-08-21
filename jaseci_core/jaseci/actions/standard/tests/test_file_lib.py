from jaseci.utils.test_core import core_test


class file_lib_test(core_test):

    fixture_src = __file__

    def test_json_dump(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("file_stuff.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "pack_it"}])
        self.assertEqual(ret["report"][0], {"hello": 5})
