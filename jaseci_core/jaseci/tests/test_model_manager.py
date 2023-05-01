import unittest
import tempfile
import shutil
from jaseci.utils.model_manager import ModelManager
from pathlib import Path


class ModelManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.manager = ModelManager(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_get_save_path_creates_directory(self):
        save_path = self.manager.get_save_path()
        self.assertTrue(save_path.exists())

    def test_get_save_path_returns_different_paths(self):
        save_path_1 = self.manager.get_save_path()
        save_path_2 = self.manager.get_save_path()
        self.assertNotEqual(save_path_1, save_path_2)

    def test_get_load_path_returns_correct_path(self):
        save_path = self.manager.get_save_path()
        load_path = self.manager.get_load_path()
        self.assertEqual(Path(save_path), Path(load_path))

    def test_delete_model_removes_directory(self):
        save_path = self.manager.get_save_path()
        self.manager.delete_model(save_path.name)
        self.assertFalse(save_path.exists())

    def test_get_version_ids_returns_version_names_in_order(self):
        self.manager.get_save_path()
        self.manager.get_save_path()
        version_ids = self.manager.get_version_ids()
        self.assertEqual(list(version_ids.values()), [1, 2])

    def test_get_latest_version_returns_latest_version(self):
        save_path = self.manager.get_save_path()
        self.assertEqual(self.manager.get_latest_version(), save_path.name)

    def test_set_latest_version_changes_latest_version(self):
        save_path_1 = self.manager.get_save_path()
        save_path_2 = self.manager.get_save_path()
        self.manager.set_latest_version(save_path_1.name)
        self.assertEqual(self.manager.get_latest_version(), save_path_1.name)

    def test_cleanup_old_versions_removes_old_versions(self):
        self.manager.get_save_path()
        self.manager.get_save_path()
        self.manager.cleanup_old_versions(retention_count=1)
        version_ids = self.manager.get_version_ids()
        self.assertEqual(len(version_ids), 1)
