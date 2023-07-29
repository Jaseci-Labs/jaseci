from jaseci.utils.test_core import CoreTest
from unittest.mock import patch
from io import BufferedReader


class FileTest(CoreTest):
    """Unit tests for Jac Walker APIs"""

    fixture_src = __file__

    def setUp(self):
        super().setUp()

    def tearDown(self):
        self.mast._h.clean_file_handler()
        super().tearDown()

    def call_walker(self, name, report=True):
        res = self.call(
            self.mast,
            [
                "walker_run",
                {"name": name, "ctx": {}},
            ],
        )

        self.assertTrue(res["success"])
        return res["report"] if report else res

    def test_file_syntax(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("file.jac")}],
        )

        reps = self.call_walker("new_file")
        self.assertEqual("", reps[1])
        self.assertEqual("", reps[2])
        self.assertEqual("0", reps[3])
        self.assertEqual("00", reps[4])
        self.assertEqual("MDA=", reps[5])
        self.assertTrue(reps[6])
        self.assertFalse(reps[7])

        reps = self.call_walker("json_file")
        self.assertEqual({"testing": 1}, reps[0])
        self.assertTrue(reps[1])
        self.assertFalse(reps[2])

        reps = self.call_walker("download_file")
        uuid = reps[0]
        self.assertEqual(
            {
                "id": f"{uuid}",
                "name": "tmp",
                "content_type": None,
                "field": None,
                "absolute_name": f"{uuid}-tmp",
                "absolute_path": f"/tmp/{uuid}-tmp",
                "persist": False,
            },
            reps[1],
        )

        reps = self.call_walker("download_file")
        uuid = reps[0]
        self.assertEqual(
            {
                "id": f"{uuid}",
                "name": "tmp",
                "content_type": None,
                "field": None,
                "absolute_name": f"{uuid}-tmp",
                "absolute_path": f"/tmp/{uuid}-tmp",
                "persist": False,
            },
            reps[1],
        )

        reps = self.mast._h.get_file_handler(
            self.call_walker("return_any_file", False)["report_file"]
        ).attr()
        uuid = reps["id"]
        self.assertEqual(
            {
                "id": f"{uuid}",
                "name": "tmp",
                "content_type": None,
                "field": None,
                "absolute_name": f"{uuid}-tmp",
                "absolute_path": f"/tmp/{uuid}-tmp",
                "persist": False,
            },
            reps,
        )

        reps = self.mast._h.get_file_handler(
            self.call_walker("return_any_file_with_name", False)["report_file"]
        ).attr()
        uuid = reps["id"]
        self.assertEqual(
            {
                "id": f"{uuid}",
                "name": "jaseci_bible.pdf",
                "content_type": "application/pdf",
                "field": None,
                "absolute_name": f"{uuid}-tmp",
                "absolute_path": f"/tmp/{uuid}-tmp",
                "persist": False,
            },
            reps,
        )

    @patch("requests.post")
    def test_manual_upload_file(self, mock_post):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("file.jac")}],
        )

        self.call_walker("manual_upload_file")
        self.assertTrue(mock_post.called)
        args, kwargs = mock_post.call_args
        self.assertEqual(1, len(args))
        self.assertEqual("https://sample/com", args[0])
        self.assertEqual({"test": 1}, kwargs["data"])
        self.assertEqual({"test": 2}, kwargs["headers"])
        self.assertEqual("file", kwargs["files"][0][0])
        self.assertEqual("tmp", kwargs["files"][0][1][0])
        self.assertIsInstance(kwargs["files"][0][1][1], BufferedReader)
        self.assertIsNone(kwargs["files"][0][1][2])
