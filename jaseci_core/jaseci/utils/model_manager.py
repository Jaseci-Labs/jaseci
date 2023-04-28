from typing import Optional
from pathlib import Path
import os
import shutil
import uuid
import json

DEFAULT_MODEL_RETENTION = 10


class ModelManager:
    def __init__(self, model_dir: str):
        self.model_dir = Path(model_dir)

        if not self.model_dir.exists():
            self.model_dir.mkdir(parents=True)

        self.metadata_file = self.model_dir / "metadata.json"
        if self.metadata_file.exists():
            with open(self.metadata_file, "r") as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {
                "latest_version": "",
                "version_table": {},
                "version_count": 0,
            }
            self.save_metadata()

    def save_metadata(self):
        with open(self.metadata_file, "w") as f:
            json.dump(self.metadata, f)

    def get_save_path(self, version_id: Optional[str] = None):
        if version_id is None:
            version_id = str(uuid.uuid4())
        save_path = self.model_dir / version_id
        os.makedirs(save_path, exist_ok=True)
        self.metadata["version_table"][version_id] = str(save_path)
        self.metadata["version_count"] += 1
        self.metadata["latest_version"] = version_id
        self.save_metadata()
        self.cleanup_old_versions()
        return save_path

    def get_load_path(self, version_id: Optional[str] = None):
        if version_id is None:
            version_id = self.metadata["latest_version"]
        load_path = self.metadata["version_table"][version_id]
        return load_path

    def delete_model(self, version_id: str):
        model_path = self.metadata["version_table"][version_id]
        shutil.rmtree(model_path)
        del self.metadata["version_table"][version_id]
        self.metadata["version_count"] -= 1
        if version_id == self.metadata["latest_version"]:
            self.metadata["latest_version"] = ""
        self.save_metadata()

    def get_version_ids(self):
        version_ids = sorted(
            self.metadata["version_table"].keys(),
            key=lambda x: os.stat(self.metadata["version_table"][x]).st_ctime,
        )
        version_id_with_idx = {}
        for idx, version_id in enumerate(version_ids):
            version_id_with_idx[version_id] = idx + 1
        return version_id_with_idx

    def get_latest_version(self):
        return self.metadata["latest_version"]

    def set_latest_version(self, version_id: Optional[str] = None):
        if version_id is None:
            self.metadata["latest_version"] = ""
        else:
            self.metadata["latest_version"] = version_id
        self.save_metadata()
        return self.metadata["latest_version"]

    def cleanup_old_versions(self, retention_count: Optional[int] = None):
        if retention_count is None:
            retention_count = DEFAULT_MODEL_RETENTION
        if self.metadata["version_count"] <= retention_count:
            return
        version_names = sorted(
            self.metadata["version_table"].keys(),
            key=lambda x: os.stat(self.metadata["version_table"][x]).st_ctime,
        )
        for version_id in version_names[:-retention_count]:
            self.delete_model(version_id)
