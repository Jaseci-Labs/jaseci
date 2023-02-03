from jaseci.utils.test_core import CoreTest
import os


class FileLibTest(CoreTest):
    fixture_src = __file__

    def test_json_dump(self):
        ret = self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("file_stuff.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "pack_it"}])
        self.assertEqual(ret["report"][0], {"hello": 5})

    def test_bin_load_save(self):
        ret = self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("file_stuff.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "bin_load_save"}])
        self.assertEqual(
            ret["report"][0],
            "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEX"
            "///+/v7+jQ3Y5AAAADklEQVQI12P4AIX8EAgALgAD/aNpbtEAAAAASUVORK5CYII=",
        )
        self.assertFalse(os.path.exists("file.gif"))

    def test_kwargs_bin_load_save(self):
        ret = self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("file_stuff.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "kwargs_bin_load_save"}])
        self.assertEqual(
            ret["report"][0],
            "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEX"
            "///+/v7+jQ3Y5AAAADklEQVQI12P4AIX8EAgALgAD/aNpbtEAAAAASUVORK5CYII=",
        )
        self.assertFalse(os.path.exists("file.gif"))
